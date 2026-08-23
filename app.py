from flask import Flask,render_template,request,redirect,session,url_for
import random,json,os,my_cryptography
import code_constructor as cc
import functions as funt

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# @app.errorhandler(Exception)
# def handle_all_errors(e):
#    return render_template('error.html')

def log_check():
    if "user_id" not in session or "role" not in session or"name" not in session or 'ip' not in session:
        return False
    else:
        if session['role'] != 'ADMIN':
            conn,cursor = funt.Functions().data_base_function()
            cursor.execute('SELECT SECRET_ID FROM SINGLE_LOG WHERE USER_TYPE = ? AND USER_ID = ?',(session['role'],session['user_id']))
            user_secret_id = int(cursor.fetchone()[0])
            funt.Functions().data_base_function(conn)
            if user_secret_id != int(session['secret_id']):
                return redirect(url_for('logout'))
        return True

@app.route("/", methods=["GET","POST"])
def welcome_page():
    if request.method == "POST":
        log_type = request.form.get('LOG_TYPE')
        U_N = request.form.get('USER_NAME')
        PWD = request.form.get('PWD')
        if funt.LOGIN().check_pwd(log_type, U_N, PWD):
            conn,cursor = funt.Data().data_base_function()
            if log_type == 'STUDENT':
                cursor.execute('SELECT Name FROM STUDENT_DATA WHERE Adm_ID = ?', (U_N,))
                row = cursor.fetchone()
            elif log_type == "TEACHER":
                cursor.execute('SELECT Name FROM TEACHER_DATA WHERE ID = ?', (U_N,))
                row = cursor.fetchone()
            else:
                row = ('ADMIN',)
            ip = request.form.get('ip_address')
            user_secret_id = int(random.randint(10000,99999))
            session["user_id"] = U_N
            session["role"] = log_type
            session["name"] = row
            session['ip'] = ip
            session['secret_id'] = user_secret_id
            if session['role'] != 'ADMIN':
                cursor.execute('UPDATE SINGLE_LOG SET SECRET_ID = ? WHERE USER_TYPE = ? AND USER_ID = ?',(user_secret_id,log_type,U_N))#########
                cursor.execute('SELECT HISTORY FROM LOG_HISTORY WHERE USER_ID = ? AND USER_TYPE = ?',(U_N,log_type))
                his = cursor.fetchone()[0]
                d,t = funt.Functions().get_date_time()
                his += f';{ip.replace(',','').replace(';','')},{str(d).replace(',','').replace(';','')},{str(t).replace(',','').replace(';','')}'
                cursor.execute('UPDATE LOG_HISTORY SET HISTORY= ? WHERE USER_ID = ? AND USER_TYPE = ?',(his,U_N,log_type))
            cursor.execute('SELECT * FROM BLOCK_USER WHERE USER_ID = ? AND USER_TYPE = ?',(U_N,log_type))
            if cursor.fetchone() is not None:
                funt.Data().data_base_function()
                return render_template("index.html",error="""<div class="warning">USER NAME IS BLOCKED BY APP ADMIN.!!! FOR ANY ISSUE CONTACT <a style="text-decoration:none;" href="https://wa.me/9897432207" target="_blank">+919897432207</a> OR <a style="text-decoration:none;" href="https://wa.me/8273998585" target="_blank">+918273998585</a>.</div>""")
            funt.Data().data_base_function(conn)
            return redirect(url_for('dashboard'))
        return render_template("index.html",error="""<div class="warning">EITHER USER NAME OR PASSWORD IS WRONG!!!</div>""")
    return render_template("index.html")

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if log_check():
        conn,cursor = funt.Data().data_base_function()
        if session["role"] == "STUDENT":
            cursor.execute('SELECT Name,Father,Mother,Class,DOB,Address,MOBILE FROM STUDENT_DATA WHERE Adm_ID = ?',(session['user_id'],))
            Name,Father,Mother,Class,DOB,Address,MOBILE = cursor.fetchone()
            funt.Data().data_base_function(conn)
            return render_template("student/dashboard.html",info=f'''NAME:- <font>{Name.upper()}</font><br>FATHER NAME:- <font>{Father.upper()}</font><br>MOTHER NAME:- <font>{Mother.upper()}</font><br>CLASS :- <font>{Class}</font><br>ADDRESS :- <font>{Address.upper()}</font><br>D.O.B. :- <font>{DOB.upper()}</font><br>MOBILE NO.:- <font>{MOBILE}</font>''')
        elif session["role"] == "TEACHER":
            cursor.execute('SELECT Name,Father,Mother,Mobile FROM TEACHER_DATA WHERE ID = ?',(session['user_id'],))
            Name,Father,Mother,Mobile = cursor.fetchone()
            funt.Data().data_base_function(conn)
            return render_template("teacher/dashboard.html",info=f'''NAME:- <font>{Name.upper()}</font><br>FATHER NAME:-<font>{Father.upper()}</font><br>MOTHER NAME:-<font>{Mother.upper()}</font><br>MOBILE NO.:-<font>{Mobile}</font>''')
        elif session["role"] == "ADMIN":
            funt.Data().data_base_function(conn)
            return render_template("admin/dashboard.html")
    else:
        return redirect(url_for("welcome_page"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('welcome_page'))

@app.route('/confirmation',methods=['GET'])
def confirmation():
    if log_check():
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('welcome_page'))
    
@app.route('/notifications')
def noti_view():
    if log_check():
        return render_template('notifications.html',code=cc.Notifications().notifications_creater())
    else:
        return redirect(url_for('welcome_page'))

