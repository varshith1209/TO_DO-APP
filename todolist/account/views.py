from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
# Create your views here.
class RegisterAPI(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'user created succesfully','status':'ok'},status=status.HTTP_201_CREATED)
        return Response({'message':'Invalid request'},status=status.HTTP_400_BAD_REQUEST)
        
class LoginAPI(APIView):
            def post(self,request):
                serializer=LoginSerializer(data=request.data)
                if serializer.is_valid():
                    user=serializer.validated_data['user']
                    refresh=RefreshToken.for_user(user)
                    return Response({'message':'loggedin successfully','user':user.username,'refresh':str(refresh),'access':str(refresh.access_token)},status=status.HTTP_202_ACCEPTED)
                return Response({'message': 'unable to login','status':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()   # 🔑 makes the token invalid
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        