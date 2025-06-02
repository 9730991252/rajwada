from django.shortcuts import render
from kafka import KafkaProducer, KafkaConsumer
import time
import json
from django.http import JsonResponse
# Create your views here.
def lindex(request):
    return render(request, 'index.html')

def send_location(request):
    return render(request, 'send_location.html')

def serializer(message):
    return json.dumps(message).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['103.150.136.82:9092'],
    value_serializer=serializer
)

def produce_lat_lon(request):
    if request.method == 'GET':
        lat = request.GET['lat']
        lon = request.GET['lon']
        producer.send('location', {'lat': lat, 'lon': lon})
        producer.flush()
        return JsonResponse({'latitude': 'status'})
    
def data(request):
    if request.method == 'GET':
        consumer = KafkaConsumer(
        'location',
        bootstrap_servers='103.150.136.82:9092',
        auto_offset_reset='earliest',
        )
        consumed_message = []
        for message in consumer:
            c = json.loads(message.value.decode())
            consumed_message.append(c)
            print(c)
            break
            
        
        d = consumed_message[0]
    return JsonResponse({'latitude': d['lat'],'longitude':d['lon']})