#!/usr/bin/python3
# -*- coding:utf-8 -*-

# Create by youtube.com/@UserEdition

import psutil
import time
import socket

from lib import epd2in13_V3
from PIL import Image,ImageDraw,ImageFont

# display init and clear
epd = epd2in13_V3.EPD()
epd.init()

# colors
color_1 = 255
color_2 = 0

# fonts
font_1 = 'font/visitor-brk.visitor-tt1-brk.ttf'
font_2 = 'font/roboto-condensed.bold.ttf'

# fonts size
font15 = 15
font16 = 16
font17 = 17

# fonts for display
tempfont = ImageFont.truetype(font_1, 55)
tempsymbol = ImageFont.truetype(font_2, 25)

timefont = ImageFont.truetype(font_1, font15)

psfont = ImageFont.truetype(font_1, font15)
pssymbol = ImageFont.truetype(font_2, font15)

cpu_usagefont = ImageFont.truetype(font_1, font15)
cpu_usagesymbol = ImageFont.truetype(font_2, font15)

mem_usagefont = ImageFont.truetype(font_1, font15)
mem_usagesymbol = ImageFont.truetype(font_2, font15)

host_font = ImageFont.truetype(font_1, font15)
host_symbol = ImageFont.truetype(font_2, font15)

user_font = ImageFont.truetype(font_1, font15)
user_symbol = ImageFont.truetype(font_2, font15)

mhz_usagefont = ImageFont.truetype(font_1, font15)
mhz_usagesymbol = ImageFont.truetype(font_2, font15)

# search ip address
def get_ip_address():
	try:
		ip_address = '';
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("dns.google.com",80))
		ip_address = s.getsockname()[0]
		s.close()
		return ip_address
	except socket.error:
		return "dns/fail"

# show data on display
def show_data():

	while True:

		# image display
		image = Image.new('1', (epd.height, epd.width), color_1)
		draw = ImageDraw.Draw(image)

		# data for display
		hostname = socket.gethostname()
		cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
		cpu_percent = psutil.cpu_percent(interval = 1)
		core = psutil.cpu_freq().current
		mem_info = psutil.virtual_memory()
		mem_percent = mem_info.percent
		time_now = time.localtime()
		time_current = time.strftime("%H:%M", time_now)
		ps = str(len(psutil.pids()))

		# line 1
		draw.line((0, 72, 90, 72), width = 1, fill = color_2)

		# line 2
		draw.line((90, 72, 111, 100), width = 2, fill = color_2)
		
		# line 3
		draw.line((111, 72, 132, 100), width = 2, fill = color_2)
		
		# line 4
		draw.line((132, 100, 250, 100), width = 1, fill = color_2)

		# line 5
		draw.line((210, 15, 250, 15), width = 1, fill = color_2)

		# line 6
		draw.line((205, 22, 210, 15), width = 1, fill = color_2)

		# cpu temp
		# draw.text((5,75), ""+str(round(cpu_temp))+"", font = tempfont, fill = color_2)
		# draw.text((73,90), "\u00b0C", font = tempsymbol, fill = color_2)

		# time
		draw.text((211,0), ""+str(time_current)+"", font = timefont, fill = color_2)

		# processes
		# draw.text((175,104), "Proc. ", font = pssymbol, fill = color_2)
		# draw.text((215,107), ""+ps, font = psfont, fill = color_2)

		# mhz usage
		# draw.text((5,4), "Mhz. ", font = mhz_usagesymbol, fill = color_2)
		# draw.text((50,7), ""+str(core)+"", font = mhz_usagefont, fill = color_2)

		# cpu usage
		# draw.text((5,24), "Cpu. ", font = cpu_usagesymbol, fill = color_2)
		# draw.text((50,27), ""+str(cpu_percent)+" %", font = cpu_usagefont, fill = color_2)

		# memory usage
		# draw.text((5,44), "Mem. ", font = mem_usagesymbol, fill = color_2)
		# draw.text((50,47), ""+str(mem_percent)+" %", font = mem_usagefont, fill = color_2)

		# host
		draw.text((125,15), "Host.", font = host_symbol, fill = color_2)
		draw.text((130,32), ""+str(hostname)+"", font = host_font, fill = color_2)

		# ip
		# draw.text((125,50), "Ip.", font = user_symbol, fill = color_2)
		# draw.text((130,67), ""+str(get_ip_address())+"", font = user_font, fill = color_2)

		# show data on display
		epd.display(epd.getbuffer(image.rotate(90)))

		# refresh display (5 min)
		time.sleep(300)


if __name__ == '__main__':
	try:
		show_data()
	except:
		print('\nCtrl + c')
	finally:
		epd.Clear()
		exit()
