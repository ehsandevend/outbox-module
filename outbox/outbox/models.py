from typing import Optional

from django.db.models import (
    Model,
    PositiveSmallIntegerField,
    DateTimeField,
    JSONField,
    TextField,
    CharField,
    URLField,
)
from django.utils import timezone

from outbox.shared.enums import OutboxStatusChoices, OutboxTypeChoices


class Outbox(Model):
    model_tag = CharField(
        max_length=255,
        blank=True,
        help_text="برچسب یا شناسه‌ای برای مدل مرتبط با این رویداد.",
    )
    status = PositiveSmallIntegerField(
        choices=OutboxStatusChoices.choices,
        default=OutboxStatusChoices.PENDING,
        db_index=True,
    )
    type = PositiveSmallIntegerField(
        choices=OutboxTypeChoices.choices,
        default=OutboxTypeChoices.LOG,
        db_index=True,
    )
    max_retries = PositiveSmallIntegerField(
        default=3,
        help_text="حداکثر تعداد دفعات تلاش مجدد برای ارسال رویداد.",
    )
    retry_count = PositiveSmallIntegerField(
        default=0,
        help_text="تعداد دفعاتی که تاکنون برای ارسال رویداد تلاش شده است.",
    )
    created_date = DateTimeField(
        auto_now_add=True,
        help_text="تاریخ و زمان ایجاد رکورد رویداد.",
    )
    modified_date = DateTimeField(
        auto_now=True,
        help_text="تاریخ و زمان آخرین تغییرات روی رکورد رویداد.",
    )
    delivered_date = DateTimeField(
        null=True,
        blank=True,
        help_text="تاریخ و زمان تحویل موفق رویداد به مقصد.",
    )
    payload = JSONField(
        help_text="داده‌های اصلی رویداد به صورت JSON ذخیره می‌شود.",
    )
    error_message = TextField(
        blank=True,
        help_text="پیام خطا در صورت شکست در ارسال یا پردازش رویداد.",
    )
    source_url = URLField(
        max_length=500,
        blank=True,
        help_text="آدرس سرویس مبدا که این رویداد را تولید کرده است، برای callback یا ردیابی توسط مصرف‌کنندگان استفاده می‌شود.",
    )

    class Meta:
        db_table = "outbox_outbox"

    def mark_as_delivered(self):
        self.delivered_date = timezone.now()
        self.status = OutboxStatusChoices.DELIVERED
        self.save(update_fields=["status", "delivered_date"])
        return self

    def mark_as_failed(self, error_message: Optional[str] = None):
        if error_message:
            self.error_message = error_message

        if self.retry_count > self.max_retries:
            self.status = OutboxStatusChoices.FAILED
        else:
            self.status = OutboxStatusChoices.PENDING
            self.retry_count += 1
        self.save(update_fields=["status", "error_message", "retry_count"])
        return self
