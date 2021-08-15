const voiceAssistant = document.querySelector('#voiceAssistant')

voiceAssistant.addEventListener('click', (event)=>{
    voiceAssistant.text = 'Speak now'
    voiceAssistant.classList.remove('bg-gradient-dark');
    voiceAssistant.classList.add('bg-gradient-danger');
    const speech_recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new speech_recognition()
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let textResult = ''
  
    let speech = new SpeechSynthesisUtterance();

    speech.lang = "en-US";  
    
    let sound = document.querySelector('#myAudio')
    sound.play()
  

        if ('speechSynthesis' in window) {
            console.log('Speech recognition supported 😊');
            recognition.start();
            // This will run when the speech recognition service returns a result
            recognition.onstart = function() {
              console.log("Voice recognition started. Try speaking into the microphone.");
            };
            
            recognition.onresult = function(event) {
              textResult = event.results[0][0].transcript;
              $.ajax({
                  type: 'POST',
                  url: '/getdata/',
                  data: {textResult: textResult, csrfmiddlewaretoken: csrftoken},

                  success: function(data){
                    speech.text = data; 
                    speech.volume = 1;
                    speech.rate = 1;
                    speech.pitch = 1;      
                    window.speechSynthesis.speak(speech);
                    voiceAssistant.text = 'Click (Voice Assistant)'
                    voiceAssistant.classList.remove('bg-gradient-danger');
                    voiceAssistant.classList.add('bg-gradient-dark');
                  }
              })
              
            };

            recognition.error = function(event){
                alert(event.error)
            }

        } else {
            console.log('Speech recognition not supported 😢');
            // code to handle error
        }

})