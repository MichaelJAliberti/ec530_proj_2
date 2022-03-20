from datetime import datetime


DATA_TEMPLATE = {
    "chat": {
        "ID":{
            "users": ["USER ID"],
            "messages": [{
                "timestamp": datetime.now(),
                "user": "USER ID",
                "payload": "" 
            }]
        },
    },
    "device": {
        "ID": {
            "timestamp": datetime.now(),
            "mac":"ff-ff-ff-ff-ff-ff",
            "value":145,
            "excess":120
        },
    },
    "user": {
        "ID": {
            "info":{
                "full_name": "John Doe",
                "email": "example@example.com",
                "dob": "1/1/2000",
                "gender": "male",
                "chats": ["CHAT ID"],
            },
            "chats": [],
        },
    },
}