@app.route('/videos')
def videos():
    if log_check():
        return render_template('videos.html',code=cc.Videos_Sender().videos_creater())
    else:
        return redirect(url_for('welcome_page'))

@app.route("/report_card",methods=["GET","POST"])
def report_card():
    if log_check():
        if session["role"] == "STUDENT":
            return render_template("student/functions/report_card.html",code=cc.Report_card().view_report_card(session['user_id']))
        
        elif session["role"] == "TEACHER":
            if request.method == "POST":
                conn,cursor = funt.Data().data_base_function()
                c_class = request.form.get('c_class')
                re_type = request.form.get('stage')
                if re_type == "st1":
                    funt.Data().data_base_function(conn)
                    return render_template("teacher/functions/report_card.html",code=cc.Report_card().select_st(c_class))
                st_id = request.form.get('st_del')
                if re_type == "st2":
                    funt.Data().data_base_function(conn)
                    return render_template("teacher/functions/report_card.html",code=cc.Report_card().select_st(c_class),code2=cc.Report_card().teach_st(int(re_type[-1]) -1,st_id,c_class))
                data = ''
                for i in range(cc.content_creator().subject_list(c_class)):
                    var = (f't{i+1}_1',f't{i+1}_2',f't{i+1}_3',f't{i+1}_4')
                    data += f'{request.form.get(var[0])},{request.form.get(var[1])},{request.form.get(var[2])},{request.form.get(var[3])};'
                data = data[:-1]
                
                if re_type == "st3":
                    cursor.execute('UPDATE EXAM_DATA SET TERM_1 = ? WHERE Adm_ID = ?',(data,st_id))
                    funt.Data().data_base_function(conn)
                    return render_template("teacher/functions/report_card.html",code=cc.Report_card().select_st(c_class),code2=cc.Report_card().teach_st(int(re_type[-1]) -1,st_id,c_class)) 
                cursor.execute('UPDATE EXAM_DATA SET TERM_2 = ? WHERE Adm_ID = ?',(data,st_id))
                funt.Data().data_base_function(conn)
                return render_template("teacher/functions/report_card.html")
            return render_template("teacher/functions/report_card.html")
        
        elif session["role"] == "ADMIN":
            if request.method == "POST":
                c_class = request.form.get('c_class')
                re_type = request.form.get('stage')
                if re_type == "st1":
                    return render_template("admin/functions/report_card.html",code=cc.Report_card().select_st(c_class))
                elif re_type == "st2":
                    st_id = request.form.get('st_del')
                    return render_template("admin/functions/report_card.html",code=cc.Report_card().select_st(c_class),code2=cc.Report_card().view_report_card(st_id))
            return render_template("admin/functions/report_card.html")
        else:
            return redirect(url_for('welcome_page'))
    else:
        return redirect(url_for('welcome_page'))

@app.route('/change_pwd',methods=["GET","POST"])
def change_pwd():
    if log_check():
        if session['role'] == "STUDENT" or session['role'] == "TEACHER":
            if request.method == "POST":
                if funt.Functions().change_pwd(user_id=session['user_id'],user_type=session['role'],pwd=request.form.get('con_pwd')):
                    return render_template('change_pwd.html',error='PASSWORD CHANGED SUCCESSFULLY.')
                else:
                    return render_template('change_pwd.html',error='PASSWORD NOT CHANGED.')
            return render_template('change_pwd.html')
        elif session['role'] == "ADMIN":
            if request.method == "POST":
                if funt.Functions().change_pwd(request.form.get('ID'),request.form.get('user_type'),request.form.get('con_pwd')):
                    return render_template('admin/functions/change_pwd.html',error='PASSWORD CHANGED SUCCESSFULLY.')
                else:
                    return render_template('admin/functions/change_pwd.html',error='PASSWORD NOT CHANGED.')
            return render_template('admin/functions/change_pwd.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/time_table',methods=["GET","POST"])
def time_table():
    if log_check():
        conn,cursor = funt.Data().data_base_function()
        if session['role'] == "STUDENT":
            cursor.execute('SELECT Class FROM STUDENT_DATA WHERE Adm_ID = ?',(session['user_id'],))
            c_class = str(cursor.fetchone()[0])
            funt.Data().data_base_function(conn)
            return render_template('time_table.html',code=cc.Online_classes().table_code(c_class))
        elif session['role'] == "TEACHER":
            if request.method == "POST":
                return render_template('teacher/functions/time_table.html',code=cc.Online_classes().table_code(request.form.get('st_class')))
            return render_template('teacher/functions/time_table.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/complains',methods=["GET","POST"])
def complains():
    if log_check():
        if session['role'] == "STUDENT" or session['role'] == "TEACHER":
            if request.method == "POST":
                d,t = funt.Functions().get_date_time()
                conn,cursor = funt.Data().data_base_function()
                cursor.execute('INSERT INTO COMPLAINS VALUES(?,?,?,?,?)',(session['user_id'],session['role'],request.form.get('complain'),d,t))
                funt.Data().data_base_function(conn)
                return render_template('complain.html',comment='<b><label>COMPLAIN SENDED SUCCESSFULLY.</b></label>',code='''<form action="/complains" method="post">
        <textarea id="nor_input" rows="5" placeholder="ENTER YOUR COMPLAIN........." name="complain" required></textarea>
        <button id="nor_btn">SUBMIT</button></form>''')
            return render_template('complain.html',code='''<form action="/complains" method="post">
        <textarea id="nor_input" rows="5" placeholder="ENTER YOUR COMPLAIN........." name="complain" required></textarea>
        <button id="nor_btn">SUBMIT</button></form>''')
        elif session['role'] == 'ADMIN':
            return render_template('complain.html',code=cc.Complains().admin_complain_code())
    else:
        return redirect(url_for('welcome_page'))

