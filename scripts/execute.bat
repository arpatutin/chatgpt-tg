echo Setting the variables...

SET OPENAI_API_KEY="Insert your OpenAI api key here"
SET TELEGRAM_KEY="Insert your Telegram api key here"

echo Successfully.

echo *

echo Starting the Python script...

Pushd ..
python main.py

echo The execution's finished.
pause
