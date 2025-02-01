from cobs import cobs
import struct

"""
Command
"""
# Interface layer
command_payload = bytearray([0x00] * 38)
command_payload[0] = 1 # Payload type
command_payload[1] = 0 # Command

# Transport protocol layer
packet = bytes([0x00]) + cobs.encode(command_payload)
print(packet)
print(len(packet))

"""
Waypoints
"""
 # Interface layer
command_payload = bytearray([0x00] * 38)
command_payload[0] = 2 # Payload type
command_payload[1] = 0 # Waypoint index
command_payload[2:14] = struct.pack("3f", 300, 500, 80)
print(' '.join(format(byte, '08b') for byte in struct.pack(">3f", 300, 500, 80)))
print()
print(' '.join(format(byte, '08b') for byte in command_payload))

# Transport protocol layer
packet = bytes([0x00]) + cobs.encode(command_payload)
# print(packet)