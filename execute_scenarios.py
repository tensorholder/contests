####Python2.7
import unittest
import  os
import time
import urllib2
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import itertools
from decimal import Decimal
from selenium.webdriver.support import expected_conditions as EC
root_name = "root"
password = "$$$$$$$"
def log_in(driver):
    # Choose language
    #driver.maximize_window()
    languages = driver.find_element_by_class_name('lang')
    languages.click()
    languages.find_element_by_css_selector('span.title-lang')
    language = driver.find_element_by_xpath("//*[contains(text(), 'EN')]")
    language.click()
    time.sleep(3)
    # Choose country
    country = driver.find_element_by_xpath("//*[contains(text(), 'Russian')]")
    actions = ActionChains(driver)
    countries = driver.find_element_by_class_name('country-menu')
    countries.click()
    try:
        actions.move_to_element(country).click().perform()
    except ElementNotVisibleException:
        print ('This language has already been selected.')
    time.sleep(3)
    if driver.title.__contains__('Sign up'):
        # Go to log in form
        driver.find_element_by_xpath("//*[contains(text(), 'log in')]").click()
    if driver.title.__contains__('Log in'):
        # Enter registration data
        driver.find_element_by_id('email').send_keys('golubin@i-teco.ru')
        driver.find_element_by_id('password').send_keys('jiJ:foig@')
        # recaptcha
        try:
            time.sleep(2)
            driver.find_element_by_xpath("//*[@role='presentation']").click()
            time.sleep(7)
        except NoSuchElementException:
            print ('reCaptcha test is not on the page')
            # Click "Log in" button
            driver.find_element_by_css_selector('td.nbtn-red-m').click()
        time.sleep(7)

#Main pannel with perms
def option_panel(driver):
    driver.find_element_by_xpath("//*[contains(text(),'Virtual machines')]").click()
    time.sleep(2)
    driver.find_element_by_xpath("//*[@value='Order now']").click()
    time.sleep(5)

#left-bar menu
def navigation_option_panel(driver,name):
    driver.find_element(By.CSS_SELECTOR,"a.list-group-item").click()
    time.sleep(2)
    driver.find_element(By.LINK_TEXT,name).click()
    time.sleep(2)

#Download image by url
def download_image(driver,url):
    if not os.path.exists(os.path.abspath(os.curdir)+"/image.iso"):
        image_url = urllib2.urlopen("http://www.example.com/songs/mp3.mp3")
        image = open('image.iso','wb')
        image.write(image_url.read())
        image.close()

def upload_instruction(driver):
    download_image(driver,"http://releases.ubuntu.com/12.04/ubuntu-12.04.5-server-amd64.iso")
    option_panel(driver)
    navigation_option_panel(driver,"Images")
    #Find add button
    driver.find_element(By.CSS_SELECTOR,"a.btn.btn-primary.add-image").click()
    time.sleep(2)
    #Declare allert window
    pop_up_wind = driver.find_element_by_xpath('//iframe')
    driver.switch_to_frame(pop_up_wind)
    sub_controll = driver.find_element_by_xpath("//form[@method='POST']")
    sub_controll.find_element_by_name("name").send_keys("Ubuntu-12.04.5-server-amd64")
    form = Select(sub_controll.find_element_by_id('disk_format'))
    form.select_by_value('iso')
    driver.find_element(By.CSS_SELECTOR,"input[type=file]").send_keys(os.path.abspath(os.curdir)+"/image.iso")
    time.sleep(2)
    driver.switch_to_default_content()
    driver.find_element(By.XPATH,"//button[@id='createButton']").click()
    try:
        el = WebDriverWait(driver,100).until(EC.presence_of_element_located((By.CSS_SELECTOR,"td.status.status-create_image")))
    finally:
        time.sleep(5)

    try:
        def func(driver):
            try:
                elem = driver.find_element(By.CSS_SELECTOR,"td.status.status-create_image")
                return False
            except NoSuchElementException:
               #Check for existance current image in list
                return  driver.find_element(By.LINK_TEXT,"Ubuntu-12.04.5-server-amd64")
        #time dependence from uploading capability of current network, so i place more than 18 mins for implicity wait
        fat = WebDriverWait(driver,1000).until(func)
    finally:
        time.sleep(5)
