
"""
For build GeneralPlus GPCE4 project.

Copyright (c) 2016, C.C.LIN(Viisin)
License: MIT (see LICENSE for details)
"""

import os
import subprocess

__author__ = 'C.C.LIN'
__version__ = '0.1.0'
__license__ = 'MIT'

def exe(command, path=None):
	if path is None:
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	else:
		process = subprocess.Popen(command, env={'PATH':path}, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = process.communicate()
	return process.returncode, out, err

def createFolder(folder):
	if not os.path.exists(folder):
		os.makedirs(folder)
		
def splitFilename(file):
	path, name = os.path.split(file)
	name, ext = os.path.splitext(name)
	return path, name, ext

class GPCE4Project:
	def __init__(self, project, env):
		self.__PROJECT = project
		self.__PATH = env
		self.__UDOCC = os.path.join(self.__PATH, 'udocc.exe')
		self.__CC = os.path.join(self.__PATH, 'gcc.exe')
		self.__AS = os.path.join(self.__PATH, 'xasm16.exe')
		self.__LD = os.path.join(self.__PATH, 'xlink16.exe')
		self.__LIB = os.path.join(self.__PATH, 'xlib16.exe')
		self.__reference = []
		self.__source = []
		self.__include = []
		self.__cflag = ['-S', '-Wall', '-mglobal-var-iram', '-mISA=2.0']
		self.__asflag = ['-t4', '-sr']
		self.__ldflag = []
		self.__object = []
		self.__outfolder = None
		# Check toolchain exist
		toolchain = []
		toolchain.append(self.__UDOCC)
		toolchain.append(self.__CC)
		toolchain.append(self.__AS)
		toolchain.append(self.__LD)
		toolchain.append(self.__LIB)
		for tool in toolchain:
			if(os.path.isfile(tool)==False):
				raise Exception(tool + ' not found.')

	def setIntermediateFolder(self, folder):
		self.__outfolder = folder

	def addCFlag(self, flag):
		self.__cflag.append(flag)

	def addReferencePath(self, path):
		if(os.path.isdir(path) == False):
			raise Exception(path + ' not found.')
		self.__reference.append(path)

	def addSourceFile(self, file):
		if(os.path.isfile(file) == False):
			for path in self.__reference:
				f = os.path.join(path, file)
				if(os.path.isfile(f) == True):
					self.__source.append(f)
					return
			raise Exception(file + ' not found.')
		else:
			self.__source.append(file)

	def addIncludePath(self, path):
		if(os.path.isdir(path) == False):
			raise Exception(path + ' not found.')
		self.__include.append(path)

	def compileC(self, file):
		path, name, ext = splitFilename(file)
		output = name + '.s'
		command = [self.__CC] + self.__cflag
		for path in self.__include:
			command.append('-I"' + path + '"')
		if self.__outfolder is not None:
			createFolder(self.__outfolder)
			output = self.__outfolder + '/' + output
			command.append('-o')
			command.append(output)
		command.append(file)
		code, out, err = exe(command, self.__PATH)
		if code != 0:
			return (code == 0), out, err, output
		return self.compileAsm(output)

	def compileAsm(self, file):
		path, name, ext = splitFilename(file)
		output = name + '.obj'
		command = [self.__AS] + self.__asflag
		for path in self.__include:
			command.append('-I' + path)
		if self.__outfolder is not None:
			createFolder(self.__outfolder)
			output = self.__outfolder + '/' + output
			command.append('-o')
			command.append(output)
		command.append(file)
		code, out, err = exe(command, self.__PATH)
		return (code == 0), out, err, output

	#def linkObject(self, object):
	#	pass

	def buildLibrary(self):
		# Empty check
		if(len(self.__source) == 0):
			raise Exception('No file added.')
		# Delete library
		try:
			if os.path.exists(self.__PROJECT):
				os.remove(self.__PROJECT)
		except OSError:
			raise Exception('Can not remove file "' + self.__PROJECT + '"')
		# Compile source
		del self.__object[:]
		for file in self.__source:
			print('Compiling \'' + file + '\'...', end="")
			path, name, ext = splitFilename(file)
			if ext.lower() == '.c':
				code, out, err, output = self.compileC(file)
			elif ext.lower() == '.asm':
				code, out, err, output = self.compileAsm(file)
			else:
				print(' (failed)')
				raise Exception(ext + ' not support.')
			if code == True:
				if(os.path.isfile(output) == False):
					print(' (failed)')
					raise Exception(output + ' not found.')
				self.__object.append(output)
				print(' (ok)')
			else:
				print(' (failed)')
				print(err)
				raise Exception('\'' + file + '\' compile failed.')
		# Build library
		print('Build static library\'' + self.__PROJECT + '\'...')
		command = [self.__LIB] + [self.__PROJECT] + ['new']
		code, out, err = exe(command, self.__PATH)
		if code != 0:
			print(err)
			raise Exception('\'' + self.__PROJECT + '\' new failed.')
		for object in self.__object:
			command = [self.__LIB] + [self.__PROJECT] + ['add', object]
			code, out, err = exe(command, self.__PATH)
			if code != 0:
				print(err)
				raise Exception('\'' + self.__PROJECT + '\' add \'' + object + '\' failed.')
