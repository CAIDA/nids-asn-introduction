# Report: Internet ASN and Customer Cone Analysis

## Student Information

- Name:
- Date:

---

## Step 1 — Dataset fields and values

### Organization dataset (orgs.jsonl)

| name    | type     | values                    | description |
| ------- | -------- | ------------------------- | ----------- |
| score   | int      | (minimum)..(maximum)      | What could this represent? What does it tell you about how the data is sorted? |
| orgId   | string   |                           | org unique id |
| orgName | string   |                           | organization name |
| members | [string] | size (minimum)..(maximum) | array of ASN members |

The table above is intentionally incomplete — your script should discover and document all fields in the dataset.

**Total organizations**: ??
**Total ASNs**: ??

### AS Relationships dataset (as-rel.txt)

| type | count |
| ---- | ----- |
| provider-customer | ??? |
| peer-peer | ??? |

**Connecting the datasets**: Which values appear in more than one dataset? How could you use those shared values to combine information across datasets?

Answer:

---

## Step 2 — Distribution plots

### Step 2.1 — Customer cone distribution

#### eCDF

(Paste your eCDF plot here)

What do you observe? What makes it hard to read?

Answer:

#### eCCDF

(Paste your eCCDF plot here)

What does this tell you about the customer cone distribution? Does it have clean lines for small, middle, and large sizes?

Answer:

### Step 2.2 — Organization size distribution (bar chart)

(Paste your bar chart here)

What does this tell you about the organization size distribution? Does it have clean lines for small, middle, and large sizes?

Answer:

---

## Step 3 — Transit-free, transit, and edge ASe counts

| type         | total | customer cone range |
| ------------ | ----- | ------------------- |
| transit free | ??    | ??..??              |
| transit      | ??    | ??..??              |
| edge         | ??    | ??..??              |
| unseen       | ??    | -                   |

What is the relationship between these three classes and customer cone sizes? What is a possible explanation?

Answer:

---

## Step 4 — How organizations distribute their customer cone across ASNs

Top 50 organizations by number of ASNs:

| organization | total ASNs | 100% cone | 99-75% cone | 74-50% cone | 49-25% cone | 25-1% cone | 0% cone |
| ------------ | ---------- | --------- | ----------- | ----------- | ----------- | ---------- | ------- |
|              |            |           |             |             |             |            |         |

Describe your three ASN classes based on the patterns you observe above:

| class name | definition |
| ---------- | ---------- |
|            |            |
|            |            |
|            |            |

---

## Step 5 — ASN class counts

| group name | total ASNs (percentage) | description |
| ---------- | ----------------------- | ----------- |
|            |                         |             |

What does this tell you about how organizations are using their ASNs?

Answer:

---

## Step 6 — Top 30 ASNs summary

| name | country | customer cone size | type of transit (step 3) | % of all visible ASNs in cone | ASN class (step 4) |
| ---- | ------- | ------------------ | ------------------------ | ----------------------------- | ------------------ |
|      |         |                    |                          |                        |                    |

What do we know from this table about the largest ASNs? What do they have in common and what is different?

Answer:
