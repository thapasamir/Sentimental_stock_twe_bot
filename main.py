import tweepy
import json
import time
import os
from datetime import datetime


from data.data_ import SentiAnal

with open("credential.json") as credential:
    dict_data = json.load(credential)


def tweet():
    auth = tweepy.OAuthHandler(dict_data["data"]['API Key'],dict_data["data"]['API Secret Key'])
    auth.set_access_token(dict_data["data"]['Access Token'],dict_data["data"]['Access Token Secret'])
    api = tweepy.API(auth)

    
    while True:

        stock_name = str(input("Enter a short stock name ? eg:tsla,btx,fb ::"))
        SentiAnal(stock_name)
        working_dir = os.getcwd() #getting the name of current directory
        list_dir = os.listdir(working_dir) #listing all the file in the current directory
        image = [img for img in list_dir if img.endswith(".jpg")] #selecting all the image from the the directory
        image_data = api.media_upload(image[0])        

        stock_name_split = stock_name.split(',')
        

        if len(stock_name_split) > 3:
            print("You can only enter upto 3 stock name ")
        
        else:
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            image_caption = stock_name +" "+ "sentimental stock prediction " + "Posted at :" + current_time    
            time.sleep(20)
            post = api.update_status(status=image_caption,media_ids=[image_data.media_id])

if __name__ == "__main__":
    tweet()


