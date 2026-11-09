from celery import shared_task
from .services import process_document
@shared_task(bind=True, max_retries=3, default_retry_delay=20)
def index_document(self, document_id):
    try: return process_document(document_id)
    except Exception as exc: raise self.retry(exc=exc)
