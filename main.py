import string
from turtle import ht
from typing import Union
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

import requests
from datetime import date

app = FastAPI()

def AxiosGenerateTemplate(url):
    today = date.today()
    today = today.strftime("%d %B, %Y")
    today = today + " \n"

    # url = "https://swarajyamag.com/api/v1/stories/286a29af-cf8e-4a61-9f08-7ddc71f798b4"
    url = "https://swarajyamag.com/api/v1/stories/" + url
    r = requests.get(url)
    response = r.json()
    storycards = response['story']['cards']

    CardParameters = []

    ArticleURL = response['story']['url']
    ArticleURL = ArticleURL + ""

    for element in storycards:
        Title = element['story-elements'][0]['text']
        Title = Title.replace("<a ", '<a style="color: #ce4242; text-decoration: none;" ')
        Title = Title.replace('<strong>','<strong style="color: #ce4242">')
        Title = Title.replace("<ins>",'<ins style="text-decoration: none;">')
        Title  =Title.replace("<p>",'<p style="color: #ce4242">')
        totalsize = len(element['story-elements'])
        Content = ""
        ImageCaption = element['metadata']['social-share']['image']['caption']
        ImageURL = element['metadata']['social-share']['image']['key']
        for i in range(1,totalsize):
            if(element['story-elements'][i]['type']=="text"):
                Content = Content + element['story-elements'][i]['text']
            if(element['story-elements'][i]['type']=="image"):
                ImageCaption = element['story-elements'][i]['title']
                ImageURL = element['story-elements'][i]['image-s3-key']
        Content = Content.replace('<a ','<a style="color: #ce4242; text-decoration: none;" ')
        Content = Content.replace('<strong>','<strong style="color: #ce4242">')
        Content= Content.replace("<ins>",'<ins style="text-decoration: none;">')

        CardObject = {
            "Title":Title,
            "Content":Content,
            "ImageURL":ImageURL,
            "ImageCaption":ImageCaption
        }
        CardParameters.append(CardObject)

    TopFile = open('./axiostempfiles/first.html','r')
    thirdfile = open('./axiostempfiles/third.html','r').readlines()
    BottomFile = open('./axiostempfiles/second.html','r')

    TopLines = TopFile.readlines()
    BottomLines = BottomFile.readlines()

    CardFirstLine = open('./axiostempfiles/CardParts/first.html','r').readlines()
    CardHeadingLine = open('./axiostempfiles/CardParts/heading.html','r').readlines()
    CardSecondLine = open('./axiostempfiles/CardParts/second.html','r').readlines()
    CardThirdLine = open('./axiostempfiles/CardParts/third.html','r').readlines()
    CardFourthLine = open('./axiostempfiles/CardParts/fourth.html','r').readlines()

    LinkFirstLine = open('./axiostempfiles/ShareButtonParts/first.html').readlines()
    LinkSecondLine = open('./axiostempfiles/ShareButtonParts/second.html').readlines()
    LinkThirdLine = open('./axiostempfiles/ShareButtonParts/third.html').readlines()
    LinkFourthLine = open('./axiostempfiles/ShareButtonParts/fourth.html').readlines()


    CardsFinal = []
    CardsFinal  = CardsFinal + TopLines
    SecondArticleURL = ArticleURL
    ArticleURL = 'href="' + ArticleURL + '" \n'
    CardsFinal.append(ArticleURL)
    CardsFinal  = CardsFinal + thirdfile
    CardsFinal.append(today)
    for data in CardParameters:
        CardsFinal = CardsFinal + CardFirstLine
        CardsFinal.append(data['Title'])
        CardsFinal = CardsFinal +  CardHeadingLine                   
        Image = ' src="https://gumlet.assettype.com/' + data['ImageURL'] + '"' + '\n'
        CardsFinal.append(Image)
        Caption = 'alt="' + data['ImageCaption'] + '"' + '\n'
        CardsFinal.append(Caption)
        CardsFinal = CardsFinal + CardSecondLine
        CardsFinal.append(data['ImageCaption'])
        CardsFinal = CardsFinal + CardThirdLine
        CardsFinal.append(data['Content'])
        CardsFinal  = CardsFinal + CardFourthLine

    CardsFinal = CardsFinal + LinkFirstLine
    # facebook href
    facebookline = 'href="https://www.facebook.com/sharer/sharer.php?u=' + SecondArticleURL + '"' + '\n' 
    CardsFinal.append(facebookline)
    CardsFinal = CardsFinal + LinkSecondLine

    # Twitter href
    twitterline = 'href="https://twitter.com/intent/tweet?url=' +  SecondArticleURL + '"' + '\n'
    CardsFinal.append(twitterline)
    CardsFinal = CardsFinal + LinkThirdLine

    # Linekdin href
    linkedinline = 'href="https://www.linkedin.com/sharing/share-offsite/?url=' + SecondArticleURL + '"' + '\n'
    CardsFinal.append(linkedinline)
    CardsFinal = CardsFinal + LinkFourthLine

    CardsFinal = CardsFinal + BottomLines
    return CardsFinal


