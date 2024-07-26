# WD_OZON_DM #  
## Введение  ##
Есть задача.  
*"Нужно скрипт чтобы парсить цены с вайлдбериз, озон и Детский мир. По определенному перечню ссылок для каждой площадки. Сохранять в формате ссылка, дата, цена"*  
Да, почему бы и нет?
### Цель ### 
Получить практический опыт работы с библиотеками requests, beautifulsoup4, selenium. Посмотреть, что из себя представляет __CloudFlare__ и __Incapsula__.

### Постановка задачи ###



1. Для каждого сайта (wildberries.ru, ozon.ru, detmir.ru) составлен свой перечень ссылок.

2. Файлы со ссылками - обычные текстовые файлы, где новая строка - новая ссылка на одну позицию товара.   
Например:
```
https://www.wildberries.ru/catalog/119203059/detail.aspx
https://www.wildberries.ru/catalog/140809313/detail.aspx
https://www.wildberries.ru/catalog/18326498/detail.aspx
```

3. Полученные данные сохраниеь в формате ссылка, дата, цена, цена со скидкой, СПП в одном файле в формате csv и в фомате json.   
Например:  
```
https://www.wildberries.ru/catalog/119203059/detail.aspx 18.05.2023 231
https://www.wildberries.ru/catalog/140809313/detail.aspx 18.05.2023 3555
https://www.wildberries.ru/catalog/18326498/detail.aspx 18.05.2023 1122```

4. Важный момент при парсинге цен нужно собирать все цены 
(До скидки, со скидкой и конечную цену которую видит человек с СПП (относится к WB))

### Создано с помощью ###
|                      -                      |                                     Ссылки                                     |                  Описание                   |
|:-------------------------------------------:|:------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------|  
|  <img src="./doc/python.svg" width="50"/>   |                     [Python 3.10](https://www.python.org/)                      | Высокоуровневый язык программирования общего назначения с динамической строгой типизацией и автоматическим управлением памятью                 |  
|                    -                     |           [Модуль Requests](https://requests.readthedocs.io/en/latest/)            | Это инструмент, который используют для составления HTTP-запросов. Библиотека Requests позволяет:  <br/> - создавать запросы посредством наиболее популярных HTTP-методов; <br/> - редактировать заголовки запросов и данных с помощью строки запроса, а также содержимого сообщения; <br> - анализировать данные запросов и откликов; <br> - создавать авторизированные запросы; <br> - настраивать запросы с целью предотвращения сбоев и замедлений в работе приложения. |
|                    -                     |                              [Модуль BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)                              | Это библиотека Python для извлечения данных из файлов HTML и XML. <bs> Для естественной навигации, поиска и изменения дерева HTML, модуль BeautifulSoup4, по умолчанию использует встроенный в Python парсер html.parser. BS4 так же поддерживает ряд сторонних парсеров Python, таких как lxml, html5lib и xml.                                                                                                                                                           |
|  <img src="./doc/lxml.png" width="50"/>  |                              [lxml](https://lxml.de/)                              |это быстрая и гибкая библиотека для обработки разметки XML и HTML на Python. Кроме того, в ней присутствует возможность разложения элементов документа в дерево.|
| <img src="./doc/html5.svg" width="50"/>  |                  [HTML5](https://html.spec.whatwg.org/multipage/)                  | Знание языка гипертекстовой разметки страницы                                                 |-|[Selenium WebDriver](https://www.selenium.dev/)|это инструмент, который позволяет производить кросс-браузерное тестирование, то есть проверять, как отображается сайт в разных браузерах.|                                                                                                                  

## Установка ##
* Создаём виртуальное окружение с помощью venv, позволяющей создавать изолированные среды для отдельных проектов 
Python, решая тем самым проблему зависимостей и совместимости приложений разных версий. Ниже, env - это директория создаётся виртуальное окружение.

### Для Windows:  ###
```
mkdir project
cd project
python -m venv env   
env\Scripts\activate 
```
### В Ubunty/Debian: ### 

```shell  
$ mkdir project
$ cd project
$ python3 -m venv env  
$ . env/bin/activate
```

* Устанавливаем модули из файла зависимостей:  

`pip install -r requirements.txt`  
* Запускаем консольную версию:  

`python main.py`</li> 

* Возможно для драйвера Хрома придётся указать к нему путь в переменных окружения. (У меня, на Windows так заработало). В Linux драйвер Хрома размещаем в `\usr\local\bin`и делаем исполняемым. 
* В файле config.py указать пути до файлов с сылками (3 шт.).

## Описание работы ##
### Реализация ###
#### Структура ####
Программа состоит из 3х основных файлов: 

+ __main.py__ - сам скрипт, который запускаем.

+ __config.py__ - конфигурационный файл, где указываем абсолютный путь к трём файлам со ссылками.

+ __auxiliary_tool.py__ - небольшая библиотечка, облегчающая жизнь.
```
.  
├── auxiliary_tool.py  
├── chromedriver  
│   └── chromedriver.exe  
├── config.py  
├── data  
│   ├── output.csv  
│   ├── output.json  
│   ├── ref.json  
│   └── temp.html  
├── links_dm.txt  
├── links_oz.txt  
├── links_wb.txt  
├── main.py  
├── README.md  
└── requirements.txt  
```
+ links_dm.txt, links_oz.txt, links_wb.txt - файлы со ссылками.  
+ chromedriver.exe - драйвер Хрома для Windows.
+ ref.json - подготовленные к парсингу ссылки.
+ temp.html - временный файл, куда Selenium сохраняет просмотренную страницу.
+ output.csv - файл в формате _csv_ с результатом парсинга.
+ output.json - файл в формате _json_ с результатом парсинга.  

#### Особенности ####
Для озона, выявил ссылки, которые пару дней назад работали, но сейчас не работают, т.к. такой товар отсутствует.
Поэтому в файле csv указаны в ценах нули.

Для WB, нашел ссылки, где запрос к API (https://card.wb.ru/cards/detail?appType=1&curr=rub&spp=30&nm=119203059) должен быть
сложнее, чем этот. Как, он формируется, непонятно, поэтому в файле csv где-то указаны в ценах нули.

Данные сохранены в файл csv и json.

## Используемый материал ##

* [geckodriver](https://github.com/mozilla/geckodriver/releases/)  
* [chromedriver](https://chromedriver.storage.googleapis.com/index.html)  
* [Видеокурс Selenium Python](https://clck.ru/34nd4h)  
* [Проверка на автоматизацию](https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html)
* [Документация Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/bs4ru.html)
* [Пишем прогресс-бары при помощи tqdm](https://teletype.in/@pythontalk/tqdm_progressbars)