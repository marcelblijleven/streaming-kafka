from aiokafka import AIOKafkaProducer
from aiokafka.structs import RecordMetadata

from streaming_kafka.settings import Settings
from streaming_kafka.streams import Stream


class KafkaEngine:
    """
    Provides a single object to interact with when communicating with the Kafka server(s).
    """
    def __init__(
        self,
        settings: Settings
    ) -> None:
        self._settings = settings
        self._producer: AIOKafkaProducer | None = None
        self._streams: list[Stream] = []

    def add_stream(self, stream: Stream) -> None:
        """
        Adds a stream to the internal stream registry

        Args:
            stream: a Stream instance

        """
        for s in self._streams:
            if stream.client_id == s.client_id:
                raise ValueError(f"a stream with {stream.client_id=} already exists")

        self._streams.append(stream)

    async def produce(self, topic: str, value: bytes) -> RecordMetadata:
        """
        Sends a message to the Kafka server

        Args:
            topic: the Topic for the message
            value: the value of the message

        Returns:
            the awaited RecordMetadata for the produced message

        """
        fut = await self._producer.send(topic=topic, value=value)
        return await fut

    async def start(self) -> None:
        """
        Initialises the AIOKafkaProducer and starts all the streams
        registered to the KafkaEngine.

        """
        await self._init_producer()

        for stream in self._streams:
            await stream.start()

    async def stop(self) -> None:
        """
        Stops all the streams registered to the KafkaEngine

        """
        if self._producer is not None:
            await self._producer.stop()

        for stream in self._streams:
            await stream.stop()

    async def _init_producer(self) -> None:
        if self._producer is not None:
            return None

        self._producer = AIOKafkaProducer(**self._settings.get_producer_settings())
        await self._producer.start()
