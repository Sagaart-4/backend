import numpy as np
from catboost import CatBoostRegressor

MODEL_PATH = 'analytics/catboost_v1.json'

(
    category,
    year,
    height,
    width,
    work_material,
    pad_material,
    count_title,
    count_artist,
    country,
    sex,
    solo_shows,
    group_shows,
    age,
    is_alive,
) = (
    "Печать",
    1983,
    60.5,
    91.0,
    "Цветная литография",
    "Сотканная бумага",
    np.NaN,
    np.NaN,
    "Россия",
    "М",
    ("centre pompidou, whitney museum of american art,"
     "the metropolitan museum of art, los angeles county "
     "museum of art (lacma)"),
    ("whitney museum of american art, the metropolitan museum of art, "
     "los angeles county museum of art (lacma)"),
    80,
    np.NaN,
)

# category - категория(str)
# year - год(float)
# height - высота(float)
# width - ширина(float)
# work_material - материал работы(str)
# pad_material - материал планшета(str)
# count_title - кол-во продаж картины(пока np.NaN)
# count_artist - кол-во работ художника(пока np.NaN)
# country - страна(str)
# sex - пол(str, М/Ж)
# solo_shows - список индивидуальных выставок(str через ,)
# group_shows - список групповых выставок(str через ,)
# age - возраст(int)
# is_alive - жив ли(пока будет np.NaN)(в будущем int)

data = [
    category,
    year,
    height,
    width,
    work_material,
    pad_material,
    count_title,
    count_artist,
    country,
    sex,
    solo_shows,
    group_shows,
    age,
    is_alive,
]


def make_shows_authority_from_shows(shows: str) -> float:
    """
    Функция для преобразования строки(полей solo_shows и group_shows),
    содержащей информацию о выставках автора(будь то индивидуальных или
    групповых) в число - эквивалент суммарного посещения выставок
    с весами authorities(пока они все одинаковы). 
    All shows - все выставки, имеющиеся у меня на данный момент, 
    в дальнейшем будет пополняться.
    """
    all_shows = [
        "centre pompidou",
        "whitney museum of american art",
        "the metropolitan museum of art",
        "los angeles county museum of art (lacma)",
        "guggenheim museum bilbao",
        "louisiana museum of art",
        "hirshhorn museum and sculpture garden",
        "museum of contemporary art",
        "los angeles (moca)",
        "tate britain",
        "museum ludwig",
        "national gallery of victoria",
        "hamburger bahnhof",
        "neue nationalgalerie",
        "national portrait gallery - london",
        "art institute of chicago",
        "national museum of modern and contemporary art - korea (mmca)",
        "museo tamayo",
        "tel aviv museum of art",
        "tate liverpool",
        "international center of photography (icp)",
        "mca chicago",
        "new museum",
        "dallas museum of art",
        "brooklyn museum",
        "museum of modern art (moma)",
        "tate modern",
        "solomon r. guggenheim museum",
        "national gallery of art",
        "washington",
        "d.c.",
        "ullens center for contemporary art (ucca)",
        "san francisco museum of modern art (sfmoma)",
        "perez art museum miami (pamm)",
        "mass moca",
        "museo reina sofia",
        "moma ps1",
        "serpentine galleries",
        "museu d'art contemporani de barcelona (macba)",
        "jewish museum",
        "k20 grabbeplatz",
        "dia:beacon",
        "museum fur moderne kunst",
        "frankfurt (mmk)",
        "museum of contemporary art australia (mca)",
        "institute of contemporary art",
        "miami (ica miami)",
        "aspen art museum",
        "schirn kunsthalle frankfurt",
        "dallas contemporary",
        "hammer museum",
        "garage museum of contemporary art",
        "deichtorhallen hamburg",
        "yuz museum shanghai",
        "mori art museum",
        "the broad",
        "tai kwun",
        "fondation beyeler",
        "malba",
        "boston",
        "stedelijk museum amsterdam",
        "castello di rivoli",
        "leeum - samsung museum of art",
        "dia:chelsea",
        "kunstmuseum basel",
        "power station of art",
        "museo jumex",
        "met breuer",
        "lenbachhaus",
        "palazzo grassi - punta della dogana",
        "nasher sculpture center",
        "haus der kunst",
        "institute of contemporary arts",
        "london",
        "whitechapel gallery",
        "secession",
        "kunsthalle basel",
        "m+",
        "museo d'arte contemporanea di roma (macro)",
        "kroller-muller museum",
        "fondazione prada",
        "martin-gropius-bau",
        "the bass museum of art",
        "palais de tokyo",
        "rockbund art museum",
        "studio museum in harlem",
        "national gallery singapore",
        "k21 standehaus",
        "kw institute for contemporary art",
        "jeu de paume",
        "zeitz mocaa",
        "museum of old and new art",
        "musée du louvre",
        "museu de arte moderna de sao paulo (mam)",
        "museu de arte moderna (mam rio)",
    ]
    n = len(all_shows)
    authorities = [0.5 for i in range(n)]
    vector = [0 for i in range(n)]
    if not isinstance(shows, float):
        shows = set([k.strip().lower() for k in shows.split(",")])
        for i in range(n):
            if all_shows[i] in shows:
                vector[i] = 1
    return sum([vector[i] * authorities[i] for i in range(n)])


