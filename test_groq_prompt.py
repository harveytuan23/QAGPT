#!/usr/bin/env python3
"""
測試 Groq API 指令
展示實際發送給 Groq 的完整指令內容
"""

import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def show_groq_prompt():
    """展示實際發送給 Groq 的指令"""
    
    # 模擬實際的輸入
    description = "我要測試登入功能，需要帳號密碼欄位，按下登入後導向 Dashboard"
    test_type = "functional"
    
    # 建立完整的 prompt
    base_prompt = f"""
請為以下功能生成詳細的測試用例：

功能描述：{description}

測試類型：{test_type}

請生成包含以下類型的測試用例：
1. 正向測試（正常流程）
2. 負向測試（錯誤處理）
3. 邊界值測試
4. 異常情況測試

請以 JSON 格式回應，格式如下：
{{
    "test_cases": [
        {{
            "id": "TC001",
            "title": "測試標題",
            "description": "測試描述",
            "type": "positive|negative|boundary|exception",
            "steps": [
                "步驟1",
                "步驟2",
                "步驟3"
            ],
            "expected_result": "預期結果",
            "priority": "high|medium|low"
        }}
    ]
}}

請確保測試用例涵蓋所有重要的功能點和可能的錯誤情況。
"""
    
    # 根據測試類型調整 prompt
    if test_type == 'functional':
        base_prompt += "\n重點：功能正確性測試"
    
    # 完整的 messages 結構
    messages = [
        {
            "role": "system", 
            "content": "你是一個專業的軟體測試工程師，專門生成高品質的測試用例。"
        },
        {
            "role": "user", 
            "content": base_prompt
        }
    ]
    
    print("🚀 實際發送給 Groq 的完整指令")
    print("=" * 60)
    print()
    
    print("📋 API 調用參數：")
    print(f"Model: llama3-8b-8192 (或其他 Groq 模型)")
    print(f"Temperature: 0.7")
    print(f"Max Tokens: 2000")
    print()
    
    print("💬 System Message:")
    print("-" * 30)
    print(messages[0]["content"])
    print()
    
    print("💬 User Message:")
    print("-" * 30)
    print(messages[1]["content"])
    print()
    
    print("📊 完整的 messages 結構：")
    print("-" * 30)
    import json
    print(json.dumps(messages, ensure_ascii=False, indent=2))
    print()
    
    print("🔍 實際的 API 調用：")
    print("-" * 30)
    print("groq_client.chat.completions.create(")
    print("    model='llama3-8b-8192',")
    print("    messages=messages,")
    print("    temperature=0.7,")
    print("    max_tokens=2000")
    print(")")
    print()
    
    # 檢查 API 金鑰
    groq_api_key = os.getenv('GROQ_API_KEY')
    if groq_api_key and groq_api_key != 'your_groq_api_key_here':
        print("✅ Groq API 金鑰已設定")
        print(f"金鑰前綴: {groq_api_key[:10]}...")
    else:
        print("⚠️  Groq API 金鑰未設定或使用預設值")
        print("請在 .env 檔案中設定您的 Groq API 金鑰")
    
    print()
    print("=" * 60)

if __name__ == '__main__':
    show_groq_prompt() 