# TeachingScript — final verification matrix

**Repository state:** post-upgrade (UI redesign, documentation, cleanup)  
**Verifier environment:** Windows 10, Python 3.10.11, `.venv` at `F:\TeachAIx`

Statuses: **PASS** | **FAIL** | **PARTIAL** | **NOT VERIFIED** | **BLOCKED BY ENVIRONMENT**

| ID | Feature | Relevant file(s) | Verification command or procedure | Observed status | Evidence / notes |
|----|---------|------------------|-----------------------------------|-----------------|------------------|
| E1 | Python dependencies import | `requirements.txt` | `python -m pytest -q` (collect + run) | PASS | 36 tests collected, 0 import errors |
| E2 | ANTLR runtime version match | `requirements.txt`, `generate_parser.ps1` | Inspect pins + JAR name | PASS | `antlr4-python3-runtime==4.13.2`, JAR `antlr-4.13.2-complete.jar` |
| G1 | ANTLR grammar generation | `generate_parser.ps1`, `*.g4` | `.\generate_parser.ps1` | PASS | Regenerated lexer/parser/visitor under `generated/` |
| G2 | Generated parser committed | `generated/TeachingScript*.py` | File presence + pytest parser tests | PASS | `test_parser_smoke.py` passed |
| L1 | Lexer token recognition | `TeachingScriptLexer.g4`, `parser_utils.lex` | `pytest tests/test_parser_smoke.py::test_tokens_recognised` | PASS | pytest PASS |
| L2 | Lexer error on `@` | `tests/test_parser.py` | `python tests/test_parser.py` | PASS | `lexer_invalid_character` PASS |
| P1 | Parser valid programs | `TeachingScriptParser.g4` | `python tests/test_parser.py` | PASS | 5/5 `.tscript` valid PASS |
| P2 | Parser rejects invalid | `examples/invalid/*.tscript` | `python tests/test_parser.py` | PASS | 5/5 invalid rejected |
| P3 | Parser smoke on `.ts` examples | `examples/valid/*.ts` | `pytest tests/test_parser_smoke.py` | PASS | All `.ts` parse clean |
| X1 | Five valid `.ts` runtime examples | `examples/valid/*.ts` | `pytest tests/test_interpreter.py::test_all_valid_examples_execute` | PASS | pytest PASS |
| X2 | Five invalid `.ts` examples | `examples/invalid/*.ts` | `pytest tests/test_interpreter.py::test_all_invalid_examples_raise` | PASS | pytest PASS |
| S1 | Syntax error reporting | `parser_utils.py`, `main.py` | `pytest test_syntax_error_raises_parse_error` | PASS | ParseError with line info |
| I1 | Interpreter full workflow | `interpreter/visitor.py` | `pytest test_full_workflow_from_example_file` | PASS | 3 tests, checkpoint, rollback |
| D1 | Dataset loading (Iris) | `ml/dataset.py`, `data/iris.csv` | `pytest tests/test_ml.py::test_iris_shape_and_split` | PASS | 120/30 split, 4 features |
| M1 | Model training | `ml/model.py` | `pytest tests/test_ml.py::test_train_and_evaluate` | PASS | accuracy ≥ 0.8 on Iris |
| M2 | add_examples | `ml/model.py`, visitor | `pytest test_add_examples_retrains_without_touching_test` | PASS | train rows +2, test=30 |
| M3 | Accuracy calculation | `ml/evaluation.py` | CLI run | PASS | `main.py` printed `accuracy = 0.9333 (28/30)` |
| M4 | Confusion matrix | `ml/evaluation.py`, `main.py` | CLI run | PASS | 3×3 matrix printed |
| M5 | Fixed test set | `ml/dataset.py` | `pytest test_dataset_split_is_fixed` | PASS | n_samples=30 both tests |
| C1 | Checkpoint save (memory) | `visitor.py`, `model.py` | `pytest test_full_workflow_from_example_file` | PASS | log contains checkpoint |
| C2 | Rollback restoration | `visitor.py` | `pytest test_rollback_in_memory_matches_baseline` | PASS | first/last accuracy equal |
| C3 | Disk checkpoint store | `checkpoint/store.py` | `pytest tests/test_checkpoint.py` | PASS | 6/6 checkpoint tests PASS |
| CLI1 | Full CLI workflow | `main.py` | `python main.py examples\valid\01_iris_full.ts` | PASS | exit 0, 3 tests executed |
| UI1 | Streamlit startup | `app.py` | `streamlit run app.py --server.headless true --server.port 8765` + HTTP GET | PASS | HTTP 200 on localhost:8765 |
| UI2 | UI compiles / backend wiring | `app.py`, `ui/execution.py` | `pytest tests/test_ui_smoke.py` | PASS | 3/3 smoke tests |
| UI3 | UI execution helper | `ui/execution.py` | `execute_source` on `02_minimal.ts` | PASS | session returned, 7 stages |
| UI4 | Interactive Run button in browser | `app.py` | Manual click **Run program** | NOT VERIFIED | Automated HTTP probe only; no browser automation |
| UI5 | Frontend responsive layout | `ui/theme.py`, `app.py` | Resize browser during demo | NOT VERIFIED | CSS reviewed statically |
| UI6 | UI error display for invalid script | `app.py` | Load invalid example + Run in browser | NOT VERIFIED | Logic present; browser not automated |
| R1 | README completeness | `README.md` | Manual review vs code | PASS | Replaced; matches structure/commands |
| R2 | Token doc accuracy | `docs/TOKENS.md` | Compare to `TeachingScriptLexer.g4` | PASS | No fictitious ID/negative NUMBER rules |
| R3 | Demo script | `docs/DEMO.md` | Manual review | PASS | Timeline + viva bank included |
| T1 | Automated test suite | `tests/` | `python -m pytest -v` | PASS | **36 passed** in ~30–38s |
| CL1 | Remove `.antlr/` Java artifacts | `.gitignore` | Delete folder + ignore rule | PASS | Folder removed; `.antlr/` in gitignore |
| CL2 | Duplicate example extensions | `examples/*/*.ts`, `*.tscript` | Inspect tests | PASS | Both retained; different test entry points |
| CL3 | Rerun tests after cleanup | `tests/` | `python -m pytest -q` | PASS | 36 passed after cleanup |

## Items marked NOT VERIFIED (action for presenter)

- **G1:** Run `.\generate_parser.ps1` once before submission if grammars changed.
- **UI4–UI6:** Open Streamlit locally and click through Workspace / Examples / Run / invalid script before viva.

## Commands log (executed during verification)

```powershell
Set-Location F:\TeachAIx
.\.venv\Scripts\python.exe -m pytest -v          # 36 passed
.\.venv\Scripts\python.exe main.py examples\valid\01_iris_full.ts
.\.venv\Scripts\python.exe tests\test_parser.py  # RESULT: PASS
.\.venv\Scripts\python.exe -c "from ui.execution import execute_source; ..."
streamlit run app.py --server.headless true --server.port 8765  # HTTP 200
```
