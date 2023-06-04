import pymysql
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

import os
import time

mydb = pymysql.connect(
    host="localhost", user="root", password="", port=3306, db="weather"
)
cursor = mydb.cursor()


def get_weather(num):
    global condition_list

    option = ChromeOptions()
    option.add_argument("--headless")

    browser = webdriver.Chrome(options=option)
    browser.minimize_window()

    url = format("http://www.weather.com.cn/weather1d/10119%02d01.shtml" % num)
    browser.get(url)

    condition = browser.find_element(
        By.XPATH, "/html/body/div[5]/div[1]/div[1]/div[2]"
    ).text
    # print(condition)

    condition_list = condition.split("\n")

    # print(condition_list[0])
    if len(condition_list) == 1:
        condition_list.append(condition_list[0])

    # print(condition_list)
    browser.close()
    browser.quit()


def connect_db(area):
    area_id = format("%s" % area)
    sql = "INSERT ignore INTO temp (id) values(%s);"  # 这里还不能加""了？ 有bug!!!

    print(sql % (area_id,))
    cursor.execute(sql, (area_id,))  # (x,)表示一个元素的元组

    update_sql = 'update temp set %s = "%s" where id = "%s";'

    # update_sql1 = format(update_sql % (condition_list[0], condition_list[0], id))

    print(update_sql % ("maxTemp", condition_list[15], area_id))
    cursor.execute(update_sql % ("maxTemp", condition_list[15], area_id))
    mydb.commit()

    print(update_sql % ("cond", condition_list[14], area_id))
    cursor.execute(update_sql % ("cond", condition_list[14], area_id))
    mydb.commit()

    select_sql = 'select * from temp where id = "%s"'
    print(select_sql % area_id)
    cursor.execute(select_sql % area_id)

    row = cursor.fetchone()
    while row:
        print("Row:", row)
        print(type(row))
        row = cursor.fetchone()

    mydb.commit()


if __name__ == "__main__":
    area_list = [
        "南京",
        "无锡",
        "镇江",
        "苏州",
        "南通",
        "扬州",
        "盐城",
        "徐州",
        "淮安",
        "连云港",
        "常州",
        "泰州",
        "宿迁",
    ]
    get_weather(1)
    connect_db("南京")
    for i in range(len(area_list)):
        get_weather(i + 1)
        connect_db(area_list[i])
