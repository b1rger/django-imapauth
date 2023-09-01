from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

import imaplib
import logging

logger = logging.getLogger(__name__)


class ImapAuthBackend(BaseBackend):
    """
    Authenticate against an Imap Server (only selected accounts).
    """

    @property
    def host(self):
        return getattr(settings, "IMAP_AUTH_HOST")

    @property
    def superusers(self):
        return getattr(settings, "IMAP_AUTH_SUPERUSER", [])

    @property
    def staff(self):
        return getattr(settings, "IMAP_AUTH_STAFF", [])

    @property
    def all_accounts(self):
        return getattr(settings, "IMAP_AUTH", []) + self.staff + self.superusers

    def authenticate(self, request, username=None, password=None):
        if username and password:
            if username in self.all_accounts and self.host is not None:
                with imaplib.IMAP4_SSL(host=self.host) as con:
                    logger.info(f"Trying to login {username} via {self.host}")
                    try:
                        con.login(username, password)
                        logger.info(f"Login {username} via {self.host} succeeded!")
                        try:
                            user = User.objects.get(username=username)
                        except User.DoesNotExist:
                            # Create a new user. There's no need to set a password
                            # because only the password from imap is checked.
                            user = User(username=username)
                            user.is_staff = username in self.staff
                            user.is_superuser = username in self.superusers
                            user.save()
                        return user
                    except imaplib.IMAP4.error as e:
                        logger.info(f"IMAP Login for {username} failed: {e}")
                        return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
