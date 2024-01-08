from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from datetime import datetime


def process_number(num):
    if isinstance(num, int) or (isinstance(num, str) and num.isdigit()):
        num_str = str(num)
        if len(num_str) == 1:
            return num
        else:
            return '+'.join(num_str)
    else:
        return "Invalid input"

def multiply_currency_value(value_str):

    numeric_part, currency_code = value_str.split(' ')

    numeric_value = float(numeric_part)

    # Multiply the numeric value by the factor
    multiplied_value = numeric_value 

    # Format the result back into the original format
    result_str = f"{multiplied_value:.2f}"
    
    return result_str
# https://summertour.az/search_tour?TOWNFROMINC=1930&STATEINC=9
# &CHECKIN_BEG=20230818&NIGHTS_FROM=7&CHECKIN_END=20230819&NIGHTS_TILL=7&ADULT=2
# &CURRENCY=2&CHILD=0&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&PRICEPAGE=1&DOLOAD=1

# https://summertour.az/search_tour?TOWNFROMINC=1930&STATEINC=9&
# TOURINC=93&CHECKIN_BEG=20230823&
# NIGHTS_FROM=7&CHECKIN_END=20230831&NIGHTS_TILL=7&ADULT=2&CURRENCY=2&CHILD=0&TOWNS_ANY=1&
# STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&FREIGHT=1&FILTER=1&PARTITION_PRICE=224&PRICEPAGE=1&DOLOAD=1

# https://summertour.az/search_tour?TOWNFROMINC=1930&STATEINC=9&CHECKIN_BEG=20230823&NIGHTS_FROM=2&
# CHECKIN_END=20230831&NIGHTS_TILL=7&ADULT=2&CURRENCY=2&CHILD=0&TOWNS=NaN%2C1959%2C1968%2C1962%2C1966%
# 2C1967%2C1960%2C1965%2C1963%2C1961%2C1964%2CNaN%2C1179%2C1432%2C1433%2CNaN%2C1947%2C1948%2CNaN%2C1973%
# 2C1970%2C1975%2C1974%2C1976%2C1979%2C1977%2C1981%2C1984%2C1978%2C1969%2C1983%2C1982%2C1980%2CNaN%2C1985%
# 2CNaN%2C2009%2C2001%2C2006%2C2008%2C2010%2C2007%2C2017%2C1999%2C2013%2C2022%2C2005%2C2072%2C2000%2C2002%2C2018%2C2003%2C1997
# %2C1998%2C2004&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&FREIGHT=1&FILTER=1&PRICEPAGE=1&DOLOAD=1

