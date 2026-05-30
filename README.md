# How the Internet assigns and uses Autonomous Systems (ASes)

### 1 Learning Objectives

The goal of this assignment is to understand Autonomous Systems, how organizations use them, and the concept of an AS's *customer cone* by processing data sets that describe how ASNs are globally distributed across networks and countries. 

### 2 Introduction

Large transit provider networks have thousands of customers, and significantly more complex routing than small networks with only a few or no customers. In this assignment, you will use Internet datasets that describe networks that operate ASNs to connect to other networks.  This assignment will introduce you to such data sets, and how analysts use them to infer *customer cones*, a metrics that describe a network's interconnection relationship to the rest of the Internet.   Computing this metric requires inferring business relationships that underlie the interconnection topology. 

For this assignment, you will explore the following two datasets:

- **AS to Organization** - Provides a list of organizations, their names, country, and the ASNs they have registered in the Internet Registries. @@BRAD link to data set page 
- **CAIDA AS Customer Cone and Relationships** — Provides an ASN's customer cone and the relationships between ASNs. @@BRAD link to data set page  (i don't think it has customer cone in the data set?) 

##### Optional Reading

- [Lecture: AS Relationships and Customer Cones](https://cseweb.ucsd.edu/classes/wi23/cse291-e/slides/cse291e-lecture-03.pdf) (slides)
- [Autonomous Systems Topology](https://www.caida.org/catalog/media/2016_as_intro_topology_wind/as_intro_topology_wind.pdf) (slides)
- [On the Importance of Being an AS: An Approach to Country-Level AS Rankings](https://catalog.caida.org/paper/2023_on_importance_being_as) (paper)
- [ASN 2 Organization](https://catalog.caida.org/dataset/as_organizations)
- [Autonomous system (Internet)](<https://en.wikipedia.org/wiki/Autonomous_system_(Internet)>) (Wikipedia)

### 2 Setup

If you have a problem using the python script the following setup will install uv and provide the libraries the script needs.  @@BRAD: what python script?  this is coming out of nowhere. need a list of required software and packages they need on laptop, or accounts where they go to do this if they don't have them.    why is this coming before they have the background section?   also you can't ask them to install sofwtare without explaining why they are installing it... 


```
### Install the Python manager uv
curl -LsSf https://astral.sh/uv/install.sh | sh

### Install dependencies
uv sync
```

### 3 Background on Autonomous Systems and "Organizations" that operate them. 

<img width="40%" style="float:right;margin-right:2em;" src="images/asn-org.png">

An Autonomous System (or AS) is an independently operated network on the Internet — a collection of IP prefixes managed by a single administrative entity under a common routing policy. Each AS is identified by a globally unique **Autonomous System Number (ASN)**.  Regional Internet Registries (RIRs), set up in the 1990s, allocates these numbers to organizations that operate network infrastructure.   One organization may operate multiple ASNs, for example, to operate separate networks in different geographic regions or service tiers. 

CAIDA uses WHOIS information available from Regional and National Internet Registries to infer a mapping from AS numbers to the organizations that operate them. In this section you will learn to parse CAIDA's *AS to Organizations* dataset to analyze properties of this global numbering system. 

In this module, we will be using an organization's visibility in the **Border Gateway Protocol (BGP)** routing. BGP is the standardized inter-network routing protocol designed to exchange routing and reachability information among **autonomous systems (AS)** on the Internet, determining the most efficient paths for data to travel.  @@BRAD are they using that data in this module, or is that the next module?) 


### 4 Data Access (AS Organization)

The CAIDA AS Organizations data set can be accessed at the API.
We have provide [scripts/orgs-download.py](scripts/orgs-download.py) to download the full set of organizations for you.  @@BRAD: what is this: it says API and theen 'download the full set'.  which is it? i thought we were having them download the entire file?   

```
nids-asn-introduction
├- scripts/orgs-download.py
├- data/orgs.jsonl               # you will download
├- scripts/org-table-fields.py   # you will write   @@BRAD do you mean modify?
└- tables/orgs-table-fields.md     # you will modify the above script to create this output file 
```

- API: https://api.data.caida.org/as2org/v1/orgs/
- script: [scripts/orgs-download.py](scripts/orgs-download.py) will download the full set of organizations<br/>
  `uv run scripts/orgs-download.py --output data/orgs.jsonl`

### 5 Understanding ASN Organization Data

Your assignment is to create the output file `scripts/org-table-fields.py`
to contain the table below, and fill in the values column. This should
give you an understanding of the values in the dataset.

`uv run scripts/org-table-fields.py --output tables/org-table-fields.md data/orgs.jsonl`

| name    | type     | values                      | description                                     |
| ------- | -------- | --------------------------- | ----------------------------------------------- |
| score   | int      | 1..120793                   | @@BRAD FIX: what is it?used to sort (min..max)   |
| orgId   | string   | (number unique)             | @@BRAD oblique Id (number of unique ids)               |
| orgName | string   | (number unique)             | number of unique organization names in file    |
| country | string   | (number unique)             | number of unique countries identified as HQs   |
| source  | string   | (number unique)             | number of unique Internet Registery sources |
| members | [string] | (min)..(max)                | @@BRAD list of member ASNs (min..max)                  |
| changed | date     | 1991/06/12 <br/> 2026/04/01 | last time the information changed in WHOIS  |
| date    | date     | 2026/04/01 <br/> 2026/04/01 | current record date                             |
| ts      | date     | 2026/04/17 <br/> 2026/04/17 | database record timestamp                       |

**number of organizations**: (number of organizations)<br/>
**number of ASNs**: (number of unique ASNs)<br/>
**sources**: list of Internet Registry

### 6 AS Customer Cones

<img width="40%" style="float:left;margin-right:2em;" src="images/customer-cones.png">

| asn   | cone      | asn   | cone |
| ----- | --------- | ----- | ---- |
| **A** | A B C D E | **E** | E    |
| **B** | B D       | **F** | F G  |
| **C** | C E D     | **G** | G    |
| **D** | D         |

The customer cone is a metric to gauge the size and influence of an AS within the global routing system. It represents the complete set of ASes (or IPv4 prefixes, or IPv4 addresses) that traffic can reach from a given AS by following only provider-to-customer (*p2c*) links.   We define an AS A's *AS-level customer cone* as the AS A itself, plus all the ASes that can be reached from A by following only p2c links in BGP paths we observed. In other words, A's customer cone contains A, plus A's customers, plus its customers' customers, and so on.
This construct embeds an assumption that ASes in the customer cone for AS A pay that AS A, directly or indirectly, for transit; it provides a coarse metric of the size or influence of AS A in the routing system.

Each AS announces a set of IPv4 prefixes. Each IPv4 prefix represents a set of contiguous IPv4 addresses that are routed as a unit. Prefixes can be nested, with the most specific prefix taking precedence for routing decisions. To find the set of prefixes reachable in AS A's IPv4 *prefix-level customer cone*, create the union of prefixes announced by all ASes found in AS A's *AS-level customer cone*. AS A's *IPv4-address-level customer cone* is the set of addresses covered by AS A's IPv4 prefix customer cone. 

We will denote the *size* of the customer cone of an AS to represent the number of other elements (ASes, IPv4 prefixes, or IPv4 addresses, depending on the cone granularity) found in its cone set. 

#### 4.2 Data Access (Customer Cone)

You will need to download CAIDA's AS Customer Cone data:  @@BRAD need more instruction here.   

```
nids-asn-introduction
├- data/20260501.ppdc-asses.txt.bz2      # you will download
├- scripts/asn-customer-cone-classes.py  # you will write
└- tables/asn-customer-cone-classes.md   # above script will create
```

**CAIDA AS Customer Cone (Serial-1)** — Provides  @@BRAD provides what? need more instruction here.   

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

In this last section, you will combine the two datasets to understand 
how ASes are distributed across countries. 

```
nids-asn-introduction
├- scripts/country-stats.py # you will write
└- tables/country-stats.md  # above script will write
```

`uv run scripts/country-stats.py --output tables/country-stats.md -O data/orgs.jsonl -C data/20260501.ppdf-ases.txt.bz2`

| column | description                                                |
| ------ | ---------------------------------------------------------- |
| name   | country name                                               |
| range  | the country's ASN's minimum and maximum customer cone size |
| total  | total number of ASNs in the country                        |
| stub   | total number of stub ASNs in the country                   |
| small  | total number of small transit ASNs in the country          |
| middle | total number of middle transit ASNs in the country         |
| large  | total number of large transit ASNs in the country          |

Provide the top 5 Countries sorted by the number of large transit ASNs.

| name          | range                    | stub    | small | middle | large |
| ------------- | ------------------------ | ------- | ----- | ------ | ----- |
| United States | `(minimum)`..`(maximum)` | (total) | ???   | ???    | ???   |
