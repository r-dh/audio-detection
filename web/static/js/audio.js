 //document.getElementById('fileInput').addEventListener('change', handleFileSelect, false);

$("#fileInput").on("change", function(e){
    console.log("changed")
    console.log(e)

});

async function sendData(url, data) {
  const formData  = new FormData();

  for(const name in data) {
    formData.append(name, data[name]);
  }

  const response = await fetch(url, {
    method: 'POST',
    body: formData
  });

  // ...
}


var wavesurfer = WaveSurfer.create({
    progressColor: '#52d9a0',
    container: '#waveform',
    hideScrollbar: true,
    normalize: true,
    plugins: [
            WaveSurfer.regions.create({})
        ]
});

wavesurfer.load('./static/audio_samples/sword1.wav');

wavesurfer.on('ready', function () {
    wavesurfer.play();
    r1 = wavesurfer.addRegion({"start": 0.01, "end":0.3, "color": "rgba(255, 87, 51, 0.3)", "drag": false, "resize": false})
    r2 = wavesurfer.addRegion({"start": 1.9, "end":3, "color": "rgba( 255, 195, 0, 0.3)", "drag": false, "resize": false})
});

$('#audio-duration').text(wavesurfer.getDuration());

wavesurfer.getCurrentTime() 


function get_analysis()