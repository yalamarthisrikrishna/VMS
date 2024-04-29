from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models.vendor import Vendor
import json


@csrf_exempt
def vendor_list(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        data = []
        for vendor in vendors:
            vendor_details = {**vendor.__dict__}
            vendor_details.pop('_state', None)
            data.append(vendor_details)
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            contact_details = data.get('contact_details')
            address = data.get('address')

            if name and contact_details and address:
                vendor = Vendor.objects.create(name=name, contact_details=contact_details, address=address)
                return JsonResponse({'message': 'Vendor created successfully', 'id': vendor.id}, status=201)
            else:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def vendor_detail(request, pk):
    try:
        vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor not found'}, status=404)

    if request.method == 'GET':
        data = {**vendor.__dict__}
        data.pop('_state', None)
        return JsonResponse(data)
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for field in ['name', 'contact_details', 'address', 'vendor_code']:
                if field in data:
                    setattr(vendor, field, data[field])
            vendor.save()
            return JsonResponse({'message': 'Vendor updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    elif request.method == 'DELETE':
        vendor.delete()
        return JsonResponse({'message': 'Vendor deleted successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