#STUDENT
@app.route('/homework')
def homework_view():
    if log_check():
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT CLASS FROM STUDENT_DATA WHERE Adm_ID = ?',(session['user_id'],))
        st_class = cursor.fetchone()[0]
        funt.Data().data_base_function(conn)
        return render_template("student/functions/hw.html",code=cc.Homework().hw_creator(st_class))
    else:
        return redirect(url_for('welcome_page'))

@app.route('/student_online_classes',methods=['GET',"POST"])
def student_online_classes():
    if log_check():
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT Class FROM STUDENT_DATA WHERE Adm_ID = ?;',(session['user_id'],))
        st_class = cursor.fetchone()[0]
        funt.Data().data_base_function(conn)
        return render_template('student/functions/online_classes.html',code=cc.Online_classes().student_code_online(st_class,funt.Functions().get_day()))
    else:
        return redirect(url_for('welcome_page'))

@app.route('/attandance',methods=["GET","POST"])
def st_attandance():
    if log_check():
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT Class FROM STUDENT_DATA WHERE Adm_ID = ?;',(session['user_id'],))
        st_class = cursor.fetchone()[0]
        funt.Data().data_base_function(conn)
        if request.method == "POST":
            return render_template('student/functions/attandance.html',subj_opt=cc.Attandance().subject_opt(st_class),attandance_list=cc.Attandance().load_student_attandance(session['user_id'],request.form.get('month'),request.form.get('subject')))
        return render_template('student/functions/attandance.html',subj_opt=cc.Attandance().subject_opt(st_class))
    else:
        return redirect(url_for('welcome_page'))

@app.route('/class_tests',methods=["GET","POST"])
def student_class_test():
    if log_check():
        st_id = session['user_id']
        return render_template('student/functions/tests.html',code=cc.Tests().test_manual_student(st_id))
    else:
        return redirect(url_for('welcome_page'))

@app.route('/class_tests/testpaper',methods=["GET","POST"])
def testpaper():
    if log_check():
        test_id = request.form.get('test_id')
        return render_template('student/functions/testpaper.html',code=cc.Tests().generate_test_code(test_id))
    else:
        return redirect(url_for('welcome_page'))

@app.route('/class_tests/testpaper/test_submittion',methods=["POST","GET"])
def test_submittion():
    if log_check():
        conn,cursor = funt.Data().data_base_function()
        test_id = request.form.get('test_id')
        li = request.form.to_dict(flat=True)
        li.pop('test_id')
        ans = ''
        for ques,item in li.items():
            ans+=f'{ques.replace('ans?=','').replace('?next?=/','').strip()}ans?={item.replace('ans?=','').replace('?next?=/','').strip()}?next?=/'
        ans = ans[:-8]
        cursor.execute('INSERT INTO STUDENT_TEST_DATA VALUES(?,?,?,?)',(test_id,int(session['user_id']),ans,''))
        funt.Data().data_base_function(conn)
        return render_template('confirmation.html')
    else:
        return redirect(url_for('welcome_page'))

#TEACHER
@app.route('/test_generator',methods=["GET"])
def test_generator():
    if log_check():
        return render_template('teacher/functions/test_generator.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/test_generator/test_del',methods=["GET","POST"])
def test_del():
    if log_check():
        testdata = request.form.get("TEST_DATA_INPUT")
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT TEST_ID FROM TEST_DATA;')
        test_id_list = []
        for row in cursor.fetchall():
            test_id_list.append(row[0])
        funt.Data().data_base_function(conn)
        while True:
            test_id = random.randint(100000000000000,999999999999999)
            if test_id not in test_id_list:
                break
        return render_template('teacher/functions/test_del.html',code=testdata,test_id=test_id)
    else:
        return redirect(url_for('welcome_page'))
    
@app.route("/test_generator/test_del/test_sending_confirmation",methods=["POST","GET"])
def test_data_storage():
    if log_check():
        conn,cursor = funt.Data().data_base_function()
        time = f'{str(request.form.get("test_time")).strip()}:00'
        cursor.execute("INSERT INTO TEST_DATA(TEST_ID,DATA,DATE,TIME,SUBJECT,CLASS,TOTAL_MARKS,T_ID) VALUES(?,?,?,?,?,?,?,?)",
        (request.form.get("test_id"),request.form.get("TEST_DATA_INPUT"),request.form.get("test_date"),time,request.form.get('test_subject'),request.form.get('test_class'),request.form.get('marks'),session['user_id']))
        funt.Data().data_base_function(conn)
        return render_template('confirmation.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/student_test_data',methods=["GET","POST"])
def student_test_data():
    if log_check():
        if request.form.get('stage') == "st1":
            return render_template('teacher/functions/test_data.html',opt_code=cc.Tests().test_ids_teacher(int(session['user_id']),request.form.get('c_class')))
        if request.form.get('stage') == "st2":
            return render_template('teacher/functions/test_data.html',code=cc.Tests().teacher_test_checker(request.form.get('test_id')))
        if request.form.get('stage') == 'st3':
            conn,cursor = funt.Data().data_base_function()
            data_dic = request.form.to_dict(flat=True)
            data_dic.pop('stage')
            for student,item in data_dic.items():
                Adm_ID = int(student.split('marks_')[1])
                cursor.execute('UPDATE STUDENT_TEST_DATA SET OBTAIN_MARKS = ? WHERE Adm_ID = ?',(int(item),Adm_ID))
            funt.Data().data_base_function(conn)
            return render_template('confirmation.html')
        return render_template('teacher/functions/test_data.html')
    else:
        return redirect(url_for('welcome_page'))


