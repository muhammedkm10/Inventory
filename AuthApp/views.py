from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import CustomUser
from .serializer import UserSerializer
from rest_framework import status
# Create your views here.



# Registraion View
class AuthView(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()  
            return Response({"data": "User created successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Login view
class LoginView(APIView):
    def post(self,request):
        return Response({"login":"succesful"})