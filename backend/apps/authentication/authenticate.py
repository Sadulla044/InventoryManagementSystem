from django.contrib.auth import (
    backends,
    get_user_model
)


UserModel = get_user_model()


class EmailBackend(backends.ModelBackend):
    def authenticate(self, request, username, password, **kwargs):
        email = username

        if not email:
            email = kwargs.get(UserModel.EMAIL_FIELD)
        if email is None and password is None:
            return
        
        try:
            user = UserModel._default_manager.get(email=email)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user=user):
                return user
