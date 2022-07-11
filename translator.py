import requests
from bs4 import BeautifulSoup


class MultilingualTranslator:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.langs = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish',
                      'Portuguese', 'Romanian', 'Russian', 'Turkish']
        self.response = None
        self.main_lang = ''
        self.main_lang_index = None
        self.chosen_lang = ''
        self.chosen_lang_index = None
        self.chosen_word = ''
        self.translated_words = []
        self.main_sentences = []
        self.translated_sentences = []

    # WELCOME MESSAGE AND DATA COLLECTION
    def data_collector(self):
        print('Type the number of your language: ')
        self.main_lang_index = self.num_checker(input())
        print('Type the number of language you want to translate to:')
        self.chosen_lang_index = self.num_checker(input())
        if self.chosen_lang_index == self.main_lang_index:
            print('Invalid input. Choose two different languages.')
            self.data_collector()
        print('Type the word you want to translate:')
        self.chosen_word = input()

    # CHECKING INPUT NUM
    def num_checker(self, user_input):
        try:
            num = int(user_input)
            if 1 <= num <= 13:
                return num - 1
            else:
                print('Enter a number between 1 and 13.')
                return self.data_collector()
        except ValueError:
            print('Invalid input. Please enter a number.')
            return self.data_collector()

    # SENDING A REQUEST
    def response_getter(self):
        self.main_lang = self.langs[self.main_lang_index].lower()
        self.chosen_lang = self.langs[self.chosen_lang_index].lower()

        self.response = requests.get(
            f'https://context.reverso.net/translation/{self.main_lang}-{self.chosen_lang}/{self.chosen_word}',
            headers=self.headers)

    # TARGETING RIGHT ELEMENTS
    def response_processor(self, response):
        content = BeautifulSoup(response.content, 'html.parser')
        words = content.find_all('span', {'class': 'display-term'})
        main_sentences = content.find_all('div', {'class': 'src'})
        tr_sentences = content.find_all('div', {'class': 'trg'})

        if not words:
            return 0
        self.translated_words = self.content_getter(words)
        self.main_sentences = self.content_getter(main_sentences)
        self.translated_sentences = self.content_getter(tr_sentences)

    # GETTING CONTENT OUT OF ELEMENTS
    @staticmethod
    def content_getter(data):
        if data:
            return [el.text for el in data]

    # GETTING RID OF UNNECESSARY CHARS
    @staticmethod
    def data_polisher(data):
        output = []
        for item in data:
            output.append(item.strip().replace('\n', '').replace('\r', ''))
        return [el for el in output if el != '']

    # PRINTING WORDS ON NEW LINES
    def words_printer(self, words_list):
        print()
        print(f'{self.chosen_lang.capitalize()} Translations:')
        if len(words_list) > 5:
            for i in range(5):
                print(words_list[i].strip())
        else:
            for word in words_list:
                print(word.strip())
        print()

    # PRINTING SENTENCES ON NEW LINES
    @staticmethod
    def sentences_printer(main_sent_list, tr_sent_list):
        for i in range(5):
            print(main_sent_list[i])
            print(tr_sent_list[i])
            if i != 4:
                print()

    # RUNNING THE PROGRAM
    def run(self):
        print('Hello, welcome to the translator. Translator supports: ')
        for i, lang in enumerate(self.langs):
            print(f'{i + 1}: {lang}')
        self.data_collector()
        self.response_getter()
        if self.response_processor(self.response) == 0:
            print('Something went wrong. Check your input and try again.')
            return self.data_collector()
        self.words_printer(self.translated_words)
        print(f'{self.chosen_lang.capitalize()} Examples:')
        self.sentences_printer(self.data_polisher(self.main_sentences), self.data_polisher(self.translated_sentences))


translator = MultilingualTranslator()
translator.run()
