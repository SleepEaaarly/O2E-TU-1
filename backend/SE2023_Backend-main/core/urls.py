"""
define the url routes of core api
"""
from django.urls import path
from core.api.auth import obtain_jwt_token, refresh_jwt_token, obtain_jwt_token_admin
from core.api.chat import get_chat_list, delete_chat, message_read, create_chat, get_chat, push_message
from core.api.friend import list_friends, list_full_friends

from core.api.my_post import list_posts
from core.api.profile import get_profile
from core.api.search import search_user_list, search_user_full_list
from core.api.sign_up import change_password, change_email, CREATE_USER_API, FORGET_PASSWORD_API
from core.api.comment import create_comment, delete_comment, get_comment, get_comment_list

from core.api.user import follow, unfollow, list_favorite_recent, change_organization

from core.api.fan import list_fans, list_full_fans
from core.api.follower import list_followers, list_full_followers
from core.api.user_icon import USER_ICON_API, read_img, read_default_img
from core.api.notification import (NOTIFICATION_API, NOTIFICATION_SET_API)
from core.api.image import (IMAGE_API, IMAGE_SET_API)

from core.api.interpretation import createInterpretation, INTERPRETATION_API, \
    collectInterpretation, uncollectInterpretation, likeInterpretation, searchInterpretation, \
    transmitInterpretation, recommendInterpretation, downloadInterpretation, randomWalkInterpretation, \
    getAllInterpretation, queryVisitorNumber, queryKeywordTops, queryTagRatio

from core.api.user import get_all_user_info, delete_user, change_user_info

from core.api._platform.need_api import create_need, get_all_need, get_need_info, get_finished_need, \
    finish_need, get_proceeding_need, edit_need, delete_need, search_need, create_need_contact,\
    get_need_contact, expert_recommend, get_saved_need, transform_need, get_needs_info, get_oneneed_allexperts, admin_delete_need

from core.api._platform.order_api import get_pending_order, get_cooperating_order, get_finished_order, finish_order, accept_order, \
    refuse_order, get_order_info, create_order, get_order_id, get_all_order, abandon_order, get_order_byID, \
    admin_delete_order, admin_get_all_order, get_user_orderid_byneedID

from core.api.enterprise import set_info, agree_enterprise, refuse_enterprise, get_enterpriseInfo, get_all_enterprise

from core.api.expert import setinfo, agree_expert, refuse_expert, get_expertInfo, get_all_expert, get_json, add_papers, add_patents, add_projects, \
    get_expert_info, add_patents_scholars, add_papers_scholars, add_projects_scholars

from core.api.feedback import get_feedback, make_feedback, reply_feedback, get_user_unreplied_feedback, get_user_replied_feedback

from core.api.ai_recommend import recommend, need_recommend, result_recommend_for_expert, result_recommend_for_enterprise


from core.api._platform.rate import rate_order, get_order_rate, get_user_rate


from core.api.ai_chat import answer_set_question, answer_free_question


from core.tests.generate_avatar import avatar, get_user_num

from core.api.achievement import add_paper, add_patent, add_project, add_result, agree_result, refuse_result, get_resultInfo

from core.api.result_pic_pdf import RES_PIC_API, read_pic, read_default_pic, RES_PDF_API

from core.api.search_api import search_expert, search_enterprise, search_result, search_mixture

from core.api.system_chat import create_system_chat, get_system_chat, push_system_message, \
    system_message_read, alter_systemchat_visible, get_all_system_chatrooms, push_system_message_by_admin

from core.api.admin_entity import get_all_result_info, change_result_info, delete_result, search_result_by_name, \
    get_all_unaudited_result_info, search_user_by_name


from core.api.order_report import get_order_report

from core.api.ai_report import generate_requirement_report, generate_result_report, get_requirement_report, get_result_report

from core.api.ai_report import generate_requirement_report_card, generate_result_report_card

