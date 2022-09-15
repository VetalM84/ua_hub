"""Custom template filters."""

from django import template
from django.utils.formats import date_format

register = template.Library()


@register.filter
def to_user_tz_short(dt):
    """Format UTC timestamp from DB to local user's short datetime format with appropriate timezone."""
    user_tz = date_format(
        dt.astimezone(), format="SHORT_DATETIME_FORMAT", use_l10n=True
    )
    return user_tz
