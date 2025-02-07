import time

import pika
import json
import requests

# RabbitMQ连接配置
rabbitmq_host = 'localhost'  # 根据实际情况修改
queue_name = 'stock-request-queue'
exchange_name = 'stock-exchange'
routing_key = 'stock-request-key'
url = "http://localhost:8080/res/python"

def callback(ch, method, properties, body):
    try:
        # 解析JSON格式的消息体
        message = json.loads(body.decode('utf-8'))
        print(f"Received message: {message}")
        res = message['type']
        if res == 1:
            response = requests.post(url, json=list(process_data_1()))
        elif res == 2:
            response = requests.post(url, json=list(process_data_2()))
        print(response.text)
        # 确认消息已处理
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Failed to process message: {e}")
        # 拒绝消息，可以重新入队或丢弃
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    # 声明交换机和队列（确保与Java端一致）
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)

    # 设置QoS以限制未确认的消息数量
    channel.basic_qos(prefetch_count=1)

    # 开始消费消息
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print('Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()
def process_data_1():
    time.sleep(5)
    return {"res": ["方法一处理好了"],"type" : 1}
def process_data_2():
    time.sleep(5)
    return {"res": ["方法二处理好了"],"type" : 2}

if __name__ == '__main__':
    main()
