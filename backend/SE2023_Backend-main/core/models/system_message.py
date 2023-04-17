"""
message: 文字消息
"""
from django.db import models
from django.contrib.auth import get_user_model
from .user import User
from datetime import datetime

UNREAD = 0
READ = 1

READ_STATE_CHIOCES = (
    (0, 'Not read'),
    (1, 'Read'),
)

FROM_SYSTEM = 0
TO_SYSTEM = 1


class SystemMessage(models.Model):
    """
    Field:
        - content
        - owner
        - is_to_system
        - created_at
        - read_state
        - type
    """
    type = models.CharField(max_length=30)
    content = models.CharField(max_length=140)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_user")
    is_to_system = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_state = models.IntegerField(choices=READ_STATE_CHIOCES)

    def set_read(self):
        """
        把消息标注为已读
        :return: 操作是否成功: boolean
        """
        try:
            self.read_state = READ
            self.save()
            print("[DBEUG] message already read" + self.read_state)
            return True
        except Exception:
            return False

    @classmethod
    def new_message(cls,
                    owner: User,
                    is_to_system: int,
                    content: str,
                    type: str):
        try:
            new_message = SystemMessage(content=content,
                                        owner=owner,
                                        is_to_system=is_to_system,
                                        type = type,
                                        read_state=UNREAD)
            new_message.save()
            print(new_message.id)
            return new_message.id
        except Exception:
            return -1
    
    def get_create_time(self):
        return self.created_at.strftime("%Y-%m-%d, %H:%M:%S")
