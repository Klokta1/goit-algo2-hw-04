from trie import Trie


def validate_param(param, param_name: str)-> None :
    if not isinstance(param, str):
        raise TypeError(f"Illegal argument for {param_name}: {param} must be a string")


class Homework(Trie):
    def count_words_with_suffix(self, pattern) -> int:
        validate_param(pattern, "pattern")
        return sum([1 for el in self.keys() if el.endswith(pattern)])

    def has_prefix(self, prefix) -> bool:
        validate_param(prefix, "prefix")
        return self.keys_with_prefix(prefix) != []


if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat
