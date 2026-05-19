# nids-asn-cone

This module guides you through an empirical investigation into Internet inequality. You will download real-world Internet and economic data, apply the Lorenz curve to measure concentration, and form a data-backed conclusion about how evenly Internet infrastructure is distributed.

**How to use this module:**

1. Read the **Question** — this frames the rest of the module.
2. Read the **Background** for required context.
3. Check **Resources** — verify you can access all data sources before you begin.
4. Follow **Setup** to install dependencies and download the data.
5. Work through the **Analysis** steps in order — each one introduces its concept and dataset.
6. Fill in the **Answer** section with your findings.

## Question

What can the Lorenz curve of a country's customer cone tell about Internet inequality?

## Background

- **Reading Required**:
  - [Lorenz curve](https://en.wikipedia.org/wiki/Lorenz_curve) (Wikipedia)
  - [Autonomous system (Internet)](<https://en.wikipedia.org/wiki/Autonomous_system_(Internet)>) (Wikipedia)
  - [Lecture: AS Relationships and Customer Cones](https://cseweb.ucsd.edu/classes/wi23/cse291-e/slides/cse291e-lecture-03.pdf) (slides)
- **Reading Optional**:
  - [Autonomous Systems Topology](https://www.caida.org/catalog/media/2016_as_intro_topology_wind/as_intro_topology_wind.pdf) (slides)

## Resources

Verify you can access each resource before beginning the module.

**CAIDA AS Rank** — A global ranking of Autonomous Systems (networks) by the size of their customer cone. Provides per-ASN data including cone sizes and country of registration. Use `scripts/asrank-download.py` to download the full dataset locally.

- API: `https://api.asrank.caida.org/v2/restful/doc`
- Recipe: [How to use AS Rank to classify ASNs](https://catalog.caida.org/recipe/how_to_use_as_rank_to_classify_asns)

**World Bank GDP** — Country-level GDP (current USD) published by the World Bank. Use `scripts/world-bank-download.py` to download.

- API: `https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD`

**CAIDA AS Relationships (Serial-1)** — Per-AS provider-peer-customer (PPDC) cones: for each AS, the set of all ASes reachable via customer links. Download `(date).ppdc-ases.txt.bz2` to the `data/` directory.

- Dataset: `https://catalog.caida.org/dataset/as_relationships_serial_1`

File format — each line: `<cone-as> <customer-1-as> <customer-2-as> … <customer-N-as>`
Example: `12 12 3 4` means AS 12's customer cone contains AS 12, 3, and 4.

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
# Full AS Rank dataset (~120k ASNs, may take a few minutes)
uv run scripts/asrank-download.py --output data/asns.csv

# World Bank GDP (all countries, most recent year)
uv run scripts/world-bank-download.py --output data/gdp.csv
```

To download a small sample for testing:

```bash
uv run scripts/asrank-download.py --output data/asns_sample.csv --limit 500
```

## Analysis

---

### Step 1 (1pt) — What is an ASN, and how does it relate to an organization?

An **Autonomous System (AS)** is an independently operated network on the Internet — a collection of IP prefixes managed by a single administrative entity under a common routing policy. Each AS is identified by a globally unique **Autonomous System Number (ASN)**. ASNs are the unit of routing on the Internet: networks exchange reachability information at the AS level using the **Border Gateway Protocol (BGP)**.

An ASN is assigned to a network, not directly to a legal entity. One organization may operate multiple ASNs (for example, to represent different geographic regions or service tiers), and in rare cases an ASN may be shared between affiliated entities.

The **CAIDA AS Rank** dataset, downloaded as `data/asns.csv`, describes every publicly visible ASN. Key columns:

| Column           | What it represents |
| ---------------- | ------------------ |
| `asn`            |                    |
| `name`           |                    |
| `rank`           |                    |
| `country_iso`    |                    |
| `cone_addresses` |                    |

Load `data/asns.csv` and print the row for a well-known ASN — try **AS13335** (Cloudflare), **AS3356** (Level3/Lumen), and **AS7922** (Comcast). Fill in the table above.

**Question**: For the three ASNs you looked up, do they all belong to different organizations? Can you find any example in the dataset where one organization appears to operate more than one ASN?

---

### Step 2 (5pts) — What is the ASN customer cone?

In BGP, networks form **provider–customer** relationships: a customer AS pays a provider AS to carry traffic to the rest of the Internet. This hierarchy is recursive — a customer may itself have customers. An alternative relationship is **peer-to-peer**, where two ASNs exchange traffic between their respective customers without providing upstream transit to one another.

The **customer cone** of an ASN is the set of all ASNs reachable from it following only customer links — its customers, their customers, and so on. Peer-to-peer links are not included in the cone because they do not create a transit dependency. A large customer cone means many networks depend on that AS for transit. The customer cone is the primary measure of an AS's influence in the routing hierarchy.

The dataset includes three cone columns:

| Column           | What it represents                                  |
| ---------------- | --------------------------------------------------- |
| `cone_asns`      | Number of ASNs in the customer cone                 |
| `cone_prefixes`  | Number of IP prefixes announced within the cone     |
| `cone_addresses` | Number of IP addresses covered by the cone prefixes |

Using `data/asns.csv`, find the top 10 ASNs by `cone_asns`. Produce a summary table:

| Rank | ASN | Name | Country | Cone ASNs | Cone Addresses |
| ---- | --- | ---- | ------- | --------- | -------------- |
| 1    |     |      |         |           |                |
| ...  |     |      |         |           |                |

**Question**: What does a large customer cone imply about an ASN's role in the Internet? Why might `cone_addresses` be a more informative measure than `cone_asns` when comparing routing power across different networks?

---

### Step 3 (5pts) — What is the Lorenz curve? (GDP baseline)

The **Lorenz curve** visualizes the inequality of a distribution. Sort all units (countries, ASNs, etc.) from smallest to largest by their share of some resource. Then plot:

- **x-axis**: cumulative fraction of units (0 = none, 1 = all)
- **y-axis**: cumulative fraction of total resource held by those units

A perfectly equal distribution produces a diagonal line (y = x). Any real distribution curves below it — the further below, the more unequal. The **Gini coefficient** summarizes this in a single number: 0 = perfect equality, 1 = one unit holds everything.

We start with **world GDP** — a familiar economic distribution — to build intuition before applying the same tool to Internet data.

Using `data/gdp.csv` (columns: `country_code`, `country_name`, `year`, `gdp_usd`):

1. Run the plotting script to generate the Lorenz curve:

```bash
uv run scripts/lorenz-plot.py data/gdp.csv \
    --value gdp_usd \
    --label "World GDP" \
    --title "Lorenz Curve: World GDP"
```

The script prints the Gini coefficient and displays the plot.

2. Inspect the plot. What fraction of global GDP do the richest 10% of countries hold? (Read from the chart: at x = 0.90, what is y? The richest 10% hold `1 - y` of total GDP.)

**Question**: What is the Gini coefficient for world GDP? What does the shape of the curve tell you about how evenly economic output is distributed across countries? Keep this Gini value — you will compare it to Internet routing inequality in later steps.

---

### Step 4 (5pts) — What is the Lorenz curve of a country's ASNs?

Now apply the same analysis to Internet routing. For a given country, each headquartered ASN controls a certain amount of IP address space through its customer cone (`cone_addresses`). We can ask: is routing power spread evenly across a country's ASNs, or concentrated in a few?

Using `data/asns.csv`:

1. Filter rows to ASNs headquartered in the **United States** (`country_iso == "US"`).
2. Drop rows where `cone_addresses` is missing or zero.
3. Save the filtered data to `data/asns_us.csv`.
4. Plot the Lorenz curve:

```bash
uv run scripts/lorenz-plot.py data/asns_us.csv \
    --value cone_addresses \
    --label "US ASNs (headquartered)" \
    --title "Lorenz Curve: US ASN Routing Power"
```

Record the Gini coefficient printed by the script.

**Question**: How concentrated is routing power among US-headquartered ASNs? Compare this Gini coefficient to the GDP Gini from Step 3 — is Internet routing more or less concentrated than economic output across countries? What does this imply about how many organizations control the majority of US Internet transit?

_Save `data/asns_us.csv` — you will use it in Step 5._

---

### Step 5 (5pts) — What is a country's customer cone?

A single country's ASNs do not act in isolation — through their customer relationships they collectively reach a much broader set of networks worldwide. The **country's customer cone** is the union of all customer cones of all ASNs headquartered in that country: every ASN reachable from any country-X ASN through customer links.

Using `data/asns.csv`:

1. Find the **top 10 US ASNs** by `cone_asns` (these cover the vast majority of the US customer cone).
2. For each of these 10 ASNs, note their `cone_asns` and `cone_addresses`.
3. Compute an **upper bound** on the US customer cone size: sum the `cone_asns` values for all US ASNs. Compare this to the cone of the single largest US ASN — what does the gap tell you about overlap?

Now compute the **actual US customer cone** using the ppdc-ases data. The true country cone is the union of every US ASN's individual customer cone:

1. Load `data/<date>.ppdc-ases.txt.bz2` — each line lists a cone AS followed by all ASes in its cone.
2. For each US ASN in `data/asns_us.csv`, look up its row in the ppdc-ases data and collect all ASNs listed in its cone.
3. Take the **union** of all collected sets — this is the US customer cone.
4. Look up each ASN in the union in `data/asns.csv` to retrieve `cone_addresses`; drop any not found or with zero addresses.
5. Save to `data/cone_us.csv`.
6. Plot both curves on one chart:

```bash
uv run scripts/lorenz-plot.py data/asns_us.csv data/cone_us.csv \
    --value cone_addresses \
    --labels "US headquartered" "US customer cone (approx.)" \
    --title "Lorenz Curve: US ASNs vs US Customer Cone"
```

**Question**: How do the two Gini coefficients compare? Is routing power more or less concentrated in the aggregate customer cone compared to just the US-headquartered ASNs? What does this tell you about the structure of networks downstream of US providers?

---

### Step 6 (5pts) — US vs China: what does the Lorenz curve reveal about Internet inequality?

Repeat Steps 4–5 for **China** (`country_iso == "CN"`), producing `data/asns_cn.csv` and `data/cone_cn.csv`.

Then create a four-line comparison chart:

```bash
uv run scripts/lorenz-plot.py \
    data/asns_us.csv data/cone_us.csv \
    data/asns_cn.csv data/cone_cn.csv \
    --value cone_addresses \
    --labels "US headquartered" "US customer cone" \
             "CN headquartered" "CN customer cone" \
    --title "Lorenz Curve: US vs China Internet Inequality"
```

Collect all Gini coefficients:

| Group                 | Gini coefficient |
| --------------------- | ---------------- |
| World GDP (Step 3)    |                  |
| US headquartered ASNs |                  |
| US customer cone      |                  |
| CN headquartered ASNs |                  |
| CN customer cone      |                  |

**Question**: Which country's Internet infrastructure is more concentrated? A higher Gini coefficient means a country's routing power is held by fewer ASNs — what does this imply about resilience and dependence on a small number of providers? How does Internet routing inequality in each country compare to the global economic inequality baseline from Step 3?

---

## Answer

_(Complete this section after finishing the analysis above.)_

What can the Lorenz curve of a country's customer cone tell about Internet inequality?

| Group            | Gini |
| ---------------- | ---- |
| World GDP        |      |
| US ASNs          |      |
| US customer cone |      |
| CN ASNs          |      |
| CN customer cone |      |

The Lorenz curve of a country's customer cone reveals \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_.

Comparing US and China: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_.

Compared to world GDP inequality (Gini = \_\_\_\_), Internet routing inequality is \_\_\_\_\_\_\_\_.

[Your interpretation here.]
