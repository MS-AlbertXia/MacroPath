from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from qfluentwidgets import (
    CardWidget, TitleLabel, SubtitleLabel, BodyLabel,
    PrimaryPushButton, ProgressRing, ScrollArea
)

class HomeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('homeWidget')
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 欢迎区域
        welcome_card = CardWidget(self)
        welcome_layout = QHBoxLayout(welcome_card)
        welcome_layout.setContentsMargins(20, 20, 20, 20)
        
        # 头像
        avatar = QLabel()
        avatar.setFixedSize(80, 80)
        
        # 从配置管理器中读取头像路径
        from app.utils.config_manager import config_manager
        avatar_path = config_manager.get_avatar_path()
        if avatar_path:
            pixmap = QPixmap(avatar_path)
            if not pixmap.isNull():
                avatar.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                avatar.setStyleSheet('border-radius: 40px;')
            else:
                avatar.setStyleSheet('border-radius: 40px; background-color: #0078D7;')
        else:
            avatar.setStyleSheet('border-radius: 40px; background-color: #0078D7;')
        
        welcome_layout.addWidget(avatar, 0, Qt.AlignTop)
        
        # 欢迎信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)
        
        # 从配置管理器中读取用户名
        from app.utils.config_manager import config_manager
        username = config_manager.get_username()
        self.welcome_title = TitleLabel(f'欢迎回来！{username}')
        welcome_subtitle = SubtitleLabel('今天的学习计划准备好了吗？')
        welcome_body = BodyLabel('让我们一起开始今天的学习之旅吧！')
        
        info_layout.addWidget(self.welcome_title)
        info_layout.addWidget(welcome_subtitle)
        info_layout.addWidget(welcome_body)
        
        start_button = PrimaryPushButton('开始学习')
        start_button.setFixedWidth(120)
        info_layout.addWidget(start_button, 0, Qt.AlignLeft)
        
        welcome_layout.addLayout(info_layout)
        layout.addWidget(welcome_card)
        
        # 学习概览
        overview_card = CardWidget(self)
        overview_layout = QVBoxLayout(overview_card)
        overview_layout.setContentsMargins(20, 20, 20, 20)
        overview_layout.setSpacing(15)
        
        overview_title = SubtitleLabel('学习概览')
        overview_layout.addWidget(overview_title)
        
        # 概览统计
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(40)
        
        # 学习时长
        time_stats = self.create_stat_item('今日学习', '2小时30分钟', 65)
        stats_layout.addWidget(time_stats)
        
        # 完成任务
        task_stats = self.create_stat_item('完成任务', '5个', 80)
        stats_layout.addWidget(task_stats)
        
        # 掌握知识点
        knowledge_stats = self.create_stat_item('掌握知识点', '12个', 70)
        stats_layout.addWidget(knowledge_stats)
        
        overview_layout.addLayout(stats_layout)
        layout.addWidget(overview_card)
        
        # 推荐学习
        recommended_card = CardWidget(self)
        recommended_layout = QVBoxLayout(recommended_card)
        recommended_layout.setContentsMargins(20, 20, 20, 20)
        recommended_layout.setSpacing(15)
        
        recommended_title = SubtitleLabel('推荐学习')
        recommended_layout.addWidget(recommended_title)
        
        # 推荐内容
        recommend_item1 = self.create_recommend_item('数学 - 二次函数', '巩固二次函数的性质和应用')
        recommended_layout.addWidget(recommend_item1)
        
        recommend_item2 = self.create_recommend_item('英语 - 阅读理解', '提高阅读理解能力和词汇量')
        recommended_layout.addWidget(recommend_item2)
        
        recommend_item3 = self.create_recommend_item('物理 - 力学基础', '复习牛顿运动定律')
        recommended_layout.addWidget(recommend_item3)
        
        layout.addWidget(recommended_card)
        
        # 底部空间
        layout.addStretch()
    
    def showEvent(self, event):
        try:
            from app.utils.config_manager import config_manager
            username = config_manager.get_username()
            self.welcome_title.setText(f'欢迎回来！{username}')
        except Exception:
            pass
        super().showEvent(event)
    
    def create_stat_item(self, title, value, progress):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        
        label = BodyLabel(title)
        value_label = TitleLabel(value)
        progress_ring = ProgressRing()
        progress_ring.setFixedSize(80, 80)
        progress_ring.setValue(progress)
        
        layout.addWidget(label)
        layout.addWidget(value_label)
        layout.addWidget(progress_ring, 0, Qt.AlignCenter)
        
        return widget
    
    def create_recommend_item(self, title, description):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(20)
        
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        title_label = SubtitleLabel(title)
        desc_label = BodyLabel(description)
        desc_label.setWordWrap(True)
        
        info_layout.addWidget(title_label)
        info_layout.addWidget(desc_label)
        
        start_button = PrimaryPushButton('开始学习')
        start_button.setFixedWidth(100)
        
        layout.addLayout(info_layout)
        layout.addWidget(start_button, 0, Qt.AlignRight | Qt.AlignVCenter)
        
        return widget