def parser(data):
    # link=data.get('link')
    
    print(data)

    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').strftime('%Y%m%d')
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').strftime('%Y%m%d')
    nights_start = str(data.get('nights_start'))
    nights_end = str(data.get('nights_start'))
    adult = str(data.get('adult'))
    child = str(data.get('child'))
    cost_min = str(data.get('cost_min'))
    cost_max = str(data.get('cost_max'))
    towns_any = str(data.get('towns_any'))
    link = f'https://summertour.az/search_tour?TOWNFROMINC=1930&STATEINC=9&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY={towns_any}&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&FREIGHT=1&FILTER=1&PRICEPAGE=1&DOLOAD=1'
    print(link)
    a = []
    http_request = requests.get(link)
    html = http_request.content
    parsed_html = BeautifulSoup(html, 'html.parser')
    z = parsed_html.find_all('tr', )
    hotels_name_list = []
    rooms_type_list = []
    hotels_price_list = []
    new_prices_list = []
    print(z,'z')
    for i in z:
        hotel_name = None
        room_type = None
        hotel_price = None
        new_price = None
        hotel_name_without_usd = None

        hotels_name = i.find_all('td', attrs={'class', 'link-hotel'})
        for instance in hotels_name:
            hotel_name = instance.text.strip()

        for instance in i:
            print(instance,'instance')
            if "ROOM" in instance.text:
                room_type = instance.text.strip()
            elif "STANDARD" in instance.text:
                room_type = instance.text.strip()
            elif "ECO" in instance.text:
                room_type = instance.text.strip()
            elif "Standard" in instance.text:
                room_type = instance.text.strip()
        hotels_price = i.find_all('td', attrs={'class', 'td_price'})

        for instance in hotels_price:
            hotel_price = instance.text.strip()
            hotel_name_without_usd = int(float(hotel_price.strip('USD')))

            def is_what_percent_of(num_a, num_b):
                return int((num_a / 100) * num_b)

            discount_amount = is_what_percent_of(hotel_name_without_usd, 3)
            new_price = hotel_name_without_usd - discount_amount
        nights = i.find_all('td', attrs={'class', 'c'})
        if len(nights)>0:
            night = process_number(nights[0].text.strip())
        else:
            night = 0
        if hotel_name is not None:
            hotels_name_list.append(hotel_name)
            rooms_type_list.append(room_type)
            # hotels_price_list.append(hotel_price)
            hotels_price_list.append(hotel_name_without_usd)
            new_prices_list.append(new_price)
            a.append({'hotel':hotel_name,'roomtype':room_type,'price':hotel_name_without_usd,'discounted_price':new_price,'night':night})
    d = {'Hotel name': hotels_name_list,
         'Room type': rooms_type_list,
         'Hotel price': hotels_price_list,
         'Discounted price': new_prices_list}
   
    df = pd.DataFrame(data=d)
    df.to_excel('report.xlsx')
 
    return a



def selfieparser(data):
    
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').strftime('%Y%m%d')
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').strftime('%Y%m%d')
    nights_start = str(data.get('nights_start'))
    nights_end = str(data.get('nights_start'))
    adult = str(data.get('adult'))
    child = str(data.get('child'))
    cost_min = str(data.get('cost_min'))
    cost_max = str(data.get('cost_max'))
    link =f'http://b2b.selfietravel.kz/search_tour?LANG=eng&TOWNFROMINC=1930&STATEINC=9&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=6&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&PRICEPAGE=1&DOLOAD=1'
    print(link)
    a = []
    http_request = requests.get(link)
    html = http_request.content
    parsed_html = BeautifulSoup(html, 'html.parser')
    z = parsed_html.find_all('tr', )
    hotels_name_list = []
    rooms_type_list = []
    hotels_price_list = []
    new_prices_list = []
    for i in z:
        hotel_name = None
        room_type = None
        hotel_price = None
        new_price = None
        hotel_name_without_usd = None

        hotels_name = i.find_all('td', attrs={'class', 'link-hotel'})
        for instance in hotels_name:
            hotel_name = instance.text.strip()

        for instance in i:
            print(instance)
            if "Dbl" in instance.text:
                room_type = instance.text.strip()
            elif "Standard" in instance.text:
                print(instance)
                room_type = instance.text.strip()
            elif "STANDARD" in instance.text:
                room_type = instance.text.strip()
        hotels_price = i.find_all('td', attrs={'class', 'td_price'})

        for instance in hotels_price:
            hotel_price = instance.text.strip()
            hotel_name_without_usd = multiply_currency_value(hotel_price)
            

            
        nights = i.find_all('td', attrs={'class', 'c'})
        if len(nights)>0:
            night = process_number(nights[0].text.strip())
        else:
            night = 0
        if hotel_name is not None:
            hotels_name_list.append(hotel_name)
            rooms_type_list.append(room_type)
            # hotels_price_list.append(hotel_price)
            hotels_price_list.append(hotel_name_without_usd)
            new_prices_list.append(new_price)
            a.append({'hotel':hotel_name,'roomtype':room_type,'price':hotel_name_without_usd,'discounted_price':new_price,'night':night})
    d = {'Hotel name': hotels_name_list,
         'Room type': rooms_type_list,
         'Hotel price': hotels_price_list,
         'Discounted price': new_prices_list}
   
    df = pd.DataFrame(data=d)
    df.to_excel('report.xlsx')
 
    return a


