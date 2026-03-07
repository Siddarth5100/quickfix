

E2 - autoname & Renaming:
Part B

Que:
Job Card's validate() to add a new check. If you
override_doctype_class and forget to update super() - what breaks?

Ans:
* In Jod Card(Parent doctype) has some validate checks, if i forgot to update super() this will break the core things(validate in core Job Card doctype wil not run). Only it runs overide doctype validate.

Que:
Explain in README_internals.md: why is doc_events safer than
override_doctype_class for most use cases?

Ans:

