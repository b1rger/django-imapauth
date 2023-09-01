# Django IMAP Auth

Lets you authenticate your Django users against an IMAP server.

Configuration settings:

* `IMAP_AUTH_HOST`: your IMAP server

* `IMAP_AUTH`: a list of accounts that should be authenticated against the IMAP server (defaults to empty list); example: `['alice', 'bob']`

* `IMAP_AUTH_STAFF`: a list of staff accounts that should be authenticated against the IMAP server (defaults to empty list); example: `['carol']`

* `IMAP_AUTH_SUPERUSER`: a list of superuser accounts that should be authenticated against the IMAP server (defaults to empty list); example: `['ted', 'grace']`
