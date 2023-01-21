# Optimal Algorithm Web App - Capstone Project
## Pierre Alkubeh

### How to Deploy w/ Docker for Production
```
git clone https://github.com/pierre-minerva/capstone.git

#Follow this link to install Docker & Docker Compose: https://docs.docker.com/engine/install/ubuntu/

cd capstone
nano capsite/capsite/settings.py
#Add IP address to allowed hosts

docker compose -f docker-compose.prod.yml up -d --build
docker compose exec -it web python3 manage.py makemigrations
docker compose exec -it web python3 manage.py migrate
docker compose exec -itd web python3 manage.py dbinit
```