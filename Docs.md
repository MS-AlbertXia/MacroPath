# 宏星智途 (MacroSTAR Path) 说明文档

## 1. 软件简介

宏星智途是一款基于AI的个性化学习助手软件，旨在通过人工智能技术为用户提供定制化的学习体验。软件采用PyQt5和PyQtFluentWidgets框架开发，界面美观现代，功能丰富实用。

### 核心功能
- **AI助手**：集成OpenAI/DeepSeek API，提供智能学习辅助
- **学习路径**：可视化学习进度，推荐个性化学习内容
- **设置中心**：支持主题切换、API配置等多种自定义选项
- **现代化界面**：采用Fluent Design设计语言，美观流畅

## 2. 系统要求

### 硬件要求
- CPU：Intel Core i3 或同等性能处理器
- 内存：4GB 及以上
- 存储空间：50MB 可用空间

### 软件要求
- 操作系统：Windows 10/11、macOS 10.15+、Linux
- Python：3.7 及以上版本
- 依赖库：详见 `requirements.txt`

## 3. 安装指南

### 方法一：使用源码安装

1. **克隆或下载源码**
   ```bash
   git clone https://github.com/MS-AlbertXia/CN-MacroSTAR-Path.git
   ```
    或直接下载源码压缩包并解压

2. **安装依赖**
   ```bash
   cd CN-MacroSTAR-Path
   pip install -r requirements.txt
   ```

3. **运行软件**
   ```bash
   python main.py
   ```


## 4. 快速开始

### 首次使用

1. **启动软件**：运行 `python app/main.py`
2. **配置AI API**：
   - 点击左侧导航栏的「设置」
   - 在「AI API设置」部分填写配置：
     - API地址：OpenAI为 `https://api.openai.com/v1`，DeepSeek为 `https://api.deepseek.com/v1`
     - API密钥：输入您的API密钥
     - 模型：OpenAI为 `gpt-3.5-turbo`，DeepSeek为 `deepseek-chat`
     - 温度：建议设置为 0.7
   - 点击「保存AI API设置」

3. **开始使用AI助手**：
   - 点击左侧导航栏的「AI助手」
   - 在输入框中输入您的问题
   - 点击发送按钮或按 Enter 键
   - 等待AI回复

## 5. 功能详解

### 5.1 首页

- **学习概览**：展示学习进度和统计数据
- **快捷入口**：快速访问常用功能
- **推荐内容**：基于AI分析的个性化学习推荐

### 5.2 AI助手

- **智能问答**：解答学习相关问题
- **学习辅助**：提供知识点解释、习题解答等
- **聊天历史**：保存对话记录，支持清空功能
- **响应式布局**：适配不同窗口大小

### 5.3 学习路径

- **进度追踪**：可视化展示学习进度
- **目标设置**：设定学习目标和计划
- **推荐路径**：基于AI分析的个性化学习路径推荐

### 5.4 设置

- **外观设置**：
  - 主题：支持浅色模式、深色模式、跟随系统
  - 字体大小：可调节界面字体大小
- **学习设置**：
  - 每日学习目标：设定每日学习时间
  - 学习提醒：开启/关闭学习提醒
  - 自动保存：开启/关闭自动保存功能
- **账户设置**：
  - 用户名：设置显示名称
  - 邮箱：绑定联系邮箱
- **AI API设置**：
  - API地址：配置API服务地址
  - API密钥：输入API访问密钥
  - 模型选择：选择使用的AI模型
  - 温度设置：调节AI回复的创造性

## 6. AI API配置

### 支持的API服务

#### OpenAI API
- **API地址**：`https://api.openai.com/v1`
- **模型**：`gpt-3.5-turbo`、`gpt-4` 等
- **获取方式**：访问 [OpenAI官网](https://platform.openai.com/) 注册账号并创建API密钥

#### DeepSeek API
- **API地址**：`https://api.deepseek.com/v1`
- **模型**：`deepseek-chat`
- **获取方式**：访问 [DeepSeek官网](https://platform.deepseek.com/) 注册账号并创建API密钥

### 配置步骤

1. 在设置页面的「AI API设置」部分填写配置信息
2. 点击「保存AI API设置」按钮
3. 切换到AI助手页面开始使用

## 7. 常见问题

### 7.1 无法连接AI API

**解决方法**：
- 检查网络连接是否正常
- 确认API地址填写正确
- 验证API密钥是否有效
- 检查防火墙设置是否阻止了网络请求

### 7.2 主题切换不生效

**解决方法**：
- 确保已安装最新版本的PyQtFluentWidgets
- 尝试重启软件
- 检查系统主题设置

### 7.3 界面显示异常

**解决方法**：
- 确保屏幕分辨率设置正常
- 尝试调整窗口大小
- 检查Python和依赖库版本

## 8. 故障排除

### 8.1 错误提示：ImportError

**原因**：缺少依赖库
**解决方法**：运行 `pip install -r requirements.txt` 安装所有依赖

### 8.2 错误提示：API请求失败

**原因**：API配置错误或网络问题
**解决方法**：
- 检查API密钥是否正确
- 确认API地址设置正确
- 验证网络连接

### 8.3 错误提示：模型不存在

**原因**：模型名称填写错误
**解决方法**：
- OpenAI模型：使用 `gpt-3.5-turbo` 或 `gpt-4`
- DeepSeek模型：使用 `deepseek-chat`

## 9. 配置文件

### 9.1 AI API配置

配置文件路径：`app/resources/openai_config.json`

**示例配置**：
```json
{
  "api_key": "sk-...",
  "model": "gpt-3.5-turbo",
  "temperature": 0.7,
  "api_base": "https://api.openai.com/v1"
}
```

### 9.2 应用设置

配置文件路径：`app/resources/app_config.json`

**示例配置**：
```json
{
  "theme": 2,
  "font_size": 14,
  "username": "学生",
  "email": "",
  "daily_goal": "2小时",
  "reminder_enabled": true,
  "auto_save_enabled": true
}
```

## 10. 开发说明

### 10.1 项目结构

```
app/
├── main.py              # 应用入口
├── main_window.py       # 主窗口
├── widgets/
│   ├── home_widget.py       # 首页
│   ├── ai_assistant_widget.py  # AI助手
│   ├── learning_path_widget.py # 学习路径
│   └── settings_widget.py      # 设置页面
└── utils/
    └── openai_client.py   # OpenAI客户端
```

### 10.2 主要模块

- **main.py**：应用程序入口，初始化应用
- **main_window.py**：主窗口实现，包含导航栏和页面切换
- **widgets/**：各个功能页面的实现
- **utils/**：工具类和API客户端

### 10.3 扩展开发

1. **添加新页面**：在 `widgets/` 目录下创建新的widget类
2. **修改导航栏**：在 `main_window.py` 中添加新的导航项
3. **扩展API**：修改 `openai_client.py` 添加新的API功能

## 11. 版本历史

### v0.0.1 (2026-02-25)（测试中版本，不代表最终品质）
- 初始版本发布
- 实现核心功能：AI助手、学习路径、设置中心
- 支持OpenAI/DeepSeek API集成
- 实现主题切换功能

## 12. 联系与支持

### 反馈建议
- 邮箱：support@macrostar.top
- GitHub：[MacroSTAR Path](https://github.com/MS-AlbertXia/CN-MacroSTAR-Path)

### 贡献代码
欢迎提交Pull Request和Issue，共同改进宏星智途！

## 13. 许可证

本软件采用 GPL v3 许可证开源。详见 `LICENSE` 文件。

---

**宏星慧学 - 让学习更智能，让未来更精彩！**