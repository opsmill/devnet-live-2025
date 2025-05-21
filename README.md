
# how to build a production-grade automation platform with Infrahub

This project was created during a 2 parts stream with Adrian from Cisco DevNet to showcase how to build a production-grade automation platform with Infrahub.

- Part 1 (April 2025) : https://www.youtube.com/watch?v=E3KLBzyNBrU
- Part 2 (May 2025) : https://www.youtube.com/watch?v=SlncONsRyX4


## Create your environment

### 1. Initialize uv project

```shell
uv init devnet-live-2025
cd devnet-live-2025
uv add infrahub-sdk --extra all
```

### 2. Create project structure

```shell
mkdir schemas
mkdir data
mkdir templates
mkdir tests
```

### 3. Start infrahub

Option 1 - start with a one liner command
```shell
curl https://infrahub.opsmill.io | docker compose -p infrahub -f - up -d
```


Option 2 - Copy the docker compose file locally and start docker compose
```shell
curl https://infrahub.opsmill.io > docker-compose.yaml
docker compose up -d
```

Stop Infrahub (assuming you used Option 2)
```shell
docker compose down -v
```

### Configure Infrahubctl
```shell
source .venv/bin/activate
```

```shell
export INFRAHUB_USERNAME=admin
export INFRAHUB_PASSWORD=infrahub
export INFRAHUB_ADDRESS=http://localhost:8000
```

```shell
infrahubctl info
```
