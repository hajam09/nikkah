from django.contrib import admin

from core.models import CareerProfile, Education, User, MatrimonialProfile, ReligiousProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(MatrimonialProfile)
class MatrimonialProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(ReligiousProfile)
class ReligiousProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    pass


@admin.register(CareerProfile)
class CareerProfileAdmin(admin.ModelAdmin):
    pass