def preprocess(data: list) -> np.ndarray:
    """
    Функция для преобразования массива входных, введеных пользователем
    данных в удобоворимый для модели вид. Все переменные должны находиться
    на таких же местах, что указано
    выше. В данном случае, когда пользователь вводит данные и мы пока не
    представляем, в каком формате они будут представлены, потому как модель
    должна будет заранее знать о
    возможных форматах, используется только функция
    make_shows_authority_from_shows. Но также привожу для справки
    дополнительные функции, которыми я обрабатывал другие поля
    """
    return np.array(
        data[:-4]
        + [
            make_shows_authority_from_shows(data[-4]),
            make_shows_authority_from_shows(data[-3]),
        ]
        + data[-2:]
    )


def price_generator(data):

    model = CatBoostRegressor()
    model.load_model(
        MODEL_PATH,
        format="json"
    )
    # выберите путь до файла
    return (
        np.clip(model.predict(preprocess(data)), 1000, np.inf)
    )  # выдает предсказание цены


# import requests
# from bs4 import BeautifulSoup
# class PriceConverter:
#     """
#     Класс для обрабоки поля pre-sale estimate, оценочной стоимости, возможно, будет использован в будущем
#     """

#     def __init__(self):
#         self.headers = {
#             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
#         }

#         us_exchange = self.return_rub_currency("https://g.co/kgs/vfXQ56b")
#         uk_exchange = self.return_rub_currency("https://g.co/kgs/fMkfg5M")
#         jap_exchange = self.return_rub_currency("https://g.co/kgs/vTQJ9xE")
#         zar_exchange = self.return_rub_currency("https://g.co/kgs/zGpBQE4")
#         hk_exchange = self.return_rub_currency("https://g.co/kgs/VyT8cWv")
#         chf_exchange = self.return_rub_currency("https://g.co/kgs/niCw6C6")
#         euro_exchange = self.return_rub_currency("https://g.co/kgs/NxoJHqL")
#         au_exchange = self.return_rub_currency("https://g.co/kgs/2urRZ5a")
#         nok_exchange = self.return_rub_currency("https://g.co/kgs/MjkfkH5")
#         nt_exchange = self.return_rub_currency("https://g.co/kgs/xJefwwK")
#         mx_exchange = self.return_rub_currency("https://g.co/kgs/C7DvvZj")
#         inr_exchange = self.return_rub_currency("https://g.co/kgs/bWkRSnf")
#         ars_exchange = self.return_rub_currency("https://g.co/kgs/EiY5zom")
#         sek_exchange = self.return_rub_currency("https://g.co/kgs/uvCL2zS")
#         php_exchange = self.return_rub_currency("https://g.co/kgs/nhAFUCi")
#         czk_exchange = self.return_rub_currency("https://g.co/kgs/r3n31ck")
#         krw_exchange = self.return_rub_currency("https://g.co/kgs/ayDQ6Yf")
#         nz_exchange = self.return_rub_currency("https://g.co/kgs/gKANJ4m")
#         s_exchange = self.return_rub_currency("https://g.co/kgs/nv9Zmwh")
#         c_exchange = self.return_rub_currency("https://g.co/kgs/34tfN7K")
#         brl_exchange = self.return_rub_currency("https://g.co/kgs/ne2vzSV")
#         aed_exchange = self.return_rub_currency("https://g.co/kgs/ZJv1FCT")
#         dkk_exchange = self.return_rub_currency("https://g.co/kgs/Da4dHbC")
#         huf_exchange = self.return_rub_currency("https://g.co/kgs/k7D8C2H")
#         idr_exchange = self.return_rub_currency("https://g.co/kgs/jBCCj9Y")
#         mad_exchange = self.return_rub_currency("https://g.co/kgs/Ts2b8Jr")
#         ngn_exchange = self.return_rub_currency("https://g.co/kgs/UwfywcS")
#         pln_exchange = self.return_rub_currency("https://g.co/kgs/ZeWMibb")
#         rm_exchange = self.return_rub_currency("https://g.co/kgs/cDTm3Du")
#         cn_exchange = self.return_rub_currency("https://g.co/kgs/VGDzifT")
#         vef_exchange = 0.00002460601  # костыль, не понял, как спарсить, потому как не выдает типовую ссылку
#         skk_exchange = 3.19247  # то же самое
#         self.exchanges = {
#             "US": us_exchange,
#             "UK": uk_exchange,
#             "JAP": jap_exchange,
#             "JPY": jap_exchange,
#             "EURO": euro_exchange,
#             "ZAR": zar_exchange,
#             "HK": hk_exchange,
#             "CHF": chf_exchange,
#             "AU": au_exchange,
#             "NOK": nok_exchange,
#             "NT": nt_exchange,
#             "MX": mx_exchange,
#             "INR": inr_exchange,
#             "ARS": ars_exchange,
#             "SEK": sek_exchange,
#             "PHP": php_exchange,
#             "CZK": czk_exchange,
#             "KRW": krw_exchange,
#             "NZ": nz_exchange,
#             "S": s_exchange,
#             "C": c_exchange,
#             "BRL": brl_exchange,
#             "AED": aed_exchange,
#             "DKK": dkk_exchange,
#             "HUF": huf_exchange,
#             "IDR": idr_exchange,
#             "MAD": mad_exchange,
#             "NGN": ngn_exchange,
#             "PLN": pln_exchange,
#             "RM": rm_exchange,
#             "CN¥": cn_exchange,
#             "VEF": vef_exchange,
#             "SKK": skk_exchange,
#             "nan": 0,
#         }

