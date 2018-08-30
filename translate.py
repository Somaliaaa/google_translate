from google_translate import getGoogleJs

words = ['发布', '运维', '启动', '元配置', '作业测试', '作业研发']

for word in words:
    getGoogleJs.get_englist(word)
