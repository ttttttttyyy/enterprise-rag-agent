from rest_framework import serializers
from .models import Tenant, Membership
class TenantSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta: model=Tenant; fields=("id","name","status","plan","created_at","role"); read_only_fields=("status","plan","created_at","role")
    def get_role(self,obj):
        m=obj.memberships.filter(user=self.context["request"].user,active=True).first()
        return m.role if m else None
class MembershipSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source="user.username",read_only=True)
    class Meta: model=Membership; fields=("id","tenant","user","username","role","active"); read_only_fields=("tenant","active")