#     def return_rub_currency(self, currency_exchange_link):
#         full_page = requests.get(currency_exchange_link, headers=self.headers)
#         soup = BeautifulSoup(full_page.content, "html.parser")
#         convert = soup.findAll(
#             "span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2}
#         )
#         if convert == []:
#             return 0
#         price = float(convert[0].text.replace(",", "."))
#         return round(price, 2)

#     def return_numbers(self, t):
#         try:
#             length = len(t)
#         except TypeError:
#             return [0, 0]
#         integers = []
#         i = 0

#         while i < length:
#             s_int = ""
#             while i < length and (
#                 "0" <= t[i] <= "9" or t[i] == "." or t[i] == ","
#             ):
#                 s_int += t[i]
#                 i += 1
#             i += 1
#             if s_int != "":
#                 try:
#                     integers.append(
#                         int("".join("".join(s_int.split(",")).split(".")))
#                     )
#                 except ValueError:
#                     return [0, 0]
#         return integers

#     def return_currency(self, t):
#         t = t.upper()
#         try:
#             t = t.upper()
#             if "US" in t:
#                 return "US"
#             if "£" in t:
#                 return "UK"
#             if "ZAR" in t:
#                 return "ZAR"
#             if "HK" in t:
#                 return "HK"
#             if "€" in t:
#                 return "EURO"
#             if "CHF" in t:
#                 return "CHF"
#             if "NOK" in t:
#                 return "NOK"
#             if "AU" in t:
#                 return "AU"
#             if "NT" in t:
#                 return "NT"
#             if "MX" in t:
#                 return "MX"
#             if "INR" in t:
#                 return "INR"
#             if "ARS" in t:
#                 return "ARS"
#             if "SEK" in t:
#                 return "SEK"
#             if "PHP" in t:
#                 return "PHP"
#             if "JPY" in t or "JAP" in t:
#                 return "JPY"
#             if "CZK" in t:
#                 return "CZK"
#             if "KRW" in t:
#                 return "KRW"
#             if "CN¥" in t:
#                 return "CN¥"
#             if "NZ" in t:
#                 return "NZ"
#             if "S$" in t:
#                 return "S"
#             if "C$" in t:
#                 return "C"
#             if "AED" in t:
#                 return "AED"
#             if "BRL" in t:
#                 return "BRL"
#             if "DKK" in t:
#                 return "DKK"
#             if "HUF" in t:
#                 return "HUF"
#             if "IDR" in t:
#                 return "IDR"
#             if "MAD" in t:
#                 return "MAD"
#             if "NGN" in t:
#                 return "NGN"
#             if "PLN" in t:
#                 return "PLN"
#             if "RM" in t:
#                 return "RM"
#             if "SKK" in t:
#                 return "SKK"
#             if "VEF" in t:
#                 return "VEF"
#             return "nan"
#         except AttributeError:
#             return "nan"

#     def return_rub_price(self, text: str):
#         mean_amount = self.return_numbers(text)
#         if len(mean_amount) == 1:
#             mean_amount = mean_amount[0]
#         else:
#             mean_amount = sum(mean_amount) / 2
#         currency = self.return_currency(text)
#         return round(self.exchanges[currency] * mean_amount, 5)


# # currencies = PriceConverter()
# # currencies.exchanges["ARS"], 
# # currencies.exchanges["KRW"], 
# # currencies.exchanges["IDR"], 
# # currencies.exchanges["NGN"], 
# # currencies.exchanges["RM"] = 0.098, 0.064, 0.0054, 0.058, 18.605


