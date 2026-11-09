from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from tenants.models import Tenant, Membership
from .services import split_chunks
User=get_user_model()
class CoreTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(username="alice",password="StrongPass123!")
        self.other=User.objects.create_user(username="bob",password="StrongPass123!")
        self.tenant=Tenant.objects.create(name="Alpha",created_by=self.user)
        Membership.objects.create(tenant=self.tenant,user=self.user,role="tenant_admin")
        self.client=APIClient()
    def test_chunking_respects_limit(self):
        chunks=split_chunks("word "*1000,size=100,overlap=10)
        self.assertTrue(chunks)
        self.assertTrue(all(len(c)<=100 for c in chunks))
    def test_tenant_isolation(self):
        self.client.force_authenticate(self.other)
        response=self.client.get("/api/v1/documents/",{"tenant_id":self.tenant.id})
        self.assertEqual(response.status_code,403)
    def test_workspace_create(self):
        self.client.force_authenticate(self.user)
        response=self.client.post("/api/v1/tenants/",{"name":"New Workspace"},format="json")
        self.assertEqual(response.status_code,201)
