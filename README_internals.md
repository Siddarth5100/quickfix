

### E2 - autoname & Renaming:
Part B

### Que:
Job Card's validate() to add a new check. If you
override_doctype_class and forget to update super() - what breaks?

### Ans:
* In Jod Card(Parent doctype) has some validate checks, if i forgot to update super() this will break the core things(validate in core Job Card doctype wil not run). Only it runs overide doctype validate.

### Que:
Explain in README_internals.md: why is doc_events safer than
override_doctype_class for most use cases?

### Ans:

### F1 - doc_events: Wildcard, Multiple Handlers, Order
Task B - Multiple handler conflict:

### Que:
Register TWO validate handlers on Job Card - one in your main controller and one in
doc_events. In README_internals.md: in what order do they run? What happens if
both raise a frappe.ValidationError?

### Ans:
when saving a Job Card documnet, the validate event is triggered.

Order:
1 controller validate() method inside JobCard class runs first
2 after controller validation completes, the hook hndler defined in hooks.py under doc_events executes

### controller validation runs before the doc_events hook validation


### Que:
what happens when you register "*" AND a specific DocType handler
for the same event? Do both run?

### Ans:
When both '*' and specific doctype handler are registered for the same event in hooks.py both handlers execute

Order:
1 Controller validate() method
2 Specific Doctype handler eg: Job Card
3 Wildcard handler (*)

therefore, both handlers run & specific Doctype handler executes before the wildcard handler