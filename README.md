# Rightmove Flask API


### Prerequisites

* Python 3.6.5
* virtualenv
* Docker

### Installing

```
git clone https://github.com/Japolk/rightm_flask.git
```
create and activate virtualenv (optional)
```
virtualenv venv
soruce venv/bin/activate
```
install required modules from requirements.txt:
```
pip install -r requirements.txt
```
Make flask_app great again:
```
export FLASK_APP=api
```

## Running

Init Database:
```
flask init-db
```
Run application:
```
flask run 
```
## API

Application has 3 endpoints:
* [GET]  '/':            Greeting page 
* [POST] '/api/add/':    Add new rightmove_urls.
  Parameters: 'urls': one string or list of strings
* [GET] '/api/csv/':     Return csv file with DB-data 

## Docker
You can make image with Docker file:
```
docker build -t rightm_flask:latest .
```
Or pull from Docker Hub:
```
docker pull kvartira92/rightm_flask
```
Run Docker container:
```
docker run -d -p 5000:5000 --rm -e REQUESTS_LIMIT=10 rightm_flask:latest

```


## Authors
* Ishchenko Alexey

