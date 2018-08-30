import requests
import execjs
from bs4 import BeautifulSoup

'''
1、访问google翻译网站，获取js代码
2、通过js代码破解tkk的值
3、通过tkk的值和需要翻译词组算出tk的值
4、通过tk的值拼接url访问获得response
5、从response中解析出对于的翻译结果
'''

url = 'https://translate.google.cn'

# 获取html文本
def get_url_content():
    content = requests.get(url).content
    return content

# 通过script获取TKK值
def get_script_tkk():
    content = get_url_content()
    soup = BeautifulSoup(content, 'html.parser')
    for script in soup.find_all('script'):
        script_text = script.get_text()
        if script_text.find('TKK') > 0:
            # output_script('TKK' + script_text.split('TKK')[1].split(');')[0] + ');')
            tmp = str(script_text.split('TKK')[1].split(');')[0][7:-1]).replace('\\x3d', '=')  # 替代等号
            command = 'eval=' + tmp.replace('\\x27', '\'')    # 替代引号
            return execjs.eval(command)

def compile_js():
    f = open('./getTK.js', 'r')
    ctx = execjs.compile(f.read())
    f.close()
    return ctx

# 计算TKK值
tkk = get_script_tkk()
# 编译脚本
ctx = compile_js()

def get_englist(word):
    tk = ctx.call('tk', word, tkk)
    trans_url = 'https://translate.google.cn/translate_a/single?client=t&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt' \
                '=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=7&tk=' + tk + '&q=' + word
    r = requests.get(trans_url)
    print(r.content.decode('utf-8'))
