from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=150)
    short_description = models.TextField()
    price_range = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=10,
        help_text="Emoji icon e.g. 💻 📷 🌐"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class SubService(models.Model):
    service = models.ForeignKey(
        Service,
        related_name="sub_services",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.service.title} → {self.name}"


class ContactMessage(models.Model):

    STATUS_CHOICES = (
        ("Unread", "Unread"),
        ("Replied", "Replied"),
    )

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_interest = models.CharField(max_length=200, blank=True)
    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Unread"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.status}"