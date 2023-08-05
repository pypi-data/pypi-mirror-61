import json
import base64
from datetime import datetime
import hmac
from hashlib import sha256
from hashlib import md5
from urllib.parse import unquote, urlparse
import requests


class Client(object):
    """http签名方式的函数计算服务请求客户端"""
    def __init__(self, server, func, account_id, accesskey_id, accesskey_secret):
        self.AccountID = account_id
        self.AccessKeyID = accesskey_id
        self.AccessKeySecret = accesskey_secret
        self.server = server
        self.func = func
        self.domain = 'https://{}.cn-hangzhou.fc.aliyuncs.com'.format(self.AccountID)
        self.url = self.domain + '/2016-08-15/proxy/' + server + '/' + func + '/'


    @staticmethod
    def __get_conf(request_config):
        api_conf = {'http_conf': json.dumps(request_config)}
        return api_conf

    @staticmethod
    def __get_md5(content):
        md5.update(content.encode())
        result = md5.hexdigest()
        return result

    def __construct_headers(self, request_method, request_body='', query_dic=None):
        headers = {
            'Content-Type': 'application/json',
            'Host': '{}.cn-hangzhou.fc.aliyuncs.com'.format(self.AccountID),
            'Date': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
        }
        headers['Authorization'] = "FC " + str(self.AccessKeyID) + ":" + self.get_signature(
            headers, request_method, request_body, query_dic)
        return headers

    @staticmethod
    def __get_fc_headers(headers):
        li = []
        raw = {}
        fc_headers = ''
        for k, v in headers.items():
            if k.lower().startswith('x-fc-'):
                raw[k.lower()] = v
                li.append(k.lower())
        li.sort(key=lambda x: x[0])
        for l in li:
            fc_headers += str(l) + ':' + str(raw[l]) + '\n'
        return fc_headers

    def get_signature(self, headers, request_method, request_body='', request_query=None):
        canon_fc_headers = self.__get_fc_headers(headers)
        request_path = urlparse(unquote(self.url)).path

        md5_res = ''
        canon_fc_resource = request_path + '\n'

        params = []
        if request_query:
            for key, values in request_query.items():
                if isinstance(values, str):
                    params.append('%s=%s' % (key, values))
                    continue

                if len(values) > 0:
                    for value in values:
                        params.append('%s=%s' % (key, value))
                else:
                    params.append('%s' % key)

            params.sort()
            canon_fc_resource += '\n'.join(params)

        if request_body:
            md5_res = self.__get_md5(request_body)

        str_before_sign = request_method + "\n" + \
                          md5_res + "\n" + \
                          headers.get('Content-Type', 'application/json') + "\n" + \
                          headers.get('Date') + "\n" + \
                          canon_fc_headers + canon_fc_resource
        res = hmac.new(self.AccessKeySecret.encode('utf-8'),
                       str_before_sign.encode('utf-8'),
                       digestmod=sha256).digest()
        signature = base64.b64encode(res).decode('utf-8')
        return signature

    def get(self, spider_config):
        api_conf = self.__get_conf(spider_config)
        resp = requests.get(self.url,
                           headers=self.__construct_headers('GET', query_dic=api_conf),
                           params=api_conf)
        return resp

    def post(self, spider_config):
        api_conf = self.__get_conf(spider_config)
        resp = requests.post(self.url,
                            headers=self.__construct_headers('POST'),
                            data=api_conf)
        return resp
