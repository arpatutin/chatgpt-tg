#!/bin/bash
echo Setting the variables...

export OPENAI_API_KEY="Insert your OpenAI api key here"
export TELEGRAM_KEY="Insert your Telegram api key here"

echo Successfully.

echo *

echo Starting the Python script...

cd ..
python3 main.py

echo The execution\'s finished.
