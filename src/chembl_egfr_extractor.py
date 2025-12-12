"""
ChEMBL EGFR Molecule Extractor
-----------------------------
This script queries the ChEMBL REST API to retrieve bioactivity data
for molecules targeting EGFR (CHEMBL203). It handles pagination,
server-side errors, and duplicate records, and collects at least
20 unique molecules with activity values.

Author: Areeba Naeem
"""

import requests
import pandas as pd
import time

# =============================
# CONFIGURATION
# =============================

BASE_URL = "https://www.ebi.ac.uk/chembl/api/data/activity.json"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "ChEMBL-Internship-Task"
}

TARGET_CHEMBL_ID = "CHEMBL203"   # EGFR
PAGE_SIZE = 50                  # Smaller page size improves stability
MAX_OFFSET = 2000               # Safety limit for pagination
REQUIRED_MOLECULES = 20


# =============================
# DATA COLLECTION
# =============================

unique_molecules = {}
offset = 0

while len(unique_molecules) < REQUIRED_MOLECULES and offset <= MAX_OFFSET:

    params = {
        "target_chembl_id": TARGET_CHEMBL_ID,
        "limit": PAGE_SIZE,
        "offset": offset
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            headers=HEADERS,
            timeout=30
        )

        # Skip pages that fail due to server-side errors
        if response.status_code != 200:
            print(f"Skipping offset {offset} due to HTTP {response.status_code}")
            offset += PAGE_SIZE
            time.sleep(1)
            continue

        data = response.json()

    except requests.exceptions.RequestException as error:
        print(f"Request failed at offset {offset}: {error}")
        offset += PAGE_SIZE
        time.sleep(1)
        continue

    # Process activity records
    for activity in data.get("activities", []):

        molecule_id = activity.get("molecule_chembl_id")
        activity_value = activity.get("value")

        # Skip incomplete records
        if not molecule_id or not activity_value:
            continue

        # Store only one record per unique molecule
        if molecule_id not in unique_molecules:
            unique_molecules[molecule_id] = {
                "molecule_chembl_id": molecule_id,
                "target": activity.get("target_chembl_id"),
                "activity_type": activity.get("standard_type"),
                "activity_value": activity_value,
                "activity_units": activity.get("units"),
                "assay_description": activity.get("assay_description")
            }

        if len(unique_molecules) >= REQUIRED_MOLECULES:
            break

    offset += PAGE_SIZE
    time.sleep(1)  # Polite delay to avoid overwhelming the API


# =============================
# FINAL DATASET
# =============================

df_unique = pd.DataFrame(unique_molecules.values())

print("Total unique molecules collected:", df_unique.shape[0])
df_unique.head()
