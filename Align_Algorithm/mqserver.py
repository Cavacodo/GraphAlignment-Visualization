import os
import time
from http.client import responses

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
    GCNA = ['IsoRank', 'BigAlign', 'FINAL', 'DeepLink', 'REGAL']
    try:
        # 解析JSON格式的消息体
        message = json.loads(body.decode('utf-8'))
        print(f"Received message: {message}")
        res = message['type']
        args = message['args']
        if res in GCNA:
            response = requests.post(url, json=process_data(res,args))
        elif res == 'GTCAlign':
            response = requests.post(url, json=process_data('GTCAlign',args))
        elif res == 'GAlign':
            response = requests.post(url, json=process_data('GAlign',args))
        else:
            print(f"Invalid type: {res}")
        print(response.text)
        # 确认消息已处理
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Failed to process message: {e}")
        # 拒绝消息，可以重新入队或丢弃
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

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
def process_data(type,args=''):
    print("Processing...")
    command = None
    GCNA = ['IsoRank','BigAlign','FINAL','DeepLink','REGAL']
    m = []
    if type in GCNA:
        os.chdir('D:\GraphAlignment-Visualization\Align_Algorithm\GCNA_Origin\GCNA')
    elif type == 'GAlign':
        os.chdir('D:\GraphAlignment-Visualization\Align_Algorithm\GAlign')
    elif type == 'GTCAlign':
        os.chdir('D:\GraphAlignment-Visualization\Align_Algorithm\GTCAlign')
    if type in GCNA:
        command = 'python -u network_alignment.py ' + type + ' ' + args
        print(command)
    elif type == 'GAlign':
        command = 'python -u network_alignment.py GAlign' + ' ' +  args
    elif type == 'GTCAlign':
        command = 'python -u main.py' + ' ' + args
    else: return None
    with os.popen(command) as pipe:
        output = pipe.read()
    with open('m.txt','r',encoding='utf-8') as f:
        for line in f:
            tmp = line.strip().split(' ')
            m.append(tmp)
    output = output.split('\n')
    acc = {'Accuracy':None,'MAP':None,'Precision_5':None,'Precision_10':None,'AUC':None,'Running time':None}
    info = ['Accuracy','MAP','Precision_5','Precision_10','AUC','Running time']
    for line in output:
        tmp = line.split(':')
        if tmp[0] in info:
            acc[tmp[0]] = tmp[1]
    acc = str(acc)[1:-1]
    ans = {'type': type,'acc':acc,'m':m}
    print("Process Done")
    return ans



if __name__ == '__main__':
    main()
