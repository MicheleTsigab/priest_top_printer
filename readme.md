# Priest Top Api
### An effective api that allows for asynchronous creation(non blocking request-response cycle) of invoice pdf based on json input and an admin page to filter.
## Built With

* Python 3.10
* Django 4.1.2
* Redis
* Wkhtmltopdf
* Bootstrap
* Django-rq

## Installation

```sh
 git clone https://github.com/MicheleTsigab/priest_top_printer 
 ```
```sh
docker compose up --build
```
```sh
pip install -r requirements.txt
```
## USAGE
### open First Terminal
```sh
docker compose up 
```
### Second Terminal
```sh 
python manage.py rqworker default
```
### Third Terminal

* `python manage.py createsuperuser`
* `python manage.py makemigrations`
* `python manage.py migrate`

```sh
 python manage.py runserver 
 ```
 * `Go to Admin page and Create a printer`

## Refer the [documentation](https://documenter.getpostman.com/view/19708900/2s83ziMics) for available apis.
 * `Have Fun :)`
## Demo
#### Generated simple invoice
<img src="demo/client.png" width="400" height="300" alt="demo">


