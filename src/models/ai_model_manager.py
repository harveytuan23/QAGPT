"""
AI 模型管理器
支援 OpenAI 和 Groq 模型
"""

import os
import openai
import groq
from typing import Dict, List, Optional, Any
import json

class AIModelManager:
    """AI 模型管理器"""
    
    def __init__(self):
        self.openai_client = None
        self.groq_client = None
        self._initialize_clients()
        
    def _initialize_clients(self):
        """初始化 AI 客戶端"""
        # 初始化 OpenAI 客戶端
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if openai_api_key and openai_api_key != 'your_openai_api_key_here':
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
            
        # 初始化 Groq 客戶端
        groq_api_key = os.getenv('GROQ_API_KEY')
        if groq_api_key and groq_api_key != 'your_groq_api_key_here':
            self.groq_client = groq.Groq(api_key=groq_api_key)
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """取得可用的 AI 模型"""
        models = []
        
        if self.openai_client:
            models.extend([
                {
                    'id': 'gpt-4',
                    'name': 'GPT-4',
                    'provider': 'openai',
                    'description': 'OpenAI GPT-4 模型'
                },
                {
                    'id': 'gpt-3.5-turbo',
                    'name': 'GPT-3.5 Turbo',
                    'provider': 'openai',
                    'description': 'OpenAI GPT-3.5 Turbo 模型'
                }
            ])
            
        if self.groq_client:
            models.extend([
                {
                    'id': 'llama3-8b-8192',
                    'name': 'Llama 3 8B',
                    'provider': 'groq',
                    'description': 'Groq Llama 3 8B 模型'
                },
                {
                    'id': 'llama3-70b-8192',
                    'name': 'Llama 3 70B',
                    'provider': 'groq',
                    'description': 'Groq Llama 3 70B 模型'
                },
                {
                    'id': 'mixtral-8x7b-32768',
                    'name': 'Mixtral 8x7B',
                    'provider': 'groq',
                    'description': 'Groq Mixtral 8x7B 模型'
                }
            ])
        
        # 如果沒有可用的模型，提供模擬模型
        if not models:
            models = [
                {
                    'id': 'demo-model',
                    'name': 'Demo Model',
                    'provider': 'demo',
                    'description': '示範模型（無需 API 金鑰）'
                }
            ]
            
        return models
    
    def generate_response(self, 
                         prompt: str, 
                         model: str = 'gpt-4',
                         temperature: float = 0.7,
                         max_tokens: int = 2000) -> str:
        """生成 AI 回應"""
        
        # 如果是示範模型，使用模擬回應
        if model == 'demo-model':
            return self._generate_demo_response(prompt)
        
        # 判斷使用哪個客戶端
        if model.startswith('gpt-'):
            if not self.openai_client:
                return self._generate_demo_response(prompt)
            return self._generate_openai_response(prompt, model, temperature, max_tokens)
        else:
            if not self.groq_client:
                return self._generate_demo_response(prompt)
            return self._generate_groq_response(prompt, model, temperature, max_tokens)
    
    def _generate_demo_response(self, prompt: str) -> str:
        """生成示範回應"""
        # 根據 prompt 內容生成模擬回應
        if '登入' in prompt or 'login' in prompt:
            return '''{
    "test_cases": [
        {
            "id": "TC001",
            "title": "使用正確帳密登入",
            "description": "測試使用正確的用戶名和密碼進行登入",
            "type": "positive",
            "steps": [
                "打開登入頁面",
                "輸入正確的用戶名",
                "輸入正確的密碼",
                "點擊登入按鈕"
            ],
            "expected_result": "成功登入並導向 Dashboard 頁面",
            "priority": "high"
        },
        {
            "id": "TC002",
            "title": "輸入錯誤密碼",
            "description": "測試使用錯誤密碼時的錯誤處理",
            "type": "negative",
            "steps": [
                "打開登入頁面",
                "輸入正確的用戶名",
                "輸入錯誤的密碼",
                "點擊登入按鈕"
            ],
            "expected_result": "顯示「帳號或密碼錯誤」訊息",
            "priority": "high"
        },
        {
            "id": "TC003",
            "title": "空白密碼欄位",
            "description": "測試密碼欄位為空時的驗證",
            "type": "negative",
            "steps": [
                "打開登入頁面",
                "輸入用戶名",
                "保持密碼欄位空白",
                "點擊登入按鈕"
            ],
            "expected_result": "顯示「密碼為必填」錯誤訊息",
            "priority": "medium"
        },
        {
            "id": "TC004",
            "title": "特殊符號用戶名",
            "description": "測試包含特殊符號的用戶名輸入",
            "type": "negative",
            "steps": [
                "打開登入頁面",
                "輸入包含特殊符號的用戶名",
                "輸入密碼",
                "點擊登入按鈕"
            ],
            "expected_result": "顯示「用戶名格式錯誤」提示",
            "priority": "medium"
        },
        {
            "id": "TC005",
            "title": "按下 Enter 鍵登入",
            "description": "測試使用 Enter 鍵進行登入",
            "type": "positive",
            "steps": [
                "打開登入頁面",
                "輸入正確的用戶名",
                "輸入正確的密碼",
                "按下 Enter 鍵"
            ],
            "expected_result": "成功登入並導向 Dashboard 頁面",
            "priority": "medium"
        }
    ]
}'''
        else:
            return '''{
    "test_cases": [
        {
            "id": "TC001",
            "title": "基本功能測試",
            "description": "測試基本功能是否正常運作",
            "type": "positive",
            "steps": [
                "打開測試頁面",
                "執行基本操作",
                "驗證結果"
            ],
            "expected_result": "功能正常運作",
            "priority": "high"
        },
        {
            "id": "TC002",
            "title": "錯誤處理測試",
            "description": "測試錯誤情況的處理",
            "type": "negative",
            "steps": [
                "打開測試頁面",
                "執行錯誤操作",
                "檢查錯誤處理"
            ],
            "expected_result": "正確處理錯誤情況",
            "priority": "medium"
        }
    ]
}'''
    
    def _generate_openai_response(self, 
                                 prompt: str, 
                                 model: str,
                                 temperature: float,
                                 max_tokens: int) -> str:
        """使用 OpenAI 生成回應"""
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一個專業的軟體測試工程師，專門生成高品質的測試用例。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API 錯誤: {str(e)}")
    
    def _generate_groq_response(self, 
                               prompt: str, 
                               model: str,
                               temperature: float,
                               max_tokens: int) -> str:
        """使用 Groq 生成回應"""
        try:
            response = self.groq_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一個專業的軟體測試工程師，專門生成高品質的測試用例。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq API 錯誤: {str(e)}")
    
    def test_connection(self, model: str = 'gpt-4') -> bool:
        """測試模型連接"""
        try:
            test_prompt = "請回應 '連接成功'"
            response = self.generate_response(test_prompt, model, temperature=0.1, max_tokens=10)
            return "連接成功" in response
        except Exception:
            return False 