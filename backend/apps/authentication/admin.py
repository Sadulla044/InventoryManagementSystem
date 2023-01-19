from django.contrib import admin

from .models import Users


uneditable_fields = (
    'id',
    'date_joined',
    'last_login'
)


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'birth_date',
        'gender',
        'is_staff',
        'is_active',
        'is_superuser'
    )

    fields = (
        'first_name',
        'last_name',
        'email',
        'birth_date',
        'gender',
        'is_staff',
        'is_active',
        'is_superuser'
    )

    class Meta:
        pass
