from rest_framework import serializers
from .models import UserProfile
from rest_framework_simplejwt.tokens import RefreshToken

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id", 
            "email",
            "password",
        )
        extra_kwargs = {
            "password" : {"write_only": True, 
                          "style": {"input_type":"password"}}
        }
        
        
    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
            )
        
        return user


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['_id', 'email', 'name', 'isAdmin']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        if obj.first_name and obj.last_name:
            name = obj.first_name + ' ' + obj.last_name
        elif obj.first_name and not obj.last_name:
            name = obj.first_name
        elif not obj.first_name and obj.last_name:
            name = obj.last_name
        else:
            name = obj.email
        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['_id', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)