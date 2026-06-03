[README](README..md) | [Background](Background.md) ⬅ Datasets ⮕  [Tasks](Tasks.md)

# Datasets

```
data
├- orgs.jsonl
└- 20260501.ppdc-ases.txt.bz2
```

### step 1: Download CAIDA AS to Organization Mapping

We have provided `scripts/org-download.py ` to download the dataset from CAIDA's as2org API.
It will place the data in your data directory as `data/orgs.jsonl`.

- API: https://api.data.caida.org/as2org/v1/orgs/
- script: [scripts/org-download.py ](scripts/org-download.py) will download the full set of organizations

**command:** `uv run scripts/org-download.py  --output data/orgs.jsonl`

### step 2: Download CAIDA AS Customer Cone

Manually download the May 1, 2026 AS Customer Cone file.

- [20260501.ppdc-ases.txt.bz2](https://publicdata.caida.org/datasets/as-relationships/serial-1/20260501.ppdc-ases.txt.bz2)
  : Per-AS provider-peer-customer (PPDC) cones: for each AS, the set of all ASes reachable via customer links.

**command**: `wget -O data/20260501.ppdc-ases.txt.bz2 https://publicdata.caida.org/datasets/as-relationships/serial-1/20260501.ppdc-ases.txt.bz2`

## CAIDA AS to Organization Mapping Dataset

CAIDA's AS-to-Organization-Mapping Dataset provides a list of organizations with ASNs and the set of ASNs assigned to those organizations. CAIDA infers these mappings based on [Regional Internet Registry](https://en.wikipedia.org/wiki/Regional_Internet_registry) [WHOIS records](https://en.wikipedia.org/wiki/WHOIS). CAIDA provides this data through an API that requires pagination to retrieve the full dataset. The provided script, [scripts/org-download.py ](scripts/org-download.py), handles this process automatically and stores the results in **data/orgs.jsonl**.

| name    | type     | values                      | description                                                                                                |
| ------- | -------- | --------------------------- | ---------------------------------------------------------------------------------------------------------- |
| score   | int      | 1..120793                   | organization sorting score (min..max)                                                                      |
| orgId   | string   | 96894                       | organization ID (number of unique IDs)                                                                     |
| orgName | string   | 91067                       | organization name (number of unique names)                                                                 |
| country | string   | 239                         | organization's headquarters country (number of unique codes)                                               |
| source  | string   | 7                           | Internet Registry source (number of registries)<br> AFRINIC, APNIC, APNIC,JPNIC, ARIN, JPNIC, LACNIC, RIPE |
| members | [string] | 1..1008                     | member ASNs (min..max list size)                                                                           |
| changed | date     | 1991/06/12 <br/> 2026/04/01 | last time the information was changed in WHOIS                                                             |
| date    | date     | 2026/04/01 <br/> 2026/04/01 | current record date                                                                                        |
| ts      | date     | 2026/04/17 <br/> 2026/04/17 | database record timestamp                                                                                  |

## AS Customer Cones

<img src="images/customer-cones.png">

The ASN customer cone is a metric used to gauge the size and influence of an Autonomous System (AS) within the global routing system. It represents the complete set of ASes that traffic can reach from a given AS by following only provider-to-customer (_p2c_) links.

We define an AS A's customer cone as:

- **AS A itself**
- **Plus all ASes reachable from A** by following only _p2c_ links in observed BGP paths.

In other words, an AS's customer cone contains itself, its customers, its customers' customers, and so on.

This construct embeds an assumption that ASes in the customer cone for AS A pay AS A—either directly or indirectly—for transit. We denote the **size** of an AS's customer cone as the **total number of ASNs in its customer cone set**, providing a coarse metric of that AS's footprint in the routing system.

### 6.1 Understanding ASN Customer Cones

You will download CAIDA's May 2026 ASN Customer Cone (_20260501.ppdc-ases.txt.bz2_) file to the data directory. You will then write a script (_scripts/asn-cone-classes.py_) that will divide the ASNs into bands based on their customer cone size.

CAIDA provides its ASN customer cone as part of the **CAIDA AS Customer Cone (Serial-1)** dataset. Follow the link below and download the file labeled **20260501.ppdc-ases.txt.bz2** and copy it to your **data** directory.

In the `ppdc-ases.txt.bz2` file, lines that start with a '#' are a comment. All other lines start with a single ASN followed by a list of ASNs in its customer cone.

```
# This is a comment
# 23's customer cone size is 3 and includes (23,4,1)
23 23 4 1
# 1's customer cone size is 1 and includes only itself
1 1
```
[README](README..md) | [Background](Background.md) ⬅ Datasets ⮕  [Tasks](Tasks.md)