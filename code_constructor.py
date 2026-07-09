import functions as funt

class content_creator:
    def __init__(self):
        super().__init__()
    def subject_list(self,st_class):
        c_type_dic = {"type1":"HINDI<E.V.S.<COMPUTER<ENGLISH<G.K.<MATHS<ART","type2":"HINDI<G.K.<E.V.S.<MATHS<SANSKRIT<ENGLISH<COMPUTER<ART",
        "type3":"MATHS<SANSKRIT<COMPUTER<ENGLISH<E.V.S.<G.K.<HINDI<ART","type4":"ENGLISH<G.K.<SANSKRIT<S.ST<MATHS<HINDI<SCIENCE<COMPUTER"}
        classes_dic = {"1":"type1","2":"type2","3":"type2","4":"type3","5":"type3","6":"type4","7":"type4","8":"type4"}
        return c_type_dic[classes_dic[st_class]].split('<')

class Complains(content_creator): 
    def admin_complain_code(self):
        html_text = ''
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT * FROM COMPLAINS;')
        li =  cursor.fetchall()
        funt.Data().data_base_function(conn)
        if len(li) <= 0:
            return '<h2>NO COMPLAIN YET.</h2>'
        if len(li) > 1:
            li.reverse()
        for item in li:
            user,user_type,complain,d,t = item
            html_text += f'<div id="notifi"><div id="noti_heading">USER ID :- {user}, USER TYPE :- {user_type}, DATE/TIME :- {d},{t}</div><b>COMPLAIN :- </b>{complain}</div>'
        return html_text + '\n<label><code><b>NOTE - </b>THESE COMPLAINS CONNOT WE DELETED.</code></label>'
    
class Tests(content_creator):
    #test content
    def option_field(self, da, num):
        html = f'<div id="TEST_CONTENT"><p>{da[0]}'
        html += f'<select id="nor_input" name="answer{num}">'
        html += '<option value="">---SELECT---</option>'
        li = da[1:]
        for i in range(len(li) - 1):
            html += f'<option value="{li[i]}">{li[i]}</option>'
        opt_mar = li[len(li)-1].split('<---MARKS--->')
        html += f'<option value="{opt_mar[0]}">{opt_mar[0]}</option>'
        html += f'</select><div class="MARKS"><b>MARK: {opt_mar[1]}</b></p></div></div><br>'
        return html

    def input_field(self, da, num):
        opt_mar = da[1].split('<---MARKS--->')
        return f'<div id="TEST_CONTENT"><p>{da[0]}<input id="nor_input" type="text" name="answer{num}" placeholder="ENTER YOUR ANSWER">{opt_mar[0]}<div class="MARKS"><b>MARK: {opt_mar[1]}</b></p></div></div><br>'

    def long_field(self, da, num):
        opt_mar = da[1].split('<---MARKS--->')
        return f'<div id="TEST_CONTENT"><p>{da[0]}<textarea rows="5" id="nor_input" name="answer{num}" placeholder="ENTER YOUR ANSWER"</textarea>{opt_mar[0]}<div class="MARKS"><b>MARK: {opt_mar[1]}</b></p></div></div><br>'
    #test
    def generate_test_code(self,test_id):
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT * FROM TEST_DATA WHERE TEST_ID = ?',(test_id,))
        test_id,question_data,d,t1,sub,cls,marks,teach_id = cursor.fetchone()
        cursor.execute('SELECT ID,Name FROM TEACHER_DATA')
        teach_dic =  dict(cursor.fetchall())
        def teach_name(teach_id,teach_dic=teach_dic):
            try:
                if not teach_id:
                    t_name = ''
                else:
                    t_name = teach_dic[teach_id]
            except:
                t_name = '[UNDEFINED]'
            return t_name
        t2 = funt.Functions().change_time(min=30,Time=str(t1))
        html_text = f'''<form id="myForm" action="test_submittion" method="POST"><div id="noti_heading"><h3>TEST ID :- {test_id}<br>TEACHER NAME :- {teach_name(teach_id)}<br>CLASS :- {cls}<br>SUBJECT :- {sub}<br>MARKS :- {marks}</h3><h3 style="margin:0px 0px;padding:0px 0px;color:white;" id="demo{test_id}"></h3></div></fieldset><fieldset>
<input name="test_id" value="{test_id}" hidden><script>
var x'''+f'''{test_id}'''+''' = setInterval(function() {
var distance'''+f'''{test_id}'''+''' = new Date("'''+f'''{d} {t2}'''+'''").getTime() - new Date().getTime();
var days'''+f'''{test_id}'''+''' = Math.floor(distance'''+f'''{test_id}'''+''' / (1000 * 60 * 60 * 24));
var hours'''+f'''{test_id}'''+''' = Math.floor((distance'''+f'''{test_id}'''+''' % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
var minutes'''+f'''{test_id}'''+''' = Math.floor((distance'''+f'''{test_id}'''+''' % (1000 * 60 * 60)) / (1000 * 60));
var seconds'''+f'''{test_id}'''+''' = Math.floor((distance'''+f'''{test_id}'''+''' % (1000 * 60)) / 1000);
document.getElementById("demo'''+f'''{test_id}'''+'''").innerHTML = days'''+f'''{test_id}'''+''' + "d " + hours'''+f'''{test_id}'''+''' + "h "+ minutes'''+f'''{test_id}'''+''' + "m " + seconds'''+f'''{test_id}'''+''' + "s ";
if (distance'''+f'''{test_id}'''+''' < 0) {
let form = document.getElementById("myForm");
form.submit();}}, 1000);
</script>'''
        funt.Data().data_base_function(conn)
        if '<---' not in question_data and '--->' not in question_data:
            return "Invalid format"
        if '<---NEXT_QUES--->' in question_data:
            question_data_list = question_data.split('<---NEXT_QUES--->')
        else:
            question_data_list = [question_data]
        for no, item in enumerate(question_data_list, start=1):
            item = item.strip()
            if '<---OPTION--->' in item:
                parts = item.split('<---OPTION--->')
                html_text += self.option_field(parts, no)
            elif '<---INPUT_FIELD--->' in item:
                parts = item.split('<---INPUT_FIELD--->')
                html_text += self.input_field(parts, no)
            elif '<---LONG_FIELD--->' in item:
                parts = item.split('<---LONG_FIELD--->')
                html_text += self.long_field(parts, no)
            else:
                html_text += f"<p>Invalid Question Format: {item}</p>"
        html_text += '''<button id="nor_btn" type="submit"">Submit</button></form>'''
        return html_text

    def test_manual_student(self,st_id):
        html_text = ''
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT ID,Name FROM TEACHER_DATA')
        teach_dic =  dict(cursor.fetchall())
        def teach_name(teach_id,teach_dic=teach_dic):
            try:
                if not teach_id:
                    t_name = ''
                else:
                    t_name = teach_dic[teach_id]
            except:
                t_name = '[UNDEFINED]'
            return t_name
        cursor.execute('SELECT Class FROM STUDENT_DATA WHERE Adm_ID = ?',(st_id,))
        st_class = cursor.fetchone()[0]
        cursor.execute('SELECT TEST_ID FROM TEST_DATA WHERE CLASS = ?',(st_class,))
        data = cursor.fetchall()
        for row in data:
            cursor.execute('SELECT * FROM TEST_DATA WHERE TEST_ID = ?',(int(row[0]),))
            test_id,_,d,t1,sub,_,_,teach = cursor.fetchone()
            t2 = funt.Functions().change_time(Time=t1,min=30)
            html_text += '''<div id="notifi"><div id="noti_heading">'''+f'''DATE/TIME :- {d} , {t1} , SUBJECT :- {sub}<br>TEACHER NAME:- {teach_name(teach)}</div>'''
            cursor.execute('SELECT Adm_ID FROM STUDENT_TEST_DATA WHERE TEST_ID = ?',(test_id,))
            li = cursor.fetchall()
            if (int(st_id),) in li:
                html_text += '''<h2>TEST ATTEMPTED</h2><code><b>MARKS :- '''
                cursor.execute('SELECT TOTAL_MARKS FROM TEST_DATA WHERE TEST_ID = ?',(int(row[0]),))
                marks = cursor.fetchone()[0]
                cursor.execute('SELECT OBTAIN_MARKS FROM STUDENT_TEST_DATA WHERE TEST_ID = ? AND Adm_ID = ?',(int(row[0]),st_id))
                d = cursor.fetchone()
                if d is not None:
                    html_text+=str(d[0])
                html_text+=f'/{marks}</b></code></div>'
            else:
                html_text += '''<form action="testpaper" method="post"><input type="number" name="test_id" value="'''+f'''{test_id}'''+'''" hidden><button style="color: rgb(0, 0, 0);background: rgb(187, 210, 11);border-radius:50px;border: 3px solid rgb(0, 0, 0);width: 98%;margin:10px 10px;padding: 12px 20px;display: none;" id="testbtn'''+f'''{test_id}'''+'''">START TEST</button>
<h2 id="'''+f'''demo{test_id}'''+'''"></h2>
<script>
var x'''+f'''{test_id}'''+''' = setInterval(function() {
var distance'''+f'''{test_id}'''+''' = new Date("'''+f'''{d} {t1}'''+'''").getTime() - new Date().getTime();
var days'''+f'''{test_id}'''+''' = Math.floor(distance'''+f'''{test_id}'''+''' / (1000 * 60 * 60 * 24));
var hours'''+f'''{test_id}'''+''' = Math.floor((distance'''+f'''{test_id}'''+''' % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
var minutes'''+f'''{test_id}'''+''' = Math.floor((distance'''+f'''{test_id}'''+''' % (1000 * 60 * 60)) / (1000 * 60));
var seconds'''+f'''{test_id}'''+''' = Math.floor((distance'''+f'''{test_id}'''+''' % (1000 * 60)) / 1000);
document.getElementById("demo'''+f'''{test_id}'''+'''").innerHTML = days'''+f'''{test_id}'''+''' + "d " + hours'''+f'''{test_id}'''+''' + "h "+ minutes'''+f'''{test_id}'''+''' + "m " + seconds'''+f'''{test_id}'''+''' + "s ";
if (distance'''+f'''{test_id}'''+''' < 0) {
clearInterval(x'''+f'''{test_id}'''+''');
document.getElementById('demo'''+f'''{test_id}').innerHTML = "";
document.getElementById("'''+f'''testbtn{test_id}'''+'''").style.display = "inline-block";}}, 1000);
//2 stage
var ex'''+f'''{test_id}'''+''' = setInterval(function() {
if (new Date("'''+f'''{d} {t2}'''+'''").getTime() - new Date().getTime() < 0) {
clearInterval(ex'''+f'''{test_id}'''+''');
document.getElementById('demo'''+f'''{test_id}'''+'''').innerHTML = "TEST ENDED";
document.getElementById("'''+f'''testbtn{test_id}'''+'''").style.display = "none";}}, 1000);
</script></form></div>'''
        funt.Data().data_base_function(conn)
        return html_text

    def teacher_test_checker(self,test_id):
        html_text = '<input name="stage" value="st3" hidden><table border="3"><tr><th>ADM. ID.</th>'
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT TOTAL_MARKS,DATA FROM TEST_DATA WHERE TEST_ID = ?',(test_id,))
        t_marks = int(cursor.fetchone()[0])
        cursor.execute('SELECT Adm_ID,ANSWERS FROM STUDENT_TEST_DATA WHERE TEST_ID = ?',(test_id,))
        data = cursor.fetchall()
        if data[0][1] is None:
            return '<h2>TEST DATA ALREADY SAVED!!!</h2>'
        for item in data[0][1].split('?next?=/'):
            html_text += f'<th>{item.split('ans?=')[0]}</th>'
        html_text += f"<th>TOTAL MARKS [{t_marks}]</th></tr>"
        for item in data:
            html_text +=f'<tr><th>{item[0]}</th>'
            for i in item[1].split('?next?=/'):
                html_text += f'<th>{i.split('ans?=')[1]}</th>'
            html_text += f'<th><input type="number" name="marks_{item[0]}" min="0" max="{t_marks}" required></th></tr>'
        funt.Data().data_base_function(conn)
        return html_text + '</table><button id="nor_btn">SAVE DATA</button>'

    def test_ids_teacher(self,t_id,c_class):
        html_text='<b>SELECT [TEST ID, CLASS, DATE/TIME, SUBJECT] <label>*</label></b><select id="nor_opt" name="test_id" required><option value="">---SELECT---</option>'
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT TEST_ID,DATE,TIME,SUBJECT,CLASS FROM TEST_DATA WHERE T_ID = ? AND CLASS = ?',(t_id,c_class))
        for item in cursor.fetchall():
            html_text +=f'<option value="{int(item[0])}">{int(item[0])} --> {item[4]} -->{item[1]},{item[2]} --> {item[3]}</option>'
        funt.Data().data_base_function(conn)
        return html_text + '</select><button id="nor_btn">LOAD TEST DATA</button>'
    
class Videos_Sender(content_creator):
    def videos_creater(self,initial_html_list,path,caption,vid_date,vid_time):
        html_text = ''
        conn,cursor = funt.Functions().data_base_function()
        cursor.execute('')
        for item in cursor.fetchall():
            html_text += f''
        funt.Functions().data_base_function(conn)
        return html_text
    #     return f'{initial_html_list[0]}<!--- ADD ALL THE HTML CONTENT HERE --->\n<div id="notifi"><div id="noti_heading">{vid_date},{vid_time}<div style="float: right;"><i class="fa fa-play"></i></div></div><video width="100%" src="{path}" controls></video>{caption}</div>{initial_html_list[1]}'

class Notifications(content_creator):
    def notifications_creater(self):
        html_text = ''
        conn,cursor = funt.Functions().data_base_function()
        cursor.execute('SELECT DATE,TIME,CAPTION FROM MEDIA_DATA WHERE MEDIA_TYPE = "NOTIFICATION";')
        data = cursor.fetchall()
        data.reverse()
        for item in data:
            DATE,TIME,CAPTION = item
            html_text += f'<div id="notifi"><div id="noti_heading">DATE/TIME:- {DATE},{TIME}<div style="float: right;"><i class="fa fa-bell"></i></div></div><b>{CAPTION}</b></div>'
        funt.Functions().data_base_function(conn)
        return html_text

class Homework(content_creator):
    def hw_code(self,st_class):
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT HW_TEXT,HW_FILE_PATH,HW_DATE,HW_TIME,T_ID FROM HW_DATA WHERE HW_CLASS = ?;',(st_class,))
        html_text = '<fieldset><h1>HOMEWORK</h1>'
        for row in cursor.fetchall():
            text,file,date,time,t_id = row
            cursor.execute('SELECT Name FROM TEACHER_DATA WHERE ID = ?',(t_id,))
            t_name = cursor.fetchone()[0]
            html_text += f'<div id="notifi"><div id="noti_heading"><b>{date},{time}<br>TEACHER:- {t_name}</b><div style="float: right;"><i class="fa fa-book"></i></div></div><b>{text}</b>'
            if file != None:
                html_text += f'<br><a href="{file}" target="_blank"><button id="hw_btn">VIEW HOMEWORK  <i class="fa fa-file"></i></button></a>'
            html_text += '</div>\n'
        html_text += '</fieldset>'
        funt.Data().data_base_function(conn)
        return html_text

class Details_Page(content_creator):
    def __init__(self):
        super().__init__()

    def students(self):
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT Adm_ID,Name,Father,Mother,DOB,Mobile,Address,Class FROM STUDENT_DATA;')
        html_text = ''
        for row in cursor.fetchall():
            st_id,name,father,mother,dob,mobile,add,cls = row
            html_text += f"""<div id="notifi">
    <div id="del_div"><b>
    CLASS:- {cls}<br>
    ADM. NO:- {st_id}<br>
    <hr>
    NAME:- {name}<br>
    FATHER:- {father}<br>
    MOTHER:- {mother}<br>
    D.O.B.:- {dob}<br>
    MOBILE:- {mobile}<br>
    ADDRESS:- {add}<br></b>
    <button onclick="run1('{st_id}','{name}','{father}','{mother}','{dob}','{mobile}','{add}')" style="width:auto;">EDIT STUDENT DETAILS</button>
    <button onclick="run2('{st_id}','{name}','{father}','{mother}','{dob}','{mobile}','{add}')" style="width:auto;">DELETE STUDENT</button>
    </div>
</div>"""
        funt.Data().data_base_function(conn)
        return html_text
    
    def teachers(self):
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT ID,Name,Father,Mother,DOB,Mobile,Address FROM TEACHER_DATA;')
        html_text = ''
        for row in cursor.fetchall():
            id,name,father,mother,dob,mobile,add = row
            html_text += f"""<div id="notifi">
    <div id="del_div"><b>
    TEACHER'S ID:- {id}<br>
    <hr>
    NAME:- {name}<br>
    FATHER:- {father}<br>
    MOTHER:- {mother}<br>
    D.O.B.:- {dob}<br>
    MOBILE:- {mobile}<br>
    ADDRESS:- {add}<br></b>
    <button onclick="run1('{id}','{name}','{father}','{mother}','{dob}','{mobile}','{add}')" style="width:auto;">EDIT TEACHER DETAILS</button>
    <button onclick="run2('{id}','{name}','{father}','{mother}','{dob}','{mobile}','{add}')" style="width:auto;">DELETE TEACHER</button>
    </div>
</div>"""
        funt.Data().data_base_function(conn)
        return html_text

