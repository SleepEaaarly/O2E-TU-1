"""
Report message: 报告信息
"""
from django.db import models
from .user import User
from .system_message import SystemMessage

UNREAD = 0
READ = 1

READ_STATE_CHIOCES = (
    (0, 'Not read'),
    (1, 'Read'),
)


class ReportMessage(SystemMessage):
    WORK = 0
    NEED = 1
    ORDER = 2

    REPORT_TYPE = ['WORK', 'NEED', 'ORDER']
    """
    Field:
        - report_type: 报告类型 work/need/order
        - report_belong_id: 该报告信息对应的报告id
        - report_title: 需求名称/成果名称/订单报告的需求名称
        - report_name: 企业名称/专家名称
        - report_logo_path: 企业头像, 专家头像
        - 需求、成果简介由父类的content字段存储
        - 生成消息时间由父类的created_at存储
    """
    report_type = models.IntegerField()
    report_belong_id = models.IntegerField()
    report_title = models.CharField(max_length=300)
    report_name = models.CharField(max_length=300)
    report_logo_path = models.CharField(max_length=300)

    @classmethod
    def new_report_message(cls,
                           owner: User,
                           info: str,
                           report_type: int,
                           title: str,
                           name: str,
                           avatar: str,
                           involved_id: int
                           ):
        try:
            if(len(info)>1000):
                info = info[:1000]
            new_report_message = ReportMessage(content=info, owner=owner,
                                             is_to_system=0, read_state=UNREAD,
                                             report_type=report_type, report_belong_id=involved_id,
                                             report_title=title, report_name=name, report_logo_path=avatar,
                                             type='report')
            # print("report_message step1")
            new_report_message.save()
            # print("report_message step2")
            return new_report_message.id
        except Exception:
            return -1

    def generate_card(self):
        # print("enter report card generation")
        # print(self.report_type)
        # print(self.REPORT_TYPE[self.report_type])
        # print(self.report_belong_id)
        # print(self.report_title)
        # print(self.report_logo_path)
        # print(self.content)
        # print(self.created_at)
        return {
            "reportType": self.REPORT_TYPE[self.report_type],
            "reportId": self.report_belong_id,
            "reportTitle": self.report_title,
            "reportLogoPath": self.report_logo_path,
            "reportInfo": self.content,
            "time": self.created_at
        }
