"""Reference implementation of the proposed rules. Mirrored exactly in PHP."""
import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

def check_email(raw):
    v = (raw or "").strip()
    if v == "":
        return False, "empty"
    if " " in v or "\t" in v:
        return False, "contains a space"
    if not EMAIL_RE.match(v):
        return False, "not an email address"
    dom = v.rsplit("@", 1)[1].lower()
    if dom.endswith(".") or ".." in v or dom.startswith("-"):
        return False, "malformed domain"
    return True, "ok"

UK_MOBILE   = re.compile(r"^07[1-9]\d{8}$")
UK_GEO      = re.compile(r"^0(1\d{8,9}|2\d{9}|3\d{9}|5\d{9}|8\d{8,9}|9\d{9})$")

def _junk(d):
    core = d.lstrip("0")
    if len(set(core)) <= 1:
        return True                                   # 077777777777, 9999999999
    for n in (2, 3, 4):                               # 1201201200, 213213213
        if len(core) >= n * 2 and core == (core[:n] * (len(core) // n + 1))[:len(core)]:
            return True
    if core in ("123456789", "1234567890", "12345678901"):
        return True
    return False

def normalise_phone(raw):
    s = (raw or "").strip()
    digits = re.sub(r"\D", "", s)
    if not digits:
        return "", "none"
    if s.startswith("+"):
        return ("0" + digits[2:], "uk") if digits.startswith("44") else ("+" + digits, "intl")
    if digits.startswith("00"):
        d = digits[2:]
        return ("0" + d[2:], "uk") if d.startswith("44") else ("+" + d, "intl")
    if digits.startswith("44") and len(digits) == 12:
        return "0" + digits[2:], "uk"
    if digits.startswith("0"):
        return digits, "uk"
    if len(digits) == 10 and digits[0] == "7":        # UK mobile, leading zero omitted
        return "0" + digits, "uk"
    return digits, "bare"

def check_phone(raw, allow_intl=True):
    v = (raw or "").strip()
    if v == "":
        return True, "", "empty (optional)"
    norm, kind = normalise_phone(v)
    digits = re.sub(r"\D", "", norm)
    if len(digits) < 9:
        return False, norm, "too short"
    if _junk(digits):
        return False, norm, "repeated/sequential junk"
    if kind == "uk":
        if UK_MOBILE.match(norm) or UK_GEO.match(norm):
            return True, norm, "uk"
        return False, norm, "not a valid UK number"
    if kind == "intl":
        if allow_intl and 8 <= len(digits) <= 15:
            return True, norm, "international"
        return False, norm, "non-UK number"
    return False, norm, "no country code and not a UK number"
