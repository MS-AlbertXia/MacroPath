from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup
from qfluentwidgets import (
    ScrollArea, CardWidget, TitleLabel, SubtitleLabel, BodyLabel,
    PrimaryPushButton, RadioButton, CheckBox, ProgressBar
)

class LearningPathWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('learningPathWidget')
        
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
        title = TitleLabel('学习路径')
        subtitle = BodyLabel('根据你的学习目标和当前水平，我们为你定制了个性化的学习路径。')
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        # 学习目标选择
        goal_card = CardWidget(scroll_content)
        goal_layout = QVBoxLayout(goal_card)
        goal_layout.setContentsMargins(20, 20, 20, 20)
        
        goal_title = SubtitleLabel('选择学习目标')
        goal_layout.addWidget(goal_title)
        
        goals = ['期末考试复习', '中考备考', '高考冲刺', '竞赛准备', '兴趣学习']
        for goal in goals:
            radio_button = RadioButton(goal)
            goal_layout.addWidget(radio_button)
        
        layout.addWidget(goal_card)
        
        # 学习路径
        path_card = CardWidget(scroll_content)
        path_layout = QVBoxLayout(path_card)
        path_layout.setContentsMargins(20, 20, 20, 20)
        
        path_title = SubtitleLabel('推荐学习路径')
        path_layout.addWidget(path_title)
        
        # 路径步骤
        steps = [
            {'title': '基础概念', 'description': '掌握基本概念和定义', 'progress': 80},
            {'title': '核心知识点', 'description': '学习重要的知识点和公式', 'progress': 60},
            {'title': '解题技巧', 'description': '掌握各种题型的解题方法', 'progress': 40},
            {'title': '综合练习', 'description': '通过综合练习巩固知识', 'progress': 20},
            {'title': '模拟测试', 'description': '进行模拟测试，检验学习成果', 'progress': 0}
        ]
        
        for i, step in enumerate(steps):
            step_widget = self.create_step_item(i + 1, step['title'], step['description'], step['progress'])
            path_layout.addWidget(step_widget)
        
        layout.addWidget(path_card)
        
        # 学习资源
        resources_card = CardWidget(scroll_content)
        resources_layout = QVBoxLayout(resources_card)
        resources_layout.setContentsMargins(20, 20, 20, 20)
        
        resources_title = SubtitleLabel('推荐学习资源')
        resources_layout.addWidget(resources_title)
        
        resources = [
            {'name': '数学基础教程', 'type': '视频课程', 'progress': '3/10课时'},
            {'name': '英语词汇手册', 'type': '电子书', 'progress': '25/100页'},
            {'name': '物理实验视频', 'type': '实验教程', 'progress': '未开始'},
            {'name': '化学公式大全', 'type': 'PDF文档', 'progress': '未开始'}
        ]
        
        for resource in resources:
            resource_widget = self.create_resource_item(resource['name'], resource['type'], resource['progress'])
            resources_layout.addWidget(resource_widget)
        
        layout.addWidget(resources_card)
        
        # 底部空间
        layout.addStretch()
        
        # 设置滚动区域内容
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
    
    def create_step_item(self, step_number, title, description, progress):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 步骤标题
        step_layout = QHBoxLayout()
        step_label = BodyLabel(f'Step {step_number}: {title}')
        step_label.setStyleSheet('font-weight: bold;')
        
        status = '进行中' if 0 < progress < 100 else '未开始' if progress == 0 else '已完成'
        status_label = BodyLabel(status)
        
        step_layout.addWidget(step_label)
        step_layout.addStretch()
        step_layout.addWidget(status_label)
        
        layout.addLayout(step_layout)
        
        # 步骤描述
        desc_label = BodyLabel(description)
        layout.addWidget(desc_label)
        
        # 进度条
        progress_bar = ProgressBar()
        progress_bar.setValue(progress)
        progress_bar.setFixedHeight(8)
        layout.addWidget(progress_bar)
        
        return widget
    
    def create_resource_item(self, name, type, progress):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 10, 0, 10)
        
        # 资源信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        name_label = BodyLabel(name)
        name_label.setStyleSheet('font-weight: bold;')
        
        type_label = BodyLabel(f'类型: {type}')
        progress_label = BodyLabel(f'进度: {progress}')
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(type_label)
        info_layout.addWidget(progress_label)
        
        # 操作按钮
        action_button = PrimaryPushButton('开始学习')
        action_button.setFixedWidth(100)
        
        layout.addLayout(info_layout)
        layout.addWidget(action_button, 0, Qt.AlignRight | Qt.AlignVCenter)
        
        return widget