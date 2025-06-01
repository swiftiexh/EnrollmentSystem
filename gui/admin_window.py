# 管理员界面
from db.db_manager import DBManager 
import tkinter as tk  
from tkinter import ttk
from utils.helpers import show_info, show_error, show_warning 

class AdminWindow(tk.Tk): 
    def __init__(self,account):
        """初始化管理员窗口，设置界面元素和事件绑定"""
        super().__init__()
        self.account = account
        self._init_window()
        self._create_widgets()
        self._drawline()
        self.db = DBManager()

    def _drawline(self):
        # 添加分割线或其他装饰元素
        line = tk.Canvas(self, width=2, height=30, highlightthickness=0, bg=self["bg"])
        line.create_line(1, 0, 1, 30, fill="#808099", width=2)
        line.place(x=228, y=0)

        line1 = tk.Canvas(self, width=226, height=2, highlightthickness=0, bg=self["bg"])
        line1.create_line(0, 1, 226, 1, fill="#808099", width=2)
        line1.place(x=0, y=220)
        
    def _init_window(self):
        self.title("管理员模式")
        width = 700
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
#-----------------------------------------------------------------------------------------------------------------
    def quit(self):
        """退出登录"""
        self.destroy()
        # 重新打开登录窗口
        from gui.login_window import LoginWindow
        login_window = LoginWindow()
        login_window.mainloop()
