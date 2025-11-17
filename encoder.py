def encode_payload(temp, hum, wind):
    # Escalar temperatura
    temp_scaled = int(temp * 100)  # (0–11000)

    # Mapear viento
    wind_map = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]
    wind_index = wind_map.index(wind)  # 0–7 (3 bits)

    # Empaquetar en un entero de 24 bits
    packed = (temp_scaled << 10) | (hum << 3) | wind_index

    # Convertir a 3 bytes (big-endian)
    return packed.to_bytes(3, byteorder="big")

def decode_payload(payload_bytes):
    wind_map = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]

    packed = int.from_bytes(payload_bytes, byteorder="big")

    # Extraer campos
    wind = packed & 0b111
    hum = (packed >> 3) & 0b1111111
    temp_scaled = (packed >> 10) & 0b11111111111111

    temp = temp_scaled / 100.0

    return {
        "temperatura": temp,
        "humedad": hum,
        "direccion_viento": wind_map[wind]
    }