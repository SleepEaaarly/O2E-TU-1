from django.db import models
from .user import User
from .need import Need


class NeedContact(models.Model):
    # expert
    expert = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expert_need_contact")
    # enterprise
    enterprise = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enterprise_need_contact")
    # need
    need = models.ForeignKey(Need, on_delete=models.CASCADE, related_name="need_contact")

    