#!/usr/bin/env python3
"""Validate all required TeachingScript syntax examples."""

import os
import sys

from antlr4 import CommonTokenStream, FileStream, InputStream
from antlr4.error.ErrorListener import ErrorListener


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATED_DIR = os.path.join(PROJECT_ROOT, "generated")
VALID_FILES = (
    "valid_01_basic_test.tscript",
    "valid_02_checkpoint.tscript",
    "valid_03_add_examples.tscript",
    "valid_04_rollback.tscript",
    "valid_05_complete_workflow.tscript",
)
INVALID_FILES = (
    "invalid_01_missing_brace.tscript",
    "invalid_02_missing_dataset_path.tscript",
    "invalid_03_missing_comma.tscript",
    "invalid_04_missing_arrow.tscript",
    "invalid_05_unquoted_checkpoint.tscript",
)

if not os.path.isdir(GENERATED_DIR):
    print(f"ERROR: Generated directory not found: {GENERATED_DIR}")
    print("Run generate_parser.ps1 first.")
    sys.exit(2)

sys.path.insert(0, GENERATED_DIR)
try:
    from TeachingScriptLexer import TeachingScriptLexer
    from TeachingScriptParser import TeachingScriptParser
except ImportError as exc:
    print("ERROR: Could not import generated lexer/parser.")
    print("Run generate_parser.ps1 first.")
    print(f"Details: {exc}")
    sys.exit(2)


class CollectingErrorListener(ErrorListener):
    """Capture lexer and parser errors for explicit pass/fail checks."""

    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offending_symbol, line, column, message, error):
        self.errors.append(f"line {line}:{column} {message}")


def parse_file(path):
    input_stream = FileStream(path, encoding="utf-8")

    lexer = TeachingScriptLexer(input_stream)
    lexer_errors = CollectingErrorListener()
    lexer.removeErrorListeners()
    lexer.addErrorListener(lexer_errors)

    token_stream = CommonTokenStream(lexer)
    parser = TeachingScriptParser(token_stream)
    parser_errors = CollectingErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(parser_errors)
    parser.program()

    return lexer_errors.errors, parser_errors.errors


def lex_errors(text):
    lexer = TeachingScriptLexer(InputStream(text))
    errors = CollectingErrorListener()
    lexer.removeErrorListeners()
    lexer.addErrorListener(errors)
    lexer.getAllTokens()
    return errors.errors


def files_in(directory):
    if not os.path.isdir(directory):
        return set()
    return {
        filename
        for filename in os.listdir(directory)
        if filename.endswith(".tscript")
    }


def main():
    examples_dir = os.path.join(PROJECT_ROOT, "examples")
    valid_dir = os.path.join(examples_dir, "valid")
    invalid_dir = os.path.join(examples_dir, "invalid")
    failures = []

    print("TeachingScript parser validation")
    print("-" * 64)

    for category, directory, expected_files, should_be_valid in (
        ("valid", valid_dir, VALID_FILES, True),
        ("invalid", invalid_dir, INVALID_FILES, False),
    ):
        expected_set = set(expected_files)
        actual_set = files_in(directory)
        for filename in sorted(actual_set - expected_set):
            print(f"FAIL  {filename} (unexpected {category} sample)")
            failures.append(filename)

        for filename in expected_files:
            path = os.path.join(directory, filename)
            if filename not in actual_set:
                print(f"FAIL  {filename} (required sample is missing)")
                failures.append(filename)
                continue

            lexer_errors, parser_errors = parse_file(path)
            errors = lexer_errors + parser_errors
            passed = not errors if should_be_valid else bool(errors)
            if passed:
                suffix = ""
                if not should_be_valid:
                    suffix = f" (rejected: {errors[0]})"
                print(f"PASS  {filename}{suffix}")
            else:
                reason = (
                    "unexpected lexer/parser error"
                    if should_be_valid
                    else "accepted, but should be rejected"
                )
                print(f"FAIL  {filename} ({reason})")
                for error in errors:
                    print(f"      {error}")
                failures.append(filename)

    for description, text in (
        ("unterminated_string", '"unfinished'),
        ("invalid_character", "@"),
    ):
        errors = lex_errors(text)
        if errors:
            print(f"PASS  lexer_{description} (reported lexical error)")
        else:
            print(f"FAIL  lexer_{description} (no lexical error reported)")
            failures.append(f"lexer_{description}")

    print("-" * 64)
    if failures:
        print(f"RESULT: FAIL - {len(failures)} problem(s).")
        return 1

    print("RESULT: PASS - all five valid samples parsed and all five invalid samples rejected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
