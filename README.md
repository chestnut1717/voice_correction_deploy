# BETTer
**접속 : http://example-server.shop/**

![image](https://user-images.githubusercontent.com/62554639/187997853-5cce284f-f17f-4506-89d3-d193365930ef.png)


## 1. 필요 라이브러리 및 프로그램

### 환경
- for local : Windows 10. python 3.7, conda virtual env
- for deploy : Ubuntu(18.04) python 3.7 

```
librosa == 0.8.1
pydub == 0.25.1
noisereduce == 2.0.1
transformers == 4.21.1
phonemizer == 3.2.1
torch
Flask==2.1.2
flask-restx==0.5.1
SoundFile==0.10.3.post1
```

### 1.1 추가 설치 프로그램
- phonemizer 라이브러리를 사용하려면 설치해야 함
```
espeak
```

#### 1.1.1 Windows에서는 다음과 같이 espeak을 깔아야 한다

1. Download and install the Windows version of espeak: http://espeak.sourceforge.net/download.html

2. set PATH=%PATH%;"C:\Program Files (x86)\eSpeak\command_line\"_

3. https://github.com/espeak-ng/espeak-ng/releases에서 .msi 설치

4. 환경변수 입력 후 재부팅
```
1.PHONEMIZER_ESPEAK_LIBRARY="c:\Program Files\eSpeak NG\libespeak-ng.dll"
2.PHONEMIZER_ESPEAK_PATH =“c:\Program Files\eSpeak NG”
```

#### 1.1.2 리눅스(ubuntu 18.04)에서는 다음과 같은 명령어로 바로 깔림
```
sudo apt-get install python-espeak
sudo apt-get update && sudo apt-get install espeak
```

#### 1.1.3추가 다운로드 파일(용량문제로 공유 drive에 업로드)
- 사전학습된 Wav2Vec2.0모델 : https://drive.google.com/drive/folders/1wpFX_3H1GbcvgyXMHtObtKp3U5v2nwVS?usp=sharing
- tokenizer : https://drive.google.com/drive/folders/1nuXzOSj4Xxh9emfi19NxEwUwkICtVMYf?usp=sharing
- 각각 다운받아서 web_flask 폴더에 넣어주면 된다

### 필요 라이브러리 및 프로그램 설치, 추가 파일 다운로드 후 web_flask 내의*app.py*를 실행시키면 된다   

* * *
## 2. 사용시 유의사항
### 2.1  마이크 사용 관련
- 아직 https 보안 연결이 안된 사이트이기 때문에 chrome, edge 등의 브라우저에서는 마이크 작동을 막아놓음
- 따라서 배포된 사이트에서는 다음과 같은 작업을 통해 마이크 제한을 해제해주어야 함
- HTTPS 연결을 하면 해결되는 문제
1. chrome://flags/#unsafely-treat-insecure-origin-as-secure 들어가기
2. insecure origins treated as secure에 http://example-server.shop/ url 등록하기
![image](https://user-images.githubusercontent.com/62554639/187994497-24b4f23a-07e7-4c0b-b658-20b5ce7dc463.png)

### 2.2 서버 속도 관련
- 개별화된 목소리를 생성하는 데 딥러닝 모델을 사용하고 있고, 무료 서버를 사용하고 있기 때문에 음성을 받아오는 데에 시간이 걸린다 (*30초 ~ 1분*)
- 여러 서버로 나누어서 분산 작업을 해도 마찬가지이다
- torch gpu버전을 설치하고 gpu환경에서 작동시키면 훨씬 빠른 속도로 음성을 받아올 수 있다


* * *


## 3. 서버 / DB
### 3.1 voice cloning 서버 - Fast API기반, Heroku로 배포(CPU * 1 / RAM : 512mb)
- 개별화된 목소리를 만들어내기 위해 다음과 같은 서버로 요청, 응답받고 있음 (https://github.com/queque5987/better-voice-cloning 참고)
- Encoder : https://better-encoder.herokuapp.com/inference/
- Synthesizer : https://better-synthesizer.herokuapp.com/inference/
- Vocoder : https://better-vocoder.herokuapp.com/inference/

### 3.2 웹 + 분석모델 서버 - Flask 기반, AWS EC2로 배포(CPU * 1 / RAM : 1G)   


### 3.3 DB - MySQL, AWS RDS

* * *
## 4. License
### 4.1 입모양 영상 파일
- https://www.bbc.co.uk/worldservice/learningenglish/grammar/pron/

### 4.2 Template

```
Template Name: FlexStart
Template URL: https://bootstrapmade.com/flexstart-bootstrap-startup-template/
Author: BootstrapMade.com
License: https://bootstrapmade.com/license/
```
</hr>
