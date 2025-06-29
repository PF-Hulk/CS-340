# Grazioso Salvare Rescue-Dog Dashboard  
**Course :** CS-340 • Module 8 Portfolio Submission  
**Author :** Chris Davidson | **Term :** May – Jun 2025  

---

## Project Artifacts

| Artifact | Description |
|----------|-------------|
| [`dashboard.ipynb`](./dashboard.ipynb) | Jupyter-Dash notebook— interactive data table, map, donut & scatter widgets |
| [`animal_shelter.py`](./animal_shelter.py) | Re-usable CRUD library (PyMongo wrapper) |
| [`README_Project2.docx`](./README_Project2.docx) | End-user installation & usage guide for the dashboard |

---

## Reflection

### How do you write programs that are maintainable, readable, and adaptable?  
I follow three habits that paid off in this project:

* **Single-purpose modules** – `animal_shelter.py` owns _all_ database I/O, so the Dash code never repeats connection strings or query syntax.  
* **PEP-8 & type hints** – names like `def read(self, query: dict, projection: dict | None = None)` make intent obvious and let IDEs catch mismatched types.  
* **Docstrings & tests** – each CRUD method has a one-line summary plus edge-case unit tests; if I ever swap MongoDB for another backend I only rewrite this file.

Because of that separation I can now import the same CRUD class into future scripts—say, a nightly ETL job or a Flask API—without touching the dashboard.

---

### How do you approach a problem as a computer scientist?  
I start by **formalising the requirements** (rescue-team presets, live filtering, geolocation).  
From there the workflow is:

1. **Model → query design** – sketch the BSON documents, prototype finds/aggregates in `mongosh`.  
2. **Controller → Python layer** – wrap those queries in functions that return plain lists/dicts.  
3. **View → Dash callbacks** – bind the data to UI components and iterate.

Compared with earlier courses where I wrote monolithic scripts, I deliberately applied MVC and test-driven steps here; next time I’d keep the same pattern but script the seed/tear-down of test databases with Docker for faster repeats.

---

### What do computer scientists do, and why does it matter?  
We turn fuzzy questions (“Which dogs fit a water-rescue profile?”) into reliable, reusable tools.  
For Grazioso Salvare, this dashboard:

* **saves hours** of manual spreadsheet filtering;  
* **reduces risk** of overlooking a candidate by showing every record;  
* **reveals trends** (age vs. outcome, location clusters) that guide training resources.
