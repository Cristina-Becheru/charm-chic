from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    
    for item_id, item_data in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        
        if isinstance(item_data, dict): 
            for size, quantity in item_data.items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'product': product,
                    'quantity': quantity,
                    'total_price': quantity * product.price,
                    'size': size  
                })
        else: 
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'product': product,
                'quantity': item_data,
                'total_price': item_data * product.price,
                'size': None  
            })
    
     # Delivery cost and free delivery threshold 
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = total + delivery

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
    
    return context   