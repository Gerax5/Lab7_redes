import json
import random
import time
import numpy as np
from confluent_kafka import Producer

DIRECCIONES_VIENTO = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]

MEDIA_TEMP = 55
VAR_TEMP = 15

MEDIA_HUM = 50
VAR_HUM = 20


def generar_temperatura():
    valor = np.random.normal(MEDIA_TEMP, VAR_TEMP)
    valor = max(0, min(110, valor))
    return round(float(valor), 2)


def generar_humedad():
    valor = np.random.normal(MEDIA_HUM, VAR_HUM)
    valor = max(0, min(100, valor))
    return int(round(valor))


def generar_direccion_viento():
    return random.choice(DIRECCIONES_VIENTO)


def generar_medicion():
    data = {
        "temperatura": generar_temperatura(),
        "humedad": generar_humedad(),
        "direccion_viento": generar_direccion_viento()
    }
    return json.dumps(data)

def test_generar_medicion():
    for _ in range(10):
        medicion = generar_medicion()
        print(medicion)

def sender():
    config = {
        'bootstrap.servers': '147.182.219.133:9092'
    }
    
    producer = Producer(config)
    topic = "22880"

    while True:
        data = generar_medicion()
        print("Enviando:", data)

        producer.produce(topic, key="sensor1", value=data)
        producer.flush()

        time.sleep(random.randint(15, 30))



# test_generar_medicion()
sender()
