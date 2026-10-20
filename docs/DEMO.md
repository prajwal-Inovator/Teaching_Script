# TeachingScript — live demonstration script (≈4–5 minutes)

## Demo title

**TeachingScript: ANTLR DSL for ML training, evaluation, and rollback**

## Objective

Show that TeachingScript is a real compiled-style pipeline (lexer → parser →
visitor), not a UI mock, and that programs drive genuine scikit-learn training
and evaluation on Iris data.

## Prerequisites and pre-demo checks

1. Project root: `F:\TeachAIx` (adjust if cloned elsewhere).
2. Virtual environment with dependencies installed (`pip install -r requirements.txt`).
3. `data/iris.csv` present.
4. Optional: `antlr-4.13.2-complete.jar` if you plan to regenerate the parser live.

```powershell
Set-Location F:\TeachAIx
.\.venv\Scripts\Activate.ps1
python -m pytest -q
python main.py examples\valid\01_iris_full.ts
```

If CLI runs successfully, the UI will use the same interpreter stack.

## Fallback plan

- **UI will not start:** Demo from CLI with `main.py` and show `tests/test_parser.py` output for syntax validation.
- **Dataset missing:** Run `python scripts\make_iris.py` if available, or copy a standard Iris CSV into `data/iris.csv`.
- **Java missing:** Skip live parser regeneration; use committed `generated/` files.

---

## Timeline

### 0:00–0:30 — Problem and project intro

**Say:** “Machine learning scripts repeat the same steps. TeachingScript is a
small language with six commands. ANTLR builds the lexer and parser; a Python
visitor executes commands against scikit-learn.”

**Show:** README architecture diagram or project folder (`TeachingScriptLexer.g4`,
`interpreter/visitor.py`, `generated/`).

---

### 0:30–1:15 — Streamlit workspace

**Do:**

```powershell
streamlit run app.py
```

**Say:** “The UI is a developer-style workspace: editor, execution pipeline, and
evaluation panels. Nothing runs until I click Run program.”

**Click:** **Workspace** in the sidebar (default).

**Point out:** Header status, version, dark theme, editor with default Iris workflow.

---

### 1:15–2:00 — Valid program and parsing

**Do:** Click **Run program** with the default script (or **Load example** →
`01_iris_full.ts` → **Load into editor** → **Run program**).

**Say:** “Stages show lexing, parsing, and interpreter execution. If syntax fails,
parsing never reports success — errors list line and column from ANTLR.”

**Expected:** Green completion message; pipeline stages through dataset, evaluation,
checkpoint, add_examples, rollback; accuracy values **as computed** (typically high
on Iris with the default tree; exact numbers depend on split and examples).

**Optional CLI mirror:**

```powershell
python main.py examples\valid\01_iris_full.ts
```

---

### 2:00–3:00 — Evaluation and add_examples

**Do:** Open **Evaluation** tab — show test metrics and confusion matrix heatmap.

**Say:** “Each `test` command evaluates on the same held-out 30-row test split
created at `dataset` time. `add_examples` only changes training rows and retrains;
the test set stays fixed.”

**Point out:** Multiple test metrics if the script ran more than one `test`.

---

### 3:00–3:40 — Checkpoint and rollback

**Do:** Open **Checkpoints** tab — saved `baseline` and restored state.

**Say:** “Checkpoint serialises training state and the fitted tree. Rollback
restores it; the last `test` should match the first when we rolled back to
baseline — the UI caption mentions this when accuracies match.”

**Optional:** Enable **Persist checkpoints to ./checkpoints_ui**, run again, show
files created under `checkpoints_ui/` (sanitised names).

---

### 3:40–4:20 — Invalid script

**Do:** Sidebar → **Examples** → select an invalid sample → **Try in workspace**
→ **Run program**.

**Say:** “Invalid programs are rejected by the lexer or parser with actionable
messages — for example missing `->`, unquoted checkpoint names, or missing `}`.”

**Expected:** Syntax error table; pipeline shows Lexing or Parsing as **fail**;
no evaluation tab with fresh success metrics from this run.

---

### 4:20–5:00 — Architecture summary

**Say:**

- **ANTLR** defines tokens and grammar; `generate_parser.ps1` produces Python code.
- **parser_utils** is the only module that imports generated parsers.
- **Interpreter** visitor maps AST nodes to ML operations.
- **Academic focus:** language + interpreter; ML is the demonstration target.

**Show:** `TeachingScriptParser.g4` `lesson` rule and one visitor method in
`interpreter/visitor.py`.

---

## Viva question bank (20+)

1. **What is TeachingScript?**  
   A DSL with six commands for ML load/train/test/checkpoint workflows, parsed by ANTLR and executed by a Python visitor.

2. **Why create a DSL?**  
   To separate workflow intent from implementation and to demonstrate compiler construction (lex/parse/interpret).

3. **What is ANTLR?**  
   A parser generator that produces lexers/parsers from `.g4` grammars.

4. **Lexer vs parser?**  
   Lexer tokenises text; parser checks token sequences against grammar rules and builds a parse tree.

5. **What is a token?**  
   A classified lexeme (e.g. `LESSON`, `STRING`, `ARROW`) emitted by the lexer.

6. **What is a grammar?**  
   Formal rules describing valid programs (`TeachingScriptParser.g4`).

7. **What is a parse tree?**  
   A tree structure representing how the parser matched the grammar (e.g. `lesson` → `statement` nodes).

8. **What is an interpreter here?**  
   The `Interpreter` visitor that walks the tree and performs side effects (load data, train, test).

9. **Role of the visitor?**  
   Encapsulates execution logic per grammar rule (`visitDatasetStmt`, etc.).

10. **Why separate grammar from ML logic?**  
    Keeps the language layer independent; ML modules can change without altering token rules.

11. **Why Python?**  
    Rapid integration with scikit-learn/pandas and ANTLR’s Python target.

12. **Why scikit-learn?**  
    Standard, reproducible ML primitives suitable for a college demo.

13. **What is a train/test split?**  
    Data divided so training fits parameters and testing estimates generalisation.

14. **Why keep the test set fixed?**  
    So accuracy changes reflect model/training updates, not a new random split.

15. **What does accuracy measure?**  
    Fraction of test predictions matching true labels.

16. **What is a confusion matrix?**  
    Table of true vs predicted class counts per label.

17. **Why might accuracy not improve after add_examples?**  
    New points may not change tree splits; tree may already fit; examples may duplicate regions.

18. **What is a checkpoint?**  
    A serialised snapshot of training arrays and the fitted classifier.

19. **How does rollback work?**  
    Loads a named snapshot back into the session model (`Model.from_snapshot`).

20. **How are syntax errors handled?**  
    ANTLR error listeners collect messages; CLI/UI raise or display `ParseError` details.

21. **How does the UI connect to the interpreter?**  
    `ui/execution.py` calls `lex`, `parse`, then `Interpreter.visitProgram` — same core as `run_source`.

22. **Current limitations?**  
    One lesson, one dataset, CSV contract, single tree model, local pickle checkpoints.

23. **Main academic contribution?**  
    Custom TeachingScript grammar, ANTLR-generated parser, and visitor-based interpreter executing real workflows.

24. **What file extension do examples use?**  
    `.ts` for runtime examples; `.tscript` duplicates used by the standalone parser test script.

25. **Are UI metrics hardcoded?**  
    No — they come from `evaluate()` on the live model after each `test` command.
