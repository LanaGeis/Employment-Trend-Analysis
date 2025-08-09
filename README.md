# Term Project: Is AI taking our jobs or transforming them?
A short, milestone-based data preparation and analysis project exploring how automation and AI relate to changes in occupations and skills. Work is organized in Jupyter notebooks across milestones (data collection, cleaning, merging, and basic analysis/visualization).
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
- Public labor statistics and occupation/skills datasets
- Web pages and APIs referenced in the milestone notebooks

## Notes
- Do not commit secrets. Keep files like env_var.env and any API key files out of version control.
- Use your conda environment for all work in this project.
