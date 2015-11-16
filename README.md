# currency_converter
Django currency converter website
##SOAP servers
This application makes use of 2 SOAP servers:  
###Kowabunga  
```$ http://currencyconverter.kowabunga.net/converter.asmx?WSDL```  
Good API with several possibilities. The values that get returned are not always trustworthy. 
###Webservicex
```$ http://www.webservicex.net/currencyconvertor.asmx?WSDL```  
This SOAP server only provides a conversion rate between 2 currencies.  
Webservicex is used as a backup in case Kowabunga does not return a value.  
##Database
For the convenience of sharing information I used a SqLite3 database.  
The database already provides the currencies and the currency pairs.  
###Caching
Because retrieving the data from the server is a relatively slow process the rates get stored in the database. 
This happens every time there is a call from the website for a currency pair. 
In case the data is not stored in the database it might take a while for the programme to retrieve the data from the soap servers. 

##Installation prerequisites
I assume that the user of the application has a basic knowledge of Python and the Linux terminal.  
This project is created in Python 3.4  
Git and pip should also be installed.   
### Install Git  
```sudo apt-get update```  
```sudo apt-get install git```  
```git config --global user.name "YOUR NAME"```  
```git config --global user.email "YOUR EMAIL ADDRESS"```
### Install pip 
```sudo apt-get install python-pip```  

##Installation
###Install Virtualenv
The project was made in a Python Virtual Environment.  
To run the project you first need to install:  
```pip install virtualenv```  

###Clone Currency Converter Project
Clone the project from github  
```$ git clone https://github.com/johanvergeer/currency_converter.git```  

### Replace the bin directory
Just to be sure all the dependencies and binaries are correct you should replace the bin directory
1. create a new virtualenv outside the project root directory  
```$ virtualenv -p /usr/bin/python3.4 venv```  
2. remove the bin directory from the project root directory  
3. move the bin directory from venv directory to the project root directory  
4. Change virtualenv path  inside bin/activate  
```$ VIRTUAL_ENV="/home/username/directory/to/virtualenv"```  
## Run the application
1. Move into the application root folder:  
```cd currency_converter```  
2. Run VirtualEnv:  
```source bin/activate```
3. Move into Django root folder:  
```cd currency_converter```
4. Run Django server:  
```python manage.py runserver```
5. You can open the application from your webbrowser using the ip address.  
ex. ```127.0.0.1:8000```

##Login and use the application
One you have created a user you can login and use the application. 
The user information is stored in the database. 

###Login to admin panel
1. create a superuser from the terminal  
```python manage.py createsuperuser --username=joe --email=joe@example.com```
2. open the admin panel in the web browser  
ex. ```127.0.0.1:8000/admin```
