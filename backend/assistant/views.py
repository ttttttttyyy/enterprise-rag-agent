from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from .models import Conversation, Message, Feedback
from .rag import retrieve, generate_answer
from tenants.permissions import membership_for
class AskView(APIView):
    def post(self,request):
        tid=request.data.get("tenant_id"); question=(request.data.get("question") or "").strip()
        if not question: raise ValidationError({"question":"Question is required."})
        if len(question)>6000: raise ValidationError({"question":"Question is too long."})
        membership_for(request.user,tid)
        conv_id=request.data.get("conversation_id")
        if conv_id:
            conv=Conversation.objects.filter(pk=conv_id,tenant_id=tid,owner=request.user).first()
            if not conv: raise NotFound("Conversation not found.")
        else: conv=Conversation.objects.create(tenant_id=tid,owner=request.user,title=question[:180])
        Message.objects.create(conversation=conv,role="user",content=question)
        evidence=retrieve(tid,question)
        answer=generate_answer(question,evidence)
        citations=[{"index":i+1,"document_id":e["document_id"],"title":e["document__title"],"page":e["page_number"],"snippet":e["content"][:500]} for i,e in enumerate(evidence)]
        # Do not show irrelevant citations when no usable evidence exists.
        if "couldn't find sufficient" in answer.lower() or "provider is not configured" in answer.lower(): citations=[]
        msg=Message.objects.create(conversation=conv,role="assistant",content=answer,citations=citations)
        return Response({"conversation_id":conv.id,"message_id":msg.id,"answer":answer,"citations":citations})
class ConversationListView(APIView):
    def get(self,request):
        tid=request.query_params.get("tenant_id")
        membership_for(request.user,tid)
        qs=Conversation.objects.filter(tenant_id=tid,owner=request.user).order_by("-updated_at")[:50]
        return Response([{"id":c.id,"title":c.title,"updated_at":c.updated_at,"messages":[{"id":m.id,"role":m.role,"content":m.content,"citations":m.citations} for m in c.messages.all()]} for c in qs])
class FeedbackView(APIView):
    def post(self,request):
        msg=Message.objects.filter(pk=request.data.get("message_id"),role="assistant",conversation__owner=request.user).select_related("conversation").first()
        if not msg: raise NotFound("Message not found.")
        membership_for(request.user,msg.conversation.tenant_id)
        rating=request.data.get("rating")
        if rating not in dict(Feedback._meta.get_field("rating").choices): raise ValidationError({"rating":"Invalid feedback type."})
        item=Feedback.objects.create(message=msg,user=request.user,rating=rating,comment=request.data.get("comment","")[:2000])
        return Response({"id":item.id,"status":"recorded"},status=201)
