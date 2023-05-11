from django.db import models


class QuesMultipic(models.Model):
    picture = models.ImageField(upload_to="images/%Y%m/%d/ques_pic")


class Question(models.Model):
    question = models.TextField(blank=True, null=True)
    ans = models.TextField(blank=True, null=True)
    multipic = models.ManyToManyField(to=QuesMultipic, related_name="question_multipic")
    vector_hit = models.TextField(blank=True, null=True)

    def get_multipic(self):
        return self.multipic.all()