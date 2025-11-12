from django.contrib import admin
from outbox.outbox.models import Outbox

admin.site.register(Outbox)
