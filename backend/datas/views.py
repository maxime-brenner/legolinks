from django.shortcuts import render
from rest_framework import viewsets
from datas.models import ProductLego
from datas.serializers import LegoSerializers

# Create your views here.
class LegoView(viewsets.ModelViewSet):
    serializer_class = LegoSerializers
    queryset = ProductLego.objects.all()