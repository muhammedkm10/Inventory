from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import CustomUser

# Create your tests here.

class AuthTests(APITestCase):
    def setUp(self) :
        self.registration_url = reverse("user_register")
        self.login_url = reverse('user_login')
        self.user_data  = {
            'username':"muhammedkm",
            'email':"abcd@gmail.com",
            'password':"12345678q"
        }
        
    def test_user_registration(self):
        response = self.client.post(self.registration_url,self.user_data,format="json")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email = self.user_data['email']).exists())
        user = CustomUser.objects.get(email = self.user_data['email'])
        self.assertEqual(user.email ,self.user_data['email'])
        
    def test_user_registration_invalid(self):
        response = self.client.post(self.registration_url,{},format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(),0)
        
        
    def test_user_login(self):
        self.client.post(self.registration_url, self.user_data, format='json')
        login_data = {
            "email":self.user_data['email'],
            "password":self.user_data['password']
        }
        response  = self.client.post(self.login_url,login_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('token',response.data)
        
    def test_user_login_invalid(self):
        login_data = {
            "email":self.user_data['email'],
            "password":self.user_data['password']
        }
        response = self.client.post(self.login_url,login_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Enter valid credentials, email and password")
        
        