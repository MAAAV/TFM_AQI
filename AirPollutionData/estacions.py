# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

from . import EOI_DF

# ---------------------------------------------------------------------------------------------------------------------
def get_nom_eoi(codi):
    df = EOI_DF[EOI_DF.codi_eoi == codi]
    if df.shape[0] == 1:
        return df['nom_eoi'].iloc[0]
    else:
        return f"None"


def get_codi_eoi(nom):
    df = EOI_DF[EOI_DF.nom_eoi == nom]
    if df.shape[0] == 1:
        return df['codi_eoi'].iloc[0]
    else:
        return f"None"


# ---------------------------------------------------------------------------------------------------------------------
# test unitari
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    nom = get_nom_eoi('08101001')
    print(f"{codi} -> {nom}")
    codi = get_codi_eoi(nom)
    print(f"{nom} -> {codi}")