[README](README.md) | [Introduction](Introduction.md) | [Datasets](Datasets.md) | Tasks ⮕ [Notebook](notebook.ipynb)

# Tasks

Complete the tasks below in order. Tasks 3 and 4 are completed inside [notebook.ipynb](notebook.ipynb) — replace the `# YOUR CODE HERE` sections with your code and answer the questions in the markdown cells that follow.

## Task 0: Set Up Your Environment

Install dependencies and verify your environment is ready. See [Setup](Setup.md) for full instructions.

- [ ] Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Install dependencies: `uv sync`

## Task 1: Download the Datasets

Download both datasets to your `data/` directory before opening the notebook. See [Datasets](Datasets.md) for details on each file.

- [ ] Download the AS-to-Organization mapping: `uv run scripts/org-download.py --output data/orgs.jsonl`
- [ ] Download the AS Customer Cone: `wget -O data/20260501.ppdc-ases.txt.bz2 https://publicdata.caida.org/datasets/as-relationships/serial-1/20260501.ppdc-ases.txt.bz2`

## Task 2: Start the Notebook

Launch Jupyter and open the notebook in your browser.

```bash
uv run jupyter notebook notebook.ipynb
```

If the browser does not open automatically, copy the URL printed in the terminal (e.g. `http://127.0.0.1:8888/...`) and paste it into your browser.

## Task 3: ASN Classified by Customer Cone Size

Parse the AS Customer Cone file and classify each ASN by cone size into tiers (edge, small transit, large transit, transit huge). The notebook writes the results to `tables/asn-cone-tiers.md`.

- [ ] Q1: What percentage of ASNs are edge ASes (cone size = 1)? What does this suggest about the structure of the Internet?
- [ ] Q2: How large is the maximum customer cone? What does this tell you about the most influential ASes?
- [ ] Q3: How do the proportions of edge, small transit, and large transit ASes compare? What does this reveal about the AS hierarchy?

## Task 4: ASN Tiers by Country

Join the customer cone tiers with the AS-to-Organization mapping to count tiers per country. The notebook writes the results to `tables/country-cone-tiers.md`.

- [ ] Q4: Which countries have the most transit huge ASNs? What does this tell you about where Internet infrastructure is concentrated?
- [ ] Q5: What proportion of all ASNs fall in the "other" category? What does this suggest about geographic distribution?
- [ ] Q6: Do the same countries dominate across all AS tiers? What patterns do you observe across the rows?

[README](README.md) | [Introduction](Introduction.md) | [Datasets](Datasets.md) | Tasks ⮕ [Notebook](notebook.ipynb)
