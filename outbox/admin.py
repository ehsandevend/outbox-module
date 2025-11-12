from django.contrib import admin
from outbox.models import Outbox

admin.site.register(Outbox)
