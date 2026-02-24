from django import template

register = template.Library()


@register.filter
def status_badge(value):
    mapping = {
        "active": "badge badge--success",
        "paused": "badge badge--warning",
        "expired": "badge badge--muted",
        "cancelled": "badge badge--danger",
        "scheduled": "badge badge--info",
        "completed": "badge badge--success",
    }
    return mapping.get(str(value), "badge")


@register.simple_tag(takes_context=True)
def is_active_path(context, prefix):
    request = context.get("request")
    if not request:
        return ""
    return "is-active" if request.path.startswith(prefix) else ""
