### Description
The application where users can publish somthing, add other users' blogs to favorites, and subscribe to publications from other authors.

## Technologies:
- Django
- Python
- Docker

## Installation
- Clone the repository:
```
git clone git@github.com:HukumaBob/yandex_test.git
```

- Collect images
```
cd ../backend  
docker build -t username/blog_backend .
cd ../nginx  
docker build -t username/blog_nginx . 
```
- Building Containers:
From the 'infra/' directory, deploy the containers using docker-compose:
```
docker-compose up -d --build
```
- Apply migrations:
```
docker-compose exec backend python manage.py migrate
```
- Create superuser:
```
docker-compose exec backend python manage.py createsuperuser
```
- Collect static files:
```
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend cp -r /app/static/. /static/
```
- Run the command:
```
docker-compose exec backend python manage.py generate_data

```
### Preparing for Project Deployment on a Remote Server:

Create the .env file in the 'infra' directory:
```
ALLOWED_HOSTS=yourhost 158.160.xxx.xxx 127.0.0.1 localhost backend
SECRET_KEY=yoursecretkey
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yoursecretpassword
POSTGRES_DB=postgres
DB_HOST=db
DB_PORT=5432
```