#49
def delete_image(driver):
    option_panel(driver)
    navigation_option_panel(driver,"Images")
    founded_elem = driver.find_element(By.LINK_TEXT,"Ubuntu-12.04.5-server-amd64")
    founded_elem.find_element(By.XPATH,"..").find_element(By.XPATH,"..").click()
    time.sleep(1)
    driver.find_element_by_link_text('Destroy').click()
    time.sleep(5)
    driver.find_element(By.XPATH,"//form[@action]").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@type='text']").send_keys('DESTROY')
    driver.find_element(By.XPATH,"//button[@value='ok']").click()
    time.sleep(5)



def console_perfomance(driver):
    try:
    #waiting until routine
        def routine(driver):
            try:
                elem = driver.find_element_by_id('buttonBar')
                return elem
            except:
                return False
        temp=WebDriverWait(driver,100).until(routine)
    except:
        raise NoSuchElementException("No buttonbar")
    time.sleep(15)
    elem = driver.find_element(By.CSS_SELECTOR,'canvas')
    elem.click()
    #Log in console by special root_name and password which are declared at the top
    elem.send_keys(root_name)
    elem.send_keys(Keys.ENTER)
    time.sleep(5)
    elem.send_keys(password)
    elem.send_keys(Keys.ENTER)
    time.sleep(5)
    return elem

def move_to_vm_console(driver):
        navigation_option_panel(driver,'Virtual servers')
        driver.find_element(By.XPATH,"//tr[@id='row-186267']").click()
        driver.find_element(By.LINK_TEXT,"Console").click()
        time.sleep(2)
        driver.find_element(By.LINK_TEXT,"Ok").click()
        time.sleep(4)



#47,48
def check_vm_image(driver,instuct):
    option_panel(driver)
    #Console routine for checking vm and open console
    move_to_vm_console(driver)
    #declare two windows(option-panel) and (console-page)
    main_wind = driver.window_handles[0]
    second = driver.window_handles[1]
    driver.switch_to_window(second)
    #console execution commands
    elem=console_perfomance(driver)
    #sequence of execution commands
    elem.send_keys("file -s/dev/sr0")
    elem.send_keys(Keys.ENTER)
    time.sleep(15)
    #return to option panel
    driver.switch_to_window(main_wind)
    navigation_option_panel(driver,'Images')
    #select check_box
    sup_elem=driver.find_element(By.LINK_TEXT,'Ubuntu-12.04.5-server-amd64').find_element(By.XPATH,'..').find_element(By.XPATH,'..').find_element(By.CSS_SELECTOR,'input.checkbox').click()
    time.sleep(2)
    #Attach image to VM1
    driver.find_element(By.LINK_TEXT,instuct).click()
    time.sleep(3)
    #Confirm allert window
    if instuct=='Detach':
        driver.find_element(By.CSS_SELECTOR,'button.btn.btn-success').click()
        time.sleep(2)
    #finding allert_frame_body
    allert = driver.find_element_by_xpath('//iframe')
    driver.switch_to_frame(allert)
    sub_controll = driver.find_element_by_xpath("//form[@method='POST']")
    form = Select(sub_controll.find_element_by_id('instance_id'))
    form.select_by_value('186267')
    #Submit
    driver.find_element(By.XPATH,"//button[@id='createButton']").click()
    time.sleep(5)
    driver.switch_to_default_content()
    #small routine for checking implicity waits
    def small_routine(driver,css_selector):
        try:
            def func(driver):
                try:
                    elem = driver.find_element(By.CSS_SELECTOR,css_selector)
                    return False
                except NoSuchElementException:
                   #Check for existence current image in list
                    return  driver.find_element(By.LINK_TEXT,"Ubuntu-12.04.5-server-amd64")
            fat = WebDriverWait(driver,40).until(func)
        except:
              raise NoSuchElementException()
    #Detach and Attach instructions
    if instuct=='Detach':
        small_routine(driver,"td.status.status-unmounting")
    else:
        small_routine(driver,"td.status.status-mounting")
    #console routine
    move_to_vm_console(driver)
    elem = console_perfomance(driver)
    elem.send_keys("file -s/dev/sr0")
    elem.send_keys(Keys.ENTER)
    time.sleep(15)

