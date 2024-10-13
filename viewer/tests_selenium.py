from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 1. Nastavení Selenium WebDriver
driver = webdriver.Chrome()

# 2. Otevření hlavní stránky
driver.get("http://localhost:8000")  # Zadejte adresu vašeho webu

# Krok 1: Registrace nového uživatele
driver.find_element(By.LINK_TEXT, "Registrovat se").click()  # Klikněte na tlačítko Registrace
time.sleep(2)  # Počkejte na načtení stránky

# Vyplnění registračního formuláře
driver.find_element(By.NAME, "username").send_keys("testuser")
driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
driver.find_element(By.NAME, "password1").send_keys("Password123!")
driver.find_element(By.NAME, "password2").send_keys("Password123!")
driver.find_element(By.XPATH, "//button[@type='submit']").click()  # Odešlete formulář
time.sleep(2)

# Ověření, že jsme na přihlašovací stránce
assert "Přihlášení" in driver.page_source

# Krok 2: Přihlášení nově zaregistrovaného uživatele
driver.find_element(By.NAME, "username").send_keys("testuser")
driver.find_element(By.NAME, "password").send_keys("Password123!")
driver.find_element(By.XPATH, "//button[@type='submit']").click()  # Klikněte na tlačítko Přihlásit se
time.sleep(2)

# Ověření, že uživatel je přihlášen
assert "Přihlášen jako testuser" in driver.page_source

# Krok 3: Přechod do kategorie "Buy Now"
driver.find_element(By.LINK_TEXT, "Buy Now").click()  # Kliknutí na kategorii Buy Now
time.sleep(2)

# Ověření, že jsme v kategorii
assert "Buy Now" in driver.page_source

# Krok 4: Výběr položky z kategorie "Buy Now"
driver.find_element(By.XPATH, "//div[@class='buy-now-auction']//a").click()  # Klikněte na první položku
time.sleep(2)

# Ověření, že jsme na stránce detailu aukce
assert "Detail" in driver.page_source  # Ověření, že se jedná o stránku detailu aukce

# Krok 5: Přidání položky do košíku
driver.find_element(By.XPATH, "//a[text()='Přidat do košíku']").click()  # Klikněte na tlačítko Přidat do košíku
time.sleep(2)

# Ověření, že položka byla přidána do košíku
assert "Košík" in driver.page_source  # Ověřte, že uživatel vidí odkaz na košík

# Krok 6: Přechod do košíku a dokončení objednávky
driver.find_element(By.LINK_TEXT, "Košík").click()  # Klikněte na košík
time.sleep(2)

# Ověření, že jsme na stránce košíku
assert "Váš košík" in driver.page_source

# Klikněte na "Pokračovat k platbě"
driver.find_element(By.LINK_TEXT, "Pokračovat k platbě").click()
time.sleep(2)

# Ověření, že jsme na stránce platby
assert "Pokračovat k platbě" in driver.page_source

# Dokončení objednávky (simulace)
print("Test úspěšně dokončen - uživatel provedl nákup.")

# Zavření prohlížeče
driver.quit()