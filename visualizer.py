import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np


def is_discrete(series, ratio_threshold=0.10, max_unique=50):
    clean = series.dropna()
    if len(clean) == 0:
        return False
    n_unique = clean.nunique()
    is_integer_dtype = pd.api.types.is_integer_dtype(series)
    if is_integer_dtype:
        return n_unique <= max_unique or n_unique / len(clean) < ratio_threshold
    if n_unique / len(clean) >= ratio_threshold and n_unique > max_unique:
        return False
    return bool((clean % 1 == 0).all())


def sep_num_col(df):
    discrete_cols = [col for col in df.columns if is_discrete(df[col])]
    continuous_cols = [col for col in df.columns if col not in discrete_cols]
    print(
        "⚠️  Автоопределение типов: "
        f"дискретные → {discrete_cols}, непрерывные → {continuous_cols}\n"
        "   Если график отображается некорректно, передайте списки вручную: "
        "discrete_cols=[...] или all_discrete_cols=[...]"
    )
    return {'discrete_cols': discrete_cols, 'continuous_cols': continuous_cols}


def get_position_fast(value, unique_vals):
    unique_array = np.array(unique_vals, dtype=float)
    idx = np.searchsorted(unique_array, value)
    if idx < len(unique_array) and unique_array[idx] == value:
        return idx
    if idx == 0:
        return 0
    if idx >= len(unique_array):
        return len(unique_array) - 1
    prev_val = unique_array[idx - 1]
    next_val = unique_array[idx]
    return (idx - 1) + (value - prev_val) / (next_val - prev_val)


def _style_discrete_axis(ax, unique_vals, max_ticks=15):
    """Прореживает метки на оси X для дискретных графиков."""
    n = len(unique_vals)
    if n <= max_ticks:
        ax.set_xticks(range(n))
        ax.set_xticklabels(unique_vals)
    else:
        step = max(1, n // max_ticks)
        positions = list(range(0, n, step))
        labels = [unique_vals[i] for i in positions]
        ax.set_xticks(positions)
        ax.set_xticklabels(labels)
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.tick_params(axis='x', which='minor', length=3)


def plt_num(df, ax, col_name, num_cols_sep, col_names, interval=False, zones=False):
    series = df[col_name].replace([np.inf, -np.inf], np.nan)
    n_inf = df[col_name].isin([np.inf, -np.inf]).sum()
    if n_inf > 0:
        print(f"[WARNING] Column '{col_name}': {n_inf} inf values removed before plotting.")
    series = series.dropna()
    if len(series) > 500_000:
        print(f"[WARNING] Column '{col_name}' has {len(series):,} rows — plotting may be slow.")
    if len(series) == 0:
        print(f"[INFO] Column '{col_name}': no data after dropping NaN/Inf, skipping.")
        ax.text(0.5, 0.5, 'Нет данных', ha='center', va='center', transform=ax.transAxes, fontsize=12)
        ax.set_title(f'Распределение "{col_names[col_name]}"')
        return
    if series.nunique() == 1 or series.std() == 0 or (series.mean() != 0 and series.std() / abs(series.mean()) < 1e-10):
        print(f"[INFO] Column '{col_name}': near-constant values (std ≈ 0), showing single bar.")
        val = series.iloc[0]
        ax.bar([0], [len(series)], width=0.4, color='skyblue', edgecolor='black', linewidth=0.5)
        ax.set_xlim(-1, 1)
        ax.set_xticks([0])
        ax.set_xticklabels([str(val)])
        ax.set_ylabel('Количество')
        ax.set_title(f'Распределение "{col_names[col_name]}"')
        ax.set_xlabel(f'{col_names[col_name]}')
        return
    mean_val = series.mean()
    median_val = series.median()

    if col_name in num_cols_sep['discrete_cols']:
        unique_vals = sorted(series.unique())
        counts = series.value_counts().sort_index()

        ax.bar(range(len(unique_vals)), counts.values,
               color=sns.color_palette('viridis', len(unique_vals)),
               edgecolor='black', linewidth=0.5)
        ax.set_ylabel('Количество')

        _style_discrete_axis(ax, [str(v) for v in unique_vals])

        mean_pos = get_position_fast(mean_val, unique_vals)
        median_pos = get_position_fast(median_val, unique_vals)
        ax.axvline(mean_pos, color='red', linestyle='--', linewidth=2, label=f'Среднее: {mean_val:.2f}')
        ax.axvline(median_pos, color='orange', linestyle='--', linewidth=2, label=f'Медиана: {median_val:.2f}')

    else:
        sns.histplot(data=df, x=col_name, bins=30, ax=ax, alpha=0.7, fill=True,
                     color='skyblue', edgecolor='black', linewidth=0.5, kde=False, stat='density')
        sns.kdeplot(data=df, x=col_name, ax=ax, color='blue', linewidth=2, warn_singular=False)
        ax.set_ylabel('Частота')
        ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=8))
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.tick_params(axis='x', which='minor', length=3)

        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Среднее: {mean_val:.2f}')
        ax.axvline(median_val, color='orange', linestyle='--', linewidth=2, label=f'Медиана: {median_val:.2f}')

        if interval:
            low = (1 - interval) / 2
            lower = series.quantile(low)
            upper = series.quantile(1 - low)
            ax.axvline(lower, color='green', linestyle='-', linewidth=2,
                       label=f'Д. интервал {interval * 100:.0f}%')
            ax.axvline(upper, color='green', linestyle='-', linewidth=2)

        if zones:
            for i, zone in enumerate(zones):
                low = ax.get_xlim()[0] if i == 0 else zone[0]
                ax.fill_between([low, zone[1]], 0, ax.get_ylim()[1] * 0.5,
                                alpha=0.4, color='red', label='Зона рисков' if i == 0 else '_')

    ax.legend(fontsize=9)
    ax.set_title(f'Распределение "{col_names[col_name]}"')
    ax.set_xlabel(f'{col_names[col_name]}')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=6, integer=True))


