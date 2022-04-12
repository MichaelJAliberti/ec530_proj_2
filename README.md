# ec530_proj_2

## Branching Strategy

All branches created should correspond to and fulfill the requirements of a specific Github Issue. 
Issues should identify a feature to add or a bug to be resolved.

Before merging to main, a branch must include the implementation of the desired feature as well as a corresponding test.
If a branch includes modifications to code in the `/src` directory, these changes should be documented in `changelog.md`

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
