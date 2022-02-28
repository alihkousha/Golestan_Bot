from pydoc import text
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.utils import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from unidecode import unidecode
from itertools import cycle
import os
import json
import Data_Handler
import telegram
from threading import Thread
import emoji
import winsound
duration = 1000  # milliseconds
freq = 440

DEFAULT_PORT = 0
DEFAULT_SERVICE_LOG_PATH = None
DEFAULT_KEEP_ALIVE = None


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

paths = {
    'Data' : os.path.join(os.getcwd(), 'Data'),
}

def zip_equal(iter1,iter2):
    return zip(iter1,cycle(iter2)) if len(iter1) > len(iter2) else zip(cycle(iter1),iter2)

def Mymap(iter):
    check_mark = emoji.emojize(":check_mark_button:")
    iter2 = []
    string = ''
    len_iter = len(iter)
    for x in range(len_iter):
        string += check_mark + iter[x]+"\n"
        if x % 10 == 0:
            iter2.append(string)
            string = ''
    iter2.append(string)
    iter2[1] = iter2[0] + iter2[1]
    iter2.pop(0)
    return iter2
    

class Golestan_Crawler(webdriver.Chrome):
    
    def __init__(self, executable_path, port=DEFAULT_PORT,
                 options = None, service_args=None,
                 desired_capabilities=None, service_log_path=DEFAULT_SERVICE_LOG_PATH,
                 chrome_options=None, service = None, keep_alive=DEFAULT_KEEP_ALIVE) -> None:
        
        super().__init__( executable_path, port=DEFAULT_PORT,
                 options = None, service_args=None,
                 desired_capabilities=None, service_log_path=DEFAULT_SERVICE_LOG_PATH,
                 chrome_options=None, service = None, keep_alive=DEFAULT_KEEP_ALIVE)
        self.user = os.environ.get("id")
        self.password = os.environ.get("pass")
        self.xpaths = {
            'user' : '/html/body/div/table[2]/tbody/tr[2]/td[2]/input',
            'password' : '/html/body/div/table[2]/tbody/tr[3]/td[2]/input',
            'Captcha' : '/html/body/div/table[2]/tbody/tr[4]/td[2]/input',
            'iframe' : '/html/body/div[4]/div/iframe',
            'infrmset-frame' : '/html/frameset/frameset',
            'Master-Frame' : '/html/frameset/frameset/frame[2]',
            'Form_Body-frame' : '/html/frameset/frame[2]',
            'Form_Body-frame2' : '/html/frameset/frame[3]',
            'report-finder' : '/html/body/table[1]/tbody/tr[8]/td[3]/table/tbody/tr/td[8]/input',
            'collage-code' : '/html/body/div[1]/div[2]/table/tbody/tr[4]/td[12]/input',
            'page-number-textbox' : '/html/body/table/tbody/tr/td[4]/input',
            'forward-buttom' :'/html/body/table/tbody/tr/td[5]/input',
            'backward-bottom' : '/html/body/table/tbody/tr/td[3]/input',
            'Close-button' : '/html/body/div[3]/div[4]/img',
        }

        self.Lessons = {
            'Lesson-Code' : [],
            'Lesson-Name' : [],
            'Lesson-Weight' : [],
            'Lesson-A-Weight' : [],
            'Capacity' : [],
            'Registered' : [],
            'Queue' : [],
            'Sex' : [],
            'Teacher' : [],
            'schedule' : [],
            'Exam-schedule' : [],
            'Abandon' : [],
            'Specification' : [],
            'Anti-Lesson' : [],
            'Presentation-Mode' : [],
            'Offline-Online' : [],
            'Description' : [],
        }
        

    def Logging(self):
        self.golestan = self.get("https://golestan.kntu.ac.ir/forms/authenticateuser/main.htm")
        self.captcha = input('enter captcha = ')
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,self.xpaths['iframe'])))
        #WebDriverWait(self, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,self.xpaths['infrmset-frame'])))
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,self.xpaths['Master-Frame'])))
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,self.xpaths['Form_Body-frame'])))
        #file = open("source.txt", "w",encoding="utf-8")
        #file.write(self.page_source)
        WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "txt")))
        self.find_elements(By.CLASS_NAME, "txt")[2].send_keys(self.user, Keys.TAB, self.password, Keys.TAB, self.captcha ,Keys.ENTER)
        self.switch_to.default_content()
    
    def Get_to_Lessons(self,log_in : bool = True,i=3):
        if log_in == True:
            self.Logging()
        else:
            pass
        sleep(0.5)
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "Faci2")))
        #WebDriverWait(self, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,self.xpaths['infrmset-frame'])))
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"Master")))
        WebDriverWait(self, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "Form_Body")))
        sleep(0.5)
        WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['report-finder'])))
        sleep(2)
        if log_in ==True:
            self.find_element(By.XPATH, self.xpaths['report-finder']).send_keys("102", Keys.ENTER ,Keys.ENTER)
        else:
            self.find_element(By.XPATH, self.xpaths['report-finder']).clear()
            self.find_element(By.XPATH, self.xpaths['report-finder']).send_keys("102", Keys.ENTER ,Keys.ENTER)
        self.switch_to.default_content()
        sleep(0.5)
        ##FACI number are increasing
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, f"Faci{i}")))
        #WebDriverWait(self, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,self.xpaths['infrmset-frame'])))
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"Master")))
        sleep(2)
        WebDriverWait(self, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "Form_Body")))
        WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['collage-code'])))
        self.find_element(By.XPATH, self.xpaths['collage-code']).send_keys("20","11","192","02", Keys.ENTER)
        self.switch_to.default_content()

    def Get_Lessons(self,i=3):
        #sleep(0.5)
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, f"Faci{i}")))
        #WebDriverWait(self, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,self.xpaths['infrmset-frame'])))
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"Master")))
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "Header")))
        WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "Form_Body")))
        WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "CTDData")))
        sleep(0.2)
        file = open("source.txt", "a",encoding="utf-8")
        self.Table_Data = self.find_elements_by_class_name('CTDData')
        self.Page_Data = self.Parse_Lessons()
        self.switch_to.default_content()
        self.Lessons = {
            'Lesson-Code' : [],
            'Lesson-Name' : [],
            'Lesson-Weight' : [],
            'Lesson-A-Weight' : [],
            'Capacity' : [],
            'Registered' : [],
            'Queue' : [],
            'Sex' : [],
            'Teacher' : [],
            'schedule' : [],
            'Exam-schedule' : [],
            'Abandon' : [],
            'Specification' : [],
            'Anti-Lesson' : [],
            'Presentation-Mode' : [],
            'Offline-Online' : [],
            'Description' : [],
        }
        return self.Page_Data
    
    ## Under Construction (look in your phone safari)##  
    def Parse_Lessons(self):    
        for element, dict_key in zip_equal(self.Table_Data, self.Lessons):
            if dict_key == 'Lesson-Weight' or  dict_key =='Lesson-A-Weight' or dict_key == 'Capacity' or dict_key =='Registered' or dict_key == 'Queue':
                if element.text != '':
                    self.Lessons[dict_key].append(int(unidecode(element.text)))
                else:
                    self.Lessons[dict_key].append(None)
            elif dict_key == 'Lesson-Code':
                if element.text != '':
                    self.Lessons[dict_key].append(int(unidecode(element.text[:-3]+element.text[-2:])))
                else:
                    self.Lessons[dict_key].append(None)
            else:
                self.Lessons[dict_key].append(element.text)
        return self.Lessons

    def Page_Controller(self,i=3):
        forward = True
        backward = False
        page_number_new = 1
        while True:
            while True:
                self.switch_to.default_content()
                try:
                    self.Page_as_dict = self.Get_Lessons(i=i)
                    with open(os.path.join(paths['Data'], f'Page-Data-{page_number_new}.json'),'w',encoding='utf-8') as outfile:
                        json.dump(self.Page_as_dict, outfile)
                        outfile.close()        
                    break
                except Exception as e:
                    print(e)
            try:
                self.switch_to.default_content()
                WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, f"Faci{i}")))
                WebDriverWait(self, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"Commander")))
                WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['forward-buttom'])))
                WebDriverWait(self, 10).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['backward-bottom'])))
                WebDriverWait(self, 10).until(EC.presence_of_element_located((By.XPATH, self.xpaths['page-number-textbox'])))
                self.f_button = self.find_element_by_xpath(self.xpaths['forward-buttom'])
                self.b_button = self.find_element_by_xpath(self.xpaths['backward-bottom'])
                self.page_number_text_box = self.find_element_by_xpath(self.xpaths['page-number-textbox'])
                page_number_old = self.page_number_text_box.get_attribute('value')
                if forward == True and backward == False:
                    self.f_button.click()
                elif forward == False and backward == True:
                    self.b_button.click()
                sleep(0.1)
                page_number_new = self.page_number_text_box.get_attribute('value')
                if page_number_new == page_number_old == "1":
                    forward = True
                    backward = False
                elif page_number_new == page_number_old != "1":
                    backward = True
                    forward = False
                    break
            except Exception as e:
                print(e)
        self.switch_to.default_content()
        self.find_element(By.XPATH,self.xpaths['Close-button']).click()


    def Threading_Crawler(self):
        i= 3
        self.Get_to_Lessons(i=i)
        self.Page_Controller(i=i)
        while True:
            i += 1
            sleep(0.5)
            self.Old_DataFrame = Data_Handler.DataFrame_Build()
            while True:
                try:
                    self.Get_to_Lessons(log_in=False,i=i)
                    self.Page_Controller(i=i)
                    break
                except Exception as e:
                    print(e)
                    self.switch_to.default_content()
            self.New_DataFrame = Data_Handler.DataFrame_Build()            
            if i >= 4:
                Thread(target=self.message_Sender).start()
            
    def message_Sender(self):
        O_DataFrame = self.Old_DataFrame
        N_DataFrame = self.New_DataFrame
        Bot = telegram.Bot(token='5160281097:AAH2HzueXkeb8O-OxcwBRI_g3cyRSJkJfJ4')
        self.report = Data_Handler.reporter(N_DataFrame,O_DataFrame)
        if self.report == []:
            winsound.Beep(freq, duration)
        for i in list(N_DataFrame['Lesson-Code']):
            self.report.append(Data_Handler.Capacity_Report(N_DataFrame,i))
        self.report = Mymap(self.report)
        for item in self.report:
                try:
                    print(Bot.send_message(chat_id="@Golestan_Updates",text=item,parse_mode=telegram.ParseMode.HTML))
                    sleep(3)
                except Exception as e:
                    cool_down = str(e).split(" ")[-2]
                    try:
                        sleep(float(cool_down))
                        print(Bot.send_message(chat_id="@Golestan_Updates",text=item,parse_mode=telegram.ParseMode.HTML))
                    except:
                        pass

