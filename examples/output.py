import re

import polars as pl
import polars.selectors as cs

from loguru import logger

# TODO: load data
df = pl.DataFrame()


def expr_rank_pct(expr):
    """rank(pct=True)"""
    return expr.rank() / (expr.len() - expr.null_count())


def func_0_ts__asset__date(df: pl.DataFrame):
    df = df.with_columns(
        # x_0 = ts_mean(OPEN, 10)
        x_0=(pl.col("OPEN").rolling_mean(10)),
        # x_1 = ts_mean(CLOSE, 10)
        x_1=(pl.col("CLOSE").rolling_mean(10)),
    )
    return df


def func_0_cs__date(df: pl.DataFrame):
    df = df.with_columns(
        # x_2 = cs_rank(x_0)
        x_2=(expr_rank_pct(pl.col("x_0"))),
        # x_3 = cs_rank(x_1)
        x_3=(expr_rank_pct(pl.col("x_1"))),
    )
    return df


def func_0_cl(df: pl.DataFrame):
    df = df.with_columns(
        # x_4 = abs(log(x_1))
        x_4=(pl.col("x_1").log().abs()),
    )
    return df


def func_0_gp__date__OPEN(df: pl.DataFrame):
    df = df.with_columns(
        # x_5 = gp_rank(OPEN, CLOSE)
        x_5=(expr_rank_pct(pl.col("CLOSE"))),
    )
    return df


def func_0_gp__date__sw_l1(df: pl.DataFrame):
    df = df.with_columns(
        # x_6 = gp_rank(sw_l1, CLOSE)
        x_6=(expr_rank_pct(pl.col("CLOSE"))),
    )
    return df


def func_1_cs__date(df: pl.DataFrame):
    df = df.with_columns(
        # x_7 = cs_rank(OPEN)
        x_7=(expr_rank_pct(pl.col("OPEN"))),
    )
    return df


def func_1_ts__asset__date(df: pl.DataFrame):
    df = df.with_columns(
        # x_8 = ts_mean(x_7, 10)
        x_8=(pl.col("x_7").rolling_mean(10)),
        # expr_1 = -ts_corr(x_2, x_3, 10)
        expr_1=(-pl.rolling_corr(pl.col("x_2"), pl.col("x_3"), window_size=10)),
    )
    return df


def func_1_cl(df: pl.DataFrame):
    df = df.with_columns(
        # expr_2 = x_2 - x_4 + x_5 + x_6
        expr_2=(pl.col("x_2") - pl.col("x_4") + pl.col("x_5") + pl.col("x_6")),
    )
    return df


def func_2_ts__asset__date(df: pl.DataFrame):
    df = df.with_columns(
        # expr_3 = ts_mean(x_2, 10)
        expr_3=(pl.col("x_2").rolling_mean(10)),
    )
    return df


def func_2_cs__date(df: pl.DataFrame):
    df = df.with_columns(
        # expr_4 = cs_rank(x_8)
        expr_4=(expr_rank_pct(pl.col("x_8"))),
    )
    return df


def func_3_ts__asset__date(df: pl.DataFrame):
    df = df.with_columns(
        # expr_5 = -ts_corr(OPEN, CLOSE, 10)
        expr_5=(-pl.rolling_corr(pl.col("OPEN"), pl.col("CLOSE"), window_size=10)),
    )
    return df


logger.info("start...")


df = df.sort(by=["asset", "date"]).groupby(by=["asset"], maintain_order=True).apply(func_0_ts__asset__date)
df = df.sort(by=["date"]).groupby(by=["date"], maintain_order=False).apply(func_0_cs__date)
df = func_0_cl(df)
df = df.sort(by=["date", "OPEN"]).groupby(by=["date", "OPEN"], maintain_order=False).apply(func_0_gp__date__OPEN)
df = df.sort(by=["date", "sw_l1"]).groupby(by=["date", "sw_l1"], maintain_order=False).apply(func_0_gp__date__sw_l1)
df = df.sort(by=["date"]).groupby(by=["date"], maintain_order=False).apply(func_1_cs__date)
df = df.sort(by=["asset", "date"]).groupby(by=["asset"], maintain_order=True).apply(func_1_ts__asset__date)
df = func_1_cl(df)
df = df.sort(by=["asset", "date"]).groupby(by=["asset"], maintain_order=True).apply(func_2_ts__asset__date)
df = df.sort(by=["date"]).groupby(by=["date"], maintain_order=False).apply(func_2_cs__date)
df = df.sort(by=["asset", "date"]).groupby(by=["asset"], maintain_order=True).apply(func_3_ts__asset__date)


# x_0 = ts_mean(OPEN, 10)
# x_1 = ts_mean(CLOSE, 10)
# x_2 = cs_rank(x_0)
# x_3 = cs_rank(x_1)
# x_4 = abs(log(x_1))
# x_5 = gp_rank(OPEN, CLOSE)
# x_6 = gp_rank(sw_l1, CLOSE)
# x_7 = cs_rank(OPEN)
# x_8 = ts_mean(x_7, 10)
# expr_1 = -ts_corr(x_2, x_3, 10)
# expr_2 = x_2 - x_4 + x_5 + x_6
# expr_3 = ts_mean(x_2, 10)
# expr_4 = cs_rank(x_8)
# expr_5 = -ts_corr(OPEN, CLOSE, 10)

# expr_1 = -ts_corr(cs_rank(ts_mean(OPEN, 10)), cs_rank(ts_mean(CLOSE, 10)), 10)
# expr_2 = -abs(log(ts_mean(CLOSE, 10))) + cs_rank(ts_mean(OPEN, 10)) + gp_rank(OPEN, CLOSE) + gp_rank(sw_l1, CLOSE)
# expr_3 = ts_mean(cs_rank(ts_mean(OPEN, 10)), 10)
# expr_4 = cs_rank(ts_mean(cs_rank(OPEN), 10))
# expr_5 = -ts_corr(OPEN, CLOSE, 10)

# drop intermediate columns
df = df.drop(columns=filter(lambda x: re.search(r"^x_\d+", x), df.columns))

# shrink
df = df.select(cs.all().shrink_dtype())
df = df.shrink_to_fit()

logger.info("done")

# save
# df.write_parquet('output.parquet', compression='zstd')

print(df.tail(5))
