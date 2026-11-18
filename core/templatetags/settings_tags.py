from django import template

register = template.Library()


@register.inclusion_tag('core/includes/settings_navigation.html')
def settings_navigation(active_setting):
    return {'active_setting': active_setting}
