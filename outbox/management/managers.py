from django.db.models import Manager

from .querysets import OutboxedLogQueryset


class OutboxedLogManager(Manager):

    def get_queryset(self):
        return OutboxedLogQueryset(self.model, using=self._db)
    
    def reindex(self, id):
        return self.get_queryset().reindex(id)