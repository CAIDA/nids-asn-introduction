README ⮕ | [Introduction](Introduction.md) | [Datasets](Datasets.md) | [Tasks](Tasks.md) | [Notebook](nids-asn-introduction.ipynb)

# How the Internet assigns and uses Autonomous Systems (ASes)

## Learning Objectives

The goal of this assignment is to understand Autonomous Systems, how organizations use them, and the concept of an AS's _customer cone_ by processing data sets that describe how ASNs are globally distributed across networks and countries. This assignment is a building block for studying the macroscopic topology of the Internet.

## Overview

Start by reading **Introduction** to get the background needed to understand the assignment. **Setup** helps you set up your environment. **Datasets** explains each dataset and how to download it.

- step 1 [read the introduction](Introduction.md)
- step 2 [read dataset overviews](Datasets.md)
- step 3 [review the tasks](Tasks.md)
- step 4 log into NRP's JuypterHub, upload and complete the nids-asn-introduction.ipynb
  - complete each task by replacing the `# YOUR CODE HERE` sections
  - answer all six questions
- step 5 download your working version and save to nids-asn-introduction-(username).ipynb ⬅ deliverable

### Directory Structure

```
nids-asn-introduction
├- Introduction.md                     # Introduction and background
├- Datasets.md                         # Dataset overview and download instructions
├- Tasks.md                            # Task checklist and instructions
├- nids-asn-introduction.ipynb     ⬅  # Complete
```

### Glossary

- **AS (Autonomous System)**: An independently operated network on the Internet, identified by a globally unique ASN, that manages its own routing policy.
- **ASN (Autonomous System Number)**: A unique number assigned to an AS by a Regional Internet Registry, used to identify the AS in global routing protocols.
- **Customer cone**: The set of all ASes reachable from a given AS by following only provider-to-customer links. It is used as a metric of an AS's size and influence in the routing system.
- **Provider-Customer relationship**: A business relationship in which a customer AS pays a provider AS for Internet transit — access to the rest of the Internet.
- **RIR (Regional Internet Registry)**: An organization that manages and allocates Internet number resources (IP addresses and ASNs) within a geographic region. The five RIRs are ARIN, RIPE NCC, APNIC, LACNIC, and AFRINIC.
- **WHOIS**: A query protocol used to look up registration records for Internet resources such as IP addresses, ASNs, and domain names.

README ⮕ | [Introduction](Introduction.md) | [Datasets](Datasets.md) | [Tasks](Tasks.md) | [Notebook](nids-asn-introduction.ipynb)
