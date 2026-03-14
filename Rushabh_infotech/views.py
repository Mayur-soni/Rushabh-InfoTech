from django.conf import settings
from django.contrib.sites import requests
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, redirect
import threading
from django.template.loader import render_to_string

from Rushabh_infotech.models import Service, ContactMessage


def home(request):
    return render(request, 'index.html')
def services(request):
    return render(request, 'services.html')
def about(request):
    return render(request, 'about.html')
def why_us(request):
    return render(request, 'why_us.html')
def contact(request):
    return render(request, 'contact.html')
def legal(request):
    return render(request, 'legal.html')

def services_view(request):
    services = Service.objects.filter(
        is_active=True
    ).prefetch_related("sub_services")

    return render(request, "services.html", {
        "services": services
    })


def contact_view(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        service = request.POST.get("service")
        message = request.POST.get("message")

        # Save message in database
        ContactMessage.objects.create(
            full_name=name,
            email=email,
            phone=phone,
            service_interest=service,
            message=message
        )

        subject = "We Received Your Request - Rushabh InfoTech"

        html_content = f"""
        <html>
        <body style="font-family:Arial;background:#f4f6f9;padding:40px;">
        <div style="max-width:600px;margin:auto;background:#ffffff;padding:30px;border-radius:10px;">
        <h2 style="color:#1d4ed8;">Rushabh InfoTech</h2>
        <p>Hi <strong>{name}</strong>,</p>
        <p>Thank you for contacting us regarding <b>{service}</b>.</p>
        <p>Our team will contact you shortly.</p>
        </div>
        </body>
        </html>
        """

        # EMAIL THREAD FUNCTION
        def send_email():

            try:
                email_message = EmailMultiAlternatives(
                    subject,
                    "",
                    settings.DEFAULT_FROM_EMAIL,
                    [email]
                )

                email_message.attach_alternative(html_content, "text/html")
                email_message.send()

                send_mail(
                    "🚨 New Contact Message Received",
                    f"""
Name: {name}
Email: {email}
Phone: {phone}
Service: {service}

Message:
{message}
""",
                    settings.DEFAULT_FROM_EMAIL,
                    ["mktg.rushabhinfotech@gmail.com"],
                    fail_silently=True
                )

            except Exception as e:
                print("Email Error:", e)

        # RUN THREAD
        threading.Thread(target=send_email).start()

        return redirect("contact")

    return render(request, "contact.html")

