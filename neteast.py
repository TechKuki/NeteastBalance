# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript

class Balance(QWebEngineView):
	def __init__(self, accounts):
		QWebEngineView.__init__(self)
		self.index = 0
		self.accounts = accounts
		self.page().loadFinished.connect(self.loadFinished)

		self.script = QWebEngineScript()
		self.script.setInjectionPoint(QWebEngineScript.Deferred)
		self.script.setRunsOnSubFrames(True)

		self.urlLogin = QUrl("http://reg.163.com/Logout.jsp?url=http://ecard.163.com/account/query_balance")
		self.urlVerify = QUrl("http://ecard.163.com/handle_login")
		self.urlBalance = QUrl("http://ecard.163.com/handle_query_verify")

	def loadFinished(self, isOk):
		if isOk:
			requestedUrl = self.page().requestedUrl()
			if requestedUrl == self.urlLogin:
				self.page().runJavaScript("""
					if(typeof($) != "undefined"){
						//#footer,#header,#urs_tab,#phone_tab删掉
						$('#footer').remove()
						$('#header').remove()
						$('#urs_tab').remove()
						$('#phone_tab').remove()
						//.nowbg的class属性删掉
						$('.nowbg').removeAttr('class')
						//#wrap的min-width属性去掉
						$('#wrap').css('min-width', 'initial');
						//#center的width属性去掉
						$('#center').css('width', 'initial');
						//#login的border-top,height,position,right,top属性去掉，加margin:auto;
						$('#login').css('border-top', 'initial');
						$('#login').css('height', 'initial');
						$('#login').css('position', 'initial');
						$('#login').css('right', 'initial');
						$('#login').css('top', 'initial');
						$('#login').css('margin', 'auto');
					}
				""")
			elif requestedUrl == self.urlVerify:
				self.page().runJavaScript("""
					//#footer,#header,.situation删掉
					$('#footer').remove()
					$('#header').remove()
					$('.situation').remove()
					//#wrap的min-width属性去掉
					$('#wrap').css('min-width', 'initial');
					//#main的width属性去掉
					$('#main').css('width', 'initial');
					//.mb-content的margin: 100px auto 78px auto;
					$('.mb-content').css('margin', '100px auto 78px auto')
					function verifyFunc(){
						if($('.TxtStatus').children().length == 1){
							clearInterval(verifyId);
							$('#query_verify_form').submit();
						}
					}
					var verifyId = setInterval(verifyFunc, 100);
				""")
			elif requestedUrl == self.urlBalance:
				self.page().runJavaScript("document.getElementsByClassName('red bold')[2].innerText", self.jsCallback)
		else:
			print("load error")

	def jsCallback(self, balance):
		self.index = self.index + 1
		print(balance)
		self.startQuery()

	def startQuery(self):
		if self.index < len(self.accounts):
			account = self.accounts[self.index]
			self.script.setSourceCode("""
				var box = document.getElementById('cnt-box');
				if(box){
					function loginFunc(){
						if(box.children.length == 4 && document.getElementById('nerror').children.length == 2){
							clearInterval(loginId);
							email = document.getElementsByName('email');email[0].value='%s';
							password = document.getElementsByName('password');password[0].value='%s';
							document.getElementById('dologin').click();
						}
					}
					var loginId = setInterval(loginFunc, 100);
					function verifyFunc(){
						if(document.getElementsByClassName('u-suc').length == 2){
							clearInterval(verifyId);
							document.getElementById('dologin').click();
						}
					}
					var verifyId = setInterval(verifyFunc, 100);
				}
			""" % (account[0], account[1]))
			self.page().scripts().insert(self.script)
			self.load(self.urlLogin)

if __name__ == "__main__":
	accounts = [('user1@163.com', 'password'),
		('user2@163.com', 'password'),
		('user3@163.com', 'password')]
	app = QApplication(sys.argv)
	balanceView = Balance(accounts)
	balanceView.resize(360, 363)
	balanceView.startQuery()
	balanceView.show()
	sys.exit(app.exec_())