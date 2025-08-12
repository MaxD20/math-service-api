import pika
import os
import logging
from math_service.schemas.log_schema import LogEntry


logger = logging.getLogger(__name__)
# RABBITMQ_PARAMS = pika.ConnectionParameters(host="localhost")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PARAMS = pika.ConnectionParameters(host=RABBITMQ_HOST)


def publish_log(entry: LogEntry) -> None:

    try:
        message_body = entry.model_dump_json()

        connection = pika.BlockingConnection(RABBITMQ_PARAMS)
        channel = connection.channel()

        channel.exchange_declare(
            exchange="math_logs",
            exchange_type="fanout",
            durable=True
        )

        channel.basic_publish(
            exchange="math_logs",
            routing_key="",
            body=message_body,
            properties=pika.BasicProperties(delivery_mode=2),
        )

    except pika.exceptions.AMQPConnectionError as e:
        logger.error("Could not publish to RabbitMQ at %s: %s", RABBITMQ_HOST, e)

    except Exception as e:
        logger.exception("Unexpected error in publish_log(): %s", e)

    finally:

        if connection is not None and connection.is_open:
            try:
                connection.close()
            except Exception:
                logger.warning("Failed to close RabbitMQ connection cleanly",
                               exc_info=True)
