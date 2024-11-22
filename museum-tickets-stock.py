import os
from dhooks import Webhook, Embed, File
import requests
import logging
from datetime import datetime
import time
import shutil


from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import requests 
import json
from time import sleep
from discordwebhook import Discord
import pyimgur
import os
import sys
from pytz import timezone, utc

class alertMe():

  def __init__(self):
    self.url = 'https://museum-tickets.nintendo.com/en/api/calendar?target_year=2024&target_month=12'
    self.HEADERS = {'x-requested-with': 'XMLHttpRequest'}
    self.urlResponse = None
    self.urlResponseCode = None
    self.Price = None
    self.sku_num  = None
    self.stock = None
    self.stock_status = None
    self.run = True
    self.logger
    self.counter = 0
    self.lvImgUrl = None
    self.localImg = None
    self.imgurLink = None
    self.imgPath = None
    self.imgFail = None
    self.refreshCounter = 0
    self.StockTime = None
    self.start_time = None
    self.printCondtion = False
    self.stockDate = None


  def execute(self):
    try:
      self.logger()
      self.start_time = time.time()
      print(self.getCSTTime()," Monitor Has Started ")
      self.logger.info(" Monitor Has Started ") 
      self.notify_start()
      self.Monitor()
    except Exception as e:
      print("Error Has Occured Chack Logs")
      self.logger.info(" Monitor Has Failed Because - %s "%e)
      self.executePostError()    

  def executePostError(self):
    try:
      self.start_time = time.time()
      print(self.getCSTTime()," Monitor Has Been Restarted Error Occured ")
      self.logger.info(" Monitor Has Been Restarted Error Occured ") 
      self.notify_restart()
      self.Monitor()
    except Exception as e:
      print("Error Has Occured Chack Logs")
      self.logger.info(" Monitor Has Failed Because - %s "%e)
      self.executePostError()

  def Monitor(self):
    while(self.run == True):
      self.counter +=1
      print()
      print(self.getCSTTime(), " Iteration Number %i Of Waiting For Stock "%(self.counter))
      self.logger.info(" Iteration Number %i Of Waiting For Stock "%(self.counter)) 
      self.getSiteData()
      print(self.getCSTTime(), " Sleeping for 60 Seconds.. ")
      self.logger.info(" Sleeping for 60 Seconds.. ")
      sleep(62)

  def getSiteData(self):
    self.readHttp()
    if(self.urlResponseCode == 200):
      self.checkResponse()
    else: 
        self.notify_badresponse()
        print(self.getCSTTime()," Something Went Wrong While Getting Website Info {%s} "%self.urlResponseCode)
        self.logger.info(" Something Went Wrong While Getting Website Info {%s} "%self.urlResponseCode)
        postLooprun = True
        while(postLooprun == True):
          print(self.getCSTTime(), " Sleeping for 60 Seconds.. ")
          self.logger.info(" Sleeping for 60 Seconds.. ")
          sleep(62)
          if(self.urlResponseCode == 200):
            self.notify_goodresponse()
            self.checkResponse()
            postLooprun = False
          else:
            print(self.getCSTTime()," Resonse From Website: {%s} Going To Attempt To Reach Again "%self.urlResponseCode)
            self.logger.info(" SResonse From Website: {%s} Going To Attempt To Reach Again "%self.urlResponseCode)
          

  def checkResponse(self): 
    print(self.getCSTTime()," Checking Response From Website..Going To Parse ")
    self.logger.info(" Checking Response From Website..Going To Parse ") 
    # List of dates to filter for
    dates_to_check = ["2024-12-04", "2024-12-05", "2024-12-06"]

    # Parse the JSON string into a Python dictionary
    data = json.loads(self.urlResponse)

    # Accessing the calendar data
    calendar = data['data']['calendar']

    # interating through data
    for date, details in calendar.items():
      if date in dates_to_check:
        if details['sale_status'] != 2:
          print(self.getCSTTime()," Found Change in sale_status for {%s}..going to notify "%date)
          self.logger.info(" Found Change in sale_status for {%s}..going to notify "%date)
          self.StockTime = time.time()
          self.stockDate = date
          self.notify_user()
          print(self.getCSTTime(),"--- %s seconds to find stock --- \n" % round(time.time() - self.start_time, 2))
          self.logger.info("--- %s seconds to find stock ---\n" % round(time.time() - self.start_time, 2))
        elif details['open_status'] != 1: 
          print(self.getCSTTime()," Found Change in open_status for {%s}..going to notify "%date)
          self.logger.info(" Found Change in open_status for {%s}..going to notify "%date)
          self.StockTime = time.time()
          self.stockDate = date
          self.notify_user()
          print(self.getCSTTime(),"--- %s seconds to find stock --- \n" % round(time.time() - self.start_time, 2))
          self.logger.info("--- %s seconds to find stock ---\n" % round(time.time() - self.start_time, 2))
        else:
          print(self.getCSTTime()," No Change Found in open_status and sale_status for {%s}..not going to notify "%date)
          self.logger.info(" No Change Found in open_status and sale_status for {%s}..not going to notify "%date)


  def readHttp(self): 
    # Making a get request 
    response = requests.get(self.url, headers= self.HEADERS) 
    # print response 
    self.urlResponseCode = response.status_code 
    self.urlResponse = response.text

    print(self.getCSTTime()," Succesfully Found HTTP Reponse From Website Response: {%s} "%self.urlResponseCode)
    self.logger.info(" Succesfully Found HTTP Reponse From Website Response: {%s} "%self.urlResponseCode)
    self.logger.info(" Reponse From Website: %s"%response.text)

  def notify_user(self):
      hook = Webhook('https://discord.com/api/webhooks/1304171219217682512/pEGmNRcF-igfk0yT19DqVtITd_Xbm0lCbxqzEZeDVQZfFpEPyD_adLmejIbwbwkYDL7k')

      source = Embed(
                title='Kyoto Museum Ticket for %s'%self.stockDate,
                url= self.url,
                description='',
                color = 0x0070ff, #red = 0xd10a07
                timestap = 'now' )

      """[Color Code]
      The solution is using 0x[Hexadecimal color code without the hash]. 
      You can convert any color you want to hexadecimal using this wesbite: http://www.colorhexa.com.

      Example:White is 0xffffff
              Red is 0xff0000

      """
      logo = "https://i.imgur.com/C6jytaB.png"
      nintendo = 'https://imgur.com/a/lfjJLCZ.png'

      source.set_author(name = 'Buy It Now!', icon_url=nintendo)
      source.set_footer(text = 'NoobPreme - Monitor', icon_url = logo)

      source.set_thumbnail('https://imgur.com/a/TzeYOVw.png')

      source.set_image('https://imgur.com/a/TzeYOVw.png')
      hook.send(embed=source)
      
      print(self.getCSTTime()," Succesfully Sent Stock Notification ")
      self.logger.info(" Succesfully Sent Stock Notification ") 
      
  def notify_start(self):
    discord = Discord(url="https://discord.com/api/webhooks/795760900157341758/HMt5jaWkf2L_JaJbjtvekY_uxc6pHB6mkFUDlrSf33ZyyrwKwkw2TTxRpqowKYHB6ayu")
    discord.post(embeds=[{"title": "Monitor Has Started For Nintendo Museum", "color": "14177041" ,"timestap" : "now" }])
    #https://www.spycolor.com/  color is in decimal format

    print(self.getCSTTime()," Succesfully Sent Monitor Start Notification ")
    self.logger.info(" Succesfully Sent Monitor Start Notification ") 

  def notify_restart(self):
    discord = Discord(url="https://discord.com/api/webhooks/795760900157341758/HMt5jaWkf2L_JaJbjtvekY_uxc6pHB6mkFUDlrSf33ZyyrwKwkw2TTxRpqowKYHB6ayu")
    discord.post(embeds=[{"title": "Monitor Has Been Restarted For Nintendo Tickets", "color": "14177041" ,"timestap" : "now"}])
    #https://www.spycolor.com/  color is in decimal format

    print(self.getCSTTime()," Succesfully Sent Monitor Restart Notification ")
    self.logger.info(" Succesfully Sent Monitor Restart Notification ") 

  def notify_badresponse(self):
    discord = Discord(url="https://discord.com/api/webhooks/795760900157341758/HMt5jaWkf2L_JaJbjtvekY_uxc6pHB6mkFUDlrSf33ZyyrwKwkw2TTxRpqowKYHB6ayu")
    discord.post(embeds=[{"title": "Monitor Has Found Bad Response From Website %s"%(self.urlResponseCode), "color": "14177041" ,"timestap" : "now"}])
    #https://www.spycolor.com/  color is in decimal format

    print(self.getCSTTime()," Succesfully Sent Monitor badresponse Notification ")
    self.logger.info(" Succesfully Sent Monitor badresponse Notification ") 

  def notify_goodresponse(self):
    discord = Discord(url="https://discord.com/api/webhooks/795760900157341758/HMt5jaWkf2L_JaJbjtvekY_uxc6pHB6mkFUDlrSf33ZyyrwKwkw2TTxRpqowKYHB6ayu")
    discord.post(embeds=[{"title": "Monitor Has Found Good Response From Website %s"%(self.urlResponseCode), "color": "14177041" ,"timestap" : "now"}])
    #https://www.spycolor.com/  color is in decimal format

    print(self.getCSTTime()," Succesfully Sent Monitor goodresponse Notification ")
    self.logger.info(" Succesfully Sent Monitor goodresponse Notification ") 

  def logger(self):
    #Create and configure logger 
    logging.basicConfig(filename="checksites.log", 
                        format='%(asctime)s.%(msecs)04d %(message)s',
                        datefmt=('%Y-%m-%d %H:%M:%S'), 
                        filemode='w') 
    #Creating an object 
    self.logger=logging.getLogger() 
    logging.Formatter.converter = self.customTime 
    #Setting the threshold of logger to INFO
    self.logger.setLevel(logging.INFO) 

  def customTime(*args):
    utc_dt = utc.localize(datetime.utcnow())
    my_tz = timezone("US/Central")
    converted = utc_dt.astimezone(my_tz)
    return converted.timetuple()

  def getCSTTime(self):
    centralTimeZone = timezone('US/Central')
    central_time = datetime.now(centralTimeZone)
    return(central_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    

if __name__== "__main__":
  taskMaster =  alertMe()
  taskMaster.execute()