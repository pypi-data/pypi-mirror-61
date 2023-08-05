#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""The output with it's server and ports"""

import asyncio
from itertools import chain

from titanfe.connection import Connection
from titanfe.messages import OutputTarget
from titanfe.utils import get_ip_address

from .port import Port
from .consumer import Consumer
from ..metrics import QueueWithMetrics


class Output:
    """The output side of a brick runner creates a Server.
       It will then send packets as requested by the following inputs.

    Arguments:
        runner (BrickRunner): instance of a parent brick runner
        name (str): a name for the output destination
        address (NetworkAddress): the network address of the output server
    """

    def __init__(self, logger, runner_setup_completed, create_output_queue):
        self.log = logger.getChild("Output")
        self.runner_setup_completed = runner_setup_completed
        self.create_queue = create_output_queue

        self.server = None
        self.address = None

        self.ports = {}

    def __iter__(self):
        return iter(self.ports.values())

    def __getitem__(self, port_name):
        return self.ports[port_name]

    @classmethod
    async def create_from_brick_runner(cls, runner):
        """Creates a new instance"""

        def create_new_queue(name):
            return QueueWithMetrics(runner.metric_emitter, name)

        output = cls(runner.log, runner.setup_completed, create_new_queue)

        await output.start_server()
        return output

    async def start_server(self):
        """start server"""
        self.server = await asyncio.start_server(self.register_new_consumer, host=get_ip_address())
        self.address = self.server.sockets[0].getsockname()

    def add_targets(self, targets, slow_queue_alert_cb):
        for target in targets:
            self.add_target(OutputTarget(*target), slow_queue_alert_cb)

    def add_target(self, target, slow_queue_alert_cb):
        """add a configured output target"""
        target_name, port_name, autoscale_queue_level = target
        try:
            port = self.ports[port_name]
        except KeyError:
            port = self.ports[port_name] = Port(port_name)

        port.add_consumer_group(
            target_name, self.create_queue(target_name), autoscale_queue_level, slow_queue_alert_cb
        )

    async def register_new_consumer(self, reader, writer):
        """create consumers for incoming connections and dispatch the connection to them"""
        await self.runner_setup_completed.wait()

        connection = Connection(reader, writer, self.log)
        message = await connection.receive()
        brick_name, port = message.content

        self[port].add_consumer(Consumer(port, brick_name, connection))

    async def close(self):
        """close all connections and the server itself"""
        if self.ports:
            await asyncio.wait({port.close() for port in self})
        if self.server:
            self.server.close()
            await self.server.wait_closed()

    @property
    def consumer_groups(self):
        return chain.from_iterable(self)

    @property
    def is_empty(self):
        """True, if no packets are waiting to be outputted"""
        return not any(group.has_unfinished_business for group in self.consumer_groups)
