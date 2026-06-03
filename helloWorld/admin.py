from django.contrib import admin
from .models import Users, Images

class ImageInline(admin.TabularInline):
    model = Images
    extra = 1


# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname")


admin.site.register(Users, MemberAdmin)
