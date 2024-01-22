import datetime
from flask import Flask, render_template, request, redirect , flash,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import query
import json

app = Flask("SeleneU")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://admin:awsk12023!@sereneu.cpu406qi0df7.ap-northeast-2.rds.amazonaws.com/sereneu'  # MySQL 데이터베이스 설정
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 경고 메시지 비활성화
app.config["SECRET_KEY"] = 'd2707fea9778e085491e2dbbc73ff30e'

db = SQLAlchemy(app)
UPLOAD_FOLDER = 'static/uploads'  # 업로드된 파일이 저장될 디렉토리
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 허용할 파일 확장자
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def certified():
    return render_template('Certified.html')

@app.route("/sub",methods=['GET', 'POST'])
def sub():
    pw = request.form.get('pw', '')
    if(pw == "900910"):
        return redirect('/scheduleview')
    else:
        flash("넌 이세희가 아니다. 돌아가")
        return render_template('Certified.html')


@app.route("/member")
def member():
    flag = request.args.get('flag','')
    search_param = request.args.get('search_param','')
    if flag == "0" :
        members = db.session.execute(query.selectMemberFilterName, {'member_name': search_param})
    elif flag == "1":
        search_param = search_param.replace("-","")
        members = db.session.execute(query.selectMemberFilterPhone, {'member_phone': search_param})
    else :
        members = db.session.execute(query.selectMemberSergical)
        
    return render_template('members.html', members=members)

@app.route("/selectMember",methods=['GET'])
def selectMember():
    flag = request.args.get('flag','')
    search_param = request.args.get('search_param','')
    if flag == "0" :
        members = db.session.execute(query.selectMemberFilterName, {'member_name': search_param})
    elif flag == "1":
        search_param = search_param.replace("-","")
        members = db.session.execute(query.selectMemberFilterPhone, {'member_phone': search_param})
    # 쿼리 결과를 딕셔너리 리스트로 변환
    members_list = []
    for member in members:
        member_dict = {
            'member_id': member.member_id,
            'customer_name': member.customer_name,
            'customer_phone': member.customer_phone,
            'gender': member.gender,
        }
        members_list.append(member_dict)
    json_data = json.dumps(members_list, ensure_ascii=False)
    
    return json_data

    
# 루트 경로에서 MEMBER 테이블 데이터 조회
@app.route('/search')
def view_members():
    flag = request.args.get('flag','')
    search_param = request.args.get('search_param','')
    if flag == "0" :
        members = db.session.execute(query.selectMemberFilterName, {'member_name': search_param})
    elif flag == "1":
        search_param = search_param.replace("-","")
        members = db.session.execute(query.selectMemberFilterPhone, {'member_phone': search_param})
    else :
        members = db.session.execute(query.selectMemberSergical)
        #members = SereneMember.query.all()
    if not members:
        flash(f"세희야... {search_param}은 고객리스트에 없단다...")
    return render_template('members.html', members=members)


