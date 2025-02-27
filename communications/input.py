from data_structures.flight_data_struct import FlightData
import time
import threading

class PayloadQueue:
    def __init__(self, timeout=5):
        self.queue = []  # List of (payload, expiry_time)
        self.timeout = timeout
        self.lock = threading.Lock()
    
    def add_payload(self, payload):
        """Adds a payload to the queue with a timeout if it doesn't already exist."""
        with self.lock:
            if any(p == payload for p, _ in self.queue):
                return
            expiry_time = time.time() + self.timeout
            self.queue.append((payload, expiry_time))
    
    def remove_payload(self, payload):
        """Removes a payload if it exists in the queue."""
        with self.lock:
            self.queue = [(p, t) for p, t in self.queue if p != payload]
    
    def get_payload(self):
        """Retrieves the next payload to send through radio, if available."""
        with self.lock:
            if self.queue:
                return self.queue[0][0]  # Return the first payload in the queue
        return None
    
    def cleanup(self):
        """Removes expired payloads from the queue."""
        current_time = time.time()
        with self.lock:
            self.queue = [(p, t) for p, t in self.queue if t > current_time]
    
    def run_cleanup(self, interval=1):
        """Runs cleanup periodically in a background thread."""
        def _loop():
            while True:
                time.sleep(interval)
                self.cleanup()
        
        thread = threading.Thread(target=_loop, daemon=True)
        thread.start()

class Input():
    def __init__(self):
        self.flight_data = FlightData()

        # When command needs to be sent, it gets added here
        # When it recieves acknowledgement, it gets removed
        self.command_queue = PayloadQueue()
        self.command_queue.run_cleanup()
    def send(self):
        pass
    def append_queue(self, payload):
        self.command_queue.add_payload(payload)