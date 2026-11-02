# Tamandua integration

Use the [tested tutorial](../TAMANDUA_TUTORIAL.md). Enable explicitly with --tamandua PATH. No API key, environment file, HTTP server, database, frontend or source modification needed.

Armadillo exports declared claims/evidence/links and SourcePresentNode labels. Tamandua returns RDFS closure and direct derivations. Declared links remain assertions even when quotes are missing; source-presence labels distinguish findings. Reasoning never changes source-audit status or proves semantic support.

Synthetic example: nine asserted triples, two inferred ArgumentNode memberships. Missing executable, timeout, incompatible version/schema, invalid RDF/JSON and invalid provenance are errors, not silent fallbacks. Omit the flag to run standalone. See [contract](INTERFACE_CONTRACT.md).
