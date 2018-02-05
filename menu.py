#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import os,sys,time

class menu():
	'''Display a menu and different choices'''
	def __init__(self):

		self.version = "version 0.1 credit : Dylan Iffrig and Axel Roudaut\n"

		self.header = "\n\n\
████████╗██╗  ██╗ ██████╗    ██████╗ ██╗     ██╗   ██╗███████╗██████╗  ██████╗ ██████╗ ███╗   ██╗███████╗\n\
╚══██╔══╝██║  ██║██╔════╝    ██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗██╔═══██╗██╔══██╗████╗  ██║██╔════╝\n\
   ██║   ███████║██║         ██████╔╝██║     ██║   ██║█████╗  ██████╔╝██║   ██║██████╔╝██╔██╗ ██║█████╗  \n\
   ██║   ██╔══██║██║         ██╔══██╗██║     ██║   ██║██╔══╝  ██╔══██╗██║   ██║██╔══██╗██║╚██╗██║██╔══╝  \n\
   ██║   ██║  ██║╚██████╗    ██████╔╝███████╗╚██████╔╝███████╗██████╔╝╚██████╔╝██║  ██║██║ ╚████║███████╗\n\
   ╚═╝   ╚═╝  ╚═╝ ╚═════╝    ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝\n\n"
                                                                                                         
		self.colors = {
				"blue" : "\033[94m",
				"pink" : "\033[95m",
				"green" : "\033[92m",
				"orange" : "\033[33m",
				"red" : "\033[31m"
				}

		self.choices = [
			{"Show interfaces" : self.f1},
			{"Sniffing" : self.f2},
			{"Exploiting" : self.f3},
			{"Exit" : self.f4},
				]
	

	def colorize(self):
		''' Colorize stuff '''
		self.header = self.colors["blue"] + self.header + "\033[0m"
		self.version = self.colors["green"] + self.version + "\033[0m"


	def display_menu(self):
		while True:
			os.system('clear')
			self.colorize()
			print(self.header)
			print(self.version)
			for item in self.choices:
				print("[" + self.colors["red"] + str(self.choices.index(item)) + "\033[0m" + "]" +
						item.keys()[0])
			try:
				choice = input(">> ")
				action = self.choices[int(choice)].values()[0]
				if not action:
					raise ValueError
				action()
				time.sleep(5)
			except(ValueError, IndexError, NameError, SyntaxError):
				pass

	def f1(self):
		print("choice 1\n")
	def f2(self):
		print("choice 2\n")
	def f3(self):
		print("choice 3\n")
	def f4(self):
		print("exit...\n")
		sys.exit(0)


if __name__ == "__main__":
	men = menu()
	men.display_menu()
