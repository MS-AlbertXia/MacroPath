import sys
from app.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator, setTheme, Theme
from PyQt5.QtCore import QTranslator, QLocale
from PyQt5.QtGui import QFont

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置全局字体为MiSans
    font = QFont('MiSans')
    app.setFont(font)
    
    # 设置全局字体样式表，确保所有组件都使用MiSans字体
    app.setStyleSheet('''
        * {
            font-family: MiSans, Microsoft YaHei, Arial, sans-serif;
        }
    ''')
    
    # 设置初始主题
    setTheme(Theme.AUTO)
    
    # 加载翻译
    translator = FluentTranslator(QLocale())
    app.installTranslator(translator)
    
    # 创建主窗口
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec_())