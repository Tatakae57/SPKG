#!/usr/bin/python3
#Autor: Tatakae
import readline, os, subprocess, platform

#Variables
exitprogram = False
EXTENSION = "spkg"
VERSION = "2.0"
HOME = os.getenv("HOME")
COMMANDS = ["add_repo", "download", "exit", "help", "install_from_repo", "install_local", "remove", "remove_repo",  "show_all_packages", "show_available", "show_info", "show_installed", "show_repos", "update_list"]
default_delims = readline.get_completer_delims()
urls, packages, sizes = [], [], []
lists, listnames = [], []

#Setear arquitectura
if platform.machine() == "x86_64" or platform.machine() == "i686":
	TEMPDIR = "/tmp/"
	ROOTDIR = "/"
elif platform.machine() == "aarch64" or platform.machine() == "armv81":
	TEMPDIR = "/data/data/com.termux/files/usr/tmp/"
	ROOTDIR = "/data/data/com.termux/files/"

#Funciones
#	Crear directorios si no existen
def create_folders():
	if not os.path.isdir(f"{HOME}/.spkg"):
		os.system(f"mkdir {HOME}/.spkg")
	if not os.path.isdir(f"{HOME}/.spkg/installed"):
		os.system(f"mkdir {HOME}/.spkg/installed")
	if not os.path.isdir(f"{HOME}/.spkg/repos-lists"):
		os.system(f"mkdir {HOME}/.spkg/repos-lists")
	
def no_empty_list():
	if len(packages) == 0:
		print(f"{HOME}/.spkg/repos.list is emtpy or not exists, use 'add_repo'.")
		return 0
	else:
		return 1

#	Cargar repos
def load_repos():
	global lists, listnames
	lists, listnames = [], []
	try:
		with open(f"{HOME}/.spkg/repos.list") as reposlist:
			lines = reposlist.readlines()
			for line in lines:
				line = line.strip()
				if line[0] == '#':
					continue
				lists.append(line)
				listnames.append(line[line.rfind("/") + 1:])
	except:
		pass

#	Cargar lista de paquetes
def load_packages():
	global packages, urls, sizes
	packages, urls, sizes = [], [], []
	repos_lists = os.listdir(f"{HOME}/.spkg/repos-lists/")
	if len(repos_lists) != 0:
		for repo_list in repos_lists:
			with open(f"{HOME}/.spkg/repos-lists/{repo_list}", "r") as filerepo:
				lines = filerepo.readlines()
				for line in lines:
					line = line.split(" ")
					urls.append(line[0])
					packages.append(line[0][line[0].rfind("/") + 1: -5])
					sizes.append(line[1])

#	Completado
def complete_commands(text, state):
	opciones = [cmd for cmd in COMMANDS if cmd.startswith(text)]
	return opciones[state] if state < len(opciones) else None

def complete_packages(text, state):
	opciones = [package for package in packages if package.startswith(text)]
	opciones = [package for package in opciones if not package in os.listdir(f"{HOME}/.spkg/installed")]
	return opciones[state] if state < len(opciones) else None

def complete_all_packages(text, state):
	opciones = [package for package in packages if package.startswith(text)]
	return opciones[state] if state < len(opciones) else None

def complete_installed(text, state):
	opciones = [installed for installed in os.listdir(f"{HOME}/.spkg/installed") if installed.startswith(text)]
	return opciones[state] if state < len(opciones) else None

def complete_paths(text, state):
	current_dir = os.path.dirname(text) or './'
	options = [os.path.join(current_dir, item) for item in os.listdir(current_dir) if item.startswith(os.path.basename(text))]
	options = [path + '/' if os.path.isdir(path) else path for path in options]
	return options[state] if state < len(options) else None

def complete_repos(text, state):
	opciones = [name for name in listnames if name.startswith(text)]
	return opciones[state] if state < len(opciones) else None

def default_completion():
	readline.set_completer_delims(default_delims)
	readline.set_completer(complete_commands)
	readline.parse_and_bind('tab: complete')

#	Descargar archivos
def download_file(url, destiny):
	command = f"wget -q {url} --directory-prefix={destiny}"
	output = subprocess.call(command, shell = True)
	if output == 0:
		return 1
	else:
		return 0

