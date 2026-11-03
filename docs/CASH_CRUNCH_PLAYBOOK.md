---
id: cash-crunch-playbook
title: "Cash-crunch playbook (general)"
audience: person
country: AR
region: ""
language: en
topics: [cash-crunch, debt, utilities, priorities]
sources: []
as_of: 2026-10-20
expires: 2027-04-18
status: draft
licence: CC-BY-4.0
verified_by: ""
not_verified: ["see the Not verified section of the page"]
---

# Cash-crunch playbook (general)

For a self-employed person who has several bills due close together and little cash. It holds method only. The real numbers, names and
dates of any one person stay in a private ledger that is never committed (see `AGENTS.md`).

Not legal or financial advice. Rules about late fees, evictions, payment plans and permits differ by place; check them locally.

## 1. See everything at once

List each item with: due date, amount, **what happens if it is late**. Add the total and the days left.
Order by consequence, not by date: a service cut or an eviction notice outranks a tax that only adds interest.

## 2. Stop recurring costs first

A fixed monthly fee is paid again every month, so cutting it is the surest saving. Cancel what free tiers or home equipment can replace.
See `CANCEL_GUIDE.md` for how to cancel and verify.

## 3. Talk before the due date

- Utilities and tax offices usually have payment plans for arrears. Ask what stops a cut or a penalty.
- A landlord is easier to deal with early: propose a date or two partial payments, and send it in writing.
- Get every agreement in writing, with dates. Do not rely on a handshake.

## 4. Cheapest money first

1. Money already owed to you: chase pending invoices; offer small extra jobs to past clients, with a rate and a date.
2. People who offered help: ask for a fixed sum and a repayment date. This usually costs less than an overdraft or a credit card.
3. Things you do not use: sell them. Compare **sold** or many active listings with filters (condition, place); asking prices run high.
   Sell what is not needed for work or moving around before what is.
4. Overdraft and cards last, and only for a short, known gap. Check the real rate first.

## 5. Quotes for repairs or works

- Decide **who pays** before comparing prices. The owner pays for the owner's property unless a written agreement says otherwise.
- Safety comes before price when something may fall or fail. Ask for a professional's opinion in writing.
- A quote should say: labour and materials separately, time to finish, guarantee, who removes the debris, what is not included.
- Ask whether a permit and a professional in charge are required. Get two or three quotes.
- Ask what happens to the rent and the contract during the works, and who covers damage.

## 6. Contracts

Read the new text before signing, in a separate sitting from other negotiations. Works and rent terms go into the contract or an attached
note, with dates.

## 7. Keep a private ledger

Dates, amounts, people and decisions go in a file that is git-ignored. Only the method (this file) is tracked. Update it as numbers arrive, and
mark what is calculated versus what was said.

## 8. Reviewing a telecom or ISP bill

- Read it line by line and add it up. Bills often carry services you forgot (a landline, a second line, a public IP).
- **Discounts expire.** A "x 6 months" or "x 12 months" discount means the real price is the list price. Find the start and end dates and
  compute the bill without the discounts: it can be several times higher.
- List prices usually rise every month; compare two bills.
- Bundle bonuses may disappear if you drop one of the services.
- Check for a minimum term and an early-cancellation fee before cancelling.
- A phone number can usually be ported to another carrier; do it before cancelling the line.
- **Asking to cancel in a carrier's chat triggers a retention ladder.** The bot first reminds you of the current discount; a human then offers
  bigger temporary discounts and free data packs, and improves the offer if you say the cost is about another service. Those offers are
  usually "x 6 months" and fall back to the list price. Compare the offer with the bill (calc the saving), and with the list price after it
  ends. Declining is fine; a retention offer is a data point for how much of the list price is negotiable.
- Ask for the **lowest plan** of each service: the cheapest tier plus a renewed discount can cost far less than the first retention offer (here under half).
- "Today only" offers from a competitor to port a line are the same shape: a temporary discount on a high list price. Compare the **net monthly change** against what you already pay (including bonuses you would lose and any fixed discount on the other service) and the list price after the promo. If the gain is small, the offer is not worth the move.
- When the bot and the bill disagree (a different discount rate or end date), trust neither until you see the contract or the app.
- Before cutting a link that hosts something, inventory what depends on it: DNS records, port forwards, firewall rules, allow-lists, monitoring
  that tests from outside, scripts that name its address. Move each, test from outside, and only then switch the link off.

## 9. Seasonality

- Energy bills move with the weather: heating in the cold months, cooling in the hot ones. A budget made in one season is wrong in the next.
- Use the consumption history printed on the bills (12 months) instead of one bill. The lowest months show the base load; the rest is weather.
- Check the weather forecast for the next days and the seasonal outlook for the coming months, from the official service; label what could not
  be found, and do not extrapolate from it.
