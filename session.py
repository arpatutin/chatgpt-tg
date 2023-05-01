from config import OPENAI_MODEL

import openai
openai.api_key = OPENAI_KEY
ans = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)
print(ans['choices'][0]['message']['content'])


class Session:
    context = []

    def new_message(self, text):
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=self.context + [{"role": "user", "content": text}],
        )
        response = response['choices'][0]['message']['content']
        self.context.append({"role": "user", "content": text})
        self.context.append({"role": "assistant", "content": response})
        return response