#-----------------------------------------------------------------------------------------------------------------
    def insert_stu(self):
        """添加学生成员"""
        insert_stu_window = tk.Toplevel(self)
        insert_stu_window.title("添加学生成员")
        # 设置窗口大小、居中
        width = 285
        height = 330
        screenwidth = insert_stu_window.winfo_screenwidth()
        screenheight = insert_stu_window.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        insert_stu_window.geometry(geometry)
        insert_stu_window.resizable(width=False, height=False)

        # 组件布局
        label_stuid = ttk.Label(insert_stu_window, text="学号", anchor="center", font=('SimSun', 13))
        label_stuid.place(x=29, y=23, width=69, height=30)
        entry_stuid = ttk.Entry(insert_stu_window)
        entry_stuid.place(x=110, y=23, width=150, height=30)

        label_classid = ttk.Label(insert_stu_window, text="班级", anchor="center", font=('SimSun', 13))
        label_classid.place(x=30, y=65, width=69, height=30)
        entry_classid = ttk.Entry(insert_stu_window)
        entry_classid.place(x=111, y=65, width=150, height=30)

        label_name = ttk.Label(insert_stu_window, text="姓名", anchor="center", font=('SimSun', 13))
        label_name.place(x=30, y=105, width=69, height=30)
        entry_name = ttk.Entry(insert_stu_window)
        entry_name.place(x=112, y=106, width=150, height=30)

        label_gender = ttk.Label(insert_stu_window, text="性别", anchor="center", font=('SimSun', 13))
        label_gender.place(x=29, y=144, width=69, height=30)
        entry_gender = ttk.Entry(insert_stu_window)
        entry_gender.place(x=110, y=143, width=150, height=30)

        label_phone = ttk.Label(insert_stu_window, text="电话", anchor="center", font=('SimSun', 13))
        label_phone.place(x=29, y=185, width=69, height=33)
        entry_phone = ttk.Entry(insert_stu_window)
        entry_phone.place(x=112, y=186, width=150, height=30)

        label_credit = ttk.Label(insert_stu_window, text="学分上限", anchor="center", font=('SimSun', 13))
        label_credit.place(x=29, y=234, width=74, height=33)
        entry_credit = ttk.Entry(insert_stu_window)
        entry_credit.place(x=113, y=233, width=150, height=30)

        def on_submit():
            student_id = entry_stuid.get().strip()
            class_id = entry_classid.get().strip()
            name = entry_name.get().strip()
            gender = entry_gender.get().strip()
            phone = entry_phone.get().strip()
            credit_limit = entry_credit.get().strip()
            # 简单校验
            if not (student_id and class_id and name and gender and phone and credit_limit):
                show_warning("warning", "未填写所有字段，请重新添加")
                return  
            else:
                try:
                    sql = "INSERT INTO student (student_id, class_id, name, gender, phone, credit_limit, password, cur_credit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    self.db.execute(sql, (student_id, class_id, name, gender, phone, credit_limit, "123456", 0))
                    show_info("OK", "添加成功")
                    insert_stu_window.destroy()
                except Exception as e:
                    msg = str(e)
                    if "class_id does not exist" in msg:
                        show_error("error", "班级输入有误，请重新添加")
                    else:
                        show_error("error", f"添加失败: {e}")

        btn_submit = ttk.Button(insert_stu_window, text="提交", command=on_submit)
        btn_submit.place(x=95, y=281, width=95, height=30)

    def insert_tec(self):
        """添加教师成员"""
        insert_tec_window = tk.Toplevel(self)
        insert_tec_window.title("添加教师成员")
        # 设置窗口大小、居中
        width = 280
        height = 330
        screenwidth = insert_tec_window.winfo_screenwidth()
        screenheight = insert_tec_window.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        insert_tec_window.geometry(geometry)
        insert_tec_window.resizable(width=False, height=False)

        # 编号
        label_id = ttk.Label(insert_tec_window, text="编号", anchor="center", font=('SimSun', 13))
        label_id.place(x=31, y=20, width=50, height=30)
        entry_id = ttk.Entry(insert_tec_window)
        entry_id.place(x=93, y=20, width=150, height=30)

        # 学院
        label_dep = ttk.Label(insert_tec_window, text="学院", anchor="center", font=('SimSun', 13))
        label_dep.place(x=31, y=61, width=50, height=30)
        cb_dep = ttk.Combobox(insert_tec_window, state="readonly")
        cb_dep['values'] = (
            "陈省身数学研究所",
            "数学科学学院（含组合中心）",
            "统计与数据科学学院",
            "物理科学学院",
            "化学学院",
            "生命科学学院",
            "医学院",
            "文学院",
            "日本研究院",
            "外国语学院",
            "经济学院",
            "商学院",
            "周恩来政府管理学院（专业学位专业）",
            "经济与社会发展研究院",
            "国家经济战略研究院与阿拉斯加国际合作项目",
            "电子信息与光学工程学院",
            "人工智能学院",
            "计算机学院",
            "网络空间安全学院",
            "软件学院",
            "环境科学与工程学院",
            "材料科学与工程学院",
            "药学院",
            "汉语言文化学院",
            "新闻与传播学院",
            "历史学院",
            "哲学院",
            "法学院",
            "周恩来政府管理学院（学术学位专业）",
            "马克思主义学院",
            "金融学院",
            "旅游与服务学院",
            "泰达应用物理研究院",
            "泰达生物技术研究院"
        )
        cb_dep.place(x=94, y=62, width=152, height=30)

        # 姓名
        label_name = ttk.Label(insert_tec_window, text="姓名", anchor="center", font=('SimSun', 13))
        label_name.place(x=31, y=103, width=51, height=30)
        entry_name = ttk.Entry(insert_tec_window)
        entry_name.place(x=96, y=104, width=150, height=30)

        # 职称
        label_sta = ttk.Label(insert_tec_window, text="职称", anchor="center", font=('SimSun', 13))
        label_sta.place(x=32, y=145, width=50, height=30)
        cb_sta = ttk.Combobox(insert_tec_window, state="readonly")
        cb_sta['values'] = ("教授", "讲师")
        cb_sta.place(x=96, y=145, width=150, height=30)

        # 备注
        label_add = ttk.Label(insert_tec_window, text="备注", anchor="center", font=('SimSun', 13))
        label_add.place(x=32, y=189, width=50, height=30)
        entry_add = ttk.Entry(insert_tec_window)
        entry_add.place(x=97, y=190, width=150, height=30)

        # 说明文字
        label_text1 = ttk.Label(insert_tec_window, text="“备注”：若所选职称为教授，则填写研究方向", anchor="center")
        label_text1.place(x=14, y=265, width=257, height=30)
        label_text2 = ttk.Label(insert_tec_window, text="若所选职称为讲师，则填写是否兼职", anchor="center")
        label_text2.place(x=65, y=290, width=202, height=30)

        def on_submit():
            teacher_id = entry_id.get().strip()
            department_name = cb_dep.get().strip()
            name = entry_name.get().strip()
            title = cb_sta.get().strip()
            add_value = entry_add.get().strip()
            # 校验
            if not (teacher_id and department_name and name and title and add_value):
                show_warning("warning", "未填写所有字段，请重新添加")
                return
            # 获取department_id（从1开始）
            dep_values = cb_dep['values']
            try:
                department_id = str(dep_values.index(department_name) + 1)  # 保证为字符串类型
            except ValueError:
                show_error("error", "学院选择有误")
                return
            try:
                # 插入teacher表
                sql_teacher = "INSERT INTO teacher (teacher_id, department_id, name, password) VALUES (%s, %s, %s, %s)"
                self.db.execute(sql_teacher, (teacher_id, department_id, name, "123456"))
                if title == "教授":
                    # 插入professor表
                    sql_prof = "INSERT INTO professor (teacher_id, research_area) VALUES (%s, %s)"
                    self.db.execute(sql_prof, (teacher_id, add_value))
                elif title == "讲师":
                    # 插入lecturer表
                    if add_value == "是":
                        is_part_time = 1 
                    elif add_value == "否":
                        is_part_time = 0
                    else:
                        show_error("error", "输入不合法，请重新添加")
                        return
                    sql_lect = "INSERT INTO lecturer (teacher_id, is_part_time) VALUES (%s, %s)"
                    self.db.execute(sql_lect, (teacher_id, is_part_time))
                else:
                    show_error("error", "职称选择有误")
                    return
                show_info("OK", "添加成功")
                insert_tec_window.destroy()
            except Exception as e:
                show_error("error", f"添加失败: {e}")

        btn_submit = ttk.Button(insert_tec_window, text="提交", command=on_submit)
        btn_submit.place(x=95, y=235, width=95, height=30)

    def change_stu(self):
        """修改学生成员"""
        change_stu_window = tk.Toplevel(self)
        change_stu_window.title("修改学生成员")
        # 设置窗口大小、居中
        width = 285
        height = 200
        screenwidth = change_stu_window.winfo_screenwidth()
        screenheight = change_stu_window.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        change_stu_window.geometry(geometry)
        change_stu_window.resizable(width=False, height=False)

        # 学号
        label_id = ttk.Label(change_stu_window, text="学号", anchor="center", font=('SimSun', 13))
        label_id.place(x=31, y=24, width=50, height=30)
        entry_id = ttk.Entry(change_stu_window)
        entry_id.place(x=101, y=23, width=150, height=30)

        # 修改属性
        label_change = ttk.Label(change_stu_window, text="修改属性", anchor="center", font=('SimSun', 13))
        label_change.place(x=18, y=67, width=78, height=30)
        cb_change = ttk.Combobox(change_stu_window, state="readonly")
        cb_change['values'] = ("学分上限", "班级")
        cb_change.place(x=101, y=71, width=154, height=30)

        # 修改值
        label_data = ttk.Label(change_stu_window, text="修改值", anchor="center", font=('SimSun', 13))
        label_data.place(x=27, y=113, width=55, height=30)
        entry_data = ttk.Entry(change_stu_window)
        entry_data.place(x=101, y=112, width=150, height=30)

        # 提交按钮
        def on_submit():
            student_id = entry_id.get().strip()
            change_field = cb_change.get().strip()
            change_value = entry_data.get().strip()
            if not (student_id and change_field and change_value):
                show_warning("warning", "未填写所有字段，请重新添加")
                return
            try:
                if change_field == "学分上限":
                    # 检查student_id是否存在
                    sql_check = "SELECT 1 FROM student WHERE student_id=%s"
                    result = self.db.fetchone(sql_check, (student_id,))
                    if not result:
                        show_error("error", "该学生不存在")
                        return
                    sql = "UPDATE student SET credit_limit=%s WHERE student_id=%s"
                    self.db.execute(sql, (change_value, student_id))
                elif change_field == "班级":
                    # 检查class表中是否存在该班级
                    sql_check = "SELECT 1 FROM class WHERE class_id=%s"
                    result = self.db.fetchone(sql_check, (change_value,))
                    if not result:
                        show_error("error", "班级不存在")
                        return
                    # 检查student_id是否存在
                    sql_check_stu = "SELECT 1 FROM student WHERE student_id=%s"
                    result_stu = self.db.fetchone(sql_check_stu, (student_id,))
                    if not result_stu:
                        show_error("error", "该学生不存在")
                        return
                    sql = "UPDATE student SET class_id=%s WHERE student_id=%s"
                    self.db.execute(sql, (change_value, student_id))
                else:
                    show_error("error", "请选择正确的修改属性")
                    return
                show_info("OK", "修改成功")
                change_stu_window.destroy()
            except Exception as e:
                show_error("error", f"修改失败: {e}")

        btn_submit = ttk.Button(change_stu_window, text="提交", command=on_submit)
        btn_submit.place(x=102, y=156, width=81, height=31)

    def change_tec(self):
        """修改教师成员"""
        change_tec_window = tk.Toplevel(self)
        change_tec_window.title("修改教师成员")
        # 设置窗口大小、居中
        width = 285
        height = 200
        screenwidth = change_tec_window.winfo_screenwidth()
        screenheight = change_tec_window.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        change_tec_window.geometry(geometry)
        change_tec_window.resizable(width=False, height=False)

        # 编号
        label_id = ttk.Label(change_tec_window, text="编号", anchor="center", font=('SimSun', 13))
        label_id.place(x=31, y=23, width=50, height=30)
        entry_id = ttk.Entry(change_tec_window)
        entry_id.place(x=101, y=23, width=150, height=30)

        # 修改属性
        label_change = ttk.Label(change_tec_window, text="修改属性", anchor="center", font=('SimSun', 13))
        label_change.place(x=18, y=67, width=78, height=30)
        cb_change = ttk.Combobox(change_tec_window, state="readonly")
        cb_change['values'] = ("学院", "研究方向", "是否兼职")
        cb_change.place(x=101, y=71, width=154, height=30)

        # 修改值
        label_data = ttk.Label(change_tec_window, text="修改值", anchor="center", font=('SimSun', 13))
        label_data.place(x=27, y=113, width=55, height=30)
        entry_data = ttk.Entry(change_tec_window)
        entry_data.place(x=101, y=112, width=150, height=30)

        # 提交按钮
        def on_submit():
            teacher_id = entry_id.get().strip()
            change_field = cb_change.get().strip()
            change_value = entry_data.get().strip()
            if not (teacher_id and change_field and change_value):
                show_warning("warning", "未填写所有字段，请重新添加")
                return

            # 学院映射
            dep_map = {
                "陈省身数学研究所": "1",
                "数学科学学院（含组合中心）": "2",
                "统计与数据科学学院": "3",
                "物理科学学院": "4",
                "化学学院": "5",
                "生命科学学院": "6",
                "医学院": "7",
                "文学院": "8",
                "日本研究院": "9",
                "外国语学院": "10",
                "经济学院": "11",
                "商学院": "12",
                "周恩来政府管理学院（专业学位专业）": "13",
                "经济与社会发展研究院": "14",
                "国家经济战略研究院与阿拉斯加国际合作项目": "15",
                "电子信息与光学工程学院": "16",
                "人工智能学院": "17",
                "计算机学院": "18",
                "网络空间安全学院": "19",
                "软件学院": "20",
                "环境科学与工程学院": "21",
                "材料科学与工程学院": "22",
                "药学院": "23",
                "汉语言文化学院": "24",
                "新闻与传播学院": "25",
                "历史学院": "26",
                "哲学院": "27",
                "法学院": "28",
                "周恩来政府管理学院（学术学位专业）": "29",
                "马克思主义学院": "30",
                "金融学院": "31",
                "旅游与服务学院": "32",
                "泰达应用物理研究院": "33",
                "泰达生物技术研究院": "34"
            }
            try:
                if change_field == "学院":
                    dep_id = dep_map.get(change_value)
                    if not dep_id:
                        show_error("error", "学院名称无效")
                        return
                    # 检查teacher_id是否存在
                    sql_check = "SELECT 1 FROM teacher WHERE teacher_id=%s"
                    result = self.db.fetchone(sql_check, (teacher_id,))
                    if not result:
                        show_error("error", "该教师不存在")
                        return
                    sql = "UPDATE teacher SET department_id=%s WHERE teacher_id=%s"
                    self.db.execute(sql, (dep_id, teacher_id))
                elif change_field == "研究方向":
                    # 检查professor表中是否存在teacher_id
                    sql_check = "SELECT 1 FROM professor WHERE teacher_id=%s"
                    result = self.db.fetchone(sql_check, (teacher_id,))
                    if not result:
                        show_error("error", "该教师不存在")
                        return
                    sql = "UPDATE professor SET research_area=%s WHERE teacher_id=%s"
                    self.db.execute(sql, (change_value, teacher_id))
                elif change_field == "是否兼职":
                    # 检查lecturer表中是否存在teacher_id
                    sql_check = "SELECT 1 FROM lecturer WHERE teacher_id=%s"
                    result = self.db.fetchone(sql_check, (teacher_id,))
                    if not result:
                        show_error("error", "该教师不存在")
                        return
                    if change_value == "是":
                        is_part_time = 1
                    elif change_value == "否":
                        is_part_time = 0
                    else:
                        show_error("error", "输入不合法，请重新添加")
                        return
                    sql = "UPDATE lecturer SET is_part_time=%s WHERE teacher_id=%s"
                    self.db.execute(sql, (is_part_time, teacher_id))
                else:
                    show_error("error", "请选择正确的修改属性")
                    return
                show_info("OK", "修改成功")
                change_tec_window.destroy()
            except Exception as e:
                show_error("error", f"修改失败: {e}")

        btn_submit = ttk.Button(change_tec_window, text="提交", command=on_submit)
        btn_submit.place(x=102, y=156, width=81, height=31)
