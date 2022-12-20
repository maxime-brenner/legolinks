from django.db import models
from django.db.models import IntegerField, CharField, ForeignKey

# Create your models here.

class ProductLego (models.Model):

    productid = IntegerField (verbose_name="Id du produit", primary_key=True, null=False)
    name =  CharField (max_length=100, verbose_name="Nom du produit", null=True)
    link_lego = CharField(verbose_name="Lien de la boutique Lego", max_length=255, null=True)
    nb_pieces = IntegerField (null=True)
    image = CharField(max_length=255, null=True)
    theme = CharField (verbose_name="Thème", max_length=50,null=True)
    
    def __str__(self):
        return self.name

class AmazonLego (models.Model):

    productid = ForeignKey(("datas.ProductLego"), on_delete=models.CASCADE)
    lien = CharField(max_length=255, verbose_name="Lien")
    prix = models.FloatField(verbose_name="Dernier prix")