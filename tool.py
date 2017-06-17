import os 

sg_types = ['Character', 'Vehicle', 'Prop', 'Environment', 'Matte Painting']
sg_category = ['Production', 'Test', 'Development']
validCategory = False
user_type = os.path.split(os.getcwd())[1]
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
		dir_names = os.listdir(os.getcwd()+'/'+user_category)
		if len(dir_names)>0:
			print "Seleccione un nombre:"
			for index, name in enumerate(dir_names):
				print '%s - %s' %(index+1, name)
else:
	print 'Revise que este en la carpeta correcta y el nombre de la misma sea el adecuado'
raw_input("Try again")
	