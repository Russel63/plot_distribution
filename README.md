# Distribution Visualizer

Библиотека для автоматической визуализации распределений признаков в pandas DataFrame.  
Просто передай датафрейм — она сама разберётся какие графики построить.

---

## Установка

### Вариант 1 — одна ячейка в Jupyter или Google Colab (рекомендуется)

Скопируй и запусти эту ячейку — скачает и подключит библиотеку автоматически:

```python
import urllib.request
import zipfile
import os

url = "https://github.com/Russel63/Distribution-Visualizer/archive/refs/heads/main.zip"
urllib.request.urlretrieve(url, "visualizer.zip")

with zipfile.ZipFile("visualizer.zip") as z:
    z.extract("Distribution-Visualizer-main/visualizer.py")

os.rename("Distribution-Visualizer-main/visualizer.py", "visualizer.py")
os.remove("visualizer.zip")
os.rmdir("Distribution-Visualizer-main")

from visualizer import plt_distr
```

### Вариант 2 — скачать с GitHub через Git

Если у тебя ещё нет Git, [скачай его здесь](https://git-scm.com/downloads).

```bash
git clone https://github.com/Russel63/Distribution-Visualizer.git
cd Distribution-Visualizer
```

### Вариант 3 — скачать вручную

1. Открой страницу репозитория: https://github.com/Russel63/Distribution-Visualizer
2. Нажми зелёную кнопку **Code → Download ZIP**
3. Распакуй архив и скопируй файл `visualizer.py` в папку своего проекта

### Установка зависимостей

```bash
pip install pandas matplotlib seaborn numpy
```

---

## Быстрый старт

Скопируй `visualizer.py` в папку своего проекта, затем:

```python
import pandas as pd
from visualizer import plt_distr

df = pd.read_csv('my_data.csv')
plt_distr(df)
```

Всё. Графики построятся автоматически.

---

## Как это работает

Функция сама определяет тип каждой колонки:

| Тип | Пример | График |
|-----|--------|--------|
| Непрерывный | зарплата, рост, цена | гистограмма + KDE |
| Дискретный | возраст, количество детей | столбчатый график |
| Категориальный | город, статус, пол | столбчатый график |

На каждом графике автоматически отображаются линии **среднего** (красная) и **медианы** (оранжевая).

---

## Примеры использования

### Базовый вызов

```python
plt_distr(df)
```

### Два графика в ряд (быстрее просматривать)

```python
plt_distr(df, ncols=2)
```

### Свои названия колонок (вместо технических)

```python
col_names = {
    'age':    'Возраст',
    'salary': 'Зарплата',
    'city':   'Город',
}
plt_distr(df, col_names=col_names)
```

### Доверительный интервал 95%

Добавляет зелёные линии, между которыми находится 95% значений.

```python
plt_distr(df, interval=0.95)
```

### Зоны рисков

Закрашивает опасные диапазоны значений красным. Используй `zones_cols` чтобы применить зоны только к нужным колонкам.

```python
plt_distr(df, zones=[(0, 10000), (90000, 120000)], zones_cols=['salary'])
```

### Ограничить число категорий на графике

По умолчанию показываются топ-20 категорий. Можно изменить:

```python
plt_distr(df, max_cat_values=10)  # показать только топ-10
```

---

## Если график отобразился неправильно

Иногда алгоритм ошибается — например, принимает возраст за непрерывный признак.  
В этом случае укажи типы вручную:

```python
# Добавить колонки к автоматически найденным дискретным
plt_distr(df, discrete_cols=['age', 'experience'])

# Или задать полный список дискретных колонок вручную (отключает автоопределение)
plt_distr(df, all_discrete_cols=['age', 'children', 'experience'])
```

---

## Максимальный пример

```python
plt_distr(
    df,
    col_names={
        'age':        'Возраст',
        'salary':     'Зарплата',
        'children':   'Кол-во детей',
        'city':       'Город',
        'experience': 'Стаж (лет)',
    },
    discrete_cols=['experience'],   # добавить к автоопределённым
    interval=0.95,                  # доверительный интервал
    zones=[(0, 20000)],             # зона рисков
    zones_cols=['salary'],          # только для колонки salary
    ncols=2,                        # два графика в ряд
    max_cat_values=15,              # топ-15 категорий
)
```

---

## Все параметры

| Параметр | Тип | По умолчанию | Описание |
|---|---|---|---|
| `df` | DataFrame | — | Входной датафрейм |
| `title` | bool | `True` | Показывать заголовок из `df.attrs["title"]` |
| `col_names` | dict | `None` | Словарь `{'колонка': 'Название'}` |
| `discrete_cols` | list | `None` | Добавить колонки к автоопределённым дискретным |
| `all_discrete_cols` | list | `None` | Задать все дискретные колонки вручную |
| `interval` | float | `False` | Доверительный интервал, например `0.95` |
| `zones` | list | `False` | Зоны в формате `[(low, high), ...]` |
| `zones_cols` | list | `None` | Колонки для зон, например `['salary']`. Если не указано — применяется ко всем |
| `ncols` | int | `1` | Количество графиков в одном ряду |
| `max_cat_values` | int | `20` | Максимум категорий на графике |

---

## Зависимости

- Python 3.7+
- pandas
- matplotlib
- seaborn
- numpy
