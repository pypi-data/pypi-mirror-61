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
import requests
import execjs
from urllib.parse import quote
from .config import *


class Google:
    def __init__(self):
        self.default_ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko' \
                          ') Chrome/55.0.2883.87 Safari/537.36'

    def get_tkk(self,host,proxies):
        self.headers = {'User-Agent': self.default_ua}
        res = requests.get(host, headers=self.headers, proxies=proxies)

        # version 2.1.0
        # RE_TKK = re.compile(r'''TKK=eval\(\'\(\(function\(\)\{(.+?)\}\)\(\)\)\'\);''')
        # code = RE_TKK.search(res.text).group(0).encode().decode('unicode-escape')
        # runjs = execjs.get()
        # tkk = runjs.eval(code[10:-3])

        # play a joke:
        runjs = execjs.get() # Avoid missing dependencies during installation.
        _ = runjs.eval('7+8')
        # joke done.

        # version 2.2.0
        tkk = re.findall("tkk:'(.*?)'",res.text)[0]
        return tkk

    # def rshift(self,val, n):
    #     """python port for '>>>'(right shift with padding)
    #     """
    #     return (val % 0x100000000) >> n


    def _xr(self, a, b):
        size_b = len(b)
        c = 0
        while c < size_b - 2:
            d = b[c + 2]
            d = ord(d[0]) - 87 if 'a' <= d else int(d)
            # d = google.rshift(self,a, d) if '+' == b[c + 1] else a << d
            d = (a % 0x100000000) >> d if '+' == b[c + 1] else a << d
            a = a + d & 4294967295 if '+' == b[c] else a ^ d
            c += 3
        return a


    def acquire(self, text, tkk):  # thanks "ssut".
        # tkk = google.get_tkk(self)
        b = tkk if tkk != '0' else ''
        d = b.split('.')
        b = int(d[0]) if len(d) > 1 else 0

        # assume e means char code array
        e = []
        g = 0
        size = len(text)
        for i, char in enumerate(text):
            l = ord(char)
            # just append if l is less than 128(ascii: DEL)
            if l < 128:
                e.append(l)
            # append calculated value if l is less than 2048
            else:
                if l < 2048:
                    e.append(l >> 6 | 192)
                else:
                    # append calculated value if l matches special condition
                    if (l & 64512) == 55296 and g + 1 < size and \
                                            ord(text[g + 1]) & 64512 == 56320:
                        g += 1
                        l = 65536 + ((l & 1023) << 10) + ord(text[g]) & 1023
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                        e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)
        a = b
        for i, value in enumerate(e):
            a += value
            a = self._xr(a, '+-a^+6')
        a = self._xr(a, '+-3^+b+-f')
        a ^= int(d[1]) if len(d) > 1 else 0
        if a < 0:  # pragma: nocover
            a = (a & 2147483647) + 2147483648
        a %= 1000000  # int(1E6)
        return '{}.{}'.format(a, a ^ b)


    def translate(self, text, TK, from_language,to_language,host,if_check_language,is_detail,proxies):
        from_language = 'zh-CN' if from_language in ('zh','zh-cn','zh-CN','zh-TW','zh-HK','zh-CHS') else from_language
        to_language = 'zh-CN' if to_language in ('zh','zh-cn','zh-CN','zh-TW','zh-HK','zh-CHS') else to_language
        if if_check_language:
            check_from_language = 'en' if from_language == 'auto' else from_language
            if (check_from_language not in LANGUAGES.keys()) or (to_language not in LANGUAGES.keys()):
                raise LanguageInputError(from_language, to_language)

        QQ = quote(text)
        url = (host + '/translate_a/single?client={0}&sl={1}&tl={2}&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md'
                + '&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=bh&ssel=0&tsel=0&kc=1&tk='
                + str(TK) + '&q=' + QQ).format('webapp',from_language,to_language)

        with requests.Session() as ss:
            r = ss.get(url, headers={'User-Agent': self.default_ua}, proxies=proxies) #client in (t,webapp)
            data = r.json()

        result = ''
        for dt in data[0]:
            if dt[0]:
                result += dt[0]

        return data if is_detail else result


class LanguageInputError(Exception):
    def __init__(self,from_language,to_language):
        Exception.__init__(self)
        self.from_language = from_language
        self.to_language = to_language
        print('LanguageInputError:  from_language[`{0}`] or to_language[`{1}`] is error, '
              'Please check dictionary of `LANGUAGES`!\n'.format(self.from_language, self.to_language))


class SizeInputError(Exception):
    def __init__(self,text):
        Exception.__init__(self)
        self.size = len(text)
        print('SizeInputError: The size[{}] of `text` is over `GOOGLE TRANSLATE LIMIT 5000`!'.format(self.size))


def google_api(text, from_language='auto',to_language='zh-CN',host='https://translate.google.cn',**kwargs):
    '''
    https://translate.google.com, https://translate.google.cn
    :param text: string
    :param from_language: string, default 'auto'.
    :param to_language: string, default 'zh'
    :param host: string,
    :param **kwargs:
            :param if_check_language: boolean, default True.
            :param is_detail: boolean, default False.
            :param proxies: dict, default None.
    :return:
    '''
    if_check_language = kwargs.get('if_check_language', True)
    is_detail = kwargs.get('is_detail', False)
    proxies = kwargs.get('proxies', None)
    
    text = str(text)
    if len(text) < 5000:
        api = Google()
        tkk = api.get_tkk(host,proxies)
        TK = api.acquire(text, tkk)
        result = api.translate(text, TK, from_language,to_language,host,if_check_language,is_detail,proxies)
        return result
    else:
        raise SizeInputError(text)


########################################################################################################################
###################################         _xr(),acquire() module js:       ###########################################
########################################################################################################################

# var b = function (a, b) {
# 	for (var d = 0; d < b.length - 2; d += 3) {
# 		var c = b.charAt(d + 2),
# 			c = "a" <= c ? c.charCodeAt(0) - 87 : Number(c),
# 			c = "+" == b.charAt(d + 1) ? a >>> c : a << c;
# 		a = "+" == b.charAt(d) ? a + c & 4294967295 : a ^ c
# 	}
# 	return a
# }
#
# var tk =  function (a,TKK) {
# 	//console.log(a,TKK);
# 	for (var e = TKK.split("."), h = Number(e[0]) || 0, g = [], d = 0, f = 0; f < a.length; f++) {
# 		var c = a.charCodeAt(f);
# 		128 > c ? g[d++] = c : (2048 > c ? g[d++] = c >> 6 | 192 : (55296 == (c & 64512) && f + 1 < a.length && 56320 == (a.charCodeAt(f + 1) & 64512) ? (c = 65536 + ((c & 1023) << 10) + (a.charCodeAt(++f) & 1023), g[d++] = c >> 18 | 240, g[d++] = c >> 12 & 63 | 128) : g[d++] = c >> 12 | 224, g[d++] = c >> 6 & 63 | 128), g[d++] = c & 63 | 128)
# 	}
# 	a = h;
# 	for (d = 0; d < g.length; d++) a += g[d], a = b(a, "+-a^+6");
# 	a = b(a, "+-3^+b+-f");
# 	a ^= Number(e[1]) || 0;
# 	0 > a && (a = (a & 2147483647) + 2147483648);
# 	a %= 1E6;
# 	return a.toString() + "." + (a ^ h)
