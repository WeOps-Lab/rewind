from django.contrib import admin
from .models import UserAPISecret, User


@admin.register(UserAPISecret)
class UserAPISecretAdmin(admin.ModelAdmin):
    list_display = ('username', 'api_secret', 'team')
    search_fields = ('username', 'team')
    readonly_fields = ('api_secret',)

    def save_model(self, request, obj, form, change):
        if not obj.api_secret:
            obj.api_secret = UserAPISecret.generate_api_secret()
        super().save_model(request, obj, form, change)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'groups')
