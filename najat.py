# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, request
#import json
#import requests
import najat_nltk as nj
from Credentials import *
#import sys,os



      
questions, answers = nj.read_yaml(dir_path)



app= Flask(__name__)


@app.route('/webhooks', methods=['GET'])
def verify_webhook():
    mode =request.args.get("hub.mode")
    token= request.args.get("hub.verify_token")
    challenge=request.args["hub.challenge"]
    if mode and challenge: 
        if mode == "subscribe" and token==WEBHOOK_TOKEN:
               return str(challenge), '200'  #success
        else:
               return '403'  #Verification token mismatch
           
@app.route('/', methods=['POST'])
def post_message():
    data=request.json
    nj.log(data)
    if data["object"]== "page":
        messaging_event=data['entry'][0]['messaging']
        for msg in messaging_event:
                UserId=msg['sender']['id']
                if ('postback' in msg):
                    if (msg['postback']['title']=="Get Started"):
                        nj.get_started_quick_reply(UserId)
                        return "ok", 200
                    elif(msg['postback']['payload']=="num"):
                        nj.send_fb_quick_reply_emergencies_numbers(UserId)
                        return "ok", 200
                    elif(msg['postback']['payload']=="8350"):
                        nj.call_button(UserId)
                        return "ok", 200
                    elif(msg['postback']['payload']=="appli"):
                        nj.send_fb_quick_reply_android_ios(UserId)
                        return "ok", 200
                        
                elif('message' in msg):
                    if ('quick_reply' in msg['message']):
                        if(msg['message']['quick_reply']['payload']=="police"):
                            nj.call_button(UserId,'police')
                            return "ok", 200
                        elif(msg['message']['quick_reply']['payload']=="gendramerie"):
                            nj.call_button(UserId,'gendramerie')
                            return "ok", 200
                        elif(msg['message']['quick_reply']['payload']=="urg_pomp"):
                            nj.call_button(UserId,'urg_pomp')
                            return "ok", 200
                        elif(msg['message']['quick_reply']['payload']=="num"):
                            nj.send_fb_quick_reply_emergencies_numbers(UserId)
                        elif(msg['message']['quick_reply']['payload']=="appli"):
                            nj.send_fb_quick_reply_android_ios(UserId)
                            return "ok", 200
                        elif(msg['message']['quick_reply']['payload']=="8350"): 
                            nj.call_button(UserId,'8350')
                            return "ok", 200 
                        else:
                            UserId=msg['sender']['id']
                            userText=msg['message']['text']
                            #my ID: 2869295273124268
                            najat_response=str(nj.response(UserId,userText,questions, answers))
                        nj.send_najat_message(UserId,najat_response)  
                            
                    else:
                        UserId=msg['sender']['id']
                        userText=msg['message']['text']
                        #my ID: 2869295273124268
                        najat_response=str(nj.response(UserId,userText, questions, answers))
                        nj.send_najat_message(UserId,najat_response)  
        return "ok", 200
      
 
        
if __name__ == "__main__":
    app.run()