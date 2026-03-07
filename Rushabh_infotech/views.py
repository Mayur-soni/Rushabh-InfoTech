from django.conf import settings
from django.contrib.sites import requests
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import render, redirect

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

    # ✅ GET Request (Page Load)
    if request.method == "GET":
        return render(request, "contact.html")

    # ✅ POST Request (Form Submit)
    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        service = request.POST.get("service")
        message = request.POST.get("message")

        # 1️⃣ Save to Admin
        ContactMessage.objects.create(
            full_name=name,
            email=email,
            phone=phone,
            service_interest=service,
            message=message
        )

        # # 2️⃣ Send to Formspree
        # try:
        #     requests.post(
        #         "https://formspree.io/f/mjgeeale",
        #         data={
        #             "name": name,
        #             "email": email,
        #             "phone": phone,
        #             "service": service,
        #             "message": message
        #         },
        #         timeout=5
        #     )
        # except:
        #     pass

        # 3️⃣ Send HTML Email to Customer
        subject = "We Received Your Request - Rushabh InfoTech"

        html_content = f"""
        <html>
        <body style="font-family:Arial;background:#f4f6f9;padding:40px;">
        <div style="max-width:600px;margin:auto;background:#ffffff;padding:30px;border-radius:10px;">
        <h2 style="color:#1d4ed8;">Rushabh InfoTech</h2>
        <p>Hi <strong>{name}</strong>,</p>
        <p>Thank you for contacting us regarding <b>{service}</b>.</p>
        <p>Our team will contact you shortly.</p>
        <hr>
        <p style="font-size:14px;color:#64748b;">
        📞 +91 9879877877 <br>
        📍 Ahmedabad, Gujarat
        </p>
        </div>
        </body>
        </html>
        """

        try:
            email_message = EmailMultiAlternatives(
                subject,
                "",
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()
        except:
            pass

        # 4️⃣ Notify Admin
        try:
            send_mail(
                subject="🚨 New Contact Message Received",
                message=f"""
New contact form submitted.

Name: {name}
Email: {email}
Phone: {phone}
Service: {service}

Message:
{message}
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=["mktg.rushabhinfotech@gmail.com"],
                fail_silently=True,
            )
        except:
            pass

        # ✅ IMPORTANT — RETURN RESPONSE
        return redirect("contact")

    # ✅ Safety fallback (never return None)
    return render(request, "contact.html")

