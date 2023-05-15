"""
 User
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from .enterprise_info import Enterprise_info
from django.core.validators import validate_comma_separated_integer_list
from django.db.models.signals import pre_delete
from django.dispatch import receiver


USER_TYPE_CHOICES = (
    (0, 'Individual'),
    (1, 'College'),
    (2, 'Company'),
)

#用户状态
USER_STATE_CHOICES = (
    (0, '普通用户'),
    (1, '专家认证中'),
    (2, '企业认证中'),
    (3, '封禁中'),
    (4, '认证专家'),
    (5, '认证企业')
)

STATE_LIST = ['普通用户', '专家认证中', '企业认证中', '封禁中', '认证专家', '认证企业']

BASE_DIR = 'http://127.0.0.1:8000/api/'


def decode_user_state(state):
    return STATE_LIST[state]


def decode_user_state(state):
    return STATE_LIST[state]


class User(AbstractUser):
    """
    Field:
        - nick_name
        - email
        - institution
        - user_type: individual, college, company
        - follows:
        - followers:
        - icon:
        - favorites:
        - is_confirmed: if the email address is passed or not
    """

    nick_name = models.CharField(max_length=20)

    email = models.CharField(max_length=30)
    institution = models.CharField(max_length=20, blank=True, null=True)
    icon = models.ImageField(upload_to="images/%Y%m/%d/icons",
                             default='images/default_user_icon.jpg')

    biogrpahy = models.CharField(max_length=50, null=True, blank=True)

    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=0)
    followers = models.ManyToManyField('User', null=True, blank=True)
    favorites = models.ManyToManyField('PapModel', related_name='favorites', null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    #用户目前状态
    state = models.IntegerField(choices=USER_STATE_CHOICES, default=0)

    enterprise_info = models.OneToOneField("Enterprise_info", on_delete=models.CASCADE, related_name="enterprise_info", null=True, blank=True)

    expert_info = models.OneToOneField("Expert", on_delete=models.CASCADE, related_name="expert_info", null=True, blank=True)

    class Meta(AbstractUser.Meta):
        default_permissions = ()
        #pass

    def get_icon(self):
        return str(self.icon)

    def to_dict(self):
        return {
            'username': self.username,
            'id': self.id,
            'email': self.email,
            'userpic': self.get_icon(),
            'institution': self.institution,
            'is_confirmed': self.is_confirmed,
            'state': decode_user_state(self.state),
        }
    
    def to_dict(self):
        return {
            'username': self.username,
            'id': self.id,
            'email': self.email,
            'userpic': self.get_icon(),
            'nickname': self.nick_name,
            'institution': self.institution,
            'is_confirmed': self.is_confirmed,
            'state': decode_user_state(self.state),
        }

    def is_followed(self, pid:int):
        return self.followers.filter(id=pid).exists()

    def get_fans(self):
        """
          follower: user的粉丝
          :return: 粉丝列表
          """
        return self.user_set.all()

    def get_followers(self):
        """
        follower: user关注的人
        :return: 关注的人列表
        """
        return self.followers.all()

    def follow_by_id(self, pid):
        """
        关注另外一个用户
        :param pid: 对方用户的id
        :return: 操作是否成功: boolean
        """
        if pid == self.id:
            return False
        try:
            p = User.objects.get(pk=pid)
            self.followers.add(p)
            self.save()
            return True
        except Exception:
            return False

    def unfollow_by_id(self, pid):
        """
        解除对另一个用户的关注
        :param pid: 对方用户的id
        :return: 操作是否成功: boolean
        """
        if pid == self.id:
            return False
        try:
            p = User.objects.get(pk=pid)
            self.followers.remove(p)
            self.save()
            return True
        except Exception:
            return False

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     return self.is_staff


@receiver(pre_delete, sender=User)
def icon_delete(instance):
    instance.icon.delete(False)


class ConfirmString(models.Model):
    """confirm string
    Field
        - code: check code
        - user: user
    """
    code = models.CharField(max_length=5)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.email + ":   " + self.code
