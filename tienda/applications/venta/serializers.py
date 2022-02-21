# 
from rest_framework import serializers

from .models import Sale, SaleDetail

class VentaReporteSerializers(serializers.ModelSerializer):
    
    productos = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Sale
        fields = (
            'id',
            'date_sale',
            'amount',
            'count',
            'type_invoce',
            'cancelado',
            'type_payment',
            'state',
            'adreese_send',
            'user',
            'productos',
        )
    
    def get_productos(self, obj):
        query = SaleDetail.objects.productos_por_ventas(obj.id)
        productos_serializados = DetalleVentaProductosSerializer(query, many=True).data
        return productos_serializados
    
class DetalleVentaProductosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SaleDetail
        fields = (
            'id',
            'sale',
            'product',
            'count',
            'price_purchase',
            'price_sale',
        )
        
class ProducDetailSerializers(serializers.Serializer):
    pk = serializers.IntegerField()
    count = serializers.IntegerField()
    
    
class ArrayIntegerSerializer(serializers.ListField):
    child = serializers.IntegerField()
    
        
class ProcesoVentaSerializers(serializers.Serializer):
    
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    productos = ProducDetailSerializers(many=True)
    
    
class ProcesoVentaSerializers2(serializers.Serializer):
    
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    productos = ArrayIntegerSerializer()
    cantidades = ArrayIntegerSerializer()
    
    def validate(self, data):
        if data['type_payment'] !='0': # modificar 0,1,2,3 ver los modulos
            raise serializers.ValidationError('ingrese un valor correcto')
        return data
    
    def validate_type_invoce(self, value):
        if value != '0':
            raise serializers.ValidationError('ingrese un valor correcto')
        return value
