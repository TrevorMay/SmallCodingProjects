# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
from plexapi.myplex import MyPlexAccount
import pandas as pd
from rapidfuzz import fuzz
from dotenv import load_dotenv
import os

load_dotenv()

PLEX_TOKEN = os.getenv("PLEX_TOKEN")

WATCHLIST_CSV = r"C:\Users\T\Downloads\letterboxd-thulium-2026-01-28-19-13-utc\watchlist.csv"
OUTPUT_CSV = "watchlist_plex_comparison.csv"

FUZZY_MATCH_THRESHOLD = 90


# %%
account = MyPlexAccount(token=PLEX_TOKEN)

resources = account.resources()
print("Accessible Plex servers:")
for r in resources:
    print(f"- {r.name} (owned={r.owned})")



# %%
plex_movies = []

for resource in account.resources():
    try:
        plex = resource.connect()
    except Exception:
        continue  # skip unreachable servers

    for section in plex.library.sections():
        if section.type != "movie":
            continue

        for movie in section.all():
            tmdb_id = None
            for guid in movie.guids:
                if "themoviedb" in guid.id:
                    tmdb_id = guid.id.split("://")[1]

            plex_movies.append({
                "server": resource.name,
                "title": movie.title,
                "norm_title": movie.title.lower().strip(),
                "year": movie.year,
                "tmdb_id": tmdb_id
            })


# %%
def normalize_title(title):
    return title.lower().strip()

def extract_tmdb_id(guids):
    for guid in guids:
        if "themoviedb" in guid.id:
            return guid.id.split("://")[1]
    return None


watchlist = pd.read_csv(WATCHLIST_CSV)
watchlist["norm_title"] = watchlist["Name"].apply(normalize_title)

# %%
plex_df = pd.DataFrame(plex_movies)

# =========================
# MATCHING LOGIC
# =========================

results = []

for _, row in watchlist.iterrows():
    found_on = []
    match_type = None

    # 1️⃣ TMDB ID match (best)
    if "tmdbID" in watchlist.columns and pd.notna(row["tmdbID"]):
        matches = plex_df[plex_df["tmdb_id"] == str(row["tmdbID"])]
        if not matches.empty:
            found_on = matches["server"].unique().tolist()
            match_type = "TMDB"

    # 2️⃣ Exact title + year
    if not found_on:
        matches = plex_df[
            (plex_df["norm_title"] == row["norm_title"]) &
            (plex_df["year"] == row["Year"])
        ]
        if not matches.empty:
            found_on = matches["server"].unique().tolist()
            match_type = "Title+Year"

    # 3️⃣ Fuzzy title match
    if not found_on:
        for _, pm in plex_df.iterrows():
            score = fuzz.ratio(row["norm_title"], pm["norm_title"])
            if score >= FUZZY_MATCH_THRESHOLD:
                found_on.append(pm["server"])
                match_type = "Fuzzy"
        found_on = list(set(found_on))

    results.append({
        "Title": row["Name"],
        "Year": row["Year"],
        "Available": bool(found_on),
        "Available On": ", ".join(found_on) if found_on else "—",
        "Match Type": match_type if found_on else "None"
    })

# =========================
# OUTPUT
# =========================

output_df = pd.DataFrame(results)
output_df.to_csv(OUTPUT_CSV, index=False)

print(f"\nDone! Results saved to {OUTPUT_CSV}")

# %%
