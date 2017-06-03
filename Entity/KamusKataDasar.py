import corpus
class KamusKataDasar:
	def read(self):
		File = open('kata-dasar.txt','r')
		var =  File.read()
		LIST_ROOT_WORD = var.split()
		return LIST_ROOT_WORD