class Online_classes(content_creator):
    def __init__(self):
        super().__init__()

    def admin_code_online(self,c_class,i):
        conn,cursor = funt.Data().data_base_function()
        time = ["09:00a.m. - 09:30a.m.","09:30a.m. - 10:00a.m.","10:00a.m. - 10:30a.m.","10:30a.m. - 11:00a.m.","11:00a.m. - 11:30a.m.","11:30a.m. - 12:00a.m.","12:00a.m. - 12:30a.m.","12:30a.m. - 01:00p.m."]
        li = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY']
        html_text = f'<input type="text" name="class" value="{c_class}" hidden>\n<input type="number" name="i" value="{i + 1}" hidden><h1>CLASS :- {c_class}</h1>'
        html_text += f'<table border="3"><tr><th>TIME</th><th>{li[i]}</th></tr>'
        cursor.execute(f'SELECT {li[i]} FROM ONLINE_CLASSES_DATA WHERE CLASS = ?',(c_class,))
        data = cursor.fetchone()
        if data is None:
            for i in range(1,9):
                html_text += f"""<tr><th>{time[i-1]}</th><td>SUBJECT<br><input type="text" value="" name="d{i}_1"><br>TEACHER ID<br><input type="number" value="" name="d{i}_2"><br>MEET ID<br><input type="text" value="" name="d{i}_3"></td></tr>"""
        else:
            for r in range(len(str(data[0].split(';')))):
                d1,d2,d3 = tuple(data[r].split(','))
                html_text += f"""<tr><th>{time[r]}</th><td>SUBJECT<br><input type="text" value="{d1.strip()}" name="d{r+1}_1"><br>TEACHER ID<br><input type="number" value="{d2.strip()}" name="d{r+1}_2"><br>MEET ID<br><input type="text" value="{d3.strip()}" name="d{r+1}_3"></td></tr>"""
        html_text += """<tr><th colspan="2"><i><b><u>NOTE:-</u></b></i>  FOR NULL TYPE(NO SCHEDULE) LEAVE FIELD BLANK.</th></tr></table>"""
        funt.Data().data_base_function(conn)
        if i < 5:
            html_text += f'''<button id="nor_btn" onclick="alert('YOUR DATA OF {li[i]} UPDATED SUCCESSFULLY!!!!')"> NEXT --> <b>[{li[i+1]}]</b></button>'''
        else:
            html_text += '<button type="submit" id="nor_btn"> UPDATE </button>'
        return html_text
    
    def student_code_online(self,st_class,day):
        html_text = ''
        if day.upper() == "SUNDAY":
            return "<h2>TODAY IS SUNDAY !!!</h2>"
        conn,cursor = funt.Data().data_base_function()
        time = ["09:00a.m. - 09:30a.m.","09:30a.m. - 10:00a.m.","10:00a.m. - 10:30a.m.","10:30a.m. - 11:00a.m.","11:00a.m. - 11:30a.m.","11:30a.m. - 12:00a.m.","12:00a.m. - 12:30a.m.","12:30a.m. - 01:00p.m."]
        cursor.execute('SELECT ID,Name FROM TEACHER_DATA')
        teach_dic =  dict(cursor.fetchall())
        def teach_name(t_id,teach_dic=teach_dic):
            try:
                if not t_id.strip():
                    t_name = ''
                else:
                    t_name = teach_dic[int(t_id.strip())]
            except:
                t_name = '[UNDEFINED]'
            return t_name
        cursor.execute(f'SELECT {day.upper()} FROM ONLINE_CLASSES_DATA WHERE CLASS = ?',(st_class,))
        in_data = cursor.fetchone()
        if in_data is None:
            return '<h2>CLASSES NOT SCHEDULED.</h2>'
        data = in_data[0].split(';')
        for i in range(len(time)):
            d1,d2,d3 = tuple(data[i].split(','))
            if d1 and d3:
                html_text += f'''<div id="notifi"><div id="noti_heading">{d1}<i class="fa fa-tv" style="float:right;"></i></div><b>TEACHER NAME :- <font style="color: red;">{teach_name(d2)}</font><br>TIME :- <font style="color: red;">{time[i]}</font><br><a href="{d3}" target="_blank" id="class">JOIN CLASS</a></b><br><br></div>\n'''
        funt.Data().data_base_function(conn)
        return html_text

    def table_code(self,st_class=None,teacher_entity=False):
        conn,cursor = funt.Data().data_base_function()
        if st_class == None and teacher_entity == False:
            return '<h2>ERROR!!!</h2>'
        day = funt.Functions().get_day().strip().upper()
        html_text = f'<table border="3"><tr style="color:blue;"><th><i class="fa fa-list"></i></th>'
        time = ["09:00a.m. - 09:30a.m.","09:30a.m. - 10:00a.m.","10:00a.m. - 10:30a.m.","10:30a.m. - 11:00a.m.","11:00a.m. - 11:30a.m.","11:30a.m. - 12:00a.m.","12:00a.m. - 12:30a.m.","12:30a.m. - 01:00p.m."]
        for t in time:
            html_text += f'<th>{t}</th>'
        html_text += '</tr>'
        cursor.execute('SELECT ID,Name FROM TEACHER_DATA')
        teach_dic =  dict(cursor.fetchall())
        def teach_name(t_id,teach_dic=teach_dic):
            try:
                if not t_id.strip():
                    t_name = ''
                else:
                    t_name = teach_dic[int(t_id.strip())]
            except:
                t_name = '[UNDEFINED]'
            return t_name
        if teacher_entity != False:
            if day == "SUNDAY":
                return '<h2>TODAY IS SUNDAY!!!</h2>'
            cursor.execute(f'SELECT Class,{day} FROM ONLINE_CLASSES_DATA;')
            for row in cursor.fetchall():
                html_text += f'<tr><th>CLASS:- {row[0]}</th>'
                data = row[1].split(';')
                for item in data:
                    d1,d2,d3 = tuple(item.split(','))
                    html_text += f'<th><b><font color="green">SUBJECT  :- </font><br>{d1}<br><font color="green">TEACHER  :- </font><br>{teach_name(d2)}</b><br><a id="class" href="{d3}" target="_blank">TAKE CLASS</a></th>\n'
                html_text += "</tr>"
        else:
            li = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY']
            for day in li:
                cursor.execute(f'SELECT {day} FROM ONLINE_CLASSES_DATA WHERE CLASS = ?;',(st_class,))
                html_text += f'<tr><th style="color:blue;">{day}</th>'
                in_data = cursor.fetchone()
                if in_data is not None:
                    data = in_data[0].split(';')
                    for i in range(len(data)):
                        d1,d2,_ = tuple(data[i].split(','))
                        html_text += f'<th><b><font color="green">SUBJECT  :- </font><br>{d1}<br><font color="green">TEACHER  :- </font><br>{teach_name(d2)}</b></th>'
                html_text += "</tr>"
        html_text += '</table>'
        funt.Data().data_base_function(conn)
        return html_text
    
