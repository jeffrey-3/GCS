from cobs import cobs

# Interface layer
command_payload = bytearray([0x00] * 38)
command_payload[0] = 0b00000001 # Payload type
command_payload[1] = 0b00000000 # Command type

# Transport protocol layer
packet = bytes([0x00]) + cobs.encode(command_payload)
print(packet)
print(len(packet))