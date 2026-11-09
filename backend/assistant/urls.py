from django.urls import path
from .views import AskView, ConversationListView, FeedbackView
urlpatterns=[path("chat/ask/",AskView.as_view()),path("chat/conversations/",ConversationListView.as_view()),path("chat/feedback/",FeedbackView.as_view())]
