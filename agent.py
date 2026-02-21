from transformers import pipeline

class StudyAgent:
    def __init__(self):
        self.generator = pipeline("text-generation", model="gpt2")

    def build_prompt(self, user_input: str):
        return (
            "You are an intelligent study assistant. "
            "Explain clearly and logically.\n\n"
            f"Student question: {user_input}\n"
            "Answer:"
        )

    def run(self, user_input: str):
        prompt = self.build_prompt(user_input)

        output = self.generator(
            prompt,
            max_length=200,
            num_return_sequences=1
        )

        return output[0]["generated_text"]