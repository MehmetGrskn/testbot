from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import time

# ChromeDriver yolu
service = Service("C:\\Users\\mehme\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)


# Siteye git
driver.get("https://gisis.imo.org/Public/MCIR/Search.aspx")

wait = WebDriverWait(driver, 200)

# Kelime grupları
event_keywords = [
    "Engine malfunction",
    "Power loss",
    "Engine breakdown",
    "Mechanical failure",
    "System malfunction",
    "Power system failure",
    "Auxiliary engine failure",
    "Turbocharger failure",
    "Fuel system failure",
    "Propeller failure",
    "Ship power failure",
    "Generator failure",
    "Emergency shutdown",
    "Motor failure",
    "Main engine failure",
    "Vibration issues",
    "Thermal failure",
    "Overheating engine",
    "Electrical malfunction",
    "Fuel contamination"
]


# Dropdown menüsünü seçme (Select kullanarak)
dropdown = wait.until(EC.presence_of_element_located((By.ID, "ctl00_cpMain_ddlAuthorityType")))
select = Select(dropdown)
print("Dropdown menüsü bulundu.")
time.sleep(1)

# "Public Users" seçeneğini seçme
select.select_by_visible_text("Public Users")
print("Public Users seçeneği seçildi.")
time.sleep(1)



print("username alanı seçilecek")
# Username input alanını bekle ve doldur
username_input = wait.until(EC.presence_of_element_located((By.ID, "ctl00_cpMain_txtUsername")))
username_input.send_keys("barbosa")  # Buraya gerçek kullanıcı adını yaz
print("Username alanı dolduruldu.")
time.sleep(1)

# Next butonunu bekle ve tıkla
next_button = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_cpMain_btnNext")))
next_button.click()
print("Next butonuna tıklandı.")
time.sleep(5)

# Şifre alanını bul ve doldur
password_input = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_cpMain_txtPassword")))
password_input.send_keys("Jklopcd2")  # buraya şifreni yaz
print("Şifre alanı dolduruldu.")
time.sleep(1)

# Log In butonuna tıkla
login_button = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_cpMain_btnLogin")))
login_button.click()

print("Log In butonuna tıklandı.")
time.sleep(5)

for keyword in event_keywords:

    print("show additional alanı seçilecek")
    # Show additional fields butonuna tıklama - class ismini kullanarak
    show_fields_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "tipsterise.cursorpointer")))
    show_fields_button.click()
    print("Show additional fields butonuna tıklandı.")
    time.sleep(1)

    # Summary of events input alanını bul ve kelimeyi yaz
    summary_input = wait.until(EC.presence_of_element_located((By.ID, "ctl00_bodyPlaceHolder_Search_tbEventsSummary")))
    summary_input.clear()  # Önceki metni temizle
    summary_input.send_keys(keyword)  # Kelimeyi gir

    # Search butonuna tıklama
    search_button = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_bodyPlaceHolder_Search_btnSearch")))
    search_button.click()
    print(f"Arama yapıldı: {keyword}")
    time.sleep(3)  # Arama sonuçlarının yüklenmesi için bekleyin

    # Download butonuna tıklama
    download_button = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_bodyPlaceHolder_Search_gridResults_gridResults_ctl01_btnDlCustom")))
    download_button.click()
    print(f"{keyword} için Download butonuna tıklandı.")
    time.sleep(7)  # Dosya indirilmesi için yeterli süre ver

    # Geri tuşuna basma
    driver.back()
    print(f"{keyword} için geri tuşuna basıldı.")
    time.sleep(2)  # Sayfa geri yüklenmesi için biraz bekle


time.sleep(25)


