@echo off
IF NOT EXIST ".venv" (
    python -m venv .venv
    echo Virtual environment .venv criada.
)

call .venv\Scripts\activate.bat

pip install --upgrade pip
pip install -r requirements.txt

echo Pacotes instalados na .venv com sucesso!
pause
