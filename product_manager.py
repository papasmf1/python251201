import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt

class ProductManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_db()
        self.init_ui()
        self.current_id = None
        
    def init_db(self):
        """SQLite 데이터베이스 초기화"""
        self.conn = sqlite3.connect('MyProducts.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                prodID INTEGER PRIMARY KEY AUTOINCREMENT,
                prodName TEXT NOT NULL,
                prodPrice INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle('전자제품 데이터 관리')
        self.setGeometry(100, 100, 700, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # 상단 입력 영역
        input_layout = QHBoxLayout()
        
        input_layout.addWidget(QLabel('제품명:'))
        self.prod_name = QLineEdit()
        input_layout.addWidget(self.prod_name)
        
        input_layout.addWidget(QLabel('가격:'))
        self.prod_price = QLineEdit()
        input_layout.addWidget(self.prod_price)
        
        main_layout.addLayout(input_layout)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        btn_add = QPushButton('입력')
        btn_add.clicked.connect(self.add_product)
        button_layout.addWidget(btn_add)
        
        btn_update = QPushButton('수정')
        btn_update.clicked.connect(self.update_product)
        button_layout.addWidget(btn_update)
        
        btn_delete = QPushButton('삭제')
        btn_delete.clicked.connect(self.delete_product)
        button_layout.addWidget(btn_delete)
        
        btn_search = QPushButton('검색')
        btn_search.clicked.connect(self.search_product)
        button_layout.addWidget(btn_search)
        
        btn_refresh = QPushButton('새로고침')
        btn_refresh.clicked.connect(self.load_products)
        button_layout.addWidget(btn_refresh)
        
        main_layout.addLayout(button_layout)
        
        # 테이블 영역
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', '제품명', '가격'])
        self.table.cellDoubleClicked.connect(self.on_table_double_click)
        main_layout.addWidget(self.table)
        
        central_widget.setLayout(main_layout)
        
        # 초기 데이터 로드
        self.load_products()
    
    def add_product(self):
        """제품 추가"""
        try:
            name = self.prod_name.text().strip()
            price = int(self.prod_price.text())
            
            if not name:
                QMessageBox.warning(self, '경고', '제품명을 입력하세요.')
                return
            
            self.cursor.execute('INSERT INTO Products (prodName, prodPrice) VALUES (?, ?)',
                              (name, price))
            self.conn.commit()
            
            QMessageBox.information(self, '성공', '제품이 추가되었습니다.')
            self.clear_input()
            self.load_products()
        except ValueError:
            QMessageBox.warning(self, '경고', '가격은 숫자를 입력하세요.')
    
    def update_product(self):
        """제품 수정"""
        try:
            if self.current_id is None:
                QMessageBox.warning(self, '경고', '수정할 제품을 선택하세요.')
                return
            
            name = self.prod_name.text().strip()
            price = int(self.prod_price.text())
            
            if not name:
                QMessageBox.warning(self, '경고', '제품명을 입력하세요.')
                return
            
            self.cursor.execute('UPDATE Products SET prodName = ?, prodPrice = ? WHERE prodID = ?',
                              (name, price, self.current_id))
            self.conn.commit()
            
            QMessageBox.information(self, '성공', '제품이 수정되었습니다.')
            self.clear_input()
            self.load_products()
        except ValueError:
            QMessageBox.warning(self, '경고', '가격은 숫자를 입력하세요.')
    
    def delete_product(self):
        """제품 삭제"""
        try:
            if self.current_id is None:
                QMessageBox.warning(self, '경고', '삭제할 제품을 선택하세요.')
                return
            
            reply = QMessageBox.question(self, '확인', '정말 삭제하시겠습니까?',
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.cursor.execute('DELETE FROM Products WHERE prodID = ?', (self.current_id,))
                self.conn.commit()
                
                QMessageBox.information(self, '성공', '제품이 삭제되었습니다.')
                self.clear_input()
                self.load_products()
        except Exception as e:
            QMessageBox.critical(self, '오류', f'삭제 실패: {str(e)}')
    
    def search_product(self):
        """제품 검색"""
        try:
            name = self.prod_name.text().strip()
            
            if not name:
                QMessageBox.warning(self, '경고', '검색할 제품명을 입력하세요.')
                return
            
            self.cursor.execute('SELECT * FROM Products WHERE prodName LIKE ?', ('%' + name + '%',))
            rows = self.cursor.fetchall()
            
            self.table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, '오류', f'검색 실패: {str(e)}')
    
    def load_products(self):
        """모든 제품 로드"""
        try:
            self.cursor.execute('SELECT * FROM Products')
            rows = self.cursor.fetchall()
            
            self.table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
            
            self.clear_input()
        except Exception as e:
            QMessageBox.critical(self, '오류', f'로드 실패: {str(e)}')
    
    def on_table_double_click(self, row, column):
        """테이블 행 더블클릭"""
        prod_id = self.table.item(row, 0).text()
        prod_name = self.table.item(row, 1).text()
        prod_price = self.table.item(row, 2).text()
        
        self.current_id = int(prod_id)
        self.prod_name.setText(prod_name)
        self.prod_price.setText(prod_price)
    
    def clear_input(self):
        """입력창 초기화"""
        self.prod_name.clear()
        self.prod_price.clear()
        self.current_id = None
    
    def closeEvent(self, event):
        """프로그램 종료"""
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = ProductManager()
    manager.show()
    sys.exit(app.exec_())