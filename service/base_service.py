from service.api_service import WclApiService
from service.constant import CONSTANT_SERVICE
from base.models import WCLLog, Fight, Friendly, Enemy, LogDetail
from django.conf import settings
import json


class BaseService():
    def __init__(self):
        pass

    @classmethod
    def load_fight_data(cls, code):
        """
        加载日志，fight数据
        :param code:
        :return:
        """
        if len(WCLLog.objects.filter(code=code)) > 0:
            return False, '您的日志已登记，请勿重复登记'

        success, result = WclApiService.get_api(api=CONSTANT_SERVICE.FIGHT_API, code=code, view=None, params=None)
        if not success:
            return success, result

        wcl_log = WCLLog()
        wcl_log.title = result.get("title", "")
        wcl_log.code = code
        wcl_log.owner = result.get("owner", "")
        wcl_log.start = result.get("start", 0)
        wcl_log.end = result.get("end", 0)
        wcl_log.zone = result.get("zone", "")
        wcl_log.parse_flag = False
        wcl_log.save()

        fights = result.get('fights')
        if len(fights) > 0:
            for fight_data in fights:
                fight = Fight()
                fight.log = wcl_log
                fight.fight_id = fight_data.get("id", 0)
                fight.start = fight_data.get("start_time", 0)
                fight.end = fight_data.get("end_time", 0)
                fight.boss = fight_data.get("boss", 0)
                fight.kill = fight_data.get("kill", True)
                fight.name = fight_data.get("name", "")
                fight.save()

        friendlies = result.get('friendlies')
        if len(friendlies) > 0:
            for friendly_data in friendlies:
                friendly = Friendly()
                friendly.log = wcl_log
                friendly.name = friendly_data.get("name", "")
                friendly.friendly_id = friendly_data.get("id", 0)
                friendly.guid = friendly_data.get("guid", 0)
                friendly.type = friendly_data.get("type", "")
                friendly.server = friendly_data.get("server", "")
                friendly.save()

        enemies = result.get("enemies")
        if len(enemies) > 0:
            for enemy_data in enemies:
                enemy = Enemy()
                enemy.log = wcl_log
                enemy.name = enemy_data.get("name", "")
                enemy.enemy_id = enemy_data.get("id", 0)
                enemy.guid = enemy_data.get("guid", 0)
                enemy.type = enemy_data.get("type", "")
                enemy.save()

        return True, ''

    @classmethod
    def get_wcl_log_by_id(cls, log_id):
        '''
        根据log id获取日志对象
        :param log_id:
        :return:
        '''
        if not log_id or log_id == 0:
            return None, 'log id is none or 0'

        log_object = WCLLog.objects.filter(id=log_id)
        if not log_object:
            return None, 'wcl log not exist'

        return log_object.first(), ''

    @classmethod
    def get_wcl_log_by_code(cls, code):
        '''
        根据code获取日志对象
        :param code:
        :return:
        '''
        if not code or code == '':
            return None, 'code is none'

        log_object = WCLLog.objects.filter(code=code)
        if not log_object:
            return None, 'wcl log not exist'

        return log_object.first(), ''

    @classmethod
    def get_fight_list(cls, log_id, name):
        '''
        根据boss查找战斗列表
        :param log_id:
        :param name:
        :return:
        '''
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return None, msg
        if isinstance(name, list):
            fight_list = Fight.objects.filter(log=log_obj, name__in=name, boss__gt=0)
        else:
            fight_list = Fight.objects.filter(log=log_obj, name=name, boss__gt=0)
        return fight_list, ''

    @classmethod
    def get_friendly_by_id(cls, friendly_id, log_id):
        '''
        根据id查找友方目标
        :param friendly_id:
        :param log_id:
        :return:
        '''
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return None, msg

        friendly_obj = Friendly.objects.filter(friendly_id=friendly_id, log=log_obj).first()
        if not friendly_obj:
            print(friendly_id, log_obj.id)
            return None, 'friendly not exist'

        return friendly_obj, ''

    @classmethod
    def get_all_friendly_by_log(cls, log_id):
        '''
        查找一个日志中所有友方目标
        :param log_id:
        :return:
        '''
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return None, msg

        friendly_obj = Friendly.objects.filter(log=log_obj)
        return friendly_obj, ''

    @classmethod
    def get_log_detail_list_by_id(cls, log_id):
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return None, msg

        log_detail_list = list()
        for detail in settings.DETAIL_LIST:
            detail_type = detail[0]
            detail_name = detail[1]
            detail_scan_url = detail[2]
            detail_info_url = detail[3]
            scan_flag_dict = json.loads(log_obj.scan_flag)
            if detail_type in scan_flag_dict.keys():
                # if scan_flag_dict[detail_type] == 1:
                #     scan_flag = True
                # else:
                #     scan_flag = False
                scan_flag = scan_flag_dict[detail_type]
            else:
                scan_flag = 0
            log_detail = LogDetail(detail_type=detail_type,
                                   detail_name=detail_name,
                                   detail_scan_url='/service%s%s' % (detail_scan_url, str(log_id)),
                                   detail_info_url='/service%s%s' % (detail_info_url, str(log_id)),
                                   scan_flag=scan_flag)
            log_detail_list.append(log_detail)

        return log_detail_list, ''

    @classmethod
    def get_enemy_by_name(cls, log_id, name):
        '''
        根据name查找敌对目标
        :param log_id:
        :param name:
        :return:
        '''
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return None, msg

        enemy_obj = Enemy.objects.filter(log=log_obj, name=name).first()
        if not enemy_obj:
            return None, 'enemy: %s not exist' % name

        return enemy_obj, ''

    @classmethod
    def test_task_async(cls):
        from wcl_analysis.tasks import test_task
        print("begin to call task")
        test_task.apply_async(args=[], queue='wcl_analysis')
        # test_task.delay()
        print("end to call task")

    @classmethod
    def update_sync_flag(cls, log_id, task, flag):
        '''
        更新扫描任务处理状态
        :param log_id:
        :return:
        '''
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return False, msg

        scan_flag = json.loads(log_obj.scan_flag)
        scan_flag[task] = flag
        log_obj.scan_flag = json.dumps(scan_flag)
        log_obj.save()
        return True, ''