#	Recibir lista
def update_list():
	load_repos()
	print()
	if len(lists) != 0:
		for i in range(len(lists)):
			print(f"Getting {lists[i]}...", end = ' ', flush = True)
			if download_file(lists[i], f"{TEMPDIR}"):
				print("OK.")
				if os.path.isfile(f"{HOME}/.spkg/repos-lists/{listnames[i]}"):
					with open(f"{HOME}/.spkg/repos-lists/{listnames[i]}", "r") as filelist1:
						with open(f"{TEMPDIR}{listnames[i]}", "r") as filelist2:
							if filelist1.read() == filelist2.read():
								os.system(f"rm {TEMPDIR}{listnames[i]}")
								print("Package list is already updated.")
							else:
								os.system(f"mv {TEMPDIR}{listnames[i]} {HOME}/.spkg/repos-lists")
								print("Package list updated.")
				else:
					os.system(f"mv {TEMPDIR}{listnames[i]} {HOME}/.spkg/repos-lists")
					print(f"Package list of {listnames[i]} created.")
				load_packages()
			else:
				print(f"error getting {lists[i]}")
			print()
	else:
		print("No repositories founded.\n")

#	Ayuda
def help_spkg():
	print("\nadd_repo: Add new repository to repos.list.")
	print(f"download: Download {EXTENSION} package from repository.")
	print("exit: Exit program.")
	print("help: Show this information.")
	print("install_from_repo: Select packages to download and install from the repository.")
	print(f"install_local: Install local {EXTENSION} package.")
	print("remove: Remove spkg from system.")
	print("remove_repo: Delete repo from repos.list.")
	print("show_all_packages: Show all the packages of the all repos.")
	print("show_available: Show no installed packages.")
	print("show_info: Show info of selected packages.")
	print("show_installed: Show installed packages.")
	print("show_repos: Show the list of repos.")
	print("update_list: Update the list of packages.\n")

#	Paquetes
#		Descarga
def download_package(url, package_name):
	print(f"Downloading {url}... ", end = ' ', flush = True)
	if download_file(url, f"{TEMPDIR}spkg-package"):
		print("OK.")
		return 1
	else:
		print(f"failed to download {url}\n")
		return 0

def download():
	if len(packages) == 0:
		print(f"{LISTNAME} is emtpy or not exists, use 'update_list'.")
	else:
		readline.set_completer(complete_all_packages)
		readline.parse_and_bind('tab: complete')
		selection = input("Selection: ")
		selection = selection.split()
		readline.set_completer_delims('\t')
		readline.set_completer(complete_paths)
		readline.parse_and_bind('tab: complete')
		destiny = input("Destiny path: ")
		
		print("--------------")
		if len(selection) != 0:
			for pack in selection:
				if pack in packages:
					index = packages.index(pack)
					if download_file(urls[index], destiny):
						print(f"{packages[index]} downloaded.\n")
				else:
					print(f"Invalid package: {pack}\n")
		else:
			print("No packages selected.\n")

#		Instalación
def install_package(package_directory, package_name):
	command = f"tar -xvf {package_directory} -C {ROOTDIR} ./usr > {HOME}/.spkg/installed/{package_name}"
	output = subprocess.call(command, shell = True)
	if output == 0:
		return 1
	else:
		os.system(f"rm {HOME}/.spkg/installed/{package_name}")
		return 0
	
def install_from_repository():
	print()
	if no_empty_list():
		readline.set_completer(complete_packages)
		readline.parse_and_bind('tab: complete')
		selection = input("Selection: ")
		selection = selection.split()
		
		print("--------------")
		if len(selection) != 0:
			os.system(f"mkdir {TEMPDIR}spkg-package/")
			for pack in selection:
				if pack in packages:
					index = packages.index(pack)
					if download_package(urls[index], f"{TEMPDIR}spkg-package/"):
						if install_package(f"{TEMPDIR}spkg-package/{packages[index]}.{EXTENSION}", packages[index]):
							print(f"{packages[index]} installed.")
							os.system(f"rm {TEMPDIR}spkg-package/*")
						else:
							print(f"Failed to install {packages[index]}.spkg, you may need to run this program with sudo.")
				else:
					print(f"Invalid package: {pack}")
			os.system(f"rm -r {TEMPDIR}spkg-package")
		else:
			print("No packages selected.")
	print()

