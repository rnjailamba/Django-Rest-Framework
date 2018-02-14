from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Industry
from .serializers import IndustrySerializer
from .serializers import UserSerializer
from django.db.models import Q
import json, ast
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def is_authenticated(request):
    return request.user.is_authenticated()

def get_forest_from_pairs(pairs):
    nodes = {}
    for i in pairs:
        id, parent_id = i
        nodes[id] = {'id': id, 'name': Industry.objects.get(industry_id=str(id)).name, }

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
    return final_response

def get_request_json(request):
    data_json = request.body
    data = json.loads(data_json)
    data = ast.literal_eval(json.dumps(data))
    return data

class UserList(APIView):
    def post(self, request, format=None):
        data = get_request_json(self.request)
        data["username"] = data["name"]
        data["password"] = data["description"]
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        try:
            user = User.objects.get(username=serializer.data['username'])
        except User.DoesNotExist:
            return Response("", status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

class IndustryList(APIView):
    def get(self, request, format=None):
        if (not is_authenticated(request)): return Response("", status=status.HTTP_401_UNAUTHORIZED)
        industries = Industry.objects.all()
        pairs = [] # parent child pairs

        for industry in industries:
            if industry.direct_parent_id is None:
                pairs.append([industry.industry_id, industry.industry_id])
            else:
                pairs.append([industry.industry_id, industry.direct_parent_id])
        final_response = get_forest_from_pairs(pairs)
        return Response(final_response)

class IndustryUpload(APIView):
    def post(self, request, format=None):
        if (not is_authenticated(request)): return Response("", status=status.HTTP_401_UNAUTHORIZED)
        data = get_request_json(self.request)
        for i in range(len(data)):
            industry_id = data[i]['id']
            num = int(industry_id)
            if(Industry.objects.filter(industry_id=str(num)).exists()):
                obj = Industry.objects.filter(industry_id=str(num)).update(name=data[i]['name'])
                continue
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
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("", status=status.HTTP_201_CREATED)

class IndustryDetail(APIView):
    """
    Retrieve an Industry instance
    """
    def get(self, request, pk, format=None):
        if (not is_authenticated(request)): return Response("", status=status.HTTP_401_UNAUTHORIZED)
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

        final_response = get_forest_from_pairs(pairs)
        return Response(final_response)

class IndustryDelete(APIView):
    def delete(self, request, format=None):
        if (not is_authenticated(request)): return Response("", status=status.HTTP_401_UNAUTHORIZED)
        Industry.objects.all().delete()
        return Response("", status=status.HTTP_200_OK)