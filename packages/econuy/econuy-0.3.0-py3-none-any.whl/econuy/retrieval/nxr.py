from os import PathLike
from pathlib import Path
from typing import Union

import pandas as pd
from pandas.tseries.offsets import MonthEnd

from econuy.resources import updates, columns
from econuy.resources.lstrings import nxr_url


def get(update: Union[str, PathLike, None] = None, 
        revise_rows: Union[str, int] = 0,
        save: Union[str, PathLike, None] = None, 
        force_update: bool = False, name: Union[str, None] = None):
    """Get nominal exchange rate data.

    Parameters
    ----------
    update : str, PathLike or None, default is None
        Path or path-like string pointing to a directory where to find a CSV 
        for updating, or None, don't update.
    revise_rows : str or int, default is 0
        How many rows of old data to replace with new data.
    save : str, PathLike or None, default is None
        Path or path-like string pointing to a directory where to save the CSV, 
        or None, don't update.
    force_update : bool, default is False
        If True, fetch data and update existing data even if it was modified
        within its update window (for nominal exchange rate, 25 days).
    name : str or None, default is None
        CSV filename for updating and/or saving.

    Returns
    -------
    nxr : Pandas dataframe

    """
    update_threshold = 25
    if name is None:
        name = "nxr"

    if update is not None:
        update_path = (Path(update) / name).with_suffix(".csv")
        delta, previous_data = updates._check_modified(update_path)

        if delta < update_threshold and force_update is False:
            print(f"{update_path} was modified within {update_threshold} "
                  f"day(s). Skipping download...")
            return previous_data

    nxr_raw = pd.read_excel(nxr_url, skiprows=4)
    nxr = (nxr_raw.dropna(axis=0, thresh=4).set_index("Mes y año").
           dropna(axis=1, how="all").rename_axis(None))
    nxr.columns = ["Tipo de cambio compra, fin de período",
                   "Tipo de cambio venta, fin de período",
                   "Tipo de cambio compra, promedio",
                   "Tipo de cambio venta, promedio"]
    nxr.index = nxr.index + MonthEnd(1)

    if update is not None:
        nxr = updates._revise(new_data=nxr, prev_data=previous_data,
                              revise_rows=revise_rows)

    nxr = nxr.apply(pd.to_numeric, errors="coerce")
    columns._setmeta(nxr, area="Precios y salarios", currency="-",
                     inf_adj="No", index="No", seas_adj="NSA",
                     ts_type="-", cumperiods=1)

    if save is not None:
        save_path = (Path(save) / name).with_suffix(".csv")
        nxr.to_csv(save_path)

    return nxr