#-----------------------------------------------------------------------------------------------------------------
    def class_ins(self):
        """增加课程"""
        class_ins_window = tk.Toplevel(self)
        class_ins_window.title("增加课程")
        # 设置窗口大小、居中
        width = 350
        height = 520
        screenwidth = class_ins_window.winfo_screenwidth()
        screenheight = class_ins_window.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        class_ins_window.geometry(geometry)
        class_ins_window.resizable(width=False, height=False)

        # 课程编号
        label_id = ttk.Label(class_ins_window, text="课程编号", anchor="center", font=('SimSun', 13))
        label_id.place(x=30, y=20, width=80, height=30)
        entry_id = ttk.Entry(class_ins_window)
        entry_id.place(x=130, y=20, width=180, height=30)

        # 课程名称
        label_name = ttk.Label(class_ins_window, text="课程名称", anchor="center", font=('SimSun', 13))
        label_name.place(x=30, y=65, width=80, height=30)
        entry_name = ttk.Entry(class_ins_window)
        entry_name.place(x=130, y=65, width=180, height=30)

        # 课程类型
        label_type = ttk.Label(class_ins_window, text="课程类型", anchor="center", font=('SimSun', 13))
        label_type.place(x=30, y=110, width=80, height=30)
        cb_type = ttk.Combobox(class_ins_window, state="readonly")
        cb_type['values'] = ("A", "B", "C", "D", "E")
        cb_type.place(x=130, y=110, width=180, height=30)

        # 开设院系
        label_dep = ttk.Label(class_ins_window, text="开设院系", anchor="center", font=('SimSun', 13))
        label_dep.place(x=30, y=155, width=80, height=30)
        cb_dep = ttk.Combobox(class_ins_window, state="readonly")
        cb_dep['values'] = (
            "陈省身数学研究所",
            "数学科学学院（含组合中心）",
            "统计与数据科学学院",
            "物理科学学院",
            "化学学院",
            "生命科学学院",
            "医学院",
            "文学院",
            "日本研究院",
            "外国语学院",
            "经济学院",
            "商学院",
            "周恩来政府管理学院（专业学位专业）",
            "经济与社会发展研究院",
            "国家经济战略研究院与阿拉斯加国际合作项目",
            "电子信息与光学工程学院",
            "人工智能学院",
            "计算机学院",
            "网络空间安全学院",
            "软件学院",
            "环境科学与工程学院",
            "材料科学与工程学院",
            "药学院",
            "汉语言文化学院",
            "新闻与传播学院",
            "历史学院",
            "哲学院",
            "法学院",
            "周恩来政府管理学院（学术学位专业）",
            "马克思主义学院",
            "金融学院",
            "旅游与服务学院",
            "泰达应用物理研究院",
            "泰达生物技术研究院"
        )
        cb_dep.place(x=130, y=155, width=180, height=30)

        # 学分
        label_credits = ttk.Label(class_ins_window, text="学分", anchor="center", font=('SimSun', 13))
        label_credits.place(x=30, y=200, width=80, height=30)
        entry_credits = ttk.Entry(class_ins_window)
        entry_credits.place(x=130, y=200, width=180, height=30)

        # 上课时间
        label_time = ttk.Label(class_ins_window, text="上课时间", anchor="center", font=('SimSun', 13))
        label_time.place(x=30, y=245, width=80, height=30)
        entry_time = ttk.Entry(class_ins_window)
        entry_time.place(x=130, y=245, width=180, height=30)

        # 上课地点
        label_loc = ttk.Label(class_ins_window, text="上课地点", anchor="center", font=('SimSun', 13))
        label_loc.place(x=30, y=290, width=80, height=30)
        entry_loc = ttk.Entry(class_ins_window)
        entry_loc.place(x=130, y=290, width=180, height=30)

        # 选课上限
        label_max = ttk.Label(class_ins_window, text="选课上限", anchor="center", font=('SimSun', 13))
        label_max.place(x=30, y=335, width=80, height=30)
        entry_max = ttk.Entry(class_ins_window)
        entry_max.place(x=130, y=335, width=180, height=30)

        # 授课教师1
        label_tec1 = ttk.Label(class_ins_window, text="授课教师1", anchor="center", font=('SimSun', 13))
        label_tec1.place(x=30, y=380, width=80, height=30)
        entry_tec1 = ttk.Entry(class_ins_window)
        entry_tec1.place(x=130, y=380, width=180, height=30)

        # 授课教师2(选填)
        label_tec2 = ttk.Label(class_ins_window, text="授课教师2(选填)", anchor="center", font=('SimSun', 11))
        label_tec2.place(x=12, y=425, width=120, height=30)
        entry_tec2 = ttk.Entry(class_ins_window)
        entry_tec2.place(x=130, y=425, width=180, height=30)

        # 提交按钮
        def on_submit():
            course_id = entry_id.get().strip()
            course_name = entry_name.get().strip()
            course_type = cb_type.get().strip()
            department_name = cb_dep.get().strip()
            credits = entry_credits.get().strip()
            class_time = entry_time.get().strip()
            class_location = entry_loc.get().strip()
            max_students = entry_max.get().strip()
            teacher1 = entry_tec1.get().strip()
            teacher2 = entry_tec2.get().strip()
            # 校验
            if not (course_id and course_name and course_type and department_name and credits and class_time and class_location and max_students and teacher1):
                show_warning("warning", "除授课教师2外，所有字段均需填写")
                return
            # 获取department_id
            dep_values = cb_dep['values']
            try:
                department_id = str(dep_values.index(department_name) + 1)
            except ValueError:
                show_error("error", "院系选择有误")
                return
            try:
                # 插入course表
                sql_course = "INSERT INTO course (course_id, name, type, department_id, credits, class_time, location, max_enrollment,cur_enrollment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
                self.db.execute(sql_course, (course_id, course_name, course_type, department_id, credits, class_time, class_location, max_students,0))
                # 插入teaching表
                sql_teaching = "INSERT INTO teaching (course_id, teacher_id) VALUES (%s, %s)"
                self.db.execute(sql_teaching, (course_id, teacher1))
                if teacher2:
                    self.db.execute(sql_teaching, (course_id, teacher2))
                show_info("OK", "添加课程成功")
                class_ins_window.destroy()
            except Exception as e:
                show_error("error", f"添加失败: {e}")

        btn_submit = ttk.Button(class_ins_window, text="提交", command=on_submit)
        btn_submit.place(x=130, y=475, width=90, height=32)