def install_local():
	readline.set_completer_delims('\t')
	readline.set_completer(complete_paths)
	readline.parse_and_bind('tab: complete')
	local_package = input("\nPackage: ")
	print("--------------")
	if local_package.endswith(".spkg"):
		package_name = local_package[local_package.rfind('/') + 1: -5]
		if install_package(local_package, package_name):
			print(f"{package_name} installed.")
		else:
			print(f"\nFailed to install {package_name}.spkg, you may need to run this program with sudo.")
	elif local_package.strip() == "":
		print("No packages selected.")
	else:
		print(f"Invalid package: {local_package}")
	print()

def remove_files(track_file):
	try:
		with open(f"{HOME}/.spkg/installed/{track_file}", "r") as file:
			lines = file.readlines()
			for line in lines:
				line = line.strip()
				if not line.endswith('/'):
					os.system(f"rm {ROOTDIR}{line[2:]}")
			os.system(f"rm {HOME}/.spkg/installed/{track_file}")
		return 1
	except:
		return 0

#		Remover
def remove_package():
	print()
	if len(os.listdir(f"{HOME}/.spkg/installed")) == 0:
		print("No packages installed.")
	else:
		readline.set_completer(complete_installed)
		readline.parse_and_bind('tab: complete')
		selection = input("Selection: ")
		selection = selection.split()
		print("--------------")
		
		if len(selection) != 0:
			for pack in selection:
				if remove_files(pack):
					print(f"{pack} uninstalled succesfully.")
				else:
					print(f"\nFailed to uninstall {pack}, you may need to run this program with sudo.")
		else:
			print("No packages selected.")
	print()

#		Información
def show_available():
	print()
	installed = os.listdir(f"{HOME}/.spkg/installed")
	if no_empty_list():
		for package in packages:
			if not package in installed:
				print(f"{package}   {sizes[packages.index(package)].strip()}")
	print()
	
def show_installed():
	print()
	installed = os.listdir(f"{HOME}/.spkg/installed")
	if len(installed) != 0:
		for package in installed:
			print(package)
	else:
		print("No packages installed.")
	print()

def show_all_packages():
	print()
	installed = os.listdir(f"{HOME}/.spkg/installed")
	if no_empty_list():
		for package in packages:
			if not package in installed:
				print(f"{package}   {sizes[packages.index(package)].strip()}")
			else:
				print(f"{package}	{sizes[packages.index(package)].strip()}	[installed]")
	print()

def get_info(package_path):
	command = f"tar -xf {package_path} -C {TEMPDIR}spkg-info ./description"
	os.system(command)
	with open(f"{TEMPDIR}spkg-info/description", "r") as file_desc:
		lines = file_desc.readlines()
		for line in lines:
			if not "Description:" in line and not "Dependences:" in line:
				line = line.split(" ")
				line[1] = line[1][:-1]
				if line[0] == "Package:":
					name = line[1]
				elif line[0] == "Mantainer:":
					mantainer = line[1]
				elif line[0] == "License:":
					licenses = line[1]
				elif line[0] == "Version:":
					version = line[1]
				elif line[0] == "Build:":
					build = line[1]
				elif line[0] == "Dependences:":
					dependences = line[1]
				elif line[0] == "Homepage:":
					homepage = line[1]
			elif "Description:" in line:
				description = line[13:-1]
			elif "Dependences:" in line:
				dependences = line[13:-1]
	return [name, mantainer, licenses, version, build, dependences, description, homepage]

