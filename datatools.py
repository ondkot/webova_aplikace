from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
class Data:
	def __init__(self):
		self.codes = {}
		with open("data",mode="r",encoding="utf-8") as f:
			readlines = f.readlines()
		for i in range(len(readlines)):
			readlines[i] = readlines[i][0:-1]
		user_hash = []
		pass_hash = []
		for i in readlines:
			user_hash.append(i[0:i.find(";")])
			pass_hash.append(i[i.find(";") + 1:])
		self.data = []
		for user, password in zip(user_hash, pass_hash):
			self.data.append([user,password])
	def login(self,username,password):
		dvojice = [username,password]
		vysledek = False
		for i, j in self.data:
			if check_password_hash(i,dvojice[0]) and check_password_hash(j,dvojice[1]):
				vysledek = True
				break
		if vysledek:
			kod = str(randint(0,1000000))
			kod = ((6 - len(kod)) * "0")
			while kod in list(self.codes.keys()):
				kod = str(randint(0,1000000))
				kod = ((6 - len(kod)) * "0")
			self.codes[kod] = username
			return vysledek,kod				
		return vysledek,None
	def append(self,username,password):
		username = generate_password_hash(username)
		password = generate_password_hash(password)
		self.data.append([username,password])
		with open("data",mode="a",encoding="utf-8") as f:
			f.write(username + ";" + password + "\n")
class DataFilmu:
	def __init__(self):
		self.data = []
		with open("dataFilmu",mode="r",encoding="utf-8") as f:
			readlines = f.readlines()
			for i in readlines:
				self.data.append(i.strip().split(";"))
	def __getitem__(self,index):
		if not isinstance(index,int):
			raise TypeError("Key must be int, not " + str(key.__class__.__name__) + ".")
		return self.data[index]
	def append(self,nazev,rezie,zanr):
		self.data.append([nazev,rezie,zanr])
		with open("dataFilmu",mode="a",encoding="utf-8") as f:
			f.write(";".join([nazev,rezie,zanr]) + "\n")			