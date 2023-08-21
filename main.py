from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import random
from tkinter import Tk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename

# Make interface for file selection
Tk().withdraw()
filename = askopenfilename()

df = pd.read_csv(filename)
l = len(df)

mess = simpledialog.askstring(title="Message", prompt="Type message. (put *** in place of name)")

driver = webdriver.Chrome("chromedriver.exe")
url = "https://web.whatsapp.com/"
driver.get(url)
print("Scan QR Code")
#scan qr code to login into whatsapp

time.sleep(60)
srchbox = driver.find_element(By.XPATH, "//*[@id='side']/div[1]/div/div/div[2]/div/div[1]")  # Searchbox
srchbox.click()

for i in range(l):
    
    mob = str(df.at[i,'Mobile'])  # Mobile/Whatsapp Number
    nam = str(df.at[i,'Name'])    # Name
    '''mess = "Hello " + nam + ", Maja ma?"   # Message'''
    mess_personal = mess.replace("***", nam)
    # Going to page of candidate in whatsapp
    srchbox.send_keys(mob)
    time.sleep(1)
    srchbox.send_keys(Keys.ENTER)
    
    p = driver.page_source
    soup= BeautifulSoup(p,'lxml')
    lastmess = soup.find_all('span',{'class':"_11JPr selectable-text copyable-text"},string=True)[-1]  # list of all messages
    recent = lastmess.get_text(strip=True)  # Last Message
    time.sleep(2)
    
    # If message already sent before, candidate will not get same message again.
    if(recent!=mess_personal):
        messbox = driver.find_element(By.XPATH, "//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[2]/div[1]")
        messbox.send_keys(mess_personal)
        messbox.send_keys(Keys.ENTER)  # Message sent with ENTER Key
        print("Message sent successfully!!!")
    else:
        continue
    
    ts = random.randint(10,30)
    time.sleep(ts)  # Stop for random time


print("Task Completed....")
#driver.close()  # Close the window