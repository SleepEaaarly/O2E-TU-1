from django.db import models


RES_STATE_CHOICES = (
    (0, "待审核"),
    (1, "已通过"),
    (2, "未通过"),
)


class ResMultipic(models.Model):
    picture = models.ImageField(upload_to="images/%Y%m/%d/res_pic")


class Results(models.Model):
    title = models.TextField()
    abstract = models.TextField(blank=True, null=True)
    scholars = models.TextField(blank=True, null=True)
    pyear = models.CharField(max_length=100, blank=True, null=True)
    field = models.CharField(max_length=100, blank=True, null=True)
    period = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to="images/%Y%m/%d/res_pic", default="images/default_result_pic.jpg")
    content = models.TextField(blank=True, null=True)
    multipic = models.ManyToManyField(to=ResMultipic, related_name="results_set")
    # file = models.FileField(upload_to="pdf/%Y%m/%d/res_pdf")
    state = models.IntegerField(choices=RES_STATE_CHOICES, default=0)
    vector = models.TextField(blank=True, null=True)

    def get_pic(self):
        return str(self.picture)

    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "abstract": self.abstract, "scholars": self.scholars,
                "pyear": self.pyear, "field": self.field, "period": self.period, "picture": self.get_pic(),
                "content": self.content, "state": self.state}

