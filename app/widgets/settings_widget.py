from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from qfluentwidgets import (
    ScrollArea, CardWidget, TitleLabel, SubtitleLabel, BodyLabel,
    ComboBox, Slider, LineEdit, PrimaryPushButton, CheckBox,
    setTheme, Theme, InfoBar, InfoBarPosition
)

class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('settingsWidget')
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建滚动区域
        scroll_area = ScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet('background: transparent; border: none;')
        
        # 滚动内容 widget
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        scroll_content.setStyleSheet('background: transparent; border: none;')
        
        # 标题
        title = TitleLabel('设置')
        subtitle = BodyLabel('自定义你的学习助手，让它更符合你的需求。')
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        # 外观设置
        appearance_card = CardWidget(scroll_content)
        appearance_layout = QVBoxLayout(appearance_card)
        appearance_layout.setContentsMargins(20, 20, 20, 20)
        appearance_layout.setSpacing(15)
        
        appearance_title = SubtitleLabel('外观设置')
        appearance_layout.addWidget(appearance_title)
        
        # 主题设置
        theme_layout = QHBoxLayout()
        theme_layout.setSpacing(20)
        
        theme_label = BodyLabel('主题:')
        theme_label.setFixedWidth(80)
        
        self.theme_combo = ComboBox()
        self.theme_combo.addItems(['浅色模式', '深色模式', '跟随系统'])
        self.theme_combo.setFixedWidth(150)
        self.theme_combo.currentIndexChanged.connect(self.on_theme_changed)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        
        appearance_layout.addLayout(theme_layout)
        
        # 字体大小
        font_layout = QHBoxLayout()
        font_layout.setSpacing(20)
        
        font_label = BodyLabel('字体大小:')
        font_label.setFixedWidth(80)
        
        self.font_slider = Slider(Qt.Horizontal)
        self.font_slider.setRange(10, 20)
        self.font_slider.setValue(14)
        self.font_slider.setFixedWidth(200)
        
        self.font_value = BodyLabel('14px')
        self.font_value.setFixedWidth(50)
        self.font_slider.valueChanged.connect(lambda value: self.font_value.setText(f'{value}px'))
        
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_slider)
        font_layout.addWidget(self.font_value)
        font_layout.addStretch()
        
        appearance_layout.addLayout(font_layout)
        layout.addWidget(appearance_card)
        
        # 学习设置
        learning_card = CardWidget(scroll_content)
        learning_layout = QVBoxLayout(learning_card)
        learning_layout.setContentsMargins(20, 20, 20, 20)
        learning_layout.setSpacing(15)
        
        learning_title = SubtitleLabel('学习设置')
        learning_layout.addWidget(learning_title)
        
        # 每日学习目标
        daily_goal_layout = QHBoxLayout()
        daily_goal_layout.setSpacing(20)
        
        daily_goal_label = BodyLabel('每日学习目标:')
        daily_goal_label.setFixedWidth(120)
        
        self.daily_goal_edit = LineEdit()
        self.daily_goal_edit.setText('2小时')
        self.daily_goal_edit.setFixedWidth(100)
        
        daily_goal_layout.addWidget(daily_goal_label)
        daily_goal_layout.addWidget(self.daily_goal_edit)
        daily_goal_layout.addStretch()
        
        learning_layout.addLayout(daily_goal_layout)
        
        # 学习提醒
        reminder_layout = QHBoxLayout()
        reminder_layout.setSpacing(20)
        
        reminder_label = BodyLabel('学习提醒:')
        reminder_label.setFixedWidth(120)
        
        self.reminder_switch = CheckBox()
        self.reminder_switch.setChecked(True)
        
        reminder_layout.addWidget(reminder_label)
        reminder_layout.addWidget(self.reminder_switch)
        reminder_layout.addStretch()
        
        learning_layout.addLayout(reminder_layout)
        
        # 自动保存
        auto_save_layout = QHBoxLayout()
        auto_save_layout.setSpacing(20)
        
        auto_save_label = BodyLabel('自动保存:')
        auto_save_label.setFixedWidth(120)
        
        self.auto_save_switch = CheckBox()
        self.auto_save_switch.setChecked(True)
        
        auto_save_layout.addWidget(auto_save_label)
        auto_save_layout.addWidget(self.auto_save_switch)
        auto_save_layout.addStretch()
        
        learning_layout.addLayout(auto_save_layout)
        layout.addWidget(learning_card)
        
        # 账户设置
        account_card = CardWidget(scroll_content)
        account_layout = QVBoxLayout(account_card)
        account_layout.setContentsMargins(20, 20, 20, 20)
        account_layout.setSpacing(15)
        
        account_title = SubtitleLabel('账户设置')
        account_layout.addWidget(account_title)
        
        # 头像设置
        avatar_layout = QHBoxLayout()
        avatar_layout.setSpacing(20)
        
        avatar_label = BodyLabel('头像:')
        avatar_label.setFixedWidth(80)
        
        # 头像显示
        self.avatar_display = QLabel()
        self.avatar_display.setFixedSize(80, 80)
        self.avatar_display.setStyleSheet('border-radius: 40px; background-color: #E0E0E0;')
        
        # 从配置管理器中读取头像路径
        from app.utils.config_manager import config_manager
        avatar_path = config_manager.get_avatar_path()
        if avatar_path:
            pixmap = QPixmap(avatar_path)
            if not pixmap.isNull():
                self.avatar_display.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.avatar_display.setStyleSheet('border-radius: 40px;')
        
        # 选择头像按钮
        avatar_button = PrimaryPushButton('选择头像')
        avatar_button.setFixedWidth(100)
        avatar_button.clicked.connect(self.select_avatar)
        
        avatar_layout.addWidget(avatar_label)
        avatar_layout.addWidget(self.avatar_display)
        avatar_layout.addWidget(avatar_button)
        avatar_layout.addStretch()
        
        account_layout.addLayout(avatar_layout)
        
        # 用户名
        username_layout = QHBoxLayout()
        username_layout.setSpacing(20)
        
        username_label = BodyLabel('用户名:')
        username_label.setFixedWidth(80)
        
        self.username_edit = LineEdit()
        # 从配置管理器中读取用户名
        self.username_edit.setText(config_manager.get_username())
        self.username_edit.setFixedWidth(200)
        
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_edit)
        username_layout.addStretch()
        
        account_layout.addLayout(username_layout)
        
        # 邮箱
        email_layout = QHBoxLayout()
        email_layout.setSpacing(20)
        
        email_label = BodyLabel('邮箱:')
        email_label.setFixedWidth(80)
        
        self.email_edit = LineEdit()
        self.email_edit.setPlaceholderText('输入你的邮箱')
        self.email_edit.setFixedWidth(200)
        
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_edit)
        email_layout.addStretch()
        
        account_layout.addLayout(email_layout)
        
        # 保存按钮
        save_button = PrimaryPushButton('保存设置')
        save_button.setFixedWidth(120)
        save_button.clicked.connect(self.save_settings)
        account_layout.addWidget(save_button, 0, Qt.AlignRight)
        
        layout.addWidget(account_card)
        
        # OpenAI设置
        openai_card = CardWidget(scroll_content)
        openai_layout = QVBoxLayout(openai_card)
        openai_layout.setContentsMargins(20, 20, 20, 20)
        openai_layout.setSpacing(15)
        
        openai_title = SubtitleLabel('AI API设置')
        openai_layout.addWidget(openai_title)
        
        # API基础URL
        api_base_layout = QHBoxLayout()
        api_base_layout.setSpacing(15)
        
        api_base_label = BodyLabel('API地址:')
        api_base_label.setFixedWidth(80)
        
        self.api_base_edit = LineEdit()
        self.api_base_edit.setPlaceholderText('https://api.deepseek.com/v1')
        self.api_base_edit.setText('https://api.openai.com/v1')
        
        api_base_layout.addWidget(api_base_label)
        api_base_layout.addWidget(self.api_base_edit, 1)  # 添加拉伸因子
        api_base_layout.addStretch()
        
        openai_layout.addLayout(api_base_layout)
        
        # API密钥
        api_key_layout = QHBoxLayout()
        api_key_layout.setSpacing(15)
        
        api_key_label = BodyLabel('API密钥:')
        api_key_label.setFixedWidth(80)
        
        self.api_key_edit = LineEdit()
        self.api_key_edit.setPlaceholderText('sk-...')
        self.api_key_edit.setEchoMode(LineEdit.Password)
        
        api_key_layout.addWidget(api_key_label)
        api_key_layout.addWidget(self.api_key_edit, 1)  # 添加拉伸因子
        api_key_layout.addStretch()
        
        openai_layout.addLayout(api_key_layout)
        
        # 模型选择
        model_layout = QHBoxLayout()
        model_layout.setSpacing(15)
        
        model_label = BodyLabel('模型:')
        model_label.setFixedWidth(80)
        
        self.model_edit = LineEdit()
        self.model_edit.setPlaceholderText('输入模型名称（例如：deepseek-chat）')
        
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_edit, 1)
        model_layout.addStretch()
        
        openai_layout.addLayout(model_layout)
        
        # 温度设置
        temperature_layout = QHBoxLayout()
        temperature_layout.setSpacing(15)
        
        temperature_label = BodyLabel('温度:')
        temperature_label.setFixedWidth(80)
        
        self.temperature_slider = Slider(Qt.Horizontal)
        self.temperature_slider.setRange(0, 100)
        self.temperature_slider.setValue(70)
        
        self.temperature_value = BodyLabel('0.7')
        self.temperature_value.setFixedWidth(50)
        self.temperature_slider.valueChanged.connect(lambda value: self.temperature_value.setText(f'{value/100:.1f}'))
        
        temperature_layout.addWidget(temperature_label)
        temperature_layout.addWidget(self.temperature_slider, 1)  # 添加拉伸因子
        temperature_layout.addWidget(self.temperature_value)
        temperature_layout.addStretch()
        
        openai_layout.addLayout(temperature_layout)
        
        # 保存按钮
        openai_save_button = PrimaryPushButton('保存AI API设置')
        openai_save_button.setFixedWidth(150)
        openai_save_button.clicked.connect(self.save_openai_settings)
        openai_layout.addWidget(openai_save_button, 0, Qt.AlignRight)
        
        layout.addWidget(openai_card)
        
        # 关于
        about_card = CardWidget(scroll_content)
        about_layout = QVBoxLayout(about_card)
        about_layout.setContentsMargins(20, 20, 20, 20)
        about_layout.setSpacing(15)
        
        about_title = SubtitleLabel('关于')
        about_layout.addWidget(about_title)
        app_name = BodyLabel('宏星慧学 | MacroSTAR Path v1.0.0')
        app_desc = BodyLabel('以星为引，以智为途')
        app_cont = BodyLabel('感谢为本程序贡献的所有单位及个人')
        app_from = BodyLabel('本作品使用了以下开源项目：DeepSeek API、OpenAI API、PyQt5、QFluentWidgets')
        app_lice = BodyLabel('本作品基于GPL v3.0协议开源')
        app_copyright = BodyLabel('© 2026 宏星工作室 保留所有权利')
        
        about_layout.addWidget(app_name)
        about_layout.addWidget(app_desc)
        about_layout.addWidget(app_cont)
        about_layout.addWidget(app_from)
        about_layout.addWidget(app_lice)
        about_layout.addWidget(app_copyright)
        
        layout.addWidget(about_card)
        
        # 底部空间
        layout.addStretch()
        
        # 设置滚动区域内容
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
    
    def on_theme_changed(self, index):
        if index == 0:
            setTheme(Theme.LIGHT)
        elif index == 1:
            setTheme(Theme.DARK)
        else:
            setTheme(Theme.AUTO)
    
    def save_settings(self):
        """保存账户设置"""
        from app.utils.config_manager import config_manager
        
        # 保存账户设置
        username = self.username_edit.text().strip()
        email = self.email_edit.text().strip()
        daily_goal = self.daily_goal_edit.text().strip()
        reminder_enabled = self.reminder_switch.isChecked()
        auto_save_enabled = self.auto_save_switch.isChecked()
        
        # 使用配置管理器保存设置
        config_manager.set_username(username)
        config_manager.set_email(email)
        config_manager.set_daily_goal(daily_goal)
        config_manager.set_reminder_enabled(reminder_enabled)
        config_manager.set_auto_save_enabled(auto_save_enabled)
        
        # 显示保存成功信息
        InfoBar.success(
            title='成功',
            content='账户设置保存成功',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
        
        # 显示重启提示
        InfoBar.warning(
            title='提示',
            content='修改用户名后需要重启程序才能在首页看到更新',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self
        )
    
    def select_avatar(self):
        """选择头像"""
        # 打开文件对话框
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle('选择头像')
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilters(['图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)', '所有文件 (*)'])
        
        if file_dialog.exec_() == QFileDialog.Accepted:
            # 获取选择的文件路径
            avatar_path = file_dialog.selectedFiles()[0]
            
            # 验证文件是否是有效的图片
            pixmap = QPixmap(avatar_path)
            if pixmap.isNull():
                InfoBar.error(
                    title='错误',
                    content='选择的文件不是有效的图片',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3000,
                    parent=self
                )
                return
            
            # 更新头像显示
            self.avatar_display.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.avatar_display.setStyleSheet('border-radius: 40px;')
            
            # 保存头像路径到配置管理器
            from app.utils.config_manager import config_manager
            config_manager.set_avatar_path(avatar_path)
            
            # 显示成功信息
            InfoBar.success(
                title='成功',
                content='头像设置成功',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
    
    def save_openai_settings(self):
        """保存AI API设置"""
        from app.utils.openai_client import OpenAIClient
        
        api_key = self.api_key_edit.text().strip()
        api_base = self.api_base_edit.text().strip()
        model = self.model_edit.text().strip()
        temperature = float(self.temperature_value.text())
        
        client = OpenAIClient()
        success = client.save_config(api_key, model, temperature, api_base)
        
        if success:
            # 显示成功信息
            InfoBar.success(
                title='成功',
                content='AI API设置保存成功',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
        else:
            # 显示失败信息
            InfoBar.error(
                title='失败',
                content='AI API设置保存失败',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )