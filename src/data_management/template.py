class Template:
    def __init__(self, *, name, data):
        self.name = name
        self.data = data


DEVICE_TEMPLATE = Template(
    name="device",
    data={
        "mac":"ff-ff-ff-ff-ff-ff",
        "value":145,
        "excess":120
    }
)

USER_TEMPLATE = Template(
    name="user",
    data={
        "full_name": "John Doe",
        "email": "example@example.com",
        "dob": "1/1/2000",
        "gender": "male",
        "chat_ids": [],
    }
)