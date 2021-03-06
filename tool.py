import os 
from shotgun_api3 import Shotgun

sg = Shotgun("https://upgdl.shotgunstudio.com",
                          login="jos_sg",
                          password="Shho3420")

sg_types = ['Character', 'Vehicle', 'Prop', 'Environment', 'Matte Painting']
sg_category = ['Production', 'Test', 'Development']
img_extension = ['.jpg', '.png', '.jpeg', '.exr']
validCategory = False
index_name = None
index_category = None
index_file = None
files = None
user_name = None
dir_names = None
assets_names = []
asset_id = None
validAsset = False
user_type = os.path.split(os.getcwd())[1]  #Nombre de la carpeta donde se corre el programa
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
def categoryValid():
	global index_category, files
	try:
		index_category = int(raw_input("Selecciona una categoria (solo numeros):"))
		if index_category>len(files):
			return False
		return True
	except:
		return False

#aqui inicia el codigo
if user_type in sg_types:
	files = os.listdir(os.getcwd())
	print "Tipo %s\n" %user_type
	if len(files)>1:
		print "Eliga una categoria:"
		for index, file in enumerate(files):
			print "%d - %s" %(index,file)
		while not categoryValid():
			print ''
		file = files[index_category]
		if file in sg_category:
			user_category  = file
			validCategory = True
			clear()
		else:
			print "No se encontro la categoria"
	else:
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
			#Encontrar el asset shotgun
			filters = [
				['sg_asset_type', 'is', user_type],
				['sg_category', 'is', user_category]
			]
			fields = ['id', 'code'] 
			assets= sg.find("Asset",filters,fields)
			for asset in assets:
				assets_names.append(asset['code'])
			if user_name in assets_names:
				asset_index = assets_names.index(user_name)
				asset_id = assets[asset_index]['id']
				print "Los archivos se subiran a %s" %user_name
				validAsset=True
			else:
				createSg = raw_input("El asset no existe, desea crearlo? (s/n)\n")
				if createSg.lower() == 's':
					data = {
						"project": {"type": "Project", "id": 113},
						"sg_asset_type": user_type,
						"sg_category": user_category,
						"code": user_name
					}
					asset_id = sg.create('Asset', data)
					asset_id = asset_id['id']
					print "Asset creado: %s" %asset_id
					validAsset=True
				else:
					print "Cambie el nombre de la carpeta y vuelva a correr el programa"
			#Subir archivos
			if validAsset:
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
						file_path = os.getcwd()+'/'+user_category+'/'+user_name+'/'+user_file
						print "Imagen seleccionada: %s" %user_file
						data = {
							'code': user_file,
							'entity': {'id': asset_id, 'type': 'Asset'},
							'description': 'Asset created by CarpetAssetsTool',
							'user': {'id':93, 'type': 'HumanUser'},
							'sg_status_list': 'rev',
							'project': {'id':113, 'type':'Project'}}
						result = sg.create("Version", data)
						sg.upload("Version", result["id"], file_path, field_name="sg_uploaded_movie", display_name="Media")
						print "Asset creado"
					elif valid == 2:
						print "Carpeta seleccionada: %s" %user_file
						imgs_dir = os.getcwd()+'/'+user_category+'/'+user_name+'/'+user_file
						os.chdir(imgs_dir)
						#ffmpegCall = "ffmpeg -i *.jpg -c:v libx264 -crf 0 output.mp4" 
						#os.system(ffmpegCall)
						for index, filename in enumerate(os.listdir(imgs_dir)):
						    if (filename.endswith(".jpg")): #or .avi, .mpeg, whatever.
						        os.system("ffmpeg -i {0} -f image2 -vf fps=fps=1 secuencia%d.mp4".format(filename) )
						    else:
						        continue
						try:
							file_path = imgs_dir+'/secuencia1.mp4'
							data = {
								'code': user_file,
								'entity': {'id': asset_id, 'type': 'Asset'},
								'description': 'Asset created by CarpetAssetsTool',
								'user': {'id':93, 'type': 'HumanUser'},
								'project': {'id':113, 'type':'Project'}}
							result = sg.create("Version", data)
							sg.upload("Version", result["id"], file_path, field_name="sg_uploaded_movie", display_name="Media")
							print "Asset creado"
						except Exception as e:
							print e
		else: 
			print "No se encontro ninguna carpeta"
else:
	print 'Revise que este en la carpeta correcta y el nombre de la misma sea el adecuado'
raw_input("Gracias por utilizar Shotgun!")
	