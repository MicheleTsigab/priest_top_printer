from base64 import b64encode
import requests
from django.template.loader import render_to_string
from .models import Check 

WKHTMLTOPDF='http://localhost:8001'

def generate_pdf(check_type, check_id, check_path, order):
    to=choose_type(check_type)
    order['check_type'] = to
    html_string = render_to_string(f'generator/{to}.html', {'order': order})
    html = b64encode(bytes(html_string, encoding='UTF-8')).decode('UTF-8')
    response = requests.post(WKHTMLTOPDF, json={'contents': html})
    update_check(check_id,'rendered')
    write_to_file(check_path,response.content)

def choose_type(check_type):
    return 'client' if check_type=='client' else 'kitchen'

def write_to_file(path,content):
    with open(path, 'wb') as f:
        f.write(content)
        
def update_check(id,status):
    Check.objects.filter(id=id).update(status=status)