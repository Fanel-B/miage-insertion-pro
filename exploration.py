import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-whitegrid')

df = pd.read_csv("fr-esr-insersup.csv", sep=";", encoding="utf-8", low_memory=False)

col_salaire = "30-Salaire mensuel net médian en équivalent temps plein - 30 mois après le diplôme"

DIPLOME_MIAGE = "METHODES INFORMATIQUES APPLIQUEES A LA GESTION DES ENTREPRISES-MIAGE"
HORIZONS = ["6", "12", "30"]

def col_emploi(horizon):
    return f"{horizon}-Taux d'emploi salarié en France - {horizon} mois après le diplôme"


#Partie 1 : MIAGE Toulouse vs autres villes

academies = ["Toulouse", "Paris", "Lyon", "Bordeaux"]

miage = df[
    (df["Libellé du diplôme"] == DIPLOME_MIAGE) &
    (df["Académie"].isin(academies)) &
    (df["Genre"] == "ensemble") &
    (df["Nationalité"] == "ensemble") &
    (df["Régime d'inscription"] == "ensemble") &
    (df["Obtention du diplôme"] == "diplômé") &
    (df["Promotion"].isin(["2019", "2020", "2021", "2022", "2023"]))
].copy()

for h in HORIZONS:
    miage[col_emploi(h)] = pd.to_numeric(miage[col_emploi(h)], errors="coerce")
miage[col_salaire] = pd.to_numeric(miage[col_salaire], errors="coerce")

# Un sous-graphique par horizon (6, 12, 30 mois), même échelle pour comparer facilement
fig, axes = plt.subplots(1, 3, figsize=(16, 5.5), sharey=True)

for ax, h in zip(axes, HORIZONS):
    emploi_villes = miage.groupby(["Académie", "Promotion"])[col_emploi(h)].mean().reset_index()
    pivot = emploi_villes.pivot(index="Promotion", columns="Académie", values=col_emploi(h)).sort_index()
    for ville in pivot.columns:
        ax.plot(pivot.index, pivot[ville], marker="o", label=ville)
    ax.set_title(f"À {h} mois")
    ax.set_xlabel("Promotion")

axes[0].set_ylabel("Taux d'emploi salarié en France (%)")
axes[0].legend(title="Académie")
fig.suptitle("Taux d'emploi des diplômés MIAGE par ville, selon l'ancienneté (2019-2023)", fontsize=13)
plt.tight_layout()
plt.savefig("images/taux_emploi_miage_villes.png", dpi=150)
plt.show()

salaire_villes = miage.groupby(["Académie", "Promotion"])[col_salaire].mean().reset_index()
pivot_salaire = salaire_villes.pivot(index="Promotion", columns="Académie", values=col_salaire).sort_index()

couleurs = {"Paris": "#2563EB", "Toulouse": "#DC2626", "Bordeaux": "#059669", "Lyon": "#D97706"}

fig, ax = plt.subplots(figsize=(11, 6.5))
for ville in pivot_salaire.columns:
    serie = pivot_salaire[ville].dropna()
    ax.plot(pivot_salaire.index, pivot_salaire[ville], marker="o", markersize=8,
            linewidth=2.5, label=ville, color=couleurs.get(ville))
    if len(serie) > 0:
        ax.annotate(f"{int(serie.iloc[-1])}€", (serie.index[-1], serie.iloc[-1]),
                    textcoords="offset points", xytext=(10, 0),
                    fontsize=10, fontweight="bold", color=couleurs.get(ville))

ax.set_title("Salaire médian à 30 mois — Diplômés MIAGE par ville", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("Promotion")
ax.set_ylabel("Salaire mensuel net médian (€)")
ax.legend(title="Ville", loc="lower right")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.text(0.02, 0.02, "Lyon non affiché : données non communiquées (secret statistique, petits effectifs)",
        transform=ax.transAxes, fontsize=8, style="italic", color="gray")
plt.tight_layout()
plt.savefig("images/salaire_miage_villes.png", dpi=200, bbox_inches="tight")
plt.show()


#Partie 2 : l'informatique face aux autres secteurs 

tous = df[
    (df["Académie"] != "National") &
    (df["Genre"] == "ensemble") &
    (df["Nationalité"] == "ensemble") &
    (df["Régime d'inscription"] == "ensemble") &
    (df["Obtention du diplôme"] == "diplômé") &
    (df["Type de diplôme"] == "Master LMD") &
    (df["Secteur disciplinaire"] != "Tous secteurs disciplinaires")
].copy()

for h in HORIZONS:
    tous[col_emploi(h)] = pd.to_numeric(tous[col_emploi(h)], errors="coerce")
tous[col_salaire] = pd.to_numeric(tous[col_salaire], errors="coerce")

secteurs = tous.groupby("Secteur disciplinaire").agg(
    **{f"taux_{h}": (col_emploi(h), "mean") for h in HORIZONS},
    n=(col_emploi("30"), "count")
).reset_index()

# Classement basé sur le taux à 30 mois, on garde le top 15 avec assez d'effectif
top_secteurs = secteurs[secteurs["n"] >= 30].sort_values("taux_30", ascending=False).head(15)
top_secteurs = top_secteurs.iloc[::-1]  # pour un affichage du meilleur en haut du graphique

y = range(len(top_secteurs))
hauteur = 0.25
couleurs_horizon = {"6": "#94A3B8", "12": "#60A5FA", "30": "#DC2626"}

plt.figure(figsize=(11, 8))
for i, h in enumerate(HORIZONS):
    decalage = (i - 1) * hauteur
    plt.barh([p + decalage for p in y], top_secteurs[f"taux_{h}"], height=hauteur,
             label=f"{h} mois", color=couleurs_horizon[h])

plt.yticks(list(y), top_secteurs["Secteur disciplinaire"])
plt.xlabel("Taux d'emploi moyen (%)")
plt.title("Top 15 des secteurs disciplinaires par taux d'emploi, selon l'ancienneté (Master)")
plt.legend(title="Ancienneté")
plt.tight_layout()
plt.savefig("images/classement_secteurs.png", dpi=150)
plt.show()


#  Partie 3 : la MIAGE face aux autres diplômes d'informatique


info = tous[tous["Secteur disciplinaire"] == "Informatique"].copy()

diplomes_info = info.groupby("Libellé du diplôme").agg(
    **{f"taux_{h}": (col_emploi(h), "mean") for h in HORIZONS},
    n=(col_emploi("30"), "count")
).reset_index()

diplomes_info = diplomes_info[diplomes_info["n"] >= 5].sort_values("taux_30", ascending=False)
diplomes_info = diplomes_info.iloc[::-1]

y = range(len(diplomes_info))
hauteur = 0.25

plt.figure(figsize=(11, 7))
for i, h in enumerate(HORIZONS):
    decalage = (i - 1) * hauteur
    plt.barh([p + decalage for p in y], diplomes_info[f"taux_{h}"], height=hauteur,
             label=f"{h} mois", color=couleurs_horizon[h])

plt.yticks(list(y), diplomes_info["Libellé du diplôme"])
plt.xlabel("Taux d'emploi moyen (%)")
plt.title("Diplômes du secteur Informatique par taux d'emploi, selon l'ancienneté (Master)")
plt.legend(title="Ancienneté")
plt.tight_layout()
plt.savefig("images/classement_diplomes_info.png", dpi=150)
plt.show()

print(diplomes_info)