def show_info():
	print()
	package_info = []
	if no_empty_list():
		readline.set_completer(complete_all_packages)
		readline.parse_and_bind('tab: complete')
		selection = input("Selection: ")
		selection = selection.split()
		print("--------------")
		
		if len(selection) != 0:
			os.system(f"mkdir {TEMPDIR}spkg-info/")
			for pack in selection:
				if pack in packages:
					index = packages.index(pack)
					print(f"Getting {pack}.spkg info...", end = ' ', flush = True)
					if download_file(urls[index], f"{TEMPDIR}spkg-info/"):
						print("OK.")
						package_info.append(get_info(f"{TEMPDIR}spkg-info/{packages[index]}.spkg"))
						os.system(f"rm {TEMPDIR}spkg-info/*")
					else:
						print(f"Failed to get {packages[index]}.spkg info.")
				else:
					print(f"Invalid package: {pack}\n")
			os.system(f"rm -r {TEMPDIR}spkg-info")
			#Imprimir información
			for i in range(len(package_info)):
				print(f"\n	Name: {package_info[i][0]}")
				print(f"	Version: {package_info[i][3]}")
				print(f"	Build: {package_info[i][4]}")
				print(f"	Mantainer: {package_info[i][1]}")
				print(f"	License: {package_info[i][2]}")
				print(f"	Homepage: {package_info[i][7]}")
				print(f"	Dependences: {package_info[i][5]}")
				print(f"	Description: {package_info[i][6]}")
		else:
			print("No packages selected.")
	print()

def show_repos():
	print()
	if len(lists) != 0:
		for repo in lists:
			print(repo)
	else:
		print("No repositories founded.")
	print()

#	Repositorios
def add_repo():
	print()
	url = input("URL of the repo list: ")
	if url == "":
		print("No URL given.")
	else:
		if download_file(url, f"{TEMPDIR}url-test"):
			try:
				with open(f"{TEMPDIR}url-test/{url[url.rfind('/') + 1:]}", "r") as urltest:
					lines = urltest.readlines()
					for line in lines:
						line = line.split(' ')
						param1 = line[0]
						param2 = line[1]
				with open(f"{HOME}/.spkg/repos.list", "w") as filerepos:
					for listl in lists:
						filerepos.write(listl + "\n")
					filerepos.write(url + "\n")
				print("Repository added.")
				load_repos()
				load_packages()
				os.system(f"rm -r {TEMPDIR}url-test")
			except:
				print("The repository list does not comply with the SPKG format: url, size of file")
		else:
			print(f"Error getting {url}, repository will not be added.")
	print()

def remove_repo():
	print()
	if os.path.isfile(f"{HOME}/.spkg/repos.list"):
		readline.set_completer(complete_repos)
		readline.parse_and_bind('tab: complete')
		selection = input("Selection: ")
		selection = selection.split(' ')
		print("--------------")
		if len(selection) != 0:
			for repo in selection:
				if repo in listnames:
					print(f"{lists[listnames.index(repo)]} removed from repos.list")
					lists.pop(listnames.index(repo))
					os.system(f"rm {HOME}/.spkg/repos-lists/{repo}")
					print(f"{repo} removed from repos-lists/")
				else:
					print(f"Invalid repo: {repo}")
			with open(f"{HOME}/.spkg/repos.list", "w") as filerepos:
				for listl in lists:
					filerepos.write(listl)
			load_repos()
			load_packages()
		else:
			print("No repositories specified.")
	else:
		print("repos.list dont exist, use 'add_repo' to create it.")
	print()

#Autocompletado
readline.set_completer(complete_commands)
readline.parse_and_bind('tab: complete')

#Principal
create_folders()
load_repos()
load_packages()
print(f"Welcome to SPKG Manager {VERSION}!\n")

while not exitprogram:
	command = input(">> ")
	if command == "add_repo":
		readline.set_completer()
		readline.parse_and_bind('tab: complete')
		add_repo()
		default_completion()
	elif command == "download":
		download()
		readline.set_completer(complete_commands)
		readline.parse_and_bind('tab: complete')
	elif command == "help":
		help_spkg()
	elif command == "exit":
		exitprogram = True
	elif command == "install_from_repo":
		install_from_repository()
		default_completion()
	elif command == "install_local":
		install_local()
		default_completion()
	elif command == "remove":
		remove_package()
		default_completion()
	elif command == "remove_repo":
		remove_repo()
		default_completion()
	elif command == "show_all_packages":
		show_all_packages()
	elif command == "show_available":
		show_available()
	elif command == "show_info":
		show_info()
		default_completion()
	elif command == "show_installed":
		show_installed()
	elif command == "show_repos":
		show_repos()
	elif command == "update_list":
		update_list()
	elif command == "":
		pass
	else:
		print(f"Unknown command: {command}.\n")
