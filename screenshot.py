import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

URL = "https://www.webcup.com.br/campeonato/campeonato-de-cf-global-2025---gta-torcidas-1754250411"

def main():
    chromedriver_autoinstaller.install()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(5)  # espera carregar

    tabela = driver.find_element("tag name", "table")
    tabela.screenshot("public/ranking.png")

    driver.quit()

if __name__ == "__main__":
    main()
