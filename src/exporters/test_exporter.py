"""
測試腳本匯出器
將生成的測試腳本匯出為檔案
"""

import os
from datetime import datetime
from typing import Optional

class TestExporter:
    """測試腳本匯出器"""
    
    def __init__(self, export_path: str = './exports'):
        self.export_path = export_path
        os.makedirs(export_path, exist_ok=True)
    
    def export_script(self, script: str, filename: str) -> str:
        """匯出測試腳本"""
        file_path = os.path.join(self.export_path, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(script)
        
        return file_path
    
    def export_with_metadata(self, 
                           script: str, 
                           test_cases: list,
                           framework: str = 'pytest') -> str:
        """匯出包含元資料的測試腳本"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_script_{framework}_{timestamp}.py"
        
        # 添加元資料註解
        metadata = self._generate_metadata(test_cases, framework)
        full_script = metadata + "\n" + script
        
        return self.export_script(full_script, filename)
    
    def _generate_metadata(self, test_cases: list, framework: str) -> str:
        """生成元資料註解"""
        lines = []
        lines.append('"""')
        lines.append('自動生成的測試腳本')
        lines.append(f'框架: {framework}')
        lines.append(f'生成時間: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        lines.append(f'測試用例數量: {len(test_cases)}')
        lines.append('')
        lines.append('測試用例摘要:')
        lines.append('"""')
        
        for i, test_case in enumerate(test_cases, 1):
            lines.append('')
            lines.append(f'# {i}. {test_case.get("title", "未命名測試")}')
            lines.append(f'#   類型: {test_case.get("type", "unknown")}')
            lines.append(f'#   優先級: {test_case.get("priority", "medium")}')
            lines.append(f'#   描述: {test_case.get("description", "無描述")}')
            lines.append(f'#   預期結果: {test_case.get("expected_result", "無預期結果")}')
        
        lines.append('')
        lines.append('"""')
        lines.append('使用說明:')
        lines.append('1. 請根據實際情況修改測試 URL 和元素定位')
        lines.append('2. 確保已安裝所需的依賴套件')
        lines.append('3. 執行測試: python test_script.py')
        lines.append('"""')
        
        return '\n'.join(lines) 