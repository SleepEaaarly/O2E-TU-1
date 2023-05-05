from django.db import models
from .papers import Papers
from .patents import Patents
from .projects import Projects
from .results import Results


class Expert(models.Model):
    create_time = models.DateTimeField(auto_now=True, null=True)
    #知兔平台唯一的学者号
    scholarID = models.CharField(max_length=200, blank=True, null=True)
    #学者姓名
    name = models.CharField(max_length=100, blank=True, null=True)
    #学者身份证号,管理端添加
    ID_num = models.CharField(max_length=20, blank=True, null=True)
    #工作单位
    organization = models.CharField(max_length=100, blank=True, null=True)
    #擅长领域
    field = models.CharField(max_length=100, blank=True, null=True)
    #自我介绍
    #self_profile = models.CharField(max_length=200, blank=True, null=True)
    self_profile = models.TextField(blank=True, null=True)
    #身份证照片
    ID_pic = models.ImageField(upload_to="images/%Y%m/%d/icons",
                                         default='images/default_user_icon.jpg')
    #学者官网
    url = models.CharField(max_length=100, blank=True, null=True)
    #学者电话
    phone = models.CharField(max_length=15, blank=True, null=True)
    #专利
    patent = models.CharField(max_length=2000, blank=True, null=True)
    #论文
    paper = models.CharField(max_length=2000, blank=True, null=True)
    #所有论文
    papers = models.ManyToManyField(to=Papers, related_name="expert_papers")
    #所有专利
    patents = models.ManyToManyField(to=Patents, related_name="expert_patents")
    #所有项目
    projects = models.ManyToManyField(to=Projects, related_name="expert_projects")
    #所有成果
    results = models.ManyToManyField(to=Results, related_name="expert_results")
    #称号
    title = models.CharField(max_length=300, blank=True, null=True)
    # hitBert编码的向量对应的milvus id
    vector_hit = models.TextField(blank=True, null=True)