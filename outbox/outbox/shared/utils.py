from typing import Any, Iterable
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.forms.models import model_to_dict
from django.utils import timezone


def to_dict(obj: Model):
    if not isinstance(obj, Model):
        raise TypeError("to_dict expects a Django Model instance")
    return _model_to_json_safe_dict(obj)


def bulk_to_dict(objs: Iterable[Model]):
    return [_model_to_json_safe_dict(o) for o in objs]


def _model_to_json_safe_dict(instance: Model):
    data = model_to_dict(instance, fields=[f.name for f in instance._meta.fields])
    data["id"] = instance.pk
    data = {k: serialize_value(v) for k, v in data.items()}

    return data


def serialize_value(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, Model):
        return value.pk

    if hasattr(value, "isoformat"):
        if hasattr(value, "tzinfo") and timezone.is_aware(value):
            return timezone.localtime(value).isoformat()
        return value.isoformat()

    if hasattr(value, "all"):
        return [item.pk for item in value.all()]

    if hasattr(value, "values_list"):
        return list(value.values_list("pk", flat=True))

    if hasattr(value, "url"):
        try:
            return value.url
        except (ValueError, AttributeError):
            return None

    if isinstance(value, (bytes, bytearray, memoryview)):
        import base64

        return base64.b64encode(value).decode() if value else None

    if hasattr(value, "__iter__") and not isinstance(value, (str, bytes, dict)):
        return [serialize_value(v) for v in value]

    if isinstance(value, dict):
        return {str(k): serialize_value(v) for k, v in value.items()}

    try:
        return DjangoJSONEncoder().default(value)
    except TypeError:
        return str(value)
