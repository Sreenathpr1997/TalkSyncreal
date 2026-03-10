let socket = null
let audioContext = null
let processor = null
let input = null
let stream = null


document.getElementById("startBtn").onclick = startRecording
document.getElementById("stopBtn").onclick = stopRecording


function startRecording(){

    console.log("Starting recording...")

    socket = new WebSocket("ws://localhost:8000/stream")

    socket.binaryType = "arraybuffer"

    socket.onopen = () => {
        console.log("WebSocket connected")
    }

    socket.onmessage = (event) => {

        // TEXT RESPONSE
        if(typeof event.data === "string"){

            const data = JSON.parse(event.data)

            document.getElementById("english").innerText =
                "English: " + data.english

            document.getElementById("hindi").innerText =
                "Hindi: " + data.hindi

            document.getElementById("punjabi").innerText =
                "Punjabi: " + data.punjabi
        }

        // AUDIO RESPONSE
        else{

            const blob = new Blob([event.data], {type:"audio/mp3"})

            const url = URL.createObjectURL(blob)

            const audio = new Audio(url)

            audio.play()
        }

    }


    navigator.mediaDevices.getUserMedia({audio:true})
    .then(s => {

        stream = s

        audioContext = new AudioContext({sampleRate:16000})

        input = audioContext.createMediaStreamSource(stream)

        processor = audioContext.createScriptProcessor(4096,1,1)

        input.connect(processor)
        processor.connect(audioContext.destination)

        processor.onaudioprocess = (event)=>{

            if(!socket || socket.readyState !== WebSocket.OPEN){
                return
            }

            const inputData = event.inputBuffer.getChannelData(0)

            const pcmData = new Int16Array(inputData.length)

            for(let i=0;i<inputData.length;i++){
                pcmData[i] = inputData[i] * 32767
            }

            socket.send(pcmData.buffer)

        }

    })

}


function stopRecording(){

    console.log("Stopping recording")

    if(processor) processor.disconnect()
    if(input) input.disconnect()

    if(audioContext) audioContext.close()

    if(stream){
        stream.getTracks().forEach(track => track.stop())
    }

    if(socket){
        socket.close()
    }

}