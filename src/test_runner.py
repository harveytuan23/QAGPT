"""
測試執行器 - 使用 Selenium 自動執行測試用例
"""

import time
import json
from typing import List, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

class TestRunner:
    """測試執行器"""
    
    def __init__(self, test_url: str = "http://localhost:5001"):
        self.test_url = test_url
        self.driver = None
        self.results = []
        
    def setup_driver(self):
        """設置 WebDriver"""
        try:
            chrome_options = Options()
            # chrome_options.add_argument("--headless")  # 移除無頭模式
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1200,800")
            chrome_options.add_argument("--start-maximized")  # 最大化視窗
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            return True
        except Exception as e:
            print(f"設置 WebDriver 失敗: {e}")
            return False
    
    def teardown_driver(self):
        """清理 WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def run_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """執行單個測試用例"""
        result = {
            'id': test_case.get('id', 'Unknown'),
            'title': test_case.get('title', 'Unknown'),
            'type': test_case.get('type', 'unknown'),
            'success': False,
            'error': None,
            'execution_time': 0,
            'steps_results': []
        }
        
        start_time = time.time()
        
        try:
            # 導航到測試頁面
            print(f"🧪 開始執行測試: {test_case.get('title', 'Unknown')}")
            self.driver.get(self.test_url)
            time.sleep(1)  # 等待頁面載入
            
            # 執行測試步驟
            steps = test_case.get('steps', [])
            for i, step in enumerate(steps):
                print(f"  步驟 {i + 1}: {step}")
                step_result = self.execute_step(step, i + 1)
                result['steps_results'].append(step_result)
                
                # 如果步驟失敗，停止執行
                if not step_result['success']:
                    result['error'] = f"步驟 {i + 1} 失敗: {step_result['error']}"
                    print(f"  ❌ 步驟失敗: {step_result['error']}")
                    break
                else:
                    print(f"  ✅ 步驟成功")
            
            # 檢查預期結果
            expected_result = test_case.get('expected_result', '')
            if expected_result:
                result['success'] = self.verify_expected_result(expected_result)
                print(f"  預期結果: {expected_result} - {'✅ 通過' if result['success'] else '❌ 失敗'}")
            
            result['execution_time'] = time.time() - start_time
            print(f"  執行時間: {result['execution_time']:.2f}秒")
            
        except Exception as e:
            result['error'] = str(e)
            result['execution_time'] = time.time() - start_time
            print(f"  ❌ 測試執行錯誤: {e}")
        
        return result
    
    def execute_step(self, step: str, step_number: int) -> Dict[str, Any]:
        """執行單個測試步驟"""
        step_result = {
            'step_number': step_number,
            'step': step,
            'success': False,
            'error': None
        }
        
        try:
            # 根據步驟內容執行相應操作
            if '輸入' in step or 'enter' in step.lower():
                if '用戶名' in step or 'username' in step.lower():
                    self.input_username(step)
                elif '密碼' in step or 'password' in step.lower():
                    self.input_password(step)
                else:
                    self.input_text(step)
                    
            elif '點擊' in step or 'click' in step.lower() or '按下' in step:
                if '登入' in step or 'login' in step.lower():
                    self.click_login()
                else:
                    self.click_element(step)
                    
            elif '驗證' in step or 'verify' in step.lower() or '檢查' in step:
                self.verify_element(step)
                
            elif '等待' in step or 'wait' in step.lower():
                self.wait_for_element(step)
                
            else:
                # 通用步驟處理
                self.execute_generic_step(step)
            
            step_result['success'] = True
            
        except Exception as e:
            step_result['error'] = str(e)
        
        return step_result
    
    def input_username(self, step: str):
        """輸入用戶名"""
        try:
            # 提取用戶名（假設格式為 "輸入用戶名 admin"）
            username = self.extract_value_from_step(step)
            if not username:
                username = "admin"  # 預設值
            
            username_field = self.driver.find_element(By.ID, "username")
            username_field.clear()
            
            # 逐字輸入，讓您看到輸入過程
            for char in username:
                username_field.send_keys(char)
                time.sleep(0.1)  # 每個字符間隔 0.1 秒
            
        except NoSuchElementException:
            raise Exception("找不到用戶名輸入欄位")
    
    def input_password(self, step: str):
        """輸入密碼"""
        try:
            # 提取密碼
            password = self.extract_value_from_step(step)
            if not password:
                password = "password123"  # 預設值
            
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            
            # 逐字輸入，讓您看到輸入過程
            for char in password:
                password_field.send_keys(char)
                time.sleep(0.1)  # 每個字符間隔 0.1 秒
            
        except NoSuchElementException:
            raise Exception("找不到密碼輸入欄位")
    
    def click_login(self):
        """點擊登入按鈕"""
        try:
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
            # 高亮顯示按鈕
            self.driver.execute_script("arguments[0].style.border='3px solid red'", login_button)
            time.sleep(0.5)
            
            login_button.click()
            
            # 等待登入結果
            time.sleep(2)
            
        except NoSuchElementException:
            raise Exception("找不到登入按鈕")
    
    def verify_element(self, step: str):
        """驗證元素"""
        try:
            if '成功' in step or 'success' in step.lower():
                # 檢查是否出現成功訊息
                success_elements = self.driver.find_elements(By.CLASS_NAME, "alert-success")
                if not success_elements:
                    raise Exception("未找到成功訊息")
                    
            elif '錯誤' in step or 'error' in step.lower():
                # 檢查是否出現錯誤訊息
                error_elements = self.driver.find_elements(By.CLASS_NAME, "alert-danger")
                if not error_elements:
                    raise Exception("未找到錯誤訊息")
                    
            elif '登入成功' in step:
                # 檢查是否跳轉到成功頁面
                success_page = self.driver.find_element(By.ID, "successPage")
                if success_page.is_displayed():
                    return
                else:
                    raise Exception("未跳轉到成功頁面")
                    
        except NoSuchElementException:
            raise Exception("驗證元素失敗")
    
    def wait_for_element(self, step: str):
        """等待元素出現"""
        try:
            # 簡單的等待
            time.sleep(2)
        except Exception as e:
            raise Exception(f"等待元素失敗: {e}")
    
    def execute_generic_step(self, step: str):
        """執行通用步驟"""
        # 根據步驟內容執行相應操作
        if '按 Enter' in step or 'press enter' in step.lower():
            from selenium.webdriver.common.keys import Keys
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ENTER)
        else:
            # 預設等待
            time.sleep(1)
    
    def extract_value_from_step(self, step: str) -> str:
        """從步驟中提取值"""
        # 簡單的文本提取邏輯
        if 'admin' in step.lower():
            return 'admin'
        elif 'test' in step.lower():
            return 'test'
        elif 'password123' in step:
            return 'password123'
        elif 'test123' in step:
            return 'test123'
        else:
            return ""
    
    def verify_expected_result(self, expected_result: str) -> bool:
        """驗證預期結果"""
        try:
            if '成功' in expected_result or 'success' in expected_result.lower():
                # 檢查成功狀態
                success_elements = self.driver.find_elements(By.CLASS_NAME, "alert-success")
                return len(success_elements) > 0
                
            elif '錯誤' in expected_result or 'error' in expected_result.lower():
                # 檢查錯誤狀態
                error_elements = self.driver.find_elements(By.CLASS_NAME, "alert-danger")
                return len(error_elements) > 0
                
            elif '登入成功' in expected_result:
                # 檢查是否在成功頁面
                try:
                    success_page = self.driver.find_element(By.ID, "successPage")
                    return success_page.is_displayed()
                except:
                    return False
                    
            return True
            
        except Exception:
            return False
    
    def run_all_tests(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """執行所有測試用例"""
        print("🚀 開始執行自動測試...")
        print(f"📝 測試頁面: {self.test_url}")
        print(f"🧪 總測試用例數: {len(test_cases)}")
        print("=" * 50)
        
        if not self.setup_driver():
            print("❌ 無法設置 WebDriver")
            return {
                'success': False,
                'error': '無法設置 WebDriver',
                'results': []
            }
        
        try:
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n📋 測試用例 {i}/{len(test_cases)}")
                result = self.run_test_case(test_case)
                self.results.append(result)
                print("-" * 30)
            
            # 統計結果
            total_tests = len(self.results)
            passed_tests = sum(1 for r in self.results if r['success'])
            failed_tests = total_tests - passed_tests
            
            print("\n" + "=" * 50)
            print("📊 測試執行完成！")
            print(f"✅ 通過: {passed_tests}")
            print(f"❌ 失敗: {failed_tests}")
            print(f"📈 成功率: {(passed_tests / total_tests * 100):.1f}%")
            print("=" * 50)
            
            return {
                'success': True,
                'summary': {
                    'total_tests': total_tests,
                    'passed_tests': passed_tests,
                    'failed_tests': failed_tests,
                    'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
                },
                'results': self.results
            }
            
        except Exception as e:
            print(f"❌ 測試執行過程中出現錯誤: {e}")
            return {
                'success': False,
                'error': str(e),
                'results': self.results
            }
        finally:
            print("🧹 清理 WebDriver...")
            self.teardown_driver()
            print("✅ 清理完成") 