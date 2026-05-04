def filter_data(df, secteur=None, annee=None, region=None, departement=None, commune=None):

    if secteur:
        df = df[df["secteur"] == secteur]

    if annee:
        df = df[df["annee"] == annee]

    if region:
        df = df[df["region"] == region]

    if departement:
        df = df[df["departement"] == departement]

    if commune:
        df = df[df["commune"] == commune]

    return df