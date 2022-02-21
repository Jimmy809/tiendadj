# 
from rest_framework.generics import (
    ListAPIView
)
# 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# 
from django.shortcuts import render
# 
from .serializers import ProductSerializer
# 
from .models import Product


# Create your views here.
class ListProductUser(ListAPIView):
    serializer_class = ProductSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # recuperando usuario
        usuario = self.request.user
        return Product.objects.productos_por_user(usuario)
    
    
class ListProductoStok(ListAPIView):
    serializer_class = ProductSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated, IsAdminUser]
    def get_queryset(self):
        # recuperando usuario
        # usuario = self.request.user
        return Product.objects.producto_con_stok()
    
    
class ListProductoGenero(ListAPIView):
    
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        genero = self.kwargs['gender']
        return Product.objects.productos_por_genero(genero)
    
class FiltrarProductos(ListAPIView):
    ''''''
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        varon = self.request.query_params.get('man', None)
        mujer = self.request.query_params.get('woman', None)
        nombre = self.request.query_params.get('name', None)  
                     
        return Product.objects.filtrar_productos(
            man=self.request.query_params.get('man', None),
            woman=mujer,
            name=nombre,
        )