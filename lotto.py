#!/bin/env python3
import random

from playwright.sync_api import Playwright, sync_playwright
import time

USER_ID = os.environ['USER_ID']
USER_PW = os.environ['USER_PW']


def login(page):
    page.goto('https://dhlottery.co.kr/user.do?method=login')

    page.click('[placeholder="아이디"]')
    page.fill('[placeholder="아이디"]', USER_ID)
    page.press('[placeholder="아이디"]', 'Tab')

    page.fill('[placeholder="비밀번호"]', USER_PW)
    page.press('[placeholder="비밀번호"]', 'Tab')

    with page.expect_navigation():
        page.press('form[name="jform"] >> text=로그인', 'Enter')


def game(page):
    page.goto(url='https://ol.dhlottery.co.kr/olotto/game/game645.do')

    # 비정상 접속 확인버튼 클릭
    if page.locator('#popupLayerAlert').is_visible():
        page.locator('#popupLayerAlert').get_by_role('button', name='확인').click()

    for _ in range(2):
        page.click('label:has-text("자동선택")')
        page.click('text=확인')

    page.click('input:has-text("구매하기")')

    time.sleep(2)
    page.click('text=확인 취소 >> input[type="button"]')
    page.click('input[name="closeLayer"]')


def run(playwright):

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    login(page)
    game(page)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

