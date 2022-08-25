import time
import telebot
from random import randint, uniform
from selenium import webdriver
from bs4 import BeautifulSoup
from constants import *


def open_site():
    """
    Запускает Chrome и открывает сайт записи к врачу
    """
    browser = webdriver.Chrome()
    ref = 'https://emias.info/'
    browser.get(ref)
    time.sleep(uniform(1, 3))
    return browser


def auth():
    """
    Выполняет авторизацию по номеру полиса и дате рождения
    """
    form = browser.find_element_by_tag_name('form')
    time.sleep(uniform(1, 3))

    pol = form.find_element_by_name('policy-number')
    pol.clear()
    pol.send_keys(POLIS)
    time.sleep(uniform(0.2, 1))

    day = form.find_element_by_name('day')
    day.clear()
    day.send_keys(B_DAY)
    time.sleep(uniform(0.2, 1))

    month = form.find_element_by_name('month')
    month.clear()
    month.send_keys(B_MONTH)
    time.sleep(uniform(0.2, 1))

    year = form.find_element_by_name('year')
    year.clear()
    year.send_keys(B_YEAR)
    time.sleep(uniform(0.2, 1))

    form.submit()
    time.sleep(uniform(1.5, 3))


def check():
    """
    Заходит в мои записи, находит врачей, для которых есть возможность переноса,
    и отправляет уведомление
    """
    my_appointments = browser.find_element_by_partial_link_text('Мои записи')
    my_appointments.click()
    time.sleep(2)
    soup = BeautifulSoup(browser.page_source)
    apps = soup.findAll("div", {"class": "headingH3 noteW-"})

    print('Текущие записи:')
    for app in apps:
        print(app.text)

    for i, app in enumerate(apps):
        button = browser.find_elements_by_xpath('//span[text()="Перенести"]')[i]
        button.submit()
        time.sleep(2)
        browser.find_element_by_css_selector('div[role="button"]').click()
        time.sleep(2)
        if 'disabled="false"' in browser.page_source:
            send_notif(app.text)
        browser.back()
        time.sleep(2)


def send_notif(app_name):
    """
    Отправляет уведомление с помощью телеграм-бота
    """
    bot = telebot.TeleBot(TOKEN)
    bot.send_message(int(CHAT_ID), f'Появился слот для переноса записи {app_name}')


if __name__ == '__main__':
    browser = open_site()
    while True:
        try:
            auth()
            check()
        except Exception as e:
            print(e)
        time.sleep(randint(20, 30))