def BrewGenerateTemplate(url):
    today = date.today()
    today = today.strftime("%d %B, %Y")
    today = today + " \n"

    url = "https://swarajyamag.com/api/v1/stories/" + url
    CardsFinal = []
    # url = input('Enter API URL: \n')
    r = requests.get(url)
    response = r.json()
    storycards = response['story']['cards']

    CardParameters = []

    ArticleURL = response['story']['url']
    ArticleURL = ArticleURL + ""

    for element in storycards:
        Title = element['story-elements'][0]['text']
        Title = Title.replace("<a ", '<a style="color: #ce4242; text-decoration: none;" ')
        Title = Title.replace('<strong>','<strong style="color: #ce4242">')
        Title = Title.replace("<ins>",'<ins style="text-decoration: none;">')
        Title  =Title.replace("<p>",'<p style="color: #ce4242">')
        totalsize = len(element['story-elements'])
        Content = ""
        ImageCaption = element['metadata']['social-share']['image']['caption']
        ImageURL = element['metadata']['social-share']['image']['key']
        for i in range(1,totalsize):
            if(element['story-elements'][i]['type']=="text"):
                Content = Content + element['story-elements'][i]['text']
            if(element['story-elements'][i]['type']=="image"):
                ImageCaption = element['story-elements'][i]['title']
                ImageURL = element['story-elements'][i]['image-s3-key']
        Content = Content.replace('<a ','<a style="color: #ce4242; text-decoration: none;" ')
        Content = Content.replace('<strong>','<strong style="color: #ce4242">')
        Content= Content.replace("<ins>",'<ins style="text-decoration: none;">')

        CardObject = {
            "Title":Title,
            "Content":Content,
            "ImageURL":ImageURL,
            "ImageCaption":ImageCaption
        }
        CardParameters.append(CardObject)

    MainFile = open('./brewtempfiles/content.html','r').readlines()
    CardFile = open('./brewtempfiles/card.html','r').readlines()



    def cardEmbedder(object):
        for line in CardFile:
            if(line=="<!-- Heading -->\n"):
                title = object["Title"] + "\n"
                CardsFinal.append(title)
            elif(line=="<!-- Content -->\n"):
                CardsFinal.append(object["Content"])
                CardsFinal.append("\n")
            elif(line=="                <!-- ImageURL -->\n"):
                url  = '                src="https://gumlet.assettype.com/' + object['ImageURL'] + '"' + '\n'
                CardsFinal.append(url)
            elif(line=="<!-- ImageCaption -->\n"):
                CardsFinal.append(object["ImageCaption"])
                CardsFinal.append("\n")
            else:
                CardsFinal.append(line)
        return

    for line in MainFile:
        if(line=="<!-- Date -->\n"):
            CardsFinal.append(today)
        elif(line=="<!-- cards -->\n"):
            for object in CardParameters:
                cardEmbedder(object)
        else:
            CardsFinal.append(line)
    return CardsFinal
  

@app.get("/")
def read_root():
    data = open("./index.html").readlines()
    htmlData = """"""
    for line in data:
        htmlData = htmlData + line
    return HTMLResponse(content=htmlData, status_code=200)

@app.post("/")
def generate(api : str = Form(), type: int = Form()):
    data = []
    if type==1:
        data = AxiosGenerateTemplate(api)
    elif type==2:
       data = BrewGenerateTemplate(api)
    htmlData =""""""
    for line in data:
        htmlData = htmlData + line
    return HTMLResponse(content=htmlData, status_code=200)

@app.get("/axios/{api}",response_class=HTMLResponse)
def read_api(api):
    htmlData =""""""
    data = AxiosGenerateTemplate(api)
    for line in data:
        htmlData = htmlData + line
    return HTMLResponse(content=htmlData, status_code=200)


@app.get("/brew/{api}",response_class=HTMLResponse)
def read_api(api):
    htmlData =""""""
    data = BrewGenerateTemplate(api)
    for line in data:
        htmlData = htmlData + line
    return HTMLResponse(content=htmlData, status_code=200)



    
