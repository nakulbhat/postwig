from rich.tree import Tree as RichTree
import sys, os
import json
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

def to_rich_tree(token, tree=None, verbose=False):
    color = POS_COLORS.get(token.pos_, "white")
    if verbose:
        label = f"[{color}]{token.text}[/{color}] [dim]{token.pos_}/{token.dep_} (morph: {token.morph})[/dim]"
    else:
        label = f"[{color}]{token.text}[/{color}] [dim]{token.pos_}/{token.dep_}[/dim]"
    node = tree.add(label) if tree else RichTree(label)
    for child in token.children:
        to_rich_tree(child, node, verbose=verbose)
    return node

def to_dict(token, verbose=False):
    entry = {
        "text": token.text,
        "pos": token.pos_,
        "dep": token.dep_,
    }
    if verbose:
        entry["morph"] = str(token.morph)
        entry["lemma"] = token.lemma_
        entry["shape"] = token.shape_
    entry["children"] = [to_dict(child, verbose=verbose) for child in token.children]
    return entry

def main():
    FLAGS = {"-v", "--verbose", "--json", "--tree", "--help"}
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    as_json = "--json" in sys.argv
    show_help = "--help" in sys.argv
    sentence = " ".join(w for w in sys.argv[1:] if w not in FLAGS)

    prog = os.path.splitext(os.path.basename(sys.argv[0]))[0]

    if show_help:
        print(f"Usage: {prog} [options] <sentence>")
        print()
        print("Parse a sentence and display its dependency tree.")
        print()
        print("Arguments:")
        print("  sentence          The sentence to parse")
        print()
        print("Options:")
        print("  -v, --verbose     Show extra token info (morphology, lemma, shape)")
        print("  --json            Output as JSON")
        print("  --tree            Output as tree (default)")
        print("  --help            Show this message and exit")
        return 0

    if not sentence.strip():
        print(f"Usage: {prog} [options] <sentence>")
        print(f"Try '{prog} --help' for more information.")
        return 1

    doc = nlp(sentence)
    root = next(t for t in doc if t.head == t)

    if as_json:
        print(json.dumps(to_dict(root, verbose=verbose), indent=2))
    else:
        from rich import print as rprint
        rprint(to_rich_tree(root, verbose=verbose))

    return 0
if __name__ == "__main__":
    sys.exit(main())
