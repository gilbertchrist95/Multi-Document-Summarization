class KamusStopWord:
	def read(self):
		File = open('stopword.txt','r')
		var =  File.read()
		LIST_STOP_WORD = var.split()
		return LIST_STOP_WORD