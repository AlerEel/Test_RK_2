from playwright.sync_api import sync_playwright, expect
import json
import time
import random
from parser_v2 import main as run_parser_v2

TARGET_URL = "https://dom.gosuslugi.ru/inspection/api/rest/services/examinations/public/search?page=1&itemsPerPage=10"


def extract_headers(request):
    headers_to_extract = {
        "user-agent": None,
        "content-type": None,
        "referer": None,
        "origin": None,
        "session-guid": None,
        "state-guid": None,
        "request-guid": None,
        "cookie": None
    }
    for name, value in request.headers.items():
        lname = name.lower()
        if lname in headers_to_extract:
            headers_to_extract[lname] = value
    print("[INFO] Headers extracted:")
    return headers_to_extract


def try_get_headers(max_attempts=3):
    """
    Пытается получить заголовки с повторными попытками
    """
    for attempt in range(max_attempts):
        print(f"[INFO] Попытка {attempt + 1}/{max_attempts} получения заголовков...")
        
        with sync_playwright() as p:
            try:
                print("[STAGE 1] Запуск браузера и переход на сайт...")
                browser = p.chromium.launch(headless=True)
            except Exception as e:
                print(f"[ERROR] Не удалось запустить браузер Playwright: {e}")
                if attempt < max_attempts - 1:
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    print(f"[INFO] Ждем {delay:.1f} секунд перед повторной попыткой...")
                    time.sleep(delay)
                    continue
                else:
                    return None
            
            page = browser.new_page()
            try:
                page.goto("https://dom.gosuslugi.ru/#!/rp", wait_until="domcontentloaded", timeout=30000)
            except Exception as e:
                print(f"[ERROR] Не удалось открыть сайт: {e}")
                browser.close()
                if attempt < max_attempts - 1:
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    print(f"[INFO] Ждем {delay:.1f} секунд перед повторной попыткой...")
                    time.sleep(delay)
                    continue
                else:
                    return None

            try:
                page.wait_for_selector("button:has-text('Найти')", timeout=15000)
            except Exception:
                print("❌ Кнопка 'Найти' не найдена")
                browser.close()
                if attempt < max_attempts - 1:
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    print(f"[INFO] Ждем {delay:.1f} секунд перед повторной попыткой...")
                    time.sleep(delay)
                    continue
                else:
                    return None

            headers_captured = {}
            def handle_route(route, request):
                nonlocal headers_captured
                if request.url == TARGET_URL and request.method == "POST":
                    print("[STAGE 2] Найден нужный POST-запрос. Извлекаем заголовки...")
                    headers_captured = extract_headers(request)
                    route.continue_()
                else:
                    route.continue_()

            page.route("**/*", handle_route)
            print("[STAGE 3] Кликаем по кнопке 'Найти'...")
            
            try:
                page.click("button:has-text('Найти')")
                page.wait_for_timeout(10000)  # Увеличиваем время ожидания
            except Exception as e:
                print(f"[ERROR] Ошибка при клике по кнопке: {e}")
                browser.close()
                if attempt < max_attempts - 1:
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    print(f"[INFO] Ждем {delay:.1f} секунд перед повторной попыткой...")
                    time.sleep(delay)
                    continue
                else:
                    return None
            
            browser.close()

            if headers_captured:
                print("[SUCCESS] Заголовки успешно получены!")
                return headers_captured
            else:
                print("[WARNING] Заголовки не были получены в этой попытке")
                if attempt < max_attempts - 1:
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    print(f"[INFO] Ждем {delay:.1f} секунд перед повторной попыткой...")
                    time.sleep(delay)
                    continue
    
    return None


def main():
    headers_captured = try_get_headers()
    
    if headers_captured:
        print("[STAGE 4] Передаём заголовки в parser_v2.py и запускаем основной парсинг...")
        run_parser_v2(headers_captured)
    else:
        print("[ERROR] Не удалось получить заголовки для запроса после всех попыток!")

if __name__ == "__main__":
    main()