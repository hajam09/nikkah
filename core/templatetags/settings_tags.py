from django import template
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from core.constants import SETTINGS_PANEL

register = template.Library()


@register.simple_tag(takes_context=True)
def settings_navigation_list(context):
    request = context.get('request')
    active_url_name = request.resolver_match.view_name if request and request.resolver_match else None

    links = format_html_join(
        '\n',
        '<a class="nav-link{}" href="{}"{}>{}</a>',
        (
            (
                ' active' if url_name == active_url_name else '',
                reverse(url_name),
                ' aria-current="page"' if url_name == active_url_name else '',
                label,
            )
            for label, url_name in SETTINGS_PANEL
        )
    )

    return format_html(
        '<nav class="nav nav-pills flex-column gap-1 settings-nav" aria-label="Settings">{}</nav>',
        links
    )
