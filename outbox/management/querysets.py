from django.db import transaction
from django.db.models import QuerySet

from outbox.services import SingleSaveOutboxService, BulkLogOutboxService, SingleUpdateOutboxService
from outbox.shared.enums import ActionChoices
from outbox.shared.exceptions import OutboxBulkCreateError


class OutboxedLogQueryset(QuerySet):
    """Custom queryset that creates outbox entries based on specific conditions"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.single_service = SingleSaveOutboxService()
        self.single_update_service = SingleUpdateOutboxService()
        self.bulk_service = BulkLogOutboxService()
    
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        """
        Prevent bulk_create when using this outboxed manager.
        read: https://code.djangoproject.com/ticket/19527?utm_source=chatgpt.com
        """
        raise OutboxBulkCreateError(
            "Cannot use bulk_create with this manager. Use individual save() calls "
            "to ensure outbox entries receive valid object IDs."
        )

    def create(self, **kwargs):
        """Override update to create outbox entries only when state_id is being changed"""
        with transaction.atomic():
            created_instance = super().create(**kwargs)
            if created_instance:
                self.single_service.create_and_publish(
                    created_instance, ActionChoices.CREATE
                )
            return created_instance
        
    def reindex(self, id):
        try:
            instance = self.get(id=id)
        except self.model.DoesNotExist:
            return False
        self.single_service.create_and_publish(
                instance, ActionChoices.REINDEX
            )
        return True
    
    def update(self, **kwargs):
        """Override update to create outbox entries only when state_id is being changed"""
        with transaction.atomic():
            updated_count = super().update(**kwargs)
            if updated_count == 0:
                return updated_count

            instances = list(self.all())
            if not instances:
                return updated_count

            if updated_count == 1:
                self.single_update_service.create_and_publish(
                    instances[0], ActionChoices.UPDATE
                )
   
            return updated_count

    def bulk_update(self, objs, fields, batch_size=None):
        """Override bulk_update to create outbox entries only when state_id is being changed"""
        with transaction.atomic():
            updated_objs = super().bulk_update(objs, fields, batch_size)

            if not updated_objs:
                return updated_objs

            if updated_objs == 1:
                self.single_service.create_and_publish(
                    updated_objs[0], ActionChoices.UPDATE
                )
            else:
                self.bulk_service.create_and_publish(updated_objs, ActionChoices.UPDATE)

            return updated_objs

    def delete(self):
        with transaction.atomic():
            instances = list(self.all())
            if not instances:
                return 0, {}

            if len(instances) == 1:
                self.single_service.create_and_publish(
                    instances[0], action=ActionChoices.DELETE
                )
            else:
                self.bulk_service.create_and_publish(
                    instances, action=ActionChoices.DELETE
                )

            deleted_count, details = super().delete()
            return deleted_count, details