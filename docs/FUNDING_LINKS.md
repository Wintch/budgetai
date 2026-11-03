---
id: funding-links
title: "Funding links and git (general)"
audience: helper
country: ""
region: ""
language: en
topics: [funding, donations]
sources: []
as_of: 2026-10-20
expires: 2027-04-18
status: draft
licence: CC-BY-4.0
verified_by: ""
not_verified: ["see the Not verified section of the page"]
---

# Funding links and git (general)

How donations connect to a git repository, and what to weigh first. Method only: no one's handle or account belongs in this repo.

## How it links
- **GitHub:** a file `.github/FUNDING.yml` on the default branch shows a Sponsor button on the repository. The `github:` key lists sponsored accounts (docs: one organization
  and up to four developers). The same button can be set in Settings > General > Features > Sponsorships. A `.github` repository in an account or organization can hold a default file for all
  its repositories. Other keys exist for other platforms and for a custom link (general knowledge, check the docs).
- **Other hosts and platforms:** a funding link is only a link; without GitHub the same is done with a line in the README. A tip platform is linked by its URL.
- The file lives in git history forever: a handle added then removed stays in old commits.

## What to weigh
1. **Privacy.** A funding link identifies the person. If a repo is meant to carry no personal data, it carries no funding link.
2. **Where it is available.** Not every platform pays out in every country; check eligibility and the payout method.
3. **Cost.** Platform commission plus the payment processor's fee, and the cost of moving the money.
4. **Size.** Donations are usually small and slow; do not count on them for an urgent bill.
5. **Taxes.** Received money may count as income; for a simplified tax regime, income ceilings may apply. Ask an accountant.
6. **Agreements.** If the code is published under a work arrangement, check whether the other side allows funding links.

## Order
Decide the repo and the identity first, then the platform, then add the file in a commit of its own so it is easy to undo.
