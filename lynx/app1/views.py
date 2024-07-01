from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404

def index(request):
    return HttpResponse("Request recieved in the app1 index view.")


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data= request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username = request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user = user)
        return Response({"token":token.key,"user":serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username = request.data["username"])

    if not user.check_password(request.data["password"]):
        return Response({"detail":"Not found"}, status=status.HTTP_400_BAD_REQUEST)
    token = Token.objects.get(user = user)
    serializer = UserSerializer(instance=user)
    return Response({"token":token.key,"user":serializer.data})
