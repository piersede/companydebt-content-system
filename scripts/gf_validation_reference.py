"""Reference implementation of the phone and email rules in
mu-plugins/cd-gform-hardening.php. Mirrored exactly in PHP; used to backtest
rule changes against real Gravity Forms entries before deploying them.
"""
import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
UK_MOBILE = re.compile(r"^07[1-9]\d{8}$")
UK_GEO    = re.compile(r"^0(1\d{8,9}|2\d{9}|3\d{9}|5\d{9}|8\d{8,9}|9\d{9})$")


def check_email(raw):
    v = (raw or "").strip()
    if v == "":
        return False, "empty"
    if " " in v or "	" in v:
        return False, "contains a space"
    if not EMAIL_RE.match(v):
        return False, "not an email address"
    dom = v.rsplit("@", 1)[1].lower()
    if dom.endswith(".") or ".." in v or dom.startswith("-"):
        return False, "malformed domain"
    return True, "ok"


def _junk(d):
    core = d.lstrip("0")
    if len(set(core)) <= 1:
        return True
    for n in (2, 3, 4):
        if len(core) >= n * 2 and core == (core[:n] * (len(core) // n + 1))[:len(core)]:
            return True
    return core in ("123456789", "1234567890", "12345678901")


def _strip_trunk(rest):
    """Drop the trunk "0" British people write in brackets after the country
    code: "+44 (0)7700 900123". Stripping non-digits makes that "4407700900123",
    and the usual "0" prefix gave "007700900123", which failed every shape check
    and refused a genuine enquirer. Removes ONE zero, only after the 44 is off."""
    return rest[1:] if rest.startswith("0") else rest


def normalise_phone(raw):
    s = (raw or "").strip()
    digits = re.sub(r"\D", "", s)
    if not digits:
        return "", "none"
    if s.startswith("+"):
        return ("0" + _strip_trunk(digits[2:]), "uk") if digits.startswith("44") else ("+" + digits, "intl")
    if digits.startswith("00"):
        d = digits[2:]
        return ("0" + _strip_trunk(d[2:]), "uk") if d.startswith("44") else ("+" + d, "intl")
    if digits.startswith("44") and len(digits) == 12:
        return "0" + digits[2:], "uk"
    if digits.startswith("0"):
        return digits, "uk"
    # Only promote a bare mobile missing its leading zero when the raw input is
    # digits and spaces. "(724) 746-3096" is North American and must not become
    # a plausible UK mobile.
    if len(digits) == 10 and digits[0] == "7" and re.fullmatch(r"[\d\s]+", s):
        return "0" + digits, "uk"
    return digits, "bare"


def check_phone(raw, allow_intl=True):
    """Returns (acceptable, normalised, reason). Empty is acceptable here; the
    form's own required setting decides whether an empty box is allowed."""
    v = (raw or "").strip()
    if v == "":
        return True, "", ""
    norm, kind = normalise_phone(v)
    digits = re.sub(r"\D", "", norm)
    if len(digits) < 9:
        return False, norm, "short"
    if _junk(digits):
        return False, norm, "filler"
    if kind == "uk":
        n = len(digits)
        if norm.startswith("07"):
            if n < 11:
                return False, norm, "short"
            if n > 11:
                return False, norm, "long"
            return (True, norm, "") if UK_MOBILE.match(norm) else (False, norm, "uk_shape")
        if n < 10:
            return False, norm, "short"
        if n > 11:
            return False, norm, "long"
        if norm.startswith("09"):
            return False, norm, "premium"
        return (True, norm, "") if UK_GEO.match(norm) else (False, norm, "uk_shape")
    if kind == "intl":
        n = len(digits)
        if allow_intl and 8 <= n <= 15:
            return True, norm, ""
        return False, norm, "intl_shape"
    return False, norm, "no_country_code"


def to_e164(raw):
    """What gets stored: Google Ads enhanced conversions only match E.164."""
    norm, kind = normalise_phone(raw)
    if kind == "uk":
        return "+44" + norm[1:]
    if kind == "intl":
        return norm
    return ""


def phone_tariff(norm):
    if re.match(r"^0(84|87)", norm):
        return "revenue-share"
    if re.match(r"^0(800|808)", norm):
        return "freephone"
    return ""
