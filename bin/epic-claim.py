#!/bin/env python3
"""
Epic Games Store Freebies Claiming bot.
Uses Chromedriver(monkeypatched if possible)
"""
import sys
import re
import logging as log
from xml.sax.saxutils import escape
from datetime import datetime
from os import environ, devnull, path, makedirs, symlink, remove, execv
from subprocess import run, Popen
from random import randint
from time import sleep

import requests as r


def randsleep(tmax=20, tmin=5):
    """
    Sleep random seconds between tmin and tmax
    """
    if environ.get('NOSLEEP', None):
        sleep(randint(tmin, tmax))


TMOUT = False
UPDATED_AT = datetime.strptime('2021-08-06T18:22:51Z', '%Y-%m-%dT%H:%M:%SZ')

try:
    from pathlib import Path
except ModuleNotFoundError:
    print("pathlib not installed")
    sys.exit()

try:
    import gi
except ModuleNotFoundError:
    print("pygobject not installed")
    sys.exit()
try:
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify, GLib
except ModuleNotFoundError:
    print("libnotify not installed")
    sys.exit()
try:
    from undetected_chromedriver import ChromeDriverManager as uc
except ImportError:
    pass
else:
    uc(executable_path=environ.get(
        'CHROMEDRIVER', '/usr/bin/chromedriver')).install()
try:
    from selenium.webdriver import Chrome, ChromeOptions
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
except ModuleNotFoundError:
    print("selenium not installed")
    sys.exit()

try:
    p = Popen(['chromedriver'], stdout=open(devnull), stderr=open(devnull))
    p.terminate()
    p.communicate()
except FileNotFoundError:
    print('chromedriver not installed')

#                            auto updater                            #
gh_data = r.post('https://api.github.com/graphql',
                 json={
                     'query':
                     """{
    user(login:"ahmubashshir") {
        gist(name:"ba1a898ab593f85597cfc76a3f8c7106") {
            pushedAt
        }
    }
}"""
                 }).json()
if gh_data:
    updated_last = datetime.strptime(
        gh_data['data']['user']['gist']['pushedAt'], '%Y-%m-%dT%H:%M:%SZ')
    if (updated_last - UPDATED_AT).seconds > 60:
        print("updating {} -> {}".format(
            UPDATED_AT.strftime('%Y%m%d%H%M%S'),
            updated_last.strftime('%Y%m%d%H%M%S')))
        gh_data = r.post('https://api.github.com/graphql',
                         json={
                             'query':
                             """{
    user(login:"ahmubashshir") {
        gist(name:"ba1a898ab593f85597cfc76a3f8c7106") {
            files {
                name
                text
            }
        }
    }
}"""
                         }).json()
        if gh_data:
            _data = next(file['text']
                         for file in gh_data["data"]['user']['gist']['files']
                         if file['name'] == 'epic-claim.py')
            with open(__file__, 'w') as f:
                f.write(_data)
                print("updated")
            execv(sys.argv[0], sys.argv)

Notify.init("epic-claim")
_DAEMON_RELOAD = False
IS_LOGGED_OUT = False
SYSTEMD = {
    'service': [
        '[Unit]', 'Description=Epic Games Store - Freebies claim bot'
        '', '[Service]', 'Environment=HEADLESS=1',
        'ExecStart=%h/.config/systemd/epic-claim', 'RestartSec=45m',
        'Restart=on-error', '', '[Install]', 'WantedBy=default.target'
    ],
    'timer': [
        '[Unit]',
        'Description=Claim Epic Games Store freebies 4 times a week.', '',
        '[Timer]', 'OnCalendar=Fri,Sun,Tue,Thu 18:00 UTC',
        'RandomizedDelaySec=30m', 'Persistent=true', '', '[Install]',
        'WantedBy=timers.target'
    ]
}

