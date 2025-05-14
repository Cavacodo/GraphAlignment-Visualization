import os
import time
from http.client import responses

import pika
import json
import requests
from sympy.codegen.ast import continue_

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
        dataset = message['dataset']
        res = message['type']
        args = message['args']
        data = message['dataset']
        if res in GCNA:
            response = requests.post(url, json=process_data(res,args,data))
        elif res == 'GTCAlign':
            response = requests.post(url, json=process_data('GTCAlign',args,data))
        elif res == 'GAlign':
            response = requests.post(url, json=process_data('GAlign',args,data))
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
    connection = connect_rabbitmq()
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
def process_data(type,args='',data=''):
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
        if data == 'ppi': command = 'python -u network_alignment.py ' + '--data ppi '+ type + ' ' + args
        else: command = 'python -u network_alignment.py ' + type + ' ' + args
        print(command)
    elif type == 'GAlign':
        command = 'python -u network_alignment.py GAlign' + ' ' +  args
    elif type == 'GTCAlign':
        if data != 'ppi' : command = 'python -u main.py' + ' ' + args
        else: command = 'python -u main.py' + ' --data ppi ' + args
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
        print(tmp)
        if tmp[0] in info:
            acc[tmp[0]] = tmp[1]
    acc = str(acc)[1:-1]
    ans = {'type': type,'acc':acc,'m':m}
    print("Process Done")
    return ans

def connect_rabbitmq():
    """增加RabbitMQ连接重试机制"""
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, heartbeat=600))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready, retrying...")
            time.sleep(5)  # 每隔5秒重试一次

if __name__ == '__main__':
    main()

