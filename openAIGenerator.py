import openai
import os

class OpenAIGen:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.set_key()

    def set_key(self):
        # If the API key is not set as a system variable, the user will be prompted to enter it.
        # To avoid entering the key each time, you can set the key as a system variable named 'OPENAI_API_KEY'.
        while not self.api_key:
            self.api_key = input("Please enter your OpenAI API key: ")
            openai.api_key = self.api_key
            if not self.is_valid_key():
                print("Invalid API key. Please try again.")
                self.api_key = None

    def is_valid_key(self):
        try:
            openai.Engine.list()
            return True
        except openai.InvalidApiKeyError:
            return False

    def gpt(self, prompt, engine="text-davinci-003", temperature=0.7, max_tokens=150, top_p=1, frequency_penalty=0, presence_penalty=0, n=1, stop=None, echo=False):
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            n=n,
            stop=stop,
            echo=echo
        )

        if n == 1:
            return response.choices[0].text
        else:
            return [choice.text for choice in response.choices]

def main():
    gen = OpenAIGen()

    # Define your prompt
    prompt = "Write a short and sweet text about any topic."

    # Call the gpt function
    generated_text = gen.gpt(prompt)

    # Print the generated text
    print(generated_text)

if __name__ == "__main__":
    main()