#-----------------------------------------------------------------------------------------------------------------
    def class_del(self):  
        """删除课程"""
        class_del_window = tk.Toplevel(self)
        class_del_window.title("删除课程")
        # 设置窗口大小、居中
        width = 285
        height = 120
        screenwidth = class_del_window.winfo_screenwidth()
        screenheight = class_del_window.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        class_del_window.geometry(geometry)
        class_del_window.resizable(width=False, height=False)

        # 课程编号
        label_id = ttk.Label(class_del_window, text="课程编号", anchor="center", font=('SimSun', 13))
        label_id.place(x=18, y=24, width=78, height=30) 
        entry_id = ttk.Entry(class_del_window)
        entry_id.place(x=101, y=23, width=150, height=30)

        # 提交按钮
        def on_submit():
            course_id = entry_id.get().strip()
            if not course_id:
                show_warning("warning", "请输入课程编号")
                return
            try:
                # 1. 检查课程是否存在
                sql_check = "SELECT credits FROM course WHERE course_id=%s"
                result = self.db.fetchone(sql_check, (course_id,))
                if not result:
                    show_error("error", "课程不存在")
                    return
                course_credit = result['credits'] if isinstance(result, dict) else result[0]

                # 开始事务
                self.db.begin()
                try:
                    # 2. 删除teaching表中的记录
                    sql_teaching = "DELETE FROM teaching WHERE course_id=%s"
                    self.db.execute(sql_teaching, (course_id,))

                    # 3. 删除enrollment表中的记录前，查找所有选了该课的学生
                    sql_enroll = "SELECT student_id FROM enrollment WHERE course_id=%s"
                    enrolled_students = self.db.fetchall(sql_enroll, (course_id,))
                    student_ids = [row['student_id'] if isinstance(row, dict) else row[0] for row in enrolled_students]

                    # 4. 删除enrollment表中的记录
                    sql_del_enroll = "DELETE FROM enrollment WHERE course_id=%s"
                    self.db.execute(sql_del_enroll, (course_id,))

                    # 5. 更新student表cur_credit
                    for stu_id in student_ids:
                        sql_update_credit = "UPDATE student SET cur_credit=cur_credit-%s WHERE student_id=%s"
                        self.db.execute(sql_update_credit, (course_credit, stu_id))

                    # 6. 删除course表中的记录
                    sql_del_course = "DELETE FROM course WHERE course_id=%s"
                    self.db.execute(sql_del_course, (course_id,))

                    self.db.commit()
                    show_info("OK", "删除成功")
                    class_del_window.destroy()
                except Exception as e:
                    self.db.rollback()
                    show_error("error", f"删除失败: {e}")
            except Exception as e:
                show_error("error", f"操作失败: {e}")

        btn_submit = ttk.Button(class_del_window, text="提交", command=on_submit)
        btn_submit.place(x=102, y=70, width=81, height=31)


    def class_cha(self):
        """修改课程"""
        class_cha_window = tk.Toplevel(self)
        class_cha_window.title("修改课程")
        # 设置窗口大小、居中
        width = 285
        height = 235
        screenwidth = class_cha_window.winfo_screenwidth()
        screenheight = class_cha_window.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        class_cha_window.geometry(geometry)
        class_cha_window.resizable(width=False, height=False)

        # 课程编号
        label_id = ttk.Label(class_cha_window, text="课程编号", anchor="center" , font=('SimSun', 13))
        label_id.place(x=18, y=29, width=78, height=30)
        entry_id = ttk.Entry(class_cha_window)
        entry_id.place(x=101, y=29, width=150, height=30)

        # 修改属性
        label_attr = ttk.Label(class_cha_window, text="修改属性", anchor="center"  , font=('SimSun', 13))
        label_attr.place(x=18, y=80, width=78, height=30)
        cb_attr = ttk.Combobox(class_cha_window, state="readonly")
        cb_attr['values'] = ("上课时间", "上课地点", "选课上限")
        cb_attr.place(x=101, y=81, width=150, height=31)

        # 修改值
        label_data = ttk.Label(class_cha_window, text="修改值", anchor="center", font=('SimSun', 13))
        label_data.place(x=20, y=135, width=68, height=30)
        entry_data = ttk.Entry(class_cha_window)
        entry_data.place(x=101, y=135, width=150, height=30)

        # 提交按钮
        def on_submit():
            course_id = entry_id.get().strip()
            change_field = cb_attr.get().strip()
            change_value = entry_data.get().strip()
            if not (course_id and change_field and change_value):
                show_warning("warning", "未填写所有字段，请重新添加")
                return
            # 字段映射
            field_map = {
                "上课时间": "class_time",
                "上课地点": "location",
                "选课上限": "max_enrollment"
            }
            db_field = field_map.get(change_field)
            if not db_field:
                show_error("error", "请选择正确的修改属性")
                return
            try:
                # 检查课程是否存在
                sql_check = "SELECT 1 FROM course WHERE course_id=%s"
                result = self.db.fetchone(sql_check, (course_id,))
                if not result:
                    show_error("error", "课程不存在")
                    return
                sql = f"UPDATE course SET {db_field}=%s WHERE course_id=%s"
                self.db.execute(sql, (change_value, course_id))
                show_info("OK", "修改成功")
                class_cha_window.destroy()
            except Exception as e:
                show_error("error", f"修改失败: {e}")

        btn_submit = ttk.Button(class_cha_window, text="提交", command=on_submit)
        btn_submit.place(x=102, y=185, width=81, height=31)
