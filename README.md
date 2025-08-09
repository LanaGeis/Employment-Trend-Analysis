# Term Project: Is AI taking our jobs or transforming them?
A short, milestone-based data preparation and analysis project exploring how automation and AI relate to changes in occupations and skills. Work is organized in Jupyter notebooks across milestones (data collection, cleaning, merging, and basic analysis/visualization).
## Project structure

├─ data/                 # Raw and intermediate datasets (CSV/HTML/etc.)
├─ notebooks/            # Jupyter notebooks for milestones and analysis
│  ├─ milestone1_*.ipynb
│  ├─ milestone2_*.ipynb
│  ├─ milestone3_*.ipynb
│  └─ ...
├─ scripts/              # Reusable Python utilities and helpers
├─ models/               # Saved models/artifacts
├─ api_responses/        # Cached API responses for reproducibility
├─ output/               # Generated reports, figures, and exports
├─ requirements.txt      # Python dependencies list
├─ env_template.env      # Example environment variables (no secrets)
└─ README.md             # Project overview and instructions

## Quick start
- Requirements:
    - Conda environment (Python 3.10.18)
    - Jupyter

- Create and activate a conda environment:
``` bash
# bash
conda create -n ai-jobs python=3.10.18 -y
conda activate ai-jobs
conda install pandas requests beautifulsoup4 python-dotenv numpy jupyter -y
```
- Launch Jupyter:
``` bash
# bash
jupyter notebook
```
## Configuration
Create a local environment file at the project root (not committed to Git) to hold data paths and credentials. Example:
``` ini
# ini
# Save as: env_var.env

# API credentials (placeholders)
ONET_API_USERNAME=your_username_here
ONET_API_PASSWORD=your_password_here
ONET_API_KEY=your_key_here

# Local data paths (adjust to your system)
declining_path=data/Fastest declining occupations.html.html
growing_path=data/Fastest growing occupations.html.html
SOC_codes_path=data/soc_structure_2018 - occupations.csv
NAICS_codes_path=data/2022_NAICS_Structure_Summary_Table - industry.csv
```
Notebooks will load environment variables with python-dotenv. Keep real secrets only in your local env file.
## Data sources
- Bureau of Labor Statistics (BLS) — SOC structure and occupational statistics

- U.S. Census Bureau — NAICS industry structure

- O*NET API — Skills and job requirements data

- Public HTML tables (“Fastest growing/declining occupations”)

- Additional datasets from APIs and public data portals

## Power BI Reports
Power BI report files are located in the *pbi_reports* folder.

## Notes
- Keep secrets private — exclude env_var.env and any credential files from version control.

- Always work inside the Conda environment (ai-jobs) to ensure package consistency.

- Follow milestone notebooks in order for reproducible results.

- For Power BI integration, connect to the SQLite database generated in Milestone 5.

