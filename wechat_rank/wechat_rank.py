import random

import execjs
import re
import requests
from urllib.parse import urlencode, unquote


class WechatRank:

    def __init__(self):
        self.js_file = '/Users/chenzhuo/Desktop/Standford/21days_DL/spyder/wechat_rank/run.js'
        self.web_url_day = "https://www.newrank.cn/xdnphb/main/v1/day/rank"
        self.web_url_week = "https://www.newrank.cn/xdnphb/main/v1/week/rank"
        self.web_url_month = "https://www.newrank.cn/xdnphb/main/v1/month/rank"
        self.nonce = "".join(
            [["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"][random.randint(0, 15)] for
             _ in range(8)])
        # self.nonce = "2412cbffa"
        self.data = {
            "end": "2023-01-30",
            "rank_name": "文化",
            "rank_name_group": "生活",
            "start": "2023-01-30",
            "nonce": self.nonce
        }
        self.header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": "148",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "acw_tc=707c9fc716751728971261482e1e2e341e0ebb91244cb2e68f33f073c883b3",
            "Host": "www.newrank.cn",
            "Origin": "https://www.newrank.cn",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "macOS",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.xyz = self.get_xyz()
        print(self.xyz)
        # web
        # "86ec94ef8af04874a01175749509d43d"
        #  86ec94ef8af04874a01175749509d43d

        self.response = self.test()
        for d in self.response["value"]["datas"]:
            print(d)
        print("done")

    def test(self):
        self.data["xyz"] = self.xyz
        self.data["nonce"] = self.nonce
        data = self.data
        print(data)
        response = requests.post(self.web_url_day, headers=self.header, data=data).json()
        print(response)
        return response

    def get_xyz(self):
        with open(self.js_file, encoding='utf-8') as f:
            js_run = f.read()
        content = execjs.compile(js_run)


        # self.nonce = "c13cfad82"
        h = unquote("/xdnphb/main/v1/day/rank?AppKey=joker&" + urlencode(self.data))
        # h = '/xdnphb/main/v1/day/rank?AppKey=joker&end=2023-01-30&rank_name=文化&rank_name_group=生活&start=2023-01-30&nonce=2412cbffa'

        print(h)
        c = content.call("run", h)
        return c


if __name__ == '__main__':
    we = WechatRank()






