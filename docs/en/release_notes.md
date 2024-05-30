# <center>Release notes</center> #

---
## v0.10.2 - 2024-05-23
## What's Changed

**Fix**

* 🐛 Fix class QueryOperators types tuples by <a href="https://github.com/mauro-andre/pyodmongo/pull/132" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.10.1...0.10.2

---
## v0.10.1 - 2024-05-23
## What's Changed

**Fix**

* 🐛 Verify in _union_collector_info if any model has model field by <a href="https://github.com/mauro-andre/pyodmongo/pull/131" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.10.0...0.10.1

---
## v0.10.0 - 2024-05-23
## What's Changed

**New Features**

* ✨ MainBaseModel by <a href="https://github.com/mauro-andre/pyodmongo/pull/129" target="_blank">@mauro-andre</a>

* ✨ elem_match query operator by <a href="https://github.com/mauro-andre/pyodmongo/pull/130" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.9.2...0.10.0

---
## v0.9.2 - 2024-05-15
## What's Changed

**Fix**

* 🐛 Fix DbModel init not set None in empty list by <a href="https://github.com/mauro-andre/pyodmongo/pull/128" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.9.1...0.9.2

---
## v0.9.1 - 2024-05-15
## What's Changed



**Fix**

* 🐛 Fix remove empty dict in DbModel init by <a href="https://github.com/mauro-andre/pyodmongo/pull/127" target="_blank">@mauro-andre</a>



**Doc**

* 📝 Release notes by <a href="https://github.com/mauro-andre/pyodmongo/pull/126" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.9.0...0.9.1

---
## v0.9.0 - 2024-04-24
## What's Changed

**New release** 

* ✨ `tz_info` in engine and find_one and find_many by <a href="https://github.com/mauro-andre/pyodmongo/pull/124" target="_blank">@mauro-andre</a>



**Fix**

* ➕ Added pytz in yml by <a href="https://github.com/mauro-andre/pyodmongo/pull/125" target="_blank">@mauro-andre</a>



**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.8.0...0.9.0

---
## v0.8.0 - 2024-04-23
## What's Changed



**Docs**

* 📝 Add Docstrings by <a href="https://github.com/mauro-andre/pyodmongo/pull/119" target="_blank">@mauro-andre</a>

* 💡 Comment resolve_db_fields by <a href="https://github.com/mauro-andre/pyodmongo/pull/120" target="_blank">@mauro-andre</a>



**Refactor**

* ♻️ Refactor Id and __init__ DbModel by <a href="https://github.com/mauro-andre/pyodmongo/pull/121" target="_blank">@mauro-andre</a>

* ♻️ Replace sort operator file by <a href="https://github.com/mauro-andre/pyodmongo/pull/122" target="_blank">@mauro-andre</a>



**New Features**

* ✨ Querying with magic methods by <a href="https://github.com/mauro-andre/pyodmongo/pull/123" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.7.3...0.8.0

---
## v0.7.3 - 2024-04-22
Bug fix

---
## v0.7.2 - 2024-04-22
## What's Changed

* ♻️ Change access to dictionary key by <a href="https://github.com/mauro-andre/pyodmongo/pull/114" target="_blank">@mauro-andre</a>

* ♻️ Move init_subclass and pydantic_init_subclass to __new__ in pyodmongometa by <a href="https://github.com/mauro-andre/pyodmongo/pull/115" target="_blank">@mauro-andre</a>

* ♻️ Remove Pyodmongometa and use just DbMeta by <a href="https://github.com/mauro-andre/pyodmongo/pull/116" target="_blank">@mauro-andre</a>

* 📝 Change de main description by <a href="https://github.com/mauro-andre/pyodmongo/pull/117" target="_blank">@mauro-andre</a>

* Refacor dbfield by <a href="https://github.com/mauro-andre/pyodmongo/pull/118" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.7.1...0.7.2

---
## v0.7.1 - 2024-04-19
## What's Changed

* ♻️ Refactor to be agnostic to Pydantic Basemodel Metaclass by <a href="https://github.com/mauro-andre/pyodmongo/pull/113" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.7.0...0.7.1

---
## v0.7.0 - 2024-04-11
## What's Changed

* ✨ find_one and find_many with sort by <a href="https://github.com/mauro-andre/pyodmongo/pull/112" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.6.8...0.7.0

---
## v0.6.8 - 2024-04-10
## What's Changed

