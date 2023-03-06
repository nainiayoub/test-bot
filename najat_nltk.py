# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:21:31 2020

@author: Jihad
"""

import os
import sys
import requests
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random
import yaml
import re
from emoji import UNICODE_EMOJI
from Credentials import *

def is_emoji(s):
    return s in UNICODE_EMOJI

def read_yaml(dir_path):
    files_list = os.listdir(dir_path + os.sep)
    questions = list()
    answers = list()
    for filepath in files_list:
        stream = open( dir_path + os.sep + filepath , 'rb')
        docs = yaml.safe_load(stream)
        conversations = docs['conversations']
        for con in conversations:
            if len( con ) > 1 :
                questions.append(con[0])
                replies = con[ 1 : ]
                temp=list()
                for rep in replies:
                    temp.append(rep)
                answers.append( temp )
            elif len( con )> 1:
                questions.append(con[0])
                answers.append(con[1])
    return questions, answers



def response(sender_id,user_response, questions, answers):
    najat_response=''
    log(user_response)
    #####Intents######
    thanks=['شكرا','شكر','الله يحفضك','شكرن','يحفضك']
    goodbyes=['بسلامة','تهلاي','باي باي','باي','إلى اللقاء ']
    affirmation=['وخا','واخا','واخ']
    pattern_laugh= re.compile("[هه]+")

    if all(is_emoji(e) for e in user_response):
        najat_response= ':)'  
    elif (pattern_laugh.fullmatch(user_response) is not None):
            najat_response=':)'
    elif  any(e in user_response for e in thanks):
             najat_response= " لا شكر على واجب"
    elif any(e in user_response for e in goodbyes):
            najat_response= " بسلامة :)"   
    elif (user_response in affirmation):
             najat_response= " :)  "
    else:
           
        dont_know_quick_reply(sender_id,answers,questions)
                   # return "ok", 200
        return najat_response


def get_started_quick_reply(sender_id):
    """This function sends quick reply"""
    headers={ 
            "Content-type": "application/json"
                }
    data = json.dumps({
              "recipient":{"id": sender_id},
              "messaging_type": "RESPONSE",
              "message":{
              "text": "مرحباً:)، كيفاش يمكن لي نعاونك ؟" ,
              "quick_replies":[
                      {
                    "content_type":"text",
                    "title": "8350 اتصلي",
                    "payload": "plateforme"
                },
                {
                    "content_type":"text",
                      "title": "شكاية مستعجلة",
                    "payload": "appli"
                },
                {
                    "content_type":"text",
                    "title": "أرقام الطوارئ",
                    "payload": "num"
                
                }
                  ]
              }})

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        GRAPH_API_URL,
        params=params,
        headers= headers,
        data=data
    )

    if response.status_code !=200:
        log(response.status_code)
    log(response.text)
    return response.content
    

def dont_know_quick_reply(sender_id,answers,questions):
    """This function sends quick reply"""
    headers={ 
            "Content-type": "application/json"
                }
    data = json.dumps({
              "recipient":{"id": sender_id},
              "messaging_type": "RESPONSE",
              "message":{
              "text": random.choice(answers[questions.index('oov')]),
              "quick_replies":[
                      {
                    "content_type":"text",
                    "title": "8350 اتصلي",
                    "payload": "plateforme"
                },
                {
                    "content_type":"text",
                      "title": "شكاية مستعجلة",
                    "payload": "appli"
                },
                {
                    "content_type":"text",
                    "title": "أرقام الطوارئ",
                    "payload": "num"
                
                }
                  ]
              }})

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    persistent_menu = {
      "persistent_menu": [
        {
            "locale": "default",
            "composer_input_disabled": true,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "منصة 8350",
                    "payload": "8350"
                },
                {
                    "type": "postback",
                      "title": "شكاية مستعجلة",
                    "payload": "appli"
                },
                {
                    "type": "postback",
                    "title": "أرقام الطوارئ",
                    "payload": "num"
                
                },
				{
                    "type": "postback",
                    "title": "شنو هو العنف أصلاً؟",
                    "payload": "violence"
                
                },
				{
                    "type": "postback",
                    "title": "تعلم و تمكين",
                    "payload": "learn"
                
                },
				{
                    "type": "postback",
                    "title": "عمل و مقاولة",
                    "payload": "work"
                
                },
				{
                    "type": "postback",
                    "title": "معلومات إضافية",
                    "payload": "else"
                
                }
            ]
        }
    ]
    }

    response = requests.post(
        GRAPH_API_URL,
        params=params,
        headers= headers,
        data=persistent_menu
    )

    if response.status_code !=200:
        log(response.status_code)
    log(response.text)
    return response.content

def call_button(sender_id, service):
    numbers={"8350":"8350","police":"19","gendramerie":"177","urg_pomp":"15"}
    texts= {"8350":"إذا اتصلتي بمنصة 8350 غتجاوبك مرشدة إجتماعية و غاتقدم لك المساعدة على حساب المشكل لي عندك","police":"رقم الشرطة","gendramerie":"رقم الدرك الملكي","urg_pomp":"رقم  الإسعاف أو المطافئ"}
    """This function sets call button"""
    headers={ 
            "Content-type": "application/json"
                }
    data = json.dumps({
        "recipient":{"id":sender_id
      },
      "message":{
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"button",
            "text":texts[service],
            "buttons":[
              {
                "type":"phone_number",
                "title":"اتصلي",
                "payload":numbers[service]
              }
            ]
          }
        }
      }
})

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        GRAPH_API_URL,
        params=params,
        headers= headers,
        data=data
    )

    if response.status_code !=200:
        log(response.status_code)
    log(response.text)
    return response.content

def send_fb_quick_reply_android_ios(sender_id):
    """This function sends quick reply"""
    headers={ 
            "Content-type": "application/json"
                }
    data = json.dumps({
              "recipient":{"id": sender_id},
              "messaging_type": "RESPONSE",
              "message":{
              "text": "الى عندك أيفون (Iphone) اختاري ios و إلى عندك شي تليفون آخر اختاري android",
              "quick_replies":[  
                      {
                    "content_type":"text",
                    "title":"android",
                    "payload":"android"
                  },
                         
                {
                    "content_type":"text",
                    "title":"ios",
                    "payload":"ios"
                
                  }
                          
                ]
              }})

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        GRAPH_API_URL,
        params=params,
        headers= headers,
        data=data
    )

    if response.status_code !=200:
        log(response.status_code)
    log(response.text)
    return response.content

def send_fb_quick_reply_emergencies_numbers(sender_id):
    """This function sends quick reply"""
    headers={ 
            "Content-type": "application/json"
                }
    data = json.dumps({
              "recipient":{"id": sender_id},
              "messaging_type": "RESPONSE",
              "message":{
              "text": "شنو الرقم لي محتاجة؟",
              "quick_replies":[  
                      {
                    "content_type":"text",
                    "title":"الشرطة",
                    "payload":"police"
                
                  },
                         
                {
                    "content_type":"text",
                    "title":"الدرك الملكي",
                    "payload":"gendarmerie"
                
                  },
                    {
                    "content_type":"text",
                    "title":" الإسعاف أو المطافئ",
                    "payload":"urg_pomp"
                
                  }
                          
                          
                ]
              }})

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        GRAPH_API_URL,
        params=params,
        headers= headers,
        data=data
    )

    if response.status_code !=200:
        log(response.status_code)
    log(response.text)
    return response.content
    
def send_fb_quick_reply(sender_id):
    """This function sends quick reply"""
    headers={ 
            "Content-type": "application/json"
                }
    data = json.dumps({
              "recipient":{"id": sender_id},
              "messaging_type": "RESPONSE",
              "message":{
              "text": "شنو هي أقرب مدينة ليك؟",
              "quick_replies":[
                     # {
                    #"content_type":"text",
                    #"title":"تطوان",
                    #"payload":"Tetouan"
                
                  #},  
                      {
                    "content_type":"text",
                    "title":"طنجة",
                    "payload":"Tanger"
                
                  },
                         
                {
                    "content_type":"text",
                    "title":"العرائش",
                    "payload":"Larache"
                
                  },
                    {
                    "content_type":"text",
                    "title":"القنيطرة",
                    "payload":"Kenitra"
                
                  },
                  {
                    "content_type":"text",
                    "title":"الرباط",
                    "payload":"Rabat"
                
                  },
                          #{
                    #"content_type":"text",
                    #"title":"مكناس",
                    #"payload":"Meknes"
                    
                 
                     #     {
                    #"content_type":"text",
                    #"title":"فاس",
                    #"payload":"Fes"
                
                  #},
                          { 
            	  "content_type":"text",
                  "title":"الدار البيضاء",
                  "payload":"casa"
                    
                  },     {
                    "content_type":"text",
                    "title":"سطات",
                    "payload":"Settat"
                
                  },{
                    "content_type":"text",
                    "title":"اسفي",
                    "payload":"safi"
                    
                  },{
                    "content_type":"text",
                    "title":"مراكش",
                    "payload":"kech"
                    
                  },{
                    "content_type":"text",
                    "title":"أكادير",
                    "payload":"Agadir"
                    
                  },#,{
                   # "content_type":"text",
                   # "title":"الرشيدية",
                   # "payload":"Rachidiya"
                    
                 # },
                  {
                    "content_type":"text",
                    "title":"مدينة أخرى",
                    "payload":"other"
                    
                  }
                          
                          
                          
                ]
              }})

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        GRAPH_API_URL,
        params=params,
        headers= headers,
        data=data
    )

    if response.status_code !=200:
        log(response.status_code)
    log(response.text)
    return response.content
    

def send_najat_message(userid, text):
    """Send a response to Facebook"""
    headers={ 
            "Content-type": "application/json"
                }
    data =json.dumps({     
            "message": {"text": text },
            "recipient": {"id": userid}
            })

    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        GRAPH_API_URL,
        params=params,
        headers= headers,
        data=data
    )
    if response.status_code !=200:
        log(response.status_code)
    log(response.text)
    
    
def log(message):
    print(str(message))
    sys.stdout.flush()

#def response_1(user_response, count_vect,questions_count, questions, answers,intent_count):
#    najat_response=''
#    context={'legal':0,'psy':0,'ngo':0}#

#    if(user_response in affrimative):
#        if context =='legal':
 #"           .....
#        elif context =='psy':
#            ....
#        elif context =='ngo'
    
    
#    print(user_response)
#    thanks=['شكرا','بسلامة','تهلاي','']
#    if(user_response in thanks):
#         najat_response= " :) نجاة: بسلامة"
#    elif user_response.startswith('كلهم'): 
#         najat_response=  '?' +' علاش كتقولي'+ ' '+ user_response 
#    elif user_response.startswith(('لأن' ,'حيت','لان','بحيت','حيتاش' )): 
#         najat_response= 'تقدر تكون هادي هي الحقيقة وربما غير كايبان ليك' 
#    else:
#        user_response_pre= f.remove_stop_words(user_response)
        
  