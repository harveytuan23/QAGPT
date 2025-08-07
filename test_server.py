#!/usr/bin/env python3
"""
測試伺服器 - 用於驗證 TestGPT 生成的測試用例
"""

from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# 讀取測試登入頁面
with open('test_login.html', 'r', encoding='utf-8') as f:
    login_template = f.read()

@app.route('/')
def login_page():
    """登入頁面"""
    return login_template

@app.route('/api/login', methods=['POST'])
def api_login():
    """API 登入端點（用於 API 測試）"""
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    # 測試帳號
    valid_users = {
        'admin': 'password123',
        'test': 'test123',
        'user': 'user123'
    }
    
    if username in valid_users and valid_users[username] == password:
        return jsonify({
            'success': True,
            'message': '登入成功',
            'user': username
        })
    else:
        return jsonify({
            'success': False,
            'message': '用戶名或密碼錯誤'
        }), 401

@app.route('/api/users', methods=['GET'])
def get_users():
    """獲取用戶列表（用於測試）"""
    return jsonify({
        'users': [
            {'username': 'admin', 'email': 'admin@example.com'},
            {'username': 'test', 'email': 'test@example.com'},
            {'username': 'user', 'email': 'user@example.com'}
        ]
    })

@app.route('/dashboard')
def dashboard():
    """儀表板頁面（登入成功後跳轉）"""
    return """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>儀表板 - TestGPT 驗證</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; }
            .dashboard-card { border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="#">
                    <i class="fas fa-tachometer-alt me-2"></i>測試儀表板
                </a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/">
                        <i class="fas fa-sign-out-alt me-1"></i>登出
                    </a>
                </div>
            </div>
        </nav>
        
        <div class="container mt-4">
            <div class="row">
                <div class="col-md-4">
                    <div class="card dashboard-card">
                        <div class="card-body text-center">
                            <i class="fas fa-user fa-3x text-primary mb-3"></i>
                            <h5>用戶資訊</h5>
                            <p class="text-muted">歡迎使用測試系統</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card dashboard-card">
                        <div class="card-body text-center">
                            <i class="fas fa-chart-bar fa-3x text-success mb-3"></i>
                            <h5>統計資料</h5>
                            <p class="text-muted">測試數據分析</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card dashboard-card">
                        <div class="card-body text-center">
                            <i class="fas fa-cog fa-3x text-warning mb-3"></i>
                            <h5>系統設定</h5>
                            <p class="text-muted">配置管理</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <div class="card dashboard-card">
                        <div class="card-header">
                            <h5><i class="fas fa-list me-2"></i>最近活動</h5>
                        </div>
                        <div class="card-body">
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">
                                    <i class="fas fa-check-circle text-success me-2"></i>
                                    用戶登入成功
                                </li>
                                <li class="list-group-item">
                                    <i class="fas fa-info-circle text-info me-2"></i>
                                    系統初始化完成
                                </li>
                                <li class="list-group-item">
                                    <i class="fas fa-clock text-warning me-2"></i>
                                    最後更新時間：2024年1月
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🚀 啟動測試伺服器...")
    print("📝 測試頁面: http://localhost:5001")
    print("🔑 測試帳號:")
    print("   - 用戶名: admin, 密碼: password123")
    print("   - 用戶名: test, 密碼: test123")
    print("   - 用戶名: user, 密碼: user123")
    print("\n💡 您可以在 TestGPT 中使用以下描述來測試:")
    print("   '測試登入功能，需要帳號密碼欄位，按下登入後導向 Dashboard'")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 