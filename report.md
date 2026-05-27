# Report: Internet ASN and Customer Cone Analysis

## Student Information

- Name:
- Date:

---

## Step 1 — Dataset fields and values

### Organization dataset (orgs.jsonl)

`scripts/org-table-fields.py`

| name    | type | values | description |
| ------- | ---- | ------ | ----------- |
| score   |      |        |             |
| orgId   |      |        |             |
| orgName |      |        |             |
| members |      |        |             |

The table above is a starter — your script should discover and document all fields.

- **total organizations**:
- **total ASNs**:

### AS Relationships dataset (as-rel.txt)

`scripts/asn-rel-table-fields.py`

| type              | count |
| ----------------- | ----- |
| provider-customer |       |
| peer-peer         |       |
| total             |       |

**clique ASNs**:

**IXP ASNs**:

**Connecting the datasets**: Which values appear in more than one dataset? How could you use those shared values to combine information across datasets?

(your answer here)

---

## Step 2 — Distribution plots

### Step 2.1 — Customer cone distribution

#### eCDF

`scripts/customer-cone-ecdf.py`

![Customer Cone eCDF](figures/customer-cone-ecdf.png)

**Question 2.1**: What do you observe? What makes it hard to read?

(your answer here)

#### eCCDF

`scripts/customer-cone-eccdf.py`

![Customer Cone eCCDF](figures/customer-cone-eccdf.png)

| type   | range | number of ASNs |
| ------ | ----- | -------------- |
| one    |       |                |
| small  |       |                |
| middle |       |                |
| large  |       |                |

**Question 2.1.2**: What does this tell you about the customer cone distribution?

(your answer here)

### Step 2.2 — Organization size distribution

`scripts/org-size-ecdf.py`

![Organization size](figures/org-size-ecdf.png)

| type   | range | number of organizations |
| ------ | ----- | ----------------------- |
| one    |       |                         |
| small  |       |                         |
| middle |       |                         |
| large  |       |                         |

**Question 2.2**: What does this tell you about the organization size distribution? How does it compare to the customer cone distribution?

(your answer here)

---

## Step 3 — Transit-free, transit, and edge ASN counts

`scripts/asn-transit-table.py`

| type         | total | customer cone range | one | small | middle | large |
| ------------ | ----- | ------------------- | --- | ----- | ------ | ----- |
| transit free |       |                     |     |       |        |       |
| transit      |       |                     |     |       |        |       |
| edge         |       |                     |     |       |        |       |
| unseen       |       | -                   |     |       |        |       |

**Question 3**: What is the relationship between these three classes and customer cone sizes? What is a possible explanation?

(your answer here)

---

## Step 4 — How organizations distribute their customer cone across ASNs

`scripts/org-cone-coverage-table.py`

| organization | total ASNs | 100-99% | 98-66% | 65-33% | 32-1% | 1 ASN | 0 ASN |
| ------------ | ---------- | ------- | ------ | ------ | ----- | ----- | ----- |
|              |            |         |        |        |       |       |       |
|              |            |         |        |        |       |       |       |
|              |            |         |        |        |       |       |       |
|              |            |         |        |        |       |       |       |
|              |            |         |        |        |       |       |       |
|              |            |         |        |        |       |       |       |
|              |            |         |        |        |       |       |       |
|              |            |         |        |        |       |       |       |
|              |            |         |        |        |       |       |       |
|              |            |         |        |        |       |       |       |

Describe your three organization classes based on the patterns you observe above:

-
-
-

`scripts/org-category-table.py`

| class name | total organizations | customer cone range |
| ---------- | ------------------- | ------------------- |
|            |                     |                     |
|            |                     |                     |
|            |                     |                     |

**Question 4**: How well do your classes divide the system?

(your answer here)

---

## Step 5 — Top 5 ASNs summary

| asn | name | country | Cone Size | Cone Class | Org Size | Org Dom |
| --- | ---- | ------- | --------- | ---------- | -------- | ------- |
|     |      |         |           |            |          |         |
|     |      |         |           |            |          |         |
|     |      |         |           |            |          |         |
|     |      |         |           |            |          |         |
|     |      |         |           |            |          |         |

**Question 5**: What do we know from this table about the largest ASNs? What do they have in common and what is different?

(your answer here)
