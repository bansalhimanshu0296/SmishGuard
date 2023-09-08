from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status
import json
from smishguard.settings import BASE_DIR
import pickle
from urlextract import URLExtract
import pandas as pd
import string

from urllib.parse import urlparse,urlencode
import ipaddress
import re
def getDomain(url):  
  domain = urlparse(url).netloc
  if re.match(r"^www.",domain):
	       domain = domain.replace("www.","")
  return domain

def havingIP(url):
  try:
    ipaddress.ip_address(url)
    ip = 1
  except:
    ip = 0
  return ip

def haveAtSign(url):
  if "@" in url:
    at = 1    
  else:
    at = 0    
  return at

def getLength(url):
  if len(url) < 54:
    length = 0            
  else:
    length = 1            
  return length

def getDepth(url):
  s = urlparse(url).path.split('/')
  depth = 0
  for j in range(len(s)):
    if len(s[j]) != 0:
      depth = depth+1
  return depth

def redirection(url):
  pos = url.rfind('//')
  if pos > 6:
    if pos > 7:
      return 1
    else:
      return 0
  else:
    return 0

def httpDomain(url):
  domain = urlparse(url).netloc
  if 'https' in domain:
    return 1
  else:
    return 0

shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"
def tinyURL(url):
    match=re.search(shortening_services,url)
    if match:
        return 1
    else:
        return 0
def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1            # phishing
    else:
        return 0            # legitimate

import re
from bs4 import BeautifulSoup
import whois
import urllib
import urllib.request
from datetime import datetime
def web_traffic(url):
  try:
    #Filling the whitespaces in the URL if any
    url = urllib.parse.quote(url)
    rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
    rank = int(rank)
  except TypeError:
        return 1
  if rank <100000:
    return 1
  else:
    return 0
def domainAge(domain_name):
  creation_date = domain_name.creation_date
  expiration_date = domain_name.expiration_date
  if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
    try:
      creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      return 1
  if ((expiration_date is None) or (creation_date is None)):
      return 1
  elif ((type(expiration_date) is list) or (type(creation_date) is list)):
      return 1
  else:
    ageofdomain = abs((expiration_date - creation_date).days)
    if ((ageofdomain/30) < 6):
      age = 1
    else:
      age = 0
  return age
# 14.End time of domain: The difference between termination time and current time (Domain_End) 
def domainEnd(domain_name):
  expiration_date = domain_name.expiration_date
  if isinstance(expiration_date,str):
    try:
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      return 1
  if (expiration_date is None):
      return 1
  elif (type(expiration_date) is list):
      return 1
  else:
    today = datetime.now()
    end = abs((expiration_date - today).days)
    if ((end/30) < 6):
      end = 0
    else:
      end = 1
  return end
import requests
# 15. IFrame Redirection (iFrame)
def iframe(response):
  if response == "":
      return 1
  else:
      if re.findall(r"[<iframe>|<frameBorder>]", response.text):
          return 0
      else:
          return 1
# 16.Checks the effect of mouse over on status bar (Mouse_Over)
def mouseOver(response): 
  if response == "" :
    return 1
  else:
    if re.findall("<script>.+onmouseover.+</script>", response.text):
      return 1
    else:
      return 0
# 17.Checks the status of the right click attribute (Right_Click)
def rightClick(response):
  if response == "":
    return 1
  else:
    if re.findall(r"event.button ?== ?2", response.text):
      return 0
    else:
      return 1

# 18.Checks the number of forwardings (Web_Forwards)    
def forwarding(response):
  if response == "":
    return 1
  else:
    if len(response.history) <= 2:
      return 0
    else:
      return 1
