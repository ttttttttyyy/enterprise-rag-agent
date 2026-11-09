from django.urls import path
from .views import DocumentListCreate, DocumentDetail
urlpatterns=[path("documents/",DocumentListCreate.as_view()),path("documents/<int:pk>/",DocumentDetail.as_view())]
