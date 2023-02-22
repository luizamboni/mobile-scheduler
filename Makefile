# WORKERS=localhost:8001,localhost:8002
DEV_WORKERS='http://localhost:8001,http://localhost:8002'

install:
	pip install -r app/requirements.txt
	mypy --install-types --non-interactive

start-worker-1:
	bash -c "PORT=8001 WORKERS='' exec -a worker-1 python3 app/server.py"

kill-worker-1:
	pkill -f worker-1

start-worker-2:
	bash -c "PORT=8002 WORKERS='' exec -a worker-2 python3 app/server.py"

kill-worker-2:
	pkill -f worker-2

# start-master:
# 	bash -c "WORKERS=${DEV_WORKERS} exec -a master python3 app/server.py"

start-master:
	bash -c "WORKERS='' exec -a master python3 app/server.py"


kill-master:
	pkill -f master