Break = type("Break", (BaseException, ), {})
if __name__ == '__main__':
    _dir = path.join(environ['HOME'], '.config/systemd/user')
    makedirs(_dir, exist_ok=True)
    _DAEMON_RELOAD = False
    for each in ['service', 'timer']:
        _file = path.join(_dir, 'epic-claim.%s' % each)
        if not path.isfile(_file):
            with open(_file, 'w') as f:
                f.write('\n'.join(SYSTEMD[each]))
            _DAEMON_RELOAD = True

    if _DAEMON_RELOAD:
        run(['systemctl', '--user', 'daemon-reload'], check=False)
        run(['systemctl', '--user', 'enable', 'epic-claim.timer'], check=False)

    paths = [path.join(environ['HOME'], '.config/systemd'), environ['HOME']]

    for each in paths:
        if not path.isfile(path.realpath(path.join(each, 'epic-claim'))):
            try:
                remove(path.join(each, 'epic-claim'))
            except FileNotFoundError:
                pass
        if not path.islink(path.join(each, 'epic-claim')):
            symlink(path.abspath(sys.argv[0]), path.join(each, 'epic-claim'))
    del each

LOGFORMAT = '[%(asctime)] %(message)s'
if 'HEADLESS' in environ.keys(
) and environ['HEADLESS'] == '1' and 'NOLOG' not in environ.keys():
    log.basicConfig(filename=Path(environ['HOME']).joinpath(
        'logs', 'epic-claim.log'),
        level=log.INFO,
        format='%(asctime)s %(message)s',
        datefmt='[%FT%T%z]')
    HEADLESS = True
else:
    log.basicConfig(level=15)
    HEADLESS = False
log.addLevelName(15, 'Info')
log.log(15, 'Started bot.')


def continue_verify_age(browser):
    """
    Continue after verifying age.
    """
    xpath = '//'.join([
        '',
        'div[@data-component="WarningLayout"]',
        'button[@data-component="BaseButton"]'
    ])
    print(xpath)
    try:
        WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
    except Exception as _e:
        print(_e)
    else:
        browser.find_element_by_xpath(xpath).click()  # I'm Not A Kid Anymore
        randsleep()


def continue_unsupported_device(browser):
    """
    Continue even if device is unsupported.
    """
    xpath = '//'.join([
        '',
        'div[@data-component="WarningLayout"]',
        'div[@data-component="makePlatformUnsupportedWarningStep"]',
        'button[@data-component="BaseButton"]'
    ])
    print(xpath)
    try:
        WebDriverWait(browser, 300).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
    except Exception as _e:
        print(_e)
    else:
        browser.find_element_by_xpath(xpath).click()  # I'm just claiming this
        randsleep()


def place_order(browser):
    """
    Place the order.
    """
    xpath = '//'.join([
        '',
        "*[@id='purchase-app']",
        "div[contains(@class, 'order-summary-content')]",
        "button[*[%s]]" % ' and '.join([
            "contains(text(), 'Place')",
            "contains(text(), 'Order')"
        ])
    ])
    print(xpath)
    try:
        WebDriverWait(browser, 600).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH,
                 "//*[@id='webPurchaseContainer']//iframe[1]")
            )
        )
        WebDriverWait(browser, 600).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath)))
        purchase_button_element = browser.find_element_by_xpath(xpath)
    except Exception as _e:
        print(_e)
    else:
        for _ in range(0, 4):
            try:
                purchase_button_element.click()
                randsleep(4, 1)
            except Exception:
                break
        browser.switch_to.parent_frame()


def i_agree(browser):
    """
    EU ?* Agreement
    """
    xpath = '''//*[%s]''' % ' and '.join([
        "contains(text(),'I')",
        "contains(text(),'Agree')"
    ])
    print(xpath)
    try:
        browser.find_element_by_xpath(xpath)
        WebDriverWait(browser, 600).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath)))
    except Exception as _e:
        print(_e)
    else:
        _i_agree = browser.find_element_by_xpath(xpath)

        _i_agree.click()
        randsleep(6)


