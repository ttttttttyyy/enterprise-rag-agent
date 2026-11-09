from rest_framework.exceptions import PermissionDenied, NotFound
from .models import Membership, Tenant
def membership_for(user, tenant_id, roles=None):
    try: tenant = Tenant.objects.get(pk=tenant_id, status="active")
    except Tenant.DoesNotExist: raise NotFound("Workspace not found.")
    try: membership = Membership.objects.get(tenant=tenant,user=user,active=True)
    except Membership.DoesNotExist: raise PermissionDenied("You do not have access to this workspace.")
    if roles and membership.role not in roles: raise PermissionDenied("Insufficient workspace role.")
    return membership