@app.route( "/home",methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route( "/surgeryForm",methods=['GET', 'POST'])
def surgeryForm():
    flag = request.args.get('flag','0')
    surgery_id = request.args.get('surgery_id','')
    if flag != "0":
        surgeryInfo = db.session.execute(query.selectSurgeryform, {'surgery_id': surgery_id})
        row = surgeryInfo.fetchone()
        return render_template('surgeryForm.html',flag=flag,row = row)
    else:
        return render_template('surgeryForm.html',flag=flag)


@app.route( "/reservation",methods=['GET', 'POST'])
def reservation():
    memberid = request.args.get('memberid')
    return render_template("reservation.html",memberid=memberid)

@app.route( "/scheduleview",methods=['GET', 'POST'])
def scheduleview():
    # 현재 날짜를 가져옵니다
    now = datetime.now()
    this_month_first_day = now.replace(day=1)
    this_month_str = this_month_first_day.strftime("%Y%m%d")
    next_month_first_day = this_month_first_day + relativedelta(months=1)
    next_month_str = next_month_first_day.strftime("%Y%m%d")
    # 쿼리 실행
    schedule = db.session.execute(query.selectSchedule, {'start_date': this_month_str, 'end_date': next_month_str})
    # 쿼리 결과를 딕셔너리 리스트로 변환
    schedule_list = []
    for row in schedule:
        row_dict = {
            'id':row[0],
            'title': row[1],  # 두 번째 열
            'start': row[2]  # 세 번째 열
        }
        schedule_list.append(row_dict)

    return render_template("calendar_schedule_table.html", schedule_list=schedule_list)

@app.route( "/eventData",methods=['GET', 'POST'])
def eventData():
    # 현재 날짜를 가져옵니다
    now = datetime.now()
    this_month_first_day = now.replace(day=1)
    this_month_str = this_month_first_day.strftime("%Y%m%d")
    next_month_first_day = this_month_first_day + relativedelta(months=1)
    next_month_str = next_month_first_day.strftime("%Y%m%d")
    # 쿼리 실행
    schedule = db.session.execute(query.selectSchedule, {'start_date': this_month_str, 'end_date': next_month_str})
    # 쿼리 결과를 딕셔너리 리스트로 변환
    schedule_list = []
    for row in schedule:
        row_dict = {
            'id':row[0],
            'title': row[1],  # 두 번째 열
            'start': row[2]  # 세 번째 열
        }
        schedule_list.append(row_dict)
    
    return schedule_list

@app.route('/add_surgery', methods=['GET'])
def add_surgery():
    if request.method == 'GET':
        member_id = request.args.get('member_id')
        categori = request.args.get('categori')
        price = int(request.args.get('price').replace(",",""))
        visit_time = request.args.get('visit_time')
    
        # Surgery 테이블에 데이터 삽입
        result = db.session.execute(query.insertSergery, {'surgery_info': categori, 'payment_amount': price, "member_id":member_id, "visit_time":visit_time})
        db.session.commit()
        resultCheck = False
        if result.rowcount > 0:
            # 업데이트 성공
            resultCheck = True
        else:
            # 업데이트 실패
            resultCheck = False
        return jsonify({"resultCheck": resultCheck})

@app.route('/update_surgery', methods=['GET'])
def updateSurgery():
    surgery_id = request.args.get('surgery_id')
    member_id = request.args.get('member_id')
    categori = request.args.get('categori')
    price = int(request.args.get('price').replace(",",""))
    visit_time = request.args.get('visit_time')
    # 쿼리 실행
    result = db.session.execute(query.update_surgery, {'sergery_id': surgery_id, 'categori': categori,'price':price,'member_id':member_id,'visit_time':visit_time})
    db.session.commit()
    resultCheck = False
    if result.rowcount > 0:
        # 업데이트 성공
        resultCheck = True
    else:
        # 업데이트 실패
        resultCheck = False
    return jsonify({"resultCheck": resultCheck})

@app.route('/delete_surgery', methods=['GET'])
def deleteSurgery():
    surgery_id = request.args.get('surgery_id')
    # 쿼리 실행
    result = db.session.execute(query.delete_surgery, {'sergery_id': surgery_id})
    db.session.commit()
    resultCheck = False
    if result.rowcount > 0:
        # 업데이트 성공
        resultCheck = True
    else:
        # 업데이트 실패
        resultCheck = False
    return jsonify({"resultCheck": resultCheck})

@app.route('/update_date', methods=['GET'])
def update_date():
    surgery_id = request.args.get('surgery_id')
    visit_time = request.args.get('visit_time')
    # 쿼리 실행
    result = db.session.execute(query.update_date, {'sergery_id': surgery_id,'visit_time':visit_time})
    db.session.commit()
    resultCheck = False
    if result.rowcount > 0:
        # 업데이트 성공
        resultCheck = True
    else:
        # 업데이트 실패
        resultCheck = False
    return jsonify({"resultCheck": resultCheck})



@app.route('/add_member', methods=['GET','POST'])
def add_member():
    return render_template("addMember.html")

@app.route('/insert_member',methods=['GET','POST'])
def insert_member():
    customer_name = request.form['name']
    customer_phone = request.form['phone']
    gender = request.form['gender']
    # Surgery 테이블에 데이터 삽입
    surgery = db.session.execute(query.insertMember, {'customer_name': customer_name,'customer_phone':customer_phone,'gender':gender})
    db.session.commit()
    
    return redirect('/search')  # 삽입 후 페이지 리디렉션

# 파일 업로드 예제
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        print(file)
        print(file.filename)
        filename = datetime.now().strftime("%Y%m%d%H%M%S%f") + "." + file.filename.split(".")[1]
        print(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # 파일 정보를 데이터베이스에 저장
        member_id = request.form['member_id']
        categori = request.form['categori']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_name = filename
        uploaddate = datetime.now()
        imgfile = db.session.execute(query.insertImgFile, {'member_id': member_id,'categori':categori,'file_path':file_path,'file_name':file_name,'uploaddate':uploaddate})
        db.session.commit()

        return redirect('/search')


#app.run(host='0.0.0.0')
app.run(debug=True)
