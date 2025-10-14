import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math


def is_discrete(series, ratio_threshold=0.05):
    # вычисляем отношение числа уникальных значений к количеству значений 
    unique_ratio = series.nunique() / len(series)
    # Проверяем, являются ли все числа целыми в массиве
    is_whole_numbers = series.dropna().apply(lambda x: float(x).is_integer()).all()
    # возвращаем истина если все числа целые и отношение уникальных знач. к n знач. ниже порога 
    return is_whole_numbers and unique_ratio < ratio_threshold


def sep_num_col(df):
    # делим колонки на дискретные и непрерывные по условию функции is_discrete()
    discrete_cols = [col for col in df.columns if is_discrete(df[col])]
    continuous_cols = [col for col in df.columns if col not in discrete_cols]
    return {'discrete_cols': discrete_cols, 'continuous_cols': continuous_cols}


def get_position(value, unique_vals):
    if value in unique_vals:
        return unique_vals.index(value)
    # Интерполяция положений 
    for i, val in enumerate(unique_vals):
        if val > value:
            if i == 0:
                return 0
            # линейная интерполяция 
            prev_val = unique_vals[i-1]
            ratio = (value - prev_val) / (val - prev_val)
            return (i-1) + ratio
    return len(unique_vals) - 1


def plt_num(df, ax, col_name, num_cols_sep):
    if col_name in num_cols_sep['discrete_cols']:
        # задаем сам график 
        sns.countplot(data=df, x=col_name, ax=ax, palette='viridis', edgecolor='black', linewidth=0.5)
        ax.set_ylabel('Количество')
        
        # работаем с уникальными значениями 
        unique_vals = sorted(df[col_name].dropna().unique())
        
        # Соотносм положение линий среднего и медианы с корректным положением столбцов 
        mean_val = df[col_name].mean()
        median_val = df[col_name].median()
        
        mean_pos = get_position(mean_val, unique_vals)
        median_pos = get_position(median_val, unique_vals)
        
        # задаем линии среднего и медианы на графике 
        ax.axvline(mean_pos, color='red', linestyle='--', 
                  linewidth=2, label=f'Среднее: {mean_val:.2f}')
        ax.axvline(median_pos, color='orange', linestyle='--', 
                  linewidth=2, label=f'Медиана: {median_val:.2f}')
        
    else:
        # Выводим гистограммы с численными непрерывными данными
        sns.histplot(data=df, x=col_name, bins=30, ax=ax, alpha=0.7, element='bars', fill=True, color='skyblue', 
                        edgecolor='black', linewidth=0.5, kde=False, stat='density' )
        sns.kdeplot(data=df, x=col_name, ax=ax, color='blue', linewidth=2)
        ax.set_ylabel('Частота')

        ax.axvline(df[col_name].mean(), color='red', linestyle='--', 
                      linewidth=2, label=f'Среднее: {df[col_name].mean():.2f}')
        ax.axvline(df[col_name].median(), color='orange', linestyle='--', 
                      linewidth=2, label=f'Медиана: {df[col_name].median():.2f}')

    ax.legend()
    ax.set_title(f'Распределение "{col_names[col_name]}"') 
    
    
def plt_cat(df, ax, col_name, order=None):
    # Выводим гистограммы для категориальных данных 
    sns.countplot(data=df, x=col_name, ax=ax, palette='Set2', order=order)
    ax.set_title(f'Распределение "{col_names[col_name]}"')
    ax.set_ylabel('Количество')
    ax.tick_params(axis='x', rotation=75)
    
    
def add_interval(interval, df, ax, col_name):
    low = (1 - interval) / 2
    up = 1 - low
    
    lower = df[col_name].quantile(low)
    upper = df[col_name].quantile(up)
    
    ax.axvline(lower, color='green', linestyle='-', 
                  linewidth=2, label=f'Границы д. интервала: {interval * 100}%')
    ax.axvline(upper, color='green', linestyle='-', 
                  linewidth=2)


def mark_zone(zones, df, ax, col_name):
    for i, zone in enumerate(zones):
        plt = ax
        median = df[col_name].median()
        std = df[col_name].std()
        if i == 0:
            low = ax.get_xlim()[0]
        else:
            low = zone[0]
        up = zone[1]
        plt.fill_between([low, up], 0, (ax.get_ylim()[1])*0.5, alpha=0.5, color='black', label='Убытки')

        
def plt_distr(df, title=True, discrete_cols=[], interval=False, zones=False):
    ''' Декларируем функцию которая принимает на входе дата фрейм любого размера 
    и выводит графики отражающие распределение значений в столбцах с количественным 
    и качественным типом данных в данном датафрейме ''' 
    # Разделяем данные на количественны и качественные
    df_num = df.select_dtypes(include=['int64', 'float64'])
    
    df_cat = df.select_dtypes(include=['object'])
    
    all_cols = list(df_num.columns) + list(df_cat.columns)
    num_cols_sep = sep_num_col(df_num) 
    num_cols_sep['discrete_cols'] += discrete_cols
    n_cols = len(all_cols)
    
    if n_cols == 0:
        print("No columns to plot")
        return
    
    n_rows = math.ceil(n_cols / 2)
    
    # обрабатываем количество колонок 
    if n_cols == 1:
        fig, ax = plt.subplots(1, 1, figsize=(6, 5))
        axes = [ax]
    else:
        fig, axes = plt.subplots(n_rows, 2, figsize=(12, 5*n_rows))
        axes = axes.flatten()
    
    # Печатаем графики поочередно двумя разными способами 
    if title:
        try:
            print(f'Распределения в таблице "{df.attrs["title"]}"')
        except:
            pass
    for i, col_name in enumerate(all_cols):
        if col_name in df_num.columns:
            # вызываем функцию для печати графиков для численных данных 
            plt_num(df, axes[i], col_name, num_cols_sep)
        else:
            # вызываем функцию для печати графиков для категориальных данных 
            plt_cat(df, axes[i], col_name)
        
        axes[i].set_xlabel(f'Значение "{col_names[col_name]}"')
    
    for i in range(n_cols, len(axes)):
        axes[i].set_visible(False)
    
    if interval:
        add_interval(interval, df, ax, col_name)
        ax.legend()
        
    if zones:
        mark_zone(zones, df, ax, col_name)
        ax.legend()
        
    plt.tight_layout()
    plt.show()
