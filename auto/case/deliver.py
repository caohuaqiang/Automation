# -*- coding:utf-8 -*-
#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
import time
from auto.method.useful import ini


class FB:
    def __init__(self, config: dict):
        self.config = config
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(20)
        self.driver.maximize_window()

    def login(self):
        driver = self.driver
        driver.get('https://erp-t.jfcaifu.com/admin/login.html')
        driver.find_element_by_id("userName").clear()
        driver.find_element_by_id("userName").send_keys("admin")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_id("valicode").clear()
        driver.find_element_by_id("valicode").send_keys("jfcf")
        driver.find_element_by_css_selector('[value=立即登录]').click()
        time.sleep(5)

    def Fa_Biao(self):
        driver = self.driver
        try:
            self.login()
            for x in driver.find_elements_by_css_selector('.panel-title.panel-with-icon'):
                if x.text == '借贷管理':
                    x.click()
            time.sleep(2)
            driver.find_element_by_partial_link_text(u'借款初审').click()
    #===============================================================================================================================================
            iframe_jiekuanchushen = 'src="/modules/loan/borrow/verifyBorrowManager.html"'
            driver.switch_to.frame(driver.find_element_by_css_selector('[%s]' % iframe_jiekuanchushen))     # 跳转到借款初审页面的iframe框架内
            driver.find_element_by_id("a").click()  # 发标
            time.sleep(1)

            iframe_tankuang = 'src="/modules/loan/borrow/borrowAddPage.html?type=112"'
            driver.switch_to.frame(driver.find_element_by_css_selector('[%s]' % iframe_tankuang))   # 跳转到弹框页面(ifram嵌套，从第一层跳到第二层)
    #-----------------------------------发标表单------------------------------------------------------------------------------------------------------

            type = driver.find_elements_by_css_selector('.layui-unselect.layui-form-radio')
            for a in type:                                                                          # 标的类型
                if a.text[1:] == self.config['type']:
                    a.click()

            activity_list = self.config['activity']                                                 # 运营活动
            activity = driver.find_elements_by_css_selector('.layui-unselect.layui-form-checkbox')
            for a in activity:
                if a.text.split('\n')[0] in activity_list:
                    a.click()
            print('--------------------------------------------')

            if self.config['is_recommend'] == 1:
                driver.find_element_by_css_selector('.layui-unselect.layui-form-checkbox>span').click()
            driver.find_element_by_id("ads").send_keys(self.config['bm'])  # 标名
            driver.find_element_by_css_selector('[name="borrowNo"]').send_keys(self.config['product_number'])  # 项目编号

            red_path = '//*[@lay-value="%s"]' % self.config['redpacket']
            coupon_path = '//*[@lay-value="%s"]' % self.config['coupon']
            driver.find_element_by_css_selector('[value="请选择红包方案"]').click()    # 弹出红包方案下拉框
            time.sleep(0.5)
            driver.find_element_by_xpath(red_path).click()

            driver.find_element_by_css_selector('[value="请选择加息券方案"]').click()   # 弹出加息券方案下拉框
            time.sleep(0.5)
            driver.find_element_by_xpath(coupon_path).click()

            driver.find_element_by_id("account").send_keys(self.config['money'])  # 标的金额
            driver.find_element_by_id("apr").send_keys(self.config['apr'])  # 年利率
            driver.find_element_by_id("timeLimit").send_keys(self.config['timelimit'])  # 标的天数
            driver.find_element_by_id("putStartTime").click()  # 开标时间
            driver.find_element_by_xpath(".//*[@id='laydate_ok']").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//*[@placeholder='请选择客服']").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//*[@lay-value='kefu123']").click()  # 客服
            driver.find_element_by_xpath('//*[@placeholder="请选择借款人邮箱"]').click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//*[@lay-value='745133655@qq.com']").click()  # 借款人
            driver.find_element_by_xpath("//*[@lay-filter='save']").click()  # 确定，创建标完成
            time.sleep(4)

    #=========================================初审=========================================================================
            driver.switch_to.default_content()                                                          # 切回主菜单
            driver.switch_to.frame(
                driver.find_element_by_css_selector('[%s]' % iframe_jiekuanchushen))                    # 跳转到借款初审页面的iframe框架内
            above = driver.find_element_by_css_selector('.datagrid-cell.datagrid-cell-c1-action')
            ActionChains(driver).move_to_element(above).perform()                                       # 悬停在“操作栏”，展开选项
            time.sleep(1)
            driver.find_element_by_link_text(u'初审').click()
            driver.switch_to.default_content()
            time.sleep(1)
            check_status = self.config['check_status']
            if check_status == '通过':
                driver.find_element_by_css_selector('[value="1"]').click()
            elif check_status == '不通过':
                driver.find_element_by_css_selector('[value="0"]').click()
            else:
                driver.find_element_by_css_selector('[value="101"]').click()
            driver.find_element_by_link_text(u"确定").click()     # 建标完成
            time.sleep(2)
            driver.find_element_by_link_text(u"确定").click()  # 关闭弹窗：操作成功！
            time.sleep(5)
        except Exception as err:
            filename = '../picture/%s.jpg' % time.strftime("%Y.%m.%d %H.%M.%S", time.localtime())
            driver.save_screenshot(filename)
            print(err)
        finally:
            driver.quit()


if __name__ == '__main__':
    config = eval(ini(filepath='..\\config\\borr.ini').get(section='borrow', option='config'))
    pprint(config)
    fb = FB(config)
    fb.Fa_Biao()



















