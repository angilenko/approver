from abc import abstractmethod
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from settings import DEBUG, SELENOID_HOST, SELENOID_PORT, SUPPLIERS_AUTH


class Approver:
    """
    Базовый класс для "подписи" заказа через b2b поставщика.

    Под процедурой "подписи" подразумевается команда поставщику отгружать заказ
    (точка невозврата, после которой заказ отменить нельзя).

    Некоторые поставщики не предоставляют API для "подписи" заказа. Согласно их
    бизнес-логике она осуществляется либо собственный менеджером, либо менеджером
    нашей компании через b2b. Так алгоритм обработки заказов допускает корректировки,
    подпись должно осуществляться менеджером нашей компании.
    """

    login = None
    password = None
    domain = None

    supplier_name = None
    # название поставщика (ключ в словаре `SUPPLIERS_AUTH`)

    def __init__(self, order_id):
        """
        :param order_id: идентификатор заказа в системе поставщика
        """

        if DEBUG:
            self.browser = webdriver.Chrome()
        else:
            self.browser = webdriver.Remote(
                command_executor=f'http://{SELENOID_HOST}:{SELENOID_PORT}/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME
            )
        self.order_id = order_id
        self.login = SUPPLIERS_AUTH[self.supplier_name]['login']
        self.password = SUPPLIERS_AUTH[self.supplier_name]['password']

    def __del__(self):
        self.browser.quit()

    @abstractmethod
    def auth(self):
        """
        Выполняет авторизацию в b2b поставщика.
        """

        raise NotImplementedError

    @abstractmethod
    def find_order(self):
        """
        Выполняет поиск заказа в b2b поставщика и переход на страницу "подписи".
        """

        raise NotImplementedError

    @abstractmethod
    def approve(self):
        """
        Выполняет "подпись" заказа.
        """

        raise NotImplementedError

    @abstractmethod
    def logout(self):
        """
        Выполняет выход из b2b поставщика.
        """

        raise NotImplementedError

    def run(self):
        self.auth()
        self.find_order()
        self.approve()
        self.logout()
