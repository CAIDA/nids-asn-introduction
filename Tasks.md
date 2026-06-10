[README](README.md) | [Introduction](Introduction.md) | [Datasets](Datasets.md) | Tasks ⮕ [Notebook](nids-asn-introduction.ipynb)

# Tasks

Complete the tasks below in order. Tasks 2 and 3 are completed inside [nids-asn-introduction.ipynb](nids-asn-introduction.ipynb) — replace the `# YOUR CODE HERE` sections with your code and answer the questions in the markdown cells that follow.

## Task 1: Get access to NRP's JuypterHub and run the notebook there.

- step 1. [https://nrp.ai](https://nrp.ai/)
- step 2. click on "Log In" in the upper right corner
- step 3. select your organization and log in
- step 4. Send an email to (address) with the email address you used to log into NRP.
  - We will add that address to the namespace `caida-nids`
- step 5. Log into NRP's JuypterHub [https://jupyterhub-west.nrp-nautilus.io/](https://jupyterhub-west.nrp-nautilus.io/)
- Step 6. Upload nids-asn-introuction.ipynb and run it

## Task 2: ASN Classified by Customer Cone Size

Parse the AS Customer Cone file and classify each ASN by cone size into tiers (edge, transit small, transit middle, transit large, transit huge). The notebook writes the results to `tables/asn-cone-tiers.md`.

- [ ] Q1: What percentage of ASNs are edge ASes (cone size = 1)? What does this suggest about the structure of the Internet?
- [ ] Q2: How large is the maximum customer cone? What does this tell you about the most influential ASes on the Internet?
- [ ] Q3: How do the proportions of edge, small transit, and large transit ASes compare? What does this distribution reveal about how ASes are organized hierarchically?

## Task 3: ASN Tiers by Country

Join the customer cone tiers with the AS-to-Organization mapping to count tiers per country.

- [ ] Q4: Which countries have the most transit huge ASNs? What does this tell you about where Internet infrastructure is concentrated?
- [ ] Q5: What proportion of all ASNs fall in the "other" category? What does this suggest about the geographic distribution of the global Internet?
- [ ] Q6: Do the same countries dominate across all AS tiers (edge, transit small, transit huge)? What patterns do you observe across the rows?

[README](README.md) | [Introduction](Introduction.md) | [Datasets](Datasets.md) | Tasks ⮕ [Notebook](nids-asn-introduction.ipynb)
