from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True)
        user = serializer.save(); token, _ = Token.objects.get_or_create(user=user)
        return Response({"token":token.key,"user":UserSerializer(user).data}, status=201)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        from django.contrib.auth import authenticate
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if not user: return Response({"detail":"Invalid username or password."}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token":token.key,"user":UserSerializer(user).data})
class MeView(APIView):
    def get(self, request): return Response(UserSerializer(request.user).data)
