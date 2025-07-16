from playwright.sync_api import sync_playwright, expect
import json
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


def main():
    with sync_playwright() as p:
        print("[STAGE 1] Запуск браузера и переход на сайт...")
        try:
            browser = p.chromium.launch(headless=True)
        except Exception as e:
            print(f"[ERROR] Не удалось запустить браузер Playwright: {e}", flush=True)
            return
        page = browser.new_page()
        try:
            page.goto("https://dom.gosuslugi.ru/#!/rp")
        except Exception as e:
            print(f"[ERROR] Не удалось открыть сайт: {e}", flush=True)
            browser.close()
            return

        try:
            page.wait_for_selector("button:has-text('Найти')", timeout=10000)
        except Exception:
            print("❌ Кнопка 'Найти' не найдена")
            browser.close()
            return

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
        page.click("button:has-text('Найти')")
        page.wait_for_timeout(8000)
        browser.close()

        if headers_captured:
            print("[STAGE 4] Передаём заголовки в parser_v2.py и запускаем основной парсинг...")
            run_parser_v2(headers_captured)
        else:
            print("[ERROR] Не удалось получить заголовки для запроса!")

if __name__ == "__main__":
    main()