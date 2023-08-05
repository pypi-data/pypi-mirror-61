# -*- coding:utf-8 -*-
import requests
from model.basic_request import BasicRequest

from grader.compatible import encode_str

__author__ = 'Feliciano'


class SingleDialogue(BasicRequest):

    DEFAULT_REPLY = u'我不知道。'
    ERROR_REPLY = u'服务器通信错误。'

    def __init__(self, service_config):
        super(SingleDialogue, self).__init__()

        server_config = service_config.get_config('server')

        self.protocol = server_config['protocol']
        self.host = server_config['host']
        self.port = server_config['port']
        self.endpoint = server_config['api']
        self.method = server_config.get('method', 'POST')

        request_config = service_config.get_config('request')

        self.payload = request_config['payload']
        self.threshold = request_config.get('threshold', None)
        self.answer_key = request_config.get('answer', 'reply')
        self.type = request_config.get('type', 'application/json')
        self.headers = request_config.get('headers', None)
        self.timeout = request_config.get('timeout', 5)

        self.url = self.to_uri()

        self.proxy = {'http': 'http://localhost:8888'}

    def chat(self, data):
        payload = encode_str(self.payload % data)

        if not self.headers:
            self.headers = {
                'content-type': self.type
            }
        else:
            self.headers['content-type'] = self.type

        r = None
        try:
            if self.method == 'GET':
                r = requests.get(self.url, params=payload, headers=self.headers, timeout=self.timeout, proxies=self.proxy)
            else:
                r = requests.post(self.url, data=payload, headers=self.headers, timeout=self.timeout, proxies=self.proxy)
            result = r.json()
        except Exception as e:
            self.logger.exception(e)
            self.logger.warning("Error process: " + (r and r.text or 'No response'))
            return SingleDialogue.ERROR_REPLY

        if not self.threshold:
            return result[self.answer_key]
        else:
            if 'probability' in result and result['probability'] > self.threshold:
                cut = result['reply'].find(' ( ')
                if cut > -1:
                    return result[self.answer_key][:cut]
                return result[self.answer_key]
        return SingleDialogue.DEFAULT_REPLY
  