# Task — Tests, code review, and fixes

> **Status:** close reconstruction (a sequence of Claude Code tasks and manual fixes).

**Unit tests:** Claude Code wrote `test_calculator.py` — **32 tests** covering the gamification calculator (`get_user_level`, `get_xp_for_next_level`, `add_xp` including subscription multipliers and level-up detection, and the progress-percentage formula). All 32 passed.

**Code review:** Claude Code reviewed the changed areas and found 9 issues across priorities. The high-priority fixes:
- validation errors now return **HTTP 400** instead of a misleading 200
- `db.session.commit()` is wrapped in **try/except** with a rollback, so a database error can't crash the signup route

**Done by hand:** when Claude Code ran out of credits, I made the two high-priority fixes **manually** in the editor and understood exactly what each did — which felt like a turning point in actually learning the code, not just accepting it.
