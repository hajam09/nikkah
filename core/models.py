from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    isVerified = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class MatrimonialProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'

    class MaritalStatus(models.TextChoices):
        SINGLE = 'SINGLE', 'Single'
        DIVORCED = 'DIVORCED', 'Divorced'
        WIDOWED = 'WIDOWED', 'Widowed'
        ANNULLED = 'ANNULLED', 'Annulled'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='matrimonialProfile')
    gender = models.CharField(max_length=10, blank=True, null=True, choices=Gender.choices)
    dateOfBirth = models.DateField(blank=True, null=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)
    maritalStatus = models.CharField(max_length=10, blank=True, null=True, choices=MaritalStatus.choices)

    numberOfChildren = models.PositiveSmallIntegerField(default=0)
    nationality = models.CharField(max_length=100, blank=True)
    ethnicity = models.CharField(max_length=100, blank=True)


class ReligiousProfile(models.Model):
    class Madhab(models.TextChoices):
        HANAFI = 'HANAFI', 'Hanafi'
        SHAFI = 'SHAFI', 'Shafi'
        MALIKI = 'MALIKI', 'Maliki'
        HANBALI = 'HANBALI', 'Hanbali'
        PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY', 'Prefer not to say'

    class PrayerFrequency(models.TextChoices):
        FIVE_TIMES = 'FIVE_TIMES', 'Five times daily'
        MOST_PRAYERS = 'MOST_PRAYERS', 'Most prayers'
        SOMETIMES = 'SOMETIMES', 'Sometimes'
        RARELY = 'RARELY', 'Rarely'
        NOT_PRACTICING = 'NOT_PRACTICING', 'Not currently practicing'
        PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY', 'Prefer not to say'

    class QuranReading(models.TextChoices):
        DAILY = 'DAILY', 'Daily'
        SEVERAL_TIMES_WEEK = 'SEVERAL_TIMES_WEEK', 'Several times a week'
        WEEKLY = 'WEEKLY', 'Weekly'
        OCCASIONALLY = 'OCCASIONALLY', 'Occasionally'
        RAMADAN = 'RAMADAN', 'During Ramadan'
        RARELY = 'RARELY', 'Rarely'
        NOT_CURRENTLY = 'NOT_CURRENTLY', 'Not currently reading'
        PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY', 'Prefer not to say'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='religiousProfile')
    madhab = models.CharField(max_length=20, choices=Madhab.choices, blank=True)
    prayerFrequency = models.CharField(max_length=20, choices=PrayerFrequency.choices, blank=True)
    quranReading = models.CharField(max_length=25, choices=QuranReading.choices, blank=True, )
    observesFasting = models.BooleanField(null=True, blank=True)
    wearsHijab = models.BooleanField(null=True, blank=True)
    wearsNiqab = models.BooleanField(null=True, blank=True)
    halalLifestyle = models.BooleanField(default=True)
    religiousPracticeDescription = models.TextField(blank=True)


class Education(models.Model):
    class EducationLevel(models.TextChoices):
        HIGH_SCHOOL = 'HIGH_SCHOOL', 'High School'
        DIPLOMA = 'DIPLOMA', 'Diploma'
        BACHELORS = 'BACHELORS', "Bachelor's"
        MASTERS = 'MASTERS', "Master's"
        PHD = 'PHD', 'PhD'
        ISLAMIC_STUDIES = 'ISLAMIC_STUDIES', 'Islamic Studies'
        OTHER = 'OTHER', 'Other'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='educations')
    qualification = models.CharField(max_length=30, choices=EducationLevel.choices)
    institution = models.CharField(max_length=255, blank=True)
    fieldOfStudy = models.CharField(max_length=150, blank=True)
    graduationYear = models.PositiveSmallIntegerField(null=True, blank=True)


