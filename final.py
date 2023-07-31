import telebot
import requests
import openai
import re
# openai.api_key = "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"

# def ai(text):
#     response = openai.Completion.create(
#     model="text-davinci-003",
#     prompt=text, 
#     temperature=0.5,
#     max_tokens=2400,
#     top_p=1.0,
#     frequency_penalty=0.5,
#     presence_penalty=0.0
#     )
#     return response["choices"][0]["text"]

bot_token = '6326953385:AAGpnXi5WO2Nwsm60M9urq3siNPpjPGdAG0'
bot = telebot.TeleBot(bot_token)

def fix_spell(message):
    text = message.text

    lines = text.splitlines()

    corrected_lines = []
    has_errors = False

    for line in lines:
        if line.strip():
            response = requests.get(f'http://speller.yandex.net/services/spellservice.json/checkText?text={line}')
            data = response.json()

            for elem in data:
                line = line.replace(elem['word'], elem['s'][0] if elem['s'] else elem['word'])

            if not has_errors and data:
                has_errors = True

        # Замена "тенге" на символ ₸ выполняется перед заменой кавычек на елочки
        line = line.replace("тенге", "₸").replace("теңге", "₸").replace(" - ", " – ")

        corrected_lines.append(line)

    corrected_text = '\n'.join(corrected_lines)

    # Замена кавычек на елочки
    while re.findall(r'(.*)\“(.*)\”(.*)' , corrected_text):
        corrected_text = re.sub(r'(.*)\“(.*)\”(.*)', r'\1«\2»\3', corrected_text)

    # corrected_text = ai("Проверь мне текст на пунктуацию:\n" + corrected_text)

    if not has_errors:
        corrected_text = "Молодец!\n" + corrected_text

    return corrected_text

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    corrected_text = fix_spell(message)
    bot.send_message(message.chat.id, corrected_text)

if __name__ == "__main__":
    bot.polling()