urlpatterns = [

    # user apis
    path('token-auth', obtain_jwt_token),
    path('token-auth/admin', obtain_jwt_token_admin),
    path('token-refresh', refresh_jwt_token),
    path('user/create', CREATE_USER_API),
    path('user/change-password', change_password),
    path('user/change-email', change_email),
    path('user/forget-password', FORGET_PASSWORD_API),
    path('user/profile', get_profile),
    path('user/icon', USER_ICON_API),
    path('user/<int:type>/all/<int:page>', get_all_user_info),
    path('user/delete', delete_user),
    path('user/changeinfo', change_user_info),

    # results
    path('res/pic', RES_PIC_API),
    path('images/<str:year>/<str:day>/res_pic/<str:file_name>', read_pic),
    path('images/default_result_pic.jpg', read_default_pic),
    path('res/pdf', RES_PDF_API),
    path('result/agree/<int:id>', agree_result),
    path('result/refuse/<int:id>', refuse_result),
    path('result/all/<int:page>', get_all_result_info),
    path('result/all/unaudited/<int:page>', get_all_unaudited_result_info),
    path('result/delete', delete_result),
    path('result/changeinfo', change_result_info),

    # comment apis
    path('comment/create', create_comment),
    path('comment/delete', delete_comment),
    path('comment/<int:id>', get_comment),
    path('comment', get_comment_list),

    # user apis
    path('user/<int:pid>/follow', follow),
    path('user/<int:pid>/unfollow', unfollow),
    path('user/organization', change_organization),
    # collection apis
    path('favorites/page/<int:pindex>', list_favorite_recent),


    # list posts - web PAGE
    path('post/<int:uid>', list_posts),

    # list fans - web PAGE
    path('fan/<int:uid>', list_fans),
    # list fans - app ROLL
    path('fan/roll/<int:uid>', list_full_fans),

    # list follower - web PAGE
    path('follower/<int:uid>', list_followers),
    # list follower - app ROLL
    path('follower/roll/<int:uid>', list_full_followers),


    # list friends - web PAGE
    path('friend/<int:uid>', list_friends),
    # list friends - app ROLL
    path('friend/roll/<int:uid>', list_full_friends),

    # notifications
    path('notification', NOTIFICATION_API),
    path('notification/page/<int:pindex>', NOTIFICATION_SET_API),

    # recommend related
    path('recommend', recommendInterpretation),
    path('Interpretation/popup', randomWalkInterpretation),

    # images
    path('image', IMAGE_API),
    path('image/page/<int:pindex>', IMAGE_SET_API),

    # chat
    path('chat/create', create_chat),
    path('chat/<int:id>', get_chat),
    path('chat/list', get_chat_list),
    path('chat/delete', delete_chat),
    path('chat/read', message_read),
    path('chat/push', push_message),

    # system chat
    path('system_chat/create',  create_system_chat),
    path('system_chat/get', get_system_chat),
    path('system_chat/push', push_system_message),
    path('system_chat/read', system_message_read),
    path('system_chat/show', alter_systemchat_visible),
    path('system_chat/getAll', get_all_system_chatrooms),
    path('system_chat/pushAdmin', push_system_message_by_admin),


    # search - web PAGE
    path('user/search/<int:uid>', search_user_list),
    # search - app ROLL
    path('user/search/roll', search_user_full_list),

    #    path('expert/search', search_expert),

    # interpretations
    path('Interpretation', createInterpretation),
    path('Interpretation/<int:id>', INTERPRETATION_API),
    path('Interpretation/<int:eid>/favor', collectInterpretation),
    path('Interpretation/<int:eid>/unfavor', uncollectInterpretation),
    path('Interpretation/<int:id>/like', likeInterpretation),
    path('Interpretation/page/<int:pid>', searchInterpretation),
    path('Interpretation/<int:id>/transmit', transmitInterpretation),
    path('Interpretation/getall', getAllInterpretation),
    path('Interpretation/getvis', queryVisitorNumber),
    path('Interpretation/getkeywords', queryKeywordTops),
    path('Interpretation/gettags', queryTagRatio),

    # image
    path('images/<str:year>/<str:day>/icons/<str:file_name>', read_img),
    path('images/default_user_icon.jpg', read_default_img),

    # downloads
    path('download/Interpretation/<int:id>', downloadInterpretation),

    # 为默认头像用户产生随机头像
    path('generateAvatar', avatar),

    # platform<---需求平台

    # need
    path('need', create_need),  # 发布新的需求
    path('need/all', get_all_need),  # 获取全部待解决需求
    path('need/<int:id>', get_need_info),  # 获取某个需求的信息
    path('user/<int:uid>/need/<int:id>/edit', edit_need),  # 修改需求
    path('user/<int:uid>/need/<int:id>/finish', finish_need),  # 企业结束需求
    path('user/<int:uid>/need/finished', get_finished_need),  # 获取某个企业正在进行的需求
    path('user/<int:uid>/need/proceeding', get_proceeding_need),  # 获取某个企业已结束的需求
    path('user/<int:uid>/need/saved', get_saved_need),  # 获取某个企业未发布的需求
    path('user/<int:uid>/need/<int:id>', delete_need),  # 企业删除需求
    path('user/<int:uid>/need/<int:id>/transform', transform_need),  # 企业将未发布需求发布
    path('need/search', search_need),               # 搜索需求
    path('need/contact', create_need_contact),      # 创建专家与企业的有关需求信息
    path('need/get_contact', get_need_contact),     # 根据专家与企业获取最近需求

    path('need/<int:id>/expert_recommend', expert_recommend),  # 基于需求的专家推荐
    path('need/getall', get_needs_info),  # 管理端获得全部需求
    # 获取需求已对接全部专家id与头像url
    path('need/<int:id>/allexperts', get_oneneed_allexperts),
    path('need/<int:id>/delete', admin_delete_need),  # 管理端删除需求

    # order
    path('order', create_order),  # 企业创建新订单
    path('order/<int:id>', get_order_info),  # 获取某个订单的信息
    path('user/<int:uid>/order/<int:id>/refuse', refuse_order),  # 专家拒绝订单
    path('user/<int:uid>/order/<int:id>/accept', accept_order),  # 专家接受订单
    path('user/<int:uid>/order/<int:id>/finish', finish_order),  # 企业结束订单
    path('user/<int:uid>/order/<int:id>/abandon', abandon_order),  # 企业放弃在合作的订单
    # 获取某个用户（企业或专家）已完成订单（拒绝和结束）
    path('user/<int:uid>/order/finished', get_finished_order),
    path('user/<int:uid>/order/pending',
         get_pending_order),  # 获取某个用户（企业或专家）新请求的订单
    path('user/<int:uid>/order/cooperating',
         get_cooperating_order),  # 获取某个用户（企业或专家）正在合作的订单
    path('user/<int:uid>/order/all', get_all_order),  # 获取用户全部订单，按state排序
    path('order/get', get_order_id),          # 根据专家、企业、需求获取对于订单
    path('order/byneed/<int:id>', get_order_byID),

    path('need/<int:id>/order', get_user_orderid_byneedID),  # 根据需求获取拒绝之外的订单

    path('admin/order/getall', admin_get_all_order),
    path('admin/order/<int:id>', admin_delete_order),

    # enterprise
    path('enterprise/setinfo', set_info),  # 企业设置认证信息，进行认证
    path('enterprise/getinfo/<int:id>', get_enterpriseInfo),  # 管理端获取企业认证信息
    path('enterprise/agree/<int:id>', agree_enterprise),  # 接受企业认证
    path('enterprise/refuse/<int:id>', refuse_enterprise),  # 拒绝企业认证
    path('enterprise/getall', get_all_enterprise),  # 获取待认证的企业

    # expert
    path('expert/setinfo', setinfo),  # 专家设置信息，进行专家认证
    path('expert/getinfo/<int:id>', get_expertInfo),  # 管理端获取专家认证信息
    path('expert/agree/<int:id>', agree_expert),  # 接受专家认证
    path('expert/refuse/<int:id>', refuse_expert),  # 拒绝专家认证
    path('expert/getall', get_all_expert),  # 获取待认证的专家
    # 获取专家信息，通过 ?tab = project, paper, patent等获取信息
    path('expert/<int:uid>', get_expert_info),

    # Feedback
    path('feedback/getall', get_feedback),
    path('user/feedback', make_feedback),

    path('feedback/reply', reply_feedback),

    path('user/<int:id>/feedback/replied', get_user_replied_feedback),
    path('user/<int:id>/feedback/unreplied', get_user_unreplied_feedback),

    # AI推荐
    path('ai/recommend/<int:id>', recommend),
    path('ai/needRecommend/<int:id>', need_recommend),
    path('ai/resultRec/expert/<int:id>', result_recommend_for_expert),
    path('ai/resultRec/enterprise/<int:id>', result_recommend_for_enterprise),
    
    # # AI客服
    path('answer/set', answer_set_question),
    path('answer/free', answer_free_question),

    # 评价
    path('order/rate', rate_order),
    path('order/<int:id>/rate', get_order_rate),
    path('user/<int:id>/rate', get_user_rate),

    # 管理端获取用户数
    path('user/all', get_user_num),

    # 成果发布
    path('paper/add', add_paper),
    path('patent/add', add_patent),
    path('project/add', add_project),
    path('result/add', add_result),

    # search
    path('result/getinfo/<int:id>', get_resultInfo),
    path('search/expert', search_expert),
    path('search/enterprise', search_enterprise),
    path('search/result', search_result),
    path('search/mixture', search_mixture),

    # 管理端search
    path('admin/search/result', search_result_by_name),
    path('admin/search/user', search_user_by_name),

    # 获得订单报告
    path('order_report/get', get_order_report),

    # 专家企业互释报告

    path('work_report/get', get_result_report),

    path("need_report/get", get_requirement_report),

    path("work_report/generateCard", generate_result_report_card),
    
    path("need_report/generateCard", generate_requirement_report_card),
    
]
