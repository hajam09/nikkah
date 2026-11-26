import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django_countries import countries
from faker import Faker

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
    Language,
    MaritalStatus,
    Madhab,
    PhysicalStatus,
    PrayerFrequency,
    QuranReading,
    Relationship,
    SmokingHabit,
    Weight,
)
from core.constants import CHILDREN_CHOICES
from core.management.seed_data import (
    EDUCATIONAL_INSTITUTIONS,
    FIELDS_OF_STUDY,
    MOTHER_OCCUPATIONS,
)
from core.models import (
    CareerProfile,
    EducationProfile,
    FamilyProfile,
    MatrimonialProfile,
    LocationProfile,
    PartnerPreference,
    ProfileView,
    ReligiousProfile,
    Shortlist,
    WaliProfile,
)


class Command(BaseCommand):
    help = "Creates realistic users and profile data for local development."
    DEFAULT_NUMBER_OF_USERS = 100
    DEFAULT_PASSWORD = "admin"
    DEFAULT_SEED = 42

    def handle(self, *args, **options):
        number_of_users = self.DEFAULT_NUMBER_OF_USERS
        password = self.DEFAULT_PASSWORD
        random.seed(self.DEFAULT_SEED)
        Faker.seed(self.DEFAULT_SEED)

        self.faker = Faker("en_GB")
        self.stdout.write(f"Baking {number_of_users} nikkah profiles...")

        with transaction.atomic():
            users = self.seed_users(number_of_users, password)
            self.seed_profiles()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(users)} users. "
                f"Password for generated accounts: {password}"
            )
        )

    def delete_super_user_data(self):
        user = get_user_model().objects.get(username='admin', is_superuser=True)
        MatrimonialProfile.objects.filter(user=user).delete()
        ReligiousProfile.objects.filter(user=user).delete()
        EducationProfile.objects.filter(user=user).delete()
        CareerProfile.objects.filter(user=user).delete()
        LocationProfile.objects.filter(user=user).delete()
        FamilyProfile.objects.filter(user=user).delete()
        WaliProfile.objects.filter(user=user).delete()
        PartnerPreference.objects.filter(user=user).delete()

    def seed_users(self, number_of_users, password):
        User = get_user_model()
        User.objects.filter(is_superuser=False).delete()
        self.delete_super_user_data()

        now = timezone.now()
        three_months_ago = now - timedelta(days=90)

        users = []
        hashed_password = make_password(password)
        for index in range(number_of_users):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}.{index + 1}"
            email = f"{username}@example.com"

            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=self.faker.phone_number()[:15],
                isVerified=self.faker.boolean(chance_of_getting_true=75),
                password=hashed_password,
                last_login=self.faker.date_time_between(
                    start_date=three_months_ago,
                    end_date=now,
                    tzinfo=timezone.get_current_timezone(),
                )
            )
            users.append(user)

        return User.objects.bulk_create(users)

    def seed_profiles(self):
        country_choices = [name for _, name in countries]
        matrimonial_profiles = []
        religious_profiles = []
        education_profiles = []
        career_profiles = []
        location_profiles = []
        family_profiles = []
        wali_profiles = []
        partner_preferences = []
        shortlists = []
        profile_views = []

        users = list(get_user_model().objects.all())
        for user in users:
            gender = random.choice(Gender.values)
            date_of_birth = self.faker.date_of_birth(
                minimum_age=18,
                maximum_age=55,
            )
            minimum_height, maximum_height = (
                (150, 195) if gender == Gender.MALE else (145, 185)
            )
            height_values = [
                value for value in Height.values
                if minimum_height <= int(value) <= maximum_height
            ]
            height = random.choice(height_values)
            country = random.choice(country_choices)

            matrimonial_profiles.append(MatrimonialProfile(
                user=user,
                createdBy=random.choice(CreatedBy.values),
                gender=gender,
                dateOfBirth=date_of_birth,
                height=height,
                weight=random.choice(Weight.values),
                maritalStatus=random.choice(MaritalStatus.values),
                physicalStatus=random.choice(PhysicalStatus.values),
                languages=random.sample(
                    Language.values,
                    k=random.randint(1, min(3, len(Language.values))),
                ),
                eatingHabit=random.choice(EatingHabit.values),
                smokingHabit=random.choice(SmokingHabit.values),
                children=random.choices([0, 1, 2, 3, 4, 5], weights=[15, 20, 35, 20, 8, 2])[0],
                nationality=country,
            ))

            religious_profiles.append(ReligiousProfile(
                user=user,
                madhab=random.choice(Madhab.values),
                prayerFrequency=random.choice(PrayerFrequency.values),
                quranReading=random.choice(QuranReading.values),
                observesFasting=self.faker.boolean(),
                hijabStatus=(
                    random.choice(HijabStatus.values)
                    if gender == Gender.FEMALE
                    else None
                ),
                halalLifestyle=self.faker.boolean(chance_of_getting_true=90),
                description=self.faker.paragraph(nb_sentences=2),
            ))

            education_profiles.append(EducationProfile(
                user=user,
                educationLevel=random.choice(EducationLevel.values),
                institution=random.choice(EDUCATIONAL_INSTITUTIONS),
                fieldOfStudy=random.choice(FIELDS_OF_STUDY),
                graduationYear=random.randint(2005, date.today().year),
            ))

            career_profiles.append(CareerProfile(
                user=user,
                employmentStatus=random.choice(EmploymentStatus.values),
                occupation=self.faker.job()[:150],
                industry=random.choice(Industry.values),
            ))

            location_profiles.append(LocationProfile(
                user=user,
                town=self.faker.city(),
                city=self.faker.city(),
                nativePlace=self.faker.city(),
                residency=country,
                citizenShip=random.choice(country_choices),
                willingToRelocate=self.faker.boolean(chance_of_getting_true=35),
                preferredCountries=random.sample(
                    country_choices,
                    k=random.randint(0, min(3, len(country_choices))),
                ) if random.choice([True, False]) else [],
            ))

            family_profiles.append(FamilyProfile(
                user=user,
                fatherOccupation=self.faker.job()[:150],
                motherOccupation=random.choice(MOTHER_OCCUPATIONS),
                numberOfSiblings=random.randint(0, 8),
                familyValue=random.choice(FamilyValue.values),
                familyType=random.choice(FamilyType.values),
                familyStatus=random.choice(FamilyStatus.values),
                aboutMyFamily=self.faker.paragraph(nb_sentences=2),
            ))

            wali_profiles.append(WaliProfile(
                user=user,
                fullName=self.faker.name(),
                relationship=random.choice(Relationship.values),
                email=self.faker.email(),
                phone=self.faker.phone_number()[:20],
                consentToContact=self.faker.boolean(chance_of_getting_true=80),
                isVerified=self.faker.boolean(chance_of_getting_true=30),
            ))

            min_age = random.randint(18, 45)
            min_height = random.choice(Height.values)
            partner_preferences.append(PartnerPreference(
                user=user,
                minAge=min_age if random.choice([True, False]) else None,
                maxAge=random.randint(min_age, 70) if random.choice([True, False]) else None,
                minHeight=min_height if random.choice([True, False]) else None,
                maxHeight=random.choice([
                    value for value in Height.values if int(value) >= int(min_height)
                ]) if random.choice([True, False]) else None,
                maritalStatus=random.sample(
                    MaritalStatus.values,
                    k=random.randint(0, min(2, len(MaritalStatus.values))),
                ),
                children=random.sample(
                    [value for value, _ in CHILDREN_CHOICES],
                    k=random.randint(0, len(CHILDREN_CHOICES)),
                ),
                nationality=random.sample(country_choices, k=random.randint(0, min(3, len(country_choices)))),
                physicalStatus=random.sample(
                    PhysicalStatus.values,
                    k=random.randint(0, len(PhysicalStatus.values)),
                ),
                eatingHabit=random.sample(
                    EatingHabit.values,
                    k=random.randint(0, len(EatingHabit.values)),
                ),
                smokingHabit=random.sample(
                    SmokingHabit.values,
                    k=random.randint(0, len(SmokingHabit.values)),
                ),
                languages=random.sample(
                    Language.values,
                    k=random.randint(0, min(3, len(Language.values))),
                ),
                residency=random.sample(country_choices, k=random.randint(0, min(3, len(country_choices)))),
                citizenship=random.sample(country_choices, k=random.randint(0, min(3, len(country_choices)))),
                educationLevel=random.sample(
                    EducationLevel.values,
                    k=random.randint(0, len(EducationLevel.values)),
                ),
                employmentStatus=random.sample(
                    EmploymentStatus.values,
                    k=random.randint(0, len(EmploymentStatus.values)),
                ),
                industry=random.sample(
                    Industry.values,
                    k=random.randint(0, min(3, len(Industry.values))),
                ),
                madhab=random.sample(
                    Madhab.values,
                    k=random.randint(0, min(2, len(Madhab.values))),
                ),
                prayerFrequency=random.sample(
                    PrayerFrequency.values,
                    k=random.randint(0, min(2, len(PrayerFrequency.values))),
                ),
                quranReading=random.sample(
                    QuranReading.values,
                    k=random.randint(0, min(2, len(QuranReading.values))),
                ),
                observesFasting=random.sample(['YES', 'NO'], k=random.randint(0, 1)),
                familyStatus=random.sample(
                    FamilyStatus.values,
                    k=random.randint(0, min(2, len(FamilyStatus.values))),
                ),
                familyType=random.sample(
                    FamilyType.values,
                    k=random.randint(0, len(FamilyType.values)),
                ),
                familyValue=random.sample(
                    FamilyValue.values,
                    k=random.randint(0, len(FamilyValue.values)),
                ),
                additionalExpectations=self.faker.sentence() if random.choice([True, False]) else '',
            ))

            other_users = [other_user for other_user in users if other_user != user]
            if other_users:
                for viewed_user in random.sample(other_users, k=random.randint(1, min(10, len(other_users)))):
                    profile_views.append(ProfileView(viewer=user, viewed=viewed_user))

                for shortlisted_user in random.sample(other_users, k=random.randint(0, min(5, len(other_users)))):
                    shortlists.append(Shortlist(user=user, profile=shortlisted_user))

        MatrimonialProfile.objects.bulk_create(matrimonial_profiles)
        ReligiousProfile.objects.bulk_create(religious_profiles)
        EducationProfile.objects.bulk_create(education_profiles)
        CareerProfile.objects.bulk_create(career_profiles)
        LocationProfile.objects.bulk_create(location_profiles)
        FamilyProfile.objects.bulk_create(family_profiles)
        WaliProfile.objects.bulk_create(wali_profiles)
        PartnerPreference.objects.bulk_create(partner_preferences)
        ProfileView.objects.bulk_create(profile_views)
        Shortlist.objects.bulk_create(shortlists)
