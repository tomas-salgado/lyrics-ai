from typing import List, Dict
import os
import anthropic
from .urban_dictionary import define
from dotenv import load_dotenv
from better_profanity import profanity

load_dotenv()

class LyricsInterpreter:
    def __init__(self):
        self.claude_api_key = os.getenv('CLAUDE_API_KEY')
        self.client = anthropic.Anthropic(api_key=self.claude_api_key)

    def filter_text(self, text: str) -> str:
        return profanity.censor(text)

    def detect_slang(self, text: str) -> List[str]:
        words = text.split()
        all_combinations = []
        
        for i in range(len(words)):
            for j in range(1, min(5, len(words) - i + 1)):
                all_combinations.append(' '.join(words[i:i+j]))
        
        if len(words) <= 5:
            all_combinations.append(text)
        
        all_combinations.sort(key=len, reverse=True)
        
        system_prompt = """You are an expert in identifying slang terms and phrases in text. 
        Given the following list of words and phrases, identify which ones are slang or have 
        idiomatic meanings. Consider both individual words and multi-word expressions, 
        prioritizing longer phrases that might have unique meanings. 
        Respond with only a Python list of strings containing the identified slang terms and phrases."""
        
        message = f"If you know what a word means AND it is not slang, remove it from the list: {all_combinations}. IMPORTANT: Return only a Python list of strings containing the identified slang and unknown terms and phrases."
        response = self.call_api(system_prompt, message)
        
        response = response.strip()
        if response.startswith("[") and response.endswith("]"):
            response = response[1:-1] 
        
        terms = [term.strip().strip("'\"") for term in response.split(",")]
        
        return [term for term in terms if term]

    def get_urban_dictionary_definitions(self, terms: List[str]) -> Dict[str, str]:
        definitions = {}
        for term in terms:
            urban_defs = define(term)
            if urban_defs:
                definitions[term] = urban_defs[0].definition
            else:
                definitions[term] = "No definition found"
        return definitions

    def interpret_text(self, text: str, slang_definitions: Dict[str, str]) -> str:
        system_prompt = "You are an expert in interpreting text with slang terms. Given the original text and a dictionary of slang definitions, provide a clear interpretation of the text. The interpretation should be in a casual tone, and only include slang terms that are present in the original text, and not the definitions. IMPORTANT: response should be one sentence total."
        message = f"Interpret this text: {text}\n\nSlang definitions: {slang_definitions}"
        return self.call_api(system_prompt, message, max_tokens=2000)

    def process_text(self, text: str) -> Dict:
        filtered_text = self.filter_text(text)
        slang_terms = self.detect_slang(filtered_text)
        slang_definitions = self.get_urban_dictionary_definitions(slang_terms)
        interpretation = self.interpret_text(filtered_text, slang_definitions)

        return {
            "original_text": text,
            "interpretation": interpretation
        }
    
    def call_api(self, system_prompt: str, message: str, max_tokens: int = 1000) -> str:
        messages = [
            {"role": "user", "content": message}
        ]
        response = ""
        with self.client.messages.stream(
            model="claude-3-sonnet-20240229",
            max_tokens=max_tokens,
            temperature=0,
            messages=messages
        ) as stream:
            for text in stream.text_stream:
                response += text
        return response

if __name__ == "__main__":
    interpreter = LyricsInterpreter()
    
    while True:
        user_input = input("Enter text (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        result = interpreter.process_text(user_input)
        print(f"Original: {result['original_text']}")
        print(f"Interpretation: {result['interpretation']}")
        print()

