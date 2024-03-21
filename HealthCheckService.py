import pytz  

from datetime import datetime  

import json  

from confluent_kafka import Consumer, KafkaError  

from flask import Flask  

app = Flask(__name__)  

class HealthCheckService:  

    def __init__(self, kafka_broker, kafka_topic):  

        self.kafka_broker = kafka_broker  

        self.kafka_topic = kafka_topic  

        self.consumer = Consumer({  

            'bootstrap.servers': self.kafka_broker,  

            'group.id': 'health_check_service',  

            'auto.offset.reset': 'earliest'  

        })  

        self.consumer.subscribe([self.kafka_topic])  

    def check_health(self):  

        #get the current timestamp

        tz = pytz.timezone('Europe/Bucharest')  

        current_time = datetime.now(tz)  

        #format the current time as an ISO 8601 string with timezone offset  - that s a copy paste description :D

        timestamp = current_time.isoformat()  

        while True:  

            msg = self.consumer.poll(1.0)  

            if msg is None:  

                continue  

            if msg.error():  

                if msg.error().code() == KafkaError._PARTITION_EOF:  

                    print('reached the end of the partition , oups {0}/{1}'  

                          .format(msg.topic(), msg.partition()))  

                else:  

                    print('ghosted: {0}'.format(msg.error()))  

            else:  

                print('got the message : {0}'.format(msg.value().decode('utf-8')))  

                #create a JSON payload with the current timestamp  

                payload = {  

                    "service_name": "my_microservice",  

                    "health_status": "OK",  

                    "timestamp": timestamp  

                }  

                #let's convert the payload to a JSON string 

                payload_str = json.dumps(payload)  

                print(payload_str)  

@app.route('/check_health')  

def check_health():  

    health_check_service.check_health()  

    return 'Health check performed'  

if __name__ == '__main__':  

    kafka_broker = 'localhost:9092'  

    kafka_topic = 'health_checks_topic'  

    health_check_service = HealthCheckService(kafka_broker, kafka_topic)  

    app.run()  



#used this for topic creation  : kafka-topics.sh --create --topic health_checks_topic --zookeeper localhost:2181 --partitions 6 --replication-factor 3 --config retention.ms=604800000
