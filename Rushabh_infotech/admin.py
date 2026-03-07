from django.contrib import admin
from .models import Service, SubService, ContactMessage

"admin_interface",
"colorfield",
"django.contrib.admin",

class SubServiceInline(admin.TabularInline):
    model = SubService
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "price_range", "is_active", "order")
    list_editable = ("is_active", "order")
    ordering = ("order",)


@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "service")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "email",
        "phone",
        "status",
        "created_at",
    )

    list_filter = ("status", "created_at")
    search_fields = ("full_name", "email")
    list_editable = ("status",)

    readonly_fields = (
        "full_name",
        "email",
        "phone",
        "service_interest",
        "message",
        "created_at",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("-created_at")
