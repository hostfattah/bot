import sys, time, json
from art import text2art
from termcolor import colored
from datetime import datetime
from selenium import webdriver
from termcolor import colored
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Tampilan awal
ascii_art = text2art("Facebook")
color_art = colored(ascii_art, color='light_red')
print(color_art)
today = datetime.now()
print(colored(today.strftime('%A, %d %B %Y'), "light_green").center(62))
print(53 * "-")

# About Author
print(colored("Author\t  : Khaeril Anwar", "light_blue"))
print(colored("Telegram  : https://t.me/khaerilanwr", "light_blue"))
print(colored("Github\t  : https://github.com/khaerilanwar", "light_blue"))
print(colored("Youtube\t  : https://www.youtube.com/@khaerilanwarr", "light_blue"))
print(53 * "-")

# Pilih Browser
print(colored("Pilih Metode Login", "light_yellow"))
print(colored(53 * "-", "light_magenta"))
print(colored("1. Cookies", "light_green"))
print(colored("2. Kredensial", "light_green"))
print(colored(53 * "-", "light_magenta"))
login_method = input(colored("Metode login [1/2]\t: ", "light_blue"))

# Menerima inputan data
print(colored(53 * "-", "light_magenta"))
print(colored("Isi Data Berikut!", "light_yellow").center(62))
if login_method == "2":
    email = input(colored("Email Facebook\t\t: ", "light_yellow"))
    password = input(colored("Kata Sandi Facebook\t: ", "light_yellow"))

link_post = input(colored("Link Post\t\t: ", "light_yellow"))
komentar = input(colored("Komentar\t\t: ", "light_yellow"))

try:
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    if login_method == "1":
        driver.get("https://web.facebook.com/")
        time.sleep(5)
        # Mengecek jika ada file cookies
        with open("cookies.json", "r") as f:
            cookies = json.load(f)
            for cookie in cookies:
                # Melakukan replace value sameSite
                # Karena value sameSite di selenium adalah
                # ["Strict", "Lax", "None"] 
                for (key, value) in cookie.items():
                    if key == "sameSite":
                        if value == "no_restriction" or  value == "unspecified":
                            cookie[key] = "None"
                        elif value == "lax":
                            cookie[key] = "Lax"

                # Menambahkan cookie ke browser
                driver.add_cookie(cookie)
        
        print(colored("Berhasil login via cookies!", "light_green"))
    elif login_method == "2":
        # LOGIN KE AKUN FACEBOOK
        driver.get("https://web.facebook.com/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email'))).send_keys(email)
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'pass'))).send_keys(password)
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'login'))).click()
        time.sleep(5)

        print(colored("Berhasil login!", "light_green"))

    # Masuk link postingan
    driver.get(link_post)
    time.sleep(5)
    body = driver.find_element(By.TAG_NAME, 'body')
    # body.send_keys(Keys.PAGE_DOWN)

    # Memulai komentar
    button_coment = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Beri komentar"][role="button"]')))
    button_coment.click()

    input_comment = driver.switch_to.active_element
    input_comment.send_keys(komentar)
    input_comment.send_keys(Keys.ENTER)

    print(colored("Komentar berhasil dikirim!", "light_green"))

    driver.quit()
except Exception as e:
    print(colored(f"Error: {e}", "red"))