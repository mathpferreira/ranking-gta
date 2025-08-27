from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

URL = "https://www.webcup.com.br/campeonato/campeonato-de-cf-global-2025---gta-torcidas-1754250411"

def main():
    options = Options()
    options.add_argument("--headless")  # roda sem abrir janela
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)  # resolução grande

    print("🔄 Acessando o Webcup...")
    driver.get(URL)
    time.sleep(5)  # espera a página carregar (pode aumentar se ficar em branco)

    driver.save_screenshot("ranking.png")
    print("✅ Screenshot completo salvo como ranking.png")

    driver.quit()

if __name__ == "__main__":
    main()
