from django.db import models

from .need import Need
from .user import User
from core.api.platform.utils import format_time

ORDER_STATE = (
    (0, "待接受"),
    (1, "正在合作中"),
    (2, "已拒绝"),
    (3, "合作结束"),
)


class Order(models.Model):
    #订单对应需求
    need = models.ForeignKey(Need, on_delete=models.CASCADE, related_name="need_order")
    #订单接收方专家
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expert_order")
    #订单的企业
    enterprise = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enterprise_order")

    # 订单创建时间，自动填充
    create_time = models.DateTimeField(auto_now_add=True)
    # 接单时间 TODO IN VIEW
    receive_time = models.DateTimeField(blank=True, null=True)
    # 订单结束时间
    end_time = models.DateTimeField(blank=True, null=True)

    #订单目前状态
    state = models.IntegerField(choices=ORDER_STATE, default=0)

    def to_dict(self) -> dict:
        return {
                "order_id": self.id,
                "create_time": format_time(self.create_time),
                "receive_time": format_time(self.receive_time),
                "end_time": format_time(self.end_time),
                "address": self.need.address,
                "description": self.need.description,
                "phone": self.enterprise.enterprise_info.phone,
                "state": self.state,
                "expert_id": self.user.id,
                "expert_name": self.user.expert_info.name,
                "need": {
                    "need_id": self.need.id,
                    "title": self.need.title,
                    "enterprise_id": self.enterprise.id,
                    "enterprise_name": self.enterprise.enterprise_info.name
                }
        }