def notify(msg, icon='face-wink'):
    """
    Show notification.
    """
    notif = Notify.Notification.new("Epic Games", msg, icon)
    notif.set_urgency(Notify.Urgency.LOW)
    notif.set_timeout(Notify.EXPIRES_NEVER)
    notif.show()


def get_game(game, browser):
    """
    Load game and place order.
    """
    url = 'https://www.epicgames.com/store/en-US/%(type)s/%(slug)s' % game
    browser.get(url)

    continue_verify_age(browser)
    xpath = ' '.join([
        '//*[@data-component="Text"',
        'and',
        f"""contains(text(),"{escape(game['name'])}")""",
        'and',
        'contains(@class,"headline")]'
    ])
    print(xpath)
    WebDriverWait(browser, 600).until(
        EC.visibility_of_element_located(
            (By.XPATH, xpath)))

    randsleep()
    xpath = '''//button[*[contains(text(),'Get')]]'''
    for button in browser.find_elements(By.XPATH, xpath):
        text = re.sub(r'[^a-zA-Z0-9]', '', button.text).upper()
        if text == 'OWNED':
            log.log(15, f"You already own '{game['name']}'")
            return False
        if text == 'GET':
            log.log(15, f"Claiming '{game['name']}' for you")
            try:
                button.find_element_by_xpath('parent::node()').click()
            except Exception as _e:
                print(_e)
            continue_unsupported_device(browser)
            place_order(browser)
            randsleep(10)
            try:
                WebDriverWait(browser, 600).until(
                    EC.visibility_of_element_located((
                        By.XPATH,
                        '/'.join([
                            '//*[@id="scrollContainerDiv"]',
                            '/div[contains(@class,"alert-danger")]',
                            'span'
                        ])
                    )))
            except Exception:
                pass
            else:
                _el = browser.find_element(
                    By.XPATH,
                    '/'.join([
                        '//*[@id="scrollContainerDiv"]',
                        '/div[contains(@class,"alert-danger")]',
                        'span'
                    ])
                )
                if _el.is_displayed():
                    log.error(_el.text)
                    return False

            i_agree(browser)
            randsleep()
            xpath = '''//span[%s]''' % ' and '.join([
                "contains(text(),'%s')" % n
                for n in 'Thank you for buying'.split(' ')
            ])
            print(xpath)
            WebDriverWait(browser, 600).until(
                EC.visibility_of_element_located(
                    (By.XPATH, xpath)))
            notify("Claimed '%(name)s'" % game)
            log.info("Claimed '%(name)s'" % game)
            return True
    return False


def try_accept_cookies(browser):
    """
    Accept cookies.
    """
    try:
        cookies = browser.find_element_by_xpath(
            '''/html/body/div/div/div[4]/header/header/div/button/span''')
    except Exception:
        pass
    else:
        WebDriverWait(browser, 600).until(EC.element_to_be_clickable(cookies))
        cookies.click()
        randsleep(3, 1)


