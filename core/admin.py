from django.contrib import admin

from core.models import (
    CareerProfile,
    EducationProfile,
    FamilyProfile,
    MatrimonialProfile,
    PartnerPreference,
    LocationProfile,
    ReligiousProfile,
    User,
    WaliProfile,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
        'isVerified',
        'is_active',
        'createdAt',
    )
    list_filter = (
        'isVerified',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
    )
    ordering = ('-createdAt',)
    list_per_page = 25
    readonly_fields = ('createdAt', 'updatedAt')


@admin.register(MatrimonialProfile)
class MatrimonialProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'gender',
        'dateOfBirth',
        'maritalStatus',
        'height',
        'nationality',
    )
    list_filter = (
        'gender',
        'maritalStatus',
        'physicalStatus',
        'eatingHabit',
        'smokingHabit',
        'nationality',
        'createdBy',
    )
    search_fields = (
        'user__username',
        'user__email',
        'user__first_name',
        'user__last_name',
        'user__phone',
        'nationality',
        'aboutMe',
    )
    ordering = ('-id',)
    list_select_related = ('user',)
    list_per_page = 25


@admin.register(PartnerPreference)
class PartnerPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'minAge',
        'maxAge',
    )
    search_fields = (
        'user__username',
        'user__email',
        'user__phone',
    )
    ordering = ('user__username',)
    list_select_related = ('user',)


@admin.register(FamilyProfile)
class FamilyProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'fatherOccupation',
        'motherOccupation',
        'numberOfSiblings',
        'familyType',
        'familyStatus',
        'familyValue',
    )
    list_filter = (
        'familyType',
        'familyStatus',
        'familyValue',
    )
    search_fields = (
        'user__username',
        'user__email',
        'user__phone',
        'fatherOccupation',
        'motherOccupation',
        'aboutMyFamily',
    )
    list_select_related = ('user',)


@admin.register(WaliProfile)
class WaliAdmin(admin.ModelAdmin):
    list_display = (
        'fullName',
        'user',
        'relationship',
        'email',
        'phone',
        'consentToContact',
        'isVerified',
    )
    list_filter = (
        'relationship',
        'consentToContact',
        'isVerified',
    )
    search_fields = (
        'fullName',
        'email',
        'phone',
        'user__username',
        'user__email',
        'user__phone',
    )
    list_select_related = ('user',)


@admin.register(ReligiousProfile)
class ReligiousProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'madhab',
        'prayerFrequency',
        'quranReading',
        'observesFasting',
        'hijabStatus',
        'halalLifestyle',
    )
    list_filter = (
        'madhab',
        'prayerFrequency',
        'quranReading',
        'observesFasting',
        'hijabStatus',
        'halalLifestyle',
    )
    search_fields = (
        'user__username',
        'user__email',
        'user__phone',
        'description',
    )
    list_select_related = ('user',)


@admin.register(EducationProfile)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'qualification',
        'institution',
        'fieldOfStudy',
        'graduationYear',
    )
    list_filter = (
        'qualification',
        'graduationYear',
    )
    search_fields = (
        'user__username',
        'user__email',
        'user__phone',
        'institution',
        'fieldOfStudy',
    )
    ordering = ('-graduationYear',)
    list_select_related = ('user',)


@admin.register(CareerProfile)
class CareerProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'employmentStatus',
        'occupation',
        'industry',
    )
    list_filter = (
        'employmentStatus',
        'industry',
    )
    search_fields = (
        'user__username',
        'user__email',
        'user__phone',
        'occupation',
    )
    list_select_related = ('user',)


@admin.register(LocationProfile)
class LocationProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'town',
        'city',
        'nativePlace',
        'residency',
        'willingToRelocate',
    )
    list_filter = (
        'residency',
        'willingToRelocate',
    )
    search_fields = (
        'user__username',
        'user__email',
        'user__phone',
        'town',
        'city',
        'nativePlace',
        'residency',
    )
    list_select_related = ('user',)
