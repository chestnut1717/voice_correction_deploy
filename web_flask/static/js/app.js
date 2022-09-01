
//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream;              //stream from getUserMedia()
var rec;                    //Recorder.js object
var input;                  //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //new audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

window.onload = init;
var context;    // Audio context
var buf;        // Audio buffer

function init() {
if (!window.AudioContext) {
    if (!window.webkitAudioContext) {
        alert("Your browser does not support any AudioContext and cannot play back this audio.");
        return;
    }
        window.AudioContext = window.webkitAudioContext;
    }

    context = new AudioContext();
}

// Audio 파일 만드는 함수
function playByteArray(byteArray) {

    var arrayBuffer = new ArrayBuffer(byteArray.length);
    var bufferView = new Uint8Array(arrayBuffer);
    for (i = 0; i < byteArray.length; i++) {
      bufferView[i] = byteArray[i];
    }

    context.decodeAudioData(arrayBuffer, function(buffer) {
        buf = buffer;
        console.log(buf)
        play();
    });
}

// 녹음 시작 함수
function startRecording() {
  console.log("recordButton clicked");

  // Disable the record button until we get a success or fail from getUserMedia()
  recordButton.disabled = true;
  stopButton.disabled = false;

  navigator.mediaDevices.getUserMedia({audio: true, video: false}).then(function(stream) {
      console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

      audioContext = new AudioContext({sampleRate: 16000});

      // assign to gumStream for later use
      gumStream = stream;

      // use the stream
      input = audioContext.createMediaStreamSource(stream);

      // Create the Recorder object and configure to record mono sound (1 channel) Recording 2 channels will double the file size
      rec = new Recorder(input, {numChannels: 1})

      //start the recording process
      rec.record()

      console.log("Recording started");

  }).catch(function(err) {
      //enable the record button if getUserMedia() fails
      recordButton.disabled = false;
      stopButton.disabled = true;
  });
}

// 녹음 정지 함수
function stopRecording() {
  console.log("stopButton clicked");

  //disable the stop button, enable the record too allow for new recordings
  stopButton.disabled = true;
  recordButton.disabled = false;

  //tell the recorder to stop the recording
  rec.stop(); //stop microphone access
  gumStream.getAudioTracks()[0].stop();

  //create the wav blob and pass it on to createDownloadLink
  rec.exportWAV(createDownloadLink);



function createDownloadLink(blob) {
  var url = URL.createObjectURL(blob);
  var au = document.createElement('audio');


  //name of .wav file to use during upload and download (without extension)
  var filename = new Date().toISOString();

  //add controls to the <audio> element
  au.controls = true;
  au.src = url;

  //save to disk link

    /* button이 클릭되었을때 이벤트 */
    var data = new FormData();
    // form형식으로 음원파일 POST
    data.append('file', blob, 'filename');


    var xhr = new XMLHttpRequest();
    data.enctype='multipart/form-data';
    data.method='post';


    xhr.open('post','{{ request.path }}', true); 
    
    xhr.responseType = "json";

    // xhr.onreadystatechange = 콜백함수명;
    xhr.send(data);
    /* 통신에 사용 될 XMLHttpRequest 객체 정의 */
    /* httpRequest의 readyState가 변화했을때 함수 실행 */
      xhr.onreadystatechange = () => {
        /* readyState가 Done이고 응답 값이 200일 때, 받아온 response로 name과 age를 그려줌 */
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
            var result = xhr.response;
            console.log(result)
            // https://stackoverflow.com/questions/38926335/flask-redirecturl-for-returning-html-but-not-loading-page
            window.location = "/feedback";

            } else {
              alert('request에 뭔가 문제가 있어요.');
            }
      }
      };

      

  }


}

