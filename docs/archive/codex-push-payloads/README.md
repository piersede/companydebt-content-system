# Archived payloads from stale `codex-push-*.php` mu-plugins

Four one-shot content-push mu-plugins were found on staging on 2026-07-29, dated 30 April 2026.
Each held a base64-encoded WordPress post body and would `wp_update_post()` it when hit with a
secret query token, then delete itself. None had fired (they were still present).

The PHP files are being removed from staging because a WP Engine file-system copy pushes every
file to live, and these are unauthenticated write endpoints guarded only by a static token.
The article content they carried is preserved here so nothing is lost.

| Archived file | Target post ID | Bytes |
|---|---|---|
| `codex-push-46579-1777527150.html` | 46579 | 38,017 |
| `codex-push-77207-1777525951.html` | 77207 | 49,232 |
| `codex-push-77207-1777526107.html` | 77207 | 49,252 |
| `codex-push-77216-1777526531.html` | 77216 | 45,627 |
