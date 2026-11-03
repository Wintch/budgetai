---
id: funding-links
title: "Funding button for a GitHub account: setup, platforms and Argentine tax notes (general)"
audience: helper
country: ""
region: ""
language: en
topics: [funding, donations]
sources:
  - {name: "GitHub Docs: Displaying a sponsor button in your repository (FUNDING.yml keys and limits)", url: "https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository", kind: official, read_on: 2026-11-03}
  - {name: "GitHub Docs: Creating a default community health file (account-level .github repository)", url: "https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file", kind: official, read_on: 2026-11-03}
  - {name: "GitHub Docs: Setting up GitHub Sponsors for your personal account", url: "https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/setting-up-github-sponsors-for-your-personal-account", kind: official, read_on: 2026-11-03}
  - {name: "GitHub Docs: About GitHub Sponsors (supported regions, fees)", url: "https://docs.github.com/en/sponsors/getting-started-with-github-sponsors/about-github-sponsors", kind: official, read_on: 2026-11-03}
  - {name: "Ley 24.977 (monotributo) arts. 3 and 20, text on ARCA library (about the first half of the page read)", url: "https://biblioteca.afip.gob.ar/dcp/LEY_C_024977_1998_06_03", kind: official, read_on: 2026-11-03}
  - {name: "La Nacion, 2025-04-14: taxes on inheritances and donations (a tax lawyer's view on donations received by individuals)", url: "https://www.lanacion.com.ar/propiedades/casas-y-departamentos/impuestos-sobre-herencias-y-donaciones-lo-que-hay-que-saber-nid09042025/", kind: press, read_on: 2026-11-03}
  - {name: "Memo: the resolution taxing influencer activity was repealed (RG 5607/2024 and RG 5612/2024)", url: "https://www.memo.com.ar/economia/arca-influencers/", kind: press, read_on: 2026-11-03}
as_of: 2026-11-03
expires: 2027-02-03
status: draft
licence: CC-BY-4.0
verified_by: ""
not_verified: ["how GitHub Sponsors payouts work for an Argentine creator (schedule, minimum, currency, fees on the payout side)", "tax treatment in Argentina of recurring sponsorships received by a monotributista (donation or payment for a service)", "the official text of RG 5607/2024 and RG 5612/2024 (press only)", "the Consejo Profesional (CPCECABA) note on content creators (page blocked to scripts; only a search summary seen)", "the second half of Ley 24.977 text"]
---

# Funding button for a GitHub account

How to put a support button on a GitHub account, what it takes to receive the money in Argentina, and what was found about the taxes. Method only: no one's handle, account or amount belongs in this page. A comparison of tipping platforms (Cafecito, Ko-fi, Patreon and others) is in `ARTIST_SUPPORT_PLATFORMS.md`.

> Information, not advice. Facts are tagged with where they were read (see `sources` above). What was not verified is listed at the end.

## Summary
- **One button for the whole account** is made with a public repository named `.github` that holds `FUNDING.yml`. It applies to every repository of the account without its own file. No per-repository files needed.
- **GitHub Sponsors** can pay out to Argentina (Argentina is on the supported-region list) and charges no fee on sponsorships from personal accounts.
- **Enrolment is done by the person** in their own GitHub account (2FA, Stripe Connect bank account, tax form W-8BEN, profile, approval).
- **Taxes are not settled by what was read.** Pure donations to individuals are described by press as outside IVA, Ganancias and Ingresos Brutos, but recurring sponsorship of someone who works independently may be read as payment for a service, and bank deposits must match declared income. Ask an accountant first (questions at the end).

## Checklist (in this order)
1. [ ] Decide which GitHub account is the public identity (the handle is public by design).
2. [ ] Ask the accountant the questions at the end of this page. It can run in parallel with step 3.
3. [ ] Enrol in GitHub Sponsors (see "Enrolling" below) and wait for approval (a few days).
4. [ ] Create the public repository `.github` in the account, with `.github/FUNDING.yml` holding `github: <username>`, in a commit of its own.
5. [ ] Open any repository of the account and check that the Sponsor button appears.
6. [ ] Make sure no personal data other than the public handle went into that repository.