# # import re
# def parse_size(t: str) -> tuple(float, float):
#     """
#     Функция для преобразования поля size(размер). Учитывает различные форматы
#     """
#     if "cm" in t.splitlines()[0] or "mm" in t.splitlines()[0]:
#         t = t.splitlines()[0]
#     elif len(t.splitlines()) > 1 and (
#         "cm" in t.splitlines()[1] or "mm" in t.splitlines()[1]
#     ):
#         t = t.splitlines()[1]

#     x = re.findall(
#         r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)? x (?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)? cm",
#         t,
#     )  # AA.a x BB.b cm
#     if len(x) == 1:
#         return float(x[0].split("x")[0]), float(x[0].split("x")[1][:-3])
#     x = re.findall(
#         r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)? x (?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?cm",
#         t,
#     )  # AA.a x BB.bcm
#     if len(x) == 1:
#         return float(x[0].split("x")[0]), float(x[0].split("x")[1][:-2])
#     x = re.findall(
#         r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)? × (?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?cm",
#         t,
#     )  # AA.a × BB.bcm
#     if len(x) == 1:
#         return float(x[0].split("×")[0]), float(x[0].split("×")[1][:-2])
#     x = re.findall(
#         r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)? × (?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)? cm",
#         t,
#     )  # AA.a × BB.b cm
#     if len(x) == 1:
#         return float(x[0].split("×")[0]), float(x[0].split("×")[1][:-3])
#     x = re.findall(
#         r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)? by (?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)? cm",
#         t,
#     )  # AA.a by BB.b cm
#     if len(x) == 1:
#         return float(x[0].split("by")[0]), float(x[0].split("by")[1][:-3])
#     x = re.findall(
#         r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)? x (?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)? mm",
#         t,
#     )  # AA.a x BB.b mm
#     if len(x) == 1:
#         return (
#             float(x[0].split("x")[0]) / 100,
#             float(x[0].split("x")[1][:-3]) / 100,
#         )
#     x = re.findall(
#         r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)? x (?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?mm",
#         t,
#     )  # AA.a x BB.bmm
#     if len(x) == 1:
#         return (
#             float(x[0].split("x")[0]) / 100,
#             float(x[0].split("x")[1][:-2]) / 100,
#         )
#     return np.NaN, np.NaN


# # from string import punctuation
# def parse_medium(t: str) -> tuple(str, str):
#     """
#     Функция для преобразования поля medium(Материала работы и планшета). Очень костыльно написана ввиду большой разрозненности входных данных
#     """
#     t = t.lower()
#     if "on" in t:
#         return t.split("on")[0].strip(punctuation + " "), t.split("on")[
#             1
#         ].strip(punctuation + " ")
#     if "," in t:
#         return t.split(",")[0].strip(punctuation + " "), t.split(",")[1].strip(
#             punctuation + " "
#         )
#     if "with" in t:
#         return t.split("with")[0].strip(punctuation + " "), t.split("with")[
#             1
#         ].strip(punctuation + " ")
#     if "in" in t:
#         return t.split("in")[0].strip(punctuation + " "), t.split("in")[
#             1
#         ].strip(punctuation + " ")
#     if "and" in t:
#         return t.split("and")[0].strip(punctuation + " "), t.split("and")[
#             1
#         ].strip(punctuation + " ")
#     if "lithograph" in t:
#         return "lithograph", "paper"
#     if "book" in t:
#         return "book", "paper"
#     if "watercolor" in t:
#         return "watercolor", "paper"
#     if "oil" in t:
#         return "oil", "paper"
#     if "ink" in t:
#         return "ink", "paper"
#     if "color" in t or "colour" in t:
#         return "color", "paper"
#     if "pencil" in t:
#         return "pencil", "paper"
#     if "charcoal" in t:
#         return "charcoal", "paper"
#     if "wood" in t:
#         return "cut", "wood"
#     return np.NaN, np.NaN


# def birth_death(birth: str, death: str) -> tuple(int, int):
#     """
#     Функция для обработки полей года рождения и года смерти.
#     Выдает на выходе возраст и факт жизни в нынешний момент.
#     Делает допущение, что если год смерти пропущен и
#     год рождения меньше 1944, то человек прожил 80 лет
#     """
#     if isinstance(birth, float) or isinstance(birth, int):
#         birth = int(float(birth))
#     else:
#         birth = int(
#             float(
#                 re.findall(r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", birth)[
#                     0
#                 ]
#             )
#         )
#     if isinstance(death, float):
#         if birth < 1944:
#             return 80, 0
#         else:
#             return 2024 - birth, 1
#     if isinstance(death, float) or isinstance(death, int):
#         death = int(float(death))
#     else:
#         death = int(
#             float(
#                 re.findall(r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", death)[
#                     0
#                 ]
#             )
#         )
#     return death - birth, 0