class CareerProfile(models.Model):
    class EmploymentStatus(models.TextChoices):
        EMPLOYED = 'EMPLOYED', 'Employed'
        SELF_EMPLOYED = 'SELF_EMPLOYED', 'Self Employed'
        BUSINESS_OWNER = 'BUSINESS_OWNER', 'Business Owner'
        STUDENT = 'STUDENT', 'Student'
        UNEMPLOYED = 'UNEMPLOYED', 'Unemployed'
        RETIRED = 'RETIRED', 'Retired'

    class Industry(models.TextChoices):
        IT = 'IT', 'Information Technology'
        HEALTHCARE = 'HEALTHCARE', 'Healthcare'
        EDUCATION = 'EDUCATION', 'Education'
        FINANCE = 'FINANCE', 'Finance'
        ENGINEERING = 'ENGINEERING', 'Engineering'
        GOVERNMENT = 'GOVERNMENT', 'Government'
        CONSTRUCTION = 'CONSTRUCTION', 'Construction'
        RETAIL = 'RETAIL', 'Retail'
        MANUFACTURING = 'MANUFACTURING', 'Manufacturing'
        HOSPITALITY = 'HOSPITALITY', 'Hospitality'
        LEGAL = 'LEGAL', 'Legal'
        TRANSPORT = 'TRANSPORT', 'Transport'
        AGRICULTURE = 'AGRICULTURE', 'Agriculture'
        ARTS_MEDIA = 'ARTS_MEDIA', 'Arts and Media'
        CONSULTING = 'CONSULTING', 'Consulting'
        ENERGY_UTILITIES = 'ENERGY_UTILITIES', 'Energy and Utilities'
        ENVIRONMENT = 'ENVIRONMENT', 'Environment'
        INSURANCE = 'INSURANCE', 'Insurance'
        NONPROFIT = 'NONPROFIT', 'Nonprofit'
        REAL_ESTATE = 'REAL_ESTATE', 'Real Estate'
        SCIENCE_RESEARCH = 'SCIENCE_RESEARCH', 'Science and Research'
        TELECOMMUNICATIONS = 'TELECOMMUNICATIONS', 'Telecommunications'
        OTHER = 'OTHER', 'Other'
        PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY', 'Prefer not to say'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='careerProfile')
    employmentStatus = models.CharField(max_length=30, choices=EmploymentStatus.choices, blank=True)
    occupation = models.CharField(max_length=150, blank=True)
    industry = models.CharField(max_length=30, choices=Industry.choices, blank=True)


class ProfileLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profileLocation')
    town = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    willingToRelocate = models.BooleanField(default=False)
    preferredCountries = models.JSONField(default=list, blank=True)


class FamilyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='familyProfile')
    fatherOccupation = models.CharField(max_length=150, blank=True)
    motherOccupation = models.CharField(max_length=150, blank=True)
    numberOfSiblings = models.PositiveSmallIntegerField(null=True, blank=True)
    familyBackground = models.TextField(blank=True)
    familyValues = models.TextField(blank=True)


class Wali(models.Model):
    class Relationship(models.TextChoices):
        FATHER = 'FATHER', 'Father'
        BROTHER = 'BROTHER', 'Brother'
        GRANDFATHER = 'GRANDFATHER', 'Grandfather'
        UNCLE = 'UNCLE', 'Uncle'
        OTHER = 'OTHER', 'Other'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wali')
    fullName = models.CharField(max_length=150)
    relationship = models.CharField(max_length=20, choices=Relationship.choices)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    consentToContact = models.BooleanField(default=False)
    isVerified = models.BooleanField(default=False)

#
# class PartnerPreference(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partnerPreference')
#     minAge = models.PositiveSmallIntegerField(null=True, blank=True)
#     maxAge = models.PositiveSmallIntegerField(null=True, blank=True)
#     minHeightCm = models.PositiveSmallIntegerField(null=True, blank=True)
#     maxHeightCm = models.PositiveSmallIntegerField(null=True, blank=True)
#     preferred_marital_status = models.JSONField(default=list, blank=True)
#     preferredNationalities = models.JSONField(default=list, blank=True)
#     preferredEthnicities = models.JSONField(default=list, blank=True)
#     willingToAcceptChildren = models.BooleanField(null=True, blank=True)
#     willingToRelocate = models.BooleanField(null=True, blank=True)
#     preferredReligiousPractice = models.TextField(blank=True)
#     additionalExpectations = models.TextField(blank=True)


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
# class Shortlist(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='shortlisted_profiles'
#     )
#
#     profile = models.ForeignKey(
#         MatrimonialProfile,
#         on_delete=models.CASCADE,
#         related_name='shortlisted_by'
#     )
#
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'profile'],
#                 name='unique_user_shortlist'
#             )
#         ]
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
