from os import environ
from typing import NoReturn, Optional
import json
import time
import requests
from util import logger, notify, github

log = logger.get_logger()


class SignIn:
    """
    签到
    """

    def __init__(
            self,
            refresh_token: str
    ):
        """
        初始化

        :param refresh_token: refresh_token
        """
        self.refresh_token = refresh_token
        self.hide_refresh_token = self.__hide_refresh_token()
        self.access_token = None
        self.new_refresh_token = None
        self.phone = None
        self.signin_count = 0
        self.signin_reward = None
        self.error = None

    def __hide_refresh_token(self) -> str:
        """
        隐藏 refresh_token

        :return: 隐藏后的 refresh_token
        """
        try:
            return self.refresh_token[:4] + '*' * len(self.refresh_token[4:-4]) + self.refresh_token[-4:]
        except IndexError:
            return self.refresh_token

    def __get_access_token(self, retry: bool = False) -> bool:
        """
        获取 access_token

        :param retry: 是否重试
        :return: 是否成功
        """
        try:
            data = requests.post(
                'https://auth.aliyundrive.com/v2/account/token',
                json={
                    'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_token,
                }
            ).json()
        except requests.RequestException as e:
            log.error(f'[{self.hide_refresh_token}] 获取 access token 请求失败: {e}')
            if not retry:
                log.info(f'[{self.hide_refresh_token}] 正在重试...')
                return self.__get_access_token(retry=True)

            self.error = e
            return False

        try:
            if data['code'] in [
                'RefreshTokenExpired', 'InvalidParameter.RefreshToken',
            ]:
                log.error(f'[{self.hide_refresh_token}] 获取 access token 失败, 可能是 refresh token 无效.')
                self.error = data
                return False
        except KeyError:
            pass

        try:
            self.access_token = data['access_token']
            self.new_refresh_token = data['refresh_token']
            self.phone = data['user_name']
        except KeyError:
            log.error(f'[{self.hide_refresh_token}] 获取 access token 失败, 参数缺失: {data}')
            self.error = f'获取 access token 失败, 参数缺失: {data}'
            return False

        return True

    def __sign_in(self, retry: bool = False) -> NoReturn:
        """
        签到函数

        :return:
        """
        try:
            data = requests.post(
                'https://member.aliyundrive.com/v1/activity/sign_in_list',
                params={'_rx-s': 'mobile'},
                headers={'Authorization': f'Bearer {self.access_token}'},
                json={'isReward': False},
            ).json()
            log.debug(str(data))
        except requests.RequestException as e:
            log.error(f'[{self.phone}] 签到请求失败: {e}')
            if not retry:
                log.info(f'[{self.phone}] 正在重试...')
                return self.__sign_in(retry=True)

            self.error = e
            return

        if data['code'] == 'AccessTokenInvalid':
            log.error(f'[{self.phone}] access token 无效, 正在重新获取...')
            if not retry:
                log.info(f'[{self.phone}] 签到失败, 正在重试...')
                return self.__sign_in(retry=True)

        if 'success' not in data:
            log.error(f'[{self.phone}] 签到失败, 错误信息: {data}')
            self.error = data
            return

        self.signin_count = data['result']['signInCount']

        try:
            data = requests.post(
                'https://member.aliyundrive.com/v1/activity/sign_in_reward',
                params={'_rx-s': 'mobile'},
                headers={'Authorization': f'Bearer {self.access_token}'},
                json={'signInDay': self.signin_count},
            ).json()
            log.debug(str(data))
        except requests.RequestException as e:
            log.error(f'[{self.phone}] 兑换请求失败: {e}')
            if not retry:
                log.info(f'[{self.phone}] 正在重试...')
                return self.__sign_in(retry=True)

        reward = (
            '无奖励'
            if not data['result']
            else f'获得 {data["result"]["name"]} {data["result"]["description"]}'
        )

        self.signin_reward = reward

        log.info(f'[{self.phone}] 签到成功, 本月累计签到 {self.signin_count} 天.')
        log.info(f'[{self.phone}] 本次签到{reward}')

    def __reward_all(self, max_day: int) -> NoReturn:
        """
        兑换当月全部奖励

        :param max_day: 最大天数
        :return:
        """
        url = 'https://member.aliyundrive.com/v1/activity/sign_in_reward'
        params = {'_rx-s': 'mobile'}
        headers = {'Authorization': f'Bearer {self.access_token}'}

        for day in range(1, max_day + 1):
            try:
                requests.post(
                    url,
                    params=params,
                    headers=headers,
                    json={'signInDay': day},
                )
            except requests.RequestException as e:
                log.error(f'[{self.phone}] 签到请求失败: {e}')

        self.signin_reward = '已自动领取本月全部奖励'

    def __generate_result(self) -> dict:
        """
        获取签到结果

        :return: 签到结果
        """
        user = self.phone or self.hide_refresh_token
        text = (
            f'[{user}] 签到成功, 本月累计签到 {self.signin_count} 天.本次签到{self.signin_reward}'
            if not self.error
            else f'[{user}] 签到失败\n{json.dumps(str(self.error), indent=2, ensure_ascii=False)}'
        )

        text_html = (
            f'<code>{user}</code> 签到成功, 本月累计签到 {self.signin_count} 天.\n本次签到{self.signin_reward}'
            if not self.error
            else (
                f'<code>{user}</code> 签到失败\n'
                f'<code>{json.dumps(str(self.error), indent=2, ensure_ascii=False)}</code>'
            )
        )

        return {
            'success': True if self.signin_count else False,
            'user': self.phone or self.hide_refresh_token,
            'refresh_token': self.new_refresh_token or self.refresh_token,
            'count': self.signin_count,
            'reward': self.signin_reward,
            'text': text,
            'text_html': text_html,
        }

    def run(self) -> dict:
        """
        运行签到

        :return: 签到结果
        """
        result = self.__get_access_token()

        if result:
            time.sleep(3)
            self.__sign_in()

        return self.__generate_result()


def main():
    refresh_token = environ['ALIYUN_REFRESH_TOKEN']

    signin = SignIn(refresh_token=refresh_token)

    result = signin.run()

    # 合并推送
    text = result['text']

    log.info('阿里云签到结果：' + text)
    if not result['success']:
        notify.send_notify('阿里云签到失败', text)

    # 更新 refresh token
    new_refresh_token = result['refresh_token']
    try:
        github.update_secret('ALIYUN_REFRESH_TOKEN', new_refresh_token)
        log.info('ALIYUN_REFRESH_TOKEN 更新成功.')
    except Exception as e:
        log.error(f'Action 更新 Github Secrets: ALIYUN_REFRESH_TOKEN 失败: {e}')


if __name__ == '__main__':
    main()
