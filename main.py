from selenium import webdriver
from os import path
from os import getcwd
from getpass import getuser
import argparse
import signal

stop = False
def signal_handler(sig, frame):
    print('Exiting nicely!')
    global stop
    stop = True
    chrome.quit()
    exit()
    
#Uses the search bar to find and open chat
def open_chat(name):
    search_field = chrome.find_element_by_xpath('//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]')
    search_field.send_keys()

    chat = chrome.find_element_by_xpath('//span[@title="{}"]'.format(name))
    chat.click()

# opens chat and sends message
def send_msg(message,group_name):
    open_chat(group_name)

    type_field = chrome.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
    type_field.send_keys(message)

    send_button = chrome.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')
    send_button.click()

def setup_args_parser(parser):
    parser.add_argument("name",type=str,help="The name of the group chat the bot will run on")
    parser.add_argument("-c","--cache",action="store_true",help = "Use browser cache to stop having to scan QR code more than once")
    parser.add_argument("-s","--system",type=str,choices=["windows","mac","linux"],default="linux",help = "What OS is being used")
    return parser

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    arg_parser = argparse.ArgumentParser()
    arg_parser = setup_args_parser(arg_parser)
    args = arg_parser.parse_args()
    
    # construct paths 
    user = getuser()
    local_path = path.abspath(getcwd())
    driver_path = local_path+"/chromedriver" if args.system!="windows" else local_path+"\chromedriver.exe"
    chrome_profiles = {"linux":'/home/{}/.config/google-chrome/default'.format(user),
                       "mac":'/Users/{}/Library/Application Support/Google/Chrome/Default'.format(user),
                       "windows":'C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Default'.format(user)}

    # Set options and use cache of the chrome browser
    options = webdriver.ChromeOptions()
    if args.cache:
        options.add_argument('--user-data-dir='+chrome_profiles[args.system])
        options.add_argument('--profile-directory=Default')

    # open chrome and whatsapp
    chrome = webdriver.Chrome(driver_path,options=options)
    chrome.get("https://web.whatsapp.com/")

    print("press ENTER once whatsapp has loaded.")
    input("")

    group_name = args.name
    send_msg("Teste", group_name)
