# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView

class BalanceTable(QTableWidget):
	def __init__(self):
		QTableWidget.__init__(self)
		self.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.setColumnCount(2)
		self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
		self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
		self.setHorizontalHeaderLabels(["账号", "余额"])

	def addItem(self, account, balance):
		rowCount = self.rowCount()
		self.insertRow(rowCount)
		self.setItem(rowCount, 0, QTableWidgetItem(account))
		self.setItem(rowCount, 1, QTableWidgetItem(balance))