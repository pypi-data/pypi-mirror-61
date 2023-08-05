#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""the actual control peer"""

import asyncio
import signal


import titanfe.log as logging
from titanfe.connection import Connection
from titanfe.utils import Flag
from .flow_director import FlowDirector
from .webapi import WebApi
from .flow import create_flows

log = logging.getLogger(__name__)


class ControlPeer:
    """The control peer application will start runners as required for the flows/bricks
       as described in the given config file. Once the runners have registered themselves,
       they will get according assignments.

    Arguments:
        brick_config (Path): path to the brick config yaml

        kafka_bootstrap_servers (str):
            'host[:port]' string (or list of 'host[:port]' strings)
            to contact the Kafka bootstrap servers on
    """

    def __init__(self, brick_config, kafka_bootstrap_servers):
        self.loop = asyncio.get_event_loop()
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.brick_config = brick_config
        self.flows = []
        self.flows_by_name = {}
        self.runners = {}
        self.runner_connections = {}

        self.server = None
        self.server_address = None
        self.webapi = None
        self.flow_director = None
        self.exit = Flag()

    @classmethod
    async def create(cls, brick_config, flow_director_address, kafka_bootstrap_servers):
        control_peer = cls(brick_config, kafka_bootstrap_servers)
        await control_peer.setup(flow_director_address)
        return control_peer

    async def setup(self, flow_director_address):
        """setup ControlPeer
        Arguments:
            flow_director_address : server address of the FlowDirector
        """
        await self.setup_runner_communication()
        self.setup_webapi()
        self.flow_director = FlowDirector(flow_director_address)

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    async def run(self):
        """run the application"""
        log.debug("running control peer")

        try:
            await self.flow_director.register(self.webapi.address)
        except Exception:   # pylint: disable=broad-except
            log.warning("Failed to register, shutting down.")
            return await self.shutdown()

        flow_config = await self.flow_director.get_flow_config()
        self.flows = create_flows(self, self.brick_config, flow_config)
        self.flows_by_name = {flow.name: flow for flow in self.flows}

        await self.exit.wait()
        log.info("Exit")

    def handle_signal(self, sig, frame):  # pylint: disable=unused-argument
        asyncio.create_task(self.shutdown())

    async def shutdown(self):
        """shut down the controlpeer"""
        log.info("Initiating shutdown")
        await self.stop_flows()
        self.flow_director.close()
        await self.webapi.stop()
        self.server.close()
        await self.server.wait_closed()

        self.exit.set()
        log.info("Shutdown sequence complete - should exit soon")

        pending_tasks = asyncio.all_tasks()
        for task in pending_tasks:
            log.info("still pending: %r", task)
            task.cancel()
            await task

    async def setup_runner_communication(self):
        """create a server to communicate with brick runners"""
        log.debug("create server")
        self.server = await asyncio.start_server(self.establish_communication, "127.0.0.1", 8888)
        self.server_address = self.server.sockets[0].getsockname()

    def setup_webapi(self):
        self.webapi = WebApi(self)
        self.webapi.run()

    async def start_flow(self, name):
        """update the configuration and start the flow"""
        # try to read the config again to get any updates
        # TODO: this is a temporary hack
        flow_config = await self.flow_director.get_flow_config()
        flows = create_flows(self, self.brick_config, flow_config)
        flow = next(iter(flow for flow in flows if flow.name == name), None)
        if not flow:
            return None

        self.flows.append(flow)
        self.flows_by_name[flow.name] = flow

        flow.start()
        return flow

    async def stop_flows(self):
        await asyncio.gather(*[flow.stop() for flow in self.flows])

    async def stop_flow(self, name):
        flow = self.flows_by_name[name]
        await flow.stop()
        return flow

    async def establish_communication(self, reader, writer):
        """establish communication with brick runners: handle registration"""
        runner_connection = Connection(reader, writer, log)

        runner_registration = await runner_connection.receive()
        _, runner_uid = runner_registration
        runner = self.runners.get(runner_uid)
        if not runner:
            log.error("No runner found for id: %s", runner_uid)
            log.debug("Available brick runner: %r", self.runners)
            return

        self.runner_connections[runner_uid] = runner_connection
        # move communication to the runner
        asyncio.create_task(runner.process_messages(runner_connection))
