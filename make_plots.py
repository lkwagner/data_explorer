import pandas as pd
import h5py
import numpy as np
import altair as alt
import os
import glob
import uuid

ATTR_NAMES = ['nconfig', 'uuid', 'steprange', 'npts']
DATA_NAMES = ['energy', 'energy_error', 'iteration']

def generate_dataframe():
    print("calling generate_dataframe")
    fnames = glob.glob("static/*.hdf5")
    alldf = []
    for fname in fnames:
        with h5py.File(fname, "r") as f:
            if "energy" not in f.keys():
                continue
            #print(list(f.keys()))
            nsteps = f[DATA_NAMES[0]].shape[0]
            dfthis = {}

            for attr in ATTR_NAMES:
                dfthis[attr] = [f.attrs[attr]]*nsteps
            for val in DATA_NAMES:
                dfthis[val] = f[val][...]
            alldf.append(pd.DataFrame(dfthis))
    return pd.concat(alldf)


def summarize(df):
    """Return a dataframe with the summary data.
    """
    dfret = pd.DataFrame()
    for nm, grp in df.groupby("uuid"):
        maxit = grp["iteration"].max()
        dfret = dfret.append(grp[grp.iteration==maxit])
    return dfret

def timeseries(df):
    base = alt.Chart(df).transform_calculate(
        emin = "datum.energy-datum.energy_error",
        emax = "datum.energy+datum.energy_error"
    )
    chart = (
        base
        .encode(
            alt.X("iteration", type="quantitative", scale=alt.Scale(zero=False)),
            alt.Y("energy", type="quantitative", scale=alt.Scale(zero=False)),
            color=alt.Color("uuid:N",legend=None),
            tooltip=ATTR_NAMES+DATA_NAMES,
        )
        .properties(width=500, height=500)
    )
    errorbars = base.mark_errorbar().encode(
        x="iteration",
        y="emin:Q",
        y2="emax:Q",
        color = "uuid:N"
    )
    return (chart.mark_circle(size=200) + chart.mark_line()+errorbars).interactive()

if __name__ == "__main__":
    df = generate_dataframe()
    print(df)
    print(summarize(df))
