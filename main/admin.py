from django.contrib import admin

from main.models import Client, Mailing, TryMailing, Message


@admin.register(Client)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "comment")
    list_filter = ("email",)
    search_fields = ("first_name", "last_name")


@admin.register(Mailing)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "interval",
        "status",
    )


@admin.register(TryMailing)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("response", "status", "last_try")
    search_fields = ("status",)
    list_filter = ("status",)


@admin.register(Message)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("subject", "body")
