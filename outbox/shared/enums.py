from django.db.models import IntegerChoices


class OutboxStatusChoices(IntegerChoices):
    PENDING = 1, "در انتظار ارسال"
    DELIVERED = 2, "ارسال شده"
    FAILED = 3, "ناموفق"


class ActionChoices(IntegerChoices):
    CREATE = 1, "create"
    UPDATE = 2, "update"
    DELETE = 3, "delete"
    REINDEX = 4, "reindex"


class OutboxTypeChoices(IntegerChoices):
    LOG = 1, "log"
    CACHE = 2, "cache"
