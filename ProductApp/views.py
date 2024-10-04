from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import ProductSerializer
from rest_framework import status
from .models import Products


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
            try:
                item = Products.objects.get(id = item_id)
                serializer = ProductSerializer(item,many=False)
                return Response(serializer.data,status=status.HTTP_302_FOUND)
            except:
                return Response({"error":"The item is not present"},status=status.HTTP_404_NOT_FOUND)
        items = Products.objects.all()
        serializer = ProductSerializer(items,many=True)
        if serializer.data:
            return Response(serializer.data,status=status.HTTP_302_FOUND)
    
    # updating the details
    def patch(self,request,item_id):
        print(item_id)
        try:
            item = Products.objects.get(id = item_id)
        except:
            return Response({'error':"Item is not found"},status=status.HTTP_404_NOT_FOUND)
        print(item)
        serializer = ProductSerializer(item,data = request.data, partial=True)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
    # deleting the product
    def delete(self,request,item_id):
        try:
            item = Products.objects.get(id = item_id)
            item.delete()
            return Response({"success":'Item deleted successfully'},status=status.HTTP_200_OK)
        except:
            return Response({"error":"Item is not present"},status=status.HTTP_404_NOT_FOUND)