# js_run = """
# function run(h) {
#     l_func = function () {
#         for (var a = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"], b = 0; b < 500; b++)
#             for (var c = "", d = 0; d < 9; d++) {
#                 var e = Math.floor(16 * Math.random());
#                 c += a[e]
#             }
#         return c
#     }
#
#     var nonce = l_func()
#     console.log(nonce)
#
#     function b(a) {
#         function b(a) {
#             return d(c(e(a)))
#         }
#
#         function c(a) {
#             return g(h(f(a), 8 * a.length))
#         }
#
#         function d(a) {
#             for (var b, c = p ? "0123456789ABCDEF" : "0123456789abcdef", d = "", e = 0; e < a.length; e++)
#                 b = a.charCodeAt(e),
#                     d += c.charAt(b >>> 4 & 15) + c.charAt(15 & b);
#             return d
#         }
#
#         function e(a) {
#             for (var b, c, d = "", e = -1; ++e < a.length;)
#                 b = a.charCodeAt(e),
#                     c = e + 1 < a.length ? a.charCodeAt(e + 1) : 0,
#                 55296 <= b && b <= 56319 && 56320 <= c && c <= 57343 && (b = 65536 + ((1023 & b) << 10) + (1023 & c),
#                     e++),
#                     b <= 127 ? d += String.fromCharCode(b) : b <= 2047 ? d += String.fromCharCode(192 | b >>> 6 & 31, 128 | 63 & b) : b <= 65535 ? d += String.fromCharCode(224 | b >>> 12 & 15, 128 | b >>> 6 & 63, 128 | 63 & b) : b <= 2097151 && (d += String.fromCharCode(240 | b >>> 18 & 7, 128 | b >>> 12 & 63, 128 | b >>> 6 & 63, 128 | 63 & b));
#             return d
#         }
#
#         function f(a) {
#             for (var b = Array(a.length >> 2), c = 0; c < b.length; c++)
#                 b[c] = 0;
#             for (var c = 0; c < 8 * a.length; c += 8)
#                 b[c >> 5] |= (255 & a.charCodeAt(c / 8)) << c % 32;
#             return b
#         }
#
#         function g(a) {
#             for (var b = "", c = 0; c < 32 * a.length; c += 8)
#                 b += String.fromCharCode(a[c >> 5] >>> c % 32 & 255);
#             return b
#         }
#
#         function h(a, b) {
#             a[b >> 5] |= 128 << b % 32,
#                 a[14 + (b + 64 >>> 9 << 4)] = b;
#             for (var c = 1732584193, d = -271733879, e = -1732584194, f = 271733878, g = 0; g < a.length; g += 16) {
#                 var h = c
#                     , i = d
#                     , o = e
#                     , p = f;
#                 c = j(c, d, e, f, a[g + 0], 7, -680876936),
#                     f = j(f, c, d, e, a[g + 1], 12, -389564586),
#                     e = j(e, f, c, d, a[g + 2], 17, 606105819),
#                     d = j(d, e, f, c, a[g + 3], 22, -1044525330),
#                     c = j(c, d, e, f, a[g + 4], 7, -176418897),
#                     f = j(f, c, d, e, a[g + 5], 12, 1200080426),
#                     e = j(e, f, c, d, a[g + 6], 17, -1473231341),
#                     d = j(d, e, f, c, a[g + 7], 22, -45705983),
#                     c = j(c, d, e, f, a[g + 8], 7, 1770035416),
#                     f = j(f, c, d, e, a[g + 9], 12, -1958414417),
#                     e = j(e, f, c, d, a[g + 10], 17, -42063),
#                     d = j(d, e, f, c, a[g + 11], 22, -1990404162),
#                     c = j(c, d, e, f, a[g + 12], 7, 1804603682),
#                     f = j(f, c, d, e, a[g + 13], 12, -40341101),
#                     e = j(e, f, c, d, a[g + 14], 17, -1502002290),
#                     d = j(d, e, f, c, a[g + 15], 22, 1236535329),
#                     c = k(c, d, e, f, a[g + 1], 5, -165796510),
#                     f = k(f, c, d, e, a[g + 6], 9, -1069501632),
#                     e = k(e, f, c, d, a[g + 11], 14, 643717713),
#                     d = k(d, e, f, c, a[g + 0], 20, -373897302),
#                     c = k(c, d, e, f, a[g + 5], 5, -701558691),
#                     f = k(f, c, d, e, a[g + 10], 9, 38016083),
#                     e = k(e, f, c, d, a[g + 15], 14, -660478335),
#                     d = k(d, e, f, c, a[g + 4], 20, -405537848),
#                     c = k(c, d, e, f, a[g + 9], 5, 568446438),
#                     f = k(f, c, d, e, a[g + 14], 9, -1019803690),
#                     e = k(e, f, c, d, a[g + 3], 14, -187363961),
#                     d = k(d, e, f, c, a[g + 8], 20, 1163531501),
#                     c = k(c, d, e, f, a[g + 13], 5, -1444681467),
#                     f = k(f, c, d, e, a[g + 2], 9, -51403784),
#                     e = k(e, f, c, d, a[g + 7], 14, 1735328473),
#                     d = k(d, e, f, c, a[g + 12], 20, -1926607734),
#                     c = l(c, d, e, f, a[g + 5], 4, -378558),
#                     f = l(f, c, d, e, a[g + 8], 11, -2022574463),
#                     e = l(e, f, c, d, a[g + 11], 16, 1839030562),
#                     d = l(d, e, f, c, a[g + 14], 23, -35309556),
#                     c = l(c, d, e, f, a[g + 1], 4, -1530992060),
#                     f = l(f, c, d, e, a[g + 4], 11, 1272893353),
#                     e = l(e, f, c, d, a[g + 7], 16, -155497632),
#                     d = l(d, e, f, c, a[g + 10], 23, -1094730640),
#                     c = l(c, d, e, f, a[g + 13], 4, 681279174),
#                     f = l(f, c, d, e, a[g + 0], 11, -358537222),
#                     e = l(e, f, c, d, a[g + 3], 16, -722521979),
#                     d = l(d, e, f, c, a[g + 6], 23, 76029189),
#                     c = l(c, d, e, f, a[g + 9], 4, -640364487),
#                     f = l(f, c, d, e, a[g + 12], 11, -421815835),
#                     e = l(e, f, c, d, a[g + 15], 16, 530742520),
#                     d = l(d, e, f, c, a[g + 2], 23, -995338651),
#                     c = m(c, d, e, f, a[g + 0], 6, -198630844),
#                     f = m(f, c, d, e, a[g + 7], 10, 1126891415),
#                     e = m(e, f, c, d, a[g + 14], 15, -1416354905),
#                     d = m(d, e, f, c, a[g + 5], 21, -57434055),
#                     c = m(c, d, e, f, a[g + 12], 6, 1700485571),
#                     f = m(f, c, d, e, a[g + 3], 10, -1894986606),
#                     e = m(e, f, c, d, a[g + 10], 15, -1051523),
#                     d = m(d, e, f, c, a[g + 1], 21, -2054922799),
#                     c = m(c, d, e, f, a[g + 8], 6, 1873313359),
#                     f = m(f, c, d, e, a[g + 15], 10, -30611744),
#                     e = m(e, f, c, d, a[g + 6], 15, -1560198380),
#                     d = m(d, e, f, c, a[g + 13], 21, 1309151649),
#                     c = m(c, d, e, f, a[g + 4], 6, -145523070),
#                     f = m(f, c, d, e, a[g + 11], 10, -1120210379),
#                     e = m(e, f, c, d, a[g + 2], 15, 718787259),
#                     d = m(d, e, f, c, a[g + 9], 21, -343485551),
#                     c = n(c, h),
#                     d = n(d, i),
#                     e = n(e, o),
#                     f = n(f, p)
#             }
#             return Array(c, d, e, f)
#         }
#
#         function i(a, b, c, d, e, f) {
#             return n(o(n(n(b, a), n(d, f)), e), c)
#         }
#
#         function j(a, b, c, d, e, f, g) {
#             return i(b & c | ~b & d, a, b, e, f, g)
#         }
#
#         function k(a, b, c, d, e, f, g) {
#             return i(b & d | c & ~d, a, b, e, f, g)
#         }
#
#         function l(a, b, c, d, e, f, g) {
#             return i(b ^ c ^ d, a, b, e, f, g)
#         }
#
#         function m(a, b, c, d, e, f, g) {
#             return i(c ^ (b | ~d), a, b, e, f, g)
#         }
#
#         function n(a, b) {
#             var c = (65535 & a) + (65535 & b);
#             return (a >> 16) + (b >> 16) + (c >> 16) << 16 | 65535 & c
#         }
#
#         function o(a, b) {
#             return a << b | a >>> 32 - b
#         }
#
#         var p = 0;
#         return b(a)
#     }
#
#     h += nonce
#     var xyz = b(h)
#     console.log(xyz)
#     return { "nonce" : nonce,
#             "xyz" : xyz,
#             }
# }
# """