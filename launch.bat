@echo off
set CONDA_ENV=base


CALL "%USERPROFILE%\anaconda3\Scripts\activate.bat"

CALL conda activate %CONDA ENV%

python gui.py