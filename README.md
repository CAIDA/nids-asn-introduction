# nids-asn-cone

This module will introduce you to the Internet's Autonomous System using real world Internet data.
Since this is an early module, it is also designed to tell you how to approach a new dataset.

**How to use this module:**

1. Read the **Focus** — this frames the rest of the module.
2. Read the **Background** for required context.
3. Check **Resources** — verify you can access all data sources before you begin.
4. Follow **Setup** to install dependencies and download the data.
5. Work through the **Analysis** steps in order — each one introduces its concept and dataset.
6. Create `report.md` and fill it in with your findings as you complete the steps. A starter template is included in this repository.

## Focus

This module is designed as an introduction to Autonomous Systems, how they are used by organizations, and how to use them to understand
the macroscopic Internet.

## Background

- **Reading Required**:
  - [Autonomous system (Internet)](<https://en.wikipedia.org/wiki/Autonomous_system_(Internet)>) (Wikipedia)
  - [Lecture: AS Relationships and Customer Cones](https://cseweb.ucsd.edu/classes/wi23/cse291-e/slides/cse291e-lecture-03.pdf) (slides)
  - [Empirical Distribution Function](https://en.wikipedia.org/wiki/Empirical_distribution_function) (wiki)
- **Reading Optional**:
  - [Autonomous Systems Topology](https://www.caida.org/catalog/media/2016_as_intro_topology_wind/as_intro_topology_wind.pdf) (slides)

#### Autonomous Systems

An **Autonomous System (AS)** is an independently operated network on the Internet — a collection of IP prefixes managed by a single administrative entity under a common routing policy. Each AS is identified by a globally unique **Autonomous System Number (ASN)**. ASNs are the unit of routing on the Internet: networks exchange reachability information at the AS level using the **Border Gateway Protocol (BGP)**.

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

### Install uv

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

| name     | type   | values     | description           |
| -------- | ------ | ---------- | --------------------- |
| score    | int    | ?..????    | sorting by importance |
| orgId    | string |            | org unique id         |
| orgName  | string |            | organization name     |
| members  | [int]  | size(?..?) | array of ASN members  |

**total organizations**: ??
**total ASNs**: ??

**AS Relationships Table Starter**
| type | number |
| provider-customer | ??? |
| peer-peer | ??? |

Suggestion for handling the JSONL file:

- Start with the first few objects in the orgs.jsonl file. Copy/paste them into a JSON pretty print to get their fields and values.
  - Populate the table with what you see.
  - Write a script that parses based on those objects and sorts and counts the values in each field. - This script should print out objects that don't parse correctly, don't have all the keys, or are unusual. - Update the script until it can handle all the objects. - Print out the table.
    For the CSV file, it's basically the same, but you don't have to worry about changing fields
  - Create the script with what you expect to find, then have it print out rows that don't match that expectation
  - Loop over the script until it handles every row.
  - Print out the table.

When you are writing this script, make sure it checks your expectation and let you know when values don't agree.
If you think org.jsonl's score always goes down by one, your code needs to check this and report when it doesn't.

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

Since the customer cone values range is very large, a good place to start is the Empirical Cumulative Distribution Function (eCDF).

(eCDF of the customer cone goes here)

As you can see, the density at the front makes it hard to read. So let's change it to be an Empirical Complementary Cumulative Distribution Function (eCCDF).
This will have the values drop down to smaller numbers for the larger customer cone sizes. Let's also make the x and y axes logarithmic, so we can keep the large values, but still see small value changes.

- x-axis: log customer cone size
- y-axis: log number of ASNs with a customer cone size equal to or greater

What does this tell you about the customer cone distribution? Does it have clean lines for small, middle, large?

---

#### Step 2.2 - Create a bar chart plot of the organization sizes.

The range of values is small enough for organization sizes that you can use a bar chart.

- x-axis: organization size
- y-axis: log number of organizations

What does this tell you about the organization size distribution? Does it have clean lines for small, middle, large?

### Step 3 (5pts) - Count the number of transit free, transit, and edge ASes.

Another way to classify ASNs is as transit free, transit, or edge. We will do this by looking at the relationships
in the as-rel.txt file.

- **transit free**: Will have no providers in the as-rel.txt file
- **transit**: will have at least one customer and one provider
- **edge**: has one provider and no customers
- **unseen**: is found in the orgs file, but not in the as-rel file (not seen in BGP)

We will do this by building a table counting the number and some properties of each of these types of ASes.

| type         | total | customer cone range |
| ------------ | ----- | ------------------- |
| transit free | ??    | ??..??              |
| transit      | ??    | ??..??              |
| edge         | ??    | ??..??              |
| unseen       | ??    | -                   |

What is the relationship between these three classes and customer cone sizes?
What is a possible explanation?

---

### Step 4 (5pts) — Looking through the lens of the customer cone, how are organizations using their ASNs?

##### Step 4.1 How does an organization distribute its customer cone routing across its ASNs?

Create a table with the top 50 organizations by the number of ASNs, that captures how organizations are using their customer cone.

For each, the last cells give the number of ASNs with that given percentage of the organization's largest customer cone size.

| organization | total ASNs | 100% cone | 99-75% cone | 74-50% cone | 49-25% cone | 25-1% cone | 0% cone |
| ------------ | ---------- | --------- | ----------- | ----------- | ----------- | ---------- | ------- |
|              |            |           |             |             |             |            |         |

Define three classes of ASNs based on how they distribute their customer cone among their ASNs.

### Step 5 (5pts) — Count the number of ASes in each class

Divide all the ASNs into your classes, count how many are in each class, and give a description of your classification.

| group name | total ASNs (percentage) | description |
| ---------- | ----------------------- | ----------- |
|            |                         |             |

What does this tell you about how organizations are using their ASNs?

---

### Step 6 - Answer these questions based on the plots and tables from earlier steps.

Fill in the table for the largest 30 ASNs.

| name | country | customer cone size | type of transit (step 3) | percentage of all ASNs | ASN class (step 4) |
| ---- | ------- | ------------------ | ------------------------ | ---------------------- | ------------------ |
|      |         |                    |                          |                        |                    |

What do we know from this table about the largest ASNs? What do they have in common and what is different?

---

## Report

Document your answers in [report.md](./report.md). Fill it in as you work so your final submission includes:

- your Step 1–6 answers,
- the distribution plots from Step 2,
- the transit classification table from Step 3,
- the organization and ASN class tables from Steps 4 and 5, and
- the top-30 ASN summary table from Step 6.