@app.route('/homework_sender',methods=["GET","POST"])
def teacher_hw_sender():
    if log_check():
        if request.method == 'POST':
            conn,cursor = funt.Data().data_base_function()
            HW_ID_LIST = []
            cursor.execute('SELECT HW_ID FROM HW_DATA;')
            for row in cursor.fetchall():
                HW_ID_LIST.append(row[0])
            while True:
                hw_id = random.randint(100000000000000,999999999999999)
                if hw_id not in HW_ID_LIST:
                    break
            hw_file= request.files['hw_file']
            if hw_file:
                path = f'static/homework_file/{hw_id}.pdf'
                hw_file.save(path)
            else:
                path = None
            cursor.execute('INSERT INTO HW_DATA(HW_ID,HW_CLASS,HW_TEXT,HW_FILE_PATH,HW_DATE,HW_TIME,T_ID) VALUES(?,?,?,?,?,?,?)',
            (hw_id,request.form.get('hw_class'),request.form.get('hw_text'),path,request.form.get('hw_date'),request.form.get('hw_time'),session['user_id'])) 
            funt.Data().data_base_function(conn)
            return render_template('confirmation.html')
        return render_template('teacher/functions/hw_sender.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/attandance',methods=["POST","GET"]) 
def st_attendance_teacher():
    if log_check():
        if request.method == "POST":
            conn,cursor = funt.Data().data_base_function()
            re_type = request.form.get('stage')
            c_class = request.form.get('st_class')
            if re_type == "st1":
                funt.Data().data_base_function()
                return render_template('teacher/functions/attandance.html',code=cc.Attandance().load_sub(c_class))
            sub =  request.form.get('subject')
            if re_type == "st2":
                funt.Data().data_base_function()
                return render_template('teacher/functions/attandance.html',code2=cc.Attandance().load_attandance_teacher(c_class,sub))
            date,_ = funt.Functions().get_date_time()
            if re_type == "st3":
                cursor.execute('SELECT Adm_ID FROM STUDENT_DATA WHERE Class = ?',(c_class,))
                at_data  = cursor.fetchall()
                date,_ = funt.Functions().get_date_time()
                for item in at_data:
                    cursor.execute('SELECT Status FROM ATTANDANCE WHERE Adm_ID = ? AND Date = ? AND Subject = ?',(item[0],date,sub))
                    stat = cursor.fetchone()
                    if stat is None:
                        cursor.execute('INSERT INTO ATTANDANCE VALUES(?,?,?,?)',(item[0],date,sub,request.form.get(str(item[0]))))
                    else:
                        cursor.execute('UPDATE ATTANDANCE SET Status = ? WHERE Adm_ID = ? AND Date = ? AND Subject = ?',(request.form.get(str(item[0])),item[0],date,sub))
                funt.Data().data_base_function(conn)
                return render_template('teacher/functions/attandance.html')
        return render_template('teacher/functions/attandance.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/online_classes_teacher',methods=["GET","POST"])
def online_classes_teacher():
    if log_check():
        return render_template('teacher/functions/online_classes.html',code=cc.Online_classes().table_code(teacher_entity=True))
    else:
        return redirect(url_for('welcome_page'))

#ADMIN
@app.route('/command_box',methods=["GET","POST"])
def command_box():
    if log_check():
        if request.method == "POST":
            if 'universal_admin' not in session:
                if str(request.form.get('pin')).strip() == my_cryptography.log_pin_decypt('gAAAAABqVkB7NZlVRW0g-LsW2GP7XACyePFv4GAqN-tN4rZccW-ZNb9bVPjET06Gb8f7o2UjP_VxrretZpszQEbzJjO0IczrR-PKLxlA3r-tMf-uArCdKbg='):
                    session['universal_admin'] = True
                    return render_template('admin/functions/command_box.html')
                else:
                    session['universal_admin'] = False
            elif session['universal_admin']:
                output,error = funt.Functions().command_box(str(request.form.get('command')).strip())
                return render_template('admin/functions/command_box.html',output=output,error=error)
            else:
                return redirect(url_for('dashboard'))
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('welcome_page'))

@app.route('/noti_sender',methods=['GET','POST'])
def noti_sender():
    if log_check():
        if request.method == "POST":
            d,t = funt.Functions().get_date_time()
            conn,cursor = funt.Functions().data_base_function()
            capt = request.form.get('noti').strip().replace('<---ENTER--->','<br>').upper()
            cursor.execute('INSERT INTO MEDIA_DATA(MEDIA_TYPE,DATE,TIME,CAPTION) VALUES(?,?,?,?)',('NOTIFICATION',d,str(t).strip()[:-3],capt))
            funt.Functions().data_base_function(conn)
            return render_template('confirmation.html')
        return render_template('admin/functions/notification_sender.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/admin_video_sender',methods=["GET","POST"])
def admin_video_sender():
    if log_check():
        if request.method == "POST":
            conn,cursor = funt.Functions().data_base_function()
            capt = request.form.get('caption')
            video_ = request.files['video']
            if video_.content_type != 'video/mp4':
                return render_template('admin/functions/videos_sender.html',status='FILE IS NOT IN MP4!!!',caption=capt)
            video_.seek(0,2)
            size = video_.tell()
            video_.seek(0)
            if size > 1024 * 1024 * 10: #10MB
                return render_template('admin/functions/videos_sender.html',status='FILE IS LARGER THAN 10MB!!!',caption=capt)
            d,t = funt.Functions().get_date_time()
            cursor.execute('INSERT INTO MEDIA_DATA VALUES(?,?,?,?,?)',('VIDEO',d,str(t).strip()[:-3],capt,video_))
            funt.Functions().data_base_function(conn)
            return render_template('confirmation.html')
        return render_template('admin/functions/videos_sender.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/add_student',methods=["GET","POST"])
