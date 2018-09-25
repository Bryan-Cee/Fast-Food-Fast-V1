[![Build Status](https://travis-ci.org/Bryan-Cee/Fast-Food-Fast-V1.svg?branch=master)](https://travis-ci.org/Bryan-Cee/Fast-Food-Fast-V1) [![Coverage Status](https://coveralls.io/repos/github/Bryan-Cee/Fast-Food-Fast-V1/badge.svg)](https://coveralls.io/github/Bryan-Cee/Fast-Food-Fast-V1) [![Maintainability](https://api.codeclimate.com/v1/badges/515632750db64aa8bf45/maintainability)](https://codeclimate.com/github/Bryan-Cee/Fast-Food-Fast-V1/maintainability)

# Fast-Food-Fast-V1
Fast-Food-Fast is a food delivery service app for a restaurant.



#### How should this be manually tested?
- Clone the repository
- Initialize and activate a virtualenv
 ```
 $ virtualenv --no-site-packages env
 $ cd env/sripts/activate
 ```
- Install the dependencies
 ```
 $ pip install -r requirements.txt
 ```
- Initialize environment variables
``` 
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
```
- Run the development server
```
$ python flask run
```
- Navigate to [http://localhost:5000](http://localhost:5000)

- Test all endpoints using postman


## Endpoints

Here is a list of all endpoints

| Endpoint                       | Functionality                 |
| ------------------------------ | ----------------------------- |
| GET   /api/v1/orders           | Get all orders                |
| GET   /api/v1/orders/orderid | Fetch a specific order        |
| POST   /api/v1/orders          | Place a new order             |
| PUT   /api/v1/orders/orderid | Update the status of an order |
| POST   /api/v1/menu            | Create a meal in the menu     |
| GET   /api/v1/menu             | Get all meals in the menu     |
 
 ## Heroku
 https://immense-ocean-82555.herokuapp.com
 
 ## Running pylint
 - Install pylint
```
$ pip install pylint
```
 - Run it against a file you want to check
```
$ pylint filename.py
```  