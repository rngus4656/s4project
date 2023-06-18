from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import re
import subprocess
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('survey_result.db')
    c = conn.cursor()

    # 테이블이 이미 존재하는지 확인하고, 없다면 새로 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS survey_result
        (id INTEGER PRIMARY KEY, satisfaction INTEGER, willingness INTEGER, feedback TEXT)
    ''')

    conn.commit()
    conn.close()

def insert_survey_result(satisfaction, willingness, feedback):
    conn = sqlite3.connect('survey_result.db')
    c = conn.cursor()

    # 데이터 삽입
    c.execute('''
        INSERT INTO survey_result (satisfaction, willingness, feedback)
        VALUES (?, ?, ?)
    ''', (satisfaction, willingness, feedback))

    conn.commit()
    conn.close()

def get_survey_results():
    conn = sqlite3.connect('survey_result.db')
    c = conn.cursor()

    # 데이터 조회
    c.execute('SELECT * FROM survey_result')

    results = c.fetchall()

    conn.close()

    return results

# 이미지를 저장할 폴더 지정
UPLOAD_FOLDER = 'img/input'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 가장 최신의 출력 파일을 찾는 함수
def get_latest_file(dir_path):
    all_files = [f for f in os.listdir(dir_path) if f.endswith('.png')]
    all_nums = [int(re.search(r'(\d+)', f).group(1)) for f in all_files]
    max_num = max(all_nums, default=None)

    if max_num is not None:
        return f'grid-{max_num:04}.png'
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file:
            filename = 'upload_img.jpg'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # 이미지 처리 코드 실행
        subprocess.run(["python", "upload_img.py"])  # upload_img.py 실행

        gender = request.form.get('gender')  # 체크박스 값 가져오기
        strength = request.form.get('strength')  # 강도 값 가져오기

        # img2img.py 실행에 필요한 프롬프트 설정
        prompt = "master_piece, best_quality, anime protagonist, " + gender

        # img2img.py 실행
        subprocess.run(["python", "./scripts/img2img.py", "--prompt", prompt, "--strength", strength])

        return redirect(url_for('result'))

    return render_template('main.html')

@app.route('/result')
def result():
    # 결과 이미지 파일 경로
    latest_file = get_latest_file('static/output')
    result_path = 'output/' + latest_file

    return render_template('result.html', image_path=result_path)

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        satisfaction = request.form.get('satisfaction')
        willingness = request.form.get('willingness')
        feedback = request.form.get('feedback')

        insert_survey_result(satisfaction, willingness, feedback)

        return redirect(url_for('survey_result'))

    return render_template('survey.html')

@app.route('/survey_result')
def survey_result():
    results = get_survey_results()

    return render_template('survey_result.html', results=results)

init_db()

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', debug=True)