class RegistrationClass(Golestan_Crawler):
    def __init__(self, executable_path, port=DEFAULT_PORT, options=None, service_args=None, desired_capabilities=None, service_log_path=DEFAULT_SERVICE_LOG_PATH, chrome_options=None, service=None, keep_alive=DEFAULT_KEEP_ALIVE) -> None:
        super().__init__(executable_path, port, options, service_args, desired_capabilities, service_log_path, chrome_options, service, keep_alive)
        
        self.objects = {
            'New-Row-Button' : '/html/body/table/tbody/tr/td[2]/input',
            'Change-Group-Button' : '/html/body/table/tbody/tr/td[4]/input', #remember in tr[{i}] i start from 2
            'Requesd-Cell' : '/html/body/div[3]/table/tbody/tr[{i}]/td[1]', 
            'Status-Cell' : '/html/body/div[3]/table/tbody/tr[{i}]/td[2]', 
            'Group-text-Cell' : '/html/body/div[3]/table/tbody/tr[{i}]/td[3]', 
            'Lesson-Code-3-text-Cell' : '/html/body/div[3]/table/tbody/tr[{i}]/td[3]', 
            'Lesson-Code-2-text-Cell' : '/html/body/div[3]/table/tbody/tr[{i}]/td[4]', 
            'Lesson-Code-1-text-Cell' : '/html/body/div[3]/table/tbody/tr[{i}]/td[5]', 
            'Lesson-Name-Cell' : '/html/body/div[3]/table/tbody/tr[{i}]/td[6]', 
            'Lesson-Weight-Cell' : '/html/body/div[3]/table/tbody/tr[{i}]/td[7]', 
            'Lesson-Weight-A-Cell' : '/html/body/div[3]/table/tbody/tr[{i}]/td[8]', 
            'Lesson-Kind-Cell' : '/html/body/div[3]/table/tbody/tr[{i}]/td[9]', 
            'Step-Of-Registration-Cell' : '/html/body/div[3]/table/tbody/tr[{i}]/td[10]', 
            'Description-Cell' : '/html/body/div[3]/table/tbody/tr[{i}]/td[11]', 
        }

if __name__ == "__main__":
    #crawler = Golestan_Crawler("chromedriver.exe")
    #crawler.Threading_Crawler()
    """df = Data_Handler.DataFrame_Build()
    it = []
    for i in list(df['Lesson-Code']):
        it.append(Data_Handler.Capacity_Report(df,i))
    it = Mymap(it)
    for x in it:
        print(x)"""