#I dont understand why this function doesn't work(problems with avg compression (in some values text is empty)
def func_to_demonstrate_avg_values(driver):
     vals = driver.find_elements(By.XPATH,"//*[contains(text(),'avg')]")
     for k in vals:
         print k.text
     avg_vals = []
     for elem in vals:
        avg_cap = str(elem.text)
        nev_str=''.join(avg_cap[i] for i in xrange(len(avg_cap))if i>4).replace(',','.')
        ind = [i for i,x in enumerate(nev_str) if x=='.']
        ind.pop(0)
        if len(ind)>0:
            for index in ind:
                nev_str = nev_str[:index]+nev_str[(index+1):]
        avg_vals.append(float(nev_str))
     return avg_vals


#50
def check_statistics_with_conditions(driver):
    option_panel(driver)
    navigation_option_panel(driver,"Statistics")
    time.sleep(2)
    def options_statistics(driver):
        vmselector= Select(driver.find_element_by_id('perf_object'))
        vmselector.select_by_visible_text('- TEST_VM1')
        periodselector = Select(driver.find_element_by_id('graph_period'))
        periodselector.select_by_value('past-five-minutes')
        time.sleep(10)
    options_statistics(driver)
    values = ['CPU usage, mhz','CPU usage, %','Disk','Bandwidth','Memory usage, %','Memory usage, MiB']
    #Checking for existance all diagrams (values)
    for value in values:
        driver.find_element(By.XPATH,"//*[contains(text(),"+"'"+value+"'"+")]")
    #Starting attempt to power_off VM
    navigation_option_panel(driver,"Virtual servers")
    driver.find_element(By.XPATH,"//tr[@id='row-186267']").click()
    time.sleep(2)
    action = ActionChains(driver)
    #Calling drop-down menu(Power)
    elem=driver.find_element(By.CSS_SELECTOR,"a.btn.btn-primary.dropdown-toggle").click()
    action.move_to_element(elem).click()
    driver.find_element(By.LINK_TEXT,"Power off").click()
    time.sleep(4)
    #Allert button success
    driver.find_element(By.CSS_SELECTOR,"button.btn.btn-success").click()
    #declare instruction for observer while vm is in one of two exsistanse states
    def waiting_for(driver,instruction):
        try:
            def routine(driver):
                elem = driver.find_element(By.XPATH,"//tr[@id='row-186267']")
                try:
                    status = elem.find_element(By.CSS_SELECTOR,instruction)
                    return False
                except:
                    return elem
            tmp = WebDriverWait(driver,60).until(routine)
            print 'OFFLANE'
        except:
            raise NoSuchElementException("Test_VM1 doest offlane")

    waiting_for(driver,'td.status.status-stopping')
    time.sleep(2)
    #Return to Statistics page
    navigation_option_panel(driver,"Statistics")
    time.sleep(2)
    options_statistics(driver)
    #checking graph tendense to zero
    #collecting and compare avg values with not recently gog data,if new avg > old avg IOError,cond ten
    def routine(driver,param,period,cond):
        init_time = 0;
        recently_vals = param
        while init_time!=180:
            init_time+=period
            time.sleep(period-5)
            driver.refresh()
            time.sleep(3)
            check_val=func_to_demonstrate_avg_values(driver)
            aggregation_val = []
            for val1,val2 in zip(recently_vals,check_val):
                if(val2>val1):
                    if(cond==0):
                        raise IOError()
                    else:
                        aggregation_val.append(val2)
                else:
                    if(cond==0):
                        aggregation_val.append(val2)
                    else:
                        raise IOError()
            recently_vals = list(aggregation_val)
        return recently_vals

    #evry 20 sec
    previous = func_to_demonstrate_avg_values(driver)
    routine(driver,previous,20,0)
    navigation_option_panel(driver,"Virtual servers")
    driver.find_element(By.XPATH,"//tr[@id='row-186267']").click()
    time.sleep(2)
    action=ActionChains(driver)
    elem=driver.find_element(By.CSS_SELECTOR,"a.btn.btn-primary.dropdown-toggle").click()
    action.move_to_element(elem).click()
    driver.find_element(By.LINK_TEXT,"Power on").click()
    waiting_for(driver,'td.status.status-running')
    time.sleep(2)
    navigation_option_panel(driver,"Statistics")
    time.sleep(2)
    options_statistics(driver)
    previous = func_to_demonstrate_avg_values(driver)
    routine(driver,previous,20,1)
    time.sleep(10)


