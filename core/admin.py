from django.contrib import admin

from core.models import (
    CareerProfile,
    Education,
    FamilyProfile,
    MatrimonialProfile,
    PartnerPreference,
    ProfileLocation,
    ReligiousProfile,
    User,
    Wali,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(MatrimonialProfile)
class MatrimonialProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(PartnerPreference)
class PartnerPreferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'isDefault')
    list_filter = ('isDefault',)
    search_fields = ('name', 'user__username', 'user__email')


@admin.register(FamilyProfile)
class FamilyProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Wali)
class WaliAdmin(admin.ModelAdmin):
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


@admin.register(ProfileLocation)
class ProfileLocationAdmin(admin.ModelAdmin):
    pass
