class KamusStopWord:
	def read(self):
		File = open('stopword.txt','r')
		return File.read()