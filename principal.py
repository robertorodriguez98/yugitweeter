from time import sleep
from datetime import datetime,date
import requests
import json
from random import randint
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
from auth2 import (
    consumer_key2,
    consumer_secret2,
    access_token2,
    access_token_secret2
)
from twython import Twython



twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

twitter_art = Twython(
    consumer_key2,
    consumer_secret2,
    access_token2,
    access_token_secret2
)

def textolargo(tocho):
    if len(tocho) >= 270:
        tochoIzq = tocho[:269]
        tochoDer = tocho[269:]
        tochoPr = tochoIchoPr = tochoIzq + "[...]"
        print(tochoPr)

        tweet = twitter.get_user_timeline(
        screen_name="twbotyugioh",
        count=1)
        twID = tweet[0]["id"]
        twitter.update_status(status=tochoPr, in_reply_to_status_id=twID)
        textolargo(tochoDer)
    else:
        print(tocho)
        tweet = twitter.get_user_timeline(
        screen_name="twbotyugioh",
        count=1)
        twID = tweet[0]["id"]
        twitter.update_status(status=tocho, in_reply_to_status_id=twID)

sleep(30)
response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
datosBD = open("cardinfo.php", "wb")
datosBD.write(response.content)
datosBD.close()
        

f = open('cardinfo.php')
yugi = json.load(f)
f.close()


a_file = open("lista.txt")
file_contents = a_file.read()
listaIDS = file_contents.splitlines()
#print(contents_split)
a_file.close()

print(len(listaIDS))
totalCartas = len(listaIDS)


bucle = True

while bucle == True:
    
    sleep(30)
    now = datetime.now()
    today = date.today()
    current_time = now.strftime("%H:%M:%S")
    fecha = today.strftime("%d/%m/%y")
    horaP = current_time[3:5]
    print(horaP)
    
    if  horaP == "00" or horaP == "30":

        a_file = open("lista.txt")
        file_contents = a_file.read()
        listaIDS = file_contents.splitlines()
        a_file.close()

        numID = randint(0,len(listaIDS)-1)
        idRand = listaIDS[numID]
        #idRand = 4538826 #chaos emperor armageddon - texto largo
        print(idRand)
        listaIDS.remove(idRand)
        idRand = int(idRand)

        with open('lista.txt','r+') as f:
                f.seek(0)
                for elemento in listaIDS:
                    f.write(str(elemento))
                    f.write('\n')
                f.truncate() 
                f.close() 

        for elemento in yugi["data"]:
            if elemento["id"] == idRand:
                try:
                    primerTwit = True
                    nombre = elemento["name"]
                    tipo = elemento["type"]
                    desc = elemento["desc"]
                    direccion = elemento["card_images"][0]["image_url"]

                    
                    texto = ("%s  //  %s\n\n%s"%(nombre,tipo,desc))
                    #print(texto)
                    


                    response = requests.get(direccion)
                    imagen = open("subida.png", "wb")
                    imagen.write(response.content)
                    imagen.close()
                    photo = open('subida.png', 'rb')
                    
                    if len(texto) >= 270:
                        textoIzq = texto[:269]
                        textoDer = texto[269:]
                        textoPr = textoIzq + "[...]"
                        print(textoPr)
                        response = twitter.upload_media(media=photo)
                        twitter.update_status(status=textoPr,media_ids=[response["media_id"]])

                        textolargo(textoDer)
                    else:
                        print(texto)
                        response = twitter.upload_media(media=photo)
                        twitter.update_status(status=texto,media_ids=[response["media_id"]])

                    photo.close()

                    tweet = twitter.get_user_timeline(
                    screen_name="twbotyugioh",
                    count=1)
                    twID = tweet[0]["id"]
                    
                    pagina = "https://db.ygoprodeck.com/card/?search=" + str(idRand)
                    respuesta = "go " + pagina + " to know more about " + nombre + "!!!"

                    twitter.update_status(status=respuesta, in_reply_to_status_id=twID)



                    #ARTES DE CARTAS
                    pagina = "https://storage.googleapis.com/ygoprodeck.com/pics_artgame/" + str(idRand) + ".jpg"
                    response = requests.get(pagina)
                    imagen = open("art.jpg","wb")
                    imagen.write(response.content)
                    imagen.close()

                    photo = open('art.jpg', 'rb')
                    texto = ("%s  //  %s"%(nombre,tipo))

                    response = twitter_art.upload_media(media=photo)
                    twitter_art.update_status(status=texto,media_ids=[response["media_id"]])
                    photo.close()
                except:
                    nombre="error"
                    listaIDS.append(idRand)

                #registro = nombre + " subido a las " + current_time + "\n"
                registro = fecha + " " + current_time + "  -  "+ nombre + "\n"
                print(registro)
                registroArch = open('registro.txt','a')
                registroArch.write(registro)
                registroArch.close()

       
        sleep(1600)
    if len(listaIDS) == 0:
        bucle == False



textoPr = "I have uploaded all " + str(totalCartas) + " cards!!!!!!!!"
photo = open('celebracion.png', 'rb')
response = twitter.upload_media(media=photo)
twitter.update_status(status=textoPr,media_ids=[response["media_id"]])
