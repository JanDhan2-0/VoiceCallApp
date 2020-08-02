# Age/Gender/Area
# Financial/Health.

import os
from flask import Flask,request
from twilio.twiml.voice_response import VoiceResponse,Gather
from twilio.rest import Client

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route("/makeACall/<phoneNo>",methods=['GET'])
def makeCall(phoneNo):
    account_sid = 'AC63307fff7d6088ec61dd563aa8974597'
    auth_token = '324512a5713e65838ddd88e6f93c054e'
    client = Client(account_sid, auth_token)
    toPhoneNo = '+91'+phoneNo
    try:
        call = client.calls.create(
                                url='https://jandhan2voice.herokuapp.com/answer',
                                to=toPhoneNo,
                                from_='+12054489824'
                            )
                            
        # print(call.sid)
        return "Success"
    except:
        return "Failure"


@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    resp = VoiceResponse()

    resp.say("जन धन दर्शन ऑनलाइन ग्राहक हेल्पलाइन में आपका स्वागत है", voice='Polly.Aditi',language="kn-IN")

    gather = Gather(num_digits=1, action='/gatherScheme')

    gather.say("वित्तीय योजनाओं के बारे में जानने के लिए, 1 दबाएँ.",voice='Polly.Aditi',language="hi-IN")
    gather.say("स्वास्थ्य संबंधी योजनाओं के बारे में जानने के लिए, 2 दबाएं.",voice='Polly.Aditi',language="hi-IN")
    resp.append(gather)

    resp.redirect('/voice')

    return str(resp)


@app.route('/gatherScheme', methods=['GET', 'POST'])
def gatherScheme():

    resp = VoiceResponse()

    if 'Digits' in request.values:
        # print(request.values)
        choice = request.values['Digits']

        if choice == '1':
            resp.say('वित्तीय योजनाओं को चुनने के लिए धन्यवाद',voice='Polly.Aditi',language="hi-IN")
            url = '/gatherStatus/'+choice
            gather = Gather(num_digits=1, action=url)

            gather.say("यदि आप शहरी भारत से हैं और पुरुष हैं, तो 1 दबाएँ.",voice='Polly.Aditi',language="hi-IN")
            gather.say("यदि आप शहरी भारत से हैं और महिला हैं, तो 2 दबाएँ.",voice='Polly.Aditi',language="hi-IN")
            gather.say("यदि आप ग्रामीण भारत से हैं और पुरुष हैं, तो 3 दबाएँ.",voice='Polly.Aditi',language="hi-IN")
            gather.say("यदि आप ग्रामीण भारत से हैं और महिला हैं, तो 4 दबाएँ.",voice='Polly.Aditi',language="hi-IN")
            resp.append(gather)

        elif choice == '2':
            resp.say('स्वास्थ्य योजनाओं को चुनने के लिए धन्यवाद',voice='Polly.Aditi',language="hi-IN")
            url = '/gatherStatus/'+choice
            gather = Gather(num_digits=1, action=url)
            
            gather.say("यदि आप शहरी भारत से हैं और पुरुष हैं, तो 1 दबाएँ.",voice='Polly.Aditi',language="hi-IN")
            gather.say("यदि आप शहरी भारत से हैं और महिला हैं, तो 2 दबाएँ.",voice='Polly.Aditi',language="hi-IN")
            gather.say("यदि आप ग्रामीण भारत से हैं और पुरुष हैं, तो 3 दबाएँ.",voice='Polly.Aditi',language="hi-IN")
            gather.say("यदि आप ग्रामीण भारत से हैं और महिला हैं, तो 4 दबाएँ.",voice='Polly.Aditi',language="hi-IN")
            
            resp.append(gather)
            
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, I don't understand that choice.")

    return str(resp)

@app.route('/gatherStatus/<schemeChoice>',methods=['GET', 'POST'])
def gatherStatus(schemeChoice):
    resp = VoiceResponse()

    if 'Digits' in request.values:
        resp.say("आपके चयन के लिए शुक्रिया.")
        print(request.values)
        statusChoice = request.values['Digits']

        url = '/gatherSchemeFinal/'+schemeChoice+'/'+statusChoice
        gather = Gather(num_digits=2, action=url)
        gather.say("आप कितने साल के है ?",voice='Polly.Aditi',language="hi-IN")
        resp.append(gather)
        return str(resp)

    resp.redirect('/gatherStatus/'+schemeChoice)

    return str(resp)

