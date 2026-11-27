# Evidence reporting safeguard

The structured claim checker rejects unsupported claims about committed files, merged pull requests, successful workflow executions and numeric measurements. It checks matching revisions, completed successful workflow status, inspection of outputs, metric values and units. It returns warnings alongside its decision. The CLI exits nonzero for rejected claims.

Run `python3 -m unittest discover -s validation -p 'test_report_gate.py' -v`. These tests intentionally exercise truthful and false claims using synthetic records. Run the existing repository validation workflow to execute them alongside catalog checks.

## Limitations
This checker is not connected to ChatGPT's response generation or the scheduled research task. It does not independently retrieve GitHub records, authenticate supplied evidence, parse natural-language reports, verify scientific claims, or guarantee that warnings appear in a human-written summary. The caller must obtain evidence independently and pass it to the checker; fabricated input can defeat it. Passing tests establishes behavior of the checker on the specified fixtures only, not reliable AI compliance. Future integration requires an authoritative read-only evidence collector, a report-generation path that cannot bypass the checker, and separate evaluation of actual AI outputs.

No changes to the founding charter, scientific acceptance criteria or owner permissions.
