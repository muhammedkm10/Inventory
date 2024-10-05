from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import ProductSerializer
from rest_framework import status
from .models import Products
from django.core.cache import cache
import logging

logger = logging.getLogger('ProductApp')

# product management view
class ProductManagment(APIView):
    permission_classes = [IsAuthenticated]
    
    # adding the data to the database
    def post(self,request):
        logger.info("Received POST request to add a new item.")
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            cache.delete('all_items')
            item = serializer.save()
            logger.info(f"Item added successfully: {serializer.data}")
            return Response({"message":'Item added successfully',"item":serializer.data},status=status.HTTP_201_CREATED)
        logger.warning("Failed to add item: %s", serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    # get a product or all produts
    def get(self,request,item_id = None):
        logger.info("Received GET request.")
        if item_id:
            cache_key = f"item_{item_id}"
            item_data = cache.get(cache_key)
            if item_data is not None:
                logger.info(f"Received GET request for item ID: {item_id}")
                # If item data is found in cache returning it
                return Response(item_data, status=status.HTTP_200_OK)
            try:
                item = Products.objects.get(id = item_id)
                serializer = ProductSerializer(item,many=False)
                cache.set(cache_key, serializer.data, timeout=3600)
                logger.info(f"Fetched item ID: {item_id} from database and stored in cache.")
                return Response(serializer.data,status=status.HTTP_200_OK)
            except:
                logger.error(f"Item ID: {item_id} not found.")
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
            logger.info("Received GET request for all items.")
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"error":"The item is not present"},status=status.HTTP_404_NOT_FOUND)
    
    # updating the details
    def patch(self,request, item_id=None):
        logger.info("Received PATCH request for item ID: %s", item_id)
        if item_id is None:
            logger.error('Item ID is required for update.')
            return Response({'error': 'Item ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # deleting all data from redis after updating
        cache_key = f"item_{item_id}"
        cache.delete(cache_key)
        cache.delete('all_items')
        try:
            item = Products.objects.get(id = item_id)
        except:
            logger.error("Item ID: %s not found for update.", item_id)
            return Response({'error':"Item is not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(item,data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info("Item ID: %s updated successfully.", item_id)
            return Response(serializer.data,status=status.HTTP_200_OK)
        logger.warning("Failed to update item ID: %s - %s", item_id, serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
    # deleting the product
    def delete(self,request, item_id=None):
        logger.info("Received DELETE request for item ID: %s", item_id)
        if item_id is None:
            logger.error('Item ID is required for deletion.')
            return Response({'error': 'Item ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cache_key = f"item_{item_id}"
            cache.delete(cache_key)
            item = Products.objects.get(id = item_id)
            item.delete()
            logger.info("Item ID: %s deleted successfully.", item_id)
            return Response({"success":'Item deleted successfully'},status=status.HTTP_200_OK)
        except:
            logger.error("Item ID: %s not found for deletion.", item_id)
            return Response({"error":"Item is not present"},status=status.HTTP_404_NOT_FOUND)