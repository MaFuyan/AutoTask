#!/usr/bin/env python
# -*- encoding=utf8 -*-
import datetime
import json

import requests

from exception import AsstException


class Messenger(object):
    """消息推送类"""

    def __init__(self, sc_key):
        if not sc_key:
            raise AsstException('sc_key can not be empty')

        self.sc_key = sc_key

    def send(self, text, desp=''):
        if not text.strip():
            print('Text of message is empty!')
            return

        now_time = str(datetime.datetime.now())
        desp = '[{0}]'.format(now_time) if not desp else '{0} [{1}]'.format(desp, now_time)

        try:
            resp = requests.get(
                'https://sctapi.ftqq.com/{}.send?title={}&desp={}'.format(self.sc_key, text, desp)
            )
            resp_json = json.loads(resp.text)
            if resp_json['data'].get('errno') == 0:
                print('Message sent successfully [text: %s, desp: %s]', text, desp)
            else:
                print('Fail to send message, reason: %s', resp.text)
        except requests.exceptions.RequestException as req_error:
            print('Request error: %s', req_error)
        except Exception as e:
            print('Fail to send message [text: %s, desp: %s]: %s', text, desp, e)
