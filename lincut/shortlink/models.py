from django.db import models
from django.core.exceptions import ValidationError
import re

url_validation_regexp = re.compile(r"^(?:(https?):\/\/)?([^\/]+)(\/.*)?$")
regex_non_ascii_characters = re.compile(r"[^\x00-\x7F]")


def custom_url_validator(value):
    _contain_unsafe_char(value)
    match = url_validation_regexp.match(value)
    if not match:
        # I'm not sure if this is possible with this re
        raise ValidationError("URL malformed")
    protocol, domain, path = match.groups()
    if not protocol:
        raise ValidationError("URL protocol must be http:// or https://")
    if not domain:
        raise ValidationError("URL must contain domain")


def _contain_unsafe_char(value):
    forbidden_chars = (
        '"',
        "'",
        "<",
        ">",
        "{",
        "}",
        "[",
        "]",
        " ",
        "|",
        "\\",
        "\n",
        "\r",
        "`",
        "^",
    )
    for char in value:
        if char in forbidden_chars:
            raise ValidationError(f"URL must not containr character: {char}")
    if regex_non_ascii_characters.search(value):
        raise ValidationError(f"URL must contain only ASCII characters")


class LinkMap(models.Model):
    # INFO: CharField used as required in task description: "do not use build in types"
    orig_url = models.CharField(unique=True, validators=[custom_url_validator])
    url_hash = models.CharField(unique=True, validators=[custom_url_validator])
