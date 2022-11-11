import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from twilio.rest import Client
from selenium.webdriver.chrome.options import Options


load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
url = "https://shop.flipperzero.one/collections/all/products/flipper-zero"


def test_message():
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body='Hello there from Twilio SMS API',
            from_=+18438944352,
            to=+16463150805
        )
    print(message.sid)


def main_message():
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body=f'FLIPPER ZERO IN STOCK! Please BUY NOW: {url}',
            from_=+18438944352,
            to=+16463150805
        )
    print(message.sid)


def snipe():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("./chromedriver", options=chrome_options)
    test_message()
    driver.get(url)

    purchase_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="addToCartCopy"]'))
    )

    while purchase_button.text == "SOLD OUT":
        driver.refresh()
        purchase_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="addToCartCopy"]')))
        if purchase_button.text != "SOLD OUT":
            main_message()
            break
    if purchase_button.text != "SOLD OUT":
        main_message()


if __name__ == "__main__":
    snipe()