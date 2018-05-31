import os
import sys
import random
import io
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QAction, qApp, QGridLayout, QLineEdit, QLabel, QMessageBox,QDialog, QApplication, QMainWindow, QFileDialog, QWidget
def NOD(a,b):
    while (a!=0) and (b!=0):
        if a>b:
            a=a%b
        else:
            b=b%a
    return (a+b)
def Evklid(a,b):#Расширенный алгоритм евклида
    div=[]
    a_original=a
    while(a%b!=0):
        div.append(a//b) #Запоминаем значение целочисленного деления на каждом шагу
        c=a%b
        a=b
        b=c
    x=0
    y=1
    for i in reversed(div): #Идём в обратном напрваление списка, и находим значения x и y
        temp=y
        y=x-y*i
        x=temp
    d=y%a_original
    return d
def to_a_degree(m,e,n):#алгоритм возведения в степень (вычисляем m^e mod n)
    h=1
    while (e):
        if e%2==0:#Проверка числа на чётность(Вместо перевода в двоичную систему)
            e/=2 #Так как число чётное, то можно "спустится" в два раза ниже
            m=(m*m)%n #Находим значение на текущем шаге
        else:
            e-=1 #Так как число нечётное, то "спускаемся" к ближайшему чётному числу 
            h=(h*m)%n #Находим значение на текущем шаге
    return h
def resheto_Atkin():
    limit=1000
    sqr_lim=int(limit**0.5)
    prime_boolean=[]
    for i in range(limit+1):
        prime_boolean.append(False)
    #Инициализация решета
    x=0 #Инициализация нечётного числа х
    for i in range(1,sqr_lim+1):
        x+=2*i-1 #Переход к следующему нечётному числу х
        y=0 #Инициализация нечётного числа у
        for j in range(1,sqr_lim+1):
            y+=2*j-1 #Переход к следующему нечётному числу y
            n=4*x+y
            if n<=limit and (n%12==1 or n%12==5):#проверки для уравнения 4*x+y 
                prime_boolean[n]=not prime_boolean[n]
            n=3*x+y
            if n<=limit and n%12==7: #проверки для уравнения 3*x+y 
                prime_boolean[n]=not prime_boolean[n]
            n=3*x-y
            if i>j and n<=limit and n%12==11: #проверки для уравнения 3*x-y 
                prime_boolean[n]=not prime_boolean[n]
    for i in range(5,sqr_lim+1): #Проверка на не является ли квадратом какого-то числа
        if prime_boolean[i]:
            n=i*i
            for j in range(n,limit+1,n):
                prime_boolean[j]=False
    prime_numbers=[]
    prime_boolean[2]=True
    prime_boolean[3]=True
    for i in range(100,limit+1):#Присваивание списку элементы простых чисел 
        if prime_boolean[i]:
            prime_numbers.append(i)
    return(prime_numbers)
#######################################################
#######################################################
#######################################################
class Notepad(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text=QTextEdit(self)
        self.clr_btn=QPushButton('New') #Создаём конопочки
        self.sav_btn=QPushButton('Save')
        self.opn_btn=QPushButton('Open')
        self.shifrWin = pq_shifr_widget(self)
        self.deshifrWin = pq_deshifr_widget(self)
        self.init_ui()

    def init_ui(self):
        #Создаём лейауты
        v_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        btn_layout.addWidget(self.clr_btn) #Добавляем кнопочкив лейаут
        btn_layout.addWidget(self.sav_btn)
        btn_layout.addWidget(self.opn_btn)
        v_layout.addWidget(self.text)

        v_layout.addLayout(btn_layout)
        self.sav_btn.clicked.connect(self.save_text)
        self.clr_btn.clicked.connect(self.clear_text)
        self.opn_btn.clicked.connect(self.open_text)


        self.setLayout(v_layout)
        self.setWindowTitle('Kirill TextEdit')
    
    
    def shifr(self): #Нажатие на кнопку Enter
        self.text_t_s= self.text.toPlainText()
        self.p=0
        self.q=0
        self.new_shifred=''
        self.shifrWin.show()

    def shifr_text(self):
            for i in range(len(self.text_t_s)):
                chisl_form=(to_a_degree(ord(self.text_t_s[i]),self.e,self.p*self.q))
                self.new_shifred+=chr(chisl_form)
            filename = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))
            if filename[0]!='':
                with io.open(filename[0], 'w',encoding="utf-8") as f:
                    #for i in self.new_shifred:
                    f.write(self.new_shifred)
                    
    def deshifr(self):
        self.text_t_s= list(self.text.toPlainText())
        self.p=0
        self.q=0
        self.new_deshifred=[]
        self.deshifrWin.show()
    def deshifr_text(self):
        f=(self.p-1)*(self.q-1)
        d=Evklid(f,self.e)
        for i in range(len(self.text_t_s)):
            self.new_deshifred.append(chr(to_a_degree(ord(self.text_t_s[i]),d,self.p*self.q)))
        self.text.setText(''.join(self.new_deshifred))      

    def save_text(self): #Нажатие на кнопку Save
        encrypt_msg=QMessageBox()
        encrypt_msg.setWindowTitle('Encrypt Question')
        encrypt_msg.setText('You are saving the text')
        encrypt_msg.setInformativeText('Do you want to encrypt it?')
        encrypt_msg.setIcon(QMessageBox.Question)
        result=encrypt_msg.addButton(QMessageBox.Yes)
        encrypt_msg.addButton(QMessageBox.No)
        encrypt_msg.exec()
        if encrypt_msg.clickedButton() == result:
            self.shifr()
        else:
            filename = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))
            if filename[0]!='':
                with io.open(filename[0], 'w',encoding="utf-8") as f:
                    my_text = self.text.toPlainText()
                    f.write(my_text)

    def open_text(self): #Нажатие на кнопку Open
        filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        if filename[0]!='':
            with io.open(filename[0], 'r',encoding="utf-8") as f:
                file_text = f.read()
                self.text.setText(file_text)
            decrypt_msg=QMessageBox()
            decrypt_msg.setWindowTitle('Decrypt Question')
            decrypt_msg.setText('You have opened the text')
            decrypt_msg.setInformativeText('Do you want to decrypt it?')
            decrypt_msg.setIcon(QMessageBox.Question)
            result=decrypt_msg.addButton(QMessageBox.Yes)
            decrypt_msg.addButton(QMessageBox.No)
            decrypt_msg.exec()
            if decrypt_msg.clickedButton() == result:
                self.deshifr()
    def clear_text(self): #Нажатие на кнопку Clear
        clear_msg=QMessageBox()
        clear_msg.setWindowTitle('Creating new text')
        clear_msg.setText('Do you want to save this file?')
        clear_msg.setIcon(QMessageBox.Question)
        result=clear_msg.addButton(QMessageBox.Yes)
        clear_msg.addButton(QMessageBox.No)
        clear_msg.exec()
        if clear_msg.clickedButton()==result:
            self.save_text()
        self.text.clear()
