from django.db import models


class Patents(models.Model):
    title = models.TextField()
    pyear = models.IntegerField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    scholars = models.TextField(blank=True, null=True)

    def to_dict(self) -> dict:
        return {"title": self.title, "pyear": self.pyear, "url": self.url, "scholarrs": self.scholars}