import time
from bs4 import BeautifulSoup
from splinter import Browser
import os
from messenger import Messenger

wait_delay = 1

users_data = os.getenv("usr_info")

def get_status(usr_info):
    b = Browser('chrome', headless=True, executable_path='chromedriver')
    time.sleep(wait_delay)
    b.visit('https://mc.manuscriptcentral.com/tip-ieee/')
    time.sleep(wait_delay)
    b.fill('USERID', usr_info[0])
    time.sleep(wait_delay)
    b.fill('PASSWORD',usr_info[1])
    time.sleep(wait_delay)
    b.click_link_by_id('logInButton')
    time.sleep(wait_delay)
    b.click_link_by_partial_href("AUTHOR")
    time.sleep(wait_delay)
    html_obj = b.html
    soup = BeautifulSoup(html_obj,"lxml")
    #  soup = BeautifulSoup(html_obj)
    # table = soup.find("table", attrs={"class":"table table-striped rt cf"})
    # row = table.tbody.findAll('tr')[1]
    # first_column_html = str(row.findAll('td')[1].contents[0])
    # current_manuscript_status = BeautifulSoup(first_column_html,"lxml").text
    current_manuscript_status = soup.find(id="queue_0").findAll('td')[0].contents[0].text
    # current_manuscript_status = 'demo'
    # print current_status_msg
    time.sleep(wait_delay)
    b.quit()
    return current_manuscript_status

if __name__ == '__main__':
    print(get_status(users_data))