## How the button works
- A file `.github/FUNDING.yml` on the default branch of a repository shows the Sponsor button on that repository (GitHub Docs). The same can be set in Settings > General > Features > Sponsorships.
- **Account default:** a **public** repository named `.github` in the account, with `FUNDING.yml` inside its `.github` folder, is used for every repository of the account that has no `FUNDING.yml` of its own. A repository's own file wins.
- **Keys:** `github: USERNAME` (one organisation and up to four developers per file), `ko_fi`, `liberapay`, `patreon`, `buy_me_a_coffee`, `open_collective`, `polar`, and others; `custom: [URL, ...]` for anything else (up to four URLs; a URL containing `:` must be in quotes). A platform with no key of its own, such as Cafecito, goes in `custom`.
- One username per external platform.
- The file lives in git history for good: a handle added and then removed stays in old commits.
- Without GitHub, a funding link is only a link: a line in the README.

## Enrolling in GitHub Sponsors (done by the person, not by a script)
1. Enable 2FA on the account.
2. Open github.com/sponsors and choose "Get sponsored" for the personal account; fill in the contact details.
3. Choose the payout method: **a bank account through Stripe Connect** (the region of residence must match the bank account's region) or a **fiscal host** (only choosable at sign-up; changing it later means contacting support).
4. Check name and date of birth before submitting: changing identity data after submitting is hard.
5. Submit the tax form: W-9 for US residents or non-resident US citizens, **W-8BEN for everyone else**. It is found in the dashboard under Overview, "tax forms".
6. Accept the terms and the privacy statement and submit. GitHub reviews the application.
7. Complete the profile (short bio and what the work is, optionally up to six featured repositories), then "Request approval". Review takes a few days. After approval the profile goes live.
- **Eligibility:** whoever contributes to an open-source project (not only code) and lives in a supported region. Argentina is listed (GitHub Docs, read 2026-11-03).
- **Fees:** none on sponsorships from personal accounts; up to 6% on those from organisations (3% card processing plus 3% GitHub service, the card part avoidable with invoiced billing).
- **Not read:** payout schedule, minimum amount and payout currency (the pages say payment timing is in the Sponsors Additional Terms).

## What to weigh
1. **Privacy.** A funding link identifies the person. A repository meant to carry no personal data carries no funding link; put the button only where the person is happy to be identified.
2. **Availability.** Not every platform pays out in every country (see `ARTIST_SUPPORT_PLATFORMS.md`).
3. **Cost.** Platform fee plus processor fee plus the cost of moving the money.
4. **Size.** Support is usually small and slow: do not count on it for an urgent bill.
5. **Agreements.** If the code is published under a work arrangement, check that the other side allows a funding link.
6. **Taxes.** See the next section.

## Argentina: what was found about taxes on money received this way
- **Monotributo income is sales, leases or services.** Ley 24.977 art. 3: "ingresos brutos" is the proceeds of sales, leases or services done on one's own or another's account. A pure donation is not named there (in the part of the text read).
- **Bank deposits are checked.** Art. 20 (Ley 27.743 text) lists as exclusion causes that personal spending or bank deposits are incompatible with declared income and not justified. Money from sponsors lands in an account and counts as a deposit.
- **Press view of a pure donation.** A tax lawyer quoted by La Nacion (2025-04-14): donations received by individuals are not covered by IVA, Ganancias or Ingresos Brutos; received by a sole proprietorship they are covered by Ganancias.
- **Habitual contributions.** A search summary of a professional-council note says pure donations are exempt but habitual contributions inside a content creator's activity may be read differently. The note itself was not readable here.
- **Content-creator activity code.** Press reports that RG 5607/2024 (an activity code for online content creation) was repealed by RG 5612/2024. Neither official text was read.
- **Inference, not a source:** a sponsorship that comes with rewards, deliveries or a regular counterpart looks more like payment for a service than a pure donation, which would change how it is counted.

## Questions for an accountant
1. Does recurring sponsorship received through a platform count as monotributo income, or as a donation, in my case?
2. How do I document the origin of these deposits so they are not read as unexplained?
3. Does the answer change by province?
4. Does it count toward my category cap?
5. Do I declare it differently if it comes from abroad (dollars)?

## Not verified
- How GitHub Sponsors pays an Argentine creator: schedule, minimum, currency, payout-side fees.
- The tax treatment of recurring sponsorships for a monotributista.
- The official texts of RG 5607/2024 and RG 5612/2024 (press only).
- The professional-council note on content creators (only a search summary seen).
- The second half of the text of Ley 24.977.
