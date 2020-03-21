from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(ReportProject)
admin.site.register(Picture)
admin.site.register(Comment)
admin.site.register(ReportComment)
admin.site.register(Donation)
admin.site.register(Rate)
admin.site.register(FeaturedProject)