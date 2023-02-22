MAC - module app scheduler
===

### To create a new task
```
POST /
{
    "command": "python3 ./app/app.py",
    "setup_cmd": "pip install -r ./app/requirements.txt",
    "env": {
        "TELEGRAM_BOT_TOKEN": "xxx"
    },
    "repo": "https://github.com/luizamboni/bombot.git",
    "name": "pybot",
    "requirements": {
        "memory_in_mb": 400
    }
}
```
the `repo` will be cloned to a folder with same name of `name`

### To list tasks and server statistics
```
GET /
```

### To stop a proccess
```
POST /app/pybot/stop
```