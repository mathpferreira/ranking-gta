from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

def main():
    url = "https://www.gtatorcidas.net/forum/"

    # Configura o Chrome em modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)

    driver.get(url)
    time.sleep(5)  # espera a tabela carregar

    # Caminho absoluto para salvar na raiz do repositório
    output_path = os.path.join(os.getcwd(), "ranking.png")

    driver.save_screenshot(output_path)
    print(f"✅ Screenshot salva em: {output_path}")

    driver.quit()

if __name__ == "__main__":
    main()
