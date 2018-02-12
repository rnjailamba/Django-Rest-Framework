from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Industry
from .serializers import IndustrySerializer


class IndustryList(APIView):
    def get(self, request, format=None):
        products = Industry.objects.all()
        serializer = IndustrySerializer(products, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        data = request.data
        for i in range(len(data)):
            print data[i]
            serializer = IndustrySerializer(data=data[i])
            if serializer.is_valid():
                serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)