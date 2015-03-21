from uuid import uuid1


def generate_id():
    """Generate 32 digit random UUID and convert them to strings"""
    return str(uuid1())
