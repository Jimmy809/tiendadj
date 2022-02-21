from rest_framework import viewsets
from rest_framework.response import Response

# from tienda.applications.venta import serializers
from .models import Colors, Product
from .managers import ProductManager

from .serializers import ColorsSerializer, ProductSerializer, PaginationSerializer, ProductSerializerViewSet


class ColorViewSet(viewsets.ModelViewSet):
    
    serializer_class = ColorsSerializer
    queryset = Colors.objects.all()
    
    
class ProductViewSet(viewsets.ModelViewSet):
    
    serializer_class = ProductSerializerViewSet
    queryset = Product.objects.all()
    pagination_class = PaginationSerializer
    
    # def create(self,request):
    #     print(request.data)
    #     return Response({'code': 'ok'})
    def perform_create(self, serializer):
        serializer.save(
            video="https://www.youtube.com/watch?v=zx0FOQDhESI"
        )
        
    def list(self,request, *args, **kwargs):
        queryset = Product.objects.productos_por_user(self.request.user)
        # 
        serializer = self.get.get_serializer(queryset, many=True)
        return Response(serializer.data)