# 登录界面
from db.db_manager import DBManager 
import tkinter as tk  
from tkinter import ttk
from utils.helpers import show_info, show_error, show_warning 
from gui.student_window import StudentWindow  # 学生窗口
from gui.teacher_window import TeacherWindow  # 教师窗口
from gui.admin_window import AdminWindow  # 教师窗口

class LoginWindow(tk.Tk):  # tk.Tk 是 tkinter 的核心类，负责创建主窗口并初始化 GUI 环境
    def __init__(self):
        """初始化登录窗口，设置界面元素和事件绑定"""
        super().__init__()
        # 窗口设置
        self.title("欢迎来到选课系统")
        width = 320
        height = 220
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (
            width, height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2
        )
        self.geometry(geometry)
        self.resizable(width=False, height=False)

        # 身份下拉框
        self.label_identity = ttk.Label(self, text="身份",font=('SimSun', 15), anchor="center")
        self.label_identity.place(x=40, y=30, width=67, height=30)
        self.combobox_identity = ttk.Combobox(self, state="readonly",font=('SimSun', 13))
        self.combobox_identity['values'] = ("学生", "教师","管理员")
        self.combobox_identity.current(0)
        self.combobox_identity.place(x=140, y=30, width=150, height=30)

        # 账号
        self.label_account = ttk.Label(self, text="账号",font=('SimSun', 15), anchor="center")
        self.label_account.place(x=40, y=87, width=67, height=30)
        self.entry_account = ttk.Entry(self)
        self.entry_account.place(x=140, y=86, width=150, height=30)

        # 密码
        self.label_password = ttk.Label(self, text="密码",font=('SimSun', 15), anchor="center")
        self.label_password.place(x=40, y=143, width=67, height=30)
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.place(x=140, y=142, width=150, height=30)

        # 登录按钮
        self.button_login = ttk.Button(self, text="登录", command=self.login)
        self.button_login.place(x=135, y=180, width=50, height=30)

    def login(self):
        """登录按钮回调，验证身份信息，切换到相应窗口"""
        # 这里可以添加登录逻辑
        identity = self.combobox_identity.get()
        account = self.entry_account.get()
        password = self.entry_password.get()
        # 示例弹窗
        if not account or not password:
            show_warning("warning","请输入账号和密码")
            return
        elif identity == "学生":
            if DBManager().fetchone("SELECT * FROM student WHERE student_id=%s AND password=%s", (account, password)):
                self.destroy()
                StudentWindow(account).mainloop()
            else:
                show_error("error","账号或密码错误")
        elif identity == "教师":
            if DBManager().fetchone("SELECT * FROM teacher WHERE teacher_id=%s AND password=%s", (account, password)):
                self.destroy()
                TeacherWindow(account).mainloop()
            else:
                show_error("error","账号或密码错误")
        elif identity == "管理员":
            if DBManager().fetchone("SELECT * FROM admin WHERE admin_id=%s AND password=%s", (account, password)):
                self.destroy()
                AdminWindow(account).mainloop()
            else:
                show_error("error","账号或密码错误")
