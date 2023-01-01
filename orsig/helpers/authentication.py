from rest_framework.authentication import TokenAuthentication


class _TokenAuthentication(TokenAuthentication):
    keyword = "Bearer"
