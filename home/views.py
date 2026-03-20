from django.shortcuts import render
from .serializers import UserRegister
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegister,UserDataSerializer
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
# Create your views here.

class Register(APIView):

    def post(self,request, formate=None):

        serializer = UserRegister(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = 'registered'
            data['username'] = account.username
            data['email'] = account.email

            token, created = Token.objects.get_or_create(user=account)
            data['token']= token.key

        else:
            data = serializer.errors
            
            
        return Response(data)

class Welcome(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        content = {"user":str(request.user),'userid':str(request.user.id)}
        return Response(content)
    
class UserDetails(APIView):
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        user_data = self.get_object(pk)
        serializer = UserDataSerializer(user_data)
        return Response(serializer.data)
    
    def put(self,request,pk,formate=None):
        user_data = self.get_object(pk)
        serializer = UserDataSerializer(user_data, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response({
            "message":"error",
            "error" : serializer.errors
        },
        status=400)
        
    def delete(self,request,pk,formate=None):
        user_data = self.get_object(pk)
        user_data.delete()
        return Response({"message":"user deleted"})
    
class SetPagination(PageNumberPagination):
    page_size=2

class paginationApi(ListAPIView): 
    queryset=User.objects.all()
    serializer_class=UserDataSerializer
    pagination_class=SetPagination
    filter_backends=(SearchFilter,)
    SearchFilter=("username","email","first_name","last_name")

    