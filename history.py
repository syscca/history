import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QMessageBox, QFormLayout)
from PyQt5.QtCore import Qt

class ProfitCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.history_file = "history_log.txt"
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('跨境利润计算器')
        self.setGeometry(300, 300, 800, 600)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        
        # 输入区域
        form = QFormLayout()
        self.cost_cny = QLineEdit('3020')
        self.shipping_idr = QLineEdit('300000')
        self.sale_price_idr = QLineEdit('8999000')
        self.exchange_rate = QLineEdit('2250')
        self.platform_fee = QLineEdit('4.25')
        self.insurance_idr = QLineEdit('20000')
        self.bonus_idr = QLineEdit('50000')
        
        inputs = [
            ('进货价 (CNY)', self.cost_cny),
            ('物流费 (IDR)', self.shipping_idr),
            ('售价 (IDR)', self.sale_price_idr),
            ('汇率 (CNY/IDR)', self.exchange_rate),
            ('平台手续费 (%)', self.platform_fee),
            ('保险费 (IDR)', self.insurance_idr),
            ('员工分红 (IDR)', self.bonus_idr)
        ]
        
        for label, widget in inputs:
            form.addRow(QLabel(label), widget)
        
        # 按钮区域
        btn_calculate = QPushButton('计算利润')
        btn_calculate.clicked.connect(self.calculate_profit)
        btn_clear = QPushButton('清空记录')
        btn_clear.clicked.connect(self.clear_history)
        
        # 结果显示
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px; color: #2c3e50;")
        
        # 历史记录
        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.load_history()
        
        # 布局组合
        layout.addLayout(form)
        layout.addWidget(btn_calculate)
        layout.addWidget(self.result_label)
        layout.addWidget(QLabel('历史记录:'))
        layout.addWidget(self.history_display)
        layout.addWidget(btn_clear)
        
        main_widget.setLayout(layout)
    
    def calculate_profit(self):
        try:
            # 获取输入值
            cost_cny = float(self.cost_cny.text())
            shipping_idr = float(self.shipping_idr.text())
            sale_price_idr = float(self.sale_price_idr.text())
            exchange_rate = float(self.exchange_rate.text())
            platform_fee = float(self.platform_fee.text())
            insurance_idr = float(self.insurance_idr.text())
            bonus_idr = float(self.bonus_idr.text())
            
            # 计算成本
            cost_idr = cost_cny * exchange_rate
            platform_fee_idr = sale_price_idr * (platform_fee / 100)
            total_cost_idr = cost_idr + shipping_idr + insurance_idr + bonus_idr + platform_fee_idr
            
            # 计算利润
            profit_idr = sale_price_idr - total_cost_idr
            profit_cny = profit_idr / exchange_rate
            
            # 显示结果
            result_text = (f"印尼盾利润: {profit_idr:,.2f} IDR\n"
                          f"人民币利润: {profit_cny:,.2f} CNY")
            self.result_label.setText(result_text)
            
            # 保存记录
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = (f"[{timestamp}] 进货: {cost_cny}CNY | 售价: {sale_price_idr}IDR | "
                        f"利润: {profit_idr:,.2f}IDR | {profit_cny:,.2f}CNY\n")
            
            with open(self.history_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            self.load_history()
            
        except ValueError:
            QMessageBox.warning(self, '输入错误', '请输入有效的数字')
    
    def load_history(self):
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.history_display.setPlainText(f.read())
        except FileNotFoundError:
            pass
    
    def clear_history(self):
        open(self.history_file, 'w', encoding='utf-8').close()
        self.history_display.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProfitCalculator()
    ex.show()
    sys.exit(app.exec_())
