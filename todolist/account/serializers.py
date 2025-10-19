from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email']
        extra_kwargs = {'password': {'write_only': True}}
    def validate(self,data):
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username already taken")
            return data
    def create(self,validated_data):
            user=User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
                
            )
            return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password")
        else:
            raise serializers.ValidationError("Both username and password are required")

        data["user"] = user
        return data

        
        
            
            
        