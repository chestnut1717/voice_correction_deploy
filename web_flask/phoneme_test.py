from utils import phonemize

if __name__ == "__main__":
    test = "Hello, my name is Ryan"
    test_pho = phonemize.text_to_phoneme(test, is_stress=True)
    print(test_pho)