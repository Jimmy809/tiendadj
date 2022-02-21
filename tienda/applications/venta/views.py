from django.utils import timezone
from django.shortcuts import render

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
)

from applications.producto.models import Product
# 
from .models import Sale, SaleDetail
# 
from .serializers import (
    VentaReporteSerializers,
    ProcesoVentaSerializers,
    ProcesoVentaSerializers2
)

# Create your views here.
class RepoteVentasList (ListAPIView):
    serializer_class =  VentaReporteSerializers
    
    def get_queryset(self):
        return Sale.objects.all()
    
    
class RegistrarVenta2(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]    
    
    serializer_class = ProcesoVentaSerializers2
    
    def create(self, request, *args, **kwargs):
        serializer = ProcesoVentaSerializers2(data=request.data)
        # 
        serializer.is_valid(raise_exception=True)
        # 
        tipo_recibo = serializer.validated_data['type_invoce']
        # 
        venta = Sale.objects.create(
            date_sale=timezone.now(),
            amount=0,
            count=0,
            type_invoce=serializer.validated_data['type_invoce'],
            type_payment=serializer.validated_data['type_payment'],
            adreese_send=serializer.validated_data['adreese_send'],
            user=self.request.user,
        )
        # variables para venta
        amount = 0 # monto total de venta
        count = 0
        # recuperamos los porductos de una venta
        productos = Product.objects.filter(
            id__in=serializer.validated_data['productos']
        )
        # 
        cantidades = serializer.validated_data['cantidades']
        # 
        ventas_datalle = []
        # 
        for producto, cantidad in zip(productos, cantidades):
            # prod = Product.objects.filter(id__in=)
            venta_datalle = SaleDetail(
                sale=venta,
                product=producto,
                count=cantidad,
                price_purchase=producto.price_purchase,
                price_sale=producto.price_sale,
                
            )
            # 
            amount = amount + producto.price_sale*cantidad
            count = count + cantidad
            ventas_datalle.append(venta_datalle)
        
        venta.amount = amount
        venta.count = count
        venta.save()
        # 
        SaleDetail.objects.bulk_create(ventas_datalle)
        
        return Response({'msj:': 'Venta Exitosa'})
    
    
    
class RegistrarVenta(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]    
    
    serializer_class = ProcesoVentaSerializers
    
    def create(self, request, *args, **kwargs):
        serializer = ProcesoVentaSerializers(data=request.data)
        # 
        serializer.is_valid(raise_exception=True)
        # 
        tipo_recibo = serializer.validated_data['type_invoce']
        # 
        venta = Sale.objects.create(
            date_sale=timezone.now(),
            amount=0,
            count=0,
            type_invoce=serializer.validated_data['type_invoce'],
            type_payment=serializer.validated_data['type_payment'],
            adreese_send=serializer.validated_data['adreese_send'],
            user=self.request.user,
        )
        # variables para venta
        amount = 0 # monto total de venta
        count = 0
        # recuperamos los porductos de una venta
        productos = serializer.validated_data['productos']
        # 
        ventas_datalle = []
        # 
        for producto in productos:
            prod = Product.objects.get(id=producto['pk'])
            # prod = Product.objects.filter(id__in=)
            venta_datalle = SaleDetail(
                sale=venta,
                product=prod,
                count=producto['count'],
                price_purchase=prod.price_purchase,
                price_sale=prod.price_sale,
                
            )
            # 
            amount = amount + prod.price_sale*producto['count']
            count = count + producto['count']
            ventas_datalle.append(venta_datalle)
        
        venta.amount = amount
        venta.count = count
        venta.save()
        # 
        SaleDetail.objects.bulk_create(ventas_datalle)
        
        return Response({'msj:': 'Venta Exitosa'})