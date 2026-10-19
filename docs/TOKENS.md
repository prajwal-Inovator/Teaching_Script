# TeachingScript token reference

This document describes the lexical tokens defined in `TeachingScriptLexer.g4`
and consumed by `TeachingScriptParser.g4`. Token names match the ANTLR
generated Python lexer (`generated/TeachingScriptLexer.py`).

The parser grammar expects a single `program` rule: one `lesson` followed by
`EOF`. There is **no** separate identifier token — names, paths, and labels
are always double-quoted `STRING` literals.

## Summary table

| Token | Pattern / lexeme | Category | Purpose | Parser use |
|-------|------------------|----------|---------|------------|
| `LESSON` | `lesson` | Keyword | Starts a workflow block | `lesson` rule |
| `DATASET` | `dataset` | Keyword | Dataset path command | `datasetStmt` |
| `ADD_EXAMPLES` | `add_examples` | Keyword | Opens labelled-example block | `addExamplesStmt` |
| `TEST` | `test` | Keyword | Request evaluation | `testStmt` |
| `CHECKPOINT` | `checkpoint` | Keyword | Save model state | `checkpointStmt` |
| `ROLLBACK` | `rollback` | Keyword | Restore saved state | `rollbackStmt` |
| `LBRACE` | `{` | Punctuation | Opens lesson or `add_examples` block | Blocks |
| `RBRACE` | `}` | Punctuation | Closes a block | Blocks |
| `LBRACKET` | `[` | Punctuation | Opens a feature vector | `featureVector` |
| `RBRACKET` | `]` | Punctuation | Closes a feature vector | `featureVector` |
| `COMMA` | `,` | Punctuation | Separates numbers in a vector | `featureVector` |
| `ARROW` | `->` | Operator | Separates features from label | `example` |
| `STRING` | `"..."` | Literal | Lesson name, path, checkpoint name, class label | Many rules |
| `NUMBER` | digits, optional fraction | Literal | Feature values in vectors | `featureVector` |
| `WS` | space, tab, CR, LF | Ignored | Separates tokens | Skipped (`-> skip`) |
| `LINE_COMMENT` | `#` … end of line | Ignored | End-of-line comments | Skipped (`-> skip`) |

`EOF` is an ANTLR parser sentinel; the lexer does not emit an `EOF` token type
in the vocabulary table used by applications.

## Keywords

All keywords are **lowercase ASCII** and **case-sensitive**:

- `lesson`, `dataset`, `add_examples`, `test`, `checkpoint`, `rollback`

Writing `Lesson` or `DATASET` produces a lexer error (no matching rule).

## Punctuation and `ARROW`

- Braces delimit the lesson body and the body of `add_examples`.
- Square brackets delimit comma-separated numeric feature lists.
- `ARROW` is the two-character sequence `->` (no spaces inside the token).
  Example: `[5.1, 3.5, 1.4, 0.2] -> "setosa"`.

## `STRING` literals

Lexer rule:

```antlr
STRING : '"' (~["\\\r\n] | '\\' .)* '"';
```

- Opening and closing double quotes are required.
- Backslash starts an escape; the next character is consumed literally by the
  lexer (the interpreter additionally interprets `\"`, `\\`, `\n`, and `\t` when
  unquoting).
- Raw line breaks inside a string are **not** allowed.
- An unterminated string (missing closing `"`) is a **lexer error**.

Examples:

| Source | Result |
|--------|--------|
| `"iris_workflow"` | Valid lesson name |
| `"data/iris.csv"` | Valid dataset path |
| `"setosa"` | Valid class label |
| `checkpoint baseline` | Parser error (unquoted text is not a `STRING`) |

## `NUMBER` literals

Lexer rule:

```antlr
NUMBER : [0-9]+ ('.' [0-9]+)?;
```

- Non-negative integers or decimals (e.g. `5`, `3.5`, `0.2`).
- **No** sign prefix, exponent, or hex — `-1` would lex as `-` (illegal) or fail.
- Used only inside `[` … `]` feature vectors.

## Whitespace and comments

| Rule | Behaviour |
|------|-----------|
| `WS` | Spaces, tabs, carriage return, newline → skipped, not passed to parser |
| `LINE_COMMENT` | `#` through end of line → skipped |

Comments may appear between any two tokens. Example:

```text
lesson "demo" {  # load data
    dataset "data/iris.csv"
    test  # evaluate
}
```

## Lexical vs parser errors

| Situation | Reported by | Example |
|-----------|-------------|---------|
| Character not matched by any lexer rule | Lexer | `@` |
| Unterminated string | Lexer | `"unfinished` |
| Valid tokens in wrong order or missing token | Parser | `dataset` without following `STRING` |
| Missing `}` before end of file | Parser | Truncated lesson body |
| Wrong feature syntax | Parser | `[1, 2]` without `->` label |

Errors are collected by `interpreter.parser_utils.CollectingErrorListener` and
surfaced as `ParseError` in the CLI and Streamlit UI.

## Case sensitivity

- Keywords: lowercase only.
- String contents: case-sensitive (`"setosa"` ≠ `"Setosa"` for labels — must
  match dataset class names after load).

## Relationship to commands

| Command | Typical token sequence |
|---------|------------------------|
| Lesson | `LESSON STRING LBRACE` … `RBRACE` |
| Dataset | `DATASET STRING` |
| Test | `TEST` |
| Checkpoint | `CHECKPOINT STRING` |
| Rollback | `ROLLBACK STRING` |
| Add examples | `ADD_EXAMPLES LBRACE` (`featureVector ARROW STRING`)* `RBRACE` |

Feature vector: `LBRACKET NUMBER (COMMA NUMBER)* RBRACKET`.
