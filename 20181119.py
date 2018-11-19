from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from pyquery import PyQuery as pq
from urllib.request import urlretrieve
# from fontTools.ttLib import TTFont
import requests 
import re
import xlrd
import datetime
from config import *
import pymongo
import time
import os
import codecs
from store_to_db import *
from tools import push_to_myself


client = pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]
db.authenticate(ACCOUNT,PASSWORD)
detail_urls=[]
detail_urls_done=[]
source_id=""
count_times = 0
#tyc_cookies=""
useraccount="****"
pwd='***'
#***************************************************************
def logon():
    browser.get("https://www.tianyancha.com/login")
    print(">>login......")
    browser.find_element_by_css_selector("#web-content > div > div > div > div.position-rel.container.company_container > div > div.in-block.vertical-top.float-right.right_content.mt50.mr5.mb5 > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in > div.pb30.position-rel > input").send_keys(useraccount)
    browser.find_element_by_css_selector("#web-content > div > div > div > div.position-rel.container.company_container > div > div.in-block.vertical-top.float-right.right_content.mt50.mr5.mb5 > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in > div.pb40.position-rel > input").send_keys(pwd)
    time.sleep(2)
    browser.find_element_by_css_selector("#web-content > div > div > div > div.position-rel.container.company_container > div > div.in-block.vertical-top.float-right.right_content.mt50.mr5.mb5 > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in > div.c-white.b-c9.pt8.f18.text-center.login_btn").click()
    #return b
    # print(">>logging")
def anti_robot():
    # browser.get(url)
    if  browser.current_url[8:17]=="antirobot":
        print("**************************************")
        print("********Robot Test**********")
        print("")
        print("")
        print("        AI training          ")
        print("***************************************")
        push_to_myself('',"爬虫遇到验证码",useraccount)
        time.sleep(1200)

def get_searchresult(keyword):
    url="https://www.tianyancha.com/search?key="+keyword+"&checkFrom=searchBox"
    browser.switch_to_window(search_window)
    browser.get(url)
    anti_robot()
    time.sleep(5)
    html = browser.page_source
    #save_search_html(keyword,html)
    try:
        result_count = browser.find_element_by_css_selector(
            "#search > span.num").text
        print("共找到", result_count, "个结果")
    except:
        print("定位查找结果数失败")
    
    try:
        browser.find_element_by_css_selector("#tyc_banner_close").click()
    except:
        pass
    time.sleep(0.2)
    try:
        print(browser.find_element_by_css_selector("#web-content > div > div.container-left > div > div.result-footer > div > ul > li"))
        pags = browser.find_elements_by_css_selector("#web-content > div > div.container-left > div > div.result-footer > div > ul > li")
        print("结果共",len(pags)-1,"页")
    except:
        pass
    
    # read_searchresult()
    # time.sleep(20)
    # for i in range(1,len(pags)-1):
    #         # a.click()
    #         print("当前页",i)
    #         js = "window.scrollTo(0,100000)"
    #         browser.execute_script(js)
    #         print("滚动到底")
    #         read_searchresult()
    #         time.sleep(1)
    #         browser.find_element_by_link_text(">").click()
    #         time.sleep(1)
    #search > span.num
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
    try:

        print("读取", 1, "页")
        read_searchresult()
        try:
            for i in range(1,len(pags)-1):
                js = "window.scrollTo(0,100000)"
                browser.execute_script(js)
                # print("滚动到底")
                time.sleep(2)
                browser.find_element_by_link_text(">").click()
                print("当前页",i+1)
                # time.sleep(1)
                read_searchresult()

        except Exception:
            print('读取多页失败', Exception)
    except:
        print("只有一页")


