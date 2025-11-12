from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from outbox.outbox.models import Outbox
    from django.db.models import Model

from django.apps import apps
from django.conf import settings
from outbox.shared.enums import ActionChoices, OutboxTypeChoices
from outbox.shared.utils import to_dict, bulk_to_dict

PROJECT_TAG = settings.outbox.get("PROJECT_TAG", "payoon")


class OutboxRepo:
    """
    Repository for managing Outbox-related data access and business logic.

    This class currently handles all queries and operations related to the Outbox.
    In the future, it can be extended to separate Command and Query responsibilities
    if needed.

    Responsibilities:
    - DAL (Data Access Layer): database queries, inserts, updates, and deletions
    - BLL (Business Logic Layer): business rules related to Outbox processing

    All Outbox-related data access and business logic should be implemented here.
    """

    def __init__(self):
        self.outbox_model = apps.get_model("outbox", "Outbox")

    def create_single_log_outbox(
        self, instance: "Model", action: ActionChoices = ActionChoices.CREATE
    ) -> "Outbox":
        default_fields, model_tag = self._build_document_default_fields(
            instance, action
        )
        doc_data = {
            **to_dict(instance),
            **default_fields,
        }
        return self.outbox_model.objects.create(
            payload=doc_data,
            model_tag=model_tag,
            type=OutboxTypeChoices.LOG,
        )

    def create_bulk_log_outbox(
        self, instances: List["Model"], action: ActionChoices = ActionChoices.CREATE
    ) -> "Outbox":
        default_fields, model_tag = self._build_document_default_fields(
            instances[0], action
        )

        docs_data = [
            {
                **doc,
                **default_fields,
            }
            for doc in bulk_to_dict(instances)
        ]
        return self.outbox_model.objects.create(
            payload=docs_data,
            model_tag=model_tag,
            type=OutboxTypeChoices.LOG,
        )

    @staticmethod
    def _build_document_default_fields(
        instance, action: ActionChoices
    ) -> Tuple[dict, str]:
        model_tag = instance.__class__.__name__
        default_data = {
            "action_type": action,
            "model_tag": model_tag,
            "project_tag": PROJECT_TAG,
        }
        return default_data, model_tag