#44 We can also check by verifying information from Virtual servers on VM1 link where we can see our PUBLIC
def checking_port_availability(driver):
    option_panel(driver)
    navigation_option_panel(driver,'Virtual servers')
    driver.find_element(By.LINK_TEXT,'TEST_VM1').click()
    time.sleep(5)
    #Check Public ip in TEST_VM1 information page
    ip_addr=driver.find_elements(By.XPATH,"//*[contains(text(),'Public IP')]")[1].find_element(By.XPATH,'..').find_elements(By.CSS_SELECTOR,'td')[1].text
    driver.back()
    move_to_vm_console(driver)
    main_wind = driver.window_handles[0]
    second = driver.window_handles[1]
    driver.switch_to_window(second)
    console=console_perfomance(driver)
    time.sleep(5)
    #Execute commands
    console.send_keys("yum install -y map")
    console.send_keys(Keys.ENTER)
    time.sleep(100)
    console.send_keys("nmap "+str(ip_addr))
    time.sleep(20)


#45
def delete_rule(driver):
    option_panel(driver)
    driver.find_element(By.XPATH,"//tr[@id='row-186267']").click()
    driver.find_element(By.LINK_TEXT,"Reconfigure").click()
    time.sleep(2)
    switch_cont=driver.find_element(By.XPATH,"//iframe")
    driver.switch_to_frame(switch_cont)
    driver.find_element_by_partial_link_text('Firewall').click()
    time.sleep(20)
    print driver.find_element(By.XPATH,"//input[@data-column='5']").send_keys('21')
    time.sleep(3)
    driver.find_element_by_css_selector('button.btn.btn-danger.btn-xs.remove-rule').click()
    time.sleep(2)
    driver.switch_to_alert().accept()
    time.sleep(1)
    driver.switch_to_default_content()
    driver.find_element(By.XPATH,"//button[@id='createButton']").click()
    time.sleep(2)



class Lattelecom(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        # Open web page
        self.driver.get("http://my-ru.lattelecomcloud.com.web.test.qa.lattelecomcloud.com/")
        log_in(self.driver)
        assert 'Wrong e-mail or password entered' not in self.driver.page_source
        assert 'You failed reCaptcha test, please try again' not in self.driver.page_source
        assert 'My subscriptions' in self.driver.title
        #Open catalog
        self.driver.find_element_by_link_text('CATALOG').click()
        time.sleep(3)



    def test_44_available_port(self):
        checking_port_availability(self.driver)

    def test_45_delete_rule(self):
        delete_rule(self.driver)

    def test_46_upload(self):
        upload_instruction(self.driver)

    def test_47_avalaibility(self):
        check_vm_image(self.driver,'Attach')

    def test_48_inaccessibility(self):
        check_vm_image(self.driver,'Detach')

    def test_49_destroy(self):
        delete_image(self.driver)

    def test_50_statistics(self):
         check_statistics_with_conditions(self.driver)


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
