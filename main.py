import asyncio

from aiokafka import ConsumerRecord

from streaming_kafka.kafka_engine import KafkaEngine
from streaming_kafka.streams import Stream
from streaming_kafka.settings import Settings


def callback(record: ConsumerRecord) -> None:
    print(record)


async def main():
    settings = Settings(_env_file=".env", _env_prefix="kafka_")

    stream = Stream("t1", client_id="test-stream", callback=callback, settings=settings)
    engine = KafkaEngine(settings=settings)

    engine.add_stream(stream)

    await engine.start()

    msgs = [b"hello", b"world", b"bami"]

    while len(msgs) > 0:
        await asyncio.sleep(1)
        msg = msgs.pop(0)
        print(f"Producing message {msg}")
        await engine.produce("t1", msg)

    await engine.stop()

if __name__ == "__main__":
    asyncio.run(main())
