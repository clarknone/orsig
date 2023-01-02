from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = models.User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        if not email and not password:
            raise ValidationError({'error': "please input all fields"})
        try:
            user = self.Meta.model.objects.get(email=email.lower())
            # user.save()
            if not user.check_password(password):
                raise ValidationError({"error": "incorrect password"})
        except self.Meta.model.DoesNotExist:
            raise ValidationError({'error': "email does not exist"})
        return attrs


class SignUp(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    # email = serializers.EmailField(validators=[], required=True)

    class Meta:
        model = models.User
        fields = ['email', 'full_name', 'phone', 'password']


class User(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['email', 'bio', "full_name", 'date_created']


class PasswordUser(serializers.ModelSerializer):
    old = serializers.CharField(required=True, max_length=64)
    new = serializers.CharField(required=True, max_length=64)

    class Meta:
        model = models.User
        fields = ['old', 'new']

    def validate(self, attrs):
        if self.instance is None:
            raise ValidationError({'error': 'invalid user'})
        if self.instance.check_password(attrs.get('old')):
            return attrs
        else:
            raise ValidationError({'error': 'incorrect old password'})

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new', instance.email))
        instance.save()
        return instance