class Report_card(content_creator):
    def __init__(self):
        super().__init__()
        
    def select_st(self,c_class):
        html_text = f'<input name="c_class" value="{c_class}" hidden><h1>CLASS:- {c_class}</h1><b>CHOOSE STUDENT ADM. ID , NAME <label>*</label></b><select id="nor_opt" name="st_del" required><option value="">---SELECT---</option>'
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT Adm_ID,Name FROM STUDENT_DATA WHERE Class = ?',(c_class,))
        for row in cursor.fetchall():
            html_text += f'<option value="{row[0]}">{row[0]} , {row[1]}</option>'
        html_text += '</select><button type="submit" id="nor_btn">LOAD REPORT CARD</button>'
        funt.Data().data_base_function(conn)
        return html_text
    
    def view_report_card(self,st_id):
        def add(data):
            try:
                data = int(data)
                return data
            except ValueError:
                return 0
        def grade(mark,total):
            eq = (mark/total)*100
            if eq > 90:
                g = 'A1'
            elif eq > 80:
                g = "A2"
            elif eq > 70:
                g = "B1"
            elif eq > 60:
                g = "B2"
            elif eq > 50:
                g = "C1"
            elif eq > 40:
                g = "C2"
            elif eq >= 33:
                g = "D"
            else:
                g = "E"
            return g
        html_text = f"""<h1>STUDENT :- {st_id}</h1><table border="3">
        <tr><th rowspan="2">SUBJECTS</th><th colspan="5">TERM - 1</th><th colspan="5">TERM - 2</th><th colspan="2">FINAL TERM</th></tr>
        <tr><th>PT-1</th><th>ACT.</th><th>N.B.</th><th>H.Y.</th><th>TOTAL</th><th>PT- 2</th><th>ACT.</th><th>N.B.</th><th>FINAL</th><th>TOTAL</th><th>TOTAL</th><th>GRADE</th></tr>
        """
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT Class FROM STUDENT_DATA WHERE Adm_ID = ?',(st_id,))
        st_class = cursor.fetchone()[0]
        cursor.execute('SELECT TERM_1,TERM_2 FROM EXAM_DATA WHERE Adm_ID = ?',(st_id,))
        row = cursor.fetchall()[0]
        term1,term2 = row[0].split(';'),row[1].split(';')
        sub = super().subject_list(st_class)
        if len(term1) == len(term2):
            fft,tff1,tff2=0,0,0
            for i in range(len(term1)):
                ft,t = 0,0
                data1 = term1[i].split(',')
                data2 = term2[i].split(',')
                html_text += f'''<tr><th>{sub[i]}</th>'''
                for data in data1:
                    t += add(data)
                    html_text += f'<th>{data}</th>'
                html_text += f'<th>{t}</th>'
                ft = add(t)
                tff1 += add(t)
                t=0
                for data in data2:
                    t += add(data)
                    html_text += f'<th>{data}</th>'
                html_text += f'<th>{t}</th>'
                ft+= add(t)
                tff2 += add(t)
                fft += ft
                html_text += f"<th>{ft}</th><th>{grade(ft,200)}</th></tr>"
            html_text += f'<tr><th colspan="5"></th><th>{tff1}</th><th colspan="4"></th><th>{tff2}</th><th>{fft}</th><th>{grade(fft,len(sub)*200)}</th></tr></table>'
            # html_text += f'<a href="{funt.Export().report_card(html_text)}" download><button id="nor_btn">DOWNLOAD REPORT CARD  <i class="fa fa-download"></i></button></a>'
        else:
            html_text = "<h2>ERROR CAUSED IN DATABASE!!!</h2>"
        funt.Data().data_base_function(conn)
        return html_text

    def teach_st(self,stage,st_id,c_class):
        html_text = f'''<input name="c_class" value="{c_class}" hidden><input name="stage" value="st{stage+2}" hidden><input type="number" name="st_del" value="{st_id}" hidden><h1>REPORT CARD</h1><table border="3"><tr><th colspan="5"><code><u><i>NOTE:- </i></u> FOR ABSENT LEAVE BLANK INPUT FIELD.</code></th></tr><tr><th rowspan="2">REPORT CARD</th><th colspan="4">TERM:- {stage}</th></tr>
        <tr><th>P.T. [10]</th><th>ACT. [5]</th><th>N.B. [5]</th><th>MAIN [80]</th></tr>'''
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT Class FROM STUDENT_DATA WHERE Adm_ID = ?',(st_id,))
        c_class = cursor.fetchone()[0]
        cursor.execute('SELECT TERM_1,TERM_2 FROM EXAM_DATA WHERE Adm_ID = ?',(st_id,))
        row = cursor.fetchall()
        data = super().subject_list(c_class)
        for i in range(len(data)):
            t_1,t_2,t_3,t_4 = row[0][stage - 1].split(';')[i].split(',')
            html_text += f'''<tr><th>{data[i]}</th><th><input type="number" value="{t_1}" name="t{i+1}_1" min="0" max="10"></th>
            <th><input type="number" value="{t_2}" name="t{i+1}_2" min="0" max="5"></th>
            <th><input type="number" value="{t_3}" name="t{i+1}_3" min="0" max="5"></th>
            <th><input type="number" value="{t_4}" name="t{i+1}_4" min="0" max="80"></th></tr>'''
        if stage < 2:
            html_text += '</table><button id="nor_btn">NEXT >>></button>'
        else:
            html_text += '</table><button id="nor_btn">SAVE DATA</button>'
        funt.Data().data_base_function(conn)
        return html_text


