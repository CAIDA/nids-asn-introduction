# nids-asn-cone

This module will introduce you to the Internet's Autonomous System using real world Internet data.
Since this is an early module, it is also designed to teach you how to approach a new dataset.

**How to use this module:**

1. Read the **Focus** — this frames the rest of the module.
2. Read the **Background** for required context.
3. Check **Resources** — verify you can access all data sources before you begin.
4. Follow **Setup** to install dependencies and download the data.
5. Work through the **Analysis** steps in order — each one introduces its concept and dataset.
6. Fill in `report.md` with your findings as you complete the steps. A starter template is included in this repository.

## Focus

What are the largest Organizations on the Internet? How could this be decided? What can we know about them from the datasets found in this module?

## Background

- **Reading Required**:
  - [Autonomous system (Internet)](<https://en.wikipedia.org/wiki/Autonomous_system_(Internet)>) (Wikipedia)
  - [Lecture: AS Relationships and Customer Cones](https://cseweb.ucsd.edu/classes/wi23/cse291-e/slides/cse291e-lecture-03.pdf) (slides)
  - [Empirical Distribution Function](https://en.wikipedia.org/wiki/Empirical_distribution_function) (Wikipedia)
  - [Ramer–Douglas–Peucker algorithm](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm) (Wikipedia)
- **Reading Optional**:
  - [On the Importance of Being an AS: An Approach to Country-Level AS Rankings](https://catalog.caida.org/paper/2023_on_importance_being_as) (paper)
  - [Autonomous Systems Topology](https://www.caida.org/catalog/media/2016_as_intro_topology_wind/as_intro_topology_wind.pdf) (slides)

#### Autonomous Systems

There are many [different ways to judge an organization's important or size](https://catalog.caida.org/paper/2023_on_importance_being_as).
In this module, we will be using an organization's visibility in **Border Gateway Protocol (BGP)** routing. BGP is the standardized exterior gateway protocol designed to exchange routing and reachability information among **autonomous systems (AS)** on the Internet, determining the most efficient paths for data to travel.

An AS is an independently operated network on the Internet — a collection of IP prefixes managed by a single administrative entity under a common routing policy. Each AS is identified by a globally unique **Autonomous System Number (ASN)**.

An ASN is assigned to a network, not directly to a legal entity. One organization may operate multiple ASNs (for example, to represent different geographic regions or service tiers), and in rare cases an ASN may be shared between affiliated entities.

Organizations own multiple ASNs, for purposes of this assignment we will call this the organization's size.

#### Customer Cone

The customer cone is a metric used to gauge the size and influence of an AS within the global routing system. It represents the complete set of ASes, IPv4 prefixes, or IPv4 addresses that can be reached from a given AS by following only provider-to-customer links.

Simply put, an AS's customer cone includes the AS itself, its direct customers, its customers' customers, and so on—effectively capturing all networks that rely on it and pay it, directly or indirectly, for Internet transit.

## Resources

Verify you can access each resource before beginning the module.

**AS Organization** - Provides a list of organizations and the ASNs they have registered in the Internet Registries.

- API: `https://api.data.caida.org/as2org/v1/orgs/`
- script: scripts/orgs-download.py

**CAIDA AS Relationships (Serial-1)** — AS Relationship and Customer Cone inferred dataset

- WEB: `https://catalog.caida.org/dataset/as_relationships_serial_1`
  - `(date).ppdc-ases.txt.bz2` : Per-AS provider-peer-customer (PPDC) cones: for each AS, the set of all ASes reachable via customer links.
  - `(date).as-rel.txt.bz2` : AS Relationships between two ASNs

## Setup

### Install the Python manager uv

If you don't have uv installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install dependencies

```bash
uv sync
```

This creates a virtual environment and installs `requests`, `matplotlib`, and `numpy`. Run once (or after pulling changes).

### Download the data

```bash
# Download the AS 2 Org information
uv run scripts/orgs-download.py --url https://api.data.caida.org/as2org/v1/orgs/ --output data/orgs.jsonl
```

Manually download the two latest files from https://catalog.caida.org/dataset/as_relationships_serial_1 and decompress them:

```bash
# Customer cone data
bunzip2 data/(date).ppdc-ases.txt.bz2
mv data/(date).ppdc-ases data/as-cone.txt

# AS relationship data
bunzip2 data/(date).as-rel.txt.bz2
mv data/(date).as-rel data/as-rel.txt
```

Replace `(date)` with the actual date in the filenames (e.g., `20260501`).

## Analysis

Please use data from 2026/05/01.

---

### Step 1 (5pt) — What kinds of values and fields do you expect to find in the dataset?

For each dataset create a table with a row for each column/field name, type, and values description.
You will create two scripts, one for each dataset, that print out the columns and the values contained in those columns.

- **name**: The name of the field or column (ASN, name, degree)
- **type**: Int, string, etc
- **values**: This will depend on what kind of values you find
  - If it's number what is the min and max?
  - Is it a small number of enumerated strings, can you list them?
  - Is it a large number of enumerated strings, are some more common than others?
  - Is it best described with a short description?

**Organization Table Starter**

| name    | type       | values                        | description                                                                    |
| ------- | ---------- | ----------------------------- | ------------------------------------------------------------------------------ |
| score   | `int`      | `(minimum)`..`(maximum)`      | What could this represent? What does it tell you about how the data is sorted? |
| orgId   | `string`   |                               | org unique id                                                                  |
| orgName | `string`   |                               | organization name                                                              |
| members | `[string]` | size `(minimum)`..`(maximum)` | array of ASN members                                                           |

The table above is intentionally incomplete — your script should discover and document all fields in the dataset.

- **total organizations**: `(total number of organiztions)`
- **total ASNs**: `(total number of ASNs)`

**AS Relationships Table Starter**

| type              | count                                    |
| ----------------- | ---------------------------------------- |
| provider-customer | `(number of provider to customer links)` |
| peer-peer         | `(number of peer to peer links)`         |

For the flat text files (as-cone.txt and as-rel.txt), start by reading the comment lines at the top of each file (lines beginning with `#`) — they describe the file's structure and how it was generated. The upstream CAIDA README at https://publicdata.caida.org/datasets/as-relationships/serial-1/README.txt is also a useful reference.

Suggestion for handling the JSONL file:

- Start with the first few objects in the orgs.jsonl file. Copy/paste them into a JSON pretty print to get their fields and values.
  - Populate the table with what you see.
  - Write a script that parses based on those objects and sorts and counts the values in each field. - This script should print out objects that don't parse correctly, don't have all the keys, or are unusual. - Update the script until it can handle all the objects. - Print out the table.
    For the flat text files, the approach is the same, but the fields are fixed per line so you don't need to handle varying keys.
  - Create the script with what you expect to find, then have it print out rows that don't match that expectation
  - Loop over the script until it handles every row.
  - Print out the table.

When you are writing this script, make sure it checks your expectation and let you know when values don't agree.
If you think org.jsonl's score always goes down by one, your code needs to check this and report when it doesn't.

**Connecting the datasets**: Look at the fields across all three datasets. Which values appear in more than one dataset? How could you use those shared values to combine information across datasets?

---

### Step 2 (1pt) — Understand the distribution of organization member and customer cone size.

We want to create a plot for both of these graphs.

| type    | x-axis | y-axis                            |
| ------- | ------ | --------------------------------- |
| eCDF    | value  | number of values equal or less    |
| eCCDF   | value  | number of values equal or greater |
| density | value  | number of values equal            |

---

#### Step 2.1 - Create a plot for the customer cone distribution

Since the customer cone values range is very large, a good place to start is the Empirical Cumulative Distribution Function (eCDF). Create it and include it in your report.

(eCDF of the customer cone goes here)

Notice the density near the low end makes it hard to read the distribution clearly. To address this, switch to an Empirical Complementary Cumulative Distribution Function (eCCDF) — this inverts the y-axis so larger customer cone sizes drop toward smaller values, making the tail easier to read. Also make both axes logarithmic so large values don't dominate and small differences remain visible.

- x-axis: log customer cone size
- y-axis: log number of ASNs with a customer cone size equal to or greater

Now use a _Ramer-Douglas-Peucker (RDP) Algorithm_ (use rdp library) to identify natural breakpoints in the line. Look for a cluster at cone=1 (leaf nodes with no downstream customers), then look for breakpoints separating small, middle, and large providers in the tail. The buckets should not overlap.

(example)
| type | range | number of ASNs |
| ------ | ------------ | -------------- |
| one | 1 | ??? |
| small | (min)..(max) | ??? |
| middle | (min)..(max) | ??? |
| large | (min)..(max) | ??? |

**\*Question 2.1**: What does this tell you about ASNs distribution?

---

#### Step 2.2 - Create a distribution plot of the organization sizes.

Create a distribution plot for organization sizes.

- x-axis: organization size
- y-axis: log number of organizations

Apply the same four-class breakdown you used for the customer cone:

(example)
| type | range | number of organizations |
| ------ | ------------ | ----------------------- |
| one | 1 | ??? |
| small | (min)..(max) | ??? |
| middle | (min)..(max) | ??? |
| large | (min)..(max) | ??? |

What does this tell you about the organization size distribution? How does it compare to the customer cone distribution?

### Step 3 (5pts) - Count the number of transit free, transit, and edge ASes.

Another way to classify ASNs is as transit free, transit, or edge. We will do this by looking at the relationships
in the as-rel.txt file.

- **transit free**: Will have no providers in the as-rel.txt file
- **transit**: will have at least one customer and one provider
- **edge**: has at least one provider and no customers
- **unseen**: is found in the orgs file, but not in the as-rel file (not seen in BGP)

We will do this by building a table counting the number and some properties of each of these types of ASes.

| type         | total          | customer cone range      | one | small | middle | large |
| ------------ | -------------- | ------------------------ | --- | ----- | ------ | ----- |
| transit free | `(total ASNs)` | `(minimum)`..`(maximum)` | ??? | ???   | ???    | ???   |
| transit      | `(total ASNs)` | `(minimum)`..`(maximum)` | ??? | ???   | ???    | ???   |
| edge         | `(total ASNs)` | `(minimum)`..`(maximum)` | ??? | ???   | ???    | ???   |
| unseen       | `(total ASNs)` | N/A                      | ??? | ???   | ???    | ???   |

What is the relationship between these three classes and customer cone sizes?
What is a possible explanation?

---

### Step 4 (5pts) — Looking through the lens of the customer cone, how are organizations using their ASNs?

##### Step 4.1 How does an organization distribute its customer cone routing across its ASNs?

Create a table with the top 10 organizations (with 2 or more ASNs) that have the largest customer cone.
Show how many of each organization's ASNs fall into each coverage bracket.

To calculate the organization's customer cone, take the union of all ASN cones the organization operates. An ASN's cone coverage is `len(asn_customer_cone) / len(organization_customer_cone)`.

| organization | total ASNs | 100-99% | 98-66% | 65-33% | 32-1% | 1 ASN | 0 ASN |
| ------------ | ---------- | ------- | ------ | ------ | ----- | ----- | ----- |
|              |            |         |        |        |       |       |       |

Define three classes of organizations based on the patterns you observe in the table above. The class definitions — their names, boundaries, and descriptions — are yours to invent.

Count how many organizations fall into each class and note the customer cone range for each:

| class name | total organizations | customer cone range |
| ---------- | ------------------- | ------------------- |
|            |                     |                     |

What does this tell you about how organizations are using their ASNs?

---

### Step 5 (5pts) — Summary of the largest ASNs

Fill in the table for the largest 5 ASNs.

| asn | name | country | Cone Size | Cone Class | Org Size | Org Dom |
| --- | ---- | ------- | --------- | ---------- | -------- | ------- |
|     |      |         |           |            |          |         |

Where:

- **Cone Size**: customer cone size (Step 2)
- **Cone Class**: one/small/middle/large classification from Step 2
- **Org Size**: number of ASNs the organization operates (Step 1)
- **Org Dom**: the organization class you assigned in Step 4

What do we know from this table about the largest ASNs? What do they have in common and what is different?

---

## Report

Document your answers in [report.md](./report.md). Fill it in as you work so your final submission includes:

- your Step 1–5 answers,
- the distribution plots from Step 2,
- the transit classification table from Step 3,
- the organization class tables from Step 4, and
- the top-5 ASN summary table from Step 5.