#######################################################
#######################################################
#######################################################
class Writer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)

        self.form_widget = Notepad()
        self.setCentralWidget(self.form_widget)

        self.init_ui()

    def init_ui(self):
        bar = self.menuBar()
        file = bar.addMenu('File')

        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')

        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')

        open_action = QAction('&Open', self)
        open_action.setShortcut('Ctrl+O')

        quit_action = QAction('&Quit', self)

        file.addAction(new_action)
        file.addAction(save_action)
        file.addAction(open_action)
        file.addAction(quit_action)

        quit_action.triggered.connect(self.quit_trigger)
        file.triggered.connect(self.respond)
        self.setWindowTitle('Text Editor')
        self.show()
    
    def quit_trigger(self):
        qApp.quit()

    def respond(self, q):
        signal = q.text()

        if signal == 'New':
            self.form_widget.clear_text()
        elif signal == '&Open':
            self.form_widget.open_text()
        elif signal == '&Save':
            self.form_widget.save_text()

#######################################################
#######################################################
#######################################################
class pq_shifr_widget(QDialog):
    def __init__(self,root,**kwargs):
        super().__init__(root, **kwargs)
        self.MainWindow=root
        self.enterPQ_btn=QPushButton('Get encryption keys')
        self.savePQ_btn=QPushButton('Save encrypted')
        self.value_shifr=QLabel()
        self.pq_ui()
    def pq_ui(self):

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        number_shifr = QLabel('Encryption key') #Делаем текстовые вставки
        self.grid.addWidget(number_shifr , 1, 0)
        self.grid.addWidget(self.enterPQ_btn,2,0)
        self.grid.addWidget(self.savePQ_btn,2,1)
        self.enterPQ_btn.clicked.connect(self.enteredPQ)
        self.savePQ_btn.clicked.connect(self.saveEncrypt)
        self.setLayout(self.grid)
        self.setWindowTitle('Encrypt key')

    def enteredPQ(self):
        k=resheto_Atkin() #Получаем список простых чисел
        self.MainWindow.p=random.choice(k) #Выбор случайного простого числа p
        self.MainWindow.q=random.choice(k) #Выбор случайного простого числа q
        while self.MainWindow.p==self.MainWindow.q: #Проверка, чтобы они не были равны
            self.MainWindow.p=random.choice(k)
            self.MainWindow.q=random.choice(k)          
        f=(self.MainWindow.p-1)*(self.MainWindow.q-1)#Вычисление функции Эйлера
        self.MainWindow.e=f
        while (NOD(f,self.MainWindow.e)!=1):
            self.MainWindow.e=random.randint(2,self.MainWindow.p*self.MainWindow.q-1)#Выбор ключа е в границах от 2 до n
        self.value_shifr.setText(str(self.MainWindow.p)+'-'+str(self.MainWindow.q)+'-'+str(self.MainWindow.e))  
        self.grid.addWidget(self.value_shifr,1,1)
    def saveEncrypt(self):
        self.MainWindow.shifr_text()
        self.value_shifr.setText('')
        self.close()
#######################################################
#######################################################
#######################################################
class pq_deshifr_widget(QDialog):
    def __init__(self,root,**kwargs):
        super().__init__(root, **kwargs)
        self.MainWindow=root
        self.deshifrEdit = QLineEdit() #Добавляем лайнэдиты
        self.enterPQ_btn=QPushButton('Enter')
        self.pq_ui()
    def pq_ui(self):

        grid = QGridLayout()
        grid.setSpacing(10)

        number_deshifr = QLabel('Encryption key') #Делаем текстовые вставки
        grid.addWidget(number_deshifr , 1, 1)
        grid.addWidget(self.deshifrEdit, 1, 2)
        grid.addWidget(self.enterPQ_btn,4,2)
        self.enterPQ_btn.clicked.connect(self.enteredPQ)
        self.setLayout(grid)
        self.setWindowTitle('Decrypt key')

    def enteredPQ(self):
        self.close()
        k=self.deshifrEdit.text().split('-')
        self.MainWindow.p=int(k[0])
        self.MainWindow.q=int(k[1])
        self.MainWindow.e=int(k[2])
        self.deshifrEdit.setText('')
        self.MainWindow.deshifr_text()


app = QApplication(sys.argv)
writer = Writer()
writer.show()
sys.exit(app.exec_())
