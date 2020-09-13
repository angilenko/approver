from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from approver.base import Approver


class OCSApprover(Approver):
    url = 'https://b2b.ocs.ru/'
    supplier_name = 'ocs'
    default_timeout = 20

    def auth(self):
        self.browser.get(f'{self.url}login/')

        login_input = self.browser.find_element_by_id('username')
        login_input.send_keys(self.login)

        password_input = self.browser.find_element_by_id('password')
        password_input.send_keys(self.password)

        self.browser.find_element_by_css_selector('button[type=submit]').submit()
        self.browser.refresh()

        WebDriverWait(self.browser, self.default_timeout).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, 'cu-top-menu')
            )
        )

    def find_order(self):
        self.browser.get(f'{self.url}order/{self.order_id}/shipment')
        WebDriverWait(self.browser, self.default_timeout).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//button[contains(., "Добавить все в отгрузку")]')
            )
        ).click()

    def approve(self):
        WebDriverWait(self.browser, self.default_timeout).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class, "button-success") and contains(text(), "Отгрузить")]')
            )
        ).click()
        WebDriverWait(self.browser, self.default_timeout).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//button[contains(@class, "button-orange") and contains(text(), "Отгрузить")]')
            )
        ).click()
        WebDriverWait(self.browser, self.default_timeout).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, '//button[contains(text(), "Закрыть")]')
            )
        ).click()

    def logout(self):
        self.browser\
            .find_element_by_css_selector('button[title="Завершить работу в B2B"]')\
            .click()
