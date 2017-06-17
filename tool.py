import os 

sg_types = ['Character', 'Vehicle', 'Prop', 'Environment', 'Matte Painting']
sg_category = ['Production', 'Test', 'Development']
img_extension = ['.jpg', '.png', '.jpeg', '.exr']
validCategory = False
user_type = os.path.split(os.getcwd())[1]  #Nombre de la carpeta donde se corre el programa
index_name = None
index_file = None
user_name = None
dir_names = None
clear = lambda: os.system('cls')



def getDirs(path):
	"""
	Obtiene solo las carpetas de cierta direccion
	y las guarda en la variable dir_names
	"""
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
	"""
	Presenta las opciones en dir_names y le pide al
	usuario que elija una con un valor valido
	"""
	global dir_names
	print "Seleccione un nombre:"
	for index, name in enumerate(dir_names):
		print '%s - %s' %(index+1, name)
	while not assignName(raw_input("Opcion seleccionada:")):
		print "Escriba correctamente la opcion seleccionada"
def selectFile(path):
	global dir_files,img_extension, index_file
	fileItems = []
	dir_files = os.listdir(path)
	print "Carpetas y archivos encontrados:"
	for index, item in enumerate(dir_files):
		if os.path.isdir(path+'/'+item):
			print "%s >%s" %(index+1, item)
		else:
			filename, file_extension = os.path.splitext(item)
			if file_extension in img_extension:
				print "%s  %s" %(index+1, item)
			else:
				fileItems.append(item)
	for item in fileItems:
		dir_files.remove(item)
	print "\n"
	try:
		index_file = int(raw_input("Opcion seleccionada:"))-1
		if index_file>len(dir_files):
			clear()
			return 0
		else:
			if not os.path.isdir(path+'/'+dir_files[index_file]):
				return 1
			else:
				return 2
	except:
		clear()
		return 0

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
			clear()
			dir_files = os.listdir(os.getcwd()+'/'+user_category+'/'+user_name)
			if len(dir_files)>0:
				#Checar que la entrada sea valida
				valid = selectFile(os.getcwd()+'/'+user_category+'/'+user_name)
				while valid == 0:
					print "Opcion invalida, vuelva a intentarlo"
					clear()
					selectFile(os.getcwd()+'/'+user_category+'/'+user_name)
				
				user_file = dir_files[index_file]
				if valid == 1:
					print "Imagen seleccionada: %s" %user_file
				elif valid == 2:
					print "Carpeta seleccionada: %s" %user_file
		else: 
			print "No se encontro ninguna carpeta"
else:
	print 'Revise que este en la carpeta correcta y el nombre de la misma sea el adecuado'
raw_input("Thanks for using Shotgun!")
	