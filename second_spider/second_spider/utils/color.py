# -*- coding: UTF-8 -*- 
#-------------------------------------
# Name: 
# Purpose: windows CMD终端打印彩色字体（调用windows API�?
# Author:
# Date: 2015-11-10
#-------------------------------------

import ctypes


STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12

FOREGROUND_BLACK = 0x0
FOREGROUND_BLUE = 0x01 # text color contains blue.
FOREGROUND_GREEN= 0x02 # text color contains green.
FOREGROUND_RED = 0x04 # text color contains red.
FOREGROUND_INTENSITY = 0x08 # text color is intensified.

BACKGROUND_BLUE = 0x10 # background color contains blue.
BACKGROUND_GREEN= 0x20 # background color contains green.
BACKGROUND_RED = 0x40 # background color contains red.
BACKGROUND_INTENSITY = 0x80 # background color is intensified.


class Color:
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
#     std_out_handle = GetStdHandle(STD_OUTPUT_HANDLE)
    
    def set_cmd_color(self, color, handle=std_out_handle):
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool
    
    #初始化颜色为黑色背景，纯白色字，CMD默认为灰色字�?
    def reset_color(self):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        
    
    #红色字体    
    def print_red_text(self, print_text):
        self.set_cmd_color(4 | 8)
        print print_text
        self.reset_color()
        
    #绿色字体    
    def print_green_text(self, print_text):
        self.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
        c = raw_input(print_text)
        self.reset_color()
        return c
        
    #黄色字体    
    def print_yellow_text(self, print_text): 
        self.set_cmd_color(6 | 8)
        print print_text
        self.reset_color()
        
    #蓝色字体
    def print_blue_text(self, print_text): 
        self.set_cmd_color(1 | 10)
        print print_text
        self.reset_color()
