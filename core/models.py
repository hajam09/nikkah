from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from core.choices import (
    CreatedBy,
    EatingHabit,
    EducationLevel,
    EmploymentStatus,
    FamilyStatus,
    FamilyType,
    FamilyValue,
    Gender,
    Height,
    HijabStatus,
    Industry,
    MaritalStatus,
    Madhab,
    PhysicalStatus,
    PrayerFrequency,
    QuranReading,
    Relationship,
    SmokingHabit,
    Weight,
)


class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    isVerified = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class MatrimonialProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matrimonialProfile')
    createdBy = models.CharField(max_length=10, blank=True, null=True, choices=CreatedBy.choices)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    dateOfBirth = models.DateField()
    height = models.PositiveSmallIntegerField(choices=Height.choices)
    weight = models.PositiveSmallIntegerField(choices=Weight.choices, null=True, blank=True)
    maritalStatus = models.CharField(max_length=12, choices=MaritalStatus.choices)
    physicalStatus = models.CharField(max_length=12, choices=PhysicalStatus.choices)
    languages = models.JSONField(default=list, blank=True)
    eatingHabit = models.CharField(max_length=20, blank=True, null=True, choices=EatingHabit.choices)
    smokingHabit = models.CharField(max_length=20, blank=True, null=True, choices=SmokingHabit.choices)
    numberOfChildren = models.PositiveSmallIntegerField(default=0)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    aboutMe = models.TextField(blank=True)

    @property
    def icons(self):
        return [
            'https://dummyimage.com/800x1000/000/fff&text=Icon+1',
            'https://dummyimage.com/800x1000/000/fff&text=Icon+2',
            'https://dummyimage.com/800x1000/000/fff&text=Icon+3',
            'https://dummyimage.com/800x1000/000/fff&text=Icon+4',
        ]

    @property
    def age(self):
        today = timezone.localdate()
        return today.year - self.dateOfBirth.year - (
                (today.month, today.day) <
                (self.dateOfBirth.month, self.dateOfBirth.day)
        )


class ReligiousProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='religiousProfile')
    madhab = models.CharField(max_length=20, choices=Madhab.choices, blank=True)
    prayerFrequency = models.CharField(max_length=25, choices=PrayerFrequency.choices, blank=True)
    quranReading = models.CharField(max_length=25, choices=QuranReading.choices, blank=True)
    observesFasting = models.BooleanField(null=True, blank=True)
    hijabStatus = models.CharField(max_length=10, blank=True, null=True, choices=HijabStatus.choices)
    halalLifestyle = models.BooleanField(null=True, blank=True)
    description = models.TextField(blank=True)


class EducationProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='educationProfile')
    qualification = models.CharField(max_length=30, choices=EducationLevel.choices)
    institution = models.CharField(max_length=255, blank=True)
    fieldOfStudy = models.CharField(max_length=150, blank=True)
    graduationYear = models.PositiveSmallIntegerField(null=True, blank=True)


class CareerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='careerProfile')
    employmentStatus = models.CharField(max_length=30, choices=EmploymentStatus.choices, blank=True)
    occupation = models.CharField(max_length=150, blank=True)
    industry = models.CharField(max_length=30, choices=Industry.choices, blank=True)


class LocationProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='locationProfile')
    town = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    nativePlace = models.CharField(max_length=100, blank=True)
    residency = models.CharField(max_length=100)
    citizenShip = models.JSONField(default=list, blank=True)
    willingToRelocate = models.BooleanField(null=True, blank=True)
    preferredCountries = models.JSONField(default=list, blank=True)


class FamilyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='familyProfile')
    fatherOccupation = models.CharField(max_length=150, blank=True)
    motherOccupation = models.CharField(max_length=150, blank=True)
    numberOfSiblings = models.PositiveSmallIntegerField(null=True, blank=True)
    familyValue = models.CharField(max_length=20, choices=FamilyValue.choices, blank=True)
    familyType = models.CharField(max_length=20, choices=FamilyType.choices, blank=True)
    familyStatus = models.CharField(max_length=20, choices=FamilyStatus.choices, blank=True)
    aboutMyFamily = models.TextField(blank=True)


class WaliProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='waliProfile')
    fullName = models.CharField(max_length=150)
    relationship = models.CharField(max_length=20, choices=Relationship.choices)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    consentToContact = models.BooleanField(null=True, blank=True)
    isVerified = models.BooleanField(null=True, blank=True)


class PartnerPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partnerPreference')
    minAge = models.PositiveSmallIntegerField(null=True, blank=True)
    maxAge = models.PositiveSmallIntegerField(null=True, blank=True)
    minHeight = models.PositiveSmallIntegerField(null=True, blank=True)
    maxHeight = models.PositiveSmallIntegerField(null=True, blank=True)
    maritalStatus = models.JSONField(default=list, blank=True)
    maxNumberOfChildren = models.PositiveSmallIntegerField(null=True, blank=True)
    nationality = models.JSONField(default=list, blank=True)
    physicalStatus = models.JSONField(default=list, blank=True)
    eatingHabit = models.JSONField(default=list, blank=True)
    smokingHabit = models.JSONField(default=list, blank=True)
    languages = models.JSONField(default=list, blank=True)
    residency = models.JSONField(default=list, blank=True)
    citizenship = models.JSONField(default=list, blank=True)
    qualification = models.JSONField(default=list, blank=True)
    employmentStatus = models.JSONField(default=list, blank=True)
    industry = models.JSONField(default=list, blank=True)
    madhab = models.JSONField(default=list, blank=True)
    prayerFrequency = models.JSONField(default=list, blank=True)
    quranReading = models.JSONField(default=list, blank=True)
    observesFasting = models.JSONField(default=list, blank=True)
    familyStatus = models.JSONField(default=list, blank=True)
    familyType = models.JSONField(default=list, blank=True)
    familyValue = models.JSONField(default=list, blank=True)
    additionalExpectations = models.TextField(blank=True)


class Shortlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shortlistedProfiles')
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shortlistedBy')
    createdAt = models.DateTimeField(auto_now_add=True)


class ProfileView(models.Model):
    viewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profilesViewed')
    viewed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profileViews')
    viewedAt = models.DateTimeField(auto_now_add=True)

# class ProfileVerification(models.Model):
#     class VerificationType(models.TextChoices):
#         EMAIL = 'EMAIL', 'Email'
#         PHONE = 'PHONE', 'Phone'
#         IDENTITY = 'IDENTITY', 'Identity'
#         PHOTO = 'PHOTO', 'Photo'
#         WALI = 'WALI', 'Wali'
#
#     class VerificationStatus(models.TextChoices):
#         PENDING = 'PENDING', 'Pending'
#         APPROVED = 'APPROVED', 'Approved'
#         REJECTED = 'REJECTED', 'Rejected'
#         EXPIRED = 'EXPIRED', 'Expired'
#
#     profile = models.ForeignKey(
#         MatrimonialProfile,
#         on_delete=models.CASCADE,
#         related_name='verifications'
#     )
#
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profileVerification')
#     verificationType = models.CharField(max_length=20, choices=VerificationType.choices)
#     status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.PENDING)
#     verifiedAt = models.DateTimeField(null=True, blank=True)
#     expiresAt = models.DateTimeField(null=True, blank=True)
#     reviewedBy = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
#                                    related_name='reviewedBy')
#     rejectionReason = models.TextField(blank=True)

#
# class Match(models.Model):
#     class MatchStatus(models.TextChoices):
#         SUGGESTED = 'SUGGESTED', 'Suggested'
#         INTERESTED = 'INTERESTED', 'Interested'
#         CONNECTED = 'CONNECTED', 'Connected'
#         DECLINED = 'DECLINED', 'Declined'
#         EXPIRED = 'EXPIRED', 'Expired'
#
#     profile_one = models.ForeignKey(
#         MatrimonialProfile,
#         on_delete=models.CASCADE,
#         related_name='matches_as_first'
#     )
#
#     profile_two = models.ForeignKey(
#         MatrimonialProfile,
#         on_delete=models.CASCADE,
#         related_name='matches_as_second'
#     )
#
#     compatibility_score = models.DecimalField(
#         max_digits=5,
#         decimal_places=2,
#         null=True,
#         blank=True
#     )
#
#     status = models.CharField(
#         max_length=20,
#         choices=MatchStatus.choices,
#         default=MatchStatus.SUGGESTED
#     )
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['profile_one', 'profile_two'],
#                 name='unique_profile_pair'
#             ),
#             models.CheckConstraint(
#                 condition=~models.Q(profile_one=models.F('profile_two')),
#                 name='match_profiles_must_differ'
#             )
#         ]
#
#
# class Interest(models.Model):
#     class InterestStatus(models.TextChoices):
#         PENDING = 'PENDING', 'Pending'
#         ACCEPTED = 'ACCEPTED', 'Accepted'
#         DECLINED = 'DECLINED', 'Declined'
#         WITHDRAWN = 'WITHDRAWN', 'Withdrawn'
#
#     sender = models.ForeignKey(
#         MatrimonialProfile,
#         on_delete=models.CASCADE,
#         related_name='sent_interests'
#     )
#
#     receiver = models.ForeignKey(
#         MatrimonialProfile,
#         on_delete=models.CASCADE,
#         related_name='received_interests'
#     )
#
#     status = models.CharField(
#         max_length=20,
#         choices=InterestStatus.choices,
#         default=InterestStatus.PENDING
#     )
#
#     message = models.TextField(blank=True)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#