def add_student():
    if log_check():
        if request.method == "POST":
            conn,cursor = funt.Data().data_base_function()
            ST_ID = int(request.form.get('st_adm'))
            ST_NAME = request.form.get('st_name')
            ST_FATHER = request.form.get('st_ft_name')
            ST_MOTHER = request.form.get('st_mt_name')
            ST_CLASS = request.form.get('st_class')
            ST_DOB = request.form.get('st_dob')
            ST_ADDRESS = request.form.get('st_add')
            ST_MOBILE = int(request.form.get('st_mob'))
            ST_ADHAAR = int(request.form.get('st_adhaar'))
            ST_PEN = int(request.form.get('st_pen'))
            r_pwd = request.form.get('st_pwd')
            ST_PWD = funt.Functions().crt_pwd(r_pwd)
            ST_DATA_LI1 = []
            ST_DATA_LI2 = []
            ST_DATA_LI3 = []
            cursor.execute('SELECT Adm_ID,Adhaar,PEN FROM STUDENT_DATA;')
            for row in cursor.fetchall():
                ST_DATA_LI1.append(row[0])
                ST_DATA_LI2.append(row[1])
                ST_DATA_LI3.append(row[2])
            if ST_ID in ST_DATA_LI1:
                return render_template('admin/functions/add_st.html',error="STUDENT ID ALREADY TAKEN. (ENTER ANOTHER ADMISSION NO.)!!!",
                e1=ST_NAME,e2=ST_FATHER,e3=ST_MOTHER,e4=ST_CLASS,e5=ST_DOB,e6=ST_ADDRESS,e7=ST_MOBILE,e8=ST_ADHAAR,e9=ST_PEN,e11=r_pwd)
            if ST_ADHAAR in ST_DATA_LI2:
                return render_template('admin/functions/add_st.html',error="STUDENT ADHAAR ALREADY REGISTERED!!!",
                e1=ST_NAME,e2=ST_FATHER,e3=ST_MOTHER,e4=ST_CLASS,e5=ST_DOB,e6=ST_ADDRESS,e7=ST_MOBILE,e9=ST_PEN,e10=ST_ID,e11=r_pwd)
            if ST_PEN in ST_DATA_LI3:
                return render_template('admin/functions/add_st.html',error="STUDENT PEN IS ALREADY REGISTERED!!!",
                e1=ST_NAME,e2=ST_FATHER,e3=ST_MOTHER,e4=ST_CLASS,e5=ST_DOB,e6=ST_ADDRESS,e7=ST_MOBILE,e8=ST_ADHAAR,e10=ST_ID,e11=r_pwd)
            cursor.execute('INSERT INTO STUDENT_DATA(Adm_ID,Name,Father,Mother,CLASS,DOB,Address,MOBILE,Adhaar,PEN) VALUES(?,?,?,?,?,?,?,?,?,?);',
            (ST_ID,ST_NAME,ST_FATHER,ST_MOTHER,ST_CLASS,ST_DOB,ST_ADDRESS,ST_MOBILE,ST_ADHAAR,ST_PEN))
            cursor.execute('INSERT INTO PASSWORDS(LOG_TYPE,USER_ID,PASSWORD) VALUES(?,?,?)',('STUDENT',ST_ID,ST_PWD))
            val = ''
            for item in cc.content_creator().subject_list(ST_CLASS):
                val += ',,,;'
            val = val[:-1]
            cursor.execute('INSERT INTO EXAM_DATA VALUES(?,?,?)',(ST_ID,val,val))
            d,t = funt.Functions().get_date_time()
            cursor.execute('INSERT INTO LOG_HISTORY VALUES(?,?,?)',(ST_ID,'STUDENT',f'CREATED,{d},{t}'))
            cursor.execute('INSERT INTO SINGLE_LOG VALUES(?,?,?)',('STUDENT',ST_ID,0))
            funt.Data().data_base_function(conn)
            return render_template('confirmation.html')
        return render_template('admin/functions/add_st.html')
    else:
        return redirect(url_for('welcome_page'))
    
