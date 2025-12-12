# ChEMBL EGFR Molecule Search

This project queries the ChEMBL REST API to extract molecules targeting
the Epidermal Growth Factor Receptor (EGFR) along with their bioactivity data.

## Objective
- Demonstrate usage of a scientific REST API
- Handle pagination and server-side errors
- Extract and clean molecular activity data

## Target
- EGFR (ChEMBL ID: CHEMBL203)

## Extracted Fields
- Molecule ChEMBL ID
- Target ChEMBL ID
- Activity type (IC50, etc.)
- Activity value and units
- Assay description

## Technologies Used
- Python 3
- ChEMBL REST API
- requests
- pandas

## How to Run

```bash
pip install -r requirements.txt
python src/chembl_egfr_extractor.py
