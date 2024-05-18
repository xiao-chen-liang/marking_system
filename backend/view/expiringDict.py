import threading
import time

class ExpiringDict:
    def __init__(self, expiration_time=600):
        self.data = {}
        self.expiration_time = expiration_time
        self.lock = threading.Lock()
        self.cleanup_thread = threading.Thread(target=self._cleanup, daemon=True)
        self.cleanup_thread.start()

    def _cleanup(self):
        while True:
            time.sleep(1)
            with self.lock:
                current_time = time.time()
                keys_to_delete = [key for key, (_, timestamp) in self.data.items() if current_time - timestamp > self.expiration_time]
                for key in keys_to_delete:
                    del self.data[key]

    def set(self, key, value):
        with self.lock:
            self.data[key] = (value, time.time())

    def get(self, key):
        with self.lock:
            if key in self.data:
                value, timestamp = self.data[key]
                if time.time() - timestamp < self.expiration_time:
                    return value
                else:
                    del self.data[key]
        return None

    def __contains__(self, key):
        with self.lock:
            if key in self.data:
                value, timestamp = self.data[key]
                if time.time() - timestamp < self.expiration_time:
                    return True
                else:
                    del self.data[key]
        return False

    def __delitem__(self, key):
        with self.lock:
            if key in self.data:
                del self.data[key]

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

# # Example usage:
# exp_dict = ExpiringDict()
#
# # Set key-value pairs
# exp_dict.set('key1', 'value1')
# exp_dict['key2'] = 'value2'
#
# # Get key-value pairs
# print(exp_dict.get('key1'))  # Outputs 'value1'
# print(exp_dict['key2'])      # Outputs 'value2'
#
# # Check if keys exist
# print('key1' in exp_dict)  # Outputs True
# print('key3' in exp_dict)  # Outputs False
#
# # Wait for more than 5 minutes (300 seconds)
# time.sleep(305)
#
# # Attempt to get expired keys
# print(exp_dict.get('key1'))  # Outputs None
# print(exp_dict['key2'])      # Outputs None
#
# # Check if keys exist after expiration
# print('key1' in exp_dict)  # Outputs False
# print('key2' in exp_dict)  # Outputs False
