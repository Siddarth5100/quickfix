
### Part D - DocStatus transitions

### Que:
What are the three numeric values of docstatus and what state does each represent?

### Ans:
The three numeric values are 0,1,2
0 = draft
1 = submitted
2 = cancelled
----------------------------------------------------------------------------------
### Que:
Can you call doc.save() on a submitted document? What about doc.submit() on a
cancelled one? Test in bench console and explain why.

### Ans:
doc.save() will not work on a submitted document, it will raise UpdateAfterSubmitError: Not allowed to change ..,
Reason to prevent overwriting, we can do in special cases
(doc.save = ignore_permissions= True, ignore_version= True)

### Eg: 
UpdateAfterSubmitError:  Not allowed to change Customer Name after submission from bala to Sid

doc.submit() not work on cancelled one, it will raise validationError, unless amend

### Eg:
ValidationError: Cannot edit cancelled document
----------------------------------------------------------------------------------
### Que:
Why would you see a "Document has been modified after you have opened it" error and how does Frappe prevent concurrent overwrites?

### Ans:

----------------------------------------------------------------------------------
### Part E - Dangerous patterns

### Que:
The following snippet has TWO bugs related to document lifecycle. Identify both and write the corrected version:

### bug task: 
def validate(self):
self.total = sum(r.amount for r in self.items)
self.save()
other = frappe.get_doc("Spare Part", self.part)
other.stock_qty -= self.qty
other.save()

Lifecycle eg: 
User clicks save -> doc.save() -> before_validate() -> validate -> before_save -> db update -> after_save

doc.submit() -> before_submit -> validate -> before_save -> db_update -> on_submit

### code - bug 1
self.parts_total = sum(r.total_price for r in self.parts_used)
	print("------------------Test print for bug fixing")
	self.save()

### output: RecursionError: maximum recursion depth exceeded
validate() runs whenever the document is saved or submitted

here user will add values in UI and click save that will trigger
doc.save()
checks line 1 and when comes to 2nd line save will call again
doc.save() this triggers validate again it is like loop hole
finally after a break point will get the recursion error

### code - bug 2
for part in self.parts_used:
	other = frappe.get_doc("Spare Part", part.part)
	print("1---------bug fix: other", other)
	other.stock_qty -= part.quantity
	other.save()

### output: this will gets save but from inside the validate()
validate() should only do validate, calculations, raise error
here in validate() we are fetching another documnent and it is trigerring doc.save() to save the record

### code leve

def validate(self):
    self.total = sum(r.amount for r in self.items)

def on_submit(self):
	for part in self.parts_used:
	    other = frappe.get_doc("Spare Part", part.part)
    	other.stock_qty -= part.qty
    	other.save()
----------------------------------------------------------------------------------
### Child Table Internals

### Que:
When you append a row to Job Card.parts_used and save, what 4 columns does Frappe automatically set on the child table row?

### Ans:
parent, parenttype, parentfield, idx are the four columns

parent => name of the parent dooctype(ID) eg: JC-2026-00004
parenttype => parent doctype eg: Job Card
parent_field =>  fieldname of the child table eg: parts_used
idx => row order inside the table

### Que:
What is the DB table name for the Part Usage Entry DocType?

### Ans:
`tabPart Usage Entry`

### Que:
If you delete row at idx=2 and re-save, what happens to idx values of remaining rows?

### Ans:
last index +1
delete row frappe reoders idx
add row frappe assigns next idx

idx => index number of the row
it is the index of the child table doctype, where maintains the row order, inside the parent document

assume we have idx = 1, 2, 3 
if we delete row at idx= 2 no this gets reassigned 1 will be there 3 becomes = 2, if we re-add, it will add 2+1 = 3
----------------------------------------------------------------------------------
### Renaming task

### Que:
Rename one of your test Technician records using the Rename Document feature.
Then check: does the assigned_technician field on linked Job Cards automatically update? Why or why not? What does "track changes" mean in this context?

### Ans:
Using the Rename option it is getting changed in both the places

Track changes here it is creating a log below so that we can see that what happens, changes in the particular document

### Eg: 
Administrator renamed from TECH-0005 to TECH-005 · 1 minute ago

### Que:
Explain unique constraints: what is the difference between setting a field as "unique" in the DocType vs doing a frappe.db.exists() check in validate()?

