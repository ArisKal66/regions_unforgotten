# Refresh Procedure for Northwind Database
## 1. Stop containers

From project's root: stops and removes the containers, but not the volumes
```bash
docker-compose -f docker/docker-compose.yml down
```

## 2. Remove the persisted volume, initially check volumes, then clean persistence
```bash
docker volume ls
docker volume rm < volume name >
```

## 3. Restart containers, to bring everything back up/refresh data volume
```bash
docker-compose -f docker/docker-compose.yml up --build
```

## `.sh` file for regular refreshes
```bash
docker-compose down
docker volume rm < volume name >
docker-compose up --build
```