class Attandance(content_creator):
    def __init__(self):
        super().__init__()

    def subject_opt(self,st_class):
        html_text = '<select id="nor_input" name="subject" required><option value="">---SELECT---</option>'
        for item in super().subject_list(st_class):
            html_text += f'<option value="{item}">{item}</option>'
        html_text += '</select>'
        return html_text
    
    def load_sub(self,st_class):
        if funt.Functions().get_day().strip().upper() == "SUNDAY":
            return f'<h2>TODAY IS SUNDAY!!!</h2>'
        html_text = f'''<input name="subject" value="{st_class}" hidden><b>CHOOSE SUBJECT <label>*</label></b>
        <select id="nor_opt" name="subject" required><option value="">---SELECT---</option>'''
        for item in super().subject_list(st_class):
            html_text += f'\n<option value="{item}">{item}</option>'
        html_text += '</select><button id="nor_btn">LOAD LIST</button>'
        return html_text
    
    def load_attandance_teacher(self,c_class,subject):
        date,_ = funt.Functions().get_date_time()
        html_text = f'<input name="st_class" value="{c_class}" hidden><input name="subject" value="{subject}" hidden><table border="2"><tr><th colspan="2">CLASS :- {c_class}</th><th colspan="3">ATTANDANCE</th></tr><tr><th>ADM. ID.</th><th>NAME</th><th>PRESENT</th><th>ABSENT</th><th>NOT STATED</th></tr>'
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT Adm_ID,Name FROM STUDENT_DATA WHERE Class = ?',(c_class,))
        at_data = cursor.fetchall()
        for item in at_data:
            cursor.execute('SELECT Status FROM ATTANDANCE WHERE Adm_ID = ? AND DATE = ? AND SUBJECT = ?',(item[0],date,subject))
            stat = cursor.fetchone()
            if stat is not None:
                if stat[0] == 'P':
                    html_text += f'<tr><th>{item[0]}</th><th>{item[1]}</th><td><input type="radio" name="{item[0]}" value="P" checked required></td><td><input type="radio" name="{item[0]}" value="A" required></td><td><input type="radio" name="{item[0]}" value="NA" required></td></tr>'
                elif stat[0] == 'A':
                    html_text += f'<tr><th>{item[0]}</th><th>{item[1]}</th><td><input type="radio" name="{item[0]}" value="P" required></td><td><input type="radio" name="{item[0]}" value="A" checked required></td><td><input type="radio" name="{item[0]}" value="NA" required></td></tr>'
                else:
                    html_text += f'<tr><th>{item[0]}</th><th>{item[1]}</th><td><input type="radio" name="{item[0]}" value="P" required></td><td><input type="radio" name="{item[0]}" value="A" required></td><td><input type="radio" name="{item[0]}" value="NA" checked required></td></tr>'
            else:
                html_text += f'<tr><th>{item[0]}</th><th>{item[1]}</th><td><input type="radio" name="{item[0]}" value="P" required></td><td><input type="radio" name="{item[0]}" value="A" required></td><td><input type="radio" name="{item[0]}" value="NA" checked required></td></tr>'
        html_text += '</table><button id="nor_btn">SUBMIT</button>'
        funt.Data().data_base_function(conn)
        return html_text
    
    def load_student_attandance(self,st_id,month,sub):
        html_text = f'<input name="stage" value="st2" hidden><table border="3"><tr><th>DATE</th><th>PRESENT [P]<br>ABSENT [A]<br>NOT STATED [NA]</th></tr>'
        def my_font(status):
            if status == 'P':
                properties = 'background:green;'
            elif status == 'A':
                properties = 'background:red;'
            elif status == 'NA':
                properties = 'background:grey;'
            elif status == 'S':
                properties = 'background:black;'
            return f'<mark style="{properties}color:white;padding:2px 2px;">{status}</mark>'
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT Date,Status FROM ATTANDANCE WHERE Adm_ID = ? AND Subject = ?',(st_id,sub))
        at_data = cursor.fetchall()
        for item in at_data:
            if item[0][5:7] == month:
                html_text += f'<tr><th>{item[0]}</th><th>{my_font(item[1])}</th></tr>'
        funt.Data().data_base_function(conn)
        html_text += '</table>'
        return html_text