### Ans:
If we are keeping unque using the Doctype(UI) it will validate automatically, weather any ducplicates is getting added in the UI itself, if True it will block there itself and throw proper error in UI(frontend level validation). 

In validate() will use frappe.db.exists() to check any value exist or not in the database (db level validation)
----------------------------------------------------------------------------------
### D1 - Roles, Permission Matrix, Document Sharing

### Que:
In bench console: call frappe.get_doc_permissions(doc) on a Job Card while logged in as different users. Document what the return dict looks like.

### Ans:
from frappe.permissions import get_doc_permissions

doc= frappe.get_doc("Job Card", "JC-2026-00004")
get_doc_permissions(doc, user= "shamir@gmail.com")

ouput:
{'if_owner': {},
 'has_if_owner_enabled': False,
 'select': 0,
 'read': 0,
 'write': 0,
 'create': 0,
 'delete': 0,
 'submit': 0,
 'cancel': 0,
 'amend': 0,
 'print': 0,
 'email': 0,
 'report': 0,
 'import': 0,
 'export': 0,
 'share': 0}
----------------------------------------------------------------------------------
### E2 - autoname & Renaming:
Part B

### Que:
Job Card's validate() to add a new check. If you
override_doctype_class and forget to update super() - what breaks?

### Ans:
In Jod Card(Parent doctype) has some validate checks, if i forgot to update super() this will break the core things(validate in core Job Card doctype wil not run). Only it runs overide doctype validate.

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
----------------------------------------------------------------------------------
### F3 - Asset, Jinja & Website Hooks

### Que:
What is the difference? When would you use each?

### Ans:
app_inclue_js: is the file for logged in desk-user (Desk user)
web_include_js: id for the website/portal pages (Frontend user)

### Que:
doctype_tree_js: not applicable here - explain in README what DocType would use a tree view and why

### Ans:
Tree view is only useful for nested/ hierarchical data, where parent child relationship exist

## Eg: 
Project Task with parent task and sub task
----------------------------------------------------------------------------------
### K1 - Background Jobs

### Que:
Explain the 3 queue names (default, long, short) and when
to use each

### Ans:
Frappe uses redis queue(RQ) to process bg job asynchronously
There are three different types of background jobs default, long, short

Short queue: 300
used for quick task, that will execute immediately, this should not wait behind the long queue

### Eg:
Sending confirmation mail, notifications etc

Default queue: 300
Used for medium duration tasks, can take few seconds/minutes

### Eg:
Generating small reports, data processing

Long queue: 1500
Time consuming tasks

### Eg:
Payroll processing to employees, large report generation which works in n number of records
----------------------------------------------------------------------------------
L1 - REST Resource API & Custom API

### Task A - Resource API (test with curl or Postman):

### Que:
GET /api/resource/Job Card - list Job Cards (use session cookie from browser)

### Ans:
* Open postman add request method & type URL
* Headers we want to pass session cookie from browser
(to copy cookie value: open browser f12(console), select storage, cookies, name and value will be there)

method: GET
url: http://quickfix-dev.localhost:8003/api/resource/Job%20Card
headers: 
	Key= Cookie 
	Value= sid=9393ac49c8442f7f3d57b90b7b6bea65fb08e0d9bbba30fbf746632e
body: raw JSON

request= http://quickfix-dev.localhost:8003/api/resource/Job%20Card
response= 
{
    "data": [
        {
            "name": "JC-2026-00004"
        },
        {
            "name": "JC-2026-00005"
        },
        {
            "name": "JC-2026-00012"
        },
        {
            "name": "JC-2026-00012-1"
        }
    ]
}

### Que:
GET /api/resource/Job Card/JC-0001 - single doc

### Ans:
method: GET
url: http://quickfix-dev.localhost:8003/api/resource/Job%20Card/JC-2026-00029
header: already enabled

