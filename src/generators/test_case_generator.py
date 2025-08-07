"""
測試用例生成器
使用 AI 模型從自然語言描述生成測試用例
"""

import json
from typing import List, Dict, Any
from src.models.ai_model_manager import AIModelManager

class TestCaseGenerator:
    """測試用例生成器"""
    
    def __init__(self, ai_manager: AIModelManager):
        self.ai_manager = ai_manager
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """載入測試模板"""
        return {
            'web_application': {
                'name': 'Web 應用程式測試',
                'description': '適用於網站、Web 應用程式的測試模板',
                'focus_areas': ['UI 測試', 'API 測試', '資料庫測試', '安全性測試'],
                'common_scenarios': ['登入/登出', '表單提交', '資料查詢', '檔案上傳']
            },
            'mobile_app': {
                'name': '行動應用程式測試',
                'description': '適用於 iOS/Android 應用程式的測試模板',
                'focus_areas': ['UI 測試', '手勢測試', '網路連線', '本地儲存'],
                'common_scenarios': ['觸控操作', '網路切換', '背景執行', '權限管理']
            },
            'api_service': {
                'name': 'API 服務測試',
                'description': '適用於 RESTful API、微服務的測試模板',
                'focus_areas': ['API 端點測試', '資料格式驗證', '錯誤處理', '效能測試'],
                'common_scenarios': ['CRUD 操作', '認證授權', '資料驗證', '錯誤回應']
            },
            'database': {
                'name': '資料庫測試',
                'description': '適用於資料庫系統的測試模板',
                'focus_areas': ['資料完整性', '查詢效能', '並發處理', '備份還原'],
                'common_scenarios': ['資料插入/更新/刪除', '複雜查詢', '交易處理', '資料遷移']
            },
            'security': {
                'name': '安全性測試',
                'description': '專注於安全漏洞檢測的測試模板',
                'focus_areas': ['輸入驗證', '權限控制', '資料保護', '加密解密'],
                'common_scenarios': ['SQL 注入', 'XSS 攻擊', 'CSRF 攻擊', '權限提升']
            }
        }
    
    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """取得可用的測試模板"""
        return self.templates
    
    def generate_with_template(self, 
                              description: str, 
                              template_name: str,
                              test_type: str = 'functional',
                              model: str = 'gpt-4') -> List[Dict[str, Any]]:
        """使用指定模板生成測試用例"""
        
        if template_name not in self.templates:
            raise ValueError(f"不支援的模板：{template_name}")
        
        template = self.templates[template_name]
        prompt = self._build_template_prompt(description, template, test_type)
        
        # 使用 AI 模型生成回應
        response = self.ai_manager.generate_response(prompt, model)
        
        # 解析回應為測試用例
        test_cases = self._parse_response(response)
        
        return test_cases
    
    def _build_template_prompt(self, description: str, template: Dict[str, Any], test_type: str) -> str:
        """建立基於模板的 prompt"""
        
        base_prompt = f"""
作為一個專業的軟體測試工程師，請使用「{template['name']}」模板為以下功能生成高品質的測試用例。

**功能描述：**
{description}

**測試類型：** {test_type}

**模板資訊：**
- 模板名稱：{template['name']}
- 模板描述：{template['description']}
- 重點測試領域：{', '.join(template['focus_areas'])}
- 常見測試場景：{', '.join(template['common_scenarios'])}

**要求：**
1. 測試用例必須符合 {template['name']} 的特點
2. 重點關注 {', '.join(template['focus_areas'])}
3. 包含 {', '.join(template['common_scenarios'])} 相關測試
4. 每個測試步驟都要具體且可執行
5. 預期結果要量化且可測量

請以 JSON 格式回應，格式如下：
{{
    "test_cases": [
        {{
            "id": "TC001",
            "title": "具體的測試標題",
            "description": "詳細的測試描述，包含測試目的和背景",
            "type": "positive|negative|boundary|exception",
            "template_focus": "對應的模板重點領域",
            "steps": [
                "具體的步驟描述（不要包含編號）",
                "具體的步驟描述（不要包含編號）",
                "具體的步驟描述（不要包含編號）"
            ],
            "expected_result": "具體可驗證的預期結果",
            "priority": "high|medium|low",
            "business_impact": "對業務的影響程度",
            "risk_level": "風險等級"
        }}
    ]
}}

**重要提醒：**
- 步驟描述中不要包含編號（如 "1."、"2." 等）
- 前端會自動為步驟添加編號
- 請直接描述步驟內容，例如："Navigate to the payment page" 而不是 "1. Navigate to the payment page"

請確保生成的測試用例：
1. 符合 {template['name']} 的測試特點
2. 涵蓋所有重要的功能點
3. 考慮各種可能的異常情況
4. 描述精確且無歧義
5. 步驟具體且可重複執行
"""
        
        return base_prompt
    
    def generate(self, 
                 description: str, 
                 test_type: str = 'functional',
                 model: str = 'gpt-4') -> List[Dict[str, Any]]:
        """生成測試用例"""
        
        # 根據測試類型生成不同的 prompt
        prompt = self._build_prompt(description, test_type)
        
        # 使用 AI 模型生成回應
        response = self.ai_manager.generate_response(prompt, model)
        
        # 解析回應為測試用例
        test_cases = self._parse_response(response)
        
        return test_cases
    
    def _build_prompt(self, description: str, test_type: str) -> str:
        """建立更精確的 prompt"""
        
        # 更詳細的 prompt 模板
        base_prompt = f"""
作為一個專業的軟體測試工程師，請為以下功能生成高品質的測試用例。

**功能描述：**
{description}

**測試類型：** {test_type}

**要求：**
1. 測試用例必須具體且可執行
2. 每個測試步驟都要明確且可驗證
3. 預期結果要量化且可測量
4. 優先級要根據業務影響程度設定
5. 測試用例要涵蓋正常流程、異常處理、邊界條件

**測試用例格式要求：**
- 標題：簡潔明確，包含測試目標
- 描述：詳細說明測試目的和背景
- 步驟：具體可執行的操作步驟
- 預期結果：可驗證的具體結果
- 優先級：根據業務重要性和風險程度

請以 JSON 格式回應，格式如下：
{{
    "test_cases": [
        {{
            "id": "TC001",
            "title": "具體的測試標題",
            "description": "詳細的測試描述，包含測試目的和背景",
            "type": "positive|negative|boundary|exception",
            "steps": [
                "具體的步驟描述（不要包含編號）",
                "具體的步驟描述（不要包含編號）",
                "具體的步驟描述（不要包含編號）"
            ],
            "expected_result": "具體可驗證的預期結果",
            "priority": "high|medium|low",
            "business_impact": "對業務的影響程度",
            "risk_level": "風險等級"
        }}
    ]
}}

**重要提醒：**
- 步驟描述中不要包含編號（如 "1."、"2." 等）
- 前端會自動為步驟添加編號
- 請直接描述步驟內容，例如："Navigate to the payment page" 而不是 "1. Navigate to the payment page"

**特殊要求：**
"""
        
        # 根據測試類型提供更具體的指導
        if test_type == 'functional':
            base_prompt += """
- 重點：功能正確性測試
- 確保所有功能點都有對應的測試用例
- 包含正常流程和異常流程
- 驗證業務邏輯的正確性
"""
        elif test_type == 'security':
            base_prompt += """
- 重點：安全性測試
- 包含輸入驗證、權限檢查、資料保護
- 測試 SQL 注入、XSS、CSRF 等安全漏洞
- 驗證身份驗證和授權機制
"""
        elif test_type == 'performance':
            base_prompt += """
- 重點：效能測試
- 包含響應時間、吞吐量、資源使用率
- 測試在不同負載下的表現
- 驗證效能瓶頸和優化點
"""
        elif test_type == 'usability':
            base_prompt += """
- 重點：可用性測試
- 包含用戶體驗、易用性、可訪問性
- 測試界面友好性和操作直觀性
- 驗證用戶工作流程的順暢性
"""
        
        base_prompt += """
請確保生成的測試用例：
1. 描述精確且無歧義
2. 步驟具體且可重複執行
3. 預期結果可測量且可驗證
4. 涵蓋所有重要的功能點
5. 考慮各種可能的異常情況
"""
        
        return base_prompt
    
    def _parse_response(self, response: str) -> List[Dict[str, Any]]:
        """解析 AI 回應為測試用例"""
        try:
            # 嘗試直接解析 JSON
            data = json.loads(response)
            return data.get('test_cases', [])
        except json.JSONDecodeError:
            # 如果 JSON 解析失敗，嘗試提取 JSON 部分
            try:
                # 尋找 JSON 開始和結束的位置
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = response[start:end]
                    data = json.loads(json_str)
                    return data.get('test_cases', [])
            except:
                pass
            
            # 如果都失敗，返回基本格式
            return self._create_basic_test_cases(response)
    
    def _create_basic_test_cases(self, response: str) -> List[Dict[str, Any]]:
        """從文字回應建立基本測試用例"""
        test_cases = []
        
        # 簡單的文本解析
        lines = response.split('\n')
        current_case = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 檢測測試用例開始
            if line.startswith('✅') or line.startswith('❌') or line.startswith('•'):
                if current_case:
                    test_cases.append(current_case)
                
                # 建立新的測試用例
                current_case = {
                    'id': f"TC{len(test_cases) + 1:03d}",
                    'title': line.replace('✅', '').replace('❌', '').replace('•', '').strip(),
                    'description': line.strip(),
                    'type': 'positive' if line.startswith('✅') else 'negative',
                    'steps': [],
                    'expected_result': '',
                    'priority': 'medium'
                }
            elif current_case and '→' in line:
                # 解析預期結果
                parts = line.split('→')
                if len(parts) >= 2:
                    current_case['expected_result'] = parts[1].strip()
        
        # 添加最後一個測試用例
        if current_case:
            test_cases.append(current_case)
        
        return test_cases
    
    def generate_login_test_cases(self, model: str = 'gpt-4') -> List[Dict[str, Any]]:
        """生成登入功能的測試用例（示範用）"""
        description = """
測試：登入功能
條件：需要帳號密碼欄位，按下登入後導向 Dashboard
要求：請提供功能測試與錯誤處理測試
"""
        
        return self.generate(description, 'functional', model) 