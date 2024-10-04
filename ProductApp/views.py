from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import ProductSerializer
from rest_framework import status
from .models import Products
from django.core.cache import cache

# product management view
class ProductManagment(APIView):
    permission_classes = [IsAuthenticated]
    # adding the data to the database
    def post(self,request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            item = serializer.save()
            return Response({"message":'Item added successfully',"item":serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    # get a product or all produts
    def get(self,request,item_id = None):
        
        if item_id:
            cache_key = f"item_{item_id}"
            item_data = cache.get(cache_key)
            if item_data is not None:
                # If item data is found in cache returning it
                return Response(item_data, status=status.HTTP_200_OK)
            try:
                item = Products.objects.get(id = item_id)
                serializer = ProductSerializer(item,many=False)
                cache.set(cache_key, serializer.data, timeout=3600)
                return Response(serializer.data,status=status.HTTP_302_FOUND)
            except:
                return Response({"error":"The item is not present"},status=status.HTTP_404_NOT_FOUND)
            
        # fetching all data from the cache
        cache_key = 'all_items'
        items = cache.get(cache_key)
        if items is not None:
            return Response(items,status=status.HTTP_200_OK)
        items = Products.objects.all()
        serializer = ProductSerializer(items,many=True)
        if serializer.data:
            cache.set(cache_key,serializer.data,timeout=3600)
            return Response(serializer.data,status=status.HTTP_302_FOUND)
    
    # updating the details
    def patch(self,request, item_id=None):
        if item_id is None:
            return Response({'error': 'Item ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            item = Products.objects.get(id = item_id)
        except:
            return Response({'error':"Item is not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(item,data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
    # deleting the product
    def delete(self,request, item_id=None):
        if item_id is None:
            return Response({'error': 'Item ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            item = Products.objects.get(id = item_id)
            item.delete()
            return Response({"success":'Item deleted successfully'},status=status.HTTP_200_OK)
        except:
            return Response({"error":"Item is not present"},status=status.HTTP_404_NOT_FOUND)