# coding=utf-8
# author=UlionTse

'''MIT License

Copyright (c) 2019 UlionTse

Warning: Prohibition of Commercial Use!
This module is designed to help students and individuals with translation services.
For commercial use, please purchase API services from translation suppliers.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. You may obtain a copy of the
License at

    https://github.com/uliontse/translators/blob/master/LICENSE

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import re
import time
import random
import requests


class Alibaba:
    def __init__(self):
        self.origin_url = 'https://translate.alibaba.com'
        self.api_url = 'https://translate.alibaba.com/translationopenseviceapp/trans/TranslateTextAddAlignment.do'
        self.check_url = 'https://translate.alibaba.com/trans/acquireSupportLanguage.do'
        self.origin_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, sdch, br",
            "accept-language": "zh-CN,zh;q=0.8,en;q=0.6",
            "dnt": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/55.0.2883.87 Safari/537.36"
        }
        self.api_headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.8,en;q=0.6",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": "https://translate.alibaba.com",
            "referer": "https://translate.alibaba.com",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/55.0.2883.87 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        

    def get_dmtrack_pageid(self,origin_res):
        try:
            e = re.findall("dmtrack_pageid='(\w+)';", origin_res.text)[0]
        except:
            e = ''
        if not e:
            e = origin_res.cookies.get_dict().get("cna","001")
            e = re.sub(pattern='[^a-z\d]',repl='',string=e.lower())[:16]
        else:
            n,r = e[0:16],e[16:26]
            i = hex(int(r,10))[2:] if re.match('^[\-+]?[0-9]+$',r) else r
            e = n + i
        
        s = int(time.time() * 1000)
        o = ''.join([e, hex(s)[2:]])
        for u in range(1,10):
            a = hex(int(random.random() * 1e10))[2:] # int->string: 16, '0x'
            o += a
        return o[:42]


    def check_language(self,from_language,to_language,session,biz_type,dmtrack_pageid,proxies=None):
        params = {'dmtrack_pageid': dmtrack_pageid, 'biz_type': biz_type}
        language_dict = session.get(self.check_url,params=params,headers=self.api_headers,proxies=proxies).json()

        from_language = 'en' if from_language == 'auto' else from_language
        if from_language in language_dict['sourceLanguage'] and to_language in language_dict['targetLanguage']:
            for lang_dict in language_dict['languageMap']:
                if from_language == lang_dict['sourceLuange'] and to_language in lang_dict['targetLanguages']: #sourceLuange
                    return True
            print('LanguageMap:',language_dict,sep='\n')
            return False
        else:
            print('LanguageMap:',language_dict,sep='\n')
            return False
            

    def alibaba_api(self,text,from_language='auto', to_language='zh', **kwargs):
        '''
        https://translate.alibaba.com/
        :param text: string
        :param from_language: string, default 'auto'.
        :param to_language: string, default 'zh'
        :param **kwargs:
            :param biz_type: string, default 'message', choose from ("general","message","offer")
            :param if_check_language: boolean, default True.
            :param is_detail: boolean, default False.
            :param proxies: dict, default None.
        :return:
        '''
        biz_type = kwargs.get('biz_type', 'message') #("general","message","offer")
        if_check_language = kwargs.get('if_check_language', True)
        is_detail = kwargs.get('is_detail', False)
        proxies = kwargs.get('proxies', None)
        
        from_language = 'zh' if from_language in ('zh','zh-cn','zh-CN','zh-TW','zh-HK','zh-CHS') else from_language
        to_language = 'zh' if to_language in ('zh','zh-cn','zh-CN','zh-TW','zh-HK','zh-CHS') else to_language
        form_data = {
            "srcLanguage": from_language,
            "tgtLanguage": to_language,
            "srcText": str(text),
            "viewType": "",
            "source": "",
            "bizType": biz_type #("general","message","offer")
        }
        ss = requests.Session()
        origin_res = ss.get(self.origin_url, headers=self.origin_headers, proxies=proxies)
        dmtrack_pageid = self.get_dmtrack_pageid(origin_res)
        
        if if_check_language:
            check_result = self.check_language(from_language,to_language,ss,biz_type,dmtrack_pageid,proxies)
            if not check_result:
                raise ValueError('from_language[{}] or to_language[{}] is not supported!'.format(from_language,to_language))
        
        i,data,ts_result = 0,{},[]
        while not ts_result and i<3:
            res = ss.post(self.api_url, data=form_data, params={"dmtrack_pageid": dmtrack_pageid}, proxies=proxies)
            data = res.json()
            ts_result = data.get('listTargetText')
            i += 1
        ss.close()
        return data if is_detail else ts_result[0]
        

ali = Alibaba()
alibaba_api = ali.alibaba_api
    