def kompasparser(data):
    
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').strftime('%Y%m%d')
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').strftime('%Y%m%d')
    nights_start = str(data.get('nights_start'))
    nights_end = str(data.get('nights_start'))
    adult = str(data.get('adult'))
    child = str(data.get('child'))
    cost_min = str(data.get('cost_min'))
    cost_max = str(data.get('cost_max'))
    link =f'https://online.kompastour.kz/search_tour?TOWNFROMINC=1411&STATEINC=17&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&FREIGHT=1&FILTER=1&PRICEPAGE=1&DOLOAD='
    print(link)
    a = []
    http_request = requests.get(link)
    html = http_request.content
    parsed_html = BeautifulSoup(html, 'html.parser')
    z = parsed_html.find_all('tr', )
    hotels_name_list = []
    rooms_type_list = []
    hotels_price_list = []
    new_prices_list = []
    for i in z:
        hotel_name = None
        room_type = None
        hotel_price = None
        new_price = None
        hotel_name_without_usd = None

        hotels_name = i.find_all('td', attrs={'class', 'link-hotel'})
        for instance in hotels_name:
            hotel_name = instance.text.strip()

        for instance in i:
            print(instance)
            if "ECO" in instance.text:
                room_type = instance.text.strip()
            elif "Standard" in instance.text:
                room_type = instance.text.strip()
            elif "STANDARD" in instance.text:
                room_type = instance.text.strip()
            elif "DELUXE" in instance.text:
                room_type = instance.text.strip()
        hotels_price = i.find_all('td', attrs={'class', 'td_price'})

        for instance in hotels_price:
            hotel_price = instance.text.strip()
            hotel_name_without_usd = multiply_currency_value(hotel_price)
            

            
        nights = i.find_all('td', attrs={'class', 'c'})
        if len(nights)>0:
            night = process_number(nights[0].text.strip())
        else:
            night = 0
        if hotel_name is not None:
            hotels_name_list.append(hotel_name)
            rooms_type_list.append(room_type)
            # hotels_price_list.append(hotel_price)
            hotels_price_list.append(hotel_name_without_usd)
            new_prices_list.append(new_price)
            a.append({'hotel':hotel_name,'roomtype':room_type,'price':hotel_name_without_usd,'discounted_price':new_price,'night':night})
    d = {'Hotel name': hotels_name_list,
         'Room type': rooms_type_list,
         'Hotel price': hotels_price_list,
         'Discounted price': new_prices_list}
   
    df = pd.DataFrame(data=d)
    df.to_excel('report.xlsx')
 
    return a


# ---------------------------------------------------


def pegastour(data):
     
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').strftime('%Y%m%d')
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').strftime('%Y%m%d')
    nights_start = str(data.get('nights_start'))
    nights_end = str(data.get('nights_start'))
    adult = str(data.get('adult'))
    child = str(data.get('child'))
    cost_min = str(data.get('cost_min'))
    cost_max = str(data.get('cost_max'))
    # link =f'https://online.kompastour.kz/search_tour?TOWNFROMINC=1411&STATEINC=17&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&FREIGHT=1&FILTER=1&PRICEPAGE=1&DOLOAD='
    link = f'http://pegast.az/pegasyssearchtour'
    
    
    print(link)
    a = []
    http_request = requests.get(link)
    html = http_request.content
    parsed_html = BeautifulSoup(html, 'html.parser')
    z = parsed_html.find_all('tr', )
    hotels_name_list = []
    rooms_type_list = []
    hotels_price_list = []
    new_prices_list = []
    for i in z:
        hotel_name = None
        room_type = None
        hotel_price = None
        new_price = None
        hotel_name_without_usd = None

        hotels_name = i.find_all('td', attrs={'class', 'hotel-column'})
        for instance in hotels_name:
            hotel_name = instance.text.strip()

        for instance in i:
            print(instance)
            if "Double Room" in instance.text:
                room_type = instance.text.strip()
                # print('tripleeeeeeeeeeeeeeeeeeeeee')
            elif "Standard Room" in instance.text:
                room_type = instance.text.strip()
            elif "Economy Room." in instance.text:
                room_type = instance.text.strip()
            elif "Eco Room" in instance.text:
                room_type = instance.text.strip()
        hotels_price = i.find_all('td', attrs={'class', 'price-column'})

        for instance in hotels_price:
            hotel_price = instance.text.strip()
            hotel_name_without_usd = multiply_currency_value(hotel_price)
            


            
        nights = i.find_all('td', attrs={'class', 'duration-column'})
        if len(nights)>0:
            night = process_number(nights[0].text.strip())
        else:
            night = 0
        if hotel_name is not None:
            hotels_name_list.append(hotel_name)
            rooms_type_list.append(room_type)
            # hotels_price_list.append(hotel_price)
            hotels_price_list.append(hotel_name_without_usd)
            new_prices_list.append(new_price)
            a.append({'hotel':hotel_name,'roomtype':room_type,'price':hotel_name_without_usd,'discounted_price':new_price,'night':night})
    d = {'Hotel name': hotels_name_list,
         'Room type': rooms_type_list,
         'Hotel price': hotels_price_list,
         'Discounted price': new_prices_list}
   
    df = pd.DataFrame(data=d)
    df.to_excel('report.xlsx')
 
    return a






# -----------------------------------------------------------

