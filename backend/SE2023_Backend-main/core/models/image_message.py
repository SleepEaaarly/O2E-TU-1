"""
Image message: 图像消息
"""
from django.db import models
from django.contrib.auth import get_user_model
from .user import User

from .system_message import SystemMessage


UNREAD = 0
READ = 1

READ_STATE_CHIOCES = (
    (0, 'Not read'),
    (1, 'Read'),
)



class ImageMessage(SystemMessage):

    """
    Field:
        - 与Message的字段完全一样，只是content的内容是图片的存储路径
    """

    @classmethod
    def new_image_message(cls,

                          owner: User,
                          is_to_system: int,
                          content: str,
                          ):
        try:
            new_image_message = ImageMessage(content=content, owner=owner,
                                             is_to_system=is_to_system, read_state=UNREAD,
                                             )
            new_image_message.save()
            return new_image_message.id
        except Exception:
            return -1
