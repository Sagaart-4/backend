import numpy as np
from catboost import CatBoostRegressor

MODEL_PATH = 'analytics/catboost_v1.json'


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
