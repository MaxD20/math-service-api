import pika
import json


params = pika.ConnectionParameters(host="localhost")


connection = pika.BlockingConnection(params)
channel = connection.channel()


channel.exchange_declare(
    exchange="math_logs",
    exchange_type="fanout",
    durable=True,
)


queue_name = "math_log_consumer"
channel.queue_declare(queue=queue_name, durable=True)


channel.queue_bind(
    exchange="math_logs",
    queue=queue_name,
    routing_key="",
)

print(f"[*] Waiting for logs in '{queue_name}'. To exit press CTRL+C")


def callback(ch, method, properties, body):
    try:
        log_entry = json.loads(body)
        print("Received log:", json.dumps(log_entry, indent=2))
    except Exception:

        print("Received raw:", body)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False,
)


channel.start_consuming()
