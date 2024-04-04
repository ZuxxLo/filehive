# back-end API


## Steps to run the project:
1. Change Dir to the location of **docker-compose.yml** file
2. Open a Terminal/CMDLine (or in VScode) and run `docker-compose up --build`: in order to build and run the containers:
   - which are 2: DB container and django container
3. the cmd will install the required stuff and automate some stuff (u need to wait some-minutes bcz there are some db_checks)
4. after the containers are up, u can start working and the django-web-server will be running on http://localhost:8000
5. For any clarifications, or problems contact me asap
## Notes:
- In order to execute specially related to django there is 2 method:
   1. recommended-way: open a Terminal/CMDLine and run `docker exec -it django_container_id sh`: u got a shell and execute the cmds u want for example: `python manage.py runserver` or python manage.py migrate` or installing any python-package using pip
   2. 2nd-method: execute a cmd on the container using docker  : `docker-compose run django ur_cmd_here` for example: `docker-compose run django python manage.py migrate`
- regarding the venv file whether u are in windows or Linux, u need to create a virtual env for python pacakges in order to resolve the imports in vscode:
   - Linux: `source venv/bin/active`
   - Windows: in vscode terminal: `.\venv\bin\activate`
- For **NASSIM**: after u complete ur work and create data/rows/tables in the database and u verify that u completed all the functions as intended:
   1. store the database data:
       1. create a folder in the fixtures called based on the app/function u did:
       2. do the cmd: `python manage.py dumpdata ur_app_name > fixtures/ur_app_or_function_name/data.json`
       3. don't forget to apply migrations before that
   2. save the installed packages: access the django-container and do this commands in order to keep updating installed pacakges:
     - `rm requirements.txt`
     - `pip freeze -l > requirements.txt`
