#!/bin/bash

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment .venv criada."
fi

source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Pacotes instalados na .venv com sucesso!"
