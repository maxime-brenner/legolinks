from django.contrib import admin
from datas.models import ProductLego

class ProductLegoAdmin(admin.ModelAdmin):
    list_display= ["productid", "name","theme", "nb_pieces", "isLinkLego"]
    
    def isLinkLego(self, obj):
        if obj.link_lego is not None:
            return True
        else : 
            return False

admin.site.register(ProductLego, ProductLegoAdmin) 

# Register your models here.