@app.route('/gatherSchemeFinal/<schemeChoice>/<statusChoice>',methods=['GET', 'POST'])
def gatherSchemeFinal(schemeChoice,statusChoice):
    resp = VoiceResponse()

    if 'Digits' in request.values:
        resp.say("आपके चयन के लिए शुक्रिया.")
        age = request.values['Digits']
        # print(schemeChoice,age,statusChoice)
        age = int(age)
        schemeChoice = int(schemeChoice)
        statusChoice = int(statusChoice)
        resp.say("ये 3 योजनाएं आपके लिए फायदेमंद हो सकती हैं.", voice='Polly.Aditi',language="hi-IN")
        if(schemeChoice == 1):
            if(statusChoice == 1):
                if(age < 60):
                    resp.say("1. प्रधान मंत्री जन धन योजना.", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. राष्ट्रीय माध्यमिक शिक्षा अभियान", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. अटल पेंशन योजना", voice='Polly.Aditi',language="hi-IN")
                else:
                    resp.say("1. अटल पेंशन योजना.", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. प्रधान मंत्री जन धन योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. अन्नपूर्णा योजना", voice='Polly.Aditi',language="hi-IN")

            elif(statusChoice == 2):

                if(age < 60):
                    resp.say("1. राष्ट्रीय माध्यमिक शिक्षा अभियान", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. केंद्रीय कल्याणी योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. प्रधान मंत्री जन धन योजना", voice='Polly.Aditi',language="hi-IN")


                else:
                    resp.say("1. अटल पेंशन योजना.", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. प्रधान मंत्री जन धन योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. अन्नपूर्णा योजना", voice='Polly.Aditi',language="hi-IN")

                    
            elif(statusChoice == 3):
                if(age < 60):
                    resp.say("1. प्रधान मंत्री जन धन योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. प्रधान मंत्री मुद्रा योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. प्रधान मंत्री जीवन ज्योति बीमा योजना", voice='Polly.Aditi',language="hi-IN")


                else:
                    resp.say("1. इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. प्रधान मंत्री वया वन्दना स्कीम", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. प्रधान मंत्री किसान पेंशन योजना", voice='Polly.Aditi',language="hi-IN")

                    
            elif(statusChoice == 4):

                if(age < 60):
                    resp.say("1. कर्मचारी योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. सेन्ट कल्याणी योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. भारतीय महिला बैंक", voice='Polly.Aditi',language="hi-IN")

                else:
                    resp.say("1. अन्नपूर्णा योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. इंदिरा गांधी राष्ट्रीय वृद्धावस्था पेंशन योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. प्रधान मंत्री किसान पेंशन योजना", voice='Polly.Aditi',language="hi-IN")

        
        elif(schemeChoice == 2):
            if(statusChoice == 1):

                if(age < 60):
                    resp.say("1. प्रधानमंत्री भारतीय जन औषधि परियोजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. प्रधानमंत्री जन आरोग्य योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. राष्ट्रीय स्वास्थ्य बीमा योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("4. आम आदमी बीमा योजना",voice='Polly.Aditi',language="hi-IN")
                else:
                    resp.say("1. प्रधानमंत्री भारतीय जन औषधि परियोजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. प्रधानमंत्री जन आरोग्य योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. राष्ट्रीय स्वास्थ्य बीमा योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("4. आम आदमी बीमा योजना",voice='Polly.Aditi',language="hi-IN")

                    
            elif(statusChoice == 2):

                if(age < 60):
                    resp.say("1. प्रधानमंत्री भारतीय जन औषधि परियोजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. प्रधानमंत्री जन आरोग्य योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. राष्ट्रीय स्वास्थ्य बीमा योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("4. आम आदमी बीमा योजना",voice='Polly.Aditi',language="hi-IN")


                else:
                    resp.say("1. प्रधानमंत्री भारतीय जन औषधि परियोजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. प्रधानमंत्री जन आरोग्य योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. राष्ट्रीय स्वास्थ्य बीमा योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("4. आम आदमी बीमा योजना",voice='Polly.Aditi',language="hi-IN")

                    
            elif(statusChoice == 3):

                if(age < 60):
                    resp.say("1. प्रधानमंत्री भारतीय जन औषधि परियोजना", voice='Polly.Aditi',language="hi-IN")    
                    resp.say("2. प्रधानमंत्री जन आरोग्य योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. राष्ट्रीय स्वास्थ्य बीमा योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("4. आम आदमी बीमा योजना",voice='Polly.Aditi',language="hi-IN")

                else:
                    resp.say("1. प्रधानमंत्री भारतीय जन औषधि परियोजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. प्रधानमंत्री जन आरोग्य योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. राष्ट्रीय स्वास्थ्य बीमा योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("4. आम आदमी बीमा योजना",voice='Polly.Aditi',language="hi-IN")
                    
            elif(statusChoice == 4):
                if(age < 60):
                    resp.say("1. प्रधानमंत्री भारतीय जन औषधि परियोजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. प्रधानमंत्री जन आरोग्य योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. राष्ट्रीय स्वास्थ्य बीमा योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("4. आम आदमी बीमा योजना",voice='Polly.Aditi',language="hi-IN")

                else:
                    resp.say("1. प्रधानमंत्री भारतीय जन औषधि परियोजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("2. प्रधानमंत्री जन आरोग्य योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("3. राष्ट्रीय स्वास्थ्य बीमा योजना", voice='Polly.Aditi',language="hi-IN")
                    resp.say("4. आम आदमी बीमा योजना",voice='Polly.Aditi',language="hi-IN")

    resp.say("हमसे संपर्क करने के लिए धन्यवाद",voice='Polly.Aditi',language="hi-IN")
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
