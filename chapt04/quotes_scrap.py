import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://quotes.toscrape.com/")

    wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "footer")
        )
    )

    login_link = wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Login")
        )
    )
    login_link.click()

    username_input = wait.until(
        EC.presence_of_element_located(
            (By.ID, "username")
        )
    )

    password_input = driver.find_element(
        By.ID, "password"
    )

    username_input.send_keys("admin")
    password_input.send_keys("admin")

    login_button = driver.find_element(
        By.CSS_SELECTOR,
        'input[type="submit"]'
    )
    login_button.click()

    wait.until(
        EC.presence_of_element_located(
            (By.LINK_TEXT, "Logout")
        )
    )

    print("로그인 성공: 작업 시작")

    rows = []

    for page_num in range(1, 101):
        print(f"{page_num} 페이지 수집")

        quotes = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".quote")
            )
        )

        for quote in quotes:
            text = quote.find_element(
                By.CSS_SELECTOR, ".text"
            ).text

            author = quote.find_element(
                By.CSS_SELECTOR, ".author"
            ).text

            link = quote.find_element(
                By.CSS_SELECTOR, "span a"
            ).get_attribute("href")

            tags = quote.find_elements(
                By.CSS_SELECTOR, ".tags > a"
            )
            tag_text = ", ".join(
                tag.text for tag in tags
            )

            rows.append({
                "text": text,
                "author": author,
                "link": link,
                "tags": tag_text
            })

        next_buttons = driver.find_elements(
            By.CSS_SELECTOR,
            "li.next a"
        )

        if not next_buttons:
            break

        next_buttons[0].click()

    df_quotes = pd.DataFrame(rows)

    df_quotes.to_csv(
        "../data/quotes_to_scrap_50.csv",
        encoding="utf-8",
        index=False
    )

    print("파일 저장 완료!")

    logout_link = driver.find_element(
        By.LINK_TEXT,
        "Logout"
    )
    logout_link.click()

    print("로그아웃 완료")

except Exception as e:
    print("실행 중 오류 발생:", e)

finally:
    driver.quit()