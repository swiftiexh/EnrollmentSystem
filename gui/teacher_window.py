# 教师界面
from db.db_manager import DBManager 
import tkinter as tk  
from tkinter import ttk
from utils.helpers import show_info, show_error, show_warning 

class TeacherWindow(tk.Tk): 
    def __init__(self,account):
        """初始化教师窗口，设置界面元素和事件绑定"""
        super().__init__()
        self.account = account
        self.db = DBManager()
        self._init_window()
        self._create_widgets()
        self._drawline()

    def _init_window(self):
        self.title("教师模式")
        width = 540
        height = 311
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

    def _drawline(self):
        # 添加分割线或其他装饰元素
        line = tk.Canvas(self, width=2, height=30, highlightthickness=0, bg=self["bg"])
        line.create_line(1, 0, 1, 32, fill="#808099", width=2)
        line.place(x=150, y=0)

        line1 = tk.Canvas(self, width=150, height=2, highlightthickness=0, bg=self["bg"])
        line1.create_line(0, 1, 150, 1, fill="#808099", width=2)
        line1.place(x=0, y=85)

    def quit(self):
        """退出登录"""
        self.destroy()
        # 重新打开登录窗口
        from gui.login_window import LoginWindow
        login_window = LoginWindow()
        login_window.mainloop()

    def _create_widgets(self):
        # 退出登录按钮
        self.btn_exit = ttk.Button(self, text="退出登录", takefocus=False,command=self.quit)
        self.btn_exit.place(x=0, y=0, width=73, height=30)
        # 修改信息按钮
        self.btn_modify = ttk.Button(self, text="修改信息", takefocus=False,command=self.change)
        self.btn_modify.place(x=76, y=0, width=73, height=30)
        # 选课查询标签
        self.label_obj = ttk.Label(self, text="选课查询", anchor="center")
        self.label_obj.place(x=150, y=0, width=62, height=30)
        # 查询教师开设课程名称
        courses = self.db.fetchall(
            "SELECT c.name FROM teaching t JOIN course c ON t.course_id = c.course_id WHERE t.teacher_id = %s",
            (self.account,)
        )
        course_names = ["全部课程"]+ [row[0] for row in courses]+["学生信息"]  if courses else ["全部课程","学生信息"]
        self.cb_obj_table = ttk.Combobox(self, state="readonly", values=course_names)
        self.cb_obj_table.place(x=220, y=0, width=245, height=32)
        self.btn_qsubmit = ttk.Button(self, text="提交", takefocus=False, command=self._on_qsubmit)
        self.btn_qsubmit.place(x=472, y=0, width=67, height=30)
        # 录入成绩按钮
        self.btn_score = ttk.Button(self, text="录入成绩", takefocus=False,command=self.score)
        self.btn_score.place(x=8, y=274, width=128, height=30)
        # 问候与教师信息标签
        teacher = self.db.fetchone(
            "SELECT 姓名, 院系, 职称, 电话,研究方向,是否兼职 FROM tec_all WHERE 编号=%s", 
            (self.account,)
        )
        name = teacher[0] if teacher else ""
        dep = teacher[1] if teacher else ""
        stat = teacher[2] if teacher else ""
        phone = teacher[3] if teacher else ""
        area = teacher[4] if teacher else ""
        part = "兼职" if teacher[5] else "全职"   

        self.label_hello = ttk.Label(self, text="您好！", anchor="center", font=('SimSun', 16))
        self.label_hello.place(x=4, y=45, width=85, height=30)
        self.label_name = ttk.Label(self, text=name, anchor="center", font=('SimSun', 16))
        self.label_name.place(x=70, y=44, width=85, height=30)
        self.label_id = ttk.Label(self, text="编号", anchor="center")
        self.label_id.place(x=4, y=102, width=50, height=30)
        self.label_i_id = ttk.Label(self, text=self.account, anchor="center")
        self.label_i_id.place(x=56, y=103, width=83, height=30)
        self.label_dep = ttk.Label(self, text="院系", anchor="center")
        self.label_dep.place(x=4, y=133, width=50, height=30)
        self.label_i_dep = ttk.Label(self, text=dep, anchor="center", font=('SimSun', 8))
        self.label_i_dep.place(x=46, y=134, width=105, height=30)
        self.label_stat = ttk.Label(self, text="职称", anchor="center")
        self.label_stat.place(x=5, y=164, width=50, height=30)
        self.label_mb7evwl6 = ttk.Label(self, text=stat, anchor="center")
        self.label_mb7evwl6.place(x=71, y=165, width=67, height=30)
        self.label_others = ttk.Label(self, text="研究方向" if area else "是否兼职", anchor="center")
        self.label_others.place(x=0, y=195, width=60, height=30)
        self.label_mb7ew1n1 = ttk.Label(self, text=area if area else part, anchor="center")
        self.label_mb7ew1n1.place(x=56, y=195, width=83, height=30)
        self.label_phone = ttk.Label(self, text="电话", anchor="center")
        self.label_phone.place(x=5, y=226, width=41, height=30)
        self.label_i_phone = ttk.Label(self, text=phone, anchor="center")
        self.label_i_phone.place(x=56, y=227, width=83, height=30)
        # 数据表
        columns = {"ID":77, "字段#1":116, "字段#2":194}
        self.table = ttk.Treeview(self, show="headings", columns=list(columns))
        for text, width in columns.items():
            self.table.heading(text, text=text, anchor='center')
            self.table.column(text, anchor='center', width=width, stretch=False)
        self.table.place(x=150, y=31, width=389, height=279)
        # 滚动条
        self._setup_scrollbars()

    def _setup_scrollbars(self):
        vbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        hbar = ttk.Scrollbar(self, orient="horizontal", command=self.table.xview)
        self.table.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        vbar.place(relx=(389 + 150) / 540, rely=31 / 311, relheight=279 / 311, anchor='ne')
        hbar.place(relx=150 / 540, rely=(31 + 279) / 311, relwidth=389 / 540, anchor='sw')
        self._scrollbar_autohide(vbar, hbar, self.table)

    def _scrollbar_autohide(self, vbar, hbar, widget):
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def _on_qsubmit(self):
        """教师查询提交按钮事件"""
        choice = self.cb_obj_table.get()
        # 清空表格
        for col in self.table["columns"]:
            self.table.heading(col, text="")
            self.table.column(col, width=0)
        self.table.delete(*self.table.get_children())
        try:
            if choice == "全部课程":
                # 查找当前教师名称
                teacher_name = self.db.fetchone("SELECT name  FROM teacher WHERE teacher_id=%s", (self.account,))
                if teacher_name:
                    teacher_name = teacher_name[0]
                else:
                    show_error("error", "未找到教师信息")
                    return
                sql = "SELECT 课程编号, 名称, 类型, 学分, 上课时间, 上课地点, 人数上限, 目前选课 FROM course_all WHERE 授课教师=%s"
                rows = self.db.fetchall(sql, (teacher_name,))
                columns = ["课程编号", "名称", "类型", "学分", "上课时间", "上课地点", "人数上限", "目前选课"]
            elif choice == "学生信息":
                sql = "SELECT 学号, 姓名, 性别, 班级, 专业, 入学年份, 电话 FROM stu_all"
                rows = self.db.fetchall(sql)
                columns = ["学号", "姓名", "性别", "班级", "专业", "入学年份", "电话"]
            else:
                # 课程名称
                sql = "SELECT  课程编号,student_id AS学号, 学生姓名, 成绩, 选课时间 FROM enroll_all WHERE 课程名称=%s"
                rows = self.db.fetchall(sql, (choice,))
                columns = ["课程编号","学号", "学生姓名", "成绩", "选课时间"]
            self.table["columns"] = columns
            for col in columns:
                self.table.heading(col, text=col, anchor='center')
                self.table.column(col, anchor='center', width=100, stretch=False)
            for row in rows:
                values = list(row.values()) if hasattr(row, "values") else list(row)
                self.table.insert("", "end", values=values)
        except Exception as e:
            show_error("error", f"查询失败: {e}")

    def score(self):
        """录入成绩按钮回调"""
        score_window = tk.Toplevel(self)
        score_window.title("录入成绩")
        # 设置窗口大小、居中
        width = 260
        height = 190
        screenwidth = score_window.winfo_screenwidth()
        screenheight = score_window.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        score_window.geometry(geometry)
        score_window.resizable(width=False, height=False)

        # 学号
        label_s_id = ttk.Label(score_window, text="学号", anchor="center", font=('SimSun', 13))
        label_s_id.place(x=4, y=16, width=78, height=30)
        entry_s_id = ttk.Entry(score_window)
        entry_s_id.place(x=84, y=15, width=150, height=30)
        # 课程编号
        label_c_id = ttk.Label(score_window, text="课程编号", anchor="center", font=('SimSun', 13))
        label_c_id.place(x=4, y=60, width=78, height=30)
        entry_c_id = ttk.Entry(score_window)
        entry_c_id.place(x=83, y=60, width=150, height=30)
        # 成绩
        label_score = ttk.Label(score_window, text="成绩", anchor="center", font=('SimSun', 13))
        label_score.place(x=4, y=104, width=78, height=30)
        entry_score = ttk.Entry(score_window)
        entry_score.place(x=82, y=104, width=150, height=30)

        # 提交按钮
        def submit_score():
            student_id = entry_s_id.get().strip()
            course_id = entry_c_id.get().strip()
            score = entry_score.get().strip()
            if not student_id or not course_id or not score:
                show_warning("warning", "请填写所有字段")
                return
            try:
                # 检查enrollment表中是否存在该学生和课程的记录
                enroll = self.db.fetchone(
                    "SELECT 1 FROM enrollment WHERE student_id=%s AND course_id=%s",
                    (student_id, course_id)
                )
                if not enroll:
                    show_error("错误", "输入错误或没有权限")
                    return
                # 更新成绩
                self.db.execute(
                    "UPDATE enrollment SET grade=%s WHERE student_id=%s AND course_id=%s",
                    (score, student_id, course_id)
                )
                show_info("Success", "成绩录入成功")
                score_window.destroy()
            except Exception as e:
                show_error("Error", f"录入失败: {e}")

        btn_submit = ttk.Button(score_window, text="提交", command=submit_score)
        btn_submit.place(x=74, y=149, width=112, height=30)
    
    def change(self):
        """修改信息窗口"""
        change_window = tk.Toplevel(self)
        change_window.title("修改信息")
        # 设置窗口大小、居中
        width = 258
        height = 140
        screenwidth = change_window.winfo_screenwidth()
        screenheight = change_window.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        change_window.geometry(geometry)
        change_window.resizable(width=False, height=False)

        # 修改属性
        label_attr = ttk.Label(change_window, text="修改属性", anchor="center", font=('SimSun', 13))
        label_attr.place(x=10, y=17, width=78, height=30)
        cb_attr = ttk.Combobox(change_window, state="readonly")
        cb_attr['values'] = ("密码", "电话")
        cb_attr.place(x=91, y=17, width=150, height=30)

        # 修改值
        label_data = ttk.Label(change_window, text="修改值", anchor="center", font=('SimSun', 13))
        label_data.place(x=15, y=58, width=70, height=30)
        entry_data = ttk.Entry(change_window)
        entry_data.place(x=91, y=58, width=150, height=30)

        # 提交按钮
        def on_submit():
            attr = cb_attr.get().strip()
            value = entry_data.get().strip()
            if not attr or not value:
                show_warning("warning", "请填写完整信息")
                return
            try:
                if attr == "密码":
                    sql = "UPDATE teacher SET password=%s WHERE teacher_id=%s"
                elif attr == "电话":
                    sql = "UPDATE teacher SET phone=%s WHERE teacher_id=%s"
                else:
                    show_error("error", "请选择正确的属性")
                    return
                self.db.execute(sql, (value, self.account))
                show_info("OK", "修改成功")
                # 更新手机号
                if attr == "电话":
                    self.label_i_phone.config(text=value)
                change_window.destroy()
            except Exception as e:
                show_error("error", f"修改失败: {e}")

        btn_submit = ttk.Button(change_window, text="提交", command=on_submit)
        btn_submit.place(x=104, y=97, width=50, height=30)
