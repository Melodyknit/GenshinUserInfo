import sys
import string
import random
import hashlib
from time import time
from json import loads
from requests import get


class GenShinInfoAPI:
    mhyVersion = "2.1.0"

    @staticmethod
    def serverType(uid: str):
        if uid == '1':
            return "cn_gf01"
        elif uid == '5':
            return "cn_qd01"

    @classmethod
    def getInfo(cls, uid: str):
        try:
            sid = cls.serverType(uid[0])
            if not sid: raise Exception("UID输入有误！！\r\n请检查UID是否为国服UID！")
            uid = get(
                url=f"https://api-takumi.mihoyo.com/game_record/genshin/api/index?server={sid}&role_id={uid}",
                headers={'Accept': 'application/json, text/plain, */*',
                         'DS': cls.DSGet(),
                         'Origin': 'https://webstatic.mihoyo.com',
                         'x-rpc-app_version': '2.1.0',
                         'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
                         'x-rpc-client_type': '4',
                         'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
                         'Accept-Encoding': 'gzip, deflate',
                         'Accept-Language': 'zh-CN,en-US;q=0.8',
                         'X-Requested-With': 'com.mihoyo.hyperion'})
            msg = loads(uid.text)
            if msg['retcode'] != 0: raise Exception(f"调用错误\n请查看是否是输入有误或没有该UID\nMessage: {msg}")
            return msg['data']
        except Exception as e:
            print(f'\033[1;31m错误异常:{e}')
            print("访问失败，请重试！")
            sys.exit(1)

    @staticmethod
    def md5(text):
        md5 = hashlib.md5()
        md5.update(text.encode())
        return md5.hexdigest()

    @classmethod
    def DSGet(cls):
        n = cls.md5(cls.mhyVersion)
        i = str(int(time() - 30000))
        r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
        c = cls.md5(f"salt={n}&t={i}&r={r}")
        return f"{i},{r},{c}"


class Analysis(GenShinInfoAPI):
    @staticmethod
    def avatars(msg: list):
        print(f'   ==> 持有角色数量: {len(msg)} <==')
        for m in msg:
            print(f"|{m['name']} => {m['rarity']} ★角色:\n|等级: {m['level']} | 好感度: {m['fetter']}\n|{'-'*24}|")

    @staticmethod
    def cityExplorations(msg: list):
        print(f'   ==>  地图探索详细  <==')
        for m in msg:
            print(f"|{m['name']} {m['level']}\n|探索进度:{m['exploration_percentage']/10}%\n|{'-'*24}|")

    @staticmethod
    def stats(msg: dict):
        print('   ==>    其他状态    <==')
        print(f"|已完成成就数: {msg['achievement_number']}个\n"
              f"|日常活跃天数: {msg['active_day_number']}天\n"
              f"|风神瞳已收集: {msg['anemoculus_number']}枚\n"
              f"|岩神瞳已收集: {msg['geoculus_number']}枚\n"
              f"|传送锚点解锁: {msg['way_point_number']}处\n"
              f"|秘境锚点解锁: {msg['domain_number']}处\n"
              f"|深境螺旋层数: {msg['spiral_abyss']}层\n"
              f"|普通宝箱开启: {msg['common_chest_number']}箱\n"
              f"|精致宝箱开启: {msg['exquisite_chest_number']}箱\n"
              f"|珍贵宝箱开启: {msg['precious_chest_number']}箱\n"
              f"|华丽宝箱开启: {msg['luxurious_chest_number']}箱\n"
              f"|{'-'*24}|")

    @classmethod
    def get(cls, uid: str):
        msg = cls.getInfo(uid)
        cls.avatars(msg['avatars'])
        cls.cityExplorations(msg['city_explorations'])
        cls.stats(msg['stats'])


if __name__ == '__main__':
    while True:
        Analysis.get(input('>>> '))
