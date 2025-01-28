from rest_framework import serializers
from .models import User, OtpCode

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "phone_num", "full_name", "password2", "password")

    def validate_phone_num(self, value):
        if not value.startswith("09"):
            raise serializers.ValidationError("Please enter a valid phone number")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        del validated_data["password2"]
        vd = validated_data
        return User.objects.create_user(**validated_data)



class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "phone_num", "full_name")
        read_only_fields = ("id",)

class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ("code",)