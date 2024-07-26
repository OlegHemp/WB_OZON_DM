"""
Можно менять пути для файлов.
reference_wb - путь к файлу с сылками WB;
reference_wb - путь к файлу с сылками OZON;
reference_wb - путь к файлу с сылками DM;
data_folder - путь к папке с выгруженными данными.
"""

work_path = {"reference_wb": r"/home/ohemp/PycharmProjects/parsing/WB_OZON_DM/links_wb.txt",
             "reference_oz": r"/home/ohemp/PycharmProjects/parsing/WB_OZON_DM/links_oz.txt",
             "reference_dm": r"/home/ohemp/PycharmProjects/parsing/WB_OZON_DM/links_dm.txt",
             "data_folder": r"./data",
             }

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
           }
ua_selenium = "User-Agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0"

