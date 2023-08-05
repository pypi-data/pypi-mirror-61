#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""The actual brick runner"""

import asyncio
from datetime import datetime, timedelta

import titanfe.log as logging

from titanfe.utils import cancel_tasks
from titanfe.messages import BrickDescription

from .controlpeer import ControlPeer
from .input import Input
from .metrics import MetricEmitter
from .output import Output
from .brick import Brick
from .packet import Packet


class BrickRunner:
    """The BrickRunner will create an Input, get an Assignment from the control peer,
       create corresponding outputs and then start processing packets from the input.

    Arguments:
        uid (str): a unique id for the runner
        controlpeer_address (NetworkAddress): (host, port) of the control peer's server
        kafka_bootstrap_servers (str):
            'host[:port]' string (or list of 'host[:port]' strings)
            to contact the Kafka bootstrap servers on
    """

    def __init__(self, uid, controlpeer_address, kafka_bootstrap_servers):
        self.uid = uid
        self.log = logging.getLogger(f"{__name__}.{self.uid}")
        self.loop = asyncio.get_event_loop()
        self.kafka_bootstrap_servers = kafka_bootstrap_servers

        cp_host, cp_port = controlpeer_address.rsplit(":", 1)
        self.cp_address = cp_host, int(cp_port)

        # done async in setup
        self.input = None
        self.output = None
        self.control_peer = None
        self.brick = None

        self.setup_completed = asyncio.Event()

        self.metric_emitter = None
        self.tasks = []

    @classmethod
    async def create(cls, uid, controlpeer_address, kafka_bootstrap_servers):
        """Creates a brick runner instance and does the initial setup phase before returning it"""
        br = cls(uid, controlpeer_address, kafka_bootstrap_servers)  # pylint: disable=invalid-name
        await br.setup()
        return br

    async def setup(self):
        """does the inital setup parts that have to be awaited"""
        self.metric_emitter = await MetricEmitter.create_from_brick_runner(self)
        self.input = Input(self)
        self.output = await Output.create_from_brick_runner(self)

        self.control_peer = ControlPeer.create_from_brick_runner(self)

        assignment = await self.control_peer.request_assignment(self.output.address)
        brick, input_sources, output_targets = assignment

        self.brick = Brick(BrickDescription(*brick), self.metric_emitter, self.log)
        self.input.add_sources(input_sources)

        if output_targets:
            self.output.add_targets(output_targets, self.control_peer.send_slow_queue_alert)
            self.tasks.append(asyncio.create_task(self.output_results()))

        self.setup_completed.set()

    async def run(self):
        """process items from the input"""
        self.log.info("start runner: %s", self.uid)

        if self.brick.is_inlet:
            # trigger processing
            await self.input.put(Packet())

        if not self.brick.is_inlet:
            self.tasks.append(asyncio.create_task(self.exit_when_idle()))

        await self.process_input()
        await self.shutdown()
        self.log.info("Exit")

    async def process_input(self):
        with self.brick:
            async for packet in self.input:
                packet.update_input_exit()
                self.log.debug("process packet: %s", packet)
                await self.brick.process(packet)

    async def stop_processing(self):
        """stop processing bricks"""
        self.log.info("Stop Processing")
        await self.input.close()
        self.brick.terminate()
        await self.output.close()

    async def shutdown(self):
        """shuts down the brick runner"""
        self.log.info("Initiating Shutdown")
        await cancel_tasks(self.tasks, wait_cancelled=True)
        await self.metric_emitter.stop()
        await self.control_peer.disconnect()
        self.log.info("Shutdown sequence complete - should exit soon")

    async def output_results(self):
        """get results from the brick execution and add them to the output queues of this runner"""
        async for packet, port in self.brick.get_results():
            await self.output[port].enqueue(packet)

    @property
    def is_idle(self):
        return self.input.is_empty and self.output.is_empty and not self.brick.is_processing

    async def exit_when_idle(self):
        """Schedule as task to initiate shutdown if the configured maximum idle time is reached"""

        # check at least once per second:
        interval = min(self.brick.exit_after_idle_seconds * 0.1, 1)

        idle_since = None
        idle_time = timedelta(seconds=0)
        max_idle_time = timedelta(seconds=self.brick.exit_after_idle_seconds)

        while idle_time <= max_idle_time:
            await asyncio.sleep(interval)

            if not self.is_idle:
                idle_since = None
                continue

            if idle_since is None:
                idle_since = datetime.now()
                continue

            idle_time = datetime.now() - idle_since

        self.log.warning("Max idle time reached. Scheduling shutdown")
        await self.stop_processing()
