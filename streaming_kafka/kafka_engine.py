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

    async def start(self) -> None:
        """
        Starts all the streams registered to the KafkaEngine

        """
        for stream in self._streams:
            await stream.start()

    async def stop(self) -> None:
        """
        Stops all the streams registered to the KafkaEngine

        """
        for stream in self._streams:
            await stream.stop()
