from selenium_helper import SeleniumHelper

login = 'admin'
password = 'admin'
band_test_name = "This is my testing band"

sh = SeleniumHelper('Firefox')
sh.go_to("http://127.0.0.1:6543/")


def connect():
    sh.click("#connection_button")
    sh.write("#username", login)
    sh.write("#password", password)
    sh.submit()


def go_to_dash_board():
    connect()
    sh.click_ajax("#dashboard_button")


def create_band():
    go_to_dash_board()
    existing_band = sh.get_text('.dashboard_title')
    sh.click_ajax('#dashboard_add_band')

    country_search()
    sh.write('#band_picture', '/home/tumulte/Systeme/mutant_enemy.jpg')
    test_markdown("#wmd-input_0")
    sh.write("#band_since", "2015-03-30")
    test_duplicate_band(existing_band)
    sh.clear("#band_name")
    sh.write("#band_name", band_test_name)
    sh.click(["name", "simple_submit"])


def test_markdown(markdown_area):
    dummy_text = "Hello world !"
    sh.write(markdown_area, dummy_text)
    assert sh.get_text("#wmd-preview_0") == dummy_text


def country_search():
    sh.select("#country", 'France')
    sh.write(".city_search", "Lyon")
    sh.wait(2)
    sh.click(".city_suggestion")

    assert sh.get_attr('#Location-latitude_0', 'value') != ''
    assert sh.get_attr('#Location-longitude_0', 'value') != ''


def test_duplicate_band(existing_band):
    sh.write("#band_name", existing_band)
    sh.submit()
    sh.wait(5)
    assert sh.get_attr('#band_name', 'class') == 'invalid'


def edit_band():
    edit_button = sh.get(['xpath', "//h1[contains(text(), '"+band_test_name+"')]/following-sibling::a[@class='dashboard_edit_link']"])
    sh.select("#country", 'Spain')
    sh.write(".city_search", "Madrid")
    sh.wait(2)
    sh.click(".city_suggestion")
    assert sh.get_attr('#Location-latitude_0', 'value') != ''
    assert sh.get_attr('#Location-longitude_0', 'value') != ''

    sh.write('#band_picture', '/home/tumulte/Systeme/mutant_enemy.jpg')
    dummy_text = "Hello world again !"
    sh.write(markdown_area, dummy_text)
    assert sh.get_text("#wmd-preview_0") == dummy_text
    sh.write("#band_since", "2014-04-02")
    sh.click(["name", "simple_submit"])
    edit_button[0].click_ajax()



def delete_band():
    sh.click_ajax("#remove_band")
    inputs = sh.get(['xpath',  "//input[@type='text']"], 'list')
    for field in inputs:
        field.write('ok')
    sh.submit()


def logout():
    sh.click('#logout')

create_band()
edit_band()
#logout()
#driver.close()
