from django.contrib import admin

from .models import Collect, Payment


admin.site.register(Collect)
admin.site.register(Payment)
