# TestGPT – AI-driven Test Case Generator

## 專案目標
利用 AI 模型（如 GPT-4 或 Groq）從自然語言描述中生成高品質測試用例與可執行的自動化測試腳本，提升測試設計效率與覆蓋率。

## 核心功能模組

### 📝 用例生成器
- 使用者輸入自然語言描述（如「我要測試註冊表單」）
- AI 生成多種正向與負向測試用例
- 支援功能測試、異常處理、邊界值測試

### 💡 腳本轉換器
- 將生成的測試用例轉換為 Pytest / Selenium 可執行的 Python 測試碼
- 自動生成測試類別、方法、斷言
- 支援多種測試框架

### ⚠️ Fuzz 測試模組
- 對欄位輸入進行隨機異常資料注入
- 測試過長文字、空值、特殊字元等邊界情況
- 自動生成異常資料測試用例

### 🧪 Prompt 模型選擇
- 可切換模型（OpenAI / Groq）
- 可設定 Prompt template
- 支援不同 AI 模型的參數調整

### 📁 測試腳本匯出
- 用戶可下載完整 .py 檔案
- 包含測試與說明文件
- 支援多種匯出格式

### 📊 報告摘要
- 顯示已生成用例分類（功能/異常/邊界）
- 覆蓋重點分析
- 建議補充區域提示

## 安裝與使用

```bash
# 安裝依賴
pip install -r requirements.txt

# 設定環境變數
cp .env.example .env
# 編輯 .env 檔案，填入您的 API 金鑰

# 執行應用程式
python app.py
```

## 示範操作流程

**輸入：**
- 測試：登入功能
- 條件：需要帳號密碼欄位，按下登入後導向 Dashboard
- 要求：請提供功能測試與錯誤處理測試

**輸出測試用例：**
- ✅ 使用正確帳密 → 導向 dashboard 頁面
- ❌ 輸入錯誤密碼 → 顯示「帳號或密碼錯誤」
- ❌ 空白密碼 → 顯示「密碼為必填」
- ❌ 輸入特殊符號帳號 → 應提示錯誤格式
- ✅ 按下 Enter 鍵也能送出表單

## 專案結構

```
TestGPT/
├── app.py                 # 主應用程式
├── requirements.txt       # 依賴套件
├── .env.example          # 環境變數範例
├── README.md             # 專案說明
├── src/
│   ├── __init__.py
│   ├── generators/       # 用例生成器
│   ├── converters/       # 腳本轉換器
│   ├── fuzz/            # Fuzz 測試模組
│   ├── models/          # AI 模型管理
│   ├── exporters/       # 測試腳本匯出
│   └── reports/         # 報告摘要
├── templates/            # HTML 模板
├── static/              # 靜態檔案
└── tests/               # 專案測試
``` 