#
# class Conversation(models.Model):
#     class ConversationStatus(models.TextChoices):
#         ACTIVE = 'ACTIVE', 'Active'
#         CLOSED = 'CLOSED', 'Closed'
#         BLOCKED = 'BLOCKED', 'Blocked'
#
#     status = models.CharField(
#         max_length=20,
#         choices=ConversationStatus.choices,
#         default=ConversationStatus.ACTIVE
#     )
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#
# class ConversationParticipant(models.Model):
#     class Role(models.TextChoices):
#         CANDIDATE = 'CANDIDATE', 'Candidate'
#         WALI = 'WALI', 'Wali'
#         FAMILY = 'FAMILY', 'Family Representative'
#
#     conversation = models.ForeignKey(
#         Conversation,
#         on_delete=models.CASCADE,
#         related_name='participants'
#     )
#
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#
#     role = models.CharField(max_length=20, choices=Role.choices)
#
#     joined_at = models.DateTimeField(auto_now_add=True)
#     left_at = models.DateTimeField(null=True, blank=True)
#
#
# class ProfilePrivacy(models.Model):
#     class Visibility(models.TextChoices):
#         PUBLIC = 'PUBLIC', 'All members'
#         MEMBERS = 'MEMBERS', 'Verified members'
#         MATCHES = 'MATCHES', 'Approved connections'
#         PRIVATE = 'PRIVATE', 'Private'
#
#     profile = models.OneToOneField(
#         MatrimonialProfile,
#         on_delete=models.CASCADE,
#         related_name='privacy'
#     )
#
#     visibility = models.CharField(
#         max_length=20,
#         choices=Visibility.choices,
#         default=Visibility.MEMBERS
#     )
#
#     show_age = models.BooleanField(default=True)
#     show_height = models.BooleanField(default=True)
#     show_location = models.BooleanField(default=True)
#     show_last_active = models.BooleanField(default=False)
#
#     allow_profile_views = models.BooleanField(default=True)
#     allow_messages = models.BooleanField(default=False)
#
#
# class BlockedProfile(models.Model):
#     blocker = models.ForeignKey(
#         MatrimonialProfile,
#         on_delete=models.CASCADE,
#         related_name='blocked_profiles'
#     )
#
#     blocked = models.ForeignKey(
#         MatrimonialProfile,
#         on_delete=models.CASCADE,
#         related_name='blocked_by'
#     )
#
#     reason = models.CharField(max_length=255, blank=True)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['blocker', 'blocked'],
#                 name='unique_blocked_profile'
#             )
#         ]
#
#
# class ProfileReport(models.Model):
#     class ReportReason(models.TextChoices):
#         FAKE_PROFILE = 'FAKE_PROFILE', 'Fake profile'
#         HARASSMENT = 'HARASSMENT', 'Harassment'
#         INAPPROPRIATE = 'INAPPROPRIATE', 'Inappropriate content'
#         SCAM = 'SCAM', 'Scam or fraud'
#         OTHER = 'OTHER', 'Other'
#
#     reporter = models.ForeignKey(
#         MatrimonialProfile,
#         on_delete=models.CASCADE,
#         related_name='reports_submitted'
#     )
#
#     reported = models.ForeignKey(
#         MatrimonialProfile,
#         on_delete=models.CASCADE,
#         related_name='reports_received'
#     )
#
#     reason = models.CharField(max_length=30, choices=ReportReason.choices)
#     description = models.TextField(blank=True)
#
#     is_resolved = models.BooleanField(default=False)
#
#     created_at = models.DateTimeField(auto_now_add=True)