def fstravel_parser(data):
    tour = str(data.get('tour'))
    qida = str(data.get('food'))
    yer = str(data.get('yer'))
    otel = str(data.get('hotel'))
    unk = str(data.get('unkmown'))
    star = str(data.get('star'))
    city = str(data.get('city'))
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').strftime('%Y%m%d')
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').strftime('%Y%m%d')
    nights_start = str(data.get('nights_start'))
    nights_end = str(data.get('nights_end'))
    adult = str(data.get('adult'))
    child =0
    child = str(data.get('child'))
    child1 = str(data.get('child1age'))
    child2 = str(data.get('child2age'))
    child3 = str(data.get('child3age'))
    cost_min = str(data.get('cost_min'))
    cost_max = str(data.get('cost_max'))
    if child:
        child = child
    else:
        child=0
    print(child)
    if yer == 'Yes':
        if tour :
            if cost_min and cost_max:
                if child:
                    if qida:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        elif star:
                             link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS={star}&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                    else:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS_ANY=1&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1' 
                else:
                    if qida:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        elif star:
                             link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS={star}&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                    else:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS_ANY=1&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1' 
            else:
                if child:
                    if qida:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&CHILD={child}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        elif star:
                             link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&CHILD={child}&TOWNS_ANY=1&STARS={star}&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&CHILD={child}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                    else:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&CHILD={child}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS_ANY=1&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&CHILD={child}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1' 
        
        else:
             if cost_min and cost_max:
                if child:
                    if qida:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        elif star:
                             print("Aytac teacher")
                             link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS={star}&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            print("Aytac")
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS={city}&STARS_ANY=1&HOTELS_ANY=1&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                    else:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS_ANY=1&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1' 
                else:
                    if qida:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        elif star:
                             link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS={star}&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS={qida}&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                    else:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS_ANY=1&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&ROOMS_ANY=1&FREIGHT=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1' 
            
    else: 
         if tour :
            if cost_min and cost_max:
                if child:
                    if qida:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        elif star:
                             link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS={star}&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS={qida}&ROOMS_ANY=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                    else:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS_ANY=1&ROOMS_ANY=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD={child}&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&ROOMS_ANY=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1' 
                else:
                    if qida:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        elif star:
                             link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS={star}&HOTELS={otel}&MEALS={qida}&ROOMS_ANY=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS={qida}&ROOMS_ANY=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                    else:
                        if otel:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS={otel}&MEALS_ANY=1&ROOMS_ANY=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                        else:
                            link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&COSTMIN={cost_min}&CHILD=0&COSTMAX={cost_max}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&ROOMS_ANY=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1' 
            else:
                if child:
                    if qida:
                        link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&CHILD={child}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS={qida}&ROOMS_ANY=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'
                    else:   
                        link =f'https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&TOURINC={tour}&CHECKIN_BEG={start_date}&NIGHTS_FROM={nights_start}&CHECKIN_END={end_date}&NIGHTS_TILL={nights_end}&ADULT={adult}&CURRENCY=2&CHILD={child}&TOWNS_ANY=1&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&ROOMS_ANY=1&FILTER=1&AGES={child1}&PRICEPAGE=1&DOLOAD=1'

    a = []
    print(link)
    http_request = requests.get(link)
    html = http_request.content
    parsed_html = BeautifulSoup(html, 'html.parser')

    z = parsed_html.find_all('tr',attrs={'class', 'price_info'} )
    
    hotels_name_list = []
    rooms_type_list = []
    qida_list  =[]
    hotels_price_list = []
    new_prices_list = []

    
    for i in z:
        hotel_name = None
        room_type = None
        hotel_price = None
        qida = None
        new_price = None
        hotel_name_without_usd = None

        hotels_name = i.find('td', attrs={'class', 'link-hotel'})           
        hotel_name = hotels_name.text.strip()
        td_elements = i.select('td:not([class])')
        qida = td_elements[1].text 
        room_type = td_elements[2].text          
        hotels_price = i.find_all('td', attrs={'class', 'td_price'})

        for instance in hotels_price:
            hotel_price = instance.text.strip()
            hotel_name_without_usd = multiply_currency_value(hotel_price)
            
        nights = i.find_all('td', attrs={'class', 'c'})
        if len(nights)>0:
            night = process_number(nights[0].text.strip())
        else:
            night = 0
        if hotel_name is not None:
            hotels_name_list.append(hotel_name)
            rooms_type_list.append(room_type)
            qida_list.append(qida)
            # hotels_price_list.append(hotel_price)
            hotels_price_list.append(hotel_name_without_usd)
            new_prices_list.append(new_price)
            a.append({'hotel':hotel_name,'roomtype':room_type,'Qida' : qida, 'price':hotel_name_without_usd,'discounted_price':new_price,'night':night})
    d = {'Hotel name': hotels_name_list,
          
         'Room type': rooms_type_list,
         'Hotel price': hotels_price_list,
         'Discounted price': new_prices_list}
   
    # df = pd.DataFrame(data=d)
    # df.to_excel('report.xlsx')
 
    return a






# def trying():
#     data = requests.get("https://b2b.fstravel.asia/search_tour?TOWNFROMINC=433614&STATEINC=18803&CHECKIN_BEG=20240103&NIGHTS_FROM=7&CHECKIN_END=20240103&NIGHTS_TILL=7&ADULT=2&CURRENCY=25&CHILD=0&TOWNS=NaN%2C355153%2C693795%2C789189%2C388026%2C761669%2C386680%2C804429%2C351898%2C304681%2C304684%2C699188%2C704110%2C704101%2C666475%2C695955%2C398914%2C351935%2C439148%2C704079%2C304696%2C666478%2C351913%2C684831%2C400116%2C304702%2C400493%2C304705%2C304708%2C304711%2C304714%2C786956%2C372240%2C761676%2C778930%2C304717%2C786944%2C761679&STARS_ANY=1&HOTELS_ANY=1&MEALS_ANY=1&FREIGHT=1&FILTER=1&PRICEPAGE=1&DOLOAD=1")
#     return data