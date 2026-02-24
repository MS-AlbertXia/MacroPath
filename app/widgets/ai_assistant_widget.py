from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from qfluentwidgets import (
    ScrollArea, CardWidget, TitleLabel, SubtitleLabel, BodyLabel,
    TextEdit, PrimaryPushButton, ProgressRing, PillPushButton,
    FluentIcon, ToolTip, isDarkTheme
)
from markdown import markdown
from PyQt5.QtWidgets import QTextBrowser
from app.utils.openai_client import OpenAIClient

class AIAssistantWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('aiAssistantWidget')
        
        # 初始化OpenAI客户端
        self.openai_client = OpenAIClient()
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        self.setStyleSheet('background: transparent;')
        
        # 标题区域
        title_layout = QVBoxLayout()
        title_layout.setSpacing(10)
        
        title = TitleLabel('AI学习助手')
        subtitle = BodyLabel('有任何学习问题都可以问我，我会为你提供详细的解答和学习建议。')
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        layout.addLayout(title_layout)
        
        # 聊天区域
        chat_card = CardWidget(self)
        chat_card.setStyleSheet('background: transparent; border: none;')
        chat_layout = QVBoxLayout(chat_card)
        chat_layout.setContentsMargins(20, 20, 20, 20)
        
        # 聊天记录
        self.chat_area = ScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setFixedHeight(450)
        self.chat_area.setStyleSheet('''
            ScrollArea {
                border: none;
                background: transparent;
            }
        ''')
        
        self.chat_widget = QWidget()
        self.chat_widget.setStyleSheet('background: transparent;')
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setSpacing(20)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)
        
        # 添加欢迎消息
        self.add_ai_message('你好！我是你的AI学习助手。有什么可以帮助你的吗？')
        
        self.chat_area.setWidget(self.chat_widget)
        chat_layout.addWidget(self.chat_area)
        
        # 输入区域
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)
        
        # MarkDown支持提示
        markdown_hint = QLabel('💡 支持MarkDown格式')
        markdown_hint.setStyleSheet('''
            QLabel {
                font-size: 12px;
                color: #666666;
            }
        ''')
        input_layout.addWidget(markdown_hint, 0, Qt.AlignRight)
        
        self.input_edit = TextEdit()
        self.input_edit.setFixedHeight(80)
        self.input_edit.setPlaceholderText('输入你的问题...')
        self.input_edit.setStyleSheet('''
            TextEdit {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                padding: 10px;
            }
            TextEdit:focus {
                border: 1px solid #0078D7;
            }
        ''')
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addWidget(self.input_edit)
        
        send_button = PillPushButton(FluentIcon.SEND, '')
        send_button.setFixedSize(48, 48)
        send_button.clicked.connect(self.send_message)
        
        button_layout.addWidget(send_button, 0, Qt.AlignBottom)
        input_layout.addLayout(button_layout)
        
        chat_layout.addLayout(input_layout)
        layout.addWidget(chat_card)
        
        # 快捷问题
        quick_questions_card = CardWidget(self)
        quick_questions_card.setStyleSheet('background: transparent; border: none;')
        quick_questions_layout = QVBoxLayout(quick_questions_card)
        quick_questions_layout.setContentsMargins(20, 20, 20, 20)
        
        quick_title = SubtitleLabel('快捷问题')
        quick_questions_layout.addWidget(quick_title)
        
        # 使用网格布局，更灵活
        from PyQt5.QtWidgets import QGridLayout
        quick_buttons_layout = QGridLayout()
        quick_buttons_layout.setSpacing(12)
        
        quick_questions = [
            '如何提高数学成绩？',
            '英语语法怎么学？',
            '物理公式记不住怎么办？',
            '如何制定学习计划？'
        ]
        
        for i, question in enumerate(quick_questions):
            button = PrimaryPushButton(question)
            button.setFixedHeight(40)
            button.setMinimumWidth(160)
            button.clicked.connect(lambda checked, q=question: self.quick_question_clicked(q))
            quick_buttons_layout.addWidget(button, i // 2, i % 2)
        
        quick_questions_layout.addLayout(quick_buttons_layout)
        layout.addWidget(quick_questions_card)
        
        # 底部空间
        layout.addStretch()
    
    def add_user_message(self, text):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # 用户头像
        avatar = QLabel()
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.blue)
        avatar.setPixmap(pixmap)
        avatar.setFixedSize(40, 40)
        avatar.setStyleSheet('border-radius: 20px;')
        layout.addWidget(avatar, 0, Qt.AlignTop)
        
        # 消息气泡
        message_bubble = QWidget()
        # 根据主题设置颜色
        if isDarkTheme():
            message_bubble.setStyleSheet('''
                QWidget {
                    background-color: #0078D7;
                    border-radius: 16px;
                    border-bottom-left-radius: 4px;
                    padding: 12px 16px;
                }
            ''')
        else:
            message_bubble.setStyleSheet('''
                QWidget {
                    background-color: #0078D7;
                    border-radius: 16px;
                    border-bottom-left-radius: 4px;
                    padding: 12px 16px;
                }
            ''')
        message_layout = QVBoxLayout(message_bubble)
        message_browser = QTextBrowser()
        message_browser.setHtml(markdown(text))
        message_browser.setStyleSheet('''
            QTextBrowser {
                color: white;
                background: transparent;
                border: none;
                padding: 0;
                font-family: MiSans, Microsoft YaHei, Arial, sans-serif;
                font-size: 14px;
            }
        ''')
        message_browser.setMinimumWidth(200)
        message_browser.setMaximumWidth(500)
        message_layout.addWidget(message_browser)
        
        layout.addWidget(message_bubble)
        layout.addStretch()
        
        self.chat_layout.addWidget(widget)
        self.chat_widget.resize(self.chat_widget.sizeHint())
        
        # 滚动到底部
        QTimer.singleShot(100, lambda: self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum()))
    
    def add_ai_message(self, text):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        layout.addStretch()
        
        # 消息气泡
        message_bubble = QWidget()
        # 根据主题设置颜色
        if isDarkTheme():
            message_bubble.setStyleSheet('''
                QWidget {
                    background-color: #333333;
                    border-radius: 16px;
                    border-bottom-right-radius: 4px;
                    padding: 12px 16px;
                }
            ''')
        else:
            message_bubble.setStyleSheet('''
                QWidget {
                    background-color: #F1F1F1;
                    border-radius: 16px;
                    border-bottom-right-radius: 4px;
                    padding: 12px 16px;
                }
            ''')
        message_layout = QVBoxLayout(message_bubble)
        message_browser = QTextBrowser()
        message_browser.setHtml(markdown(text))
        # 根据主题设置文本颜色
        if isDarkTheme():
            message_browser.setStyleSheet('''
                QTextBrowser {
                    color: #FFFFFF;
                    background: transparent;
                    border: none;
                    padding: 0;
                    font-family: MiSans, Microsoft YaHei, Arial, sans-serif;
                    font-size: 14px;
                }
            ''')
        else:
            message_browser.setStyleSheet('''
                QTextBrowser {
                    color: #333333;
                    background: transparent;
                    border: none;
                    padding: 0;
                    font-family: MiSans, Microsoft YaHei, Arial, sans-serif;
                    font-size: 14px;
                }
            ''')
        message_browser.setMinimumWidth(200)
        message_browser.setMaximumWidth(500)
        message_layout.addWidget(message_browser)
        
        layout.addWidget(message_bubble)
        
        # AI头像
        avatar = QLabel()
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.green)
        avatar.setPixmap(pixmap)
        avatar.setFixedSize(40, 40)
        avatar.setStyleSheet('border-radius: 20px;')
        layout.addWidget(avatar, 0, Qt.AlignTop)
        
        self.chat_layout.addWidget(widget)
        self.chat_widget.resize(self.chat_widget.sizeHint())
        
        # 滚动到底部
        QTimer.singleShot(100, lambda: self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum()))
        
        return widget
    
    def add_loading_message(self):
        """添加加载状态消息"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        layout.addStretch()
        
        # 加载气泡
        loading_bubble = QWidget()
        # 根据主题设置颜色
        if isDarkTheme():
            loading_bubble.setStyleSheet('''
                background-color: #333333;
                border-radius: 16px;
                border-bottom-right-radius: 4px;
                padding: 12px 16px;
            ''')
        else:
            loading_bubble.setStyleSheet('''
                background-color: #F1F1F1;
                border-radius: 16px;
                border-bottom-right-radius: 4px;
                padding: 12px 16px;
            ''')
        loading_layout = QVBoxLayout(loading_bubble)
        loading_layout.setSpacing(8)
        
        # 加载文本
        loading_label = BodyLabel('AI正在思考...')
        # 根据主题设置文本颜色
        if isDarkTheme():
            loading_label.setStyleSheet('color: #FFFFFF;')
        else:
            loading_label.setStyleSheet('color: #333333;')
        loading_layout.addWidget(loading_label)
        
        # 进度环
        progress_ring = ProgressRing()
        progress_ring.setFixedSize(32, 32)
        loading_layout.addWidget(progress_ring, 0, Qt.AlignCenter)
        
        layout.addWidget(loading_bubble)
        
        # AI头像
        avatar = QLabel()
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.green)
        avatar.setPixmap(pixmap)
        avatar.setFixedSize(40, 40)
        avatar.setStyleSheet('border-radius: 20px;')
        layout.addWidget(avatar, 0, Qt.AlignTop)
        
        self.chat_layout.addWidget(widget)
        self.chat_widget.resize(self.chat_widget.sizeHint())
        self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())
        return widget
    
    def send_message(self):
        text = self.input_edit.toPlainText().strip()
        if text:
            # 添加用户消息
            self.add_user_message(text)
            
            # 清空输入
            self.input_edit.clear()
            
            # 显示加载状态
            loading_widget = self.add_loading_message()
            
            # 使用QTimer模拟异步请求
            QTimer.singleShot(100, lambda: self.get_ai_response(text, loading_widget))
    
    def quick_question_clicked(self, question):
        # 添加用户消息
        self.add_user_message(question)
        
        # 显示加载状态
        loading_widget = self.add_loading_message()
        
        # 使用QTimer模拟异步请求
        QTimer.singleShot(100, lambda: self.get_ai_response(question, loading_widget))
    
    def get_ai_response(self, question, loading_widget):
        """获取AI回复"""
        # 移除加载状态
        self.chat_layout.removeWidget(loading_widget)
        loading_widget.deleteLater()
        self.chat_widget.resize(self.chat_widget.sizeHint())
        
        # 使用OpenAI客户端获取回复
        if self.openai_client.is_configured():
            response = self.openai_client.get_response(question)
        else:
            # 如果未配置，使用模拟回复
            responses = {
                '如何提高数学成绩？': '提高数学成绩的关键是多练习和理解概念。建议：1. 理解基本概念和公式；2. 多做练习题，特别是错题；3. 建立错题本；4. 定期复习。',
                '英语语法怎么学？': '学习英语语法的方法：1. 系统学习语法规则；2. 通过例句理解用法；3. 多做语法练习；4. 在实际对话和写作中应用。',
                '物理公式记不住怎么办？': '记忆物理公式的技巧：1. 理解公式的推导过程；2. 知道每个符号的含义；3. 通过做题巩固记忆；4. 分类整理公式，找规律。',
                '如何制定学习计划？': '制定有效的学习计划：1. 设定明确的目标；2. 合理分配时间；3. 分解大任务为小任务；4. 留出休息和娱乐时间；5. 定期检查和调整计划。'
            }
            response = responses.get(question, '感谢你的问题！我正在思考如何给你一个满意的答案...')
        
        # 添加AI回复
        self.add_ai_message(response)
    
    def simulate_ai_response(self, question):
        # 简单的回复模拟
        responses = {
            '如何提高数学成绩？': '提高数学成绩的关键是多练习和理解概念。建议：1. 理解基本概念和公式；2. 多做练习题，特别是错题；3. 建立错题本；4. 定期复习。',
            '英语语法怎么学？': '学习英语语法的方法：1. 系统学习语法规则；2. 通过例句理解用法；3. 多做语法练习；4. 在实际对话和写作中应用。',
            '物理公式记不住怎么办？': '记忆物理公式的技巧：1. 理解公式的推导过程；2. 知道每个符号的含义；3. 通过做题巩固记忆；4. 分类整理公式，找规律。',
            '如何制定学习计划？': '制定有效的学习计划：1. 设定明确的目标；2. 合理分配时间；3. 分解大任务为小任务；4. 留出休息和娱乐时间；5. 定期检查和调整计划。'
        }
        
        response = responses.get(question, '感谢你的问题！我正在思考如何给你一个满意的答案...')
        self.add_ai_message(response)