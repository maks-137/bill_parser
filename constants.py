PAYLOAD_FIELDS = [
    'BillSearchModel.session',
    'BillSearchModel.registrationNumberCompareOperation',
    'BillSearchModel.registrationNumber',
    'BillSearchModel.registrationRangeStart',
    'BillSearchModel.registrationRangeEnd',
    'BillSearchModel.name',
    'BillSearchModel.detailView',
    'Paging.page',
    'Paging.per_page',
]


PAYLOAD_KEYWORDS = {
    'BillSearchModel.session': {
        'IX скл. 1 сесія': 10011,
        'IX скл. 2 сесія': 10013,
        'IX скл. 3 сесія': 10014,
        'IX скл. 4 сесія': 10015,
        'IX скл. 5 сесія': 10016,
        'IX скл. 6 сесія': 10017,
        'IX скл. 7 сесія': 10018,
        'IX скл. 8 сесія': 10019,
        'IX скл. 9 сесія': 10020,
        'Всі сесії IX скл.': 10,
    },
    'BillSearchModel.registrationNumberCompareOperation': {
        'Містить': 2,
        'Дорівнює': 1,
        'Перелік': 3,
    }
}

TABLE_FIELDS = [
    'Номер реєстрації',
    'Дата реєстрації',
    'Номер акту',
    'Дата акту',
    'Сесія реєстрації',
    'Рубрика законопроекту',
    "Суб'єкт права законодавчої ініціативи",
    'Ініціатор(и) законопроекту',
    'Головний комітет',
    'Інші комітети',
    'Текст законопроекту та супровідні документи',
    "Документи, пов'язані із роботою",
]
