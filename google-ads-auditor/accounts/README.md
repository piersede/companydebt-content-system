# Account configurations

One YAML file per Google Ads account. `company-debt.yml` is the live config for the Company Debt account — see its inline comments for fields that still need real values (customer ID, conversion action names, target CPA, protected terms).

Run `python scripts/validate-config.py accounts/company-debt.yml` after editing to check required fields, catch conflicts (a term can't be both primary and ignored, or both protected and irrelevant), and confirm types.

Never commit customer IDs alongside OAuth credentials or developer tokens — the customer ID alone is not a secret, but keep credential files out of this directory regardless.
