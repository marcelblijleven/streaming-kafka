import asyncio
import logging

from aiokafka import ConsumerRecord

from streaming_kafka.kafka_app import KafkaStreamingApp
from streaming_kafka.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings(_env_file=".env", _env_prefix="kafka_")
streaming_app = KafkaStreamingApp(settings=settings)


@streaming_app.register_callback("t1", client_id="t1-consumer")
def callback_t1(record: ConsumerRecord) -> None:
    logging.info("received record on topic t1: %s", record)


@streaming_app.register_callback("t2", client_id="t2-consumer")
def callback_t2(record: ConsumerRecord) -> None:
    logging.info("received record on topic t2: %s", record)


def get_msg(queue: list[bytes]) -> bytes | None:
    try:
        return queue.pop(0)
    except IndexError:
        return None


async def main():
    t1_msgs = [b"hello", b"world"]
    t2_msgs = [b"foo", b"bar", b"baz"]

    async with streaming_app:
        while len(t1_msgs) > 0 and len(t2_msgs) > 0:
            await asyncio.sleep(1)

            if (t1_msg := get_msg(t1_msgs)) is not None:
                print(f"Producing for t1 {t1_msg=}")
                await streaming_app.produce("t1", t1_msg)

            if (t2_msg := get_msg(t2_msgs)) is not None:
                print(f"Producing for t2 {t2_msg=}")
                await streaming_app.produce("t2", t2_msg)


if __name__ == "__main__":
    asyncio.run(main())