def featureExtraction(url,label):

  features = []
  #Address bar based features (10)
  features.append(getDomain(url))
  features.append(havingIP(url))
  features.append(haveAtSign(url))
  features.append(getLength(url))
  features.append(getDepth(url))
  features.append(redirection(url))
  features.append(httpDomain(url))
  features.append(tinyURL(url))
  features.append(prefixSuffix(url))
  
  #Domain based features (4)
  dns = 0
  try:
    domain_name = whois.whois(urlparse(url).netloc)
  except:
    dns = 1

  features.append(dns)
  features.append(web_traffic(url))
  features.append(1 if dns == 1 else domainAge(domain_name))
  features.append(1 if dns == 1 else domainEnd(domain_name))
  
  # HTML & Javascript based features (4)
  try:
    response = requests.get(url)
  except:
    response = ""
  features.append(iframe(response))
  features.append(mouseOver(response))
  features.append(rightClick(response))
  features.append(forwarding(response))
  features.append(label)
  
  return features

def find_url(text):
    extractor = URLExtract()
    urls = extractor.find_urls(text)
    result_list = []
    for url in urls:
       text = text.replace(url, "")
    return urls

# Create your views here.
class Test_Api(APIView):
    def post(self, request):
        #retrieve information from request 
        try:
            name = request.data["name"]

            response_dict = {
                    "status": "OK",
                    "message": "Hello " + name
                }
            response = JsonResponse(response_dict, safe=False)
        except:
            response_dict = {
                    "status": "ERROR",
                    "message": "System Backend Error"
                }
            response = JsonResponse(response_dict, safe=False)

        return response

class Analyze_Text(APIView):
    def post(self, request):
        #retrieve information from request 
        try:
            text = request.data["text"]

            text_model_name = "TextClassifier.pickle.dat"
            url_model_name = "URLClassifier.pickle.dat"
            vectorizer_model_name = "TextVectorizer.pickle.dat"

            models_dir = str(BASE_DIR) + "/backend/models/"

            with open(models_dir + 'words.json') as json_file:
                words_data = json.load(json_file)


            #URL Processing
            url_list = find_url(text)

            if not len(url_list) == 0:
              phish_features = []
              for url in url_list:
                  phish_features.append(featureExtraction(url,0))

              feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth','Redirection', 
                                  'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic', 
                                  'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over','Right_Click', 'Web_Forwards', 'Label']

              phishing = pd.DataFrame(phish_features, columns=feature_names)
              y = phishing['Label']
              X = phishing.drop('Label',axis=1)
              X = X.drop('Domain',axis=1)

              url_model = pickle.load(open(models_dir + url_model_name, "rb"))

              url_result = url_model.predict(X)

              url_result_dict = []

              url_smish_flag = False
              for i in range(len(url_list)):
                  if url_result[i] == 0:
                      url_class = "ham"
                  else:
                      url_class = "smish"
                      url_smish_flag = True

                  url_result_dict.append({"url": url_list[i], "result": url_class})
            else:
              url_result_dict = []
              url_smish_flag = False

            #Text Processing
            temp_text = text
            for url in url_list:
                temp_text = temp_text.replace(url,"")
            temp_text = temp_text.lower()

            vectorizer_model = pickle.load(open(models_dir + vectorizer_model_name, "rb"))
            text_li = [temp_text]
            integers = vectorizer_model.transform(text_li)

            text_model = pickle.load(open(models_dir + text_model_name, "rb"))
            text_result = text_model.predict(integers)

            text_smish_flag = False
            text_class = text_result[0]
            if not text_class == "ham":
              text_smish_flag = True

            words_li = []
            translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
            temp_str = temp_text.translate(translator)
            temp_str = " ".join(temp_str.split())

            temp_words_li = temp_str.split(" ")
            for word in temp_words_li:
                try:
                    value = words_data[word]
                    if value > -9.5:
                        words_li.append(word)
                except:
                    garbage_text = "hey"

            if url_smish_flag:
              result_label = "smish"
            else:
              if text_smish_flag:
                result_label = "smish"
              else:
                result_label = "ham"

            response_dict = {
                    "status": "OK",
                    "result": result_label,
                    "data": {"inputText": text, "urlResult": url_result_dict, "textResult": text_class, "words": words_li}
                }
            response = JsonResponse(response_dict, safe=False)
        except:
            response_dict = {
                    "status": "ERROR",
                    "message": "System Backend Error"
                }
            response = JsonResponse(response_dict, safe=False)
            raise

        return response