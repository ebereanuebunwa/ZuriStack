from uuid import uuid4


# Generate a unique id
def generate_random_id(length=5):
    random_id = str(uuid4())
    return random_id[:length]