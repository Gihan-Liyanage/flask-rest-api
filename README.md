# Flask Rest API for Education System

This repo consists of a RESTful api developed for a Smart Education System based on the requirements provided. 

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