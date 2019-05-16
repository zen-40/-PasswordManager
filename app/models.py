from django.db import models
from django.conf import settings


class PasswordObject(models.Model):
    site_name = models.CharField(max_length=100)
    site_url = models.URLField()
    account_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '%s - %s' %(self.site_name, self.user)

    class Meta:
        ordering = ['-date_created']
