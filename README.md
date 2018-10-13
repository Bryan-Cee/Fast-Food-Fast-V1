[![Build Status](https://travis-ci.org/Bryan-Cee/Fast-Food-Fast-V1.svg?branch=master)](https://travis-ci.org/Bryan-Cee/Fast-Food-Fast-V1) [![Coverage Status](https://coveralls.io/repos/github/Bryan-Cee/Fast-Food-Fast-V1/badge.svg?branch=challenge-3)](https://coveralls.io/github/Bryan-Cee/Fast-Food-Fast-V1?branch=challenge-3) [![Maintainability](https://api.codeclimate.com/v1/badges/515632750db64aa8bf45/maintainability)](https://codeclimate.com/github/Bryan-Cee/Fast-Food-Fast-V1/maintainability)

# Fast-Food-Fast-V1
Fast-Food-Fast is a food delivery service app for a restaurant.



#### How should this be manually tested?
- Clone the repository
- Initialize and activate a virtualenv
 ```
 $ virtualenv --no-site-packages env
 $ source env/sripts/activate
 ```
- Install the dependencies
 ```
 $ pip install -r requirements.txt
 ```
- Initialize environment variables
``` 
$ export FLASK_APP=run.py
$ export FLASK_ENV=development
$ export APP_SETTINGS=development
$ export ADMIN_PASSWORD=your_choice
$ export ADMIN_NAME=your_choice
$ export AMDIN_EMAIL=a_valid_email
```
- Run the development server
```
$ flask run
```
- Navigate to [http://localhost:5000](http://localhost:5000)

- Test all endpoints using postman
- Use Basic Auth for authorization

## Endpoints

Here is a list of all endpoints

| Endpoint                     | Functionality                 |
| ---------------------------- | ----------------------------- |
| GET   /api/v2/orders         | Get all orders                |
| GET   /api/v2/orders/orderid | Fetch a specific order        |
| POST   /api/v2/users/orders  | Place a new order             |
| GET   /api/v2/users/orders   | Get user order history        |
| PUT   /api/v2/orders/orderid | Update the status of an order |
| PUT   /api/v2/users/orderid  | Change the role of a user     |
| POST   /api/v2/menu          | Create a meal in the menu     |
| GET   /api/v2/menu           | Get all meals in the menu     |
| GET   /api/v2/auth/signup    | Signup for an account         |
| GET   /api/v2/auth/login     | login to an account           |

 ## Heroku
 https://immense-ocean-82555.herokuapp.com
 
 ## Running pylint
 - Install pylint
```
$ pip install pylint
```
 - Run the command with the filename as shown below
```
$ pylint filename.py
```  
