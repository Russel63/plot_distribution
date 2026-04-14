# Distribution Visualizer

Библиотека для автоматической визуализации распределений признаков в pandas DataFrame. Автоматически определяет тип данных (дискретные, непрерывные, категориальные) и строит подходящие графики.

## Установка

bash
pip install pandas matplotlib seaborn numpy

Copy
Быстрый старт
plt_distr(df)

Copy
python
Возможности
Автоматическое определение типа признака (дискретный / непрерывный / категориальный)

Гистограммы с KDE для непрерывных данных

Countplot для дискретных и категориальных данных

Линии среднего и медианы на каждом графике

Доверительные интервалы

Зоны убытков

Поддержка пользовательских названий колонок

Использование
Базовый вызов
plt_distr(df)

Copy
python
Пользовательские названия колонок
col_names = {
    'age': 'Возраст',
    'salary': 'Зарплата',
}
plt_distr(df)

Copy
python
Указание дискретных колонок вручную
plt_distr(df, discrete_cols=['age', 'children'])

Copy
python
Доверительный интервал
plt_distr(df, interval=0.95)

Copy
python
Зоны убытков
plt_distr(df, zones=[(0, 1000), (5000, 10000)])

Copy
python
Параметры
Параметр	Тип	По умолчанию	Описание
df	DataFrame	—	Входной датафрейм
title	bool	True	Печатать заголовок из df.attrs["title"]
discrete_cols	list	[]	Дополнительные дискретные колонки
all_discrete_cols	list	[]	Полный список дискретных колонок (отключает автоопределение)
interval	float	False	Доверительный интервал, например 0.95
zones	list	False	Зоны в формате [(low, high), ...]
Зависимости
Python 3.7+

pandas

matplotlib

seaborn

numpy
