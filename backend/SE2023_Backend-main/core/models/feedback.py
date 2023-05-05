from django.db import models
from core.models.user import User

FLAG = (
    (0, '未回复'),
    (1, '已回复'),
)


'''
管理员和用户的反馈消息

'''
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_feedback", default=19)
    # enterprise = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enterprise_need")
    name = models.CharField(max_length=20, blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    qtype = models.CharField(max_length=10)
    description = models.TextField()
    dataTime = models.DateTimeField(auto_now_add=True)
    flag = models.IntegerField(choices=FLAG, default=0)
    message = models.TextField(blank=True, null=True)


    