request= http://quickfix-dev.localhost:8003/api/resource/Job%20Card/JC-2026-00029
response=
{
    "data": {
        "name": "JC-2026-00029",
        "owner": "Administrator",
        "creation": "2026-03-18 11:04:15.077628",
        "modified": "2026-03-18 11:57:47.578793",
        "modified_by": "Administrator",
        "docstatus": 2,
        "idx": 0,
        "customer_name": "Sid",
        "customer_phone": "8898",
        "customer_email": "siddarthsiddhu5100@gmail.com",
        "device_type": "Laptop",
        "device_brand": "Dell",
        "device_model": "5410",
        "imei_or_serial": "12n132eo",
        "problem_description": "<div class=\"ql-editor read-mode\"><p>Laptop issue</p></div>",
        "assigned_technician": "TECH-0004",
        "estimated_cost": 0.0,
        "priority": "Urgent",
        "parts_total": 7000.0,
        "labour_charge": 1000.0,
        "final_amount": 8000.0,
        "payment_status": "Unpaid",
        "delivery_date": "2026-03-18",
        "remarks": "NA",
        "status": "Ready For Delivery",
        "doctype": "Job Card",
        "parts_used": [
            {
                "name": "fb8mnvf250",
                "owner": "Administrator",
                "creation": "2026-03-18 11:04:15.077628",
                "modified": "2026-03-18 11:57:47.578793",
                "modified_by": "Administrator",
                "docstatus": 2,
                "idx": 1,
                "part": "SP-01",
                "part_name": "Dell Mother Board",
                "unit_price": 7000.0,
                "quantity": 1.0,
                "total_price": 7000.0,
                "parent": "JC-2026-00029",
                "parentfield": "parts_used",
                "parenttype": "Job Card",
                "doctype": "Part Usage Entry"
            }
        ]
    }
}

### Que:
POST /api/resource/Spare Part - create a part

### Ans:
method: POST
url: http://quickfix-dev.localhost:8003/api/resource/Spare%20Part
headers:
cookie + value &
key : X-Frappe-CSRF-Token
value: e58f704cb883f3299444cdd47ad97fe39019c556dd0417d7b18818d6

body: (raw + json)
{
"part_name": "Battery",
"part_code": "P010",
"compatible_device_type": "Laptop",
"unit_cost": 1500,
"selling_price": 1800,
"stock_qty": 50,
"reorder_level": 10
}

### Que:
PUT /api/resource/Spare Part/PART-0001 - update a field

### Ans:
method: PUT
url: http://quickfix-dev.localhost:8003/api/resource/Spare%20Part/PART-2026-0002
headers:
key + Value
Cookie + sid=9393ac49c8442f7f3d57b90b7b6bea65fb08e0d9bbba30fbf746632e
X-Frappe-CSRF-Token + e58f704cb883f3299444cdd47ad97fe39019c556dd0417d7b18818d6

request: http://quickfix-dev.localhost:8003/api/resource/Spare%20Part/PART-2026-0002
body: raw + json
{
    "stock_qty": 45
}

response:
{
    "data": {
        "name": "PART-2026-0002",
        "owner": "Administrator",
        "creation": "2026-02-26 14:25:57.668167",
        "modified": "2026-03-18 19:17:27.538017",
        "modified_by": "Administrator",
        "docstatus": 0,
        "idx": 10,
        "part_name": "Mother Board",
        "part_code": "002",
        "compatible_device_type": "Laptop",
        "unit_cost": 20000.0,
        "selling_price": 25000.0,
        "stock_qty": 45.0,
        "reorder_level": 5.0,
        "is_active": 1,
        "doctype": "Spare Part"
    }
}

### Que:
DELETE /api/resource/Spare Part/PART-0001 - delete it

### Ans:
method: DELETE
url: http://quickfix-dev.localhost:8003/api/resource/Spare%20Part/SP-0006

header: key + value
Cookie + sid=9393ac49c8442f7f3d57b90b7b6bea65fb08e0d9bbba30fbf746632e
x-Frappe-CSRF-Token + e58f704cb883f3299444cdd47ad97fe39019c556dd0417d7b18818d6

request: http://quickfix-dev.localhost:8003/api/resource/Spare%20Part/SP-0006

response:
{
    "data": "ok"
}

### Que:
what is the difference between session cookie auth and token
auth? Which is appropriate for browser use and which for server-to-server?

### Ans:

Session cookie auth:
* session user will run till the user session is active
* this will get changed once the session got expired
* goto browser click fn + f12 => storage => cookies => url => username(eg:sid) copy the value too
* fronend browser request

token auth:
* token based will run until we delete it
* this will gets changed only when we generate new one
* this we can take from the user exist in the record
goto user => settings => api access => generate keys
* api key will remain same where the secret gets changed 
when we click generate keys
* server to server communication