@app.route('/add_teacher',methods=["GET","POST"])
def add_teacher():
    if log_check():
        if request.method == "POST":
            conn,cursor = funt.Data().data_base_function()
            T_ID_ = int(request.form.get('T_ID'))
            T_NAME = request.form.get('T_name')
            T_FATHER = request.form.get('T_ft_name')
            T_MOTHER = request.form.get('T_mt_name')
            T_DOB = request.form.get('T_dob')
            T_ADDRESS = request.form.get('T_add')
            T_MOBILE = request.form.get('T_mob')
            T_ADHAAR = request.form.get('T_adhaar')
            r_pwd = request.form.get('T_pwd')
            T_PWD = funt.Functions().crt_pwd(r_pwd)
            cursor.execute("SELECT ID,Adhaar FROM TEACHER_DATA;")
            T_DATA_LI1 = []
            T_DATA_LI2 = []
            for row in cursor.fetchall():
                T_DATA_LI1.append(row[0])
                T_DATA_LI2.append(str(row[1]))
            if T_ID_ in T_DATA_LI1:
                return render_template('admin/functions/add_t.html',error="TEACHER ID ALREADY TAKEN!!!",
                e1=T_NAME,e2=T_FATHER,e3=T_MOTHER,e4=T_ADDRESS,e5=T_DOB,e6=T_ADHAAR,e8=r_pwd,e9=T_MOBILE)
            if T_ADHAAR in T_DATA_LI2:
                return render_template('admin/functions/add_t.html',error="TEACHER ADHAAR IS ALREADY REGISTERED!!!"
                ,e1=T_NAME,e2=T_FATHER,e3=T_MOTHER,e4=T_ADDRESS,e5=T_DOB,e7=T_ID_,e8=r_pwd,e9=T_MOBILE)
            cursor.execute('INSERT INTO TEACHER_DATA(ID,Name,Father,Mother,DOB,Address,MOBILE,Adhaar) VALUES(?,?,?,?,?,?,?,?);',
            (T_ID_,T_NAME,T_FATHER,T_MOTHER,T_DOB,T_ADDRESS,T_MOBILE,T_ADHAAR))
            cursor.execute('INSERT INTO PASSWORDS(LOG_TYPE,USER_ID,PASSWORD) VALUES(?,?,?);',("TEACHER",T_ID_,T_PWD))
            d,t = funt.Functions().get_date_time()
            cursor.execute('INSERT INTO LOG_HISTORY VALUES(?,?,?)',(T_ID_,'TEACHER',f'CREATED,{d},{t}'))
            cursor.execute('INSERT INTO SINGLE_LOG VALUES(?,?,?)',('TEACHER',T_ID_,0))
            funt.Data().data_base_function(conn)
            return render_template('confirmation.html')
        return render_template('admin/functions/add_t.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route("/student_manual",methods=["GET","POST"])
def student_manual():
    if log_check():
        if request.method == "POST":
            conn,cursor = funt.Data().data_base_function()
            if request.form.get('action_type') == "EDIT":
                st_id = int(request.form.get('st_id'))
                st_name = request.form.get('st_name')
                st_father = request.form.get('st_father')
                st_mother = request.form.get('st_mother')
                st_dob = request.form.get('st_dob')
                st_mob = request.form.get('st_mob')
                st_add = request.form.get('st_add')
                cursor.execute('UPDATE STUDENT_DATA SET Name=?,Father=?,Mother=?,DOB=?,MOBILE=?,Address=? WHERE Adm_ID = ?',
                (st_name,st_father,st_mother,st_dob,st_mob,st_add,st_id))
                
            elif request.form.get('action_type') == "DELETE":
                dest_id = int(request.form.get('dest_id'))
                cursor.execute('DELETE FROM STUDENT_DATA WHERE Adm_ID = ?',(dest_id,))
                cursor.execute('DELETE FROM PASSWORDS WHERE LOG_TYPE = "STUDENT" AND USER_ID = ?',(dest_id,))
                cursor.execute('DELETE FROM BLOCK_USER WHERE USER_ID = ? AND USER_TYPE = "STUDENT";',(dest_id,))
                cursor.execute('DELETE FROM EXAM_DATA WHERE Adm_ID = ?',(dest_id,))
                cursor.execute('DELETE FROM LOG_HISTORY WHERE USER_TYPE = "STUDENT" AND USER_ID = ?',(dest_id,))
                cursor.execute('DELETE FROM SINGLE_LOG WHERE USER_TYPE = "STUDENT" AND USER_ID = ?',(dest_id,))

            funt.Data().data_base_function(conn)
        return render_template('admin/functions/st_del.html',code=cc.Details_Page().students())
    else:
        return redirect(url_for('welcome_page'))

@app.route("/teacher_manual",methods=["GET","POST"])
def teacher_manual():
    if log_check():
        if request.method == "POST":
            conn,cursor = funt.Data().data_base_function()
            if request.form.get('action_type') == "EDIT":
                t_id = int(request.form.get('t_id'))
                t_name = request.form.get('t_name')
                t_father = request.form.get('t_father')
                t_mother = request.form.get('t_mother')
                t_dob = request.form.get('t_dob')
                t_mob = request.form.get('t_mob')
                t_add = request.form.get('t_add')
                cursor.execute('UPDATE TEACHER_DATA SET Name=?,Father=?,Mother=?,DOB=?,MOBILE=?,Address=? WHERE ID = ?',
                (t_name,t_father,t_mother,t_dob,t_mob,t_add,t_id))

            elif request.form.get('action_type') == "DELETE":
                det_id = int(request.form.get('det_id'))
                cursor.execute('DELETE FROM TEACHER_DATA WHERE ID = ?',(det_id,))
                cursor.execute('DELETE FROM PASSWORDS WHERE LOG_TYPE = "TEACHER" AND USER_ID = ?',(det_id,))
                cursor.execute('DELETE FROM BLOCK_USER WHERE USER_ID = ? AND USER_TYPE = "TEACHER";',(det_id,))
                cursor.execute('DELETE FROM SINGLE_LOG WHERE USER_TYPE = ? AND USER_ID = ?',('TEACHER',det_id))

            funt.Data().data_base_function(conn)
        return render_template('admin/functions/t_del.html',code=cc.Details_Page().teachers())
    else:
        return redirect(url_for('welcome_page'))

@app.route('/online_class_manager',methods=["GET","POST"])
def online_class_manager():
    if log_check():
        if request.method == "POST":
            re_type = request.form.get('stage')
            c_class = request.form.get('class')
            if re_type == "st1":
                return render_template('admin/functions/online_class_manager.html',code=cc.Online_classes().admin_code_online(c_class,0))
            else:
                li = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY']
                i = int(request.form.get('i'))
                conn,cursor = funt.Data().data_base_function()
                da = f'{str(request.form.get('d1_1')).strip()},{str(request.form.get('d1_2')).strip()},{str(request.form.get('d1_3')).strip()};'
                da += f'{str(request.form.get('d2_1')).strip()},{str(request.form.get('d2_2')).strip()},{str(request.form.get('d2_3')).strip()};'
                da += f'{str(request.form.get('d3_1')).strip()},{str(request.form.get('d3_2')).strip()},{str(request.form.get('d3_3')).strip()};'
                da += f'{str(request.form.get('d4_1')).strip()},{str(request.form.get('d4_2')).strip()},{str(request.form.get('d4_3')).strip()};'
                da += f'{str(request.form.get('d5_1')).strip()},{str(request.form.get('d5_2')).strip()},{str(request.form.get('d5_3')).strip()};'
                da += f'{str(request.form.get('d6_1')).strip()},{str(request.form.get('d6_2')).strip()},{str(request.form.get('d6_3')).strip()};'
                da += f'{str(request.form.get('d7_1')).strip()},{str(request.form.get('d7_2')).strip()},{str(request.form.get('d7_3')).strip()};'
                da += f'{str(request.form.get('d8_1')).strip()},{str(request.form.get('d8_2')).strip()},{str(request.form.get('d8_3')).strip()}'
                cursor.execute(f'UPDATE ONLINE_CLASSES_DATA SET {li[i-1]} = ? WHERE CLASS = ?',(da,c_class))
                funt.Data().data_base_function(conn)
                if i <= 5:
                    return render_template('admin/functions/online_class_manager.html',code=cc.Online_classes().admin_code_online(c_class,i))
                else:
                    return render_template('confirmation.html')
        return render_template('admin/functions/online_class_manager.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/export_data',methods=["GET","POST"])
def export_data():
    if log_check():
        if request.method == "POST":
            exp_type = request.form.get('btn_type')
            if exp_type == "1":
                funt.Export().student_data()
                return render_template('admin/functions/export_data.html',
                code=f'''<a href="{url_for('static',filename='files/STUDENT_DETAILS.pdf')}" download><button id="nor_btn">DOWNLOAD <i class="fa fa-download"></i></button></a>''')
            elif exp_type == "2":
                funt.Export().student_pwd()
                return render_template('admin/functions/export_data.html',
                code=f'''<a href="{url_for('static',filename='files/STUDENT_PASSWORDS.pdf')}" download><button id="nor_btn">DOWNLOAD <i class="fa fa-download"></i></button></a>''')
            elif exp_type == "3":
                funt.Export().teacher_data()
                return render_template('admin/functions/export_data.html',
                code=f'''<a href="{url_for('static',filename='files/TEACHER_DETAILS.pdf')}" download><button id="nor_btn">DOWNLOAD <i class="fa fa-download"></i></button></a>''')
            elif exp_type == "4":
                funt.Export().teacher_pwd()
                return render_template('admin/functions/export_data.html',
                code=f'''<a href="{url_for('static',filename='files/TEACHER_PASSWORDS.pdf')}" download><button id="nor_btn">DOWNLOAD <i class="fa fa-download"></i></button></a>''')
        return render_template('admin/functions/export_data.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/fees_slip',methods=["GET","POST"])
def fees_slip():
    if log_check():
        if request.method == "POST":
            conn,cursor = funt.Data().data_base_function()
            re_type = request.form.get('stage')
            st_id = request.form.get('st_id')
            cursor.execute('SELECT Name,Father,Mother,Class FROM STUDENT_DATA WHERE Adm_ID = ?;',(st_id,))
            row = cursor.fetchone()
            if row is None:
                return render_template('admin/functions/fees_slip.html',error="ID NOT FOUND!!!")
            st_name,st_father,st_mother,st_class = row
            cursor.execute('SELECT REST FROM FEES_DATA WHERE Adm_ID = ?',(st_id,))
            if cursor.fetchone() is None:
                fees = funt.Data().class_fees(st_class)
            else:
                cursor.execute('SELECT REST FROM FEES_DATA WHERE Adm_ID = ?',(st_id,))
                for row in cursor.fetchall():
                    fees = row[0]

            if re_type == "st1":
                if fees == 0:
                    return render_template('admin/functions/fees_slip.html',code="NO FEES LEFT IN THIS SESSION!!!")
                else:
                    code=f'''<input type="text" name="stage" value="st2" hidden>
                    <input type="number" name="st_id" value="{st_id}" hidden>
                    <b>ENTER FEE AMOUNT <label>*</label> [LEFT FEES ({fees})]</b>
                    <input type="number" name="fees_amount" id="nor_input" min="1" max="{fees}" placeholder="ENTER FEES AMOUNT" required>
                    <button id="nor_btn">SAVE DATA</button>'''
                funt.Data().data_base_function(conn)
                return render_template('admin/functions/fees_slip.html',
                code=code,st_id=st_id,st_name=st_name,st_father=st_father,st_mother=st_mother,st_class=st_class)
            
            elif re_type == "st2":
                with open('datasync.json',"r") as f:
                    sync_data = json.load(f)
                sync_data_list = [int(item) for item in sync_data.keys() if item.isdigit()]
                fees_session = max(sync_data_list)
                fees_amount = int(request.form.get('fees_amount'))
                cursor.execute('SELECT FEES_ID FROM FEES_DATA ORDER BY FEES_ID DESC;')
                FEES_ID_LI = []
                for item in cursor.fetchall():
                    d = item[0]
                    if d != 0:
                        FEES_ID_LI.append(int(d))
                FEES_ID = max(FEES_ID_LI)
                cursor.execute('INSERT INTO FEES_DATA(FEES_ID,Adm_id,CURRENT_DEPOSIT,REST,SESSION) VALUES(?,?,?,?);',(FEES_ID,st_id,fees_amount,fees-fees_amount,fees_session))
                funt.Export().fees_slip_export(st_id,fees_amount,fees-fees_amount)
                code2=f'''<a href="{url_for('static',filename='files/FEES_SLIP.pdf')}" download><button id="nor_btn">DOWNLOAD FEES RECIEPT <i class="fa fa-download"></i></button></a>'''
                funt.Data().data_base_function(conn)
                return render_template('admin/functions/fees_slip.html',
                code="DATA SAVED SUCCESFULLY!!!",code2=code2,st_id=st_id,st_name=st_name,st_father=st_father,st_mother=st_mother,st_class=st_class)
        return render_template('admin/functions/fees_slip.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/block_user',methods=["GET","POST"])
def block_user():
    if log_check():
        if request.method == "POST":
            conn,cursor = funt.Data().data_base_function()
            user_type = request.form.get('user_type')
            user_id = int(request.form.get('ID'))
            if user_type == "STUDENT":
                cursor.execute('SELECT Name FROM STUDENT_DATA WHERE Adm_ID = ?;',(user_id,))
            else:
                cursor.execute('SELECT Name FROM TEACHER_DATA WHERE ID = ?;',(user_id,))
            if cursor.fetchone() is None:
                return render_template('admin/functions/block_user.html',code="USER NOT FOUND[]")
            
            d,t = funt.Functions().get_date_time()
            action_type = request.form.get('action_type')
            cursor.execute('SELECT * FROM BLOCK_USER WHERE USER_ID = ? AND USER_TYPE = ?',(user_id,user_type))
            if action_type == "BLOCK":
                if cursor.fetchone() is None:
                    cursor.execute('INSERT INTO BLOCK_USER(USER_ID,USER_TYPE,DATE,TIME) VALUES(?,?,?,?);',(user_id,user_type,d,t))
                else:
                    funt.Data().data_base_function(conn)
                    return render_template('admin/functions/block_user.html',code="USER ALREADY BLOCK[]")
            else:
                if cursor.fetchone() is not None:
                    cursor.execute('DELETE FROM BLOCK_USER WHERE USER_ID = ? AND USER_TYPE = ?',(user_id,user_type))
                else:
                    funt.Data().data_base_function(conn)
                    return render_template('admin/functions/block_user.html',code="USER NOT BLOCK[]")
            funt.Data().data_base_function(conn)
            return render_template('admin/functions/block_user.html',code="DATA SAVED SUCCESSFULLLY")
        return render_template('admin/functions/block_user.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/user_log_history',methods=["GET","POST"])
def user_log_history():
    if log_check():
        if request.method == "POST":
            return render_template('admin/functions/user_log_history.html',code=cc.Log_History().user_log_history(request.form.get('USER_ID'),request.form.get('USER_TYPE')))
        return render_template('admin/functions/user_log_history.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/special_log',methods=["GET","POST"])
def special_log_function():
    if log_check():
        if request.method == "POST":
            conn,cursor = funt.Data().data_base_function()
            log_type = request.form.get('type').upper()
            ID = int(request.form.get('ID'))
            if log_type == "STUDENT":
                cursor.execute('SELECT Adm_ID FROM STUDENT_DATA;')
                li = []
                for i in cursor.fetchall():
                    li.append(int(i[0]))
                conn.close()
                if ID in li:
                    session["user_id"] = ID
                    session["role"] = 'STUDENT'
                    session["name"] = '[[SAMLPE SPACE]][200]'
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('admin/functions/special_log.html',code='STUDENT ADMISSION NUMBER IS WRONG.')
            else:
                cursor.execute('SELECT ID FROM TEACHER_DATA;')
                li = []
                for i in cursor.fetchall():
                    li.append(int(i[0]))
                funt.Data().data_base_function(conn)
                if ID in li:
                    session["user_id"] = ID
                    session["role"] = 'TEACHER'
                    session["name"] = '[[SAMLPE SPACE]][200]'
                    return redirect(url_for('dashboard'))
                else:
                    return render_template('admin/functions/special_log.html',code='TEACHER ID IS WRONG.')
        return render_template('admin/functions/special_log.html')
    else:
        return redirect(url_for('welcome_page'))

@app.route('/sync_db_new_session',methods=["GET","POST"])
def sync_db_new_session():
    if log_check():    
        if request.method == "POST":
            return render_template('admin/functions/sync_db_new_session.html',code=funt.Data_sync().data_sync(request.form.to_dict(flat=True)))
        d,_ = funt.Functions().get_date_time()
        my_date = str(d).strip()[:-3]
        with open('datasync.json','r') as f:
            data_sync = json.load(f)
        if str(funt.Functions().date_show_mon(int(my_date[:4]))) not in data_sync:
            if my_date[5:] == '04' or my_date[5:] == '05':
                return render_template('admin/functions/sync_db_new_session.html',code=cc.Data_Sync().data_sync())
            else:
                return render_template('admin/functions/sync_db_new_session.html',code='<h2>DATABASE SYNC PERIOD IS EXPIRED.</h2>')
        return render_template('admin/functions/sync_db_new_session.html',code=funt.Data_sync().data_sync_status_funt())
    else:
        return redirect(url_for('welcome_page'))

if __name__== "__main__":
    app.run(debug=True)

