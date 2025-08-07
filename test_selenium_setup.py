#!/usr/bin/env python3
"""
測試 Selenium 設置
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def test_selenium_setup():
    """測試 Selenium 設置"""
    print("🧪 測試 Selenium 設置...")
    
    try:
        # 設置 Chrome 選項
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # 移除無頭模式
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--start-maximized")  # 最大化視窗
        
        # 創建 WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        print("✅ WebDriver 創建成功")
        
        # 測試訪問網頁
        driver.get("http://localhost:5001")
        print("✅ 成功訪問測試頁面")
        
        # 測試查找元素
        title = driver.title
        print(f"✅ 頁面標題: {title}")
        
        # 測試查找登入表單
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        print("✅ 成功找到登入表單元素")
        
        # 測試輸入和點擊
        username_field.send_keys("admin")
        password_field.send_keys("password123")
        login_button.click()
        
        print("✅ 成功執行登入操作")
        
        # 等待結果
        time.sleep(2)
        
        # 檢查結果
        try:
            success_elements = driver.find_elements(By.CLASS_NAME, "alert-success")
            if success_elements:
                print("✅ 登入成功，找到成功訊息")
            else:
                print("⚠️ 未找到成功訊息，但操作完成")
        except:
            print("⚠️ 無法檢查結果，但操作完成")
        
        driver.quit()
        print("✅ Selenium 測試完成")
        return True
        
    except Exception as e:
        print(f"❌ Selenium 測試失敗: {e}")
        return False

if __name__ == "__main__":
    print("🚀 開始測試 Selenium 設置...")
    print("📝 請確保測試伺服器正在運行: python test_server.py")
    print("🔑 測試頁面: http://localhost:5001")
    print()
    
    success = test_selenium_setup()
    
    if success:
        print("\n🎉 Selenium 設置成功！您可以開始使用自動測試功能了。")
    else:
        print("\n❌ Selenium 設置失敗，請檢查以下項目：")
        print("1. 是否安裝了 Chrome 瀏覽器")
        print("2. 是否安裝了 ChromeDriver")
        print("3. 測試伺服器是否正在運行")
        print("4. 網路連接是否正常") 