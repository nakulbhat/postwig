import spacy
from nltk import Tree
import sys, os
import en_core_web_sm

nlp = en_core_web_sm.load()

def to_nltk_tree(token):
    label = f"{token.text}/{token.pos_}/{token.dep_}"
    if list(token.children):
        return Tree(label, [to_nltk_tree(c) for c in token.children])
    else:
        return label

def main():
    if (len(sys.argv) < 2):
        print(f"Usage: {sys.argv[0]} <sentence>")
        return -1

    sentence = " ".join(sys.argv[1:])
    doc = nlp(sentence)
    root = next(t for t in doc if t.head == t)

    to_nltk_tree(root).pretty_print()

    return 0
if __name__ == "__main__":
    main()
