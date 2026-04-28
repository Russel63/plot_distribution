# Distribution Visualizer

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Библиотека для автоматической визуализации распределений признаков в pandas DataFrame.  
Просто передай датафрейм — она сама разберётся какие графики построить.

---

## Быстрый старт

```python
import pandas as pd
from visualizer import plt_distr

df = pd.read_csv('my_data.csv')
plt_distr(df)
```

Всё. Графики построятся автоматически.

---

## Установка

### Вариант 1 — одна строка в Jupyter или Google Colab (рекомендуется)

```python
!wget -nc https://raw.githubusercontent.com/Russel63/Distribution-Visualizer/main/visualizer.py
```

### Вариант 2 — одна ячейка (если `wget` недоступен)

```python
import urllib.request
import zipfile
import os

if not os.path.exists('visualizer.py'):
    url = "https://github.com/Russel63/Distribution-Visualizer/archive/refs/heads/main.zip"
    urllib.request.urlretrieve(url, "visualizer.zip")
    with zipfile.ZipFile("visualizer.zip") as z:
        z.extract("Distribution-Visualizer-main/visualizer.py")
    os.rename("Distribution-Visualizer-main/visualizer.py", "visualizer.py")
    os.remove("visualizer.zip")
    os.rmdir("Distribution-Visualizer-main")
    print("✓ Готово!")
else:
    print("✓ visualizer.py уже существует, пропускаем загрузку.")

from visualizer import plt_distr
```

### Вариант 3 — через Git

```bash
git clone https://github.com/Russel63/Distribution-Visualizer.git
cd Distribution-Visualizer
```

### Вариант 4 — вручную

1. Нажми зелёную кнопку **Code → Download ZIP**
2. Распакуй архив и скопируй `visualizer.py` в папку своего проекта

### Зависимости

```bash
pip install pandas matplotlib seaborn numpy
```

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

### Два графика в ряд

```python
plt_distr(df, ncols=2)
```

### Свои названия колонок

```python
plt_distr(df, col_names={
    'age':    'Возраст',
    'salary': 'Зарплата',
    'city':   'Город',
})
```

### Доверительный интервал 95%

```python
plt_distr(df, interval=0.95)
```

### Зоны рисков

```python
plt_distr(df, zones=[(0, 10000), (90000, 120000)], zones_cols=['salary'])
```

### Если график отобразился неправильно

Иногда алгоритм ошибается — например, принимает возраст за непрерывный признак.  
В этом случае укажи типы вручную:

```python
# Добавить колонки к автоматически найденным дискретным
plt_distr(df, discrete_cols=['age', 'experience'])

# Или задать полный список вручную (отключает автоопределение)
plt_distr(df, all_discrete_cols=['age', 'children', 'experience'])
```

### Максимальный пример

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
    discrete_cols=['experience'],
    interval=0.95,
    zones=[(0, 20000)],
    zones_cols=['salary'],
    ncols=2,
    max_cat_values=15,
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
| `zones_cols` | list | `None` | Колонки для зон. Если не указано — применяется ко всем |
| `ncols` | int | `1` | Количество графиков в одном ряду |
| `max_cat_values` | int | `20` | Максимум категорий на графике |

---

## Туториал

Интерактивный самоучитель со всеми примерами доступен на Kaggle:  
👉 [Distribution Visualizer — Самоучитель](https://www.kaggle.com/code/osvaldspengler/distribution-visualizer-tutorial)

---

## Зависимости

- Python 3.7+
- pandas
- matplotlib
- seaborn
- numpy