#-----------------------------------------------------------------------------------------------------------------
    def _create_widgets(self):
        # 退出登录按钮
        self.btn_exit = ttk.Button(self, text="退出登录", takefocus=False,command=self.quit)
        self.btn_exit.place(x=0, y=0, width=227, height=30)
        # 数据表
        columns = {"ID":94,"字段#1": 141,"字段#2":235}
        self.table = ttk.Treeview(self, show="headings", columns=list(columns))
        for text, width in columns.items():
            self.table.heading(text, text=text, anchor='center')
            self.table.column(text, anchor='center', width=width, stretch=False)
        self.table.place(x=228, y=31, width=471, height=467)
        # 其它标签和控件
        self.label_hello = ttk.Label(self, text="您好！", anchor="center", font=('SimSun', 20))
        self.label_hello.place(x=79, y=66, width=80, height=40)
        self.label_admin = ttk.Label(self, text="管理员 ：", anchor="center", font=('SimSun', 15))
        self.label_admin.place(x=29, y=151, width=80, height=30)
        self.label_id = ttk.Label(self, text=self.account, anchor="center",font=('SimSun', 15))
        self.label_id.place(x=130, y=151, width=80, height=30)
#-----------------------------------------------------------------------------------------------------------------
        self.label_insert = ttk.Label(self, text="添加成员", anchor="center", font=('SimSun', 11))
        self.label_insert.place(x=10, y=252, width=70, height=30)
        self.label_change = ttk.Label(self, text="修改属性", anchor="center", font=('SimSun', 11))
        self.label_change.place(x=9, y=327, width=70, height=30)
        self.label_class = ttk.Label(self, text="管理课程", anchor="center", font=('SimSun', 11))
        self.label_class.place(x=9, y=409, width=70, height=30)

        self.cb_insert_table = ttk.Combobox(self, state="readonly", values=("学生","教师"))
        self.cb_insert_table.place(x=97, y=252, width=111, height=30)
        # 默认按钮，初始command设为空
        self.btn_insert = ttk.Button(self, text="选择添加", takefocus=False, command=lambda: None)
        self.btn_insert.place(x=74, y=290, width=68, height=30)
        # 绑定选择事件
        self.cb_insert_table.bind("<<ComboboxSelected>>", self._on_insert_identity_changed)

        self.cb_change_table = ttk.Combobox(self, state="readonly", values=("学生","教师"))
        self.cb_change_table.place(x=98, y=327, width=111, height=30)
        # 默认按钮，初始command设为空
        self.btn_change = ttk.Button(self, text="选择修改", takefocus=False, command=lambda: None)
        self.btn_change.place(x=74, y=365, width=68, height=30)
        # 绑定选择事件
        self.cb_change_table.bind("<<ComboboxSelected>>", self._on_change_identity_changed)


        self.cb_class_table = ttk.Combobox(self, state="readonly", values=("增加","删除","修改"))
        self.cb_class_table.place(x=98, y=409, width=111, height=30)
        # 默认按钮，初始command设为空
        self.btn_class = ttk.Button(self, text="选择管理", takefocus=False, command=lambda: None)
        self.btn_class.place(x=74, y=450, width=68, height=30)
        # 绑定选择事件
        self.cb_class_table.bind("<<ComboboxSelected>>", self._on_class_choice_changed)
