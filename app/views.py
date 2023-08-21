import os
from . forms import LinkForm
from django.shortcuts import render, HttpResponse
from app.utils.parser import parser,selfieparser,kompasparser
from django.conf import settings
import time

def home(request):
   
    context = {
        'queryset':[]
    }
    if request.method == 'POST':
        data = request.POST
        adult = data.get('adult')
        queryset = parser(data)
        queryset = queryset + selfieparser(data)
        queryset = queryset + kompasparser(data)
        for x in range(len(queryset)):
            queryset[x]['adult'] = adult
        sorted_data = sorted(queryset, key=lambda x: int(float(x['price'])))
        print('000000000000000000000000000000000000000000000000000000000000000')
        context['queryset'] = sorted_data
        return render(request,'hotel-list-2.html', context)
    return render(request, 'hotel-list-2.html', context)

def index(request):
    form = LinkForm(request.POST)
    link = "https://summertour.az/search_tour?TOWNFROMINC=1930&STATEINC=9&CHECKIN_BEG=20230818&NIGHTS_FROM=7&CHECKIN_END=20230819&NIGHTS_TILL=7&ADULT=2&CURRENCY=2&CHILD=0&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&PRICEPAGE=1&DOLOAD=1"

    if request.method == 'POST':
        
        # link = request.POST.get('link')
        data = request.POST
        
        # link = myAI()
        # link = request.POST.get('link')
        
        if 'summertour.az' in link:  
            a=1
            data = parser(data)
            b =data
            
            print(data,'-0------------------------------------------------------------')
        elif 'selfietravel' in link:

            a=2
            data = selfieparser(link)
            
        elif 'kompas' in link:

            a=3
            data = kompasparser(link)

        if a==1:
            with open(f"{settings.BASE_DIR}/report.xlsx", "rb") as excel:
                data = excel.read()
                                        
                response = HttpResponse(data, content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
                time.sleep(1)

        if a==2:
            with open(f"{settings.BASE_DIR}/selfietravlereport.xlsx", "rb") as excel:
                data = excel.read()
                                        
                response = HttpResponse(data, content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
                time.sleep(1)

        if a==3:
            with open(f"{settings.BASE_DIR}/kompasreport.xlsx", "rb") as excel:
                data = excel.read()
                                        
                response = HttpResponse(data, content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
                time.sleep(1)


        if a==1:
            os.remove(f"{settings.BASE_DIR}/report.xlsx")
        if a==2:
            os.remove(f"{settings.BASE_DIR}/selfietravlereport.xlsx")  
        if a==3:
            os.remove(f"{settings.BASE_DIR}/kompasreport.xlsx")  
        print(b)
        context = {'form': form,'data':b,'options':set(x['hotel'] for x in b)}
        

        return render(request, 'index.html',context)
    
    context = {'form': form}
    
    return render(request, 'index.html', context)


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


