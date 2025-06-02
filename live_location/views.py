from django.shortcuts import render
from django.http import JsonResponse
from kafka import KafkaProducer, KafkaConsumer
import json

# Kafka topic name
KAFKA_TOPIC = 'location'
KAFKA_SERVER = '103.150.136.82:9092'

# Helper function to serialize data
def serializer(message):
    return json.dumps(message).encode('utf-8')

# Kafka Producer (reuse connection)
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_SERVER],
    value_serializer=serializer
)

# Render Home
def lindex(request):
    return render(request, 'index.html')

# Render Send Location Page
def send_location(request):
    return render(request, 'send_location.html')

# Send lat/lon to Kafka
def produce_lat_lon(request):
    if request.method == 'GET':
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')

        if not lat or not lon:
            return JsonResponse({'error': 'Latitude and longitude required'}, status=400)

        try:
            producer.send(KAFKA_TOPIC, {'lat': lat, 'lon': lon})
            return JsonResponse({'status': 'success', 'lat': lat, 'lon': lon})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# Get latest lat/lon from Kafka
def data(request):
    if request.method == 'GET':
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_SERVER],
            auto_offset_reset='latest',
            consumer_timeout_ms=2000,  # wait max 2 seconds
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        try:
            for message in consumer:
                data = message.value
                print("Received:", data)
                return JsonResponse({
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon')
                })
            # No new messages
            return JsonResponse({'error': 'No new location data'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        finally:
            consumer.close()
