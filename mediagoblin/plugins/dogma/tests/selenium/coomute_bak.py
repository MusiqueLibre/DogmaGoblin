from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

login = 'admin'
password = 'admin'
band_test_name = "This is my testing band"

driver = webdriver.Firefox()
#driver = webdriver.PhantomJS()
# driver.get("http://www.coomute.net")
print driver
driver.get("http://127.0.0.1:6543/")



def wait_page_to_complete(element_id):
    try:
        WebDriverWait(driver, 18).until(EC.presence_of_element_located((By.ID, element_id)))
        print "Page is ready!"
    except TimeoutException:
        print "Loading took too much time!"


def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException, e:
        print e

def wait_for_ajax():
    WebDriverWait(driver, 10).until(
                 ajax_complete,  "Timeout waiting for page to load")



def test_if_exists(dom_element):
    try:
        tested_element = dom_element
    except NoSuchElementException, e:
        print e
        tested_element = False
    return tested_element


def connect():
    login_link = test_if_exists(driver.find_element_by_id("connection_button"))
    login_link.click()
    wait_for_ajax()
    login_field = test_if_exists(driver.find_element_by_name("username"))
    login_pass = test_if_exists(driver.find_element_by_id("password"))
    login_field.send_keys(login)
    login_pass.send_keys(password)
    login_pass.send_keys(Keys.RETURN)


def go_to_dash_board():
    connect()
    dashboard = test_if_exists(driver.find_element_by_id("dashboard_button"))
    dashboard.click()
    wait_for_ajax()


def create_band(submit_and_continue=False, test_duplicate=True):
    go_to_dash_board()
    existing_band = test_if_exists(driver.find_element_by_class_name('dashboard_title'))
    existing_band = existing_band.text
    add_band = test_if_exists(driver.find_element_by_id("dashboard_add_band"))
    add_band.click()
    wait_for_ajax()

    country_search()
    picture = test_if_exists(driver.find_element_by_id("band_picture"))
    picture.send_keys('/home/tumulte/Systeme/mutant_enemy.jpg')
    markdown_area = test_if_exists(driver.find_element_by_id("wmd-input_0"))
    test_markdown(markdown_area)
    date = test_if_exists(driver.find_element_by_id("band_since"))
    date.send_keys("2015-03-30")
    if test_duplicate:
        test_duplicate_band(existing_band)
    band_name_field = test_if_exists(driver.find_element_by_id("band_name"))
    band_name_field.clear()
    band_name_field.send_keys(band_test_name)
    if(submit_and_continue):
        submit = test_if_exists(driver.find_element_by_name("submit_and_continue"))
    else:
        submit = test_if_exists(driver.find_element_by_name("simple_submit"))


    submit.click()


def test_markdown(markdown_area):
    dummy_text = "Hello world !"
    markdown_area.send_keys(dummy_text)
    markdown_preview = test_if_exists(driver.find_element_by_id("wmd-preview_0"))

    assert markdown_preview.text == dummy_text, markdown_preview.text


def country_search():
    select = Select(test_if_exists(driver.find_element_by_id("country")))
    select.select_by_visible_text('France')
    city_search = test_if_exists(driver.find_element_by_class_name("city_search"))
    city_search.send_keys("Lyon")
    driver.implicitly_wait(2)
    city_suggestion = test_if_exists(driver.find_element_by_class_name("city_suggestion"))
    city_suggestion.click()

    latitude = test_if_exists(driver.find_element_by_id('Location-latitude_0'))
    longitude = test_if_exists(driver.find_element_by_id('Location-latitude_0'))
    assert latitude is not None
    assert longitude is not None


def test_duplicate_band(existing_band):
    band_name_field = test_if_exists(driver.find_element_by_id("band_name"))
    band_name_field.send_keys(existing_band)
    band_name_field.send_keys(Keys.RETURN)
    driver.implicitly_wait(5)
    band_name_field = test_if_exists(driver.find_element_by_id("band_name"))
    assert band_name_field.get_attribute('class') == 'invalid'


def edit_band(delete=False):
    edit_button = test_if_exists(driver.find_elements_by_xpath("//h1[contains(text(), '"+band_test_name+"')]/following-sibling::a[@class='dashboard_edit_link']"))
    edit_button[0].click()
    wait_for_ajax()
    if delete:
        delete_band()
    else:
        pass


def delete_band():
    remove_button = test_if_exists(driver.find_element_by_id("remove_band"))
    remove_button.click()
    wait_for_ajax()
    inputs = test_if_exists(driver.find_elements_by_xpath("//input[@type='text']"))
    for field in inputs:
        field.send_keys('ok')
    inputs[-1].send_keys(Keys.RETURN)


def logout():
    logout = test_if_exists(driver.find_element_by_id("logout"))
    logout.click()

create_band()
wait_page_to_complete('dashboard_add_band')
edit_band(True)
#logout()
#driver.close()
