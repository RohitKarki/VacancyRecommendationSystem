from rest_framework import serializers, exceptions
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy_Detail
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register_Detail
        fields = '__all__'

class LoginSerilizer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")
        print(password)
        if email and password:
            user = authenticate(email=email, password = password)
            print(user)
            if user:
                # if user.is_active:
                #     data["user"] = user
                # else:
                #     msg = "User is deactivated."
                #     raise exceptions.ValidationError(msg)
                data["user"] = user
            else:
                msg = "Unable to log in with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide email and password both."
            raise exceptions.ValidationError()