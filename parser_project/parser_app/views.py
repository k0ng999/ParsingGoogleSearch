import logging
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

from rest_framework.response import Response
from rest_framework.views import APIView

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_google_rank(keyword: str, site_name: str):
    logging.info(f"Запуск парсинга для запроса: {keyword} и сайта: {site_name}")

    options = Options()
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"'
    )

    try:
        logging.info("Инициализация браузера Chrome")
        service = Service(os.path.join(BASE_DIR, "chromedriver.exe"))
        driver = webdriver.Chrome(service=service, options=options)

        try:
            search_url = f"https://www.google.com.au/search?num=100&q={keyword.replace(' ', '+')}"
            logging.info(f"Открытие страницы поиска: {search_url}")
            driver.get(search_url)

            time.sleep(5)

            logging.info("Поиск результатов Google")
            elements = driver.find_elements(By.CSS_SELECTOR, ".tjvcx.GvPZzd.cHaqb")
            logging.info(f"Найдено {len(elements)} результатов")
            counter = 0
            positions = []  # Список для хранения всех позиций

            for index, el in enumerate(elements):
                link = el.text.strip()
                if "https://" in link:
                    counter += 1
                else:
                    continue



                # Разделяем ссылку по пробелу или символу › и ищем только первое слово
                first_word = link.split(' › ')[0]
                logging.info(f"Позиция: {counter}, {first_word}, {positions}")

                if site_name.lower() in first_word:
                    positions.append(counter)

            logging.info(f"Финальные позиции: {positions}")

            # Форматируем числа с пробелами
            formatted_result = " ".join(map(str, positions))  # Преобразуем список чисел в строку с пробелами
            return formatted_result if formatted_result else "Нет совпадений"

        except Exception as e:
            logging.error(f"Ошибка при парсинге: {e}", exc_info=True)
            return str(e)

        finally:
            driver.quit()
            logging.info("Закрытие браузера")

    except WebDriverException as e:
        logging.error(f"Ошибка Selenium: {e}", exc_info=True)
        return str(e)


# API-контроллер
class GoogleRankAPIView(APIView):
    def post(self, request):
        keyword = request.data.get("keyword", "")
        site_name = request.data.get("site_name", "")

        if not keyword or not site_name:
            return Response({"error": "Keyword and site_name are required"}, status=400)

        result = get_google_rank(keyword, site_name)
        return Response({"result": result})
