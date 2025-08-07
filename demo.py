#!/usr/bin/env python3
"""
TestGPT 示範腳本
展示 AI 驅動測試用例生成器的功能
"""

import requests
import json
import time

def demo_test_case_generation():
    """示範測試用例生成"""
    print("🚀 TestGPT 示範 - 測試用例生成")
    print("=" * 50)
    
    # 測試資料
    test_data = {
        "description": "我要測試登入功能，需要帳號密碼欄位，按下登入後導向 Dashboard",
        "test_type": "functional",
        "model": "gpt-4"
    }
    
    try:
        print("📝 正在生成測試用例...")
        response = requests.post(
            'http://localhost:8080/generate',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ 測試用例生成成功！")
                print(f"📊 生成了 {len(data['test_cases'])} 個測試用例")
                
                for i, test_case in enumerate(data['test_cases'], 1):
                    print(f"\n{i}. {test_case.get('title', '未命名測試')}")
                    print(f"   類型: {test_case.get('type', 'unknown')}")
                    print(f"   描述: {test_case.get('description', '無描述')}")
                    if test_case.get('expected_result'):
                        print(f"   預期結果: {test_case['expected_result']}")
                
                return data['test_cases']
            else:
                print(f"❌ 生成失敗: {data.get('error', '未知錯誤')}")
        else:
            print(f"❌ HTTP 錯誤: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 網路錯誤: {e}")
    
    return []

def demo_script_conversion(test_cases):
    """示範腳本轉換"""
    print("\n💡 示範腳本轉換")
    print("=" * 30)
    
    if not test_cases:
        print("❌ 沒有測試用例可轉換")
        return
    
    try:
        print("🔄 正在轉換為 Pytest 腳本...")
        response = requests.post(
            'http://localhost:8080/convert',
            json={
                'test_cases': test_cases,
                'framework': 'pytest'
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ 腳本轉換成功！")
                print("📄 生成的腳本片段:")
                script_lines = data['script'].split('\n')[:20]
                for line in script_lines:
                    print(f"   {line}")
                print("   ...")
            else:
                print(f"❌ 轉換失敗: {data.get('error', '未知錯誤')}")
        else:
            print(f"❌ HTTP 錯誤: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 網路錯誤: {e}")

def demo_fuzz_testing():
    """示範 Fuzz 測試"""
    print("\n⚠️ 示範 Fuzz 測試")
    print("=" * 30)
    
    # 測試欄位
    fields = [
        {'name': 'username', 'type': 'text'},
        {'name': 'password', 'type': 'text'},
        {'name': 'email', 'type': 'email'}
    ]
    
    try:
        print("🐛 正在生成 Fuzz 測試...")
        response = requests.post(
            'http://localhost:8080/fuzz',
            json={'fields': fields},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✅ Fuzz 測試生成成功！")
                print(f"📊 生成了 {len(data['fuzz_tests'])} 個 Fuzz 測試用例")
                
                for i, test in enumerate(data['fuzz_tests'][:3], 1):
                    print(f"\n{i}. {test.get('title', '未命名測試')}")
                    print(f"   欄位: {test.get('field_name', 'unknown')}")
                    print(f"   模式: {test.get('fuzz_pattern', 'unknown')}")
            else:
                print(f"❌ Fuzz 測試生成失敗: {data.get('error', '未知錯誤')}")
        else:
            print(f"❌ HTTP 錯誤: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 網路錯誤: {e}")

def demo_report_generation(test_cases):
    """示範報告生成"""
    print("\n📊 示範報告生成")
    print("=" * 30)
    
    if not test_cases:
        print("❌ 沒有測試用例可分析")
        return
    
    try:
        print("📈 正在生成報告...")
        response = requests.post(
            'http://localhost:8080/report',
            json={'test_cases': test_cases},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                report = data['report']
                print("✅ 報告生成成功！")
                print(f"📋 摘要: {report.get('summary', '無摘要')}")
                
                if 'statistics' in report:
                    stats = report['statistics']
                    print(f"📊 統計: 總共 {stats.get('total_cases', 0)} 個測試用例")
                
                if 'recommendations' in report and report['recommendations']:
                    print("💡 建議:")
                    for rec in report['recommendations'][:3]:
                        print(f"   • {rec}")
            else:
                print(f"❌ 報告生成失敗: {data.get('error', '未知錯誤')}")
        else:
            print(f"❌ HTTP 錯誤: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 網路錯誤: {e}")

def check_server_status():
    """檢查伺服器狀態"""
    try:
        response = requests.get('http://localhost:8080/health')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 伺服器運行正常 (版本: {data.get('version', 'unknown')})")
            return True
        else:
            print(f"❌ 伺服器回應異常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 無法連接到伺服器: {e}")
        return False

def main():
    """主函數"""
    print("🎯 TestGPT 功能示範")
    print("=" * 50)
    
    # 檢查伺服器狀態
    if not check_server_status():
        print("\n💡 請確保應用程式正在運行:")
        print("   source venv/bin/activate && python app.py")
        return
    
    print("\n" + "=" * 50)
    
    # 示範測試用例生成
    test_cases = demo_test_case_generation()
    
    # 示範腳本轉換
    demo_script_conversion(test_cases)
    
    # 示範 Fuzz 測試
    demo_fuzz_testing()
    
    # 示範報告生成
    demo_report_generation(test_cases)
    
    print("\n" + "=" * 50)
    print("🎉 示範完成！")
    print("🌐 您可以在瀏覽器中訪問 http://localhost:8080 來使用完整的 Web 介面")

if __name__ == '__main__':
    main() 