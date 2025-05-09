source "$(conda info --base)/etc/profile.d/conda.sh"
conda init
conda activate $ENV_NAME
python gui.py