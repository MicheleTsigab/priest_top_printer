import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Check, Printer
from .tasks import create_task

@csrf_exempt   
def create_checks(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('UTF-8')
        try:
            body_data = json.loads(body_unicode)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        try:
            order_id=body_data['id']
            point_id=body_data['point_id']
        except KeyError:
            return JsonResponse({'error':'Please provide an order ID and point Id'},status=400)
        if Check.objects.filter(order__id=order_id).exists(): 
            return JsonResponse({"error": "check already exists"}, status=400)
        if not Printer.objects.filter(point_id=point_id).exists():
            return JsonResponse({"error": "No printers for this point"}, status=400)
        
        #async task
        create_task(body_data)
        return JsonResponse({"sucess": "check is being created"}, status=200)
    return JsonResponse({"error": "Bad Method, use Post"}, status=400)
        

def checks(request):    
    if request.method == 'GET':
        try:
            api_key = request.GET['api_key']
        except KeyError:
            return JsonResponse({"error": "Provide an api_key as parameter"}, status=400)
        
        try:
            printer = Printer.objects.get(api_key=api_key)
        except Printer.DoesNotExist:
            return JsonResponse({"error": "Printer Doesnot Exist"}, status=404)
        
        rendered_checks = Check.objects.filter(printer_id=printer, status='rendered')
        checks = []
        for check in rendered_checks:
            checks.append({"id": check.id})
        
        return JsonResponse({"checks": checks}, status=200)
    return JsonResponse({"error": "Bad Method"}, status=400)


def get_check_pdf(request):
    if request.method == 'GET':
        try:
            api_key = request.GET['api_key']
        except KeyError:
            return JsonResponse({"error": "Provide api_key as parameter"}, status=400)

        try:
            check_id = int(request.GET['check_id'])
        except KeyError:
            return JsonResponse({"error": "Check Doesnot Exist"}, status=404)
        
        try:
            printer = Printer.objects.get(api_key=api_key)
        except Printer.DoesNotExist:
            return JsonResponse({"error": "Invalid API"}, status=401)

        try:
            check = Check.objects.get(printer_id=printer, id=check_id)
        except Check.DoesNotExist:
            return JsonResponse({"error": "Check doesnot Exist"}, status=400)
        
        if check.status == 'new':
            return JsonResponse({"error": "Not Rendered into Pdf yet."}, status=400)
        
        check_path = check.pdf_file.path
        with open(check_path, 'rb') as f:
            pdf = f.read()
            
        response = HttpResponse(pdf, headers={
                'Content-Type': 'application/pdf',
                'Content-Disposition': 
                f'attachment; attachment;filename={check_path}'}, status=200)
        Check.objects.filter(id=check_id).update(status='printed')
        return response
    return JsonResponse({"error": "Bad Method"}, status=400)