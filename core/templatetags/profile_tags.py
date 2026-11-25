from django import template
from django.utils.html import format_html

from core.choices import (
    Height,
)
from core.constants import PARTNER_PREFERENCES_DETAIL_PANEL

register = template.Library()


@register.simple_tag
def profile_detail(key, value, suffix=""):
    if value is None or value == "":
        value = "Not specified"
    elif isinstance(value, list):
        value = ", ".join(value) if value else "Not specified"
    elif isinstance(value, bool):
        value = "Yes" if value else "No"

    return format_html(
        '<div><dt>{}</dt><dd>{}{}</dd></div>',
        key,
        value,
        suffix
    )


@register.simple_tag
def preference_detail(key, value, field):
    if field in ('minHeight', 'maxHeight'):
        labels = {str(value): label for value, label in Height.choices}
        value = labels.get(str(value), value) if value is not None else None
    elif isinstance(value, list):
        labels = {str(value): label for value, label in PARTNER_PREFERENCES_DETAIL_PANEL.get(field, ())}
        value = ', '.join(labels.get(str(item), str(item)) for item in value) if value else None

    if value is None or value == '':
        value = 'Any' if field != 'additionalExpectations' else 'Not specified'

    return format_html('<div><dt>{}</dt><dd>{}</dd></div>', key, value)
