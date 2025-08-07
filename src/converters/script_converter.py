"""
腳本轉換器
將測試用例轉換為可執行的 Python 測試腳本
"""

from typing import List, Dict, Any
import re

class ScriptConverter:
    """腳本轉換器"""
    
    def __init__(self):
        self.supported_frameworks = ['pytest', 'unittest', 'selenium']
    
    def convert(self, 
                test_cases: List[Dict[str, Any]], 
                framework: str = 'pytest') -> str:
        """轉換測試用例為測試腳本"""
        
        if framework not in self.supported_frameworks:
            raise ValueError(f"不支援的測試框架: {framework}")
        
        if framework == 'pytest':
            return self._convert_to_pytest(test_cases)
        elif framework == 'unittest':
            return self._convert_to_unittest(test_cases)
        elif framework == 'selenium':
            return self._convert_to_selenium(test_cases)
    
    def _convert_to_pytest(self, test_cases: List[Dict[str, Any]]) -> str:
        """轉換為 Pytest 格式"""
        
        script = """#!/usr/bin/env python3
\"\"\"
自動生成的測試腳本
使用 Pytest 框架
\"\"\"

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class TestGeneratedCases:
    \"\"\"自動生成的測試類別\"\"\"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        \"\"\"測試設置\"\"\"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        yield
        self.driver.quit()
    
"""
        
        for i, test_case in enumerate(test_cases):
            script += self._generate_pytest_method(test_case, i)
        
        return script
    
    def _convert_to_unittest(self, test_cases: List[Dict[str, Any]]) -> str:
        """轉換為 unittest 格式"""
        
        script = """#!/usr/bin/env python3
\"\"\"
自動生成的測試腳本
使用 unittest 框架
\"\"\"

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class TestGeneratedCases(unittest.TestCase):
    \"\"\"自動生成的測試類別\"\"\"
    
    def setUp(self):
        \"\"\"測試設置\"\"\"
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
    
    def tearDown(self):
        \"\"\"測試清理\"\"\"
        self.driver.quit()
    
"""
        
        for i, test_case in enumerate(test_cases):
            script += self._generate_unittest_method(test_case, i)
        
        script += """
if __name__ == '__main__':
    unittest.main()
"""
        
        return script
    
    def _convert_to_selenium(self, test_cases: List[Dict[str, Any]]) -> str:
        """轉換為 Selenium 格式"""
        
        script = """#!/usr/bin/env python3
\"\"\"
自動生成的 Selenium 測試腳本
\"\"\"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def run_tests():
    \"\"\"執行所有測試\"\"\"
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    
    try:
"""
        
        for i, test_case in enumerate(test_cases):
            script += self._generate_selenium_function(test_case, i)
        
        script += """
    finally:
        driver.quit()

if __name__ == '__main__':
    run_tests()
"""
        
        return script
    
    def _generate_pytest_method(self, test_case: Dict[str, Any], index: int) -> str:
        """生成 Pytest 測試方法"""
        
        method_name = self._sanitize_method_name(test_case.get('title', f'test_case_{index}'))
        
        script = f"""
    def test_{method_name}(self):
        \"\"\"
        {test_case.get('description', '測試用例')}
        類型: {test_case.get('type', 'unknown')}
        優先級: {test_case.get('priority', 'medium')}
        \"\"\"
        try:
"""
        
        # 添加測試步驟
        steps = test_case.get('steps', [])
        if not steps:
            # 如果沒有步驟，根據類型生成基本步驟
            steps = self._generate_default_steps(test_case)
        
        for step in steps:
            script += f"            # {step}\n"
            script += self._convert_step_to_selenium(step)
        
        # 添加預期結果驗證
        expected_result = test_case.get('expected_result', '')
        if expected_result:
            script += f"            # 驗證預期結果: {expected_result}\n"
            script += self._generate_assertion(expected_result)
        
        script += """
        except Exception as e:
            pytest.fail(f"測試失敗: {{e}}")
"""
        
        return script
    
    def _generate_unittest_method(self, test_case: Dict[str, Any], index: int) -> str:
        """生成 unittest 測試方法"""
        
        method_name = self._sanitize_method_name(test_case.get('title', f'test_case_{index}'))
        
        script = f"""
    def test_{method_name}(self):
        \"\"\"
        {test_case.get('description', '測試用例')}
        類型: {test_case.get('type', 'unknown')}
        優先級: {test_case.get('priority', 'medium')}
        \"\"\"
        try:
"""
        
        # 添加測試步驟
        steps = test_case.get('steps', [])
        if not steps:
            steps = self._generate_default_steps(test_case)
        
        for step in steps:
            script += f"            # {step}\n"
            script += self._convert_step_to_selenium(step)
        
        # 添加預期結果驗證
        expected_result = test_case.get('expected_result', '')
        if expected_result:
            script += f"            # 驗證預期結果: {expected_result}\n"
            script += self._generate_assertion(expected_result)
        
        script += """
        except Exception as e:
            self.fail(f"測試失敗: {{e}}")
"""
        
        return script
    
    def _generate_selenium_function(self, test_case: Dict[str, Any], index: int) -> str:
        """生成 Selenium 測試函數"""
        
        function_name = self._sanitize_method_name(test_case.get('title', f'test_case_{index}'))
        
        script = f"""
        # {test_case.get('description', '測試用例')}
        # 類型: {test_case.get('type', 'unknown')}
        # 優先級: {test_case.get('priority', 'medium')}
        try:
"""
        
        # 添加測試步驟
        steps = test_case.get('steps', [])
        if not steps:
            steps = self._generate_default_steps(test_case)
        
        for step in steps:
            script += f"            # {step}\n"
            script += self._convert_step_to_selenium(step)
        
        # 添加預期結果驗證
        expected_result = test_case.get('expected_result', '')
        if expected_result:
            script += f"            # 驗證預期結果: {expected_result}\n"
            script += self._generate_assertion(expected_result)
        
        script += """
            print(f"✅ {test_case.get('title', '測試用例')} - 通過")
        except Exception as e:
            print(f"❌ {test_case.get('title', '測試用例')} - 失敗: {{e}}")
"""
        
        return script
    
    def _sanitize_method_name(self, name: str) -> str:
        """清理方法名稱，使其符合 Python 命名規範"""
        # 移除特殊字符，只保留字母、數字和下劃線
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        # 確保不以數字開頭
        if sanitized and sanitized[0].isdigit():
            sanitized = 'test_' + sanitized
        # 確保不以底線開頭
        if sanitized.startswith('_'):
            sanitized = 'test' + sanitized
        return sanitized.lower()
    
    def _generate_default_steps(self, test_case: Dict[str, Any]) -> List[str]:
        """根據測試類型生成預設步驟"""
        test_type = test_case.get('type', 'positive')
        title = test_case.get('title', '').lower()
        
        if '登入' in title or 'login' in title:
            if test_type == 'positive':
                return [
                    "打開登入頁面",
                    "輸入正確的用戶名",
                    "輸入正確的密碼",
                    "點擊登入按鈕"
                ]
            else:
                return [
                    "打開登入頁面",
                    "輸入錯誤的用戶名或密碼",
                    "點擊登入按鈕"
                ]
        elif '註冊' in title or 'register' in title:
            if test_type == 'positive':
                return [
                    "打開註冊頁面",
                    "填寫所有必填欄位",
                    "點擊註冊按鈕"
                ]
            else:
                return [
                    "打開註冊頁面",
                    "填寫不完整的資訊",
                    "點擊註冊按鈕"
                ]
        else:
            return [
                "打開測試頁面",
                "執行測試操作",
                "驗證結果"
            ]
    
    def _convert_step_to_selenium(self, step: str) -> str:
        """將測試步驟轉換為 Selenium 代碼"""
        
        step_lower = step.lower()
        
        if '打開' in step or 'open' in step:
            return """            self.driver.get("http://localhost:3000")  # 請修改為實際的測試URL
            time.sleep(1)
"""
        elif '輸入' in step or 'input' in step:
            if '用戶名' in step or 'username' in step:
                return """            username_input = self.driver.find_element(By.ID, "username")
            username_input.clear()
            username_input.send_keys("testuser")
"""
            elif '密碼' in step or 'password' in step:
                return """            password_input = self.driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys("testpass")
"""
            else:
                return """            # 請根據實際情況修改元素定位
            input_element = self.driver.find_element(By.ID, "input_field")
            input_element.clear()
            input_element.send_keys("test_input")
"""
        elif '點擊' in step or 'click' in step:
            if '登入' in step or 'login' in step:
                return """            login_button = self.driver.find_element(By.ID, "login-button")
            login_button.click()
            time.sleep(2)
"""
            elif '註冊' in step or 'register' in step:
                return """            register_button = self.driver.find_element(By.ID, "register-button")
            register_button.click()
            time.sleep(2)
"""
            else:
                return """            # 請根據實際情況修改元素定位
            button = self.driver.find_element(By.ID, "button")
            button.click()
            time.sleep(1)
"""
        else:
            return """            # 請根據實際情況實現此步驟
            time.sleep(1)
"""
    
    def _generate_assertion(self, expected_result: str) -> str:
        """根據預期結果生成斷言"""
        
        expected_lower = expected_result.lower()
        
        if '導向' in expected_result or 'redirect' in expected_result:
            return """            # 驗證頁面跳轉
            assert "dashboard" in self.driver.current_url or "home" in self.driver.current_url
"""
        elif '錯誤' in expected_result or 'error' in expected_result:
            return """            # 驗證錯誤訊息
            error_element = self.driver.find_element(By.CLASS_NAME, "error-message")
            assert error_element.is_displayed()
"""
        elif '成功' in expected_result or 'success' in expected_result:
            return """            # 驗證成功訊息
            success_element = self.driver.find_element(By.CLASS_NAME, "success-message")
            assert success_element.is_displayed()
"""
        else:
            return """            # 請根據實際情況添加驗證邏輯
            assert True  # 臨時斷言，請替換為實際驗證
""" 