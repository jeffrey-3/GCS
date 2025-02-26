import struct

print(struct.unpack("B", bytes([len(payload)]))[0])