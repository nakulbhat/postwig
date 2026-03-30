from rich.tree import Tree as RichTree
import sys
import en_core_web_sm

nlp = en_core_web_sm.load()

POS_COLORS = {
    "NOUN": "cyan",
    "VERB": "green",
    "DET": "dim",
    "ADP": "yellow",
    "ADJ": "magenta",
    "ADV": "blue",
}

def to_rich_tree(token, tree=None):
    color = POS_COLORS.get(token.pos_, "white")
    label = f"[{color}]{token.text}[/{color}] [dim]{token.pos_}/{token.dep_}[/dim]"
    node = tree.add(label) if tree else RichTree(label)
    for child in token.children:
        to_rich_tree(child, node)
    return node

def main():
    if (len(sys.argv) < 2):
        print(f"Usage: {sys.argv[0]} <sentence>")
        return -1

    sentence = " ".join(sys.argv[1:])
    doc = nlp(sentence)
    root = next(t for t in doc if t.head == t)

    from rich import print
    print(to_rich_tree(root))

    return 0
if __name__ == "__main__":
    main()
