import pytz  
from datetime import datetime  
import json  
from confluent_kafka import Consumer, KafkaError  
from flask import Flask  
app = Flask(__name__)  
class ConsumerHealthCheckService:  
    def __init__(self, kafka_broker, kafka_topic):  
        self.kafka_broker = kafka_broker  
        self.kafka_topic = kafka_topic  
        self.consumer = Consumer({  
            'bootstrap.servers': self.kafka_broker,  
            'group.id': 'consumer_health_check_service',  
            'auto.offset.reset': 'latest'  
        })  
        self.consumer.subscribe([self.kafka_topic])  
    def get_latest_health_check(self):  
        # get the current timestamp  
        tz = pytz.timezone('Europe/Bucharest')  
        current_time = datetime.now(tz)  
        # Format the current time as an ISO 8601 string with timezone offset - same copy paste from previous health_check_service
        timestamp = current_time.isoformat()  
        # latest message pool from kafka_topic  
        self.consumer.poll(0)  
        self.consumer.seek_to_end()  
        msg = self.consumer.consume(1)  
        if msg is None or len(msg) == 0:  
            return "found nothing there"  
        else:  
            # latest health check message from kafka  
            latest_health_check = msg[0].value().decode('utf-8')  
            print('the newest health check is this: {0}'.format(latest_health_check))  
            # json payload with current timestamp  
            payload = {  
                "service_name": "my_microservice",  
                "health_status": "OK",  
                "timestamp": timestamp  
            }  
            # convert the payload
            payload_str = json.dumps(payload)  
            print(payload_str)  
            return latest_health_check  
@app.route('/get_latest_health_check')  
def get_latest_health_check():  
    return consumer_health_check_service.get_latest_health_check()  
if __name__ == '__main__':  
    kafka_broker = 'localhost:9092'  
    kafka_topic = 'health_checks_topic'  
    consumer_health_check_service = ConsumerHealthCheckService(kafka_broker, kafka_topic)  
    app.run()  
