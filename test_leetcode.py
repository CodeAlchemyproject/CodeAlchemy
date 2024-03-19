from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
import json

def get_all_titles():
    # 使用 Selenium 模擬瀏覽器動作
    driver = webdriver.Chrome()
    driver.get("https://leetcode.com/api/problems/all/")

    slugs = []

    try:
        # 等待頁面載入
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "pre"))
        )

        # 獲取 JSON 數據
        json_data = driver.find_element_by_tag_name("pre").text

        # 解析 JSON
        r_json = json.loads(json_data)

        # 提取標題
        for slug in r_json["stat_status_pairs"]:
            slugs.append(slug["stat"]["question__title_slug"])

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()  # 爬取完畢後關閉瀏覽器

    return slugs
# 測試函數
# titles = get_all_titles()
# print(titles)
