import discord
import random
import os


class Markov:
    def __init__(self):
        self.words = {}

    def append(self, sentence):
        sentence = sentence.split(" ")
        for i, token in enumerate(sentence):
            if i == len(sentence) - 1:
                break
            word_to_append = sentence[i + 1]
            word_to_append = str.strip(word_to_append)
            if not self.words.keys().__contains__(token):
                self.words[token] = [word_to_append]
            else:
                self.words[token].append(word_to_append)

    def gen_sentence(self, n) -> str:
        word = " "
        sentence = []
        next_word = ""
        while not word[0].isupper():
            word = random.choice(list(self.words.keys()))
            next_word = word
        sentence.append(next_word)
        for i in range(n):
            next_word = random.choice(list(self.words[next_word]))
            sentence.append(next_word)
        return str.join(" ", sentence)


class Bot(discord.Client):
    def __init__(self, markov: Markov):
        super().__init__()
        self.markov = markov

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('markov pls'):
            print("markov pls")
            count = self.get_count(message.content)
            await message.channel.send(self.markov.gen_sentence(count))
            return
        self.markov.append(message.content)
        print('Appending {0.content}'.format(message))

    @staticmethod
    def get_count(command: str) -> int:
        tokens = command.split(" ")
        if tokens[2].isdigit() and 3 < int(tokens[2]) < 40:
            return int(tokens[2])
        return 7


def main():
    token = os.getenv("DISCORD_TOKEN")
    markov = Markov()
    client = Bot(markov)
    client.run(token)


if __name__ == '__main__':
    main()
