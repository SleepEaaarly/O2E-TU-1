from core.models.user import User
from core.models.chat import Chatroom
from core.models.message import Message
from core.models.pap_model import PapModel
from core.models.interpretation import Interpretation
from core.models.notification import Notification

from django.contrib import admin
from core.models.enterprise_info import Enterprise_info
from core.models.need import Need
from core.models.order import Order
from core.models.papers import Papers
from core.models.projects import Projects
from core.models.patents import Patents
from core.models.expert import Expert
from core.models.rate import Rate
from django.contrib.auth.models import Group

# Register your models here.
# for test
admin.site.register([User])
admin.site.register([Enterprise_info])
admin.site.register([Need])
admin.site.register([Order])
admin.site.register([Papers])
admin.site.register([Projects])
admin.site.register([Patents])
admin.site.register([Expert])
#admin.site.register([Notification,PapModel,Notation,Interpretation,Updating])

#super user
#admin.site.register([User])
# admin_group = Group.objects.create(name='admin_group')
# admin_group.save()
# super_user_1 = User.objects.create_user(username='admin', password='888888', email='xiyue.su@qq.com', is_confirmed=True)
# super_user_1.save()
# admin_group.user_set.add(super_user_1)
#admin_group.permissions.add()
