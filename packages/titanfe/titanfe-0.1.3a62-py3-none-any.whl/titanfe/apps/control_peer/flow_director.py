#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#
"""Flow Director communication"""

import asyncio
import json
from http import HTTPStatus
from aiohttp.client_exceptions import ClientError
from aiohttp_requests import requests
import titanfe.log as logging
from titanfe.utils import Flag

log = logging.getLogger(__name__)


class FlowDirector:
    """FlowDirector """

    def __init__(self, flow_director_address):
        self.address = "http://"+flow_director_address
        self._closing = Flag()

    def close(self):
        self._closing.set()
        # TODO: unregister?

    async def register(self, control_peer_address):
        """Register controlpeer at Flowdirector"""

        def registration_success():
            log.info("Registered ControlPeerApi (%s) at FlowDirector", control_peer_address)
            return True

        def registration_bad_request():
            log.error("Registration failed with status BadRequest")
            raise ValueError("Registration failed")

        def registration_conflict():
            log.error("Registration failed with status Conflict")
            raise ValueError("Registration failed, address already registered")

        response_handlers = {
            HTTPStatus.OK: registration_success,
            HTTPStatus.CREATED: registration_success,
            HTTPStatus.BAD_REQUEST: registration_bad_request,
            HTTPStatus.CONFLICT: registration_conflict,
        }

        registration = json.dumps(control_peer_address).strip('"')

        while not self._closing:
            try:
                response = await requests.post(self.address+"/controlpeers", json=registration)
                response_handler = response_handlers.get(response.status)
                if response_handler:
                    return response_handler()
            except ClientError:
                log.debug("Could not register at FlowDirector", exc_info=True)
            else:
                log.debug("Could not register at FlowDirector: %r", response)

            await asyncio.sleep(0.1)

    async def get_flow_config(self):
        """ask the flow director for the configuration of the flows"""
        try:
            response = await requests.get(self.address+"/flows")
            if response.status == HTTPStatus.OK:
                return await response.json()
        except ClientError:
            log.error("Requesting flow config failed", exc_info=True)
        else:
            log.error("Requesting flow config failed: %r", response)

        return []
