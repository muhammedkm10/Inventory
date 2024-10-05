from django.test import TestCase
from rest_framework.test import APITestCase
from AuthApp.models import CustomUser
from django.urls import reverse
from rest_framework import status
from .models import Products
from rest_framework_simplejwt.tokens import RefreshToken
# Create your tests here.

class ProductViewTest(APITestCase):
    
    # basic setup for the product view tests
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testusername",
            email='testuser@example.com',
            password='testpassword123',
        )
        
        self.token = self.get_access_token(self.user)
        
        self.product_management_url = reverse('product_management_create')
        
        
        self.product_details = {
            "name":"product1",
            'description':"This is the product for something",
            "stock":1
        }
      
      
   # getting the access token for the user
    def get_access_token(self,user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
                
#   add product success case
    def test_create_product(self):
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.post(self.product_management_url,self.product_details,format = 'json',**headers)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Products.objects.count(),1)
        self.assertEqual(Products.objects.get().name,self.product_details['name'])
        
    
    # add product falure
    
    def test_create_product_failure(self):
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.post(self.product_management_url,{},format = 'json',**headers)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Products.objects.count(), 0) 
        
    # get all products
    
    def test_get_all_product(self):
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        self.client.post(self.product_management_url,self.product_details,format = 'json',**headers)
        
        # Now, make a request to get all products
        response = self.client.get(reverse('product_management_create'), format='json', **headers) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 
        
        
        # fetching one data details with specific id
    def test_get_one_product(self):
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response  = self.client.post(self.product_management_url,self.product_details,format = 'json',**headers)
        response = self.client.get(reverse('product_management_update',kwargs={"item_id":response.data["item"]["id"]}), format='json', **headers) 
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    
    # item not found
    def test_get_one_product_failed(self):
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response = self.client.get(reverse('product_management_update',kwargs={"item_id":1}), format='json', **headers) 
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        
        
        
      # test for update product
    def test_update_product(self):
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response  = self.client.post(self.product_management_url,self.product_details,format = 'json',**headers)
        print("my data",response.data)
        updated_data = {
            'name': 'Updated Product',
        }
        response = self.client.patch(reverse('product_management_update', kwargs={'item_id': response.data["item"]["id"]}), updated_data, format='json',**headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Products.objects.get(id=response.data["id"]).name, 'Updated Product')


# test for delete 
    def test_delete_product(self):
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        response  = self.client.post(self.product_management_url,self.product_details,format = 'json',**headers)
        
        response = self.client.delete(reverse('product_management_update', kwargs={'item_id': response.data["item"]["id"]}),**headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Products.objects.count(), 0) 
         
        
        
