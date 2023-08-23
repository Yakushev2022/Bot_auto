import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import My_keys as key
#import time
import json


def request_page(i):
    ua = UserAgent()
    fake_ua = {'user-agent': ua.random}
    proxy = {
               'http': f'socks5://0R6Q3J:{key.proxy_ID}@45.133.35.176:8000',
               'https': f'socks5://0R6Q3J:{key.proxy_ID}@45.133.35.176:8000'
    }

    url = f'https://auto.ru/moskva/cars/nissan/terrano/20145592/all/?page={i}'
    headers = {
       # 'user-agent': f'fake_ua',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "cookie": "_ym_uid=1616617239979817255; _ga=GA1.2.2052040551.1616617240; gdpr=0; yandexuid=1497039261545935261; rounded-banner-shown=true; notification_yandex_auth_suggest_closed=true; hide-proauto-pimple=1; i=JiixHMidktkEDl3QYEQF+vosGyRlM+puIJ/nB2GRz2WaNHTyFI8sgSCnlH7RPGbBB9Qd+5SeDKgzDjAFiXuMoyKeEyA=; suid=855aff9dfb4dd032fa84e41208c72396.49261beed911d5e1038f92e823ebd560; _csrf_token=137e950e8c01391037e56fec7a079e62bdacbe66b4481979; autoru_sid=48303374%7C1686151635534.7776000.ahZ7KB4Sqkyie_1Oe4OsVQ.DLp2eQ8a7Rpz6-9UPC67Ez9nyOWU4ypEtDHKQzvClAE; from=direct; autoruuid=g638e346128oti9nru4qi4g83l5hu5nj.908db0975dc0e123a5217942d9f89d7a; gids=; gradius=200; my=YwA=; L=WkB+Bnxnb09oAkxxYVpVbmxFSQVkXmhUBkQCNhINJBoQJQ==.1619160905.14580.314360.035b64b7406c33c41c15fd27bec59024; _ym_isad=2; mindboxDeviceUUID=667dc8fc-b8f0-4ac3-b050-79642181011c; directCrm-session=%7B%22deviceGuid%22%3A%22667dc8fc-b8f0-4ac3-b050-79642181011c%22%7D; autoru_sso_blocked=1; _yasc=PeJeJfmae5hdKn/ZMlc5iptNe8XRLw4x6xqchb2sTyLJXtaCKK27l0h1Cu8sLQ==; Session_id=3:1692107178.5.0.1619160905653:mP1FgA:2b.1.2:1|176916829.0.2|61:10015424.507930.fzEX9LluMGlLBaw2MF2bHFGhvZI; sessar=1.1181.CiDU0E5-_c8jZiSjJ-w-xIwcIVJJjQ9psI_p9PkcLDZ0fA.5jPV2Jv0T9vUSezQ-m630rYJD97WDC0QTA3bzkzf3iA; ys=udn.cDpPcGVsS29tcmFk#c_chck.1745766177; mda2_beacon=1692107178388; sso_status=sso.passport.yandex.ru:synchronized; count-visits=1; yaPassportTryAutologin=1; layout-config={\"screen_height\":768,\"screen_width\":1366,\"win_width\":677.3333129882812,\"win_height\":802.6666870117188}; from_lifetime=1692107235516; _ym_d=1692107235; cycada=T32MvGZvVFGDNuqzbTprH1kfR+GSG84jstUTSesXTEg=",
        "Referer": "https://sso.auto.ru/",
        "Referrer-Policy": "no-referrer-when-downgrade"
    }
    s = requests.Session()
    response = s.get(url=url, headers=headers, proxies=proxy)
    response.encoding = 'utf-8'
    soup = BS(response.text, 'lxml')
    return soup
def page_max(soup):
    pages = [x.text.strip() for x in soup.find_all('span', class_="ControlGroup ControlGroup_responsive_no ControlGroup_size_s ListingPagination__pages")]
    n_page = [x for x in pages[-1]]
    return n_page

i=1
soup = request_page(i)
#print(soup.prettify())
k =int(page_max(soup)[-1])


#result_json=[]
def creating_dict():
    year = [x.text.strip() for x in soup.find_all('div', class_="ListingItem__year")]
    Km_item = [x.text.strip() for x in soup.find_all('div', class_="ListingItem__kmAge")]
    url_address_item = [x['href'] for x in soup.find_all('a', class_="Link ListingItemTitle__link")]
    param = [x.text.strip() for x in soup.find_all('div', class_="ListingItemTechSummaryDesktop__cell")]
    price = [x.text.strip().split(' ') for x in soup.find_all('div', class_='ListingItem__priceBlock')]
    # Преобразуем данные о машине
    V_eng = [par.split('/')[0] for i, par in enumerate(param, 0) if i in range(0, len(param), 5)]
    W_eng = [par.split('/')[1] for i, par in enumerate(param, 0) if i in range(0, len(param), 5)]
    type_eng = [par.split('/')[2] for i, par in enumerate(param, 0) if i in range(0, len(param), 5)]
    Transmission = [par for i, par in enumerate(param, 0) if i in range(1, len(param), 5)]
    Gear = [par for i, par in enumerate(param, 0) if i in range(3, len(param), 5)]
    Color = [par for i, par in enumerate(param, 0) if i in range(4, len(param), 5)]

    # Скидки и цены идут вместе, разделяем их
    lst_price = []  # Список цен
    lst_skid = []  # список цен со скидкой
    for item in (price):
        if 'Цена' in item[0]:
            lst_price.append(item[0].split('Цена')[0])
            lst_skid.append('NaN')
        else:
            lst_price.append(item[0])
            if len(item) == 2:

                if 'НДС' in item[1]:  # .split('Цена'):
                    lst_skid.append(item[1].split('Цена')[0])
                else:
                    lst_skid.append(item[1])
            else:
                lst_skid.append('NaN')

    global result_json
    result_json=[]
    for Y, K, V, W, T_p, Tr, G, C, P, P_s, U in zip(year, Km_item, V_eng, W_eng, type_eng,
                                                  Transmission, Gear, Color, lst_price, lst_skid, url_address_item):
        result_json.append({
            'Год':Y,
            'Пробег':K,
            'Обьем дв':V,
            'Мощность дв':W,
            'Тип дв':T_p,
            'Трансмиссия':Tr,
            'Тип привода':G,
            'Цвет':C,
            'Цена':P,
            'Скидочная цена':P_s,
            'URL':U
        })
    with open('res.json', 'w', encoding='utf-8') as file:
        json.dump(result_json, file, indent=4, ensure_ascii=False)
    #return result_json

#lst_choice_json = []
def filter_dict(Age_from, Age_for, Mileage):
    global lst_choice_json
    lst_choice_json = []
    for item in result_json:
        if int(item['Год']) >= Age_from and int(item['Год']) <= Age_for and \
                int(item['Пробег'][0:-2].replace('\xa0', "")) <= Mileage:
            lst_choice_json.append(item)
    with open('filter_json.json', 'w', encoding='utf-8') as file:
         json.dump(lst_choice_json, file, indent=4, ensure_ascii=False)
    return lst_choice_json

Age_from = 2014
Age_for = 2022
Mileage = 150000

print(k)
creating_dict()
filter_dict(Age_from, Age_for, Mileage)
