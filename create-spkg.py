#!/usr/bin/python3
#Autor: Tatakae
import readline, os, platform

#Variables
exitprogram = False
EXTENSION = "spkg"
VERSION = "2.0"
ARCHITECTURE = platform.machine()
COMMANDS = [f"create_{EXTENSION}", "help", "exit"]

#Funciones
#	Completado
def complete_commands(text, state):
    opciones = [cmd for cmd in COMMANDS if cmd.startswith(text)]
    return opciones[state] if state < len(opciones) else None

def complete_paths(text, state):
	current_dir = os.path.dirname(text) or './'
	options = [os.path.join(current_dir, item) for item in os.listdir(current_dir) if item.startswith(os.path.basename(text))]
	options = [path + '/' if os.path.isdir(path) else path for path in options]
	return options[state] if state < len(options) else None
	
#	Ayuda
def help():
	print(f"\ncreate_{EXTENSION}: Create .{EXTENSION} packages.")
	print("exit: Exit program.")
	print("help: Show this information.\n")

#Crear spkg
def create_spkg(package_path, destiny_path, name, version, build):
	comando = f"tar -cf {destiny_path}{name}-{version}-{build}-{ARCHITECTURE}.{EXTENSION} -C {package_path} ."
	os.system(comando)
	print("--------------------")
	print(f"{EXTENSION} package created in " + destiny_path + "\n")
	
#Stripear paquetes
def strip_package(package_path, binaries_paths):
	for binary in binaries_paths:
		if not '.' in binary:
			os.system(f"strip -s {package_path}{binary}")

def strip_packages(package_path):
	binary_founded = False
	try:
		binaries1 = os.listdir(package_path + "usr/bin")
		strip_package(package_path + "usr/bin/", binaries1)
		binary_founded = True
	except:
		print(f"{package_path}usr/bin not founded.")
	try:
		binaries2 = os.listdir(package_path + "usr/local/bin")
		strip_package(package_path + "usr/local/bin/", binaries2)
		binary_founded = True
	except:
		print(f"{package_path}usr/local/bin not founded.")
	
	if binary_founded:
		print("Packages stripped.")
	print("--------------------")

def create_description(package_path, name, mantainer, licenses, version, build, dependences, description, homepage):
	filedesc = open(package_path + "description", "w")
	filedesc.write("Package: " + name + "\n")
	filedesc.write("Mantainer: " + mantainer + "\n")
	filedesc.write("Version: " + version + "\n")
	filedesc.write("Build: " + build + "\n")
	filedesc.write("License: " + licenses + "\n")
	filedesc.write("Homepage: " + homepage + "\n")
	filedesc.write("Description: " + description + "\n")
	filedesc.write("Dependences: " + dependences + "\n")
	filedesc.close()
	print("Description created.")
	
def show_info(name, package_path, destiny_path, mantainer, licenses, homepage, description):
	print("\n-----Resume-----")
	print("Package:")
	print("	Package name: " + name)
	print("	Package directory: " + package_path)
	print("	Package destiny: " + destiny_path)
	print("Aditional info:");
	print("	Mantainer: " + mantainer);
	print("	License: " + licenses);
	print("	Homepage: " + homepage);
	print("	Description: " + description);

def get_info():
	#Variables
	description_exists = False
	
	#Detección de rutas
	readline.set_completer_delims('\t')
	readline.set_completer(complete_paths)
	readline.parse_and_bind('tab: complete')
	
	package_path = input("Project directory: ") or "./"
	destiny_path = input("Package destiny: ") or "./"
	if package_path == '.':
		package_path = './'
	if destiny_path == '.':
		destiny_path = './'
	
	try:
		with open(package_path + "description", "r") as filedesc:
			lines = filedesc.readlines()
			for line in lines:
				if not "Description:" in line and not "Dependences:" in line:
					line = line.split(' ')
					line[1] = line[1][:-1]
					if line[0] == "Package:":
						autoname = line[1]
					elif line[0] == "Mantainer:":
						automantainer = line[1]
					elif line[0] == "License:":
						autolicense = line[1]
					elif line[0] == "Version:":
						autoversion = line[1]
					elif line[0] == "Build:":
						autobuild = line[1]
					elif line[0] == "Dependences:":
						autodependences = line[1]
					elif line[0] == "Homepage:":
						autohomepage = line[1]
				elif "Description:" in line:
					autodescription = line[13:-1]
				elif "Dependences:" in line:
					autodependences = line[13:-1]
		description_exists = True
	except:
		description_exists = False
		
	if description_exists: readline.set_startup_hook(lambda: readline.insert_text(autoname))
	name = input("Program name: ") or "example"
	if description_exists: readline.set_startup_hook(lambda: readline.insert_text(autoversion))
	version = input("Program version: ") or "1.0"
	if description_exists: readline.set_startup_hook(lambda: readline.insert_text(autobuild))
	build = input("Build: ") or "1"
	if description_exists: readline.set_startup_hook(lambda: readline.insert_text(automantainer))
	mantainer = input("Mantainer (optional): ") or "Unknown"
	if description_exists: readline.set_startup_hook(lambda: readline.insert_text(autolicense))
	licenses = input("License (optional): ") or "Unknown"
	if description_exists: readline.set_startup_hook(lambda: readline.insert_text(autohomepage))
	homepage = input("Homepage (optional): ") or "Unknown"
	if description_exists: readline.set_startup_hook(lambda: readline.insert_text(autodependences))
	dependences = input("Dependences (optional): ") or "Unknown"
	if description_exists: readline.set_startup_hook(lambda: readline.insert_text(autodescription))
	description = input("Description (optional): ") or "Unknown"
	
	if description_exists: readline.set_startup_hook(lambda: readline.insert_text())
	show_info(name, package_path, destiny_path, mantainer, licenses, homepage, description)
	while True:
		proceed = input("\nProceed with the package creation? (y/n): ")
		if proceed == "y":
			print("--------------------")
			strip_packages(package_path)
			create_description(package_path, name, mantainer, licenses, version, build, dependences, description, homepage)
			create_spkg(package_path, destiny_path, name, version, build)
			break
		elif proceed == "n":
			print("Cancelled.\n")
			break
		elif command == "":
			pass
		else:
			print("Invalid option: " + proceed)

#Autocompletado
readline.set_completer(complete_commands)
readline.parse_and_bind('tab: complete')

#Inicio
print(f"Welcome to SPKG Creator {VERSION}!\n")
while not exitprogram:
	command = input(">> ")
	if command == "help":
		help()
	elif command == f"create_{EXTENSION}":
		get_info()
		readline.set_completer(complete_commands)
		readline.parse_and_bind('tab: complete')
	elif command == "exit":
		exitprogram = True
	elif command == "":
		pass
	else:
		print(f"Unknown command: {command}.")