def read_searchresult():
    # print(">start reading result")
    results = browser.find_elements_by_css_selector("#web-content > div > div.container-left > div > div.result-list > div")
    print(len(results))
    # print(results)
    for item in results:
        name = item.find_element_by_css_selector("div.content > div.header > a").text
        corp_id=item.get_attribute('data-id')
        # print(divs.text)
        status=item.find_element_by_css_selector("div.content > div.header > div").text
        try:
            legalPeasonName=item.find_element_by_css_selector("div.content > div.info > div:nth-child(1) > a").text
        except:
            legalPeasonName="未公开"
        regCapital=item.find_element_by_css_selector("div.content > div.info > div:nth-child(2) > span").text
        regTime= item.find_element_by_css_selector("div.content > div.info > div:nth-child(3) > span").text
        try:
            reg_area=item.find_element_by_css_selector(".site").text
        except:
            reg_area=""    
        try:
            score=item.find_element_by_css_selector(".score").text
        except:
            score=''
        url=item.find_element_by_css_selector("div.content > div.header > a").get_attribute('href')
        data = {
                "name": name,
                "corp_id":corp_id,
                "status": status,
                "legalPeasonName": legalPeasonName,
                "regCapital": regCapital,
                "regTime": regTime,
                "reg_area": reg_area,
                "score": score,
                "url":url
            }
        # print(data)
  
        add_job(data)
        # tmp=db[T_CORP_LIST].find({"corp_id":corp_id}).count()
        # print(type(tmp))
        # print(tmp)

        # if (db[T_CORP_LIST].find({"corp_id":corp_id}).count()>0):
            # print("Exists>>>>",name)
            
            # time.sleep(2)
        # else:
            # print("New Company~>",name)
            # save_corp_list(data)
def read_investinfo(investment):
    # print(">对外投资")
    anti_robot()
    trs=browser.find_elements_by_css_selector("#_container_invest > table > tbody > tr")
    # print(trs)

    for tr in trs:
        #_container_invest > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td:nth-child(2) > a
        invest_corpname=tr.find_element_by_css_selector("td:nth-child(2) > table > tbody > tr > td:nth-child(2)").text
        try:
            invest_corpurl=tr.find_element_by_css_selector("td:nth-child(2) > table > tbody > tr > td:nth-child(2) > a").get_attribute("href")
        except:
            invest_corpurl=''

        inv_corplgp=tr.find_element_by_css_selector("td.left-col > span").text
        inv_cap=tr.find_element_by_css_selector("td:nth-child(4) > span").text
        #_container_invest > table > tbody > tr:nth-child(1) > td:nth-child(4) > span
        #_container_invest > table > tbody > tr:nth-child(5) > td:nth-child(4) > span
        inv_rate=tr.find_element_by_css_selector("td:nth-child(5) > span").text
        inv_time=tr.find_element_by_css_selector("td:nth-child(6) > span").text
        inv_status=tr.find_element_by_css_selector("td:nth-child(7) > span").text
        item={
            "invest_corpname":invest_corpname,
            "invest_corpurl":invest_corpurl,
            "inv_corplgp":inv_corplgp,
            "inv_rate":inv_rate,
            "inv_cap":inv_cap,
            "inv_time":inv_time,
            "inv_status":inv_status
        }
        # print(item)
        investment.append(item)
        job={
        "name":invest_corpname,
        "url":invest_corpurl
        }
        if invest_corpurl:
            add_job(job)
def get_investinfo(): 
    anti_robot()
    investment=[]
    try:       
        pags=browser.find_elements_by_css_selector("#_container_invest > div > ul > li")
        page_count=len(pags)
    except:
        page_count=1
    print()    
    if page_count==1:
        read_investinfo(investment)
    else:
        read_investinfo(investment)
        for i in range(1,page_count-1):
            print(">click nextp")
            pags=browser.find_elements_by_css_selector("#_container_invest > div > ul > li")
            ActionChains(browser).move_to_element(pags[len(pags)-1]).perform()
            js = "window.scrollBy(0,220)"
            browser.execute_script(js)
            ActionChains(browser).click(pags[len(pags)-1]).perform()
            time.sleep(3)
            read_investinfo(investment)
    return investment    

