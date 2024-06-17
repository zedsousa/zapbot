from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver import chrome
from parser import parser
import time
import os

class group:
    def __init__(self,name,chrome):
        print("Creating group object")
        group_header = chrome.find_element_by_xpath('//*[@id="main"]/header')
        group_header.click()
        close_button = chrome.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[5]/span/div/span/div/div/header/div/div[1]/div/span')
        time.sleep(0.5)
        self.name = name
        self.birth = self.find_birth(chrome)
        self.desc = self.find_desc(chrome)
        self.size = self.find_size(chrome)
        self.prev_msg_hash = 0
        close_button.click()

        # Create a parser object
        self.parser  = parser()
    
    # find the date and time the group chat was created
    def find_birth(self,chrome):
        birth = chrome.find_element_by_css_selector('#app > div > div.three._aigs > div._aigv._aig-._aohg > span > div > span > div > div > div > section > div.x13mwh8y.x1q3qbx4.x1wg5k15.x1bnvlk4.x1n2onr6.x1c4vz4f.x2lah0s.xdl72j9.x13x2ugz.x6x52a7.xxpdul3.xat24cr.x1cnzs8.xx6bls6 > div.x1f6kntn.x16h55sf.x1fcty0u.x1rw0npd')
        return birth.text

    # find the date and time the group chat was created
    def find_desc(self,chrome):
        desc = chrome.find_element_by_css_selector('#app > div > div.three._aigs > div._aigv._aig-._aohg > span > div > span > div > div > div > section > div.x13mwh8y.x1q3qbx4.x1wg5k15.x1bnvlk4.x1n2onr6.x1c4vz4f.x2lah0s.xdl72j9.x13x2ugz.x6x52a7.xxpdul3.xat24cr.x1cnzs8.xx6bls6 > div.x126k92a.xqmxbcd > div > div > div > span > span')
        return desc.text

    # find the total number of members in the group
    def find_size(self,chrome):
        total = chrome.find_element_by_css_selector('#app > div > div.three._aigs > div._aigv._aig-._aohg > span > div > span > div > div > div > section > div.x13mwh8y.x1q3qbx4.x1wg5k15.x1bnvlk4.x1n2onr6.x1c4vz4f.x2lah0s.xdl72j9.xyorhqc.x13x2ugz.x7sb2j6.x6x52a7.x1i2zvha.xxpdul3 > div > div.x1evy7pa.x1kgmq87.x2b8uid > span > span > button')
        total_text = total.text.replace("Membro: ", "")
        return int(total_text)

    # finds all the participants name
    def find_names(self,chrome):
        div = chrome.find_element_by_class_name('_aou8 _aj_h')
        span = div.find_element_by_class_name('x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1rg5ohu _ao3e')

        # create the list of names because get_attribute function doesnt return correct format
        names = []
        buffer = ""
        for c in span.get_attribute('title'):
            print(c)
            if c==",":
                names.append(buffer.lstrip(" "))
                buffer=""
            else:
                buffer+=c
        return names

    # send a message to group chat, chat must be open already
    def send_msg(self,contents,chrome):
        type_field = chrome.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
        type_field.send_keys(contents["text"])

        send_button = chrome.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')
        send_button.click()

    def read_msgs(self,chrome):
        msgs_in = chrome.find_elements(By.CLASS_NAME,"message-in")
        for msg in msgs_in:
            msg_span = msg.find_element(By.CLASS_NAME,"eRacY")
            print(msg_span.text)

    def send_img(self,contents,chrome):
        attach = chrome.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div')
        attach.click()

        img_button = chrome.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input')
        img_button.send_keys(os.path.abspath(contents["media_location"]))
        
        time.sleep(1)
        send_button = chrome.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div')
        send_button.click()
        
    def send_img_text(self,contents,chrome):
        attach = chrome.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div')
        attach.click()

        img_button = chrome.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input')
        img_button.send_keys(os.path.abspath(contents["media_location"]))

        time.sleep(0.5)
        text_field = chrome.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div[1]/span/div/div[2]/div/div[3]/div[1]/div[2]')
        text_field.send_keys(contents["text"])
        
        send_button = chrome.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div')
        send_button.click()
        
    def send_msg_line_by(self,contents,chrome):
        type_field = chrome.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        for line in contents["text"]:
            actions = ActionChains(chrome)
            type_field.send_keys(line)
            actions.key_down(
                Keys.SHIFT
            ).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
            actions.reset_actions()
        send_button = chrome.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
        send_button.click()
        
    # read latest message of the current chat and perform action if any
    def read_latest_msg(self,chrome):
        text = ""
        msg_hash = self.prev_msg_hash
        
        try:
            msg_in = chrome.find_elements(By.CLASS_NAME,"message-in")[-1]
            msg_span = msg_in.find_element(By.CLASS_NAME,"eRacY")
            msg_hash = hash(msg_span.text)
            text = msg_span.text
        except:
            print("can't read message")
        
        if text[:3]=="@JD" and self.prev_msg_hash!=msg_hash:
            print("bot called")
            self.perform_action(text,chrome)
        
        if text!="" and text=="@all" and self.prev_msg_hash!=msg_hash:
            print("@all detected")
            self.at_all(chrome)
        
        self.prev_msg_hash = msg_hash if text!="" else self.prev_msg_hash
        return msg_hash

    # @ everyone in the group chat
    def at_all(self,chrome):
        type_field = chrome.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        actions = ActionChains(chrome) 
        for i in range(self.size-1):
            actions.send_keys("@")
            actions.send_keys(Keys.ARROW_DOWN*i)
            actions.send_keys(Keys.TAB)
        actions.perform()
        type_field.send_keys(Keys.ENTER)
        
    # perform action if any
    def perform_action(self,text,chrome):
        actions = {"text":self.send_msg,
                   "error":self.send_msg,
                   "help":self.send_msg_line_by,
                   "image":self.send_img,
                   "image-text":self.send_img_text}
        cmd = text.split()
        final_cmd = " ".join(cmd[1:])
        print(final_cmd)
        if len(cmd)>1:
            try:
                contents = self.parser.parse(final_cmd)
                actions[contents["media"]](contents,chrome)
            except Exception as e:
                print(e)
                self.send_msg({"text":"oops something went wrong.."},chrome)