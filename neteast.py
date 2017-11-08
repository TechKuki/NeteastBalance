# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QProgressBar
from balance_view import BalanceView
from balance_table import BalanceTable

class Neteast(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle('neteast balance tool')
		self.initUI()

	def initUI(self):
		hboxLayout = QHBoxLayout()
		vboxLayout = QVBoxLayout()

		balanceView = BalanceView()
		balanceView.setLoadProgress(self.setProgress)
		balanceView.setFixedSize(360, 380)

		progressBar = QProgressBar()
		progressBar.setTextVisible(False)
		progressBar.setFixedSize(360, 5)

		balanceTable = BalanceTable()
		balanceTable.setFixedSize(300, 385)

		vboxLayout.addWidget(balanceView)
		vboxLayout.addWidget(progressBar)
		hboxLayout.addLayout(vboxLayout)
		hboxLayout.addWidget(balanceTable)

		self.balanceView = balanceView
		self.progressBar = progressBar
		self.balanceTable = balanceTable

		self.setLayout(hboxLayout)
		self.show()

	def setAccounts(self, accounts):
		self.accounts = accounts
		self.balanceView.setAccounts(accounts)

	def startQuery(self):
		if self.accounts:
			self.balanceView.startQuery(self.queryCallBack)

	def queryCallBack(self, account, balance):
		self.balanceTable.addItem(account, balance)

	def setProgress(self, value):
		self.progressBar.setValue(value)

if __name__ == "__main__":
	from account import accounts
	app = QApplication(sys.argv)
	ex = Neteast()
	ex.setAccounts(accounts)
	ex.startQuery()
	sys.exit(app.exec_())