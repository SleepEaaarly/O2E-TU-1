"""
Switch message: 模式转换消息
"""
from django.db import models
from django.contrib.auth import get_user_model
from .user import User
<<<<<<< HEAD
from .message import Message
=======
from .system_message import SystemMessage
>>>>>>> 4bb4ae121deaa8e30fdb67117994c9103adf4afc

UNREAD = 0
READ = 1

READ_STATE_CHIOCES = (
    (0, 'Not read'),
    (1, 'Read'),
)

AI = 0
MANUAL = 1

SWITCH_TYPE = (
    (0, 'AI'),
    (1, 'Manual'),
)


<<<<<<< HEAD
class SwitchMessage(Message):
=======
class SwitchMessage(SystemMessage):
>>>>>>> 4bb4ae121deaa8e30fdb67117994c9103adf4afc
    """
    Field:
        - 与Message的字段完全一样，只是content的内容是转换后的模式
    """

    @classmethod
    def new_switch_message(cls,
<<<<<<< HEAD
                           from_user: User,
                           to_user: User,
                           content: str,
                           ):
        try:
            new_switch_message = SwitchMessage(content=content, from_user=from_user,
                                               to_user=to_user, read_state=UNREAD,
=======
                           owner: User,
                           is_to_system: int,
                           content: str,
                           ):
        try:
            new_switch_message = SwitchMessage(content=content, owner=owner,
                                               is_to_system=is_to_system, read_state=UNREAD,
>>>>>>> 4bb4ae121deaa8e30fdb67117994c9103adf4afc
                                               )
            new_switch_message.save()
            return new_switch_message.id
        except Exception:
            return -1
