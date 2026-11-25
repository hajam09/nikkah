from calendar import monthrange
from datetime import timedelta

from django.utils import timezone

from core.choices import Gender, CreatedBy, MaritalStatus, SmokingHabit
from core.constants import MATRIMONIAL_PROFILE_RELATIONS
from core.models import MatrimonialProfile


def getOppositeGender(user):
    gender = MatrimonialProfile.objects.values_list('gender', flat=True).get(user=user)
    return Gender.FEMALE if gender == Gender.MALE else Gender.MALE


def getDateOfBirthFromAge(age):
    today = timezone.localdate()
    year = today.year - age
    month = today.month
    return today.replace(year=year, month=month, day=min(today.day, monthrange(year, month)[1]))


def getBaseMatches(user):
    return MatrimonialProfile.objects.filter(gender=getOppositeGender(user)).select_related(
        *MATRIMONIAL_PROFILE_RELATIONS
    ).exclude(user=user)


def getMatchesJoinedRecently(user):
    last30Days = timezone.now() - timedelta(days=30)
    return getBaseMatches(user).filter(user__createdAt__gte=last30Days)


def getMatchesRecentlyActive(user):
    last30Days = timezone.now() - timedelta(days=30)
    return getBaseMatches(user).filter(user__last_login__gte=last30Days)


def getMatchesCreatedByParentOrRelative(user):
    return getBaseMatches(user).filter(
        createdBy__in=[
            CreatedBy.PARENTS,
            CreatedBy.SIBLING,
            CreatedBy.RELATIVE,
        ]
    )


def getMatchesSingle(user):
    return getBaseMatches(user).filter(maritalStatus=MaritalStatus.SINGLE)


def getMatchesDivorced(user):
    return getBaseMatches(user).filter(maritalStatus=MaritalStatus.DIVORCED)


def getMatchesWidowed(user):
    return getBaseMatches(user).filter(maritalStatus=MaritalStatus.WIDOWED)


def getMatchesWithoutChildren(user):
    return getBaseMatches(user).filter(numberOfChildren=0)


def getMatchesWithChildren(user):
    return getBaseMatches(user).filter(numberOfChildren__gt=0)


def getMatchesBetween18And25(user):
    return getBaseMatches(user).filter(
        dateOfBirth__lte=getDateOfBirthFromAge(18),
        dateOfBirth__gt=getDateOfBirthFromAge(26)
    )


def getMatchesBetween26And35(user):
    return getBaseMatches(user).filter(
        dateOfBirth__lte=getDateOfBirthFromAge(26),
        dateOfBirth__gt=getDateOfBirthFromAge(36)
    )


def getMatches36AndAbove(user):
    return getBaseMatches(user).filter(dateOfBirth__lte=getDateOfBirthFromAge(36))


def getMatchesNonSmokers(user):
    return getBaseMatches(user).filter(smokingHabit=SmokingHabit.NON_SMOKER)


def getMatchesWillingToRelocate(user):
    return getBaseMatches(user).filter(locationProfile__willingToRelocate=True)


MATCHES_FILTER_FUNCTIONS = {
    'newly-joined': getMatchesJoinedRecently,
    'recently-active': getMatchesRecentlyActive,
    'created-by-family': getMatchesCreatedByParentOrRelative,
    'single': getMatchesSingle,
    'divorced': getMatchesDivorced,
    'widowed': getMatchesWidowed,
    'no-children': getMatchesWithoutChildren,
    'with-children': getMatchesWithChildren,
    'age-18-25': getMatchesBetween18And25,
    'age-26-35': getMatchesBetween26And35,
    'age-36-plus': getMatches36AndAbove,
    'non-smoker': getMatchesNonSmokers,
    'relocate': getMatchesWillingToRelocate,
}
