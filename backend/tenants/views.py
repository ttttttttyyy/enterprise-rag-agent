from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .models import Tenant, Membership
from .serializers import TenantSerializer, MembershipSerializer
from .permissions import membership_for
User=get_user_model()
class TenantListCreate(APIView):
    def get(self,request):
        qs=Tenant.objects.filter(memberships__user=request.user,memberships__active=True).distinct()
        return Response(TenantSerializer(qs,many=True,context={"request":request}).data)
    def post(self,request):
        name=(request.data.get("name") or "").strip()
        if not name: raise ValidationError({"name":"Workspace name is required."})
        tenant=Tenant.objects.create(name=name,created_by=request.user)
        Membership.objects.create(tenant=tenant,user=request.user,role="tenant_admin")
        return Response(TenantSerializer(tenant,context={"request":request}).data,status=201)
class MemberListCreate(APIView):
    def get(self,request):
        tid=request.query_params.get("tenant_id")
        if not tid: raise ValidationError({"tenant_id":"Required."})
        membership_for(request.user,tid,["tenant_admin","knowledge_manager","reviewer"])
        qs=Membership.objects.filter(tenant_id=tid).select_related("user")
        return Response(MembershipSerializer(qs,many=True).data)
    def post(self,request):
        tid=request.data.get("tenant_id"); membership_for(request.user,tid,["tenant_admin"])
        username=(request.data.get("username") or "").strip()
        try: user=User.objects.get(username=username)
        except User.DoesNotExist: raise ValidationError({"username":"User does not exist. Ask them to register first."})
        role=request.data.get("role","user")
        if role not in dict(Membership.ROLES): raise ValidationError({"role":"Invalid role."})
        obj,created=Membership.objects.get_or_create(tenant_id=tid,user=user,defaults={"role":role})
        if not created: obj.role=role; obj.active=True; obj.save()
        return Response(MembershipSerializer(obj).data,status=201 if created else 200)
