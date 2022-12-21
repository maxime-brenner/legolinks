from django.contrib import admin
from datas.models import ProductLego, AmazonLego

class ProductLegoAdmin(admin.ModelAdmin):
    list_display= ["productid", "name","theme", "nb_pieces", "isLinkLego"]
    
    def isLinkLego(self, obj):
        if obj.link_lego is not None:
            return True
        else : 
            return False

class AmazonLegoAdmin(admin.ModelAdmin):
    list_display=["productid_tag", "lien"]

    def productid_tag(self, obj):
        return obj.productid.productid

admin.site.register(ProductLego, ProductLegoAdmin) 
admin.site.register(AmazonLego, AmazonLegoAdmin)

# Register your models here.
