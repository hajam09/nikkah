from django.contrib import admin

from core.models import User, MatrimonialProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(MatrimonialProfile)
class MatrimonialProfileAdmin(admin.ModelAdmin):
    pass
