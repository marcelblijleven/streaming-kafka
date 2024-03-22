import asyncio
from asyncio import Future
from typing import Callable, TypeAlias

from aiokafka import ConsumerRecord, AIOKafkaConsumer

StreamCallback: TypeAlias = Callable[[ConsumerRecord], None]


class Stream:
    def __init__(self, topics: str | list[str], *, client_id: str, callback: StreamCallback):
        self.topics = topics if isinstance(topics, list) else [topics]

        self._client_id = client_id
        self._callback = callback
        self._task: Future | None = None
        self._consumer: AIOKafkaConsumer | None = None
        self._started = False

    @property
    def is_started(self) -> bool:
        """
        Returns True if the stream was started
        """
        return self._started

    async def start(self) -> None:
        """
        Start the stream by creating a Kafka consumer which subscribes to the topics
        that were provided to this stream.

        The stream will listen to any incoming messages in an asyncio task.

        """
        self._consumer = AIOKafkaConsumer(
            *self.topics, bootstrap_servers="localhost:9092", group_id="test"
        )

        await self._consumer.start()
        self._started = True

        self._task = await asyncio.create_task(
            self._listener(), name=f"listener-{self._client_id}"
        )

    async def stop(self) -> None:
        """
        Stop the stream, this will also stop the asyncio task that listens to the incoming
        messages.

        """
        if self._consumer is None:
            return None

        self._started = False

        if self._task is not None:
            self._task.cancel(msg="consumer is being stopped")
        await self._consumer.stop()

    async def _listener(self):
        """
        While the stream is running, this will listen to the incoming messages
        on the subscribed topics and call the callback on the received messages.

        """
        while self._started:
            cr = await self._consumer.getone()
            self._callback(cr)
