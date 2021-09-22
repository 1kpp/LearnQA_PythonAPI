

class TestPhrase:
    def test_check_phrase_length(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, f'Length of the {phrase} is more or equal to 15 symbols'
