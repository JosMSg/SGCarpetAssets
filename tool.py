import os 

sg_types = ['Character', 'Vehicle', 'Prop', 'Environment', 'Matte Painting']
sg_category = ['Production', 'Test', 'Development']
validCategory = False
user_type = os.path.split(os.getcwd())[1]  #Nombre de la carpeta donde se corre el programa
index_name = None
user_name = None
dir_names = None


def getDirs(path):
	global dir_names
	fileItems = []
	dir_names = os.listdir(path)
	for item in dir_names:
		if not os.path.isdir(path+'/'+item):
			fileItems.append(item)
	for item in fileItems:
		dir_names.remove(item)


def assignName(number):
	"""
	Entrada: String que representa la posicion 
	del nombre deseado en dir_names
	Funcion: Trata de convertir la variable
	number a un entero. Si no es posible o
	el numero esta fuera de rango retorna
	False.
	"""
	global index_name, user_name, dir_names
	try:
		index_name = int(number)
		if index_name > len(dir_names):
			return False
		user_name = dir_names[index_name-1]
		return True
	except:
		return False
def showOptions():
	global dir_names
	print "Seleccione un nombre:"
	for index, name in enumerate(dir_names):
		print '%s - %s' %(index+1, name)
	while not assignName(raw_input("Opcion seleccionada:")):
		print "Escriba correctamente la opcion seleccionada"

if user_type in sg_types:
	files = os.listdir(os.getcwd())
	print "Tipo %s\n" %user_type
	for file in files:
		if file in sg_category:
			user_category  = file
			validCategory = True
			break
	if validCategory:
		print "Categoria %s\n" %user_category
		#dir_names = os.listdir(os.getcwd()+'/'+user_category)
		getDirs(os.getcwd()+'/'+user_category)
		if len(dir_names)>0:
			showOptions()
			print "Usted selecciono: %s" %user_name
		else: 
			print "No se encontro ninguna carpeta"
		raw_input("asdf")
		dir_files = os.listdir(os.getcwd()+'/'+user_category+'/'+user_name)
		if len(dir_files)>0:
			print "Seleccione un nombre:"
			for index, name in enumerate(dir_files):
				print '%s - %s' %(index+1, name)
			index_file = int(raw_input("Opcion seleccionada:"))
			user_file = dir_files[index_name-1]
			print "Usted selecciono: %s" %user_file
else:
	print 'Revise que este en la carpeta correcta y el nombre de la misma sea el adecuado'
raw_input("Try again")
	