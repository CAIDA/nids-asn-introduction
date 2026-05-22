# Report: Internet Inequality and ASN Customer Cones

## Student Information

- Name:
- Date:

## Research Question

What can the Lorenz curve of a country's customer cone tell about Internet inequality?

## Step 1 — What is an ASN, and how does it relate to an organization?

Write 2-4 sentences explaining what an Autonomous System Number (ASN) is and how it maps to a real organization such as an ISP, cloud provider, university, or company.

Answer:

## Step 2 — What is the ASN customer cone?

Explain, in your own words:

- what a provider-customer relationship means,
- what a peer-to-peer relationship means, and
- why customer cones include customer links but not peer links.

Then explain what a large customer cone suggests about an AS's role in Internet routing.

Answer:

## Step 3 — Lorenz Curve of World GDP

Plot:

![World GDP Lorenz curve placeholder](plots/world-gdp-lorenz.png)

_Replace this placeholder path with your saved Step 3 plot if you use a different filename._

Record the Gini coefficient from your GDP Lorenz curve:

- World GDP Gini:

Interpretation:

What does this Lorenz curve show about how evenly or unevenly GDP is distributed across countries?

Answer:

## Step 4 — Lorenz Curve of US-Headquartered ASNs

Plot:

![US headquartered ASN Lorenz curve placeholder](plots/us-asns-lorenz.png)

_Replace this placeholder path with your saved Step 4 plot if you use a different filename._

Record the Gini coefficient from the US ASN Lorenz curve:

- US headquartered ASN Gini:

Question:

How concentrated is routing power among US-headquartered ASNs? Compare this Gini coefficient to the GDP Gini from Step 3. Is Internet routing more or less concentrated than economic output across countries? What does this imply about how many organizations control the majority of US Internet transit?

Answer:

## Step 5 — Lorenz Curve of the US Customer Cone

Plot:

![US headquartered vs customer cone Lorenz curve placeholder](plots/us-cone-comparison-lorenz.png)

_Replace this placeholder path with your saved Step 5 plot if you use a different filename._

Record the values you computed while building the US customer cone:

- Top 10 US ASNs by `cone_asns`:
- Upper bound from summing all US `cone_asns`:
- Actual US customer cone size from ppdc union:
- US customer cone Gini:

Question:

How do the two Gini coefficients compare? Is routing power more or less concentrated in the aggregate customer cone compared to just the US-headquartered ASNs? What does this tell you about the structure of networks downstream of US providers?

Answer:

## Step 6 — US vs China

Plot:

![US vs China Lorenz curve placeholder](plots/us-vs-cn-lorenz.png)

_Replace this placeholder path with your saved Step 6 plot if you use a different filename._

Record the Gini coefficients for all groups:

| Group                 | Gini coefficient |
| --------------------- | ---------------- |
| World GDP (Step 3)    |                  |
| US headquartered ASNs |                  |
| US customer cone      |                  |
| CN headquartered ASNs |                  |
| CN customer cone      |                  |

Question:

Which country's Internet infrastructure is more concentrated? A higher Gini coefficient means a country's routing power is held by fewer ASNs. What does this imply about resilience and dependence on a small number of providers? How does Internet routing inequality in each country compare to the global economic inequality baseline from Step 3?

Answer:

## Final Conclusion

Return to the main research question:

What can the Lorenz curve of a country's customer cone tell about Internet inequality?

Complete the statements below.

- The Lorenz curve of a country's customer cone reveals:
- Comparing the US and China:
- Compared to world GDP inequality, Internet routing inequality is:

Final interpretation:
