import struct
import json
from typing import NamedTuple

class BinaryStruct:
    """
    A modular class to handle binary data unpacking, packing, and setting data with multipliers.
    The unpacked data is stored internally as a namedtuple.
    """
    def __init__(self, json_file_path: str, endianness: str = '='):
        """
        Initialize the BinaryStruct with a JSON file containing field definitions.

        :param json_file_path: The path to the JSON file containing the field definitions.
        :param endianness: The endianness character (e.g., '=' for native, '<' for little-endian, '>' for big-endian).
                           Use '=' to disable padding and enforce tight packing.
        """
        # Load the JSON file
        with open(json_file_path, 'r') as file:
            fields = json.load(file)

        # Validate the JSON structure
        if not isinstance(fields, list):
            raise ValueError("JSON file must contain a list of field definitions.")

        # Initialize fields
        self.fields = fields
        self.format_string = endianness + ''.join(field['type'] for field in fields)  # Build the format string
        self.field_names = tuple(field['name'] for field in fields)  # Extract field names
        self.multipliers = {field['name']: field.get('multiplier', 1) for field in fields}  # Extract multipliers
        self.struct_size = struct.calcsize(self.format_string)
        self._data = None  # Internal storage for the unpacked namedtuple

    def unpack(self, data: bytes):
        """
        Unpack binary data into a namedtuple and store it internally.
        Applies multipliers to scale the data.

        :param data: The binary data to unpack.
        """
        if len(data) != self.struct_size:
            raise ValueError(f"Data size ({len(data)}) does not match struct size ({self.struct_size})")

        # Unpack the data
        unpacked_data = struct.unpack(self.format_string, data)

        # Apply multipliers to scale the data
        scaled_data = []
        for field, value in zip(self.fields, unpacked_data):
            scaled_value = value * field.get('multiplier', 1)  # Multiply by multiplier if it exists
            scaled_data.append(scaled_value)

        # Create a namedtuple dynamically
        StructTuple = NamedTuple('StructTuple', zip(self.field_names, scaled_data))
        self._data = StructTuple(*scaled_data)  # Store the namedtuple internally

    def pack(self) -> bytes:
        """
        Pack the internally stored namedtuple back into binary data.
        Applies multipliers to scale the data.

        :return: Packed binary data.
        """
        if self._data is None:
            raise ValueError("No data has been unpacked or set yet.")

        # Apply multipliers to scale the data
        scaled_data = []
        for field, value in zip(self.fields, self._data):
            scaled_value = value / field.get('multiplier', 1)  # Divide by multiplier if it exists
            scaled_data.append(scaled_value)

        # Pack the scaled data
        return struct.pack(self.format_string, *scaled_data)

    def set_data(self, **kwargs):
        """
        Set the internal data using keyword arguments.

        :param kwargs: Field names and their corresponding values.
        """
        # Validate that all fields are provided
        if set(kwargs.keys()) != set(self.field_names):
            raise ValueError(f"Expected fields: {self.field_names}, got: {list(kwargs.keys())}")

        # Create a namedtuple dynamically
        StructTuple = NamedTuple('StructTuple', zip(self.field_names, self.field_names))
        self._data = StructTuple(**kwargs)  # Store the namedtuple internally

    @property
    def data(self):
        """
        Get the internally stored namedtuple.

        :return: The namedtuple containing the unpacked or set data.
        """
        if self._data is None:
            raise ValueError("No data has been unpacked or set yet.")
        return self._data

    def __repr__(self):
        return (f"BinaryStruct(format={self.format_string}, fields={self.field_names}, "
                f"size={self.struct_size}, data={self._data}, multipliers={self.multipliers})")

class TelemetryPayload(BinaryStruct):
    def __init__(self):
        super().__init__("communication/telemetry_format.json")

class WaypointPayload(BinaryStruct):
    def __init__(self):
        super().__init__("communication/waypoint_format.json")