- Plan the dearest season in advance: the bills of the months after a cold or hot spell arrive weeks later.

## 10. Reconciling bills

- Keep the user's words as dictated in one file and the readings in another, so a reading can be checked and corrected.
- Every bill has a "previous balance" line: a bill that does not fit may be carrying an unpaid earlier one. A difference that comes out exact (no cents)
  between two bills is a hint, not proof.
- Do not add a bill on top of a total that may already contain it. Find out first.
- Price per unit = amount / consumption, all-in; fixed charges make a low-consumption month look dearer. Two bills in the same period say whether the tariff moved.
- Dates written day/month can be read either way; check them against the due dates that the bills give.
- Do not extrapolate a seasonal saving from a guess: compare real consecutive bills first.

## 11. Turning a CV into a money map

- List what the CV says people pay for, project by project, and note which already have a charging idea and which are free work.
- Rank by **speed to cash**: existing contacts first, then local services in the local currency, then products and open-source support, then a job.
- Convert every target into the currency of the bills (the exchange rate, with its date and source) and into hours, so the numbers can be compared with the monthly cost.
- Find what the CV does not say (rate, availability, how to hire, a way to pay) and fix those lines.
- Keep the work search itself in its own repo; here only the money side.

## 12. A free model's plan is a source of ideas, not of facts

A generic "plan to survive with nothing" from a free language model lists shelters, free meals and apps, with names and prices that are often invented or out of date. Use it to harvest ideas, then
(1) drop what does not fit your situation (it assumes you have no home, no income, no skills), (2) check every name, price and place before acting, (3) rank what is left by how much it earns or saves
against the amount due, and keep only what moves that number. A good test: how many hours does it take to earn one bill? If the answer is hundreds, it is not the plan.

## 13. A vehicle you do not use

A vehicle that sits idle still costs money every month (insurance, tax, parking, maintenance). Before cancelling anything:
- Compare **N months of premium** with the one-off cost of making the vehicle insurable again (an expired inspection can block a new policy: the cancel-and-lose-cover trap).
- Ask the insurer, in writing: can the policy be **suspended**, is there a cheaper **parked-vehicle cover** (theft and fire), and can third-party cover be **reactivated without a new inspection**?
- Check the inspection price and rules for your jurisdiction; going to the plant with an expired inspection can itself be an infraction.
- The legal minimum is the mandatory third-party insurance (`VEHICLE_OWNERSHIP_AR.md`); the owner answers for damage the car causes even while parked (a storm, a roll), so cancelling a policy is a risk decision, not only a saving.
- If it will never be used again, selling it is the end of all the recurring costs; check for pending fines on the plate first.


## 14. Work in exchange for rent, and rent clauses

- A landlord who cannot fund a repair may accept **work in place of rent**. It only protects the tenant if it is **in writing** (the contract or an attached note, even a chat message from the landlord): the start and end of the no-rent period; whether the arrears are cancelled or only paused; the exact scope of the work, defined by a professional (an architect or a master builder); **who buys the materials and who pays the labour**; what happens to the rent afterwards; who is liable if something fails.
- Compare the value of the work with the rent forgone: a repair quote can cost several months of rent, so the exchange can be a loss that is only visible later. Get two or three quotes, splitting labour and materials (a free online marketplace for tradespeople can give them: `PORTALS.md`).
- Safety first when the work is structural or above a dwelling: ask the professional what may be touched before anyone cuts or demolishes.
- **An inflation adjustment** in the contract needs two facts written down: the index and how often it applies. Compute the rent after the first adjustment before agreeing to the term.
- A verbal promise under a signed contract is the weak point: confirm it in writing before starting the work.

## 15. Changing foreign currency
- Use a licensed exchange house (the register number of the central bank is shown on the premises or its site). Expect to sign a standard declaration citing the foreign-exchange criminal regime and the anti-money-laundering law: routine, not a sign of a problem. Keep the receipt.
- Compare two or three nearby houses (buy rate and any commission) before changing: the spread is usually small but not zero, and for a small amount the walk can cost more than the difference. Rates move by the hour (not verified).
- Whether the foreign currency came from invoiced work matters for the tax records: ask the accountant once.

## 16. Leaving a paid accountant for a routine regime
- Order: log in with your own key; **delegate** the services the accountant needs in the relations service; **change the key**; export the issued invoices; ask in writing for the current category, what was filed in the last windows and the registered activities; only then agree the last payment (`MONOTRIBUTO_DIY.md` s.4).
- An official API exists for invoicing and registry data (digital certificate, `GOV_LOOKUPS.md` s.1); none for the monthly quota or the current account: pay by direct debit and a calendar.
