from django_rq import enqueue
from .models import Check, Printer
from .pdf import generate_pdf
def create_task(body_data):
    kitchen_printer = Printer.objects.get(point_id=body_data['point_id'],
                                          check_type='kitchen')                                   
    kitchen_path = f'media/pdf/{body_data["id"]}_kitchen.pdf'

    kitchen_check = Check.objects.create(printer_id=kitchen_printer, 
                                        type='kitchen', 
                                        order=body_data,
                                        status='new', pdf_file=kitchen_path)

    enqueue(generate_pdf, 'kitchen', kitchen_check.id, kitchen_path, body_data)

    client_printer = Printer.objects.get(point_id=body_data['point_id'], 
                                        check_type='client')
    client_path = f'media/pdf/{body_data["id"]}_client.pdf'

    client_check = Check.objects.create(printer_id=client_printer,
                                        type='client', 
                                        order=body_data, 
                                        status='new', pdf_file=client_path)
    enqueue(generate_pdf, 'client', client_check.id, client_path, body_data)