from django.db import models
from django.utils.translation import ugettext_lazy as _

from silent_night.mixins.models import TimeStamped, Owned


# Create your models here.
class Profile(TimeStamped):
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ["-created"]

    user = models.OneToOneField("auth.User", related_name="%(class)s")
    nickname = models.CharField(_("Nickname"), max_length=50)
    description = models.CharField(_("Description"), max_length=5000, blank=True, null=True)
    image = models.ImageField(upload_to="profile_images", blank=True, null=True)

    def __str__(self):
        return self.nickname

    def get_full_name(self):
        return self.user.get_full_name()
