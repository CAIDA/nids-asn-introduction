# nids-asn-cone

This module will introduce you to the Internet's Autonomous System using real world Internet data.

### 1 Introduction

The goal of this assignment is to understand Autumous Systems, how they are used by organizations, and the ASN customer cone. Large transit provider networks have thousands of customers, and significantly more complex routing than small networks with only a few or no customers. In this assignment, you will become familiar with some Internet datasets that describe organization that operate ASNs and ASN's customer cone provided by CAIDA. We will use this to become
familair and use such datasets to explore business relationships that underlie the interconnection topology. Specifically, you will explore the following two datasets:

- **AS Organization** - Provides a list of organizations, their names, country, and the ASNs they have registered in the Internet Registries.
- **CAIDA AS Customer Cone and Relationships** — Provides an ASN's customer cone and the relationships between ASNs.

##### Optional Reading

- [Lecture: AS Relationships and Customer Cones](https://cseweb.ucsd.edu/classes/wi23/cse291-e/slides/cse291e-lecture-03.pdf) (slides)
- [Autonomous Systems Topology](https://www.caida.org/catalog/media/2016_as_intro_topology_wind/as_intro_topology_wind.pdf) (slides)
- [On the Importance of Being an AS: An Approach to Country-Level AS Rankings](https://catalog.caida.org/paper/2023_on_importance_being_as) (paper)

### 2 Setup

If you have a problem using the python script the following setup will install uv and provide the libraries the script needs.

```
### Install the Python manager uv
curl -LsSf https://astral.sh/uv/install.sh | sh

### Install dependencies
uv sync
```

### 3 AS Organizations (4pts)

<img width="40%" style="float:right;margin-right:2em;" src="images/asn-org.png">

#### 3.1 Background

CAIDA uses WHOIS information available from Regional and National Internet Registries to infer a mapping from AS numbers to the organizational entities that operate them. In this section you will learn to parse the CAIDA's AS Organizations dataset and analyze the parsed result.

In this module, we will be using an organization's visibility in **Border Gateway Protocol (BGP)** routing. BGP is the standardized exterior gateway protocol designed to exchange routing and reachability information among **autonomous systems (AS)** on the Internet, determining the most efficient paths for data to travel.

An AS is an independently operated network on the Internet — a collection of IP prefixes managed by a single administrative entity under a common routing policy. Each AS is identified by a globally unique **Autonomous System Number (ASN)**.

An ASN is assigned to a network, not directly to a legal entity. One organization may operate multiple ASNs (for example, to represent different geographic regions or service tiers), and in rare cases an ASN may be shared between affiliated entities.

Organizations own multiple ASNs, for purposes of this assignment we will call this the organization's size.

##### Additional Reading:

- [ASN 2 Organization](https://catalog.caida.org/dataset/as_organizations)
- [Autonomous system (Internet)](<https://en.wikipedia.org/wiki/Autonomous_system_(Internet)>) (Wikipedia)

#### 3.2 Data Access (AS Organization)

The CAIDA AS Organizations data set can be accessed at the API.
We have provide [scripts/orgs-download.py](scripts/orgs-download.py) to download the full set of organizations for you.

```
nids-asn-introduction
├- scripts/orgs-download.py
├- data/orgs.jsonl               # you will download
├- scripts/org-table-fields.py   # you will write
└- tables/orgs-table-fields.md     # above script will create
```

- API: https://api.data.caida.org/as2org/v1/orgs/
- script: [scripts/orgs-download.py](scripts/orgs-download.py) will download the full set of organizations<br/>
  `uv run scripts/orgs-download.py --output data/orgs.jsonl`

#### 3.3 Understanding ASN Organization Data

Your job is to write `scripts/org-table-fields.py` to create the table below and fill
in the values column. This should give you an understanding of the values in the dataset.

`uv run scripts/org-table-fields.py --output tables/org-table-fields.md data/orgs.jsonl`

| name    | type     | values                      | description                                     |
| ------- | -------- | --------------------------- | ----------------------------------------------- |
| score   | int      | 1..120793                   | score of "important", used to sort (min..max)   |
| orgId   | string   | (number unique)             | oblique Id (number of unique ids)               |
| orgName | string   | (number unique)             | organization name (number of unique)            |
| country | string   | (number unique)             | organization's head quarter (number of codes)   |
| source  | string   | (number unique)             | Internet Registery source (number of regisries) |
| members | [string] | (min)..(max)                | list of member ASNs (min..max)                  |
| changed | date     | 1991/06/12 <br/> 2026/04/01 | last time the information was changed in WHOIS  |
| date    | date     | 2026/04/01 <br/> 2026/04/01 | current record date                             |
| ts      | date     | 2026/04/17 <br/> 2026/04/17 | database record timestamp                       |

**number of organizations**: (number of organizations)<br/>
**number of ASNs**: (number of unique ASNs)<br/>
**sources**: list of Internet Registry

### 4 AS Customer Cone

#### 4.1 Background

<img width="40%" style="float:left;margin-right:2em;" src="images/customer-cones.png">

| asn   | cone      | asn   | cone |
| ----- | --------- | ----- | ---- |
| **A** | A B C D E | **E** | E    |
| **B** | B D       | **F** | F G  |
| **C** | C E D     | **G** | G    |
| **D** | D         |

The customer cone is a metric used to gauge the size and influence of an AS within the global routing system. It represents the complete set of ASes, IPv4 prefixes, or IPv4 addresses that can be reached from a given AS by following only provider-to-customer links.

We define an AS A's AS customer cone as the AS A itself plus all the ASes that can be reached from A by following only p2c links in BGP paths we observed. In other words, A's customer cone contains A, plus A's customers, plus its customers' customers, and so on.

Each AS announces a set of IPv4 prefixes. Each IPv4 prefix represents a set of contiguous IPv4 addresses which are routed as a unit. Prefixes can be nested, with the most specific prefix used for routing over less specific prefixes. To find the set of prefixes which are reachable in AS A's IPv4 prefix customer cone create the union of prefixe announced by all ASes found in AS A's AS customer cone. AS A's IPv4 address customer cone is the set of addresses covered by AS A's IPv4 prefix customer cone. Prefixes overlap, which represent a set of IPv4 addresses.

The size of the customer cone of an AS reflects the number of other elements (ASes, IPv4 prefixes, or IPv4 addresses) found in it's set. An AS in the customer cone is assumed to pay, directly or indirectly, for transit, and provides a coarse metric of the size or influence of an AS in the routing system.

#### 4.2 Data Access (Customer Cone)

You will need to download CAIDA's AS Customer Cone data downloaded directly.

```
nids-asn-introduction
├- data/20260501.ppdc-asses.txt.bz2      # you will download
├- scripts/asn-customer-cone-classes.py  # you will write
└- tables/asn-customer-cone-classes.md   # above script will create
```

**CAIDA AS Customer Cone (Serial-1)** — Provides

- download `https://catalog.caida.org/dataset/as_relationships_serial_1`
  - [20260501.ppdc-ases.txt.bz2](https://publicdata.caida.org/datasets/as-relationships/serial-1/20260501.ppdc-ases.txt.bz2) : Per-AS provider-peer-customer (PPDC) cones: for each AS, the set of all ASes reachable via customer links.

Each line in the Per AS Provider Peer Customer (PPDC) cone file is a comment if it start with `#` or starts with a single ASN followed by the ASN in it's customer cone.

```
# This is a comment
# 23's customer cone size is 3 and includes (23,4,1)
23 23 4 1
# 1's customer cone size is 1 and includes only itself
1 1
```

#### 4.3 Understanding ASN Organization Data

Your job is to write `scripts/asn-customer-cone-classes.py`
and fill in the number of ASes in each class in the table below.

```bash
uv run scripts/asn-customer-cone-classes.py --output tables/asn-customer-cone-classes.md data/20260501-ppdc-ases.txt.bz2
```

| type           | range           | number of ASNs |
| -------------- | --------------- | -------------- |
| stub           | 1               | ??? (??.?%)    |
| transit small  | 2..10           | ??? (??.?%)    |
| transit middle | 11..1000        | ??? (??.?%)    |
| transit large  | 1001..(maximum) | ??? (??.?%)    |

### 5 Country Prevenace at each layer of the Internet

In this last section, we will be combining to the two datasets to
understand something about how different countries are seen
through the customer cone.

```
nids-asn-introduction
├- scripts/country-stats.py # you will write
└- tables/country-stats.md  # above script will write
```

`uv run scripts/country-stats.py --output tables/country-stats.md -O data/orgs.jsonl -C data/20260501.ppdf-ases.txt.bz2`

| column | description                                                |
| ------ | ---------------------------------------------------------- |
| name   | country name                                               |
| range  | the country's ASN's mininum and maximum customer cone size |
| total  | total number of ASNs in the country                        |
| stub   | total number of stub ASNs in the country                   |
| small  | total number of small transit ASNs in the country          |
| middle | total number of middle transit ASNs in the country         |
| large  | total number of large transit ASNs in the country          |

Provide the top 5 Countries sorted by the number of large transit ASNs.

| name          | range                    | stub    | small | middle | large |
| ------------- | ------------------------ | ------- | ----- | ------ | ----- |
| United States | `(minimum)`..`(maximum)` | (total) | ???   | ???    | ???   |
