## Overview

```
Tasks.md                            ⬅ # Update with tables and answers
└- scripts/
|  ├- asn-cone-classes.py           ⬅ # You will need to write
|  └- country-cone-classes.py       ⬅ # You will need to write
└- tables/
   ├- asn-customer-cone-classes.md
   └- country-cone-classes.md
```

- Task 1 [Download Datasets and read Overviews](Datasets.md)
- Task 2: Create **scripts/asn-cone-classes.py**
  - step 2.1 use that script to create **tables/asn-cone-classes.md**
  - step 2.2 use **tables/asn-cone-classes.md** to answer questions 1,2, and 3
- Task 3: Create **scripts/country-cone-classes.py**
  - step 3.1 use that script to create **tables/country-cone-classes.md**
  - step 3.2 use **tables/country-cone-classes.md** to answer questions 4, 5, and 6

## Task 1 Download datasets

([Instructions and Overview](Datasets.md))

- data/orgs.jsonl
- data/20260501.ppdc-ases.txt.bz2

## Task 2: ASN Classified by ASN Customer Cone size

### 2.1 Create scripts/asn-cone-classes.py

Create `scripts/asn-cone-classes.py` so that it creates **Table 1**

Since we will be testing your script with the following command:

```bash
uv run scripts/asn-cone-classes.py --output tables/asn-cone-classes.md data/20260501.ppdc-ases.txt.bz2
```

### Table 1: ASN Customer Cone Classes

- **class**: the name of the class
- **range**: the range of values that defines the class
  - [**max**]: is the maximum customer cone size seen in the class
- **number of ASNs**: the number of ASNs in the class
  - **[total]**: is the total number of ASNs in the class
  - **[percentage]**: is the percentage of all ASNs in the class (one decimal place)

|          class | range        | number of ASNs |   percentage |
| -------------: | ------------ | -------------: | -----------: |
|           stub | 1            |        [total] | [percentage] |
|  transit small | 2..10        |        [total] | [percentage] |
| transit middle | 11..1000     |        [total] | [percentage] |
|  transit large | 1001..10000  |        [total] | [percentage] |
|   transit huge | 10001..[max] |        [total] | [percentage] |

### 2.2 Answer questions 1, 2, and 3

1. What percentage of ASNs are stub ASes (customer cone size of 1)? What does this suggest about the structure of the Internet?
2. How large is the maximum customer cone? What does this tell you about the most influential ASes on the Internet?
3. How do the proportions of stub, small transit, and large transit ASes compare? What does this distribution reveal about how ASes are organized hierarchically?

## Task 3: How are these classes divided across countries

Create `scripts/country-cone-classes.py` so that it creates **Table 2**

- You will use the classification from task 2
- Use `data/orgs.jsonl` to map each ASN into a country.
- Find the top 4 countries by the number of ASNs in the country.
  - All other ASNs will be mapped to **other**.
- These countries are the columns of table 2 as two letter country code (`US`,`JP`) .
- For each class, provide a count
- Each row will be a single customer cone class
  - [**total**] : total number of ASN in that country with that class
  - [**%**] : percentage of the class in that country

We will test your script with the following command:

```bash
uv run scripts/country-cone-classes.py --output tables/country-cone-classes.md -O data/orgs.jsonl -C data/20260501.ppdc-ases.txt.bz2
```

### Table 2: How ASNs in each class are divided between the Top Ranked Countries

| column      | description                                             |
| ----------- | ------------------------------------------------------- |
| name        | class name                                              |
| 1st country | country with the most ASNs (dynamically determined)     |
| 2nd country | country with the 2nd most ASNs (dynamically determined) |
| 3rd country | country with the 3rd most ASNs (dynamically determined) |
| 4th country | country with the 4th most ASNs (dynamically determined) |
| other       | all other ASNs                                          |

The example table below uses numbered placeholders for column headers. Your script should replace these with the actual 2-letter country codes it discovers from the data (e.g., `US`, `CN`, `BR`).

| name           | 1st           | 2nd           | 3rd           | 4th           | other         |
| -------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| stub           | [total] ([%]) | [total] ([%]) | [total] ([%]) | [total] ([%]) | [total] ([%]) |
| transit small  | [total] ([%]) | [total] ([%]) | [total] ([%]) | [total] ([%]) | [total] ([%]) |
| transit middle | [total] ([%]) | [total] ([%]) | [total] ([%]) | [total] ([%]) | [total] ([%]) |
| transit large  | [total] ([%]) | [total] ([%]) | [total] ([%]) | [total] ([%]) | [total] ([%]) |
| transit huge   | [total] ([%]) | [total] ([%]) | [total] ([%]) | [total] ([%]) | [total] ([%]) |

### 3.2 Answer questions 4, 5, and 6

4. Which countries have the most transit huge ASNs? What does this tell you about where Internet infrastructure is concentrated?
5. What proportion of all ASNs fall in the "other" category? What does this suggest about the geographic distribution of the global Internet?
6. Do the same countries dominate across all AS classes (stub, transit small, transit huge)? What patterns do you observe across the rows?
