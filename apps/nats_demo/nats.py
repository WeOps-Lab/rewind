import nats_client
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str


@nats_client.register
def hello_message(message: str, token: str, dict_example: dict):
    user = User(id=1, name="John Doe", email="john.doe@example.com")
    return {
        'message': message,
        'token': token,
        'dict_example': dict_example,
        'user': user.json()
    }
