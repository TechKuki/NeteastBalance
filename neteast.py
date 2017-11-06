# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout
from balance_view import BalanceView
from balance_table import BalanceTable

class Neteast(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.setWindowTitle('neteast balance tool')
		self.initUI()

	def initUI(self):
		hboxLayout = QHBoxLayout()
		balanceView = BalanceView()
		balanceView.setFixedSize(360, 385)

		balanceTable = BalanceTable()
		balanceTable.setFixedSize(300, 385)

		hboxLayout.addWidget(balanceView)
		hboxLayout.addWidget(balanceTable)

		self.balanceView = balanceView
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

if __name__ == "__main__":
	accounts = [('user1@163.com', 'password'),
		('user2@163.com', 'password'),
		('user3@163.com', 'password')]
	app = QApplication(sys.argv)
	ex = Neteast()
	ex.setAccounts(accounts)
	ex.startQuery()
	sys.exit(app.exec_())