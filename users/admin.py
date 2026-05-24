from django.contrib import admin
from django.contrib.auth import get_user_model

from users.models import Position


admin.site.register(get_user_model())
admin.site.register(Position)
