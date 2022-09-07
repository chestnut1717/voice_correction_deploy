import asyncio
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from utils import *
import soundfile as sf

# 처음 서버를 열때 모델 동시 불러옴(배포시 메모리 / 시간절약)
global model, tokenizer
model = phonemize.load_model()
tokenizer = phonemize.load_tokenizer()


# 서버로부터 응답시간이 걸리기 때문에 그동안 비동기 처리
async def get_result(audio, ans_transcription):

    # Answer -> phoneme
    ans_phoneme = await loop.run_in_executor(None, phonemize.text_to_phoneme, ans_transcription, False)
    ans_phoneme_stress = await loop.run_in_executor(None, phonemize.text_to_phoneme, ans_transcription, True)

    # User voice(.wav) -> text -> phoneme
    deaf_transcription, deaf_phoneme = await loop.run_in_executor(None, phonemize.speak_to_phoneme, audio, tokenizer, model, False)

    # 발음 평가
    lcs = result.lcs_algo(ans_phoneme, deaf_phoneme, len(ans_phoneme), len(deaf_phoneme))    
    accuracy, score = result.calculate_acc(ans_phoneme, lcs)

    # 틀린 음소 추출
    correct_list = result.highlight(ans_phoneme, lcs)

    global data
    data = {"answer" : [ans_transcription, ans_phoneme_stress],
        "deaf" : [deaf_transcription, deaf_phoneme],
        "result": [accuracy, score],
        "correct_list" : correct_list }


# 개별화 음성 제작하기 위해 외부 딥러닝 서버 통신과정
async def connect_server(audio, ans_transcription, sr):
    print("서버 연결 시작")
    ans_wav, sr = await loop.run_in_executor(None, rtvc_conn.get_wav, audio, sr, ans_transcription)
    # ans_wav, sr = rtvc_conn.get_wav(audio, sr, ans_transcription)
    
    # 맞춤형 원어민 발화 데이터 저장
    sf.write("database/audio/answer.wav", ans_wav, sr)
    print('개별화된 audio 저장 완료')


# 비동기 처리 메인함수
async def main(audio, ans_transcription, sr):
    task1 = asyncio.create_task(get_result(audio, ans_transcription))
    task2 = asyncio.create_task(connect_server(audio, ans_transcription, sr))
    await task2
    await task1


#Flask 객체 인스턴스 생성
app = Flask(__name__)

# main page
@app.route('/', methods=['GET', 'POST']) 
def index():
    rtvc_conn.wake_server()
    return render_template('index.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        return render_template('signup.html')


# service page
@app.route('/service_qa/<level>', methods=["GET", "POST"])
def record(level):
    if request.method == "GET":
        global answer

        # 각 레벨별 사이트에 접속하면 db에서 각 level에 맞는 데이터를 가져온다
        context, question, answer, sentence, blank_answer, title = link_mysql.load_context(level)


        return render_template('service_qa.html', data={"level"       : level,
                                                        "context"     : context,
                                                        "question"    : question,
                                                        "blank_answer": blank_answer,
                                                        "sentence"    : sentence, 
                                                        "title"       : title})
    
    elif request.method == 'POST':
        # 사용자가 음성을 녹음해서 전송하면 다음 명령이 실행
        audio, sr = preprocessing.blob_to_wav(request)
        # 전역변수 사용
        ans_transcription = answer

        # 비동기처리 작업
        global loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main(audio, ans_transcription, sr))          # main이 끝날 때까지 기다림
        loop.close()

        # 처리가 끝나고 개별화된 목소리를 받아온다
        ans_wav, sr = sf.read('database/audio/answer.wav')

        # 그리고 개별화된 정답 목소리와 사용자 목소리의 pitch 비교
        result.to_graph(ans_wav, audio, smoothing=True)

        return redirect(url_for('feedback'))


# 피드백 화면
@app.route('/feedback', methods=['GET'])
def feedback():
    return render_template('feedback.html', data=data)

# 동영상
@app.route('/database/video/<filename>')
def video_download(filename):
    return send_from_directory('database/video', filename)

# 이미지
@app.route('/database/image/<filename>')
def image_download(filename):
    return send_from_directory('database/image', filename)

# 그래프
@app.route('/database/graph/<filename>')
def graph_download(filename):
    return send_from_directory('database/graph', filename)

# 오디오
@app.route('/database/audio/<filename>')
def audio_download(filename):
    return send_from_directory('database/audio', filename)


if __name__=="__main__":
    # rtvc_conn.wake_server()
    app.run(host="0.0.0.0", port="5000", use_reloader=False)
    # wake external model server