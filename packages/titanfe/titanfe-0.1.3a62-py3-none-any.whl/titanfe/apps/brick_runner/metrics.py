#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""Handle creation of metric data and streaming it to Kafka"""

import asyncio
import os
import pickle
import platform
from abc import ABC
from dataclasses import dataclass, field

import aiokafka

from titanfe.utils import DictConvertable, iso_utc_time_string, cancel_tasks

# tiny little hack for development purposes only
DISABLED = os.getenv("TITAN_METRICS_DISABLED") is not None


class MetricEmitter:
    """The MetricEmitter encapsulates creation of metric data and sending them to a Kafka instance

    Arguments:
        kafka_bootstrap_servers (str):
            'host[:port]' string (or list of 'host[:port]' strings)
            to contact the Kafka bootstrap servers on
        logger (logging.logger): the parent's logger instance
    """

    def __init__(self, metrics_metadata, kafka_bootstrap_servers, logger):
        self.log = logger
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.kafka = None
        self.metrics_meta = metrics_metadata

    @classmethod
    async def create_from_brick_runner(cls, runner) -> "MetricEmitter":
        """Creates, starts and returns a MetricEmitter instance"""
        metrics_meta = MetricsBase.extract_from_runner(runner)
        emitter = cls(metrics_meta, runner.kafka_bootstrap_servers, runner.log)
        await emitter.start()
        return emitter

    async def start(self):
        """creates and starts the internal Kafka producer"""
        if DISABLED or not self.kafka_bootstrap_servers:
            self.log.info("Kafka is disabled or no bootstrap servers were given")
            return

        self.log.info("Starting Kafka producer")
        self.kafka = aiokafka.AIOKafkaProducer(
            loop=asyncio.get_event_loop(),
            bootstrap_servers=self.kafka_bootstrap_servers,
            # key_serializer=str.encode,
            # value_serializer=str.encode
            value_serializer=pickle.dumps,
        )
        await self.kafka.start()

    async def emit(self, metrics_dict):
        self.log.metric("%s", metrics_dict)

        if self.kafka:
            await self.kafka.send("titanfe.metrics", metrics_dict)

    async def emit_queue_metrics(self, queue_name, queue_length):
        queue_metrics = QueueMetrics(
            **self.metrics_meta, queue_name=queue_name, queue_length=queue_length
        )
        await self.emit(queue_metrics.to_dict())

    async def emit_packet_metrics(self, packet, duration):   # pylint: disable=missing-docstring
        packet_metrics = PacketMetricsAtBrick(
            **self.metrics_meta,
            packet=packet.uid,
            execution_time=duration,
            traveling_time=packet.traveling_time,
            **packet.queue_times,
        )
        await self.emit(packet_metrics.to_dict())

    async def emit_brick_metrics(self, execution_time):
        brick_metrics = BrickMetrics(**self.metrics_meta, execution_time=execution_time)
        await self.emit(brick_metrics.to_dict())

    async def stop(self):
        if self.kafka is not None:
            await self.kafka.stop()


class QueueWithMetrics(asyncio.Queue):
    """an ayncio.Queue that emits metrics (queue length)"""

    def __init__(self, emitter, name, interval=0.1, maxsize=0):
        super().__init__(maxsize)

        self.name = name
        self.metrics = asyncio.create_task(self.emit_metrics(emitter, interval))

    async def emit_metrics(self, emitter, interval=0.1):
        """automatically scheduled as task"""
        while True:
            await asyncio.sleep(interval)
            queue_length = self.qsize()
            if queue_length:
                await emitter.emit_queue_metrics(self.name, queue_length)

    async def put(self, item):
        await super().put(item)

    async def close(self):
        await cancel_tasks((self.metrics,), wait_cancelled=True)

    @property
    def unfinished_tasks(self):
        return self._unfinished_tasks


@dataclass
class MetricsBase(DictConvertable, ABC):
    """Information that every "metric" should contain"""

    flow: str = "FlowName?"
    brick: str = "BrickName?"
    runner: str = "RunnerUid?"
    host: str = platform.node()
    timestamp: str = field(default_factory=iso_utc_time_string)

    @staticmethod
    def extract_from_runner(runner):
        """extract the basic information from a brick runner instance"""
        if runner.brick:
            return dict(runner=runner.uid, brick=runner.brick.name, flow=runner.brick.flowname)

        return dict(runner=runner.uid)


@dataclass
class PacketMetricsAtBrick(MetricsBase):
    """Metric data for a packet being processed at a Brick"""

    content_type: str = "titan-packet-metrics"
    packet: str = "PacketUid?"
    execution_time: float = 0.0
    traveling_time: float = 0.0
    time_in_input: float = 0.0
    time_in_output: float = 0.0
    time_on_wire: float = 0.0
    at_outlet: bool = False  # TODO


@dataclass
class QueueMetrics(MetricsBase):
    """Metric data for Input/Output-queues"""

    content_type: str = "titan-queue-metrics"
    queue_name: str = "QueueName?"
    queue_length: int = 0


@dataclass
class BrickMetrics(MetricsBase):
    """Metric data for brick executions"""

    content_type: str = "titan-brick-metrics"
    execution_time: float = 0.0
