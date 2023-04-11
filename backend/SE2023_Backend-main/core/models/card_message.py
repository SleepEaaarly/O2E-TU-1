"""
card message: 卡片式消息
"""
from django.db import models
from django.contrib.auth import get_user_model
from .user import User

from .message import Message

from .system_message import SystemMessage


UNREAD = 0
READ = 1

READ_STATE_CHIOCES = (
    (0, 'Not read'),
    (1, 'Read'),
)

EXPERT = 0
ENTERPRISE = 1
DEMAND = 2
TECHNIQUE = 3

CARD_TYPE = (
    (0, 'expert'),
    (1, 'enterprise'),
    (2, 'demand'),
    (3, 'technique')
)


class CardMessage(SystemMessage):

    """
    Field:
        - card_type: 卡片信息类型
        - title: 卡片标题 (卡片内容共用Message中的content字段)
        - avatar: 卡片内图像
    """
    card_type = models.IntegerField(choices=CARD_TYPE)
    title = models.CharField(max_length=30)
    avatar = models.CharField(max_length=300)

    @classmethod
    def new_card_message(cls,

                         owner: User,
                         is_to_system: int,
                         content: str,
                         card_type: int,
                         title: str,
                         avatar: str):
        try:

            new_card_message = CardMessage(content=content, owner=owner,
                                           is_to_system=is_to_system, read_state=UNREAD,
                                           card_type=card_type, title=title, avatar=avatar)
            new_card_message.save()
            return new_card_message.id
        except Exception:
            return -1

    def generate_card(self):
        return {
            "cardType": CARD_TYPE[self.card_type][1],
            "title": self.title,
            "avatar": self.avatar,
            "info": self.content
        }
