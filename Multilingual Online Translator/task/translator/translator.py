import requests
from bs4 import BeautifulSoup
import sys

headers = {'User-Agent': 'Mozilla/5.0'}
languages = {1: "Arabic", 2: "German", 3: "English", 4: "Spanish", 5: "French", 6: "Hebrew", 7: "Japanese",
             8: "Dutch", 9: "Polish", 10: "Portuguese", 11: "Romanian", 12: "Russian", 13: "Turkish"}

word_translation = []
examples = []
examples_translated = []
args = sys.argv


language_to_translate = args[1]
language_translate_to = args[2]
word_choice = args[3]

r = requests.get(f"https://context.reverso.net/translation/{language_to_translate}"
                         f"-{language_translate_to}/{word_choice}", headers=headers)


class InvalidLanguageError(Exception):
    pass


class StatusCodeError(Exception):
    pass


class WrongInternetConnection(Exception):
    pass


def single_translate():

    global word_translation

    r = requests.get(f"https://context.reverso.net/translation/{language_to_translate}"
                         f"-{language_translate_to}/{word_choice}", headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    origin = soup.find_all("span", {"class": "display-term"})
    sentences_content = soup.find('section', {"id": 'examples-content'})
    word_translation = [element.text.strip() for element in origin]
    original_sentence_examples = [element.text.strip() for element in
                                      sentences_content.find_all('div', class_='src ltr')]
    translated_sentence_examples = [element.text.strip() for element in
                                        sentences_content.find_all
                                        ('div', {"class": ["trg ltr", "trg rtl arabic", "trg rtl"]})]
    print(f"\n{language_translate_to.capitalize()} Translations:", file=working_file)
    word_translation = word_translation[:1]

    for translation in range(len(word_translation)):
        print(word_translation[translation], file=working_file)

    print(f"\n{language_translate_to.capitalize()} Examples:", file=working_file)

    for a, b in zip(original_sentence_examples[:1], translated_sentence_examples[:1]):
        print(a, file=working_file)
        print(b, '\n', file=working_file)


def multi_translate():

    global word_translation

    for language in languages:
        if language_to_translate.capitalize() == languages[language]:
            continue
        else:
            r = requests.get(f"https://context.reverso.net/translation/{language_to_translate}"f"-{languages[language].lower()}/{word_choice}", headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            origin = soup.find_all("span", {"class": "display-term"})
            sentences_content = soup.find('section', {"id": 'examples-content'})
            word_translation = [element.text.strip() for element in origin]
            original_sentence_examples = [element.text.strip() for element in sentences_content.find_all('div', class_='src ltr')]
            translated_sentence_examples = [element.text.strip() for element in sentences_content.find_all('div', {"class": ["trg ltr", "trg rtl arabic", "trg rtl"]})]

            print(f"\n{languages[language]} Translations:", file=working_file)
            word_translation = word_translation[:1]

            for translation in range(len(word_translation)):
                print(word_translation[translation], file=working_file)

            print(f"\n{languages[language]} Examples:", file=working_file)

            for _, __ in zip(original_sentence_examples[:1], translated_sentence_examples[:1]):
                print(_, file=working_file)
                print(__, '\n', file=working_file)

try:

    if r.status_code != 200:
        raise StatusCodeError
    elif language_to_translate.capitalize() not in languages.values():
        language_entered = language_to_translate
        raise InvalidLanguageError
    elif language_translate_to.capitalize() not in languages.values() and language_translate_to != "all":
        language_entered = language_translate_to
        raise InvalidLanguageError
    else:
        with open(f'{word_choice}.txt', 'w') as working_file:
            if language_translate_to == "all":
                multi_translate()
            else:
                single_translate()
            working_file.close()

        with open(f'{word_choice}.txt', 'r') as working_file:
            content = working_file.read()
            print(content)
            working_file.close()

except InvalidLanguageError:
    print(f"Sorry, the program doesn't support {language_entered}")
except WrongInternetConnection:
    print('Something wrong with your internet connection')
except StatusCodeError:
    print(f"Sorry, unable to find {word_choice}")



# try:
#
#     if r.status_code == 404 or r.:
#         raise StatusCodeError
#     elif r.status_code == 204:
#         raise StatusCodeError
#     elif r.status_code != 200 and r.status_code != 404:
#         raise WrongInternetConnection
#     elif language_to_translate.capitalize() not in languages.values():
#         language_entered = language_to_translate
#         raise InvalidLanguageError
#     elif language_translate_to.capitalize() not in languages.values() and language_translate_to != "all":
#         language_entered = language_translate_to
#         raise InvalidLanguageError
#     else:
#         with open(f'{word_choice}.txt', 'w') as working_file:
#             if language_translate_to == "all":
#                 multi_translate()
#             else:
#                 single_translate()
#             working_file.close()
#
#         with open(f'{word_choice}.txt', 'r') as working_file:
#             content = working_file.read()
#             print(content)
#             working_file.close()
#
# except InvalidLanguageError:
#     print(f"Sorry, the program doesn't support {language_entered}")
# except WrongInternetConnection:
#     print('Something wrong with your internet connection')
# except StatusCodeError:
#     print(f"Sorry, unable to find {word_choice}")