def plt_cat(df, ax, col_name, col_names, max_cat_values=20):
    series = df[col_name].dropna()
    if len(series) == 0:
        print(f"[INFO] Column '{col_name}': no data after dropping NaN, skipping.")
        ax.text(0.5, 0.5, 'Нет данных', ha='center', va='center', transform=ax.transAxes, fontsize=12)
        ax.set_title(f'Распределение "{col_names[col_name]}"')
        return
    n_unique = series.nunique()
    if n_unique > 100_000:
        print(f"[WARNING] Column '{col_name}' has {n_unique:,} unique values — skipping plot to save RAM.")
        ax.text(0.5, 0.5, f'Слишком много уникальных значений\n({n_unique:,})', ha='center', va='center',
                transform=ax.transAxes, fontsize=11)
        ax.set_title(f'Распределение "{col_names[col_name]}"')
        return
    counts = series.value_counts()

    truncated = len(counts) > max_cat_values
    if truncated:
        counts = counts.head(max_cat_values)

    sns.barplot(x=counts.index, y=counts.values, ax=ax, hue=counts.index,
                palette='Set2', edgecolor='black', linewidth=0.5, legend=False)
    ax.set_title(f'Распределение "{col_names[col_name]}"' +
                 (f' (топ {max_cat_values})' if truncated else ''))
    ax.set_ylabel('Количество')
    ax.set_xlabel(f'{col_names[col_name]}')
    ax.tick_params(axis='x', rotation=45)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=6, integer=True))
    ax.xaxis.set_minor_locator(ticker.NullLocator())


def plt_distr(df, title=True, col_names=None, discrete_cols=None, all_discrete_cols=None,
              interval=False, zones=False, ncols=1, max_cat_values=20):
    # Валидация входных данных
    if not isinstance(df, pd.DataFrame):
        print(f"❌ Ожидается pandas DataFrame, получено: {type(df).__name__}\n"
              "   Пример: plt_distr(df)")
        return
    if df.empty:
        print("❌ DataFrame пустой — нечего отображать.")
        return
    if len(df.columns) != len(set(df.columns)):
        print("⚠️  DataFrame содержит дублирующиеся имена колонок — это может вызвать ошибки.")
    if interval is not False and not (0 < interval < 1):
        print(f"❌ interval должен быть числом от 0 до 1, например 0.95. Получено: {interval}")
        return
    if zones is not False:
        if not isinstance(zones, list) or not all(isinstance(z, tuple) and len(z) == 2 for z in zones):
            print(f"❌ zones должен быть списком кортежей: [(low, high), ...]. Получено: {zones}")
            return
    if not isinstance(ncols, int) or ncols < 1:
        print(f"❌ ncols должен быть целым числом >= 1. Получено: {ncols}")
        return
    # фильтруем колонки с нехэшируемыми значениями (списки, словари и т.д.)
    unhashable = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, (list, dict, set))).any()]
    if unhashable:
        print(f"⚠️  Колонки {unhashable} содержат нехэшируемые значения (списки, словари) — они будут пропущены.")
        df = df.drop(columns=unhashable)
    if not df.index.is_unique:
        print("[WARNING] DataFrame has duplicate index — resetting index to avoid errors.")
        df = df.reset_index(drop=True)
    if col_names is None:
        col_names = {col: col for col in df.columns}
    else:
        # дополняем недостающие ключи именем колонки
        col_names = {col: col_names.get(col, col) for col in df.columns}
    if discrete_cols is None:
        discrete_cols = []
    if all_discrete_cols is None:
        all_discrete_cols = []

    df_num = df.select_dtypes(include=[np.number, bool])
    df_num = df_num.apply(lambda col: col.astype(int) if col.dtype == bool else col)
    df_cat = df.select_dtypes(include=['object', 'category'])
    all_cols = list(df_num.columns) + list(df_cat.columns)

    if not all_discrete_cols:
        num_cols_sep = sep_num_col(df_num)
        num_cols_sep['discrete_cols'] += discrete_cols
    else:
        num_cols_sep = {
            'discrete_cols': all_discrete_cols,
            'continuous_cols': [col for col in df_num.columns if col not in all_discrete_cols]
        }

    n_cols_total = len(all_cols)
    if n_cols_total == 0:
        print("No columns to plot")
        return

    n_rows = -(-n_cols_total // ncols)  # ceiling division
    fig_w = 6 * ncols
    fig_h = 5 * n_rows

    fig, axes = plt.subplots(n_rows, ncols, figsize=(fig_w, fig_h))
    axes = np.array(axes).flatten()

    if title:
        try:
            fig.suptitle(f'Распределения в таблице "{df.attrs["title"]}"',
                         fontsize=14, y=1.01)
        except Exception:
            pass

    for i, col_name in enumerate(all_cols):
        if col_name in df_num.columns:
            plt_num(df, axes[i], col_name, num_cols_sep, col_names, interval, zones)
        else:
            plt_cat(df, axes[i], col_name, col_names, max_cat_values)

    for i in range(n_cols_total, len(axes)):
        axes[i].set_visible(False)

    plt.tight_layout()
    plt.show()