#-----------------------------------------------------------------------------------------------------------------
        self.label_obj = ttk.Label(self, text="查询对象", anchor="center")
        self.label_obj.place(x=240, y=0, width=62, height=30)
        self.cb_obj_table = ttk.Combobox(self, state="readonly", values=("学生","教师","课程"))
        self.cb_obj_table.place(x=320, y=0, width=280, height=32)
        self.btn_submit = ttk.Button(self, text="提交", takefocus=False, command=self._on_submit)
        self.btn_submit.place(x=610, y=0, width=67, height=30)
        # 滚动条相关方法
        self._setup_scrollbars()

    def _setup_scrollbars(self):
        # 只为table添加垂直和水平滚动条
        vbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        hbar = ttk.Scrollbar(self, orient="horizontal", command=self.table.xview)
        self.table.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)
        vbar.place(relx=(471 + 228) / 700, rely=31 / 500, relheight=467 / 500, anchor='ne')
        hbar.place(relx=228 / 700, rely=(31 + 467) / 500, relwidth=471 / 700, anchor='sw')
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

    def _on_insert_identity_changed(self, event):
        identity = self.cb_insert_table.get()
        if identity == "学生":
            self.btn_insert.config(command=self.insert_stu)
        elif identity == "教师":
            self.btn_insert.config(command=self.insert_tec)
        else:
            self.btn_insert.config(command=lambda: None)

    def _on_change_identity_changed(self, event):
        identity = self.cb_change_table.get()
        if identity == "学生":
            self.btn_change.config(command=self.change_stu)
        elif identity == "教师":
            self.btn_change.config(command=self.change_tec)
        else:
            self.btn_change.config(command=lambda: None)

    def _on_class_choice_changed(self, event):
        choice = self.cb_class_table.get()
        if choice == "增加":
            self.btn_class.config(command=self.class_ins)
        elif choice == "删除":
            self.btn_class.config(command=self.class_del)
        elif choice == "修改":
            self.btn_class.config(command=self.class_cha)
        else:
            self.btn_class.config(command=lambda: None)
