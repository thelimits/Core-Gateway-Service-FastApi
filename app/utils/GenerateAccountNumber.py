import random
from datetime import datetime

TIMESTAMP_FORMAT = "%H%M%S%f"
RANDOM_STRING_LENGTH = 3
RANDOM_STRING_CHARS = "0123456789"

class GenerateAccountNumber:
    def __init__(self) -> None:
        pass
    
    def generate_random_string(self, length) -> str:
        random_string = ''.join(random.choice(RANDOM_STRING_CHARS) for _ in range(length))
        return random_string

    def generate_id(self) -> str:
        id = "5250"

        # Generate timestamp
        now = datetime.now()
        timestamp = now.strftime(TIMESTAMP_FORMAT)
        id += timestamp

        # Generate random string
        random_string = self.generate_random_string(RANDOM_STRING_LENGTH)
        id += random_string

        return id