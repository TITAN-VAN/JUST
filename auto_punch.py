from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import time
import os


def clock_in(uname, passwd, name, Location):
    # 实现无可视化操作，设置JavaScript脚本
    chrome_options = Options()
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('window-size=2048x1080')
    chrome_options.binary_location = r'/usr/bin/google-chrome'
    bro = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)
    js_top = "var q=document.documentElement.scrollTop=0"
    # js = "document.getElementsByClassName('ant-input ant-input-disabled')[1].removeAttribute('disabled')"
    js = "function getElementByXpath(path) {return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;};getElementByXpath('./html/body/div[2]/div/div[1]/div[2]/form/div/div[2]/div/div[2]/div/div/div/span/input').disabled = false"

    # 请求门户网站，获取授权
    i = 1
    while i < 5:
        print('这是第' + str(i) + '次尝试登陆门户网站')
        bro.get('http://ids2.just.edu.cn/cas/login?service=http%3A%2F%2Fmy.just.edu.cn%2F')
        sleep(2)
        bro.get('http://ids2.just.edu.cn/cas/login?service=http%3A%2F%2Fmy.just.edu.cn%2F')
        sleep(5)
        try:
            username_btn = bro.find_element_by_xpath(
                '/html/body/div[2]/div[1]/div[2]/div/div[1]/div/div/form[1]/div[2]/input')
            password_btn = bro.find_element_by_xpath(
                '/html/body/div[2]/div[1]/div[2]/div/div[1]/div/div/form[1]/div[3]/input')
            username_btn.send_keys(uname)
            password_btn.send_keys(passwd)
            login_btn = bro.find_element_by_xpath(
                '/html/body/div[2]/div[1]/div[2]/div/div[1]/div/div/form[1]/div[5]/input[4]')
            login_btn.click()
            sleep(2)
        except:
            i = i + 1
            print('第' + str(i-1) + '次登录门户网站失败（tips:三次登陆失败会出验证码）')
            continue
        # 进行是否登陆成功的检查
        try:
            bro.get('http://my.just.edu.cn/_s2/students_sy/main.psp')
            sleep(5)
            out = bro.find_element_by_xpath(
                '/html/body/div/div[1]/div[1]/div/div[1]/div[2]/div/div/div/div/div/div/div/li[6]/span').text #get_attribute("textContent")
        except:
            i = i + 1
            print('第' + str(i - 1) + '次登录门户网站失败')
        else:
            if "退出" in out:
                print('信息门户登录完成')
                break
            else:
                print('信息门户登录失败（也许）')
                break

    # 直接请求打卡页面，通过js解除input的disabled属性，然后填写地址
    j = 1
    while j < 5:
        bro.get('http://dc.just.edu.cn/jkdk.html')
        sleep(2)
        bro.get('http://dc.just.edu.cn/jkdk.html')
        sleep(6)
        try:
            bro.execute_script(js)
        except:
            print("第" + str(j) + "访问打卡页面失败,原因未知，截图已保存")
            if j == 1:
                bro.get_screenshot_as_file(u"/root/screenshot/" + "failed" + str(j) + name + time_format() + ".png")
            j = j + 1
        else:
            print('已设置禁用')
            sleep(1)
            wz = bro.find_element_by_xpath(
                '/html/body/div[2]/div/div[1]/div[2]/form/div/div[2]/div/div[2]/div/div/div/span/input')
            wz.send_keys(Location)
            print('位置已填写' + Location)
            bro.execute_script(js_top)
            bro.get_screenshot_as_file(u"/root/screenshot/" + "1" + name + time_format() + ".png")
            submit_btn = bro.find_element_by_xpath('//*[@id="root"]/div/div[1]/div[2]/div[2]/button')
            submit_btn.click()
            print(name + '已提交')
            sleep(1)
            break

    # # 如果提交成功，(二次验证返回打卡成功)，通过判断div是否存在和捕获异常来实现
    try:
        bro.find_element_by_xpath('//*[@id="root"]/div/div/p/div/p[2]/span')
    except NoSuchElementException:
        print(name + '二次确认打卡失败（也许）')
    else:
        text = bro.find_element_by_xpath('//*[@id="root"]/div/div/p/div/p[2]/span').text
        if '填报成功' in text:
            print(name + '二次确认打卡成功')
        else:
            print(name + '二次确认打卡失败,失败原因：' + text)

    print(name + "结束")
    print("——————————————————————————————————————————————————")
    bro.quit()


def time_format():
    current_time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(time.time()))
    return current_time


if __name__ == '__main__':
    print(time_format())
    #写自己的位置
    Location1 = ""位置
    #删除上一次的截图
    os.system('rm -rf /root/screenshot/*')
    #由于脚本出错可能会导致进程残留，而chrome是内存怪兽，故进行预防
    os.system('killall chromedriver')
    os.system('killall chrome')
    uname_passwd = [
        ['学号', '密码', '姓名', Location1]
    ]
    for up in uname_passwd:
        clock_in(up[0], up[1], up[2], up[3])
