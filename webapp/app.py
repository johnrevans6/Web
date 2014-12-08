from gevent import monkey
monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room
import unirest

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'KoDiNg'
socketio = SocketIO(app)
thread = None

def background_thread():
    count = 0
    while True:
        time.sleep(10)
        count += 1
      
@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.start()
    return render_template('chatter.html')


@socketio.on('event', namespace='/service')
def receive_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('response',
         {'data': message['data'],'count': session['receive_count']})


@socketio.on('broadcast event', namespace='/service')
def send_message(message):


    text=message['data']

    text=text.replace(' ','+') 
    
    if message['language']=='Language' or message['language']=='English':
      lang_code='en-us'
    elif message['language']=='French':
      lang_code='fr-fr'
    elif message['language']=='Spanish':
      lang_code='es-es'
    elif message['language']=='German':
      lang_code='de-de'
    elif message['language']=='Italian':
      lang_code='it-it'
    elif message['language']=='Yoda':
      lang_code='yo'

    #Saddly, the Yoda Speak endpoint doesn't always respond
    if lang_code=='yo':           
      response = unirest.get('https://yoda.p.mashape.com/yoda?sentence='+text,
        headers={
          "X-Mashape-Key": "i3E3o4Tc19mshcKgoENuEr2SoqFGp1OMEjCjsnJjLmVROkf3iu"
        }
      )
      response=response.body          
    else:
      secret_key='3f6f5fe73b75454545492fb2aa60f7a7'
      public_key='xGz9WjknDmcJHd62LRtr'     
      response = unirest.get('https://community-onehourtranslation.p.mashape.com/mt/translate/text?public_key='+public_key+'&secret_key='+secret_key+'&source_content='
        +text+'&source_language=en-us&target_language='+lang_code,
        headers={
          "X-Mashape-Key": "i3E3o4Tc19mshcKgoENuEr2SoqFGp1OMEjCjsnJjLmVROkf3iu"
        }
      )

      response=response.body['results']
      response=response['TranslatedText']
      
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('response',
         {'data': response,'count': session['receive_count']},
         broadcast=True)


@socketio.on('disconnect', namespace='/service')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
