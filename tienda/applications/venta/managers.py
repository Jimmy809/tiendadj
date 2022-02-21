from django.db import models

class SaleDetailManagers(models.Manager):
    
    def productos_por_ventas(self, venta_id):
        consulta = self.filter(
            sale__id=venta_id
        ).order_by('count', 'product__name')
        return consulta