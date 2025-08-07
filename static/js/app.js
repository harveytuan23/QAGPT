// TestGPT 前端 JavaScript

let currentTestCases = [];
let currentScript = '';

// 頁面載入完成後初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // 綁定表單提交事件
    document.getElementById('testCaseForm').addEventListener('submit', handleTestCaseGeneration);
    
    // 初始化 Fuzz 測試欄位
    initializeFuzzFields();
    
    // 載入可用的 AI 模型
    loadAvailableModels();
    
    // 綁定模板選擇事件
    document.getElementById('testTemplate').addEventListener('change', handleTemplateChange);
}

// 處理測試用例生成
async function handleTestCaseGeneration(event) {
    event.preventDefault();
    
    const description = document.getElementById('description').value.trim();
    const testType = document.getElementById('testType').value;
    const model = document.getElementById('aiModel').value;
    const template = document.getElementById('testTemplate').value;
    
    if (!description) {
        showAlert('請輸入功能描述', 'warning');
        return;
    }
    
    // 顯示載入中
    showLoadingModal();
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                description: description,
                test_type: testType,
                model: model,
                template: template
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentTestCases = data.test_cases;
            displayTestCases(data.test_cases);
            showAlert('測試用例生成成功！', 'success');
            
            // 自動執行轉換腳本和生成報告
            await autoGenerateScriptAndReport();
        } else {
            showAlert('生成失敗: ' + data.error, 'danger');
        }
    } catch (error) {
        showAlert('網路錯誤: ' + error.message, 'danger');
    } finally {
        hideLoadingModal();
    }
}

