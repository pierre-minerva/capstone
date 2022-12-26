# Optimal Algorithm Web App - Capstone Project
## Pierre Alkubeh

### How to Deploy w/ Docker for Production
```
docker compose -f docker-compose.prod.yml up -d --build
docker exec web python3 optalg/db_initialization.py
```

### How to Deploy w/ Docker For Development
```
docker compose up -d --build
docker exec web python3 optalg/db_initialization.py
```