def get_holderinfo(): 
    anti_robot()
    main_holder=[]
    try:       
        pags=browser.find_elements_by_css_selector("#_container_holder > div > ul > li")
        page_count=len(pags)
    except:
        page_count=1
    # print()    
    if page_count==1:
        read_holderinfo(main_holder)
    else:
        read_holderinfo(main_holder)
        for i in range(1,page_count-1):
            print(">click nextp")
            pags=browser.find_elements_by_css_selector("#_container_holder > div > ul > li")
            ActionChains(browser).move_to_element(pags[len(pags)-1]).perform()
            
            js = "window.scrollBy(0,50)"
            browser.execute_script(js)
            time.sleep(2)
            ActionChains(browser).click(pags[len(pags)-1]).perform()
            time.sleep(3)
            read_holderinfo(main_holder)
    return main_holder    

def read_holderinfo(main_holder):
    # print(">对外投资")
    anti_robot()
    trs=browser.find_elements_by_css_selector("#_container_holder > table > tbody > tr")
    
    # print(trs)


    for tr in trs:
        holder_name=tr.find_element_by_css_selector("td:nth-child(2) > div > div.dagudong > a").text
        inv_rate=tr.find_element_by_css_selector("td:nth-child(3) > div > div > span").text
        inv_cap=tr.find_element_by_css_selector("td:nth-child(4) > div > span").text
        inv_time=tr.find_element_by_css_selector("td:nth-child(5) > div > span").text
        holder_url=tr.find_element_by_css_selector("td:nth-child(2) > div > div.dagudong > a").get_attribute("href")
        item={
            "holder_name":holder_name,
            "holder_url":holder_url,
            "inv_rate":inv_rate,
            "inv_cap":inv_cap,
            "inv_time":inv_time
        }
        print(item)
        main_holder.append(item)

def get_staffinfo(): 
    main_staff=[]
    anti_robot()
    try:       
        pags=browser.find_elements_by_css_selector("#_container_staff > div > ul > li")
        page_count=len(pags)
    except:
        page_count=1
    # print()    
    if page_count==1:
        read_staffinfo(main_staff)
    else:
        read_staffinfo(main_staff)
        for i in range(1,page_count-1):
            print(">click nextp")
            pags=browser.find_elements_by_css_selector("#_container_staff > div > ul > li")
            ActionChains(browser).move_to_element(pags[len(pags)-1]).perform()
            
            js = "window.scrollBy(0,50)"
            browser.execute_script(js)
            time.sleep(2)
            ActionChains(browser).click(pags[len(pags)-1]).perform()
            time.sleep(3)
            read_staffinfo(main_staff)
    return main_staff    

def read_staffinfo(main_staff):
    print(">主要人员")
    anti_robot()
    trs=browser.find_elements_by_css_selector("#_container_staff > div > table > tbody > tr")
    # _container_staff > div > table > tbody > tr:nth-child(1)
    # print(trs)
    for tr in trs:
        psn_name=tr.find_element_by_css_selector("td:nth-child(2) > div > a.link-click").text
        psn_positon=tr.find_element_by_css_selector("td:nth-child(3) > span").text
        try:
            psn_url=tr.find_element_by_css_selector("td:nth-child(2) > div > a.link-click").get_attribute("href")
        except:
            psn_url=''
        item={
            "psn_name":psn_name,
            "psn_url":psn_url,
            "psn_positon":psn_positon
        }
        main_staff.append(item)
        print(item)

    # for tr in trs:
    #     holder_name=tr.find_element_by_css_selector("td:nth-child(2) > div > div.dagudong > a").text
    #     inv_rate=tr.find_element_by_css_selector("td:nth-child(3) > div > div > span").text
    #     inv_cap=tr.find_element_by_css_selector("td:nth-child(4) > div > span").text
    #     inv_time=tr.find_element_by_css_selector("td:nth-child(5) > div > span").text
    #     item={
    #         "holder_name":holder_name,
    #         "inv_rate":inv_rate,
    #         "inv_cap":inv_cap,
    #         "inv_time":inv_time
    #     }
    #     print(item)
    #     main_staff.append(item)

