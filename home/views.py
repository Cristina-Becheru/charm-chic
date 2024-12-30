from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')

def about(request):
    return render(request, 'info/about.html')

def contact(request):
    """Handle contact form submissions."""
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Compose the email
        subject = f"Contact Us Message from {name}"
        email_message = f"""
        Name: {name}
        Email: {email}
        Phone: {phone if phone else 'Not Provided'}
        Message:
        {message}
        """

        try:
            # Send email to admin
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact_confirmation')  
        except Exception as e:
            messages.error(request, "An error occurred while sending your message. Please try again later.")
            return redirect('contact')

    return render(request, 'info/contact.html')

def contact_confirmation(request):
    """A view to display the contact confirmation page."""
    return render(request, 'info/contact_confirmation.html')