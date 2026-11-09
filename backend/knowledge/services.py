import hashlib, re
from pathlib import Path
from django.conf import settings
from django.utils import timezone
from .models import Chunk, Document

def extract_text(path, file_type):
    if file_type == "pdf":
        from pypdf import PdfReader
        reader=PdfReader(path)
        return [(i+1, page.extract_text() or "") for i,page in enumerate(reader.pages)]
    if file_type == "docx":
        from docx import Document as DocxDocument
        doc=DocxDocument(path)
        return [(None,"\n".join(p.text for p in doc.paragraphs))]
    if file_type == "txt":
        return [(None,Path(path).read_text(encoding="utf-8",errors="replace"))]
    raise ValueError("Unsupported file type.")

def split_chunks(text, size=None, overlap=None):
    size=size or settings.CHUNK_SIZE; overlap=overlap if overlap is not None else settings.CHUNK_OVERLAP
    text=re.sub(r"\s+"," ",text).strip()
    if not text: return []
    result=[]; start=0
    while start<len(text):
        end=min(start+size,len(text))
        if end<len(text):
            boundary=text.rfind(" ",start,end)
            if boundary>start+size//2: end=boundary
        result.append(text[start:end].strip())
        if end>=len(text): break
        start=max(end-overlap,start+1)
    return result

def embed_texts(texts):
    if settings.OPENAI_API_KEY:
        from openai import OpenAI
        client=OpenAI(api_key=settings.OPENAI_API_KEY)
        response=client.embeddings.create(model=settings.EMBEDDING_MODEL,input=texts)
        return [item.embedding for item in response.data]
    # Deterministic local fallback for development; not semantically equivalent to a trained embedding model.
    import hashlib
    vectors=[]
    for text in texts:
        vals=[0.0]*1536
        for token in re.findall(r"\w+",text.lower()):
            digest=hashlib.sha256(token.encode()).digest()
            idx=int.from_bytes(digest[:4],"big")%1536
            vals[idx]+=1.0 if digest[4]%2 else -1.0
        norm=sum(v*v for v in vals)**0.5 or 1
        vectors.append([v/norm for v in vals])
    return vectors

def process_document(document_id):
    doc=Document.objects.get(pk=document_id)
    doc.status="processing"; doc.error_message=""; doc.save(update_fields=["status","error_message"])
    try:
        pages=extract_text(doc.file.path,doc.file_type)
        all_chunks=[]
        for page,text in pages:
            for part in split_chunks(text):
                all_chunks.append((page,part))
        if not all_chunks: raise ValueError("No extractable text found in this file.")
        vectors=embed_texts([x[1] for x in all_chunks])
        Chunk.objects.filter(document=doc).delete()
        Chunk.objects.bulk_create([
            Chunk(tenant=doc.tenant,document=doc,ordinal=i,content=part,page_number=page,embedding=vectors[i])
            for i,(page,part) in enumerate(all_chunks)
        ],batch_size=100)
        doc.status="indexed"; doc.indexed_at=timezone.now(); doc.save(update_fields=["status","indexed_at"])
    except Exception as exc:
        doc.status="failed"; doc.error_message=str(exc)[:1000]; doc.save(update_fields=["status","error_message"])
        raise
