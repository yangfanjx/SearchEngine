from kafka import KafkaProducer
from kafka import KafkaConsumer

KAFAKA_HOST = "172.16.109.99"
KAFAKA_PORT = 9092
KAFAKA_TOPIC = "test"

sercer = '172.16.109.99:9092'

def prodect_function():
    producer = KafkaProducer(bootstrap_servers=sercer)  # 连接kafka

    msg = "Hello World".encode('utf-8')  # 发送内容,必须是bytes类型
    producer.send('test', msg)  # 发送的topic为test
    producer.close()



def consum_function():
    consumer = KafkaConsumer('test', bootstrap_servers=[sercer])
    for msg in consumer:
        recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
        print(recv)


if __name__ == "__main__":
    # prodect_function()
    # print("prodect ok")
    consum_function()
