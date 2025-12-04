import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    """Configura el driver de Selenium"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


class TestCompleteFlow:
    """Pruebas E2E del flujo completo del sistema"""

    def test_complete_user_flow(self, driver):
        """
        Prueba el flujo completo:
        1. Crear una categoría
        2. Crear un producto
        3. Visualizar el producto en el listado
        """

        FRONTEND_URL = "http://localhost:3000"

        driver.get(f"{FRONTEND_URL}/categories")

        wait = WebDriverWait(driver, 10)

        name_input = wait.until(
            EC.presence_of_element_located((By.ID, "category-name"))
        )
        name_input.send_keys("Electrónica E2E")

        submit_btn = driver.find_element(By.ID, "submit-btn")
        submit_btn.click()

        time.sleep(2)

        table_body = driver.find_element(By.ID, "categories-list")
        assert "Electrónica E2E" in table_body.text

        driver.get(f"{FRONTEND_URL}/products")

        wait.until(EC.presence_of_element_located((By.ID, "product-name")))

        driver.find_element(By.ID, "product-name").send_keys("Laptop E2E")

        category_select = driver.find_element(By.ID, "product-category")
        options = category_select.find_elements(By.TAG_NAME, "option")
        for option in options:
            if "Electrónica E2E" in option.text:
                option.click()
                break

        driver.find_element(By.ID, "product-price").send_keys("1500")
        driver.find_element(By.ID, "product-stock").send_keys("10")
        driver.find_element(By.ID, "product-description").send_keys(
            "Laptop de prueba E2E"
        )

        submit_btn = driver.find_element(By.ID, "submit-btn")
        submit_btn.click()

        time.sleep(2)

        products_table = driver.find_element(By.ID, "products-list")
        assert "Laptop E2E" in products_table.text
        assert "1500" in products_table.text
        assert "Electrónica E2E" in products_table.text

        print("✓ Flujo E2E completado exitosamente")

    def test_home_page_loads(self, driver):
        """Prueba que la página de inicio carga correctamente"""
        FRONTEND_URL = "http://localhost:3000"
        driver.get(FRONTEND_URL)

        assert "Sistema de Inventario" in driver.title

        hero = driver.find_element(By.CLASS_NAME, "hero")
        assert "Bienvenido" in hero.text

    def test_navigation_between_pages(self, driver):
        """Prueba la navegación entre páginas"""
        FRONTEND_URL = "http://localhost:3000"
        driver.get(FRONTEND_URL)

        categories_link = driver.find_element(By.LINK_TEXT, "Categorías")
        categories_link.click()
        assert "/categories" in driver.current_url

        products_link = driver.find_element(By.LINK_TEXT, "Productos")
        products_link.click()
        assert "/products" in driver.current_url

        home_link = driver.find_element(By.LINK_TEXT, "Inicio")
        home_link.click()
        assert driver.current_url == f"{FRONTEND_URL}/"