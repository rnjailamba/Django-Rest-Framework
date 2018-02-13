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

class IndustryUpload(APIView):
    def post(self, request, format=None):
        data = request.data
        for i in range(len(data)):
            print data[i]
            industry_id = data[i]['industry_id']
            num = industry_id
            if(Industry.objects.filter(industry_id=str(num)).exists()):
                obj = Industry.objects.filter(industry_id=str(num)).update(name=data[i]['name'])
                return Response(obj, status=status.HTTP_201_CREATED)
            arr = []
            direct_parent_id = None
            string = str(num)
            for c in string:
                num = num / 10
                if (num > 0 and Industry.objects.filter(industry_id=str(num)).exists()):
                    if direct_parent_id is None:
                        direct_parent_id = num
                    print Industry.objects.get(industry_id=str(num)).name
                    arr.append(num)
                print num
            print arr
            data[i]['parent_ids'] = arr
            data[i]['direct_parent_id'] = direct_parent_id
            industries = Industry.objects.filter(industry_id__startswith=string)
            for industry in industries:
                print(industry.industry_id)
                industry.parent_ids.append(string)
                direct_parent_id = industry.direct_parent_id
                if direct_parent_id is None or int(direct_parent_id) < industry_id :
                    industry.direct_parent_id = industry_id
                industry.save()
            serializer = IndustrySerializer(data=data[i])
            if serializer.is_valid():
                serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IndustryDetail(APIView):
    """
    Retrieve an Industry instance
    """
    def get_object(self, pk):
        try:
            return Industry.objects.get(pk=pk)
        except Industry.DoesNotExist:
            raise Response("", status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = IndustrySerializer(snippet)
        return Response(serializer.data)