from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Industry
from .serializers import IndustrySerializer
from django.db.models import Q
import json, ast


class IndustryList(APIView):
    def get(self, request, format=None):
        industries = Industry.objects.all()
        pairs = [] # parent child pairs

        for industry in industries:
            if industry.direct_parent_id is None:
                pairs.append([industry.industry_id, industry.industry_id])
            else:
                pairs.append([industry.industry_id, industry.direct_parent_id])

        nodes = {}
        for i in pairs:
            id, parent_id = i
            nodes[id] = {'id': id, 'name': Industry.objects.get(industry_id=str(id)).name,}

        forest = []
        for i in pairs:
            id, parent_id = i
            node = nodes[id]
            if id == parent_id:
                forest.append(node)
            else:
                parent = nodes[parent_id]
                if not 'children' in parent:
                    parent['children'] = []
                children = parent['children']
                children.append(node)
        final_response = {}
        final_response["industries"] = forest
        return Response(final_response)

class IndustryUpload(APIView):
    def post(self, request, format=None):
        data_json = self.request.body
        data = json.loads(data_json)
        data = ast.literal_eval(json.dumps(data))
        for i in range(len(data)):
            industry_id = data[i]['id']
            num = int(industry_id)
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
                    arr.append(num)
            data[i]['industry_id'] = data[i]['id']
            data[i]['parent_ids'] = arr
            data[i]['direct_parent_id'] = direct_parent_id
            industries = Industry.objects.filter(industry_id__startswith=string)
            for industry in industries:
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
    def get(self, request, pk, format=None):

        try:
            industries = Industry.objects.filter(Q(parent_ids__contains=[str(pk)]) | Q(industry_id=str(pk)))
        except Industry.DoesNotExist:
            raise Response("", status=status.HTTP_400_BAD_REQUEST)

        pairs = []  # parent child pairs
        for industry in industries:
            if industry.direct_parent_id is None or int(industry.direct_parent_id) < int(pk):
                pairs.append([industry.industry_id, industry.industry_id])
            else:
                pairs.append([industry.industry_id, industry.direct_parent_id])

        nodes = {}
        for i in pairs:
            id, parent_id = i
            nodes[id] = {'id': id, 'name': Industry.objects.get(industry_id=str(id)).name,}

        forest = []
        for i in pairs:
            id, parent_id = i
            node = nodes[id]
            if id == parent_id:
                forest.append(node)
            else:
                parent = nodes[parent_id]
                if not 'children' in parent:
                    parent['children'] = []
                children = parent['children']
                children.append(node)
        final_response = {}
        final_response["industries"] = forest
        return Response(final_response)