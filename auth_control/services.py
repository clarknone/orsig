from auth_control.models import User


def create_user(email, **kwargs):
    email = email.lower()
    password = kwargs.pop("password", None)
    try:
        user = User.objects.create_user(email, password, **kwargs)
    except User.IntegrityError:
        raise ValueError

    # TODO send notification
    return user
