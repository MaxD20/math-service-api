import json
import pika
from math_service.schemas.log_schema import LogEntry
from math_service.models.request_log_model import log_to_db


RABBITMQ_PARAMS = pika.ConnectionParameters(host='localhost')


def main() -> None:
    connection = pika.BlockingConnection(RABBITMQ_PARAMS)

    channel = connection.channel()

    channel.exchange_declare(
        exchange='math_logs',
        exchange_type='fanout',
        durable=True
    )

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='math_logs', queue=queue_name)

    def on_message(ch, method, properties, body):
        try:
            payload = json.loads(body)
            entry = LogEntry(**payload)
            log_to_db(entry)

            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    channel.basic_consume(queue=queue_name, on_message_callback=on_message)

    print(" [*] Log messages waiting. ctrl+c to exit")
    channel.start_consuming()


if __name__ == '__main__':
    main()
