# ec530_proj_2

## Branching Strategy

All branches created should correspond to and fulfill the requirements of a specific Github Issue. 
Issues should identify a feature to add or a bug to be resolved.

Before merging to main, a branch must include the implementation of the desired feature as well as a corresponding test.
If a branch includes modifications to code in the `/src` directory, these changes should be documented in `changelog.md`

---

## Queuing System

All of the work for the task queuing system may be found under `src/speech_to_text`.

Celery and Rabbitmq are used as the the python library and broker, respectively, with and `rpc` backend to store task results.

Unfortunately, despite attempting to follow multiple tutorials, Celery workers were never able to finish tasks despite receiving them. This likely has to do with attempting to run Celery and Rabbitmq on a Windows System rather than on  Mac or Linux.

Ultimately, I felt it wise to turn to  the Final project due to time constrtaints, leaving this queuing system unfinished.

---

## API Schema

### `/chats`:

```
{
    "<id>": {
        "users": [str],
        "messages": [
            {
                "timestamp": datetime.datetime,
                "user": str,
                "payload": str,
            }
        ]
    }
}
```

### `/chats/<id>`:

```
{
    "users": [str],
    "messages": [
        {
            "timestamp": datetime.datetime,
            "user": str,
            "payload": str,
        }
    ]
}
```

### `/chats/<id>/users`:

```
[str]
```

### `/chats/<id>/messages`:

```
[
    {
        "timestamp": datetime.datetime,
        "user": str,
        "payload": str,
    }
]
```

### `/devices`:

```
{
    "<id>": {
        "timestamp": datetime.datetime,
        "mac": str,
        "value": int,
    }
}
```

### `/devices/<id>`:

```
{
    "timestamp": datetime.datetime,
    "mac": str,
    "value": int,
}
```

### `/users`:

```
{
    "<id>": {
        "info": {
            "full_name": str,
            "email": str,
            "dob": str,
            "gender": str,
        },
        "chats": [str]
    }
}
```

### `/users/<id>`:

```
{
    "info": {
        "full_name": str,
        "email": str,
        "dob": str,
        "gender": str,
    },
    "chats": [str]
}
```

### `/users/<id>/info`:

```
{
    "full_name": str,
    "email": str,
    "dob": str,
    "gender": str,
}
```

### `/users/<id>/chats`:

```
[str]
```
