"""
TestGPT 基本測試
"""

import pytest
import sys
import os

# 添加專案根目錄到 Python 路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.ai_model_manager import AIModelManager
from src.generators.test_case_generator import TestCaseGenerator
from src.converters.script_converter import ScriptConverter
from src.fuzz.fuzz_tester import FuzzTester
from src.exporters.test_exporter import TestExporter
from src.reports.report_generator import ReportGenerator

class TestAIModelManager:
    """測試 AI 模型管理器"""
    
    def test_initialization(self):
        """測試初始化"""
        manager = AIModelManager()
        assert manager is not None
    
    def test_get_available_models(self):
        """測試取得可用模型"""
        manager = AIModelManager()
        models = manager.get_available_models()
        assert isinstance(models, list)

class TestTestCaseGenerator:
    """測試測試用例生成器"""
    
    def test_initialization(self):
        """測試初始化"""
        ai_manager = AIModelManager()
        generator = TestCaseGenerator(ai_manager)
        assert generator is not None
    
    def test_build_prompt(self):
        """測試 prompt 建立"""
        ai_manager = AIModelManager()
        generator = TestCaseGenerator(ai_manager)
        prompt = generator._build_prompt("測試登入功能", "functional")
        assert "登入功能" in prompt
        assert "functional" in prompt

class TestScriptConverter:
    """測試腳本轉換器"""
    
    def test_initialization(self):
        """測試初始化"""
        converter = ScriptConverter()
        assert converter is not None
        assert 'pytest' in converter.supported_frameworks
    
    def test_sanitize_method_name(self):
        """測試方法名稱清理"""
        converter = ScriptConverter()
        assert converter._sanitize_method_name("Test Case 1") == "test_case_1"
        assert converter._sanitize_method_name("123Test") == "test_123test"
        assert converter._sanitize_method_name("_test") == "test_test"

class TestFuzzTester:
    """測試 Fuzz 測試器"""
    
    def test_initialization(self):
        """測試初始化"""
        fuzz_tester = FuzzTester()
        assert fuzz_tester is not None
        assert 'empty' in fuzz_tester.fuzz_patterns
    
    def test_generate_fuzz_tests(self):
        """測試生成 Fuzz 測試"""
        fuzz_tester = FuzzTester()
        fields = [{'name': 'username', 'type': 'text'}]
        fuzz_tests = fuzz_tester.generate_fuzz_tests(fields)
        assert len(fuzz_tests) > 0
        assert all('FUZZ_' in test['id'] for test in fuzz_tests)

class TestTestExporter:
    """測試測試匯出器"""
    
    def test_initialization(self):
        """測試初始化"""
        exporter = TestExporter()
        assert exporter is not None
    
    def test_export_script(self, tmp_path):
        """測試匯出腳本"""
        exporter = TestExporter(str(tmp_path))
        script = "print('test')"
        filename = "test.py"
        file_path = exporter.export_script(script, filename)
        assert file_path.endswith(filename)
        assert os.path.exists(file_path)

class TestReportGenerator:
    """測試報告生成器"""
    
    def test_initialization(self):
        """測試初始化"""
        generator = ReportGenerator()
        assert generator is not None
    
    def test_generate_report_empty(self):
        """測試空報告生成"""
        generator = ReportGenerator()
        report = generator.generate_report([])
        assert report['summary'] == '無測試用例'
        assert report['statistics'] == {}
    
    def test_generate_report_with_data(self):
        """測試有資料的報告生成"""
        generator = ReportGenerator()
        test_cases = [
            {
                'id': 'TC001',
                'title': '測試用例1',
                'type': 'positive',
                'priority': 'high'
            }
        ]
        report = generator.generate_report(test_cases)
        assert '總共生成了 1 個測試用例' in report['summary']
        assert report['statistics']['total_cases'] == 1

if __name__ == '__main__':
    pytest.main([__file__]) 