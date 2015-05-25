import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SeleniumHelper():
    def __init__(self, selected_driver='Firefox'):
        self.selected_input = False
        try:
            driver = getattr(webdriver, selected_driver)
            self.driver = driver()
            print(bcolors.OKGREEN+"Using driver "+selected_driver+bcolors.ENDC)
        except:
            print(bcolors.FAIL+"There is no driver "+selected_driver +
                  bcolors.ENDC)

    def __getattr__(self, method):
        try:
            driver_method = getattr(self.driver, method)
            driver_method()
        except:
            print(bcolors.FAIL+'There is no method '+method+' in the driver' +
                  bcolors.ENDC)

    def go_to(self, url):
        print self.driver
        print url
        self.driver.get(url)

    def get_dom(self, dom_selector, return_type=False):
        return_str = ""

        if return_type:
            return_str = "s"

        if type(dom_selector) is WebElement:
            return self.test_if_exists(dom_selector)
        elif type(dom_selector) is list:
            print "finding by "+dom_selector[0]+" : "+dom_selector[1]
            dom_finder = getattr(self.driver,
                                 'find_element'+return_str+'_by_' +
                                 dom_selector[0])
            selected_dom = dom_finder(dom_selector[1])
            selector_string = dom_selector[0]+' : '+dom_selector[1]
        elif type(dom_selector) is str:
            dom_finder = getattr(self.driver,
                                 'find_element'+return_str +
                                 '_by_css_selector')
            selected_dom = dom_finder(dom_selector)
            selector_string = 'css selector : '+dom_selector

        self.test_if_exists(selected_dom)
        print(bcolors.OKGREEN+'"'+selector_string+'" FOUND !'+bcolors.ENDC)
        return selected_dom

    def test_if_exists(self, dom_element):
        end_time = time.time() + 2
        while True:
            try:
                tested_element = dom_element
                return tested_element
            except NoSuchElementException, e:
                print(bcolors.FAIL+e+bcolors.ENDC)
                return False
            if time.time() > end_time:
                break


    def wait(self, duration):
        self.driver.implicitly_wait(duration)

    def wait_page_to_complete(self, element_id):
        try:
            WebDriverWait(self.driver, 18)\
                .until(EC.presence_of_element_located((By.ID, element_id)))
            print "Page is ready!"
        except TimeoutException:
            print "Loading took too much time!"

    def ajax_complete(self, driver):
        try:
            return 0 == self.driver.execute_script("return jQuery.active")
        except WebDriverException, e:
            print e

    def wait_for_ajax(self):
        WebDriverWait(self.driver, 10).until(
            self.ajax_complete,  "Timeout waiting for page to load")

    def click(self, dom_element):
        selected_dom = self.get_dom(dom_element)
        selected_dom.click()

    def click_wait_id(self, dom_element, id_to_check):
        self.click(dom_element)
        self.wait_page_to_complete(id_to_check)

    def click_ajax(self, dom_element):
        self.click(dom_element)
        self.wait_for_ajax()

    def write(self, dom_element, text):
        selected_dom = self.get_dom(dom_element)
        print(bcolors.OKBLUE+'Writing : '+text+bcolors.ENDC)
        selected_dom.send_keys(text)
        self.selected_input = selected_dom

    def clear(self, selector):
        dom_element = self.get_dom(selector)
        dom_element.clear()

    def get_text(self, dom_element):
        selected_dom = self.get_dom(dom_element)
        return selected_dom.text

    def get_attr(self, dom_element, attr):
        selected_dom = self.get_dom(dom_element)
        return selected_dom.get_attribute(attr)

    def select(self, dom_element, selected_option):
        selected_dom = self.get_dom(dom_element)
        select = Select(selected_dom)
        select.select_by_visible_text(selected_option)
        self.selected_input = selected_dom

    def submit(self):
        try:
            selected_input = self.selected_input
            selected_input.submit()
        except:
            print("submit only works if an input/select field has\
                    been interacted with in this form.\
                    You can use click(<css_selector>) instead.")
