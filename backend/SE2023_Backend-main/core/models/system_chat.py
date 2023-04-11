"""
SystemChatroom: 用户与平台的聊天
"""
from django.db import models


from .system_message import SystemMessage

from .user import User
from core.api.platform.utils import get_now_time


class SystemChatroom(models.Model):
    """
    Fields:
        - id
        - owner: owner of the chatroom, that is the user id.
        - message: list of messages
        - isai: whether the user in ai mode or manual mode.0 for AI reply, 1 for Manual reply
        - last_message_time
        - unread_message_num
    """
    AI_REPLY = 0
    MANUAL_REPLY = 1
    owner = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="system_chatroom_list")
    created_at = models.DateTimeField(auto_now_add=True)
    messages = models.ManyToManyField(

        'SystemMessage', related_name='system_message_list')

    isai = models.IntegerField()
    last_message_time = models.DateTimeField()
    unread_message_num = models.IntegerField()

    # 新加入一条消息
    def add_message(self, message_id: int) -> bool:
        try:

            m = SystemMessage.objects.get(id=message_id)
            self.messages.add(m)
            self.last_message_time = get_now_time()
            self.unread_message_num = self.unread_message_num + 1
            self.save()
            return True
        except Exception:
            return False

    # 切换聊天模式
    def alter_mode(self, mode: int):
        try:
            self.isai = mode
            self.save()
            return True
        except Exception:
            return False
