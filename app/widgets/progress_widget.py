from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem
from qfluentwidgets import (
    CardWidget, TitleLabel, SubtitleLabel, BodyLabel, ScrollArea, 
    ProgressBar, PrimaryPushButton, ProgressRing, TableWidget
)
class ProgressWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('progressWidget')
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 创建滚动区域
        scroll_area = ScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet('background: transparent; border: none;')
        
        # 滚动内容 widget
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        scroll_layout.setContentsMargins(30, 30, 30, 30)
        scroll_content.setStyleSheet('background: transparent; border: none;')
        
        # 标题
        title = TitleLabel('学习进度')
        subtitle = BodyLabel('查看你的学习数据和进步情况。')
        scroll_layout.addWidget(title)
        scroll_layout.addWidget(subtitle)
        
        # 学习统计
        stats_card = CardWidget(scroll_content)
        stats_layout = QVBoxLayout(stats_card)
        stats_layout.setContentsMargins(20, 20, 20, 20)
        
        stats_title = SubtitleLabel('学习统计')
        stats_layout.addWidget(stats_title)
        
        # 统计数据
        stats_grid = QHBoxLayout()
        stats_grid.setSpacing(40)
        
        # 总学习时长
        time_stats = self.create_stats_item('总学习时长', '48小时', 60)
        stats_grid.addWidget(time_stats)
        
        # 完成任务数
        task_stats = self.create_stats_item('完成任务', '120个', 75)
        stats_grid.addWidget(task_stats)
        
        # 掌握知识点
        knowledge_stats = self.create_stats_item('掌握知识点', '85个', 55)
        stats_grid.addWidget(knowledge_stats)
        
        # 正确率
        accuracy_stats = self.create_stats_item('平均正确率', '82%', 82)
        stats_grid.addWidget(accuracy_stats)
        
        stats_layout.addLayout(stats_grid)
        scroll_layout.addWidget(stats_card)
        
        # 学科进度
        subjects_card = CardWidget(scroll_content)
        subjects_layout = QVBoxLayout(subjects_card)
        subjects_layout.setContentsMargins(20, 20, 20, 20)
        
        subjects_title = SubtitleLabel('学科进度')
        subjects_layout.addWidget(subjects_title)
        
        # 学科列表
        subjects = [
            {'name': '数学', 'progress': 70},
            {'name': '英语', 'progress': 85},
            {'name': '物理', 'progress': 60},
            {'name': '化学', 'progress': 75},
            {'name': '生物', 'progress': 65}
        ]
        
        for subject in subjects:
            subject_widget = self.create_subject_item(subject['name'], subject['progress'])
            subjects_layout.addWidget(subject_widget)
        
        scroll_layout.addWidget(subjects_card)
        
        # 最近学习记录
        history_card = CardWidget(scroll_content)
        history_layout = QVBoxLayout(history_card)
        history_layout.setContentsMargins(20, 20, 20, 20)
        
        history_title = SubtitleLabel('最近学习记录')
        history_layout.addWidget(history_title)
        
        # 学习记录表
        self.history_table = TableWidget()
        self.history_table.setRowCount(5)
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(['日期', '学科', '内容', '时长'])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        
        # 填充数据
        records = [
            ['2026-02-23', '数学', '二次函数练习', '1小时30分钟'],
            ['2026-02-22', '英语', '阅读理解', '1小时'],
            ['2026-02-21', '物理', '力学实验', '2小时'],
            ['2026-02-20', '化学', '化学反应方程式', '45分钟'],
            ['2026-02-19', '数学', '几何证明', '1小时15分钟']
        ]
        
        for i, record in enumerate(records):
            for j, item in enumerate(record):
                self.history_table.setItem(i, j, QTableWidgetItem(item))
        
        self.history_table.setFixedHeight(200)
        history_layout.addWidget(self.history_table)
        
        scroll_layout.addWidget(history_card)
        
        # 底部空间
        scroll_layout.addStretch()

        # 设置滚动区域内容
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
    
    def create_step_item(self, step_number, title, description, progress):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        num_label = TitleLabel(str(step_number))
        title_label = SubtitleLabel(title)
        desc_label = BodyLabel(description)
        bar = ProgressBar()
        bar.setValue(progress)
        
        layout.addWidget(num_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addWidget(bar)
        
        return widget

    def create_stats_item(self, title, value, progress):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = BodyLabel(title)
        value_label = TitleLabel(value)
        progress_ring = ProgressRing()
        progress_ring.setFixedSize(80, 80)
        progress_ring.setValue(progress)
        
        layout.addWidget(label, 0, Qt.AlignCenter)
        layout.addWidget(value_label, 0, Qt.AlignCenter)
        layout.addWidget(progress_ring, 0, Qt.AlignCenter)
        
        return widget
    
    def create_subject_item(self, name, progress):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 10, 0, 10)
        
        # 学科名称
        name_label = BodyLabel(name)
        name_label.setFixedWidth(80)
        
        # 进度条
        progress_bar = ProgressBar()
        progress_bar.setValue(progress)
        progress_bar.setFixedHeight(8)
        
        # 进度百分比
        progress_label = BodyLabel(f'{progress}%')
        progress_label.setFixedWidth(50)
        
        layout.addWidget(name_label)
        layout.addWidget(progress_bar)
        layout.addWidget(progress_label)
        
        return widget