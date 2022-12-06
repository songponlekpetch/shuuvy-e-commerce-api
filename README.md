# shuuvy-e-commerce-api
Api for shuuvy-e-commerce

Run
1. Create ```docker-compose.dev.yml``` file to define enviroment vaiable
2. Build docker image in local ```docker-compose -f docker-compose.dev.yml build```
3. Create admin user for using Django Admin ```docker-compose -f docker-compose.dev.yml run --rm app python manage.py createsuperuser```
2. Run ```docker-compose -f docker-compose.dev.yml up``` to start API

Swagger
http://localhost:8989/api/docs/

Django Admin
htpp://locahost:8989/admin/
