import json
import time
from confluent_kafka import Consumer
import matplotlib.pyplot as plt

# Listas globales para almacenar telemetría
all_temp = []
all_hume = []
all_wind = []

def procesarMensaje(msg):
    data = msg.value().decode("utf-8")
    return json.loads(data)


def plotAllData(temp, hum, wind):
    plt.clf()  # limpia la figura para redibujar

    plt.subplot(2, 1, 1)
    plt.plot(temp, marker='o')
    plt.title("Temperatura (°C) en tiempo real")
    plt.ylabel("°C")

    plt.subplot(2, 1, 2)
    plt.plot(hum, marker='o')
    plt.title("Humedad (%) en tiempo real")
    plt.ylabel("%")

    plt.tight_layout()
    plt.pause(0.1)   


def main():
    config = {
        'bootstrap.servers': '147.182.219.133:9092',
        'group.id': 'foo2',
        'auto.offset.reset': 'latest'
    }

    consumer = Consumer(config)
    topic = "22880"
    consumer.subscribe([topic])

    print(f"Escuchando mensajes del topic '{topic}'...\n")

    plt.ion()
    plt.figure(figsize=(8,6))

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Error en mensaje:", msg.error())
            continue

        print("Mensaje recibido:", msg.value())

        payload = procesarMensaje(msg)

        all_temp.append(payload["temperatura"])
        all_hume.append(payload["humedad"])
        all_wind.append(payload["direccion_viento"])

        plotAllData(all_temp, all_hume, all_wind)


main()
