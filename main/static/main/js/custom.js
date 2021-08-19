let modal = new bootstrap.Modal(document.getElementById('createWallet'), {backdrop: 'static', keyboard: false})
const loader = document.querySelector('#loader')
const walletDetails = document.querySelector('#walletDetails')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
window.addEventListener('load', (event) => {
  $.ajax({
    type: 'GET',
    url: '/get-wallet/',
    beforeSend: function(){
      loader.style.display = ''
      walletDetails.innerHTML=''
    },
    success: function(data){
        walletDetail(data)
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
  if(c.currency.symbol){
    let div = document.createElement('div')
    div.id = `cc_${c.currency.code}`
    div.className = 'col-md-6 mt-3'
    div.innerHTML = `<div class="mt-3 mb-3">
                      <img src="data:image/png;base64, ${c.flag}" class="img-thumbnail">
                      <div>
                        <span>${c.currency.name}  ${c.currency.code} - ${c.currency.symbol}</span>
                      </div>
                     </div>`
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
  }
  
  // let spanNameDiv = document.createElement('div')
  // let span = document.createElement('span')
  // let textNode = document.createTextNode(text)
  // let img = document.createElement('img')
  // let spanRow = document.createElement('row')
  // let spanDiv = document.createElement('div')
  // div.className = 'col-md-6 mt-3'
  // div.id = `cc_${c.currency.code}`
  // span.className = 'text-input'
  // img.src = `data:image/png;base64, ${c.flag}`
  // span.appendChild(textNode)
  // spanDiv.appendChild(img)
  // spanDiv.appendChild(span)
  // spanRow.appendChild(spanDiv)
  // div.appendChild(spanRow)

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
    beforeSend: function(){
        loader.style.display = ''
        walletDetails.innerHTML=''
    },
    success: function(data){
        walletDetail(data)
    }
   })
  })
})

const walletDetail = (data) => {
      setTimeout(function(){
      loader.style.display = 'none'
      walletDetails.innerHTML=''
      let details = JSON.parse(data)
      details.forEach(detail => {
         let wdiv = document.createElement('div')
         wdiv.innerHTML = `<div class="d-flex justify-content-between">
                          <h6>Wallet Details</h6>
                          <div>
                            <button type="button" class="btn btn-outline-dark"><i class="far fa-edit"></i></button>
                            <button type="button" class="btn btn-outline-danger" id="deleteWallet" data-value="${detail.pk}"><i class="fas fa-minus-circle"></i></button>
                          </div>
                        </div>
                        <h4>${detail.fields.wallet_name}</h4>
                        <small class="font-weight-bold">${detail.fields.currency}</small>
                        <div>
                        </div>
                        <div class="form-check form-switch mt-3">
                          <input class="form-check-input" type="checkbox" id="freezeWallet" data-value="${detail.pk}" ${detail.fields.freeze ? 'checked' : ''}>
                          <label class="form-check-label font-weight-bold" for="freezeWallet">Freeze</label>
                        </div>
                        <div class="float-end mt-4">
                            <button type="button" class="float-right btn bg-gradient-dark btn-md">Adust Balance</button>
                        </div>
                        `
         walletDetails.appendChild(wdiv)
      })
    }, 1000)    
    freeze()
    dWallet()
}


const freezeWallet = () => {
  let promise = new Promise(function(resolve, reject) {
    setTimeout(() => {
      resolve(document.querySelector('#freezeWallet'))
    }, 1100);
  });
  return promise
}

async function freeze() {
  const result = await freezeWallet();
  result.addEventListener('click', () => {
    console.log(result.getAttribute('data-value'))
    const loaderFreeze = document.querySelector(`#loaderFreeze_${result.getAttribute('data-value')}`)
    const walletButton = document.querySelector(`#walletSubmit_${result.getAttribute('data-value')}`)
    let id = result.getAttribute('data-value')
    $.ajax({
      type: 'POST',
      url: '/my-wallet/freeze/',
      data:{id: id, freeze: result.checked, csrfmiddlewaretoken: csrftoken},
      beforeSend: function() {
        loaderFreeze.style.display = 'block'
        walletButton.style.display = 'none'
      },
      success: function(data) {
        setTimeout(function() {
          loaderFreeze.style.display = 'none'
          walletButton.style.display = ''
        },1000)
        
      }
    })
    if(result.checked){
      walletButton.classList.remove('btn-outline-success')
      walletButton.classList.add('btn-secondary')
    }else{
      walletButton.classList.remove('btn-secondary')
      walletButton.classList.add('btn-outline-success')
    }
  })
}

//delete
const deleteWallet = () => {
  let promise = new Promise(function(resolve, reject) {
    setTimeout(() => {
      resolve(document.querySelector('#deleteWallet'))
    }, 1100);
  });
  return promise
}

async function dWallet() {
  const result = await deleteWallet();
  result.addEventListener('click', () => {
    let id = result.getAttribute('data-value')
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.isConfirmed) {
        
        $.ajax({
          type: 'POST',
          url:'/my-wallet/delete/',
          data: {id: id, csrfmiddlewaretoken: csrftoken},
          success: function(data){
            Swal.fire(
             'Deleted!',
             'Your file has been deleted.',
             'success'
           )
          }
        })
      }
    })
  })
}


