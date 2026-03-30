## `postwig` — CLI Dependency Tree Visualizer

> [!NOTE]
> Part of this readme was generated using AI. The whole readme has been
> manually verified for accuracy.


`postwig` parses an English sentence using spaCy and renders its syntactic dependency tree, showing how words relate to each other (subject, object, modifier, etc.) with POS-tagged, color-coded output. It supports both a pretty Rich tree view and structured JSON output, with an optional verbose mode for morphology and lemma data.

---

### Installation

Nix is needed for installation and dependency management.

**Using `nix develop`**
```bash
nix develop
postwig --help
```

**Using `nix profile install`**

`nix profile install` makes the binary available everywhere in your shell.
```bash
nix profile install .
# nix profile remove postwig # uninstallation command
```



### Usage

```bash
postwig [options] <sentence>
```

### Options

| Flag | Description |
|---|---|
| `-v`, `--verbose` | Show morphology and lemma alongside each token |
| `-j`, `--json` | Output as JSON instead of a tree |
| `--tree` | Explicit tree output (default) |
| `--help` | Show help and exit |

---

### Examples

**Basic dependency tree**
```bash
postwig the cat sat on the mat
```

**Verbose tree — includes morphology and lemma**
```bash
postwig she quickly ran to the store -v
```

**JSON output — useful for piping or scripting**
```bash
postwig the dog barked loudly -j
```

**JSON + verbose — full token metadata as structured data**
```bash
postwig i have been waiting -j -v
```

**Flags can be placed anywhere in the command**
```bash
postwig -v dogs are loyal companions
postwig dogs -j are loyal -v companions
```

**Pipe JSON into `jq` for further processing**
```bash
postwig the quick brown fox jumps -j | jq '.children[].text'
```

**Show help**
```bash
postwig --help
```
