from django.contrib import admin
from .models import University, User  # Modellaringizni import qiling

admin.site.register(University)
admin.site.register(User)