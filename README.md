# TestGPT - AI-Driven Test Case Generator with Selenium Automation

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15+-orange.svg)](https://selenium-python.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Overview

TestGPT is an AI-powered test case generator that leverages advanced language models (GPT-4, Groq) to automatically generate high-quality test cases and executable automation scripts. It features a modern web interface with real-time test execution capabilities using Selenium.

## ✨ Key Features

### 🤖 AI-Powered Test Generation
- **Natural Language Input**: Describe your test requirements in plain English
- **Multiple Test Types**: Functional, Security, Performance, and Usability testing
- **Smart Templates**: Pre-built templates for Web Apps, Mobile Apps, APIs, and more
- **Comprehensive Coverage**: Positive, negative, boundary, and exception test cases

### 🔄 Automated Test Execution
- **Real-time Execution**: Watch tests run in a visible browser window
- **Selenium Integration**: Automated browser testing with detailed step-by-step execution
- **Visual Feedback**: See each test step being performed in real-time
- **Comprehensive Reporting**: Detailed test results with success/failure analysis

### 📊 Advanced Features
- **Multi-Framework Support**: Generate tests for Pytest, Unittest, and Selenium
- **Fuzz Testing**: Automatic boundary value and security testing
- **Test Script Export**: Download executable Python test scripts
- **Smart Analytics**: Coverage analysis and improvement recommendations
- **Template System**: Professional test templates for different application types

## 🏗️ Architecture

```
TestGPT/
├── app.py                    # Main Flask application
├── src/                      # Core modules
│   ├── generators/           # Test case generator
│   ├── converters/           # Script converter
│   ├── test_runner.py       # Selenium test executor
│   ├── fuzz/                # Fuzz testing module
│   ├── models/              # AI model management
│   ├── exporters/           # Test script export
│   └── reports/             # Report generator
├── templates/                # HTML templates
├── static/                   # CSS/JS assets
├── test_server.py           # Test validation server
├── test_login.html          # Sample login page
└── requirements.txt         # Dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Chrome browser (for Selenium automation)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/harveytuan23/QAGPT.git
   cd QAGPT
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your API keys (optional)
   ```

5. **Start the application**
   ```bash
   python app.py
   ```

6. **Access the web interface**
   Open your browser and go to: http://localhost:8080

## 🧪 Testing Your Generated Tests

### Start the Test Server
```bash
python test_server.py
```
This starts a sample login page at http://localhost:5001 for testing your generated test cases.

### Test Credentials
- **Username**: admin, **Password**: password123
- **Username**: test, **Password**: test123
- **Username**: user, **Password**: user123

## 📖 Usage Guide

### 1. Generate Test Cases
1. Open the web interface at http://localhost:8080
2. Enter your test description (e.g., "Test login functionality with username/password fields")
3. Select a test template (Web Application, Mobile App, API, etc.)
4. Choose your preferred AI model
5. Click "Generate Test Cases"

### 2. Execute Tests Automatically
1. After generating test cases, click "Execute Tests"
2. Watch the tests run in a real browser window
3. View detailed results in the "Test Results" tab

### 3. Export Test Scripts
1. Switch to the "Convert Script" tab
2. Choose your preferred framework (Pytest, Unittest, Selenium)
3. Download the generated test script

### 4. Generate Reports
1. Switch to the "Generate Report" tab
2. View comprehensive test analysis and recommendations

## 🎯 Example Workflow

### Input Description
```
"Test login functionality with username/password fields, 
redirect to dashboard after successful login"
```

### Generated Test Cases
- ✅ **Positive Test**: Valid credentials → Successful login
- ❌ **Negative Test**: Invalid password → Error message
- ❌ **Boundary Test**: Empty fields → Validation errors
- ❌ **Security Test**: SQL injection attempts → Security validation
- ✅ **Usability Test**: Enter key submission → Form submission

### Executed Results
- **Total Tests**: 5
- **Passed**: 4
- **Failed**: 1
- **Success Rate**: 80%

## 🔧 Technical Stack

### Backend
- **Flask**: Lightweight web framework
- **OpenAI API**: GPT-4 integration
- **Groq API**: High-speed LLM integration
- **Selenium**: Web automation testing

### Frontend
- **Bootstrap 5**: Modern responsive UI
- **Font Awesome**: Rich icon library
- **Vanilla JavaScript**: Lightweight interactions
- **AJAX**: Asynchronous API calls

### Testing Frameworks
- **Pytest**: Modern Python testing
- **Unittest**: Standard Python testing
- **Selenium**: Web automation testing

## 🎨 Features in Detail

### AI-Powered Generation
- **Natural Language Processing**: Convert plain English to structured test cases
- **Smart Templates**: Domain-specific test patterns
- **Multi-Model Support**: GPT-4, Groq, and simulated models
- **Context Awareness**: Understands application types and requirements

### Visual Test Execution
- **Real-time Browser**: Watch tests execute in visible Chrome window
- **Step-by-step Animation**: See each action performed
- **Detailed Logging**: Console output with execution details
- **Error Highlighting**: Clear indication of failed steps

### Comprehensive Reporting
- **Test Statistics**: Success rates, execution times, coverage analysis
- **Visual Charts**: Interactive charts and graphs
- **Improvement Suggestions**: AI-powered recommendations
- **Export Options**: Multiple format support

### Advanced Testing
- **Fuzz Testing**: Boundary value and security testing
- **Template System**: Professional test patterns
- **Multi-Framework**: Support for various testing frameworks
- **CI/CD Ready**: Integration-ready test scripts

## 🛠️ Configuration

### Environment Variables
```bash
# .env file
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
SECRET_KEY=your_secret_key
FLASK_DEBUG=True
PORT=8080
```

### Test Server Configuration
```python
# test_server.py
TEST_URL=http://localhost:5001
CHROME_OPTIONS=--no-sandbox --disable-dev-shm-usage
```

## 📊 Performance

- **Test Generation**: 2-5 seconds per test case
- **Execution Speed**: Real-time with visual feedback
- **Accuracy**: 85%+ success rate on standard test cases
- **Scalability**: Supports large test suites

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Groq for high-speed LLM API
- Selenium for web automation
- Bootstrap for UI components
- Flask for web framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/harveytuan23/QAGPT/issues)
- **Documentation**: [Wiki](https://github.com/harveytuan23/QAGPT/wiki)
- **Examples**: Check the `demo.py` file for usage examples

---

**🎯 TestGPT - Revolutionizing Test Automation with AI!**

*Built with ❤️ for the testing community* 