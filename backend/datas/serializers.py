from rest_framework import serializers
from datas.models import ProductLego

class LegoSerializers(serializers.ModelSerializer):

    class Meta:
        model=ProductLego
        fields=["productid", "name", "nb_pieces"]