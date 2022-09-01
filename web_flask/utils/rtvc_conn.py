import requests
import json
import numpy as np

url1 = "https://better-encoder.herokuapp.com/inference/"
url2 = "https://better-synthesizer.herokuapp.com/inference/"
url3 = "https://better-vocoder.herokuapp.com/inference/"
url4 = "https://better-synthesizer.herokuapp.com/inference/"

url_list = [url1, url2, url3, url4]


headers = {
    'Content-Type': 'application/json'
}

# real-time voice cloning 담당 서버를 단순히 요청해서 미리 깨워주는 역할
## heroku를 기반으로 무료로 배포하면, 30분 사용하지 않을 경우 자동으로 서버가 유휴상태가 되버리기 때문에 방지
def wake_server():
    for _url in url_list:
        try:
            response = requests.request("GET", _url, headers=headers)

        except:
            print(_url, response)
            continue
        print(_url, response)

# 맞춤형 사용자 목소리 얻는 함수
## 서버 한계상, 각 서버마다 encoder, synthesizer, vocoder 각각 역할별로 분산해서 배포했기 때문에 순서대로 요청하는 함수
def get_wav(wav, sr, text):
    wav = wav.tolist()
    # print("\n\n-----\n{}\n\n-----\n\n".format(type(wav)))
    wav_json = json.dumps({
        "wav": wav,
        "sr": sr,
        "text": text
    })
  

    # encoder -> syn
    response1 = requests.request("POST", url1, headers=headers, data=wav_json)
    print(response1)
    print('response1 완료')
    embed = dict(eval(response1.json()))
    encoder_request_data = json.dumps({
        "embed": embed['embed'],
        "text": text
    })

    #syn -> vocoder
    response2 = requests.request("POST", url2, headers=headers, data=encoder_request_data)
    print(response2)
    print('response2 완료')

    spec = dict(eval(response2.json()))
    vocoder_request_data = json.dumps({
        "spec": spec['spec'],
        "sr": sr
    })

    # vocoder -> wav
    response3 = requests.request("POST", url3, headers=headers, data=vocoder_request_data)
    print(response3)
    print("response3 완료")


    # conn = mysql_connect()
    # wav_list = conn.get_wav()
    wav_list = eval(response3.json())['wav']


    wav = np.array(wav_list)
    sr = 16000
    return wav, sr