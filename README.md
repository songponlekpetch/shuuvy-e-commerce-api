# shuuvy-e-commerce-api
Api for shuuvy-e-commerce

## Run
1. Create ```docker-compose.dev.yml``` file to define enviroment vaiable
2. Build docker image in local ```docker-compose -f docker-compose.dev.yml build```
3. Migrate database with ```docker-compose -f docker-compose.dev.yml run app sh -c "python manage.py wait_for_db && python manage.py migrate" ```
3. Create admin user for using Django Admin ```docker-compose -f docker-compose.dev.yml run --rm app python manage.py createsuperuser```
2. Run ```docker-compose -f docker-compose.dev.yml up``` to start API

## Swagger
http://localhost:8989/api/docs/

## Django Admin
http://localhost:8989/admin/

## Diagram
### Usecase 
https://lucid.app/lucidchart/d2f65adc-68ff-41d2-9a22-16872a67b53b/edit?viewport_loc=4%2C73%2C2385%2C1201%2C0_0&invitationId=inv_9173cdba-9801-4091-a33b-18a362717903
### ER 
https://lucid.app/lucidchart/527c4315-28e5-4208-b6d2-19609fc0fb5c/edit?viewport_loc=-696%2C-177%2C2604%2C1312%2C0_0&invitationId=inv_1d620b55-b823-4b1c-b4ac-41fbee06a8be
