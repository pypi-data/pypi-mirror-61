#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""Flow config: parsing and representation"""
import asyncio
from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import List

from ruamel import yaml

import titanfe.log as logging

from titanfe.constants import DEFAULT_PORT, DEFAULT_MAX_IDLE_TIME
from titanfe.utils import create_uid
from .brick import Brick

log = logging.getLogger(__name__)


class FlowState(IntEnum):
    ACTIVE = 1
    INACTIVE = 2


@dataclass
class BrickConnection:
    """a connection between two bricks"""

    source: str
    target: str
    source_port: str
    target_port: str

    @classmethod
    def from_config(cls, connection_config, bricks_by_name):
        """create from a dict e.g. as read from yaml"""
        source = bricks_by_name[connection_config["Source"]]
        target = bricks_by_name[connection_config["Target"]]
        ports = defaultdict(lambda: DEFAULT_PORT)
        ports.update(connection_config.get("Ports", {}))
        if not ports["Source"]:
            ports["Source"] = DEFAULT_PORT
        if not ports["Target"]:
            ports["Target"] = DEFAULT_PORT
        return cls(source, target, ports["Source"], ports["Target"])


class Flow:
    """Represent a flow configuration with it bricks and connections

    Arguments:
        flow_config (dict): the flow configuration as dict
        bricks_config (dict): the bricks part of the configuration as dict
        path_to_bricks (Path): path to directory holding the "./bricks" folder
    """

    def __init__(self, name, control_peer, exit_after_idle_seconds, bricks):
        self.name = name
        self.uid = create_uid("F-")
        self.state = FlowState.INACTIVE

        self.control_peer = control_peer
        self.bricks = bricks
        self.exit_after_idle_seconds = exit_after_idle_seconds

    @classmethod
    def from_config(cls, control_peer, flow_config, bricks_config, path_to_bricks):
        """ create a Flow instance from the given configurations

        Args:
            control_peer (ControlPeer): the control peer
            flow_config (dict): the flow configuration
            bricks_config (dict): the local bricks' configuration
            path_to_bricks (str): path to the local folder containing the bricks' modules

        Returns: a Flow instance
        """
        # pylint: disable=too-many-locals

        flow = cls(
            flow_config["Name"],
            control_peer,
            flow_config.get("exit_after_idle_seconds", DEFAULT_MAX_IDLE_TIME),
            None,
        )

        bricks_general_config_by_name = {brick["Name"]: brick for brick in bricks_config}

        bricks_by_name = {}
        for brick_config in flow_config["Bricks"]:
            brick_name = brick_config["Brick"]
            brick = Brick.from_config(
                flow, bricks_general_config_by_name[brick_name], brick_config, path_to_bricks
            )
            bricks_by_name[brick.name] = brick

        connections_by_source = defaultdict(list)
        connections_by_target = defaultdict(list)
        for connection in flow_config["Connections"]:
            conn = BrickConnection.from_config(connection, bricks_by_name)
            connections_by_source[conn.source].append(conn)
            connections_by_target[conn.target].append(conn)

        for brick in bricks_by_name.values():
            brick.update_connections(
                input_connections=connections_by_target[brick],
                output_connections=connections_by_source[brick],
            )

        flow.bricks = bricks_by_name.values()
        return flow

    def __repr__(self):
        return f"Flow({self.name}, {self.bricks})"

    def start(self):
        """start brick runners for each brick in the flow"""
        log.debug("start flow: %s", self.name)
        self.state = FlowState.ACTIVE
        for brick in self.bricks:
            brick.start()

    async def stop(self):
        """send a stop signal to all bricks"""
        log.info("stopping all bricks for: %s", self)
        await asyncio.gather(*[brick.stop() for brick in self.bricks])
        self.state = FlowState.INACTIVE
        log.info("%s stopped", self)


def _parse_brick_config(config_file):
    """retrieve the basic brick config by parsing the brick configuration file (yaml)"""
    with open(config_file) as config:
        brick_config = yaml.safe_load(config)["Bricks"]
    return brick_config


def create_flows(control_peer, config_file, all_flows_config) -> List[Flow]:
    """assemble the flows utilizing the two config sources"""
    bricks_path = Path(config_file).resolve().parent
    brick_config = _parse_brick_config(config_file)
    flows = [
        Flow.from_config(control_peer, flow_config, brick_config, bricks_path)
        for flow_config in all_flows_config
    ]
    log.info("Configured Flows: %r", flows)
    return flows
