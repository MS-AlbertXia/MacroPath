from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import (
    NavigationItemPosition,
    setTheme, Theme, FluentIcon, FluentWindow
)
from app.widgets.home_widget import HomeWidget
from app.widgets.ai_assistant_widget import AIAssistantWidget
from app.widgets.learning_path_widget import LearningPathWidget
from app.widgets.progress_widget import ProgressWidget
from app.widgets.settings_widget import SettingsWidget

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 700)
        self.setMinimumSize(800, 600)
        self.setWindowTitle('宏星慧学 - MacroSTAR Path')
        
        # 创建页面
        self.home_widget = HomeWidget(self)
        self.ai_assistant_widget = AIAssistantWidget(self)
        self.learning_path_widget = LearningPathWidget(self)
        self.progress_widget = ProgressWidget(self)
        self.settings_widget = SettingsWidget(self)
        
        # 初始化导航
        self.init_navigation()
        
        # 设置默认页面
        self.navigationInterface.setCurrentItem(self.home_widget.objectName())
    
    def init_navigation(self):
        # 添加导航项
        self.addSubInterface(
            self.home_widget,
            FluentIcon.HOME,
            '首页',
            position=NavigationItemPosition.TOP
        )
        
        self.addSubInterface(
            self.ai_assistant_widget,
            FluentIcon.IOT,
            'AI助手',
            position=NavigationItemPosition.TOP
        )
        
        self.addSubInterface(
            self.learning_path_widget,
            FluentIcon.EDUCATION,
            '学习路径',
            position=NavigationItemPosition.TOP
        )
        
        self.addSubInterface(
            self.progress_widget,
            FluentIcon.DEVELOPER_TOOLS,
            '学习进度',
            position=NavigationItemPosition.TOP
        )
        
        self.addSubInterface(
            self.settings_widget,
            FluentIcon.SETTING,
            '设置',
            position=NavigationItemPosition.BOTTOM
        )
