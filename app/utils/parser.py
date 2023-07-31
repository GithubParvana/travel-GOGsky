from bs4 import BeautifulSoup
import requests
import pandas as pd


def parser(link):
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
        hotels_name = i.find_all('td', attrs={'class', 'link-hotel'})
        for instance in hotels_name:
            hotel_name = instance.text.strip()
        for instance in i:
            if "ROOM" in instance.text:
                room_type = instance.text.strip()
            elif "STANDARD" in instance.text:
                room_type = instance.text.strip()
        hotels_price = i.find_all('td', attrs={'class', 'td_price'})
        for instance in hotels_price:
            hotel_price = instance.text.strip()
            hotel_name_without_usd = int(float(hotel_price.strip('USD')))

            def is_what_percent_of(num_a, num_b):
                return int((num_a / 100) * num_b)

            discount_amount = is_what_percent_of(hotel_name_without_usd, 3)
            new_price = hotel_name_without_usd - discount_amount
        if hotel_name is not None:
            hotels_name_list.append(hotel_name)
            rooms_type_list.append(room_type)
            hotels_price_list.append(hotel_price)
            new_prices_list.append(new_price)
    d = {'Hotel name': hotels_name_list,
         'Room type': rooms_type_list,
         'Hotel price': hotels_price_list,
         'Discounted price': new_prices_list, }
    df = pd.DataFrame(data=d)

    return df.to_excel('report.xlsx')