def find_games():
    """
    Filter claimable freebies.
    """
    API = ''.join([
        'https://store-site-backend-static.ak.epicgames.com/',
        'freeGamesPromotions?locale=en-US',
        '&country=%(country)s',
        '&allowCountries=%(country)s'
    ]) % r.get(
        'https://ipinfo.io').json()
    data = r.get(API).json()['data']['Catalog']['searchStore']['elements']
    free_games = []

    for each in data:
        datecomp, pricecomp, vouchcomp = False, False, False
        start, end = None, None
        prices = each['price']['totalPrice']
        now = datetime.utcnow()
        if each['promotions'] and len(each['promotions']['promotionalOffers']) > 0:
            start = datetime.strptime(
                next(
                    iter(
                        next(iter(each['promotions']['promotionalOffers']))
                        ['promotionalOffers']))['startDate'],
                '%Y-%m-%dT%H:%M:%S.%fZ')
        if len(next(iter(each['price']['lineOffers']))['appliedRules']) > 0:
            end = datetime.strptime(
                next(iter(
                    next(iter(each['price']['lineOffers']))['appliedRules']))
                ['endDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
        elif each['promotions'] and len(each['promotions']['promotionalOffers']) > 0:
            end = datetime.strptime(
                next(
                    iter(
                        next(iter(each['promotions']['promotionalOffers']))
                        ['promotionalOffers']))['endDate'],
                '%Y-%m-%dT%H:%M:%S.%fZ')

        if start and end:
            datecomp = now > start and now < end
        pricecomp = prices['originalPrice'] == prices['discount']
        vouchcomp = prices['discountPrice'] == prices['voucherDiscount']
        if datecomp and (pricecomp and vouchcomp
                         or prices['originalPrice'] == 0):
            free_games.append({
                'name':
                each['title'],
                'slug':
                each['productSlug'],
                'type':
                'product' if any(i['path'] == 'freegames'
                                 for i in each['categories']) else 'bundles'
            })
    return free_games


def find_user(browser):
    """
    Find logged in users name.
    """
    WebDriverWait(browser, 600).until(
        EC.presence_of_element_located((By.ID, 'user')))
    return browser.find_element_by_xpath(
        '''//*[@id="user"]//a/span''').text.lower().replace(' ', '')


def login(browser):
    """
    Ask user to log in.
    """
    notif = Notify.Notification.new("Epic Games")
    notif.set_urgency(Notify.Urgency.LOW)
    notif.set_timeout(Notify.EXPIRES_NEVER)
    user = find_user(browser)
    if user == "signin" and 'HEADLESS' in environ.keys(
    ) and environ['HEADLESS'] == '1':
        notif.update("Epic Games", "You have to log in to Epic Store.",
                     "face-plain")
        notif.show()
        log.error(
            ' '.join([
                "You have to log in to Epic Store.",
                "Run 'epic-claim login' to log in."
            ])
        )
        raise Break
    if 'login' in sys.argv or user == "signin":
        loop = GLib.MainLoop()
        notif.update(
            "Epic Games",
            "Login to epic store now, then click on this notification.",
            "face-uncertain")
        notif.show()
        notif.connect('closed', lambda x: loop.quit())
        print("Login to epic store now, then click on the notification.")
        loop.run()


def config_browser():
    """
    Configure and return a chromedriver.
    """
    profile_path = Path(environ['HOME']).joinpath(".config/epic-auto")

    if not path.isdir(profile_path):
        sys.argv.append('login')

    _options = ChromeOptions()
    _options.add_argument(f"user-data-dir={profile_path}")

    if 'HEADLESS' in environ.keys() and environ['HEADLESS'] == '1':
        _options.headless = True
    return Chrome(options=_options)


def load_store(browser):
    """
    Load store.
    """
    store = '''https://www.epicgames.com/store/'''
    try:
        log.log(15, "Loading Store")
        browser.get(store)

        WebDriverWait(browser, 600).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="dieselReactWrapper"]')))
        log.log(15, "Finding free games")
    except TimeoutException:
        log.error("Operation timed out")
        globals()['TMOUT'] = True
    except Break:
        pass
    except Exception as _e:
        print(_e)


# MAIN #
if __name__ == '__main__':
    _browser = config_browser()

    if 'HEADLESS' in environ.keys() and environ['HEADLESS'] == '1':
        _browser.minimize_window()
    remove('chromedriver')

    CLAIMED = 0
    load_store(_browser)
    login(_browser)

    for n in find_games():
        log.log(15, 'Opening \'%s\'', n['name'])
        try:
            if get_game(n, _browser):
                CLAIMED += 1
        except TimeoutException:
            log.error("Operation timed out")
        except Break:
            pass
        except Exception as _e:
            print(_e)
            break
    if CLAIMED > 0:
        log.info('Finalizing bot')
    _browser.close()
    if TMOUT:
        sys.exit(1)
