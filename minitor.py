from bs4 import BeautifulSoup
import requests
import time
import sys,time
from tkinter import messagebox


#定义一个进度条
def process_bar(num, total):
    rate = float(num)/total
    ratenum = int(100*rate)
    r = '\r[{}{}]{}%'.format('*'*ratenum,' '*(100-ratenum), ratenum)
    sys.stdout.write(r)
    sys.stdout.flush()

def process_bar1(num, total):
    r = '\r[{}{}]{}/{}'.format('*'*num, ' '*(total - num), num, total)
    sys.stdout.write(r)
    sys.stdout.flush()
while 1:
    response = requests.get("https://www.domp4.cc/html/LdwZzHFFFFFH.html")
    response = response.content.decode('utf-8')
    # print(response)

    soup = BeautifulSoup(response, 'html.parser')
    # blog_titles = soup.findAll('h2', attrs={"class":"blog-card__content-title"})
    # label = soup.findAll('span', attrs={"class" : "update_time"})
    # print(label)
    label = soup.findAll('a', attrs={"target": "_self"})
    print(len(label))

    if len(label) > 37:
        print("=================")
        print(label[0].text)
        messagebox.showinfo("new EP")
        break
    i, n = 0, 60
    for i in range(n):
        time.sleep(1)
        process_bar1(i + 1, n)
    print()



