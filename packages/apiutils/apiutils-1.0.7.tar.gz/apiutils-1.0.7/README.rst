#######################
ApiUtils
#######################

.. image:: https://travis-ci.org/007gzs/apiutils.svg?branch=master
       :target: https://travis-ci.org/007gzs/apiutils
.. image:: https://img.shields.io/pypi/v/apiutils.svg
       :target: https://pypi.org/project/apiutils

CONSTANCE 配置::

    CONSTANCE_CONFIG = OrderedDict((
        ('SL_CPROFILE_LOG', (False, '请求函数耗时统计')),
        ('SL_CPROFILE_LOG_MIN_SECONDS', (10, '函数耗时LOG最小时间')),
        ('SL_CPROFILE_LOG_SKIP_PATH', ("", '请求函数耗时统计排除URL')),
        ('SL_CPROFILE_LOG_WHITE_PATH', ("", '关闭函数耗时统计时仍然统计的URL')),
        ('SL_LONG_TIME_MAIL_MIN_SECONDS', (20, '函数耗时mail最小时间')),
        ('SL_LONG_TIME_COUNT_MIN_SECONDS', (10, '函数耗时记录到长时间统计')),

        'VERIFY_CODE_MOBILE_COUNT': (10, '每个手机号每天可发送次数'),
        'VERIFY_CODE_WHITE_LIST_MOBILES': ('13800138000', '白名单手机号(逗号隔开)'),
        'VERIFY_CODE_WHITE_LIST_CODE': ('6379', '白名单验证码'),
        'VERIFY_CODE_SEND_EXPIRE_SECONDS': (60, '验证码发送限制秒数, 成功发送验证码后再次请求将在该时间过后才会重新发送'),
        'VERIFY_CODE_EXPIRE_SECONDS': (1800, '验证码默认过期秒数'),
        'VERIFY_CODE_MAX_TIMES': (10, '验证码可验证次数, 达到验证码次数后重新发送才能继续验证'),
        'VERIFY_CODE_SMS_CONTENT': ('直接发送短信以验证手机号，半小时内发送有效', '验证码上行说明文字'),
    ))

settings配置::

    
    def async_call(func, *args, **kwargs):
        return func(*args, **kwargs)

    SERVER_IP
    SMS_ACCESS_KEY_ID = '阿里短信key'
    SMS_ACCESS_KEY_SECRET = '阿里短信secret'
    SMS_SIGNNAME_VCODE = '验证码短信签名'
    SMS_TEMPLATE_VCODE = '验证码短信模板id'
    SMS_TEMPLATE_VCODE_PARAM = '验证码短信模板参数明'
