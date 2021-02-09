from django.contrib import admin
from read_only_admin.admin import ReadonlyAdmin

from .models import Message, Tap


class TapAdmin(admin.ModelAdmin):
    list_display = ("path", "is_active")
    list_filter = ("is_active",)
    search_fields = ("path",)
    ordering = ("path",)


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "request_path",
        "remote_addr",
        "started_at",
        "response_status_code",
        "response_reason_phrase",
        "duration",
    )
    list_filter = (
        "started_at",
        "request_method",
        "response_status_code",
    )
    search_fields = (
        "remote_addr",
        "request_path",
    )
    ordering = ("-id",)


admin.site.register(Tap, TapAdmin)
admin.site.register(Message, MessageAdmin)