#-----------------------------------------------------------------------------------------------------------------
    def _on_submit(self):
        """提交按钮事件，根据下拉框选择更新表格结构和内容"""
        obj = self.cb_obj_table.get()
        self._update_table(obj)

    def _update_table(self, obj):
        """根据选择的对象更新表格结构和内容"""
        # 清空原有表格
        for col in self.table["columns"]:
            self.table.heading(col, text="")
            self.table.column(col, width=0)
        self.table.delete(*self.table.get_children())

        # 查询数据库视图
        view_map = {
            "学生": "stu_all",
            "教师": "tec_all",
            "课程": "course_all"
        }
        if obj in view_map:
            try:
                sql = f"SELECT * FROM {view_map[obj]}"
                rows = self.db.fetchall(sql)
                if not rows:
                    return
                # 获取字段名
                columns = rows[0].keys() if hasattr(rows[0], "keys") else [desc[0] for desc in self.db.cursor.description]
                # 重新设置表头
                self.table["columns"] = list(columns)
                for col in columns:
                    self.table.heading(col, text=col, anchor='center')
                    self.table.column(col, anchor='center', width=100, stretch=False)
                # 插入数据
                for row in rows:
                    values = list(row.values()) if hasattr(row, "values") else list(row)
                    self.table.insert("", "end", values=values)
            except Exception as e:
                show_error("error", f"查询失败: {e}")
        else:
            columns = {"ID": 94, "字段#1": 141, "字段#2":235}
            data = []
            self.table["columns"] = list(columns)
            for text, width in columns.items():
                self.table.heading(text, text=text, anchor='center')
                self.table.column(text, anchor='center', width=width, stretch=False)
            for row in data:
                self.table.insert("", "end", values=row)

