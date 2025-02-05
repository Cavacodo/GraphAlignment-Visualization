import pika
# from GTCAlign import main

# RabbitMQ服务器连接配置
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
print("建立连接")

# 声明要监听的队列，确保与Java端的队列名称相匹配
queue_name = 'stock-queue'
channel.queue_declare(queue=queue_name, durable=True)


# 建立回调函数，获取队列消息内容
def callback(ch, method, properties, body):
    try:
        print("连接成功")
        print("回调函数执行成功")
        print("Received JSON data:", body)
        response_body = "接收到了"
        ch.basic_publish(exchange='', routing_key=method.routing_key, body=response_body)
        print("Message sent back to queue")
    except Exception as e:
        print("Error:", str(e))

    # 设置回调函数，当有消息到达时将被调用


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit, press Ctrl+C')
channel.start_consuming()

# main.run()