def get_corpdetails():
    anti_robot()
    # cur_corp=db[T_CORP_LIST].find_one()
# 处理插队任务
    if db["detail_urls_root"].find().count()>0:
        cur_corp=db["detail_urls_root"].find_one_and_delete({})
        # add_job(cur_corp)
        db["detail_urls_root"].insert(cur_corp)
        url=cur_corp["url"]
        cur_corp["src"]="root_job"
        print(url)
        browser.switch_to_window(detail_window)
        try:
            browser.find_element_by_css_selector("#tyc_banner_close").click()
        except:
            pass
        browser.get(url)
        time.sleep(3)
        read_corpdetails(cur_corp)
    else:
        print("No detail Jobs!")
        time.sleep(2)
# 处理常规JOB任务
    if db["detail_urls"].find().count()>0:
        cur_corp=db["detail_urls"].find_one_and_delete({})
        add_job(cur_corp)
        url=cur_corp["url"]
        cur_corp["src"]="nomal_job"
        print(url)
        browser.switch_to_window(detail_window)
        try:
            browser.find_element_by_css_selector("#tyc_banner_close").click()
        except:
            pass
        browser.get(url)
        time.sleep(3)
        read_corpdetails(cur_corp)
    else:
        print("No detail Jobs!")
        time.sleep(2)
def get_front(url,corp_id): 
    
    # print "downloading with requests"
    # url = 'http://ww.pythontab.com/test/demo.zip' 
    r = requests.get(url) 
    filename="./css/"+corp_id+".css"
    with open(filename, "wb") as code:
        code.write(r.content)
    fronturl=''
    with open(filename, 'r') as f:
        for l in f.readlines():
            woff=re.findall('.+(https.+\.woff).+',l,re.M)
            if len(woff)>0:
                # print(woff[0])
                fronturl=woff[0]
    print(fronturl)
    return fronturl

def decode_txt(text,front_url):
    data={
    'text':text,
    'woff':front_url
    }

    try:
        r=requests.post("http://47.105.125.121:8080/decodewoff",data=data)
    except:
        pass
    print(r.text)
    return r.text

