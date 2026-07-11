# ==========================================
# LISTE DES SECTEURS
# ==========================================
SECTEURS = [
'AGRICULTURE',
'AQUACULTURE',
'ASSAINISSEMENT',
'COMMERCE_ARM',
'CULTURE',
'EAU',
'ELEVAGE',
'ENERGIE',
'FAMILLE_AUTONOMISATION',
'GESTION_FONCIERE',
'GOUVERNANCE_TERRITORIALE',
'HYGIENE',
'INDUSTRIE_ARTISANAT',
'JEUNESSE',
'MINES_GEOLOGIE',
'PECHE',
'PROTECTION_JUDICIAIRE_SOCIALE_AEMO',
'SANTE',
'SFD_BANQUES',
'SPORTS',
'TIC',
'TOURISME',
'TRANSPORTS',
'VULNERABILITE_PROTECTION_SOCIALE',
'CENTRE_FORMATION',
'DAARA',
'ELEMENTAIRE',
'MOYEN',
'PRESCOLAIRE',
'SECONDAIRE'
]


# ==========================================
# MOTS CLES DES INDICATEURS DE TYPE TAUX
# ==========================================
# Si un indicateur contient un de ces mots,
# il sera automatiquement agrégé par MOYENNE.
#
# Les autres indicateurs seront agrégés
# par SOMME.
# ==========================================

TAUX_KEYWORDS = [

    "taux",
    "ratio",
    "%",
    "proportion",
    "pourcentage",
    "moyenne",
    "prévalence",
    "prevalence",
    "incidence",
    "couverture",
    "fréquence",
    "frequence",
    "indice",
    "densité",
    "densite",
    "tap",
    "tbs",
    "tba",
    "tbn",
    "espérance",
    "esperance",

    # Santé
    "sf/far",
    "far/sf",

    # Education
    "réussite",
    "reussite",
    "admission",
    "achèvement",
    "achevement",

    # Eau
    "accès",
    "acces",

    # Agriculture
    "rendement",

    # Finances
    "croissance",

    # Santé maternelle
    "césarienne",
    "cesarienne"
]


# ==========================================
# FORMAT D'AFFICHAGE
# ==========================================

NB_DECIMALES_TAUX = 2

NB_DECIMALES_BRUT = 0


# ==========================================
# LABELS
# ==========================================

LABEL_BRUT = "Somme"

LABEL_TAUX = "Moyenne"


# ==========================================
# TEXTE AFFICHAGE NA
# ==========================================

LABEL_NA = "NA"

LABEL_OBSERVATIONS = "Observations"


# ==========================================
# EXPORTS
# ==========================================

EXPORT_IMAGE_SCALE = 2

EXPORT_IMAGE_WIDTH = 1400

EXPORT_IMAGE_HEIGHT = 800