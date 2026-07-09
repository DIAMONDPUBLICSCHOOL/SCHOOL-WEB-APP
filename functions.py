import sqlite3,my_cryptography,datetime,json,subprocess
from reportlab.lib.pagesizes import A4,landscape
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import my_cryptography as crypt

class Data:
    def __init__(self):
        super().__init__()
    def data_base_function(self,conn=None):
        if conn != None:
            conn.commit()
            conn.close()
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        return conn,cursor
    def class_fees(self,st_class):
        fees_dic = {"1":3000,"2":3300,"3":3900,"4":4200,"5":4500,"6":4800,"7":5100,"8":5400}
        return int(fees_dic[str(st_class)])
    
class Functions(Data):
    def __init__(self):
        super().__init__()
    
    def command_box(self,command):
        with open('output.py', 'w') as f:
            f.write(command)
        result = subprocess.run(['python','output.py'],capture_output=True,text=True)
        output = result.stdout
        error = result.stderr
        with open('com_history.json','r') as f:
            li = json.load(f)
        li_list = [int(num) for num in li.keys() if num.isdigit()]
        num = max(li_list) if li_list else 0
        li[num+1] = {"command": command, "output": output, "error": error}
        open('output.py', 'w').close()
        with open('com_history.json', 'w') as f:
            json.dump(li,f,indent=4)
        return output, error

    def date_show_mon(self,d):
        if len(str(d).strip()) == 1:
            return f'0{d}'
        return d
    
    def get_date_time(self):
        d = datetime.date.today()
        t = datetime.datetime.now().strftime("%H:%M:%S")
        return d,t
    
    def get_day(self):
        day = datetime.date.today().strftime('%A')
        return day
    
    def get_month(self):
        day = datetime.date.today().strftime('%B')
        return day
    
    def change_time(self,Time='',hrs=0,min=0,sec=0):
        if hrs > 24 or min > 60 or sec > 60:
            raise ValueError('MINUTE & SECOND VALUES HAVE TO BE LESS THAN 60 AND HRS IS LESS THAN 24.')
        if not Time:
            Time = str(datetime.datetime.now().strftime("%H:%M:%S"))
        else:
            Time = str(Time)
        li = [int(data) for data in Time.split(':') if data.strip()]
        if sec != 0:
            li[2] = li[2] + sec
            if li[2] >= 60:
                li[2] = li[2] % 60
                li[1] = li[1] + 1
            if li[1] >= 60:
                li[1] = li[1] % 60
                li[0] = li[0] + 1
            if li[0] >= 24:
                li[0] = li[0] % 24
        if min != 0:
            li[1] = li[1] + min
            if li[1] >= 60:
                li[1] = li[1] % 60
                li[0] = li[0] + 1
            if li[0] >= 24:
                li[0] = li[0] % 24
        if hrs != 0:
            li[0] = li[0] + hrs
            if li[0] >= 24:
                li[0] = li[0] % 24
        return f'{self.date_show_mon(li[0])}:{self.date_show_mon(li[1])}:{self.date_show_mon(li[2])}'
    
    def crt_pwd(self,PWD):
        return crypt.log_pin_encrypt(PWD)
    
    def change_pwd(self,user_id,user_type,pwd,admin_entity=False,old_pwd=None):
        conn,cursor = self.data_base_function()
        if admin_entity is not False: 
            en_pwd = my_cryptography.log_pin_encrypt(pwd)
            cursor.execute('UPDATE PASSWORDS SET PASSWORD = ? WHERE LOG_TYPE = ? AND USER_ID = ?',(en_pwd,user_type,user_id))
            self.data_base_function(conn)
            return True
        else:
            if old_pwd is None:
                return False
            cursor.execute('SELECT PASSWORD FROM PASSWORDS WHERE LOG_TYPE = ? AND USER_ID = ?',(user_type,user_id))
            data = cursor.fetchone()
            if data is not None:
                de_pwd = my_cryptography.log_pin_decypt(data[0])
                if de_pwd == old_pwd:
                    en_pwd = my_cryptography.log_pin_encrypt(pwd)
                    cursor.execute('UPDATE PASSWORDS SET PASSWORD = ? WHERE LOG_TYPE = ? AND USER_ID = ?',(en_pwd,user_type,user_id))
                    self.data_base_function(conn)
                    return True
                else:
                    self.data_base_function(conn)
                    return False
            return False
            
    
    def crt_pdf(self,data,pdf_name,land=False,content=[]):
        element = []
        styles = getSampleStyleSheet()
        path = f"static/files/{pdf_name}"
        if land != False:
            pdf = SimpleDocTemplate(path,pagesize=landscape(A4))
        else:
            pdf = SimpleDocTemplate(path,pagesize=A4)
        element.append(Paragraph("<b>DIAMOND PUBLIC SCHOOL (D.P.S.)</b>", styles["Title"]))
        # element.append(Paragraph((pdf_name.upper()), styles["Heading2"]))
        if content:
            for item in content:
                item_ = item.split(';')
                if item_[1] == 'h1':
                    element.append(Paragraph(item_[0], styles["Heading1"]))
                elif item_[1] == 'h2':
                    element.append(Paragraph(item_[0], styles["Heading2"]))
                elif item_[1] == 'h3':
                    element.append(Paragraph(item_[0], styles["Heading3"]))
        table = Table(data)
        table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 1, colors.black),("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),("ALIGN", (0,0), (-1, -1), "CENTER"),("FONT", (0, 0), (-1, 0), "Helvetica-Bold")]))
        element.append(table)
        element.append(Paragraph("AUTO GENERATED BY COMPUTER. SIGNATURE NOT REQUIRED. [FOR MORE INFO. VISIT:- <u>bit.ly/dpsjalesar</u>]", styles["Heading6"]))
        pdf.build(element)
        return

class LOGIN(Functions):
    def __init__(self):
        super().__init__()
    def check_pwd(self,log_type,U_N,PWD):
        if log_type == 'ADMIN':
            if U_N == '1' and PWD == crypt.log_pin_decypt(crypt.admin_log_pass()):
                return True
            else:
                return False        
        conn,cursor = self.data_base_function()
        de_PWD = ''
        cursor.execute('SELECT PASSWORD FROM PASSWORDS WHERE LOG_TYPE = ? AND USER_ID = ?',(log_type,U_N))
        de_PWD = cursor.fetchone()
        if de_PWD and de_PWD is not None:
            if PWD == crypt.log_pin_decypt(str(de_PWD)):
                return True
        self.data_base_function(conn)
        return False
    

class Export(Functions):
    def __init__(self):
        super().__init__()

    def student_data(self):
        conn,cursor = self.data_base_function()
        ST_LIST = [["ADM. ID","NAME","FATHER","MOTHER","CLASS","DOB","ADDRESS","MOBILE","ADHAAR","PEN"]]
        cursor.execute('SELECT * FROM STUDENT_DATA;')
        for row in cursor.fetchall():
            draft_list = [d for d in row]
            ST_LIST.append(draft_list)
        pdf = "STUDENT_DETAILS.pdf"
        content = ["STUDENT DETAILS;h2"]
        super().crt_pdf(ST_LIST,pdf,land=True,content=content)
        self.data_base_function(conn)
        return 

    def student_pwd(self):
        conn,cursor = self.data_base_function()
        PWD_LIST = [["ADM. NO.","PASSWORD"]]
        cursor.execute('SELECT USER_ID,PASSWORD FROM PASSWORDS WHERE LOG_TYPE = ?;',("STUDENT",))
        for row in cursor.fetchall():
            darft_list = []
            darft_list.append(row[0])
            darft_list.append(my_cryptography.log_pin_decypt(row[1]))
            PWD_LIST.append(darft_list)
        pdf = "STUDENT_PASSWORDS.pdf"
        content = ["STUDENT PASSWORDS;h2"]
        super().crt_pdf(PWD_LIST,pdf,content=content)
        self.data_base_function(conn)
        return
    
    def teacher_data(self):
        conn,cursor = self.data_base_function()
        T_LIST = [["ID","NAME","FATHER","MOTHER","DOB","ADDRESS","MOBILE","ADHAAR"]]
        cursor.execute('SELECT * FROM TEACHER_DATA;')
        for row in cursor.fetchall():
            draft_list = [d for d in row]
            T_LIST.append(draft_list)
        pdf = "TEACHER_DETAILS.pdf"
        content = ["TEACHER DETAILS;h2"]
        super().crt_pdf(T_LIST,pdf,land=True,content=content)
        self.data_base_function(conn)
        return 

    def teacher_pwd(self):
        conn,cursor = self.data_base_function()
        PWD_LIST = [["ID.","PASSWORD"]]
        cursor.execute('SELECT USER_ID,PASSWORD FROM PASSWORDS WHERE LOG_TYPE = ?;',("TEACHER",))
        for row in cursor.fetchall():
            darft_list = []
            darft_list.append(row[0])
            darft_list.append(my_cryptography.log_pin_decypt(row[1]))
            PWD_LIST.append(darft_list)
        pdf = "TEACHER_PASSWORDS.pdf"
        content = ["TEACHER PASSWORDS;h2"]
        super().crt_pdf(PWD_LIST,pdf,content=content)
        self.data_base_function(conn)
        return
    
    def fees_slip_export(self,st_id,fees_amount,rest):
        conn,cursor = self.data_base_function()
        cursor.execute('SELECT Name,Father,Mother,Class FROM STUDENT_DATA WHERE Adm_ID = ?;',(st_id,))
        st_name,st_father,st_mother,st_class = cursor.fetchone()
        pdf = f"FEES_SLIP.pdf"
        cursor.execute("SELECT FEES_ID FROM FEES_DATA ORDER BY FEES_ID DESC;")
        receipt_id = int(cursor.fetchone()[0]) + 1
        d,t = super().get_date_time()
        content = ["FEES SLIP;h2",f"RECEIPT NO :- {receipt_id};h3",f"DATE/TIME :- {d}{t};h3",f"ADMISSION NO.:- {st_id};h3",f"NAME :- {st_name};h3",f"FATHER NAME:- {st_father};h3",f"MOTHER NAME :- {st_mother};h3",f"CLASS :- {st_class};h3"]
        Fees_list = [["ACCECCIRORIES","AMOUNT"],["TUTION FEES","-"],["ELECTRICITY FEES","-"],["MAINTENANCE FEES","-"],["FURNITURE FEES","-"],["OTHER FEES","-"],["TOTAL FEES",fees_amount],["REST FEES:-",rest]]
        super().crt_pdf(Fees_list,pdf,content=content)
        self.data_base_function(conn)
        return

    def report_card(self,html_text):
        a = ''
        return


class Data_sync(Functions):
    def __init__(self):
        super().__init__()
    
    def data_sync(self,data_dic):
        conn,cursor = self.data_base_function()
        with open('datasync.json','r') as f:
            data_sync_dic = json.load(f)
        d,t = self.get_date_time()
        data_sync_dic[str(d)[:4]]={"DATE":str(d),"TIME":str(t),"STATUS":{}}
        try:
            for item,value in data_dic.items():
                cursor.execute('SELECT CLASS FROM STUDENT_DATA WHERE Adm_ID = ?',(int(item),))
                st_class = cursor.fetchone()[0]
                if value == 'P':
                    if int(st_class) < 8:
                        st_class = str(int(st_class)+1)
                        cursor.execute('UPDATE STUDENT_DATA SET CLASS = ? WHERE Adm_ID = ?',(st_class,int(item)))
                    else:
                        cursor.execute('DELETE FROM STUDENT_DATA WHERE Adm_ID = ?',(int(item),))
                        cursor.execute('DELETE FROM LOG_HISTORY WHERE USER_ID = ? AND USER_TYPE = = "STUDENT"',(int(item),))
                        cursor.execute('DELETE FROM EXAM_DATA WHERE Adm_ID = ?',(int(item),))
                        cursor.execute('DELETE FROM BLOCK_USER WHERE USER_ID = ? AND USER_TYPE = "STUDENT";',(int(item),))
                elif value == 'L':
                    cursor.execute('DELETE FROM STUDENT_DATA WHERE Adm_ID = ?',(int(item),))
                    cursor.execute('DELETE FROM LOG_HISTORY WHERE USER_ID = ? AND USER_TYPE = "STUDENT"',(int(item),))
                    cursor.execute('DELETE FROM EXAM_DATA WHERE Adm_ID = ?',(int(item),))
                    cursor.execute('DELETE FROM SINGLE_LOG WHERE USER_TYPE = ? AND USER_ID = ?',('STUDENT',int(item)))
                    cursor.execute('DELETE FROM BLOCK_USER WHERE USER_ID = ? AND USER_TYPE = "STUDENT";',(int(item),))
                else:
                    pass
            data_sync_dic[str(d)[:4]]["STATUS"]["CLASSES"]="PASS"
        except:
            data_sync_dic[str(d)[:4]]["STATUS"]["CLASSES"]="FAILED"
        conn.commit()

        ###data reset
        try:
            cursor.execute('DELETE FROM ATTANDANCE;')
            cursor.execute('DELETE FROM EXAM_DATA;')
            cursor.execute('DELETE FROM STUDENT_TEST_DATA;')
            cursor.execute('DELETE FROM TEST_DATA;')
            cursor.execute('DELETE FROM HW_DATA;')
            data_sync_dic[str(d)[:4]]["STATUS"]["DATA_RESET"]="PASS"
        except:
            data_sync_dic[str(d)[:4]]["STATUS"]["DATA_RESET"]="FAILED"
        conn.commit()

        ###fees data
        try:
            fees_session = str(d)[:4]
            cursor.execute('SELECT Adm_ID,CLASS FROM STUDENT_DATA;')
            data = cursor.fetchall()
            for item in data:
                cursor.execute('SELECT REST FROM FEES_DATA WHERE SESSION = ? AND Adm_ID = ? ORDER BY FEES_ID DESC;',(fees_session,item[0]))
                rest_fees = cursor.fetchone()
                if rest_fees is not None:
                    fees = rest_fees[0] + Data().class_fees(st_class)
                    cursor.execute('INSERT INTO FEES_DATA VALUES(?,?,?,?,?)',(0,item[0],0,fees,fees_session+1))
            data_sync_dic[str(d)[:4]]["STATUS"]["FEES"]="PASS"
        except:
            data_sync_dic[str(d)[:4]]["STATUS"]["FEES"]="FAILED"
        conn.commit()
        self.data_base_function(conn)

        ###last step
        with open('datasync.json','w') as f:
            json.dump(data_sync_dic,f,indent=4)
        return str(self.data_sync_status_funt())

    def data_sync_status_funt(self):
        html_text = '<table border="3"><caption><h2>STATUS TABLE</h2></caption><tr><th>ACTION</th><th>STATUS</th></tr>'
        def color(status):
            status = status.upper().strip()
            if status == "PASS":
                return '<font style="color:green;"><i class="fa fa-check-circle"></i></font>'
            else:
                return '<font style="color:red;">&times;</font>'
        d,_ = self.get_date_time()
        with open('datasync.json','r') as f:
            data_sync_dic = json.load(f)
        data_sync_status_dic = data_sync_dic[str(d)[:4]]['STATUS']
        html_text += f'''<tr><th>STUDENT PROMOTION</th><th>{color(data_sync_status_dic["CLASSES"])}</th></tr>
<tr><th>DATA RESET</th><th>{color(data_sync_status_dic["DATA_RESET"])}</th></tr>
<tr><th>FEES DATA UPDATE</th><th>{color(data_sync_status_dic["FEES"])}</th></tr></table>
<h3>OVERALL STATUS:- '''
        if data_sync_status_dic["CLASSES"].upper().strip() == "PASS"  and data_sync_status_dic["DATA_RESET"].upper().strip() == "PASS" and data_sync_status_dic["FEES"].upper().strip() == "PASS":
            html_text += f'<font style="color:green;"><i class="fa fa-check-circle"></i> DONE!!!</font> SESSION:- {str(d)[:4]}</h3>'
        else:
            html_text += f'<font style="color:red;">&times; FAILED!!!</font></h3><b>NOTE:- CONTACT DEVELOPER!!!</b>'
        html_text += f'<b>DATA UPDATE DATE/TIME:- <font style="color:red;">{data_sync_dic[str(d)[:4]]['DATE']},{data_sync_dic[str(d)[:4]]['TIME']}</font></b>'
        return html_text 


