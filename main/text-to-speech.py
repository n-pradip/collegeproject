# import numpy as np
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import cmudict
# import random

# # Load the CMU Pronouncing Dictionary
# nltk.download('cmudict')
# pronouncing_dict = cmudict.dict()

# def preprocess_text(text):
#     tokens = word_tokenize(text.lower())  # Tokenize the text and convert to lowercase
#     return tokens

# def extract_features(tokens):
#     features = []
#     for token in tokens:
#         if token in pronouncing_dict:
#             phonemes = pronouncing_dict[token][0]  # Take the first pronunciation
#             features.append(phonemes)
#     return features

# # Speech Synthesis Model
# class SimpleConcatenativeSynthesis:
#     def __init__(self):
#         pass
    
#     def generate_speech(self, features):
#         speech = []
#         for phonemes in features:
#             # For simplicity, we'll randomly select a word with the same phonemes from the dictionary
#             word_list = [word for word, phoneme_list in pronouncing_dict.items() if phoneme_list == phonemes]
#             if len(word_list) > 0:
#                 selected_word = random.choice(word_list)
#                 speech.append(selected_word)
#             else:
#                 speech.append("UNKNOWN")
#         return ' '.join(speech)

# # Training (Not implemented in this example)
# # In a real-world scenario, you would need a dataset of text-speech pairs to train the model.

# # Example Usage
# if __name__ == "__main__":
#     input_text = "Hello, how are you doing today?"
    
#     tokens = preprocess_text(input_text)
    
#     features = extract_features(tokens)
    
#     tts_model = SimpleConcatenativeSynthesis()
#     generated_speech = tts_model.generate_speech(features)
    
#     print("Generated Speech:", generated_speech)

import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import cmudict
import random
from gtts import gTTS

# Load the CMU Pronouncing Dictionary
nltk.download('cmudict')
pronouncing_dict = cmudict.dict()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize the text and convert to lowercase
    return tokens

def extract_features(tokens):
    features = []
    for token in tokens:
        if token in pronouncing_dict:
            phonemes = pronouncing_dict[token][0]  # Take the first pronunciation
            features.append(phonemes)
    return features

# Speech Synthesis Model
class SimpleConcatenativeSynthesis:
    def __init__(self):
        pass
    
    def generate_speech(self, features):
        speech = []
        for phonemes in features:
            # For simplicity, we'll randomly select a word with the same phonemes from the dictionary
            word_list = [word for word, phoneme_list in pronouncing_dict.items() if phoneme_list == phonemes]
            if len(word_list) > 0:
                selected_word = random.choice(word_list)
                speech.append(selected_word)
            else:
                speech.append("UNKNOWN")
        return ' '.join(speech)

# Example Usage
if __name__ == "__main__":
    input_text = "Hello, how are you doing today?"
    
    tokens = preprocess_text(input_text)
    
    features = extract_features(tokens)
    
    tts_model = SimpleConcatenativeSynthesis()
    generated_speech = tts_model.generate_speech(features)
    
    tts = gTTS(text=generated_speech, lang='en', slow=False)
    tts.save("output_audio.mp3")
