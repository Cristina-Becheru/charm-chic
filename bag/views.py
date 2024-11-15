from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product




def view_bag(request):
    """ A view that renders the bag contents page """
    
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    product = get_object_or_404(Product, pk=item_id)
    try:
        quantity = int(request.POST.get('quantity'))
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quantity provided.')
        return redirect('view_bag')  

    size = request.POST.get('product_size', None)
    redirect_url = request.POST.get('redirect_url', 'view_bag') 
    bag = request.session.get('bag', {})

    if item_id in bag:
        if size:
            if isinstance(bag[item_id], dict) and size in bag[item_id]:
                bag[item_id][size] += quantity
                messages.success(request, f'Updated {product.name} ({size}) quantity in your bag.')
            else:
                if not isinstance(bag[item_id], dict):
                    bag[item_id] = {}
                bag[item_id][size] = quantity
                messages.info(request, f'Added {product.name} ({size}) to your bag.')
        else:
            if isinstance(bag[item_id], int):
                bag[item_id] += quantity
            else:
                bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity in your bag.')
    else:
        bag[item_id] = {size: quantity} if size else quantity
        messages.success(request, f'Added {product.name} to your bag.')

    request.session['bag'] = bag
    return redirect(redirect_url)
