from django.db import models
from .user import User


class AIReport(models.Model):
    TO_ENTERPRISE = 0  # 成果报告
    TO_EXPERT = 1   # 需求报告
    
    # 报告生成时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 报告类型
    type = models.IntegerField()
    # 成果/需求/订单id
    involved_id = models.IntegerField()
    # 报告内容
    content = models.CharField(max_length=10000)

    