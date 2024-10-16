from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm, ContactFormLoggedIn


def contact(request):
    msg_sent = False
    context = {
        "contact_form": ContactForm(),
        "contact_form_logged_in": ContactFormLoggedIn(),
        "msg_sent": msg_sent
    }
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        contact_form_logged_in = ContactFormLoggedIn(request.POST)
        if "contact_form" in request.POST:
            if contact_form.is_valid():
                message = f"""
        Name: {contact_form.cleaned_data['name']}
        Email: {contact_form.cleaned_data['email']}
        
        {contact_form.cleaned_data['message']}
                    """
                email = EmailMessage(
                    subject=contact_form.cleaned_data['contact_reason'],
                    body=message,
                    from_email="placeholder",
                    to=['robertworsham01@gmail.com']
                )
                try:
                    email.send()
                    msg_sent = True
                except Exception as e:
                    msg_sent = False
                    print(f"Error sending email: {e}")
        else:
            contact_form = ContactForm()

        if "contact_form_logged_in" in request.POST:
            if contact_form_logged_in.is_valid():
                message = f"""
            Name: {request.user.username}
            Email: {request.user.email}
    
            {contact_form_logged_in.cleaned_data['message']}
                        """
                email = EmailMessage(
                    subject=contact_form_logged_in.cleaned_data['contact_reason'],
                    body=message,
                    from_email="placeholder",
                    to=['robertworsham01@gmail.com']
                )
                try:
                    email.send()
                    msg_sent = True
                except Exception as e:
                    msg_sent = False
                    print(f"Error sending email: {e}")
        else:
            contact_form_logged_in = ContactFormLoggedIn()

    return render(request, 'contact.html', context)
