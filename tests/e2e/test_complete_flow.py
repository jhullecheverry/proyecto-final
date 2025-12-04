import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


@pytest.fixture
def driver():
    """Configura el driver de Selenium"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


class TestCompleteFlow:
    """Pruebas E2E del flujo completo del sistema"""

    def test_home_page_loads(self, driver):
        """Prueba que la página de inicio carga correctamente"""
        FRONTEND_URL = "http://localhost:3000"

        try:
            driver.get(FRONTEND_URL)

            # Esperar a que cargue el título
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h2"))
            )

            # Verificar título de la página
            assert "Sistema de Inventario" in driver.title or "Inventario" in driver.title

            # Verificar que hay contenido en la página
            body = driver.find_element(By.TAG_NAME, "body")
            assert len(body.text) > 0

            print("✓ Página de inicio cargada correctamente")

        except Exception as e:
            print(f"Error en test_home_page_loads: {str(e)}")
            driver.save_screenshot("error_home_page.png")
            raise

    def test_navigation_between_pages(self, driver):
        """Prueba la navegación entre páginas"""
        FRONTEND_URL = "http://localhost:3000"

        try:
            driver.get(FRONTEND_URL)

            # Esperar a que cargue la navegación
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "navbar"))
            )

            # Navegar a categorías
            categories_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Categorías"))
            )
            categories_link.click()

            # Verificar URL
            WebDriverWait(driver, 10).until(
                lambda d: "/categories" in d.current_url
            )
            assert "/categories" in driver.current_url

            # Navegar a productos
            products_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Productos"))
            )
            products_link.click()

            # Verificar URL
            WebDriverWait(driver, 10).until(
                lambda d: "/products" in d.current_url
            )
            assert "/products" in driver.current_url

            # Volver a inicio
            home_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Inicio"))
            )
            home_link.click()

            # Verificar URL
            WebDriverWait(driver, 10).until(
                lambda d: d.current_url.endswith("/") or d.current_url.endswith(":3000")
            )

            print("✓ Navegación entre páginas exitosa")

        except Exception as e:
            print(f"Error en test_navigation_between_pages: {str(e)}")
            driver.save_screenshot("error_navigation.png")
            raise

    def test_complete_user_flow(self, driver):
        """
        Prueba el flujo completo:
        1. Crear una categoría
        2. Crear un producto
        3. Visualizar el producto en el listado
        """

        FRONTEND_URL = "http://localhost:3000"
        CATEGORY_NAME = f"Electrónica E2E {int(time.time())}"  # Nombre único
        PRODUCT_NAME = f"Laptop E2E {int(time.time())}"

        try:
            # PASO 1: IR A CATEGORÍAS
            driver.get(f"{FRONTEND_URL}/categories")

            # Esperar a que cargue el formulario
            wait = WebDriverWait(driver, 15)

            name_input = wait.until(
                EC.presence_of_element_located((By.ID, "category-name"))
            )

            # PASO 2: CREAR CATEGORÍA
            name_input.clear()
            name_input.send_keys(CATEGORY_NAME)

            submit_btn = driver.find_element(By.ID, "submit-btn")
            submit_btn.click()

            # Esperar a que se procese (mensaje de éxito o actualización de tabla)
            time.sleep(3)

            # Verificar que aparece en la tabla
            try:
                table_body = driver.find_element(By.ID, "categories-list")
                assert CATEGORY_NAME in table_body.text, f"Categoría '{CATEGORY_NAME}' no encontrada en la tabla"
                print(f"✓ Categoría '{CATEGORY_NAME}' creada exitosamente")
            except AssertionError:
                # Si no aparece inmediatamente, recargar la página
                driver.refresh()
                time.sleep(2)
                table_body = driver.find_element(By.ID, "categories-list")
                assert CATEGORY_NAME in table_body.text, f"Categoría '{CATEGORY_NAME}' no encontrada después de recargar"

            # PASO 3: IR A PRODUCTOS
            driver.get(f"{FRONTEND_URL}/products")

            # Esperar a que cargue el formulario de productos
            product_name_input = wait.until(
                EC.presence_of_element_located((By.ID, "product-name"))
            )

            # PASO 4: CREAR PRODUCTO
            product_name_input.clear()
            product_name_input.send_keys(PRODUCT_NAME)

            # Seleccionar categoría
            category_select = wait.until(
                EC.presence_of_element_located((By.ID, "product-category"))
            )

            # Esperar a que las opciones se carguen
            time.sleep(2)

            # Buscar la categoría que acabamos de crear
            options = category_select.find_elements(By.TAG_NAME, "option")
            category_found = False
            for option in options:
                if CATEGORY_NAME in option.text:
                    option.click()
                    category_found = True
                    break

            assert category_found, f"Categoría '{CATEGORY_NAME}' no encontrada en el select"

            # Llenar precio
            price_input = driver.find_element(By.ID, "product-price")
            price_input.clear()
            price_input.send_keys("1500")

            # Llenar stock
            stock_input = driver.find_element(By.ID, "product-stock")
            stock_input.clear()
            stock_input.send_keys("10")

            # Llenar descripción
            description_input = driver.find_element(By.ID, "product-description")
            description_input.clear()
            description_input.send_keys("Laptop de prueba E2E")

            # Enviar formulario
            submit_btn = driver.find_element(By.ID, "submit-btn")
            submit_btn.click()

            # Esperar a que se procese
            time.sleep(3)

            # PASO 5: VERIFICAR QUE EL PRODUCTO APARECE EN LA TABLA
            try:
                products_table = driver.find_element(By.ID, "products-list")
                table_text = products_table.text

                assert PRODUCT_NAME in table_text, f"Producto '{PRODUCT_NAME}' no encontrado en la tabla"
                assert "1500" in table_text, "Precio no encontrado en la tabla"
                assert CATEGORY_NAME in table_text, f"Categoría '{CATEGORY_NAME}' no encontrada en la tabla"

                print(f"✓ Producto '{PRODUCT_NAME}' creado exitosamente")
                print(f"✓ Producto visible en el listado con todos los datos correctos")

            except AssertionError:
                # Si no aparece, recargar
                driver.refresh()
                time.sleep(2)
                products_table = driver.find_element(By.ID, "products-list")
                table_text = products_table.text
                assert PRODUCT_NAME in table_text, f"Producto '{PRODUCT_NAME}' no encontrado después de recargar"

            print("✓ Flujo E2E completado exitosamente")

        except TimeoutException as e:
            print(f"Timeout esperando elemento: {str(e)}")
            print(f"URL actual: {driver.current_url}")
            print(f"HTML de la página:")
            print(driver.page_source[:500])  # Primeros 500 caracteres
            driver.save_screenshot("error_timeout.png")
            raise

        except NoSuchElementException as e:
            print(f"Elemento no encontrado: {str(e)}")
            print(f"URL actual: {driver.current_url}")
            driver.save_screenshot("error_element_not_found.png")
            raise

        except Exception as e:
            print(f"Error inesperado en test_complete_user_flow: {str(e)}")
            print(f"URL actual: {driver.current_url}")
            driver.save_screenshot("error_complete_flow.png")
            raise