#!/usr/bin/env python3
"""
TestGPT - AI-driven Test Case Generator
主應用程式入口點
"""

import os
from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
import json
from datetime import datetime
import uuid

# 載入環境變數
load_dotenv()

# 建立 Flask 應用程式
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# 匯入模組
from src.generators.test_case_generator import TestCaseGenerator
from src.converters.script_converter import ScriptConverter
from src.fuzz.fuzz_tester import FuzzTester
from src.models.ai_model_manager import AIModelManager
from src.exporters.test_exporter import TestExporter
from src.reports.report_generator import ReportGenerator
from src.test_runner import TestRunner

# 初始化模組
ai_manager = AIModelManager()
test_generator = TestCaseGenerator(ai_manager)
script_converter = ScriptConverter()
fuzz_tester = FuzzTester()
test_exporter = TestExporter()
report_generator = ReportGenerator()
test_runner = TestRunner()

@app.route('/')
def index():
    """首頁"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_test_cases():
    """生成測試用例"""
    try:
        data = request.get_json()
        description = data.get('description', '')
        test_type = data.get('test_type', 'functional')
        model = data.get('model', 'openai')
        template = data.get('template', '')
        
        # 根據是否使用模板生成測試用例
        if template:
            test_cases = test_generator.generate_with_template(description, template, test_type, model)
        else:
            test_cases = test_generator.generate(description, test_type, model)
        
        return jsonify({
            'success': True,
            'test_cases': test_cases,
            'message': '測試用例生成成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/convert', methods=['POST'])
def convert_to_script():
    """轉換為測試腳本"""
    try:
        data = request.get_json()
        test_cases = data.get('test_cases', [])
        framework = data.get('framework', 'pytest')
        
        # 轉換為測試腳本
        script = script_converter.convert(test_cases, framework)
        
        return jsonify({
            'success': True,
            'script': script,
            'message': '腳本轉換成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/fuzz', methods=['POST'])
def generate_fuzz_tests():
    """生成 Fuzz 測試"""
    try:
        data = request.get_json()
        fields = data.get('fields', [])
        
        # 生成 Fuzz 測試
        fuzz_tests = fuzz_tester.generate_fuzz_tests(fields)
        
        return jsonify({
            'success': True,
            'fuzz_tests': fuzz_tests,
            'message': 'Fuzz 測試生成成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/export', methods=['POST'])
def export_test_script():
    """匯出測試腳本"""
    try:
        data = request.get_json()
        script = data.get('script', '')
        filename = data.get('filename', f'test_script_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py')
        
        # 匯出測試腳本
        file_path = test_exporter.export_script(script, filename)
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/report', methods=['POST'])
def generate_report():
    """生成報告摘要"""
    try:
        data = request.get_json()
        test_cases = data.get('test_cases', [])
        
        # 生成報告
        report = report_generator.generate_report(test_cases)
        
        return jsonify({
            'success': True,
            'report': report,
            'message': '報告生成成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/models', methods=['GET'])
def get_available_models():
    """取得可用的 AI 模型"""
    try:
        models = ai_manager.get_available_models()
        return jsonify({
            'success': True,
            'models': models
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health_check():
    """健康檢查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/run-tests', methods=['POST'])
def run_tests():
    """執行測試用例"""
    try:
        data = request.get_json()
        test_cases = data.get('test_cases', [])
        
        if not test_cases:
            return jsonify({
                'success': False,
                'error': '沒有測試用例可執行'
            }), 400
        
        # 執行測試
        result = test_runner.run_all_tests(test_cases)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 確保匯出目錄存在
    os.makedirs('exports', exist_ok=True)
    
    # 啟動應用程式
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 8080)),
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    ) 