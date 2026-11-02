# Test strategy

Armadillo baseline had no code/tests; no preexisting pass is claimed. Existing Tamandua Rust tests ran before real adapter checks.

Unit tests establish exact discrete expected values, fabricated/missing quotes, Unicode distinctions, schema/reference errors, hashes, escaping and immutability. CLI subprocess cases check workflows, errors and output preservation. Mock adapter tests cover failure protocols only.

Separate mandatory real suite invokes pinned Tamandua, verifies expected subclass membership and direct provenance, compares repeat output, parses Unicode/control literals, rejects malformed RDF and executes the full CLI. No engine skip is allowed.

No scientific numeric algorithm, units conversion or probabilistic model exists; scientific validation is NOT EXECUTED/not applicable. Expected discrete results use exact equality. No random seeds/tolerances apply.

Security tests cover malformed/duplicate JSON, invalid Unicode, traversal IDs, oversized/nonregular files, destination collisions and subprocess failures. No malicious-executable sandbox or vulnerability database scan is implied. CI defines standalone and explicit actual-engine jobs; local success does not establish hosted execution.
