#!/usr/bin/env python3
"""
TestGPT 啟動腳本
"""

import os
import sys
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def check_dependencies():
    """檢查依賴套件"""
    required_packages = [
        'flask',
        'openai',
        'groq',
        'python-dotenv',
        'selenium',
        'pytest'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下依賴套件:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n請執行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依賴套件已安裝")
    return True

def check_environment():
    """檢查環境設定"""
    required_env_vars = [
        'OPENAI_API_KEY',
        'GROQ_API_KEY'
    ]
    
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  缺少以下環境變數:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n請複製 env.example 為 .env 並填入您的 API 金鑰")
        return False
    
    print("✅ 環境變數設定完成")
    return True

def main():
    """主函數"""
    print("🚀 TestGPT - AI-driven Test Case Generator")
    print("=" * 50)
    
    # 檢查依賴
    if not check_dependencies():
        sys.exit(1)
    
    # 檢查環境
    if not check_environment():
        print("\n💡 提示: 如果您沒有 API 金鑰，可以:")
        print("   1. 註冊 OpenAI 帳號: https://platform.openai.com/")
        print("   2. 註冊 Groq 帳號: https://console.groq.com/")
        print("   3. 將 API 金鑰添加到 .env 檔案中")
        print("\n即使沒有 API 金鑰，您仍可以測試其他功能")
    
    # 啟動應用程式
    print("\n🌐 啟動 Web 應用程式...")
    print("   網址: http://localhost:5000")
    print("   按 Ctrl+C 停止")
    print("-" * 50)
    
    try:
        from app import app
        app.run(
            host='0.0.0.0',
            port=int(os.getenv('PORT', 5000)),
            debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
        )
    except KeyboardInterrupt:
        print("\n👋 應用程式已停止")
    except Exception as e:
        print(f"\n❌ 啟動失敗: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 