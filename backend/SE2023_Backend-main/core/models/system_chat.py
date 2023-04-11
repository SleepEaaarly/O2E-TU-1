"""
SystemChatroom: 用户与平台的聊天
"""
from django.db import models

<<<<<<< HEAD
from .message import Message
=======
from .system_message import SystemMessage
>>>>>>> 4bb4ae121deaa8e30fdb67117994c9103adf4afc
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
<<<<<<< HEAD
        'Message', related_name='system_message_list')
=======
        'SystemMessage', related_name='system_message_list')
>>>>>>> 4bb4ae121deaa8e30fdb67117994c9103adf4afc
    isai = models.IntegerField()
    last_message_time = models.DateTimeField()
    unread_message_num = models.IntegerField()

    # 新加入一条消息
    def add_message(self, message_id: int) -> bool:
        try:
<<<<<<< HEAD
            m = Message.objects.get(id=message_id)
=======
            m = SystemMessage.objects.get(id=message_id)
>>>>>>> 4bb4ae121deaa8e30fdb67117994c9103adf4afc
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