class Log_History(content_creator):
    def user_log_history(self,user_id,user_type):
        html_text = '<table border="3"><tr><th>SR. NO.</th><th>IP ADDRESS</th><th>DATE</th><th>TIME</th></tr>'
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT HISTORY FROM LOG_HISTORY WHERE USER_ID = ? AND USER_TYPE = ?',(user_id,user_type))
        data = cursor.fetchone()
        funt.Data().data_base_function(conn)
        if data is None or data[0].strip() is None:
            return '<h2>DATA NOT FOUND</h2>'
        if ';' in data[0]:
            for i,item in enumerate(data[0].split(';'),start=1):
                nxt_data = item.split(',')
                html_text += f'<tr><td>{i}</td><td>{nxt_data[0]}</td><td>{nxt_data[1]}</td><td>{nxt_data[2]}</td></tr>'
        else:
            return '<h2>USER NOT LOGGED</h2>'
        return html_text + '</table>'

class Data_Sync:
    def data_sync(self):
        html_text = '''<form action="" method="post">
<table border="3"><caption><h2>PROGRESSION MODULE</h2></caption><tr><th rowspan="2"  style="width:5%;">ADM. ID.</th><th rowspan="2">NAME</th><th rowspan="2">FATHER</th><th rowspan="2">MOTHER</th><th rowspan="2">CLASS</th><th rowspan="2">D.O.B.</th><th colspan="3" style="width:20%;">CLASS ACTION</th></tr>
<tr><th>PROMOTED</th><th>NOT PROMOTED</th><th>LEAVED</th></tr>'''
        conn,cursor = funt.Data().data_base_function()
        cursor.execute('SELECT Adm_ID,Name,Father,Mother,Class,DOB FROM STUDENT_DATA;')
        for item in cursor.fetchall():
            Adm_ID,Name,Father,Mother,Class,DOB = item
            html_text += f'<tr><th>{Adm_ID}</th><th>{Name}</th><th>{Father}</th><th>{Mother}</th><th>{Class}</th><th>{DOB}</th><th><input type="radio" name="{Adm_ID}" value="P" required></th><th><input type="radio" name="{Adm_ID}" value="NP" required></th><th><input type="radio" name="{Adm_ID}" value="L" required></th></tr>'
        html_text += '''</table>
<fieldset>
<ul class="lines">
<li><input type="checkbox" required>I AM AGREED TO UPDATE ALL THE DATA. [FILLED ABOVE].</li>
<li><input type="checkbox" required>I AM AGREED TO RESET DATA TYPES HOMEWORK, ATTANDACE, CLASS TEST / EXAM TERMS, REPORT CARD.</li>
<li><input type="checkbox" required>I AM AGREED TO PROCEED FEES DATA OF STUDENTS INTO NEW SESSION.</li>
<hr>
<li><input type="checkbox" required>I HAVE READ ALL THE <a href="" target="_blank">INSTRUCTIONS & DIRECTIONS</a> TO USE THIS PROCESS.</li>
</ul>
<code><b><i>NOTE :- </i> ABOVE DATA FILLED BY YOU CANNOT BE CHANGED. ONLY REMOVING OF STUDENT ALLOW.</b></code>
<button id="nor_btn"><b>COMMIT DATA <i class="fa fa-upload"></i></b></button></form>
</fieldset>
'''
        funt.Data().data_base_function(conn)
        return html_text





