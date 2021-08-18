from main.forms import BudgetForm, BillsPaymentsForm, WalletForm
import speech_recognition as sr
import pyttsx3
from main.models import Budget, BillsPayments
from django.db.models import Sum


r = sr.Recognizer()
r.energy_threshold = 4000
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 145)

def wallet(request):
    wallet_form = WalletForm()

    return {'wallet_form': wallet_form}

    
def set_budget(request):
    budget_form = BudgetForm()

    return {'budget_form': budget_form}

def add_transaction(request):
    transaction_form = BillsPaymentsForm()

    return {'transaction_form': transaction_form}

# def record_audio():
#     with sr.Microphone() as source:
#         print('Say something')
#         voice_data = ''
#         try:
#             audio = r.listen(source)
#             voice_data = r.recognize_google(audio)
#         except sr.UnknownValueError:
#             voice_data = 'Sorry, I did not get that'
#         except sr.RequestError:
#             voice_data = 'Sorry, my speech service is down'

#         return voice_data

# def respond(voice_data):
#     response = ''
#     if 'hey' in voice_data:
#         response = 'My name is Marks'
#     if 'budget for this month' in voice_data:
#         data = Budget.objects.get(month='8-2021')
#         response = f"You're current budget for this month is {data}"
#     if 'breakdown of expenses for this month' in voice_data:
#         data = BillsPayments.objects.values('category').filter(expense_date__istartswith='2021-08').annotate(total=Sum('amount')).order_by('-total')
#         for d in data:
#             response+=f"Category: {d.get('category')} Total: {d.get('total')}, "


#     return response

# def lexi_speech(audio_string):
#     engine.say(audio_string)
#     engine.runAndWait()

# def speech_recognition(request):
#     # time.sleep(1)
#     # while 1:
#     voice_data = record_audio()
#     response = respond(voice_data)
#     lexi_speech(response)
    
#     return {'voice_data': response}
