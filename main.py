from pathlib import Path
import config
import logging
from bs4 import BeautifulSoup as bs
from auxiliary_tool import read_file, write_file, save_json, load_json, get_response
import json
import tqdm
import datetime
import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
today = datetime.datetime.today()
current_date = today.strftime("%d-%m-%Y")
title = ["reference_wb", "reference_oz", "reference_dm"]
data_folder = Path(config.work_path["data_folder"])
referenses = {}
chrome_options = Options()
chrome_options.add_argument(config.ua_selenium)


def input_data():
    """
    Подготовка входных данных.
    Проверка наличия директории data_folder и файлов с сылками.
    Проверка ссылок на наличие 'https://.....'
    Для озона, сокращение ссылок.
    :return: Словарь списков ссылок на требуемые сайты.
    """
    ref = {}
    if not data_folder.exists():
        data_folder.mkdir()
    for name in title:
        reference_list = Path(config.work_path[name])
        if not reference_list.is_file():
            logging.warning(f"{reference_list} нет такого файла или такого пути к нему не существует!")
            exit("Завершение программы")
        if name == title[1]:
            ref[name] = [url.split(r"/?")[0] for url in read_file(reference_list).split() if
                         url.startswith("https://www.ozon.ru")]
        else:
            ref[name] = [url for url in read_file(reference_list).split()
                         if url.startswith("https://www.wildberries.ru") or url.startswith("https://www.detmir.ru")]
    return ref


def get_id(link: str) -> str:
    """WB - получение ID из ссылки"""
    return link.split("/")[-2]


def resp_wb(reference: list, title: str) -> dict:
    """
    Парсинг WB. Получение цены, скидки, СПП из API запроса.
    :param reference: список подготовленных ссылок
    :param title: ключ для словаря result
    :return: Словарь списков.
    """
    result = {title: []}
    count = 0
    try:
        for entry in tqdm.tqdm(reference, desc='Парсинг wildberries.ru', colour="green"):
            count += 1
            if count > 100:
                time.sleep(0.6)
                count = 0
            link_json = f"https://card.wb.ru/cards/detail?appType=1&curr=rub&spp=30&nm={get_id(entry)}"
            req = get_response(link_json, {}, config.headers)
            req_dict = json.loads(req)["data"]["products"][0]
            priceu = 0
            bpriceu = 0
            cpriceu = 0
            if "priceU" in req_dict.keys():
                priceu = req_dict["priceU"] // 100
                bpriceu = req_dict["extended"]["basicPriceU"] // 100
                cpriceu = req_dict["extended"]["clientPriceU"] // 100
            result[title].append({"url": entry,
                                  "date": current_date,
                                  "price_before_discount": priceu,
                                  "discounted_price": bpriceu,
                                  "cpp": cpriceu})
    except Exception as e:
        logging.error(f" Парсинг wildberries.ru закончился неудачей.\n {entry} \n {e}")
    return result


def resp_oz(reference: list, title: str) -> dict:
    result = {title: []}
    count = 0
    try:
        for entry in tqdm.tqdm(reference, desc='Парсинг ozon.ru', colour="green"):
            count += 1
            if count > 100:
                time.sleep(0.6)
            # browser = webdriver.Chrome(chrome_options, executable_path="C:\python_project\parsers\WB_OZON_DM\chromedriver.exe")
            browser = webdriver.Chrome(options=chrome_options)
            time.sleep(0.1)
            browser.get(entry)
            time.sleep(0.3)
            current_page = browser.page_source
            write_file(data_folder / "temp.html", current_page)
            browser.quit()
            html = read_file(data_folder / "temp.html")
            soup = bs(html, "lxml")
            price = []
            try:
                price = soup.find("div", slot="content").findAll("span", string=re.compile(r"₽"))
            except Exception as e:
                logging.error(f"\n Вероятно товар закончился. \n {entry} \n {e}")
            black_price = 0
            red_price = 0
            if len(price) == 1:
                black_price = price[0].get_text()[:-2].replace("\u2009", "")
            if len(price) == 2:
                black_price = price[1].get_text()[:-2].replace("\u2009", "")
                red_price = price[0].get_text()[:-2].replace("\u2009", "")
            result[title].append({"url": entry,
                                  "date": current_date,
                                  "price_before_discount": black_price,
                                  "discounted_price": red_price,
                                  "cpp": "-", })
    except Exception as e:
        logging.error(f" Парсинг ozon.ru закончился неудачей. \n {e}")
    return result


def resp_dm(reference: list, title: str) -> dict:
    result = {title: []}
    count = 0
    for entry in tqdm.tqdm(reference, desc='Парсинг detmir.ru', colour="green"):
        count += 1
        if count > 100:
            time.sleep(0.6)
        html = get_response(entry, {}, config.headers)
        soup = bs(html, "lxml")
        big_price = soup.find("div", string=re.compile(r"₽")).get_text()
        big_price = big_price[0:-2].replace("\u2009", "")
        small_price = 0
        try:
            small_price = soup.find("span", string=re.compile(r"₽")).get_text()
            small_price = small_price[0:-2].replace("\u2009", "")
            small_price, big_price = big_price, small_price
        except:
            pass
        time.sleep(0.1)
        result[title].append({"url": entry,
                              "date": current_date,
                              "price_before_discount": big_price,
                              "discounted_price": small_price,
                              "cpp": "-", })
    return result


def out_csv(catalog: dict, site: list):
    file_path = data_folder / "output.csv"
    with file_path.open(mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["url", "date", "price_before_discount", "discounted_price", "cpp"], delimiter=';')
        writer.writeheader()
        for elem in site:
            writer.writerows(catalog[elem])
    logging.info(f"SCV файл сохранён: {file_path}")


def main():
    catalog = {}
    save_json(data_folder / "ref.json", input_data())
    ref = load_json(data_folder / "ref.json")
    wb = resp_wb(ref[title[0]], title[0])
    #wb = {title[0]: []}
    oz = resp_oz(ref[title[1]], title[1])
    dm = resp_dm(ref[title[2]], title[2])
    catalog = catalog | wb | oz | dm
    save_json(data_folder / "output.json", catalog)
    catalog = load_json(data_folder / "output.json")
    out_csv(catalog, title)


if __name__ == '__main__':
    main()