* ♻️ Reference pipeline with deep nested object and list by <a href="https://github.com/mauro-andre/pyodmongo/pull/111" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.6.7...0.6.8

---
## v0.6.7 - 2024-04-08
## What's Changed

* 🐛 Db Model init with empty objects treatment by <a href="https://github.com/mauro-andre/pyodmongo/pull/110" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.6.6...0.6.7

---
## v0.6.6 - 2024-03-31
## What's Changed

* 🔥 Remove $project stage in pipeline by <a href="https://github.com/mauro-andre/pyodmongo/pull/109" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.6.5...0.6.6

---
## v0.6.5 - 2024-03-26
## What's Changed

* Match stage before by <a href="https://github.com/mauro-andre/pyodmongo/pull/108" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.6.4...0.6.5

---
## v0.6.4 - 2024-03-22
## What's Changed

* ⚡️ Change count pipeline by <a href="https://github.com/mauro-andre/pyodmongo/pull/107" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.6.3...0.6.4

---
## v0.6.3 - 2024-03-15
## What's Changed

* Recursive nested object pipeline by <a href="https://github.com/mauro-andre/pyodmongo/pull/106" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.6.2...0.6.3

---
## v0.6.2 - 2024-03-13
## What's Changed

* 🎨 Pipeline reference at first by <a href="https://github.com/mauro-andre/pyodmongo/pull/105" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.6.1...0.6.2

---
## v0.6.1 - 2024-03-01
## What's Changed

* 📝 Populate - remove reference list limitation by <a href="https://github.com/mauro-andre/pyodmongo/pull/101" target="_blank">@mauro-andre</a>

* 🐛 datetime in mount query filter by <a href="https://github.com/mauro-andre/pyodmongo/pull/102" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.6.0...0.6.1

---
## v0.6.0 - 2024-02-22
## What's Changed

* ⚡️ recursive reference pipeline with lookup by <a href="https://github.com/mauro-andre/pyodmongo/pull/100" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.5.1...0.6.0

---
## v0.5.1 - 2024-02-19
## What's Changed

* 🐛 Passing pipeline in lookup with project stage for serialize fields by <a href="https://github.com/mauro-andre/pyodmongo/pull/99" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.5.0...0.5.1

---
## v0.5.0 - 2024-02-16
## What's Changed

* ✨ as_dict response in find_one and find_many by <a href="https://github.com/mauro-andre/pyodmongo/pull/98" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.4.0...0.5.0

---
## v0.4.0 - 2024-02-12
## What's Changed

* ✨ regex js format in $in operator by <a href="https://github.com/mauro-andre/pyodmongo/pull/97" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.3.2...0.4.0

---
## v0.3.2 - 2024-01-17
## What's Changed

* ⚡️ Added project pipeline stage in aggregate by <a href="https://github.com/mauro-andre/pyodmongo/pull/96" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.3.1...0.3.2

---
## v0.3.1 - 2023-11-20
## What's Changed

* 🔥 Remove metaclass and add DbModelCore by <a href="https://github.com/mauro-andre/pyodmongo/pull/95" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.3.0...0.3.1

---
## v0.3.0 - 2023-11-17
## What's Changed

* 🔖 Compatibility with pydantic 2.5.x by <a href="https://github.com/mauro-andre/pyodmongo/pull/94" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.2.11...0.3.0

---
## v0.2.11 - 2023-10-17
## What's Changed

* 🐛 id, created_at, updated_at can set with None by <a href="https://github.com/mauro-andre/pyodmongo/pull/93" target="_blank">@mauro-andre</a>

**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.2.10...0.2.11

---
## v0.2.10 - 2023-10-05
## What's Changed

* 🔥 _id alias analysis in consolidate dict by <a href="https://github.com/mauro-andre/pyodmongo/pull/84" target="_blank">@mauro-andre</a>

* 🚑 DbModel with empty dict in a key by <a href="https://github.com/mauro-andre/pyodmongo/pull/90" target="_blank">@mauro-andre</a>



**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.2.9...0.2.10

---
## v0.2.9 - 2023-10-03


---
## v0.2.8 - 2023-09-26
## What's Changed

* ✏️ Dynamic plain validator in id_model by <a href="https://github.com/mauro-andre/pyodmongo/pull/69" target="_blank">@mauro-andre</a>





**Full Changelog**: https://github.com/mauro-andre/pyodmongo/compare/0.2.7...0.2.8

