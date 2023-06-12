from pydantic import BaseModel

# Message model
class Message(BaseModel):
    content: str