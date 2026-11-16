# Apply to a TTRP resident GitHub repository

This is an add-on for the existing persistent TTRP project repository, not a replacement for accepted work from DAB00 or earlier backlogs.

1. Start from the latest accepted project baseline in your own repository. Preserve `TTRP_GUIDE.md`, existing source files, decisions, earlier reflections, and Git history.
2. Add `src/supplier_receipt_summary.py`, `tests/test_supplier_receipt_summary.py`, `tests/fixtures/receipt_lines_sample.csv` and `requirements.txt` (merge dependencies with existing requirements rather than replacing them).
3. Add `docs/reflections/BL-P001-000002.md` in the official template format; update its actual submission date and describe your own verification.
4. Append the decision entries to the existing `docs/DECISIONS.md`, assigning the next available IDs instead of overwriting it.
5. Merge relevant sections of `README.md` into the existing README, preserving setup and usage instructions for accepted functionality.
6. Add the synthetic evidence files only if relevant; do not claim they validate the real source dataset.
7. Test using the accepted upstream CSV in the actual repository before committing. Review the changes, commit and push to the default branch required by the T21 board, then submit the public repository URL.

The ZIP intentionally contains no `TTRP_GUIDE.md`, no existing DAB00 source, no real supplier data, and no credentials; those must be preserved from the resident's own repository.