def read_corpdetails(cur_corp):
    # print(browser.title)
    anti_robot()
    print(cur_corp)
    corp_url=cur_corp["url"]
    print(">>reading details")
    # print( browser.current_url[8:17])
    if  browser.current_url[8:17]=="antirobot":
        time.sleep(1200)
    
    print("获取字体文件")
    corp_id=re.search("(\d+)",corp_url).group(0)
    links=browser.find_elements_by_css_selector("head > link")
    front_url=''
    for link in links:
        if link.get_attribute("href").find("font.css")>-1:
            print(link.get_attribute("href"))
            front_url=get_front(link.get_attribute("href"),corp_id)
            
    time.sleep(2)
    try:
        browser.find_element_by_css_selector("#tyc_banner_close").click()
    except:
        pass
    #开始获得详细信息
    # tg=browser.find_element_by_css_selector("#company_web_top > div.box > div.content > div.header > h1")
    # tg.screenshot("tg1.png")
    # tg.screenshot_as_png("tg.png")



    # time.sleep(20)
    try:
        corp_name=browser.find_element_by_css_selector("#company_web_top > div.box > div.content > div.header > h1").text
    except:
        corp_name=cur_corp["name"]
    try:
        corp_link=browser.find_element_by_css_selector("#company_web_top > div.box > div.content > div.detail > div:nth-child(2) > div:nth-child(1) > a").get_attribute("href")
    except:
        corp_link="-"
    try:
        lgl_repr=browser.find_element_by_css_selector("#_container_baseInfo > table:nth-child(1) > tbody > tr:nth-child(1) > td.left-col.shadow > div > div:nth-child(1) > div.humancompany > div.name > a").text
    except:
        lgl_repr='-'
    try:
        reg_cptl=browser.find_element_by_css_selector("#_container_baseInfo > table:nth-child(1) > tbody > tr:nth-child(1) > td:nth-child(2) > div:nth-child(2)").get_attribute("title")
    except:
        reg_cptl=''
    try:
        reg_date=browser.find_element_by_css_selector("#_container_baseInfo > table:nth-child(1) > tbody > tr:nth-child(2) > td > div:nth-child(2) > text").text
    except:
        reg_date=''
    try:
        reg_num=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(1) > td:nth-child(2)").text
    except:
        reg_num=''
    try:
        org_num=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(1) > td:nth-child(4)").text
    except:
        org_num=''
    try:
        uni_num=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(2) > td:nth-child(2)").text
    except:
        uni_num=''
    try:
        tax_num=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(3) > td:nth-child(2)").text
    except: 
        tax_num=''
    try:    
        com_type=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(2) > td:nth-child(4)").text
    except:
        com_type=''
    try:

        industry=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(3) > td:nth-child(4)").text
    except:
        industry=''
    try:
        term=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(4) > td:nth-child(2) > span").text
    except:
        term=''
    try:
        chk_date=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(4) > td:nth-child(4) > text").text
    except:
        chk_date=''
    try:
        tax_type=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(5) > td:nth-child(2)").text
    except:
        tax_type=''
    try:       
        emp_scale=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(5) > td:nth-child(4)").text
    except:
        emp_scale=''
    try:
        act_captal=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(6) > td:nth-child(2)").text
    except:
        act_captal=''
    try:
        reg_org=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(6) > td:nth-child(4)").text
    except:
        reg_org=''
    try:
        canbao_num=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(7) > td:nth-child(2)").text
    except:
        canbao_num=''
    try:
        eng_name=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(7) > td:nth-child(4)").text
    except:
        eng_name=''
    try:
        reg_addr=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(8) > td:nth-child(2)").text.replace("附近公司","")
    except:
        reg_addr=''
    # try:
    #     scope=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(9) > td:nth-child(2) > span > span > span.js-split-container").text
    #     # scope=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(9) > td:nth-child(2) > span > span > span.js-full-container.hidden").text
    # except:
    #     scope=''
    try:
        # scope=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(9) > td:nth-child(2) > span > span > span.js-full-container.hidden").text
        scope=browser.find_element_by_css_selector("#_container_baseInfo > table.table.-striped-col.-border-top-none > tbody > tr:nth-child(9) > td:nth-child(2) > span > span > span.js-full-container.hidden")
        scope=re.search('.*">(.+)</.*', scope.get_attribute("outerHTML")).group(1)
    except:
        scope=''

    before_text=reg_cptl+"|"+reg_date+"|"+chk_date
    after_text=decode_txt(before_text,front_url)

    # decode_texts=after_text.split("|")
    # 处理解密后数据你2018-11-19
    t,reg_date,chk_date=after_text.split("|")

    base_info={
        "corp_name":corp_name,
        "corp_url":corp_url,
        # "corp_id":cur_corp["corp_id"],
        "corp_link":corp_link,
        "lgl_repr":lgl_repr,
        "reg_cptl":reg_cptl,
        "reg_date":reg_date,
        "reg_num":reg_num,
        "org_num":org_num,
        "uni_num":uni_num,
        "tax_num":tax_num,
        "com_type":com_type,
        "industry":industry,
        "term":term,
        "chk_date":chk_date,
        "tax_type":tax_type,
        "emp_scale":emp_scale,
        "act_captal":act_captal,
        "reg_org":reg_org,
        "canbao_num":canbao_num,
        "eng_name":eng_name,
        "reg_addr":reg_addr,
        "scope":scope,
        "front_url":front_url,
        "before_text":before_text,
        "after_text":after_text
    }
    # main_staff=[]
    try:
        main_staffcount=browser.find_element_by_css_selector("#nav-main-staffCount > span").text
        print("主要人员数量",main_staffcount)
    except:
        pass
    main_staff=get_staffinfo()


    base_info["main_staff"]=main_staff
    # main_holder=[]
    try:
        main_holdercount=browser.find_element_by_css_selector("#nav-main-holderCount > span").text
        print("主要股东数量",main_holdercount)

    except:
        pass
    main_holder=get_holderinfo()
    base_info["main_holder"]=main_holder
