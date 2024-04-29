# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models.purchase_order import PurchaseOrder
import json


@csrf_exempt
def purchase_order_list(request):
    if request.method == 'GET':
        if 'vendor_id' in request.GET:
            vendor_id = request.GET['vendor_id']
            purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()

        data = []
        for po in purchase_orders:
            pos = {**po.__dict__}
            pos.pop('_state', None)
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            po_number = data.get('po_number')
            vendor_id = data.get('vendor_id')
            order_date = data.get('order_date')
            delivery_date = data.get('delivery_date')
            items = data.get('items')
            quantity = data.get('quantity')
            status = data.get('status')
            quality_rating = data.get('quality_rating')
            issue_date = data.get('issue_date')
            acknowledgment_date = data.get('acknowledgment_date')

            if po_number and vendor_id and order_date and delivery_date and items and quantity and status:
                purchase_order = PurchaseOrder.objects.create(po_number=po_number, vendor_id=vendor_id,
                                                              order_date=order_date, delivery_date=delivery_date,
                                                              items=items, quantity=quantity, status=status,
                                                              quality_rating=quality_rating, issue_date=issue_date,
                                                              acknowledgment_date=acknowledgment_date)
                return JsonResponse(
                    {'message': 'Purchase Order created successfully', 'po_number': purchase_order.po_number},
                    status=201)
            else:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def purchase_order_detail(request, pk):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=pk)
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({'error': 'Purchase Order not found'}, status=404)

    if request.method == 'GET':
        data = {**purchase_order.__dict__}
        data.pop('_state', None)
        return JsonResponse(data)
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for field in ['po_number', 'vendor_id', 'order_date', 'delivery_date', 'items', 'quantity', 'status',
                          'quality_rating', 'issue_date', 'acknowledgment_date']:
                if field in data:
                    setattr(purchase_order, field, data[field])
            purchase_order.save()
            return JsonResponse({'message': 'Purchase Order updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    elif request.method == 'DELETE':
        purchase_order.delete()
        return JsonResponse({'message': 'Purchase Order deleted successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
