# 公用工具函数
from tkinter import messagebox

def show_info(title: str, message: str):
    """
    弹出信息提示框
    """
    messagebox.showinfo(title, message)

def show_error(title: str, message: str):
    """
    弹出错误提示框
    """
    messagebox.showerror(title, message)

def show_warning(title: str, message: str):
    """
    弹出警告提示框
    """
    messagebox.showwarning(title, message)
