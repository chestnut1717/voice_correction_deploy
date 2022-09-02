# BETTer
**페이지 접속 : http://example-server.shop/**

![image](https://user-images.githubusercontent.com/62554639/187997853-5cce284f-f17f-4506-89d3-d193365930ef.png)


## 1. 필요 라이브러리 및 프로그램(로컬에서 실행할 경우에서만 필요합니다)

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
- phonemizer 라이브러리 사용을 위해서는 설치가 필요합니다.
```
espeak
```

#### 1.1.1 Windows에서는 다음과 같이 espeak을 설치해야 합니다.

1. Download and install the Windows version of espeak: http://espeak.sourceforge.net/download.html

2. set PATH=%PATH%;"C:\Program Files (x86)\eSpeak\command_line\"_

3. https://github.com/espeak-ng/espeak-ng/releases에서 .msi 설치

4. 환경변수 입력 후 재부팅
```
1.PHONEMIZER_ESPEAK_LIBRARY="c:\Program Files\eSpeak NG\libespeak-ng.dll"
2.PHONEMIZER_ESPEAK_PATH =“c:\Program Files\eSpeak NG”
```

#### 1.1.2 리눅스(ubuntu 18.04)에서는 다음과 같은 명령어를 통해 바로 실행이 가능합니다.
```
sudo apt-get install python-espeak
sudo apt-get update && sudo apt-get install espeak
```

#### 1.1.3추가 다운로드 파일(용량문제로 인해 공유 drive에 업로드)
- 사전학습 된 Wav2Vec2.0모델 : https://drive.google.com/drive/folders/1wpFX_3H1GbcvgyXMHtObtKp3U5v2nwVS?usp=sharing
- tokenizer : https://drive.google.com/drive/folders/1nuXzOSj4Xxh9emfi19NxEwUwkICtVMYf?usp=sharing
- 각각 다운받아 web_flask 폴더에 담아주세요.

### 필요 라이브러리 및 프로그램 설치, 추가 파일 다운로드 후 web_flask 내의*app.py*를 실행시키면 사용이 가능합니다.   

* * *
## 2. 사용 시 유의사항
### 2.1  마이크 사용 관련
- 아직 https 보안 연결이 되지 않은 사이트이기 때문에 chrome, edge 등의 브라우저에서는 마이크 작동이 불가능합니다.
- 따라서 다음과 같이  HTTPS를 연결하는 작업을 통해 마이크 제한을 해제해야 합니다.
1. chrome://flags/#unsafely-treat-insecure-origin-as-secure 들어가기
2. insecure origins treated as secure에 http://example-server.shop/ url 등록하기
![image](https://user-images.githubusercontent.com/62554639/187994497-24b4f23a-07e7-4c0b-b658-20b5ce7dc463.png)

### 2.2 서버 속도 관련
- 개별화된 목소리를 생성하기 위해 딥러닝 모델을 사용하고 있으며, 무료 서버를 사용하고 있기 때문에 음성을 받아오는 데에 어느 정도의 시간이 소요됩니다. (*30초 ~ 1분*)
- torch gpu버전을 설치한 후 gpu환경에서 작동하면 비교적 빠른 속도로 음성을 받아올 수 있습니다.


* * *


## 3. 서버 / DB
### 3.1 voice cloning 서버 - Fast API기반, Heroku로 배포(CPU * 1 / RAM : 512mb)
- 개별화된 목소리 서비스 제공을 위해 다음과 같은 서버로 요청 및 응답을 받고 있습니다. (https://github.com/queque5987/better-voice-cloning 참고)
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
