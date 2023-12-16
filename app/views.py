import os
from . forms import LinkForm
from django.shortcuts import render, HttpResponse
from app.utils.parser import parser,selfieparser,kompasparser, pegastour,fstravel_parser
from django.conf import settings
import time

def home(request):
   
    context = {
        'queryset':[]
    }
    if request.method == 'POST':
        data = request.POST
        adult = data.get('adult')
   
        # queryset = parser(data)
        queryset = pegastour(data)
        # queryset = queryset + selfieparser(data)
        # queryset = queryset + kompasparser(data)
        # queryset = queryset + fstravel_parser(data)
       
        
        for x in range(len(queryset)):
            queryset[x]['adult'] = adult
        sorted_data = sorted(queryset, key=lambda x: int(float(x['price'])))
 
        context['queryset'] = sorted_data
        return render(request,'hotel-list-2.html', context)
    return render(request, 'hotel-list-2.html', context)











# def myAI(Date=None,Tour=None,Hotel=None):
    
#     driver = webdriver.Chrome()
#     driver.get("http://online.kompastour.kz/search_tour")
#     wait = WebDriverWait(driver, 10)
    
#     time.sleep(5)
    
#     close_button = driver.find_element(By.CLASS_NAME, "close")
#     close_button.click()
    
#     time.sleep(5)
    
#     enddate_input = driver.find_element(By.CSS_SELECTOR, ".frm-input.date.CHECKIN_END")
#     startdate_input = driver.find_element(By.CSS_SELECTOR, ".frm-input.date.CHECKIN_BEG")
    
#     # enddate_input.clear()
#     # enddate_input.send_keys('10.08.2023')
    
#     time.sleep(3)
    
#     # startdate_input.clear()
#     # startdate_input.send_keys('12.08.2023')
    
#     time.sleep(5)
    
#     search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".load")))
#     search_button.click()
    
#     time.sleep(6)
    
#     link_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="samo-link-to-page"]/a[2]')))
#     link_element.click()
    
#     time.sleep(3)
    
#     textarea_element = wait.until(EC.presence_of_element_located((By.ID, 'copyto')))
#     textarea_text = textarea_element.get_attribute("value")

#     return textarea_text


