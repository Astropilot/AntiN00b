# -*- coding: utf-8 -*-

head = """
################################################################
     _          _   _ _   _  ___   ___  _     
    / \   _ __ | |_(_) \ | |/ _ \ / _ \| |__  
   / _ \ | '_ \| __| |  \| | | | | | | | '_ \ 
  / ___ \| | | | |_| | |\  | |_| | |_| | |_) |
 /_/   \_\_| |_|\__|_|_| \_|\___/ \___/|_.__/ 
                                              
                                                                
                   ##########################                   
                   ####   Team R3V3RS3   ####                   
                   ##########################                   
                   ##                      ##                   
                   ##  Code : - Astro      ##                   
                   ##                      ##                   
                   ##########################                   
                                                                
                                                                
################################################################
"""
print(head)

# Ce C/C de l'entête n'est absolument pas une provocation ;)

import os
import time

try:
	import paramiko
except ImportError:
	os.system('python -m pip install paramiko==2.0.4')
	import paramiko
	
from threading import Thread


SECURE_LOG = '/var/log/secure'
SSHD_CONFIG = '/etc/ssh/sshd_config'

def getSshFromHost(host):
	ssh = None
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(host, port=22, username="root", password="#TpLinux#")
		
	except:
		print("Impossible de se connecter au N00b "+host+", il n'est pas connecté ou protégé")
	return ssh

class sshCmd(Thread):
	def __init__(self, host):
		Thread.__init__(self)
		self.ssh = getSshFromHost(host)
	def run(self):
		if self.ssh is not None:
			ssh = self.ssh
			for i in range(5):
				ssh.exec_command("eject")
				ssh.exec_command("echo -e '\a' >/dev/tty9")
				time.sleep(4)

# 1. On bloque la connexion en root du daemon ssh

writeConfig = True

with open(SSHD_CONFIG, 'r') as file:
	lines = file.readlines()
	for line in lines:
		if "PermitRootLogin no" in line:
			writeConfig = False

if writeConfig == True:
	with open(SSHD_CONFIG, 'a') as file:
		file.writelines('PermitRootLogin no')
	
# 2. On redemarre le daemon

os.system('service sshd restart')

# 3. On écoute le fichier de log sshd

open(SECURE_LOG, 'w').close()
print("En attente de N00bs...")

while 1:

	if os.stat(SECURE_LOG).st_size > 0:
	
		with open(SECURE_LOG, 'r') as file:
			lines = file.readlines()
			ip_noob = ""
			for line in lines:
				if "Failed" in line:
					start = line.index("192.168")+10
					end = line.index("port")-1
					ip_noob = line[start:end]
			if ip_noob != "":
				print("N00b detected: dinfo"+ip_noob)
			
				print("N00b detector started")
				sshCmd("192.168.0."+ip_noob).start()
			
				open(SECURE_LOG, 'w').close()
				print("En attente de N00bs...")
	time.sleep(3)
