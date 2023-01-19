from django import forms

from .models import Users


uneditable_fields = (
    'id',
    'password',
    'date_joined',
    'last_login',
    'is_active',
    'is_staff',
    'is_superuser'
)


class SignUpForm(forms.ModelForm):
    confirm = forms.CharField(
        max_length=255
    )

    class Meta:
        model = Users
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm',
            'birth_date',
            'gender'
        )


class LoginForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = (
            'email',
            'password'
        )


class EditForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = [field.name for field in Users._meta.fields if field.name not in uneditable_fields]
