# Flask Rest API for Education System

This repo consists of a RESTful api developed for a Smart Education System based on the requirements provided. 

## General Details
This api was written in Flask-Restx and the database is PostgreSQL. If you want to change the database please change the connection string `SQLALCHEMY_DATABASE_URI` accordingly

All the endpoints are jwt protected except for login. 

Swagger documentation is available for API testing. For the `Postman` users, please find the postman collection [here.](https://api.postman.com/collections/9004865-6be67543-7b49-4023-a6fa-5d71b30cc8e7?access_key=PMAT-01GTBKEE1V8VGRKRSZVM3GNQZY)

Admin user is automatically created and instructors can be created using admin.

Students and classes can be created by instructors. 

### Future Improvements

Unit tests and integration tests should be written in the ideal scenario (using pytest). However, due to time restriction they weren't written

The API can be deployed in a platform like Heroku.

There are some more validations can be implemented based on the requirement. This implementation consists only the basic validations.

Database design can be further improved to make APIs more dynamic.


## Setup Instructions 

This api was written in Flask. Python should be installed before setting up the project.

### Steps:

1. Clone the git [repository](https://github.com/Gihan-Liyanage/flask-rest-api.git) 
2. go to the folder
```bash
cd flask-rest-api
```
3. install virtualenv
```bash
pip install virtualenv
```
4. create a virtual environment
```bash
virtualenv venv
```
5. Activate the virtual environment
```bash
source venv/bin/activate
```
6. Install requirements from `requirements.txt`
```bash
pip install -r requirements.txt
```
6. Export the environment path variable
```bash
export FLASK_APP=src/
echo $FLASK_APP
```
7. Create .env file using `.env.sample`
8. Run `runserver.py` file
```bash
python runserver.py
```
> Development server will start and Swagger documentation will be available on `http://127.0.0.1:5000/`