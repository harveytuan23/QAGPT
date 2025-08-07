"""
Fuzz 測試器
生成異常資料測試用例
"""

import random
import string
from typing import List, Dict, Any

class FuzzTester:
    """Fuzz 測試器"""
    
    def __init__(self):
        self.fuzz_patterns = {
            'empty': '',
            'null': None,
            'very_long': 'a' * 10000,
            'special_chars': '!@#$%^&*()_+-=[]{}|;:,.<>?',
            'unicode': '测试数据🎉🚀💻',
            'sql_injection': "' OR 1=1 --",
            'xss': '<script>alert("xss")</script>',
            'numbers': '1234567890',
            'spaces': '   ',
            'newlines': '\n\r\t',
            'negative': '-123',
            'decimal': '123.456',
            'scientific': '1.23e+10'
        }
    
    def generate_fuzz_tests(self, fields: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """生成 Fuzz 測試用例"""
        fuzz_tests = []
        
        for field in fields:
            field_name = field.get('name', 'unknown_field')
            field_type = field.get('type', 'text')
            
            # 為每個欄位生成多種 Fuzz 測試
            for pattern_name, pattern_value in self.fuzz_patterns.items():
                test_case = {
                    'id': f"FUZZ_{field_name}_{pattern_name}",
                    'title': f"Fuzz 測試 - {field_name} ({pattern_name})",
                    'description': f"對 {field_name} 欄位進行 {pattern_name} 測試",
                    'type': 'fuzz',
                    'field_name': field_name,
                    'field_type': field_type,
                    'fuzz_pattern': pattern_name,
                    'fuzz_value': pattern_value,
                    'steps': [
                        f"打開測試頁面",
                        f"在 {field_name} 欄位輸入異常值: {pattern_value}",
                        f"提交表單",
                        f"驗證系統處理異常輸入的反應"
                    ],
                    'expected_result': "系統應該正確處理異常輸入，不崩潰或洩露敏感資訊",
                    'priority': 'high'
                }
                fuzz_tests.append(test_case)
        
        return fuzz_tests
    
    def generate_random_fuzz_value(self, field_type: str = 'text') -> Any:
        """生成隨機 Fuzz 值"""
        if field_type == 'email':
            return self._generate_fuzz_email()
        elif field_type == 'number':
            return self._generate_fuzz_number()
        elif field_type == 'date':
            return self._generate_fuzz_date()
        else:
            return self._generate_fuzz_text()
    
    def _generate_fuzz_email(self) -> str:
        """生成異常的電子郵件格式"""
        patterns = [
            'test@',  # 不完整的郵箱
            '@test.com',  # 缺少用戶名
            'test..test@test.com',  # 連續點
            'test@test@test.com',  # 多個 @
            'test test@test.com',  # 包含空格
            'test@test..com',  # 域名中有連續點
            'test@test',  # 缺少頂級域名
            'test@.com',  # 缺少域名
            'test@test.c',  # 不完整的頂級域名
            'test@test.com.',  # 結尾有點
        ]
        return random.choice(patterns)
    
    def _generate_fuzz_number(self) -> str:
        """生成異常的數字格式"""
        patterns = [
            'abc',  # 非數字
            '12.34.56',  # 多個小數點
            '1,234,567',  # 包含逗號
            '1e999',  # 極大數
            '-0',  # 負零
            '0.0.0',  # 多個小數點
            '1/0',  # 除零
            'NaN',  # 非數字
            'Infinity',  # 無窮大
            '-Infinity',  # 負無窮大
        ]
        return random.choice(patterns)
    
    def _generate_fuzz_date(self) -> str:
        """生成異常的日期格式"""
        patterns = [
            '2023-13-01',  # 無效月份
            '2023-12-32',  # 無效日期
            '2023/12/01',  # 不同分隔符
            '01-12-2023',  # 不同順序
            '2023-12-01 25:00:00',  # 無效時間
            '2023-12-01T25:00:00',  # 無效 ISO 格式
            'invalid-date',  # 無效字串
            '2023-00-01',  # 零月份
            '2023-12-00',  # 零日期
            '9999-12-31',  # 極遠日期
        ]
        return random.choice(patterns)
    
    def _generate_fuzz_text(self) -> str:
        """生成異常的文字格式"""
        patterns = [
            '',  # 空字串
            '   ',  # 只有空格
            '\n\r\t',  # 控制字符
            'a' * 10000,  # 極長字串
            '🎉🚀💻',  # Unicode 表情
            '<script>alert("xss")</script>',  # XSS
            "' OR 1=1 --",  # SQL 注入
            'test<script>alert("xss")</script>test',  # 混合內容
            'test' + '\x00' + 'test',  # 包含 null 字符
            'test' + '\x1f' + 'test',  # 包含控制字符
        ]
        return random.choice(patterns) 