#获取对外投资信息
    
    # page_count=1
    # main_investcount=0
    try:
        main_investcount=browser.find_element_by_css_selector("#nav-main-inverstCount > span").text
        print("对外投资数量：",main_investcount)
    #     pags=browser.find_elements_by_css_selector("#_container_invest > div > ul > li")
    #     page_count=len(pags)
        
    except:
        pass
    investment=get_investinfo()
    
    base_info["investment"]=investment

    # print(base_info)  
    save_base_info(base_info)
    job={
        "name":corp_name,
        "url":corp_url,
        "src":cur_corp["src"]
    }
    job_done(job)
    # db[T_CORP_LIST].remove({"corp_id" : cur_corp["corp_id"]})
# 清理job    
def job_done(job):
    if job["src"]=="nomal_job":
        db["detail_urls"].remove({"url":job["url"]})
        print("移除nomal_job",job["name"])
    if job["src"]=="root_job":
        db["detail_urls_root"].remove({"url":job["url"]})
        print("移除root_job",job["name"])    
    db["detail_urls_done"].insert(job)
    print("job添加到已完成",job["name"])
    print(">>>Hiding~~~Be a good AI spider!")
    time.sleep(20)


def init_tasklist(break_time):
    donejobs=db["detail_urls_done"].find()

def add_job(job):
    if (db["detail_urls"].find({"url":job["url"]}).count()==0):
        if(db["detail_urls_done"].find({"url":job["url"]}).count()==0):
            db["detail_urls"].insert(job)
            print("添加JOB:",job)
        else:
            print("exist in job-done")
    else:
        print("exist in job")




# ======================================================================================================
#主代码开始
chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox') 
chrome_options.add_argument('–-disable-plugins') 
chrome_options.add_argument('–-disable-images') 
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(chrome_options=chrome_options)
# browser.maximize_window()
need_recovery='N'
# need_recovery='Y'
break_time = "2017-09-26 23:24:55"
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(now)
search_window=browser.window_handles[0]
js='window.open("www.baidu.com");'
browser.execute_script(js)
detail_window=browser.window_handles[1]
#可选开始切换IP
# change_ip()

# if need_recovery=='Y':
#     [detail_urls, detail_urls_done] = init_tasklist(break_time)


def main():
    print("start working.....")
    starttime = datetime.datetime.now()
    #输入上次断点保存时间
    # d={
    #     "keyword":"复星高科"
    # }
    # db[T_SEARCHKEY].insert(d)
    


    logon()
    time.sleep(1)
    try:
        push_to_myself('',"爬虫开始执行",useraccount)
        while True:
            if db[T_SEARCHKEY].find().count()>0:
                keywords=db[T_SEARCHKEY].find()
                anti_robot()
                for tmp in keywords:
                    keyword=tmp["keyword"]
                    print("Get search job:",keyword)
                    get_searchresult(keyword)
                    db[T_SEARCHKEY].remove({"keyword":keyword})
                    print("Finish search job:",keyword)
            else:
                print(datetime.datetime.now(),"No search Jobs!")
                print(browser.window_handles)
                # browser.switch_to_window(browser.window_handles[1])
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(now)
                anti_robot()
                get_corpdetails()
                # print(browser.title)
                # print(search_window)
                # print(detail_window)
                time.sleep(0.5)
    except:
        
        push_to_myself('',"爬虫遇到错误而停止",useraccount)
    
    

         


if __name__ == '__main__':
    main()
    browser.close()

