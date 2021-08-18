let modal = new bootstrap.Modal(document.getElementById('createWallet'), {backdrop: 'static', keyboard: false})
window.addEventListener('load', (event) => {
  $.ajax({
    type: 'GET',
    url: '/get-wallet/',
    success: function(data){
      if(!data){
        modal.show()
      }
    }
  })
})

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


let currency = countries
let row = document.querySelector('#currency')

let search_input = document.getElementById('search');

let search_term = '';

const showCountries = () => {
  row.innerHTML = ''
  currency.filter(c => c.name.toLowerCase().includes(search_term.toLocaleLowerCase())
  ).forEach(c => {
  let text = ` ${c.currency.name}  ${c.currency.code} - ${c.currency.symbol}`
  let div = document.createElement('div')
  let spanNameDiv = document.createElement('div')
  let span = document.createElement('span')
  let textNode = document.createTextNode(text)
  let img = document.createElement('img')
  let spanRow = document.createElement('row')
  let spanDiv = document.createElement('div')
  div.className = 'col-md-6 mt-3'
  div.id = `cc_${c.currency.code}`
  span.className = 'text-input'
  img.src = `data:image/png;base64, ${c.flag}`
  span.appendChild(textNode)
  spanDiv.appendChild(img)
  spanDiv.appendChild(span)
  spanRow.appendChild(spanDiv)
  div.appendChild(spanRow)
  div.setAttribute('data-value', `${c.currency.code}-${c.currency.symbol}`)
  div.addEventListener("mouseover", function( event ) {
    // highlight the mouseover target
    event.target.style.cursor = "pointer"
    event.target.style.backgroundColor = "#dff9fb";
  
    // reset the color after a short delay
    div.addEventListener("mouseleave", function() {
      event.target.style.backgroundColor = "";
    }, false);
  }, false);

  row.appendChild(div)
})
}

let currencyModal = new bootstrap.Modal(document.getElementById('currencyModal'))
let id_currency = document.querySelector('#id_currency')
id_currency.addEventListener('click', function() {
  search_input.value = ''
  currencyModal.show()
  search_term = ''
  showCountries(); 
  currencyCodeValue();
})


const showCountriesFilter = () => {search_input.addEventListener('keyup', e => {
    search_term = e.target.value
    showCountries(); 
    currencyCodeValue();
});
}
showCountriesFilter()

//Getting Currency Value
const currencyCodeValue = () => {
  let currencyCode = document.querySelectorAll("div[id^='cc_']");
  currencyCode.forEach(div => {
  div.addEventListener('click', function() {
    id_currency.value = div.getAttribute('data-value')
    currencyModal.hide()
  })
})
}


const walletId = document.getElementById('walletId')
const wallet = document.querySelectorAll('[id^="walletSubmit"]')
wallet.forEach(w => {
  w.addEventListener('click', function(e){
    e.preventDefault();
  let csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
  let id =  w.getAttribute('data-value')
  console.log(id)
  $.ajax({
    type:'POST',
    url: walletId.getAttribute('action'),
    data: {
       id: id,
       csrfmiddlewaretoken: csrf_token
      },
    success: function(data){
        const walletDetails = document.querySelector('#walletDetails')
        walletDetails.innerHTML=''
        let details = JSON.parse(data)
        details.forEach(detail => {
           let tr = document.createElement('tr')
           let td = document.createElement('td')
           td.innerHTML = `<h4>${detail.fields.wallet_name}</h4>
                          <small class="font-weight-bold">${detail.fields.currency}</small>
                          `
           tr.appendChild(td)
           walletDetails.appendChild(tr)
        })
        
    }
   })
  })
})


