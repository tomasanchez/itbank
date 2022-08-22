from django.contrib import admin

from .models import Branch, Employee, Address

# Register your models here.
admin.site.register(Branch)
admin.site.register(Employee)
admin.site.register(Address)
