import logging

from django.db.models import TextField

from crypto.models.crypto_file import Crypto_file, CryptoManager
from isc_common.fields.related import ForeignKeyProtect
from kaf_pas.kd.models.documents import Documents
from kaf_pas.kd.models.lotsman_documents_hierarcy import Lotsman_documents_hierarcy

logger = logging.getLogger(__name__)


class Documents_thumb10(Crypto_file):
    # Менять на cascade нельзя, потому как не происходит удаленеи файлов изображений при удалении документа
    document = ForeignKeyProtect(Documents, verbose_name='КД', null=True, blank=True)
    lotsman_document = ForeignKeyProtect(Lotsman_documents_hierarcy, verbose_name='Лоцман', null=True, blank=True)
    path = TextField()

    objects = CryptoManager()

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'JPEG варианты документов'
        unique_together = (('lotsman_document', 'path'), ('document', 'path'),)
