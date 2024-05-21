# Use usb to print out of a Godex RT863i printer
# we will print some random text

import win32print
import win32ui
import win32con
import win32api
import os
from PIL import Image, ImageDraw, ImageFont
import random
import string

def print_text(printer_name, text):
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Test Print", None, "RAW"))
        try:
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, text.encode())
            win32print.EndPagePrinter(hPrinter)
        finally:
            win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)

def print_text_file(printer_name, file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    print_text(printer_name, text)

def print_text_file_with_font(printer_name, file_path, font_path, font_size):
    with open(file_path, 'r') as f:
        text = f.read()
    print_text_with_font(printer_name, text, font_path, font_size)

def print_text_with_font(printer_name, text, font_path, font_size):
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Test Print", None, "RAW"))
        try:
            win32print.StartPagePrinter(hPrinter)
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)
            hDC.StartDoc("Test Print")
            hDC.StartPage()
            hDC.SetMapMode(win32con.MM_TWIPS)
            hDC.SetTextAlign(win32con.TA_CENTER)
            hDC.SetTextColor(win32api.RGB(0, 0, 0))
            hDC.SetBkMode(win32con.TRANSPARENT)
            hDC.SetFont((font_path, font_size, 0))
            hDC.TextOut(3000, 3000, text)
            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()
            win32print.EndPagePrinter(hPrinter)
        finally:
            win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)

def print_text_with_font_and_image(printer_name, text, font_path, font_size, image_path):
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Test Print", None, "RAW"))
        try:
            win32print.StartPagePrinter(hPrinter)
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)
            hDC.StartDoc("Test Print")
            hDC.StartPage()
            hDC.SetMapMode(win32con.MM_TWIPS)
            hDC.SetTextAlign(win32con.TA_CENTER)
            hDC.SetTextColor(win32api.RGB(0, 0, 0))
            hDC.SetBkMode(win32con.TRANSPARENT)
            hDC.SetFont((font_path, font_size, 0))
            hDC.TextOut(3000, 3000, text)
            hDC.DrawIcon((3000, 6000), hDC.CreateIconFromResource(win32api.LoadResource(0, win32con.OIC_INFORMATION, 0)))
            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()
            win32print.EndPagePrinter(hPrinter)
        finally:
            win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)


        # print the text
printer_name = win32print.GetDefaultPrinter()
text = "Hello World"
print_text(printer_name, text)

