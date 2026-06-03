[README](Readme.md) | [Introduction](Introduction.md) | [Datasets](Datasets.md) | [Tasks](Tasks.md) | Report

# How the Internet assigns and uses Autonomous Systems (ASes)

**Name:** (your name here)<br/>
**Date:** (date here)

## To Do

- **Task 1**: Download and review Data
  - [ ] [Read Dataset Overview](Datasets.md)
  - [ ] download orgs.jsonl <br/>
        `uv run scripts/org-download.py  --output data/orgs.jsonl`
  - [ ] download ppdc-ases.txt <br/>
        `wget -O data/20260501.ppdc-ases.txt.bz2 https://publicdata.caida.org/datasets/as-relationships/serial-1/20260501.ppdc-ases.txt.bz2`
- **Task 2**: ASN Classififed by ASN Customer Cone size
  - [ ] [Read Task 2](Tasks.md#task-2-asn-classified-by-asn-customer-cone-size)
  - [ ] [Replace the TODO comments with your code in asn-cone-classes.py](scripts/asn-cone-classes.py)
  - [ ] build tables/asn-cone-classes.md <br/>
        `uv run scripts/asn-cone-classes.py --output tables/asn-cone-classes.md data/20260501.ppdc-ases.txt.bz2`
  - [ ] copy the table/asn-cone-classes.md into this document at INSERT

---

## Task 2: ASN Classified by ASN Customer Cone size

### Table 1: ASN Customer Cone Classes

{{INSERT:tables/asn-cone-classes.md}}

### 2.2 Answer questions 1, 2, and 3

1. What percentage of ASNs are stub ASes (customer cone size of 1)? What does this suggest about the structure of the Internet?

   **(your answer here)**

2. How large is the maximum customer cone? What does this tell you about the most influential ASes on the Internet?

   **(your answer here)**

3. How do the proportions of stub, small transit, and large transit ASes compare? What does this distribution reveal about how ASes are organized hierarchically?

   **(your answer here)**

---

## Task 3: How are these classes divided across countries

### Table 2: How ASNs in each class are divided between the Top Ranked Countries

{{INSERT:tables/country-cone-classes.md}}

### 3.2 Answer questions 4, 5, and 6

4. Which countries have the most transit huge ASNs? What does this tell you about where Internet infrastructure is concentrated?

   **(your answer here)**

5. What proportion of all ASNs fall in the "other" category? What does this suggest about the geographic distribution of the global Internet?

   **(your answer here)**

6. Do the same countries dominate across all AS classes (stub, transit small, transit huge)? What patterns do you observe across the rows?

   **(your answer here)**

[README](Readme.md) | [Introduction](Introduction.md) | [Datasets](Datasets.md) | [Tasks](Tasks.md) | Report
