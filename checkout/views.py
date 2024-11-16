from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm
from bag.contexts import bag_contents
from django.conf import settings

import stripe
import json

def checkout(request):
    """
    Display the checkout page and process the order.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    
    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    order_form = OrderForm()
    stripe_total = round(total * 100)
    stripe_total = round(total * 100)
    intent = None
    
    if stripe_secret_key:
        try:
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )
        except stripe.error.StripeError as e:
            messages.error(request, "There was an issue with the payment system. Please try again later.")
            
    
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret if intent else None,
        
        
    }
    
    return render(request, template, context)
