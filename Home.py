from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys




class MainWindow(QMainWindow):
	def __init__(self,*args, **kwargs):
		super(MainWindow,self).__init__(*args, **kwargs)

		self.tabs = QTabWidget()
		self.add_new_tab(QUrl('https://www.google.com'), 'HomePage')
		self.setCentralWidget(self.tabs)


		navtb = QToolBar("Navigation")
		navtb.setIconSize(QSize(30,30))
		self.addToolBar(navtb)

		back_btn = QAction(QIcon(os.path.join('icons', 'back.png')), "Back", self)
		back_btn.setStatusTip("Back To Pevious page")
		back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
		navtb.addAction(back_btn)

		next_btn = QAction(QIcon(os.path.join('icons', 'forward.png')), "Forward", self)
		next_btn.setStatusTip("Forward To Next page")
		next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
		navtb.addAction(next_btn)

		#no ssl
		navtb.addSeparator()

		self.httpsicon = QLabel()#Labele ssl
		#self.httpsicon.setPixmap( QPixmap(os.path.join('icons', 'unlock-icon.png')))
		navtb.addWidget(self.httpsicon)

		self.urlbar = QLineEdit()
		self.urlbar.returnPressed.connect(self.navigate_to_url)
		navtb.addWidget(self.urlbar)

		reload_btn = QAction(QIcon(os.path.join('icons', 'reload.png')), "Reload", self)
		reload_btn.setStatusTip("Forward To Next page")
		reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
		navtb.addAction(reload_btn)

		stop_btn = QAction(QIcon(os.path.join('icons', 'stop.png')), "Stop", self)
		stop_btn.setStatusTip("Stop Loading Current Page")
		stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
		navtb.addAction(stop_btn)





		file_menu = self.menuBar().addMenu("&File")

		open_file_action = QAction(QIcon(os.path.join('icons','open.png')),"Opening ...", self)
		open_file_action.setStatusTip("Open from file")
		open_file_action.triggered.connect(self.open_file)
		file_menu.addAction(open_file_action)

		save_file_action = QAction(QIcon(os.path.join('icons','save.png')),"Saving ...", self)
		save_file_action.setStatusTip("Save current page to file")
		save_file_action.triggered.connect(self.save_file)
		file_menu.addAction(save_file_action)

		print_action = QAction(QIcon(os.path.join('icons','print.png')),"Printing ...", self)
		print_action.setStatusTip("Print current page")
		print_action.triggered.connect(self.print_page)
		file_menu.addAction(print_action)


		help_menu = self.menuBar().addMenu("&Help")


		navigate_rooham_action = QAction(QIcon(os.path.join('icons','me.png')),"Rooham Linkdin", self)
		navigate_rooham_action.setStatusTip("Go to Rooham Linkdin")
		navigate_rooham_action.triggered.connect(self.navigate_rooham)
		help_menu.addAction(navigate_rooham_action)

	def navigate_rooham(self):
	    self.tabs.currentWidget().setUrl(QUrl("https://linkedin.com/in/amosalli"))



	def print_page(self):
		dlg = QPrintPreviewDialog()
		dlg.paintRequested.connect(self.tabs.currentWidget().print_)
		dlg.exec_()
	def open_file(self):
		filename, _ = QFileDialog.getOpenFileName(self, "Open file", "" ,
		                  "Hypertext Markup Language (*.html *.html);;"
						  	"All file (*.*)")
		if filename:
			with open(filename, 'r') as f:
				html = f.read()
			self.tabs.currentWidget().setHtml(html)
			self.urlbar.setText(filename)


	def save_file(self):
		filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "" ,
		                  "Hypertext Markup Language (*.html *.html);;"
						  	"All file (*.*)")
		if filename:
			html = self.tabs.currentWidget().page().mainFrame().tohtml()
			with open(filename, 'w') as f:
				f.write(html)





		self.show()
		self.setWindowTitle("Rooham Broswer")
		self.setWindowIcon(QIcon(os.path.join('icons','amir.png')))



	def navigate_home(self):

		self.tabs.currentWidget().setUrl(QUrl("https://www.google.com"))

	def add_new_tab(self, qurl, label):
			browser = QWebView()
			browser.setUrl(qurl)
			self.tabs.addTab(browser, label)

			browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl,browser))





	def navigate_to_url(self):
		q = QUrl(self.urlbar.text())
		if q.scheme() == "":
			q.setScheme("http")
		self.tabs.currentWidget().setUrl(q)


	def update_urlbar(self, q, browser=None):
		if browser != self.tabs.currentWidget():
			return



		if q.scheme() == 'https':
			self.httpsicon.setPixmap( QPixmap(os.path.join('icons', 'ssl.png')))
		else:
			self.httpsicon.setPixmap( QPixmap(os.path.join('icons', 'unlock-icon.png')))



		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)

app = QApplication(sys.argv)
app.setApplicationName("Rooham Browser")
app.setOrganizationName("Rooham Mosalli")
app.setOrganizationDomain("Rooham.com")

window = MainWindow()
window.show()


app.exec_()
