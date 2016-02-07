from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext, ugettext_lazy as _
from player_api.utils import get_user_model_name

user_model_name = get_user_model_name()


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        _now = now()
        self.updated = _now
        if not self.id:
            self.created = _now
        super(TimeStamped, self).save(*args, **kwargs)


class SoftOwned(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(user_model_name, verbose_name=_("Author"), related_name="+")


class SoftOwnable(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(user_model_name, verbose_name=_("Author"), related_name="+", blank=True, null=True)


class Owned(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(user_model_name, verbose_name=_("Author"), related_name="%(class)ss")


class Ownable(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(user_model_name, verbose_name=_("Author"), related_name="%(class)ss", blank=True, null=True)