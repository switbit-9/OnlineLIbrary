from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import *

admin.site.register(User)
admin.site.register(Books)
admin.site.register(Publisher)
admin.site.register(Borrow)
admin.site.register(Save)
admin.site.register(Review)
admin.site.register(Message)
admin.site.register(Activity)


# Register your models here.
