# 学生界面
from db.db_manager import DBManager 
import tkinter as tk  
from tkinter import ttk
from utils.helpers import show_info, show_error, show_warning 

class StudentWindow(tk.Tk): 
    def __init__(self,account):
        """初始化学生窗口，设置界面元素和事件绑定"""
        super().__init__()
        self.account = account
        self.db = DBManager()
        self._init_window()
        self._create_widgets()
        self._drawline()
    
    def _drawline(self):
        # 添加分割线或其他装饰元素
        line = tk.Canvas(self, width=2, height=30, highlightthickness=0, bg=self["bg"])
        line.create_line(1, 0, 1, 30, fill="#808099", width=2)
        line.place(x=148, y=0)

        line1 = tk.Canvas(self, width=150, height=2, highlightthickness=0, bg=self["bg"])
        line1.create_line(0, 1, 150, 1, fill="#808099", width=2)
        line1.place(x=0, y=72)

    def _init_window(self):
        self.title("学生模式")
        width = 540
        height = 311
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

    def quit(self):
        """退出登录"""
        self.destroy()
        # 重新打开登录窗口
        from gui.login_window import LoginWindow
        login_window = LoginWindow()
        login_window.mainloop()

    def _create_widgets(self):
        # 退出登录按钮
        self.btn_exit = ttk.Button(self, text="退出登录", takefocus=False, command=self.quit)
        self.btn_exit.place(x=0, y=0, width=73, height=30)
        # 修改信息按钮
        self.btn_modify = ttk.Button(self, text="修改信息", takefocus=False,command=self.change)
        self.btn_modify.place(x=75, y=0, width=73, height=30)
        # 选课按钮
        self.btn_select_course = ttk.Button(self, text="选课", takefocus=False,command=self.enroll)
        self.btn_select_course.place(x=0, y=278, width=73, height=32)
        # 退课按钮
        self.btn_drop_course = ttk.Button(self, text="退课", takefocus=False,command=self.deroll)   
        self.btn_drop_course.place(x=75, y=278, width=73, height=32)
        # 选课/信息标签
        self.label_obj = ttk.Label(self, text="选课查询", anchor="center")
        self.label_obj.place(x=150, y=0, width=62, height=30)
        self.cb_obj_table = ttk.Combobox(self, state="readonly", values=("课程信息","当前选课","教师信息"))
        self.cb_obj_table.place(x=220, y=0, width=245, height=32)
        self.btn_esubmit = ttk.Button(self, text="提交", takefocus=False, command=self._on_esubmit)
        self.btn_esubmit.place(x=472, y=0, width=67, height=30)
        # 问候与学生信息标签
        student = self.db.fetchone(
            "SELECT name, class_id, phone, credit_limit, cur_credit FROM student WHERE student_id=%s", 
            (self.account,)
        )
        name = student[0] if student else ""
        class_id = student[1] if student else ""
        phone = student[2] if student else ""
        credit_limit = student[3] if student else ""
        cur_credit = student[4] if student else ""

        self.label_hello = ttk.Label(self, text="您好！", anchor="center", font=('SimSun', 15))
        self.label_hello.place(x=4, y=35, width=78, height=30)
        self.label_name = ttk.Label(self, text=name, anchor="center", font=('SimSun', 15))
        self.label_name.place(x=70, y=34, width=78, height=30)
        self.label_id_title = ttk.Label(self, text="学号：", anchor="center")
        self.label_id_title.place(x=15, y=82, width=41, height=30)
        self.label_id = ttk.Label(self, text=self.account, anchor="center")
        self.label_id.place(x=56, y=83, width=83, height=30)
        self.label_gender_title = ttk.Label(self, text="班级：", anchor="center")
        self.label_gender_title.place(x=15, y=119, width=41, height=30)
        self.label_gender = ttk.Label(self, text=class_id, anchor="center")
        self.label_gender.place(x=56, y=119, width=83, height=30)
        self.label_phone_title = ttk.Label(self, text="电话：", anchor="center")
        self.label_phone_title.place(x=15, y=157, width=41, height=30)
        self.label_phone = ttk.Label(self, text=phone, anchor="center")
        self.label_phone.place(x=56, y=157, width=83, height=30)
        self.label_max_title = ttk.Label(self, text="选课上限：", anchor="center")
        self.label_max_title.place(x=4, y=195, width=69, height=30)
        self.label_max = ttk.Label(self, text=credit_limit, anchor="center")
        self.label_max.place(x=77, y=195, width=50, height=30)
        self.label_cur_title = ttk.Label(self, text="已选学分：", anchor="center")
        self.label_cur_title.place(x=3, y=234, width=69, height=30)
        self.label_cur = ttk.Label(self, text=cur_credit, anchor="center")
        self.label_cur.place(x=78, y=235, width=50, height=30)
        # 数据表
        columns = {"ID":78, "字段#1":117, "字段#2":195}
        self.table = ttk.Treeview(self, show="headings", columns=list(columns))
        for text, width in columns.items():
            self.table.heading(text, text=text, anchor='center')
            self.table.column(text, anchor='center', width=width, stretch=False)
        self.table.place(x=148, y=30, width=392, height=280)
        # 滚动条
        self._setup_scrollbars()

    def _setup_scrollbars(self):
        # 为table添加垂直和水平滚动条
        vbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        hbar = ttk.Scrollbar(self, orient="horizontal", command=self.table.xview)
        self.table.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        vbar.place(relx=(392 + 148) / 540, rely=30 / 311, relheight=280 / 311, anchor='ne')
        hbar.place(relx=148 / 540, rely=(30 + 280) / 311, relwidth=392 / 540, anchor='sw')
        # 自动隐藏滚动条
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
                    sql = "UPDATE student SET password=%s WHERE student_id=%s"
                elif attr == "电话":
                    sql = "UPDATE student SET phone=%s WHERE student_id=%s"
                else:
                    show_error("error", "请选择正确的属性")
                    return
                self.db.execute(sql, (value, self.account))
                show_info("OK", "修改成功")
                # 更新手机号
                if attr == "电话":
                    self.label_phone.config(text=value)
                change_window.destroy()
            except Exception as e:
                show_error("error", f"修改失败: {e}")

        btn_submit = ttk.Button(change_window, text="提交", command=on_submit)
        btn_submit.place(x=104, y=97, width=50, height=30)

    def enroll(self):
        """选课窗口"""
        enroll_window = tk.Toplevel(self)
        enroll_window.title("选课")
        # 设置窗口大小、居中
        width = 258
        height = 100
        screenwidth = enroll_window.winfo_screenwidth()
        screenheight = enroll_window.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        enroll_window.geometry(geometry)
        enroll_window.resizable(width=False, height=False)

        # 课程编号标签
        label_class_id = ttk.Label(enroll_window, text="课程编号", anchor="center", font=('SimSun', 13))
        label_class_id.place(x=7, y=17, width=78, height=30)
        # 课程编号输入框
        entry_class_id = ttk.Entry(enroll_window)
        entry_class_id.place(x=83, y=16, width=150, height=30)

        # 提交按钮
        def on_submit():
            import datetime
            course_id = entry_class_id.get().strip()
            if not course_id:
                show_warning("warning", "请输入课程编号")
                return
            # 检查课程是否存在
            try:
                sql_check = "SELECT 1 FROM course WHERE course_id=%s"
                result = self.db.fetchone(sql_check, (course_id,))
                if not result:
                    show_error("error", "课程不存在")
                    return
                sql_check_enroll = "SELECT 1 FROM enrollment WHERE course_id=%s AND student_id=%s"
                result_enroll = self.db.fetchone(sql_check_enroll, (course_id, self.account))
                if result_enroll:
                    show_warning("warning", "您已选过此课程")
                    return
                # 检查时间冲突
                sql_time = """
                SELECT 1 FROM enrollment e
                JOIN course c1 ON e.course_id = c1.course_id
                JOIN course c2 ON c2.course_id = %s
                WHERE e.student_id = %s AND c1.class_time = c2.class_time
                """
                conflict = self.db.fetchone(sql_time, (course_id, self.account))
                if conflict:
                    show_warning("warning", "此时段已选课，请重试！")
                    return
                now = datetime.datetime.now()
                # 调用enroll存储过程
                sql = "CALL enroll(%s, %s, %s)"
                self.db.execute(sql, (course_id, self.account, now))
                show_info("OK", "选课成功")
                # 更新已选学分
                cur_credit = self.db.fetchone(
                      "SELECT  cur_credit FROM student WHERE student_id=%s", 
                  (self.account,)
                )
                self.label_cur.config(text=cur_credit)
                enroll_window.destroy()
            except Exception as e:
                show_error("error", f"选课失败: {e}")

        btn_submit = ttk.Button(enroll_window, text="提交", command=on_submit)
        btn_submit.place(x=104, y=59, width=50, height=30)

    def deroll(self):
        """退课窗口"""
        deroll_window = tk.Toplevel(self)
        deroll_window.title("退课")
        # 设置窗口大小、居中
        width = 258
        height = 100
        screenwidth = deroll_window.winfo_screenwidth()
        screenheight = deroll_window.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        deroll_window.geometry(geometry)
        deroll_window.resizable(width=False, height=False)

        # 课程编号标签
        label_class_id = ttk.Label(deroll_window, text="课程编号", anchor="center", font=('SimSun', 13))
        label_class_id.place(x=7, y=17, width=78, height=30)
        # 课程编号输入框
        entry_class_id = ttk.Entry(deroll_window)
        entry_class_id.place(x=83, y=16, width=150, height=30)

        # 提交按钮
        def on_submit():
            course_id = entry_class_id.get().strip()
            if not course_id:
                show_warning("warning", "请输入课程编号")
                return
            try:
                sql_check_enroll = "SELECT 1 FROM enrollment WHERE course_id=%s AND student_id=%s"
                result_enroll = self.db.fetchone(sql_check_enroll, (course_id, self.account))
                if not result_enroll:
                    show_error("error", "您未选此课程")
                    return
                # 删除enrollment表中的记录
                sql_delete = "DELETE FROM enrollment WHERE course_id=%s AND student_id=%s"
                self.db.execute(sql_delete, (course_id, self.account))
                # 更新student表的cur_credit属性
                sql_update_student = """
                    UPDATE student 
                    SET cur_credit = (
                        SELECT IFNULL(SUM(c.credits), 0)
                        FROM enrollment e
                        JOIN course c ON e.course_id = c.course_id
                        WHERE e.student_id = %s
                    )
                    WHERE student_id = %s
                """
                self.db.execute(sql_update_student, (self.account, self.account))
                # 更新course表的cur_enrollment属性
                sql_update_course = """
                    UPDATE course
                    SET cur_enrollment = (
                        SELECT COUNT(*) FROM enrollment WHERE course_id = %s
                    )
                    WHERE course_id = %s
                """
                self.db.execute(sql_update_course, (course_id, course_id))
                show_info("OK", "退课成功")
                # 更新已选学分
                cur_credit = self.db.fetchone(
                      "SELECT  cur_credit FROM student WHERE student_id=%s", 
                  (self.account,)
                )
                self.label_cur.config(text=cur_credit)
                deroll_window.destroy()
            except Exception as e:
                show_error("error", f"退课失败: {e}")

        btn_submit = ttk.Button(deroll_window, text="提交", command=on_submit)
        btn_submit.place(x=104, y=59, width=50, height=30)


    def _on_esubmit(self):
        """选课查询提交按钮事件"""
        choice = self.cb_obj_table.get()
        # 清空表格
        for col in self.table["columns"]:
            self.table.heading(col, text="")
            self.table.column(col, width=0)
        self.table.delete(*self.table.get_children())
        if choice == "课程信息":
            try:
                sql = "SELECT * FROM course_all"
                rows = self.db.fetchall(sql)
                if not rows:
                    return
                columns = rows[0].keys() if hasattr(rows[0], "keys") else [desc[0] for desc in self.db.cursor.description]
                self.table["columns"] = list(columns)
                for col in columns:
                    self.table.heading(col, text=col, anchor='center')
                    self.table.column(col, anchor='center', width=100, stretch=False)
                for row in rows:
                    values = list(row.values()) if hasattr(row, "values") else list(row)
                    self.table.insert("", "end", values=values)
            except Exception as e:
                show_error("error", f"查询失败: {e}")
        elif choice == "当前选课":
            try:
                # 只显示指定列
                columns = ["选课时间","课程编号", "课程名称", "授课教师", "开课学院", "课程类型", "学分", "上课时间", "上课地点", "成绩"]
                sql = "SELECT `选课时间`,`课程编号`, `课程名称`, `授课教师`, `开课学院`, `课程类型`, `学分`, `上课时间`, `上课地点`, `成绩` FROM enroll_all WHERE student_id=%s"
                rows = self.db.fetchall(sql, (self.account,))
                self.table["columns"] = columns
                for col in columns:
                    self.table.heading(col, text=col, anchor='center')
                    self.table.column(col, anchor='center', width=100, stretch=False)
                for row in rows:
                    values = list(row.values()) if hasattr(row, "values") else list(row)
                    self.table.insert("", "end", values=values)
            except Exception as e:
                show_error("error", f"查询失败: {e}")
        elif choice == "教师信息":
            try:
                sql = "SELECT * FROM tec_all"
                rows = self.db.fetchall(sql)
                if not rows:
                    return
                columns = rows[0].keys() if hasattr(rows[0], "keys") else [desc[0] for desc in self.db.cursor.description]
                self.table["columns"] = list(columns)
                for col in columns:
                    self.table.heading(col, text=col, anchor='center')
                    self.table.column(col, anchor='center', width=100, stretch=False)
                for row in rows:
                    values = list(row.values()) if hasattr(row, "values") else list(row)
                    self.table.insert("", "end", values=values)
            except Exception as e:
                show_error("error", f"查询失败: {e}")
        else:
            # 默认空表头
            columns = {"ID":78, "字段#1":117, "字段#2":195}
            self.table["columns"] = list(columns)
            for text, width in columns.items():
                self.table.heading(text, text=text, anchor='center')
                self.table.column(text, anchor='center', width=width, stretch=False)



