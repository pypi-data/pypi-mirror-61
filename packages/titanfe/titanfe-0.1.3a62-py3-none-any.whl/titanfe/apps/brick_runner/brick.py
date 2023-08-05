#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

""" A Brick within the brick runner """
import asyncio
import time

import janus

from titanfe.constants import DEFAULT_PORT
from titanfe.utils import get_module, time_delta_in_ms, Flag
from titanfe.brick import LegacyBrick, InletBrickBase

from .adapter import BrickAdapter


class Brick:
    """Wraps all the Brick-Handling"""

    def __init__(self, brick_description, metric_emitter, logger):
        self.metric_emitter = metric_emitter
        self.log = logger.getChild("Brick")

        self.flowname = brick_description.flowname
        self.name = brick_description.name
        self.uid = brick_description.uid
        self.is_inlet = brick_description.is_inlet
        self.exit_after_idle_seconds = brick_description.exit_after_idle_seconds

        self.module = get_module(brick_description.path_to_module)

        self.results = janus.Queue()
        self.adapter = BrickAdapter(self.name, self.results.sync_q.put, self.log)
        self.parameters = brick_description.parameters
        self.instance = None

        self.last_execution_start = None
        self.is_processing = Flag()

    def create_instance(self):
        """create an instance of the actual Brick"""
        try:
            self.instance = self.module.Brick(self.adapter, self.parameters)
        except AttributeError:
            self.log.debug(
                "Module has no 'Brick' "
                ", must implement 'do_brick_processing'"
                "- create a LegacyBrick"
            )

            self.instance = LegacyBrick(self.adapter, self.parameters, self.module)

    def terminate(self):
        if isinstance(self.instance, (InletBrickBase, LegacyBrick)):
            self.instance.stop_processing()

    def __enter__(self):
        self.create_instance()
        self.instance.setup()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.instance.teardown()
        self.instance = None

    async def get_results(self):
        """async generator over the results from the brick"""
        queue = self.results.async_q

        while not (queue.closed and queue.empty()):
            packet, port = await queue.get()
            await self.metric_emitter.emit_packet_metrics(packet, self.execution_time)
            queue.task_done()
            yield packet, port

        raise StopAsyncIteration

    @property
    def execution_time(self):
        return time_delta_in_ms(self.last_execution_start)

    async def process(self, packet):
        with self.is_processing:
            await self.execute_brick(packet)

    async def execute_brick(self, packet):
        """run the brick module for the given packet in a separate thread"""
        self.log.info(
            "(%s) execute Brick: %s(%s) for %r", self.flowname, self.name, self.uid, packet
        )

        self.last_execution_start = time.time_ns()

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.run_instance_processing, packet.payload)
        if result:
            port = DEFAULT_PORT
            if not isinstance(result, tuple):
                packet.payload = result
            else:
                try:
                    packet.payload, port = result
                except ValueError:
                    raise ValueError("Invalid brick result ")
            await self.results.async_q.put((packet, port))

        await self.results.async_q.join()
        await self.metric_emitter.emit_brick_metrics(self.execution_time)

    def run_instance_processing(self, payload):
        """do the actual execution of the brick module and return it's result"""
        try:
            return self.instance.process(payload)
        except Exception:  # pylint: disable=broad-except
            self.log.error("brick execution failed", exc_info=True)
            return None
