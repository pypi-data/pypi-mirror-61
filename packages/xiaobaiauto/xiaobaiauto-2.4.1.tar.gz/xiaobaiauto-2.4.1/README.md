# xiaobaiauto

## 介绍
简化现有Selenium、Requests等框架对于页面及接口的操作，也扩展了日志搜集、报告生成、
邮件发送等功能

### 版本说明
    版本：   功能：                        实现：
    1.*     只支持Web端                    √
    2.*     支持Web+API端                  √
    3.*     支持Web+API+Mock               ×
    4.*     支持Web+API+Mock+APP           ×
    5.*     支持Web+API+Mock+APP+Pref      ×
    备注：计划将mock独立成子项目
## 软件架构
集成了Selenium、SMTP、HTMLTestRunner、logging、Reuqests等模块

## 安装教程
    pip install xiaobaiauto
    or
    pip install xiaobaiauto==版本号
    or
    pip install -U xiaobaiauto # 更新到最新版
    or
    pip install xiaobaiauto -i https://pypi.doubanio.com/simple  #网速一般的使用本命令

    ***********************************注意******************************************
    正确安装之后若不能正常导入本库，请将auto.*.pyd与HTMLTestRunner.py复制到自己的项目包中
    *********************************************************************************

#### 使用代码之前请确保您的电脑中已经安装好浏览器及对应的驱动内容
    chrome与chromdriver驱动之间存在不兼容问题，所以最好都下载最新版本为最佳效果
    默认会自动安装，下载默认为与当前安装chrome版本相匹配的驱动文件，默认下载到本地，
    若自当安装失败可能是写入文件权限受限（下方为驱动下载地址）
[chromedriver下载](http://npm.taobao.org/mirrors/chromedriver/) √

#### 基于autogenertor代码生成器的使用
- 查看帮助文档(包含生成器关键词)

    `autogenertor -h`
    
- 创建YAML格式的用例文件

    `autogenertor -t 模板名称.yaml`
    
- 生成单元测试用例文件

    `autogenertor -y yaml用例文件 -c 代码文件名.py`
    
    或者
    
    `autogenertor`       

#### TestCase文件实例（Pycharm社区版 2019.3，Python3.8+）
    import unittest
    from xiaobaiauto.auto import pageObject, Report, log, EmailHandler, Api, Key
    # from auto import pageObject, Report, log, EmailHandler, Api, Key  # 库文件复制到本目录下使用本行代码
    class MyTestCase(unittest.TestCase):
        def setUp(self):
            """
            初始化日志
            :return:
            """
            self.logger = log()
            self.client = Api()
            self.page = pageObject()
            self.page.init(is_max=True)

        def test_api_xxx(self):
            headers = {'content-type': 'application/json'}
            json = {'type': 1, 'orderno': 'abcdef'}
            path = 'http://127.0.0.1:8080/api/v/1.0/'
            try:
                self.client.api(
                                method='GET',
                                url=path,
                                json=json,
                                headers=headers,
                                assertText="包含的预期结果"
                                ).json()
                self.logger.info('xxx接口请求成功')
            except:
                self.logger.error('xxx接口请求失败')
            # self.logger.debug('调试日志信息')
            # self.logger.warning('警告日志信息')
            # self.logger.error('错误日志信息')

        def test_web_12306(self):
            # 通过self.page   调用集成方法
            self.page.get(url='https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E4%B8%8A%E6%B5%B7,SHH&ts=%E9%83%91%E5%B7%9E,ZZF&date=2020-02-02&flag=N,N,Y')
            #self.page.add_cookie(cookie_dict={'name': '', 'value': ''})
            #self.page.add_cookie(cookie_str='name=xiaobai; password=123456')
            chufa = self.page.xpath('//*[@id="fromStationText"]')
            chufa.clear()
            chufa.send_keys('上海')
            chufa.send_keys(Keys.ENTER)

        def tearDown(self):
            pass

    if __name__ == '__main__':
        report_file_name = 'testReport.html'
        suite = unittest.TestSuite()
        # 添加需要执行的测试用例
        suite.addTest(MyTestCase('test_web_12306'))
        #suite.addTest(MyTestCase('test_api_xxx'))  # 不运行就注释掉
        fp = open(report_file_name, 'wb')
        # 生成报告
        runner = Report(
            stream=fp,
            title='测试',
            description='备注信息',
            tester='Tser'
        )
        runner.run(suite)
        fp.close()
        # 将测试报告发送指定邮件<数据务必修改>建议使用QQ邮箱（port参数默认使用SSL端口）
        email = EmailHandler(smtp='smtp.qq.com', port=465, sender_name='qq号', sender_passwd='邮箱授权码')
        email.sendemail(
            _to=['1@qq.com', '2@qq.com'],
            _cc=['admin@163.com', 'leader@gmail.com'],
            title='邮件标题',
            email_content='邮箱内容',
            _type='html',
            filename=[report_file_name]
        )

### 运行脚本
    方式一 （python命令运行）
    step 1 :   打开cmd
    step 2 :   cd 脚本目录
    step 3 :   python 用例脚本名.py

    方式二 （定时器运行脚本）
    - 查看命令帮助文档
    autorunner -h
    
    - 通过定时器循环运行指定脚本
    autorunner -t "0 6,22 0 0 1-5" -d "D:\\Cases" -s 1 -j "a.py,b.py"
    或
    - 运行当前目录下的所有py脚本
    autorunner -t "0 6,22 0 0 1-5"  
    
    - 注意
    日志与测试报告文件默认在命令执行所在的目录下
### 提示
<b>QQ邮箱或者其它企业邮箱必须提前开启SMTP服务</b>
<b>部分邮箱对频发发送邮件进行拦截，所以大家在使用邮箱发送消息时请勿频繁尝试</b>

[点击这里了解QQ邮箱如何开启SMTP服务](https://jingyan.baidu.com/article/6079ad0eb14aaa28fe86db5a.html)

### 更新日志
    V2.4.0
    修改附件为中文名称的BUG，新增定时器功能autorunner
    V2.3.8
    修复BUG
    V2.3.7
    新增了xiaobaiauto代码生成器autogenertor基于yaml格式文件,可以命令行运行：autogenertor -h
    V2.3.6
    更新2.3.4中下载文件的bug（chrome版本不匹配时脚本运行出错）
    V2.3.4
    更新chromedriver.exe下载方式，部分失败原因为网络问题
    V2.3.3
    更新至Py3.8进行编译，有效解决高版本不能调用库的问题
    V2.3.1
    add_cookie()方法添加了cookie_str参数，允许使用从F12直接复制的cookie字符串
    直接赋值即可，cookie_dict与cookie_str两个参数只需要一个赋值即可
    V2.2.1
    因2.0.0版本不能适用于Pycharm社区版，调用失败问题，已修复

#### 参与贡献

作者: <b>@Tser</b><br>
©<b title="公众号：big_touch">小白科技</b>