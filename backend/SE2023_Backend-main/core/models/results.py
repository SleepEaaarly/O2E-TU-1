from django.db import models


RES_STATE_CHOICES = (
    (0, "待审核"),
    (1, "已通过"),
    (2, "未通过"),
)



class Multipic(models.Model):
    picture = models.ImageField(upload_to="images/%Y%m/%d/res_pic")


class Results(models.Model):
    title = models.TextField()
    abstract = models.TextField(blank=True, null=True)
    scholars = models.TextField(blank=True, null=True)
    pyear = models.IntegerField(blank=True, null=True)
    field = models.CharField(max_length=100, blank=True, null=True)
    period = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to="images/%Y%m/%d/res_pic", default="images/default_result_pic.jpg")
    content = models.TextField(blank=True, null=True)
    multipic = models.ManyToManyField(to=Multipic, related_name="result_multipic")
    # file = models.FileField(upload_to="pdf/%Y%m/%d/res_pdf")
    state = models.IntegerField(choices=RES_STATE_CHOICES, default=0)

    def get_pic(self):
        return str(self.picture)

    def get_pdf(self):
        return str(self.file)

    def to_dict(self) -> dict:
        return {"title": self.title, "abstract": self.abstract, "scholars": self.scholars,
                "pyear": self.pyear, "field": self.field, "period": self.period, "picture": self.picture,
                "content": self.content, "file": self.file, "state": self.state, "relate_expert_id": self.relate_expert_id}