// 顯示測試用例
function displayTestCases(testCases) {
    const container = document.getElementById('testCasesResult');
    
    if (!testCases || testCases.length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted">
                <i class="fas fa-exclamation-triangle fa-2x mb-2"></i>
                <p>沒有生成測試用例</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    testCases.forEach((testCase, index) => {
        const typeClass = testCase.type || 'unknown';
        const priorityClass = testCase.priority || 'medium';
        
        html += `
            <div class="test-case-item ${typeClass} fade-in">
                <div class="test-case-header">
                    <h6 class="test-case-title">${testCase.title || `測試用例 ${index + 1}`}</h6>
                    <div>
                        <span class="test-case-type ${typeClass}">${getTypeDisplayName(testCase.type)}</span>
                        <span class="priority-badge ${priorityClass} ms-2">${getPriorityDisplayName(testCase.priority)}</span>
                    </div>
                </div>
                
                <div class="test-case-description">
                    ${testCase.description || '無描述'}
                </div>
                
                ${testCase.steps && testCase.steps.length > 0 ? `
                    <div class="test-case-steps">
                        <strong>測試步驟:</strong>
                        <ol>
                            ${testCase.steps.map(step => `<li>${cleanStepNumber(step)}</li>`).join('')}
                        </ol>
                    </div>
                ` : ''}
                
                ${testCase.expected_result ? `
                    <div class="test-case-expected">
                        <strong>預期結果:</strong> ${testCase.expected_result}
                    </div>
                ` : ''}
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// 轉換為測試腳本
async function convertToScript() {
    if (!currentTestCases || currentTestCases.length === 0) {
        showAlert('請先生成測試用例', 'warning');
        return;
    }
    
    // 如果腳本已經存在，直接切換到腳本分頁
    if (currentScript) {
        const scriptTab = new bootstrap.Tab(document.getElementById('script-tab'));
        scriptTab.show();
        showAlert('腳本已存在，已切換到腳本分頁', 'info');
        return;
    }
    
    const framework = document.getElementById('frameworkSelect').value;
    
    try {
        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                test_cases: currentTestCases,
                framework: framework
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentScript = data.script;
            document.getElementById('scriptContent').innerHTML = `<pre class="bg-light p-3 rounded">${data.script}</pre>`;
            
            // 切換到腳本分頁
            const scriptTab = new bootstrap.Tab(document.getElementById('script-tab'));
            scriptTab.show();
            
            showAlert('腳本轉換成功！', 'success');
        } else {
            showAlert('轉換失敗: ' + data.error, 'danger');
        }
    } catch (error) {
        showAlert('網路錯誤: ' + error.message, 'danger');
    }
}

// 生成報告
async function generateReport() {
    if (!currentTestCases || currentTestCases.length === 0) {
        showAlert('請先生成測試用例', 'warning');
        return;
    }
    
    // 檢查報告是否已經生成（通過檢查報告內容區域是否有內容）
    const reportContent = document.getElementById('reportContent');
    if (reportContent.innerHTML && !reportContent.innerHTML.includes('請先生成測試用例')) {
        const reportTab = new bootstrap.Tab(document.getElementById('report-tab'));
        reportTab.show();
        showAlert('報告已存在，已切換到報告分頁', 'info');
        return;
    }
    
    try {
        const response = await fetch('/report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                test_cases: currentTestCases
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayReport(data.report);
            
            // 切換到報告分頁
            const reportTab = new bootstrap.Tab(document.getElementById('report-tab'));
            reportTab.show();
            
            showAlert('報告生成成功！', 'success');
        } else {
            showAlert('報告生成失敗: ' + data.error, 'danger');
        }
    } catch (error) {
        showAlert('網路錯誤: ' + error.message, 'danger');
    }
}

// 顯示報告
function displayReport(report) {
    const container = document.getElementById('reportContent');
    
    let html = `
        <div class="report-section">
            <h6>📊 摘要</h6>
            <p>${report.summary}</p>
        </div>
    `;
    
    // 統計資料
    if (report.statistics && Object.keys(report.statistics).length > 0) {
        html += `
            <div class="report-section">
                <h6>📈 統計資料</h6>
                <div class="statistics-grid">
                    <div class="stat-card">
                        <div class="stat-number">${report.statistics.total_cases || 0}</div>
                        <div class="stat-label">總測試用例</div>
                    </div>
        `;
        
        if (report.statistics.by_type) {
            Object.entries(report.statistics.by_type).forEach(([type, count]) => {
                html += `
                    <div class="stat-card">
                        <div class="stat-number">${count}</div>
                        <div class="stat-label">${getTypeDisplayName(type)}</div>
                    </div>
                `;
            });
        }
        
        html += `</div></div>`;
    }
    
    // 覆蓋率
    if (report.coverage && report.coverage.percentages) {
        html += `
            <div class="report-section">
                <h6>🎯 覆蓋率分析</h6>
        `;
        
        Object.entries(report.coverage.percentages).forEach(([area, percentage]) => {
            html += `
                <div class="mb-2">
                    <div class="d-flex justify-content-between">
                        <span>${getCoverageDisplayName(area)}</span>
                        <span>${percentage.toFixed(1)}%</span>
                    </div>
                    <div class="coverage-bar">
                        <div class="coverage-fill" style="width: ${percentage}%"></div>
                    </div>
                </div>
            `;
        });
        
        html += `</div>`;
    }
    
    // 建議
    if (report.recommendations && report.recommendations.length > 0) {
        html += `
            <div class="report-section">
                <h6>💡 改進建議</h6>
        `;
        
        report.recommendations.forEach(recommendation => {
            html += `<div class="recommendation-item">${recommendation}</div>`;
        });
        
        html += `</div>`;
    }
    
    container.innerHTML = html;
}

// 生成 Fuzz 測試
async function generateFuzzTests() {
    const fields = getFuzzFields();
    
    if (fields.length === 0) {
        showAlert('請至少添加一個測試欄位', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/fuzz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                fields: fields
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 將 Fuzz 測試添加到現有測試用例中
            currentTestCases = currentTestCases.concat(data.fuzz_tests);
            displayTestCases(currentTestCases);
            showAlert('Fuzz 測試生成成功！', 'success');
        } else {
            showAlert('Fuzz 測試生成失敗: ' + data.error, 'danger');
        }
    } catch (error) {
        showAlert('網路錯誤: ' + error.message, 'danger');
    }
}

// 匯出腳本
async function exportScript() {
    if (!currentScript) {
        showAlert('請先生成測試腳本', 'warning');
        return;
    }
    
    const filename = `test_script_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.py`;
    
    try {
        const response = await fetch('/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                script: currentScript,
                filename: filename
            })
        });
        
        if (response.ok) {
            // 下載檔案
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showAlert('腳本下載成功！', 'success');
        } else {
            const data = await response.json();
            showAlert('下載失敗: ' + data.error, 'danger');
        }
    } catch (error) {
        showAlert('網路錯誤: ' + error.message, 'danger');
    }
}

// Fuzz 測試欄位管理
function initializeFuzzFields() {
    // 初始化預設欄位
    addField();
    addField();
}

function addField() {
    const fieldList = document.getElementById('fieldList');
    const fieldDiv = document.createElement('div');
    fieldDiv.className = 'input-group mb-2';
    fieldDiv.innerHTML = `
        <input type="text" class="form-control" placeholder="欄位名稱">
        <select class="form-select" style="max-width: 120px;">
            <option value="text">文字</option>
            <option value="email">電子郵件</option>
            <option value="number">數字</option>
            <option value="date">日期</option>
        </select>
        <button type="button" class="btn btn-outline-danger btn-sm" onclick="removeField(this)">
            <i class="fas fa-trash"></i>
        </button>
    `;
    fieldList.appendChild(fieldDiv);
}

function removeField(button) {
    const fieldList = document.getElementById('fieldList');
    if (fieldList.children.length > 1) {
        button.closest('.input-group').remove();
    }
}

function getFuzzFields() {
    const fields = [];
    const fieldGroups = document.querySelectorAll('#fieldList .input-group');
    
    fieldGroups.forEach(group => {
        const nameInput = group.querySelector('input');
        const typeSelect = group.querySelector('select');
        
        if (nameInput && nameInput.value.trim()) {
            fields.push({
                name: nameInput.value.trim(),
                type: typeSelect.value
            });
        }
    });
    
    return fields;
}

// 載入可用的 AI 模型
async function loadAvailableModels() {
    try {
        const response = await fetch('/models');
        const data = await response.json();
        
        if (data.success) {
            const modelSelect = document.getElementById('aiModel');
            modelSelect.innerHTML = '';
            
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model.id;
                option.textContent = model.name;
                modelSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('載入模型失敗:', error);
    }
}

// 工具函數
function getTypeDisplayName(type) {
    const typeNames = {
        'positive': '正向測試',
        'negative': '負向測試',
        'boundary': '邊界測試',
        'exception': '異常測試',
        'fuzz': 'Fuzz 測試'
    };
    return typeNames[type] || type;
}

function getPriorityDisplayName(priority) {
    const priorityNames = {
        'high': '高',
        'medium': '中',
        'low': '低'
    };
    return priorityNames[priority] || priority;
}

function getCoverageDisplayName(area) {
    const areaNames = {
        'functional': '功能測試',
        'security': '安全性測試',
        'performance': '效能測試',
        'usability': '可用性測試',
        'error_handling': '錯誤處理',
        'boundary_testing': '邊界測試',
        'input_validation': '輸入驗證'
    };
    return areaNames[area] || area;
}

// 清理步驟中的編號
function cleanStepNumber(step) {
    // 移除開頭的數字和點號（如 "1. "、"2. " 等）
    return step.replace(/^\d+\.\s*/, '');
}

// 自動生成腳本和報告
async function autoGenerateScriptAndReport() {
    try {
        // 顯示載入提示
        showAlert('正在自動生成腳本和報告...', 'info');
        
        // 更新分頁標籤顯示進度
        updateTabProgress();
        
        // 並行執行腳本轉換和報告生成
        const [scriptResult, reportResult] = await Promise.allSettled([
            autoConvertToScript(),
            autoGenerateReport()
        ]);
        
        // 處理腳本轉換結果
        if (scriptResult.status === 'fulfilled' && scriptResult.value) {
            showAlert('腳本轉換完成！', 'success');
        } else if (scriptResult.status === 'rejected') {
            console.error('腳本轉換失敗:', scriptResult.reason);
        }
        
        // 處理報告生成結果
        if (reportResult.status === 'fulfilled' && reportResult.value) {
            showAlert('報告生成完成！', 'success');
        } else if (reportResult.status === 'rejected') {
            console.error('報告生成失敗:', reportResult.reason);
        }
        
        // 清除進度指示器
        clearTabProgress();
        
        // 顯示完成提示
        setTimeout(() => {
            showAlert('所有功能已完成！您可以切換分頁查看結果', 'success');
        }, 1000);
        
    } catch (error) {
        console.error('自動生成過程出錯:', error);
        showAlert('自動生成過程中出現錯誤', 'warning');
        clearTabProgress();
    }
}

// 更新分頁進度指示器
function updateTabProgress() {
    const scriptTab = document.getElementById('script-tab');
    const reportTab = document.getElementById('report-tab');
    
    // 添加載入動畫
    scriptTab.innerHTML = '<i class="fas fa-code me-1"></i>轉換腳本 <i class="fas fa-spinner fa-spin ms-1"></i>';
    reportTab.innerHTML = '<i class="fas fa-chart-bar me-1"></i>生成報告 <i class="fas fa-spinner fa-spin ms-1"></i>';
}

// 清除分頁進度指示器
function clearTabProgress() {
    const scriptTab = document.getElementById('script-tab');
    const reportTab = document.getElementById('report-tab');
    
    // 恢復原始文字
    scriptTab.innerHTML = '<i class="fas fa-code me-1"></i>轉換腳本';
    reportTab.innerHTML = '<i class="fas fa-chart-bar me-1"></i>生成報告';
}

// 自動轉換腳本（不切換分頁）
async function autoConvertToScript() {
    if (!currentTestCases || currentTestCases.length === 0) {
        return false;
    }
    
    const framework = document.getElementById('frameworkSelect').value;
    
    try {
        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                test_cases: currentTestCases,
                framework: framework
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentScript = data.script;
            document.getElementById('scriptContent').innerHTML = `<pre class="bg-light p-3 rounded">${data.script}</pre>`;
            return true;
        } else {
            console.error('腳本轉換失敗:', data.error);
            return false;
        }
    } catch (error) {
        console.error('腳本轉換網路錯誤:', error);
        return false;
    }
}

// 自動生成報告（不切換分頁）
async function autoGenerateReport() {
    if (!currentTestCases || currentTestCases.length === 0) {
        return false;
    }
    
    try {
        const response = await fetch('/report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                test_cases: currentTestCases
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayReport(data.report);
            return true;
        } else {
            console.error('報告生成失敗:', data.error);
            return false;
        }
    } catch (error) {
        console.error('報告生成網路錯誤:', error);
        return false;
    }
}

// 執行測試用例
async function runTests() {
    if (!currentTestCases || currentTestCases.length === 0) {
        showAlert('請先生成測試用例', 'warning');
        return;
    }
    
    // 更新按鈕狀態
    const runButton = document.getElementById('runTestsBtn');
    const originalText = runButton.innerHTML;
    runButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>執行中...';
    runButton.disabled = true;
    
    try {
        const response = await fetch('/run-tests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                test_cases: currentTestCases
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayTestResults(data);
            
            // 切換到測試結果分頁
            const testResultsTab = new bootstrap.Tab(document.getElementById('test-results-tab'));
            testResultsTab.show();
            
            showAlert('測試執行完成！', 'success');
        } else {
            showAlert('測試執行失敗: ' + data.error, 'danger');
        }
    } catch (error) {
        showAlert('網路錯誤: ' + error.message, 'danger');
    } finally {
        // 恢復按鈕狀態
        runButton.innerHTML = originalText;
        runButton.disabled = false;
    }
}

// 顯示測試結果
function displayTestResults(data) {
    const container = document.getElementById('testResultsContent');
    
    if (!data || !data.results) {
        container.innerHTML = `
            <div class="text-center text-muted">
                <i class="fas fa-exclamation-triangle fa-2x mb-2"></i>
                <p>沒有測試結果</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    // 顯示摘要
    if (data.summary) {
        const summary = data.summary;
        html += `
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white">
                        <div class="card-body text-center">
                            <h4>${summary.total_tests}</h4>
                            <small>總測試數</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white">
                        <div class="card-body text-center">
                            <h4>${summary.passed_tests}</h4>
                            <small>通過測試</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-danger text-white">
                        <div class="card-body text-center">
                            <h4>${summary.failed_tests}</h4>
                            <small>失敗測試</small>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-info text-white">
                        <div class="card-body text-center">
                            <h4>${summary.success_rate.toFixed(1)}%</h4>
                            <small>成功率</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    // 顯示詳細結果
    html += '<div class="test-results-list">';
    data.results.forEach((result, index) => {
        const statusClass = result.success ? 'success' : 'danger';
        const statusIcon = result.success ? 'check-circle' : 'times-circle';
        
        html += `
            <div class="test-result-item ${statusClass} mb-3">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h6 class="mb-1">
                            <i class="fas fa-${statusIcon} text-${statusClass} me-2"></i>
                            ${result.title}
                        </h6>
                        <small class="text-muted">ID: ${result.id} | 類型: ${getTypeDisplayName(result.type)}</small>
                        <div class="mt-2">
                            <small class="text-muted">執行時間: ${result.execution_time.toFixed(2)}秒</small>
                        </div>
                    </div>
                    <span class="badge bg-${statusClass}">${result.success ? '通過' : '失敗'}</span>
                </div>
        `;
        
        if (result.error) {
            html += `
                <div class="alert alert-danger mt-2 mb-0">
                    <strong>錯誤:</strong> ${result.error}
                </div>
            `;
        }
        
        // 顯示步驟結果
        if (result.steps_results && result.steps_results.length > 0) {
            html += '<div class="mt-2"><small class="text-muted">步驟詳情:</small></div>';
            result.steps_results.forEach((step, stepIndex) => {
                const stepStatusClass = step.success ? 'success' : 'danger';
                const stepStatusIcon = step.success ? 'check' : 'times';
                
                html += `
                    <div class="step-result ${stepStatusClass} ms-3 mt-1">
                        <small>
                            <i class="fas fa-${stepStatusIcon} text-${stepStatusClass} me-1"></i>
                            步驟 ${step.step_number}: ${step.step}
                        </small>
                    </div>
                `;
                
                if (step.error) {
                    html += `
                        <div class="step-error ms-3 mt-1">
                            <small class="text-danger">錯誤: ${step.error}</small>
                        </div>
                    `;
                }
            });
        }
        
        html += '</div>';
    });
    
    html += '</div>';
    container.innerHTML = html;
}

// 處理模板選擇變更
function handleTemplateChange(event) {
    const templateSelect = event.target;
    const selectedTemplate = templateSelect.value;
    const templateInfo = document.getElementById('templateInfo');
    
    if (!templateInfo) {
        // 如果模板資訊區域不存在，創建它
        const templateContainer = document.createElement('div');
        templateContainer.id = 'templateInfo';
        templateContainer.className = 'alert alert-info mt-2';
        templateSelect.parentNode.appendChild(templateContainer);
    }
    
    const templateMap = {
        'web_application': {
            name: 'Web 應用程式測試',
            description: '適用於網站、Web 應用程式的測試模板',
            focus: 'UI 測試、API 測試、資料庫測試、安全性測試',
            scenarios: '登入/登出、表單提交、資料查詢、檔案上傳'
        },
        'mobile_app': {
            name: '行動應用程式測試',
            description: '適用於 iOS/Android 應用程式的測試模板',
            focus: 'UI 測試、手勢測試、網路連線、本地儲存',
            scenarios: '觸控操作、網路切換、背景執行、權限管理'
        },
        'api_service': {
            name: 'API 服務測試',
            description: '適用於 RESTful API、微服務的測試模板',
            focus: 'API 端點測試、資料格式驗證、錯誤處理、效能測試',
            scenarios: 'CRUD 操作、認證授權、資料驗證、錯誤回應'
        },
        'database': {
            name: '資料庫測試',
            description: '適用於資料庫系統的測試模板',
            focus: '資料完整性、查詢效能、並發處理、備份還原',
            scenarios: '資料插入/更新/刪除、複雜查詢、交易處理、資料遷移'
        },
        'security': {
            name: '安全性測試',
            description: '專注於安全漏洞檢測的測試模板',
            focus: '輸入驗證、權限控制、資料保護、加密解密',
            scenarios: 'SQL 注入、XSS 攻擊、CSRF 攻擊、權限提升'
        }
    };
    
    const templateContainer = document.getElementById('templateInfo');
    
    if (selectedTemplate && templateMap[selectedTemplate]) {
        const template = templateMap[selectedTemplate];
        templateContainer.innerHTML = `
            <strong>${template.name}</strong><br>
            <small>${template.description}</small><br>
            <strong>重點領域：</strong>${template.focus}<br>
            <strong>常見場景：</strong>${template.scenarios}
        `;
        templateContainer.style.display = 'block';
    } else {
        templateContainer.style.display = 'none';
    }
}

function showLoadingModal() {
    const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
    modal.show();
}

function hideLoadingModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
    if (modal) {
        modal.hide();
    }
}

function showAlert(message, type = 'info') {
    // 移除現有的警告
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // 創建新的警告
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // 插入到頁面頂部
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // 自動隱藏
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
} 