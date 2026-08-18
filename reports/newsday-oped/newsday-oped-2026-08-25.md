# Newsday guest essay: Nassau school enrollment and housing turnover

**Status:** draft for Jeff. Not submitted. Target submission **Monday, 2026-08-25**.
**Word count:** 595 (Newsday's form caps at 600).
**Source of every figure:** the campaign facts ledger, <https://rvc-taxes.jeffpinto.com/validation>.
Nassau-wide adaptation of the published note,
<https://www.jeffpinto.com/notes/four-governments-one-rule/>.

---

## 1. Newsday's current submission rules (verified 2026-08-18)

Verified by fetching Newsday's own pages, not from prior guidance. `WebFetch` is blocked
on newsday.com (the tool returns "unable to fetch"); the pages were retrieved with `curl`
and the form configuration read out of the page HTML.

| Item | Finding | Evidence |
|---|---|---|
| Where op-eds go | Web form on **<https://www.newsday.com/opinion/submit-your-essay-vnuwj0gk>** ("Submit Your Essay"), linked from /opinion. There is no op-ed email address published on the page. | HTTP 200, page HTML |
| Word limit | **600**, enforced by the form widget: `data-max-word-count="600"`. Intro text: "The word count for published essays is around **600 words.**" | `data-max-word-count="600"` on the embedded `lettersform` div |
| Letters vs essays | Letters to the editor are a **different, 200-word** form at <https://www.newsday.com/opinion/letters/submitting-your-letter-nzj035rq> (`data-max-word-count="200"`), and letters route to letters@newsday.com. Do not use the letters lane for this. | letter page HTML |
| Subject fit | "Our geographic focus is Long Island, followed by New York State issues." Nassau-wide framing is the right lead. | form intro text |
| Identity fields | The essay form overrides its community field to **"Community where you live"** (`data-community-field-text-override`). All required fields must be completed. "Contact information will not be disclosed." | form attributes |
| Response | "An editor will follow up if we are interested in pursuing your piece for publication." No auto-acknowledgement of publication. | form attributes |
| Page vintage | The essay-submission page was published/updated **2026-02-12**. | `publishedDate` / `updatedDate` in page JSON |

The older 700-800 word / `oped@newsday.com` guidance is **not** what Newsday currently
publishes. Draft to 600 and submit through the form.

---

## 2. The draft (default version, opens on the Nassau frame)

Suggested headline (Newsday writes its own):
**"Nassau's schools are shrinking. Four governments each hold one piece of the fix."**
Alternates: "The homes stopped changing hands" · "Nassau can't price its own senior-tax decision"

61% of Nassau's 56 school districts lost enrollment over the past decade. That number sits under most of our school budget fights.

In May my village balanced its school budget by cutting 22 teaching positions and 40 teaching assistants. Rockville Centre is not poor. The median household here earns $151,938. The budget passed 1,915 to 1,195, and people still found no better answer.

The problem is not money. The homes stopped changing hands.

28% of owner-occupied homes in Rockville Centre are headed by someone 65 or older, 2,076 of 7,453. Those are the four-bedroom houses near the schools, bought when the schools were the reason to buy. A neighborhood is a flow, not a stock. When the flow slows, the buildings and the staffing plan stay sized for a village that no longer exists, while the allowable levy increase is capped at 2.00% for a fifth straight year against a 2.63% inflation factor.

The easy version of this argument is wrong. Most older owners are not trying to leave. Freddie Mac found 68% of boomers plan to age in place, a legitimate choice nothing here should touch. The narrower claim is the honest one: of the minority who do want to move, many are blocked by rules, not preference. The test I hold every proposal to: a senior who never moves is left exactly as they are today.

Four levels of government each sit on one small rule. Not one fix needs a new program, a new agency, or new money. None takes a benefit away.

Federal. The capital-gains exclusion on a primary home, $250,000 single and $500,000 married, has not been indexed since 1997. Thirty years of appreciation later, selling can trigger a bill big enough to make staying the rational choice. H.R. 1340 would double and index it.

State. Hold a senior exemption, move within New York, and you can lose the benefit for the year you move. S3309 and its Assembly twin A5288 fix that. S3309 cleared Senate Aging 7-0 in April and died in Finance. The Assembly version never left committee. Nobody voted them down. They ran out of calendar.

County. Nassau has never published how many parcels in each school district hold a senior exemption, by income tier. It is not secret, just unpublished, so nobody, including me, can price what this costs or saves. I refuse to guess.

Local. On July 1, 2027, the ceiling on the senior-exemption income limit a locality may adopt rises from $50,000 to $75,000, if it opts in. Nassau applies its top tier at income at or below $47,000, while the median Rockville Centre household headed by someone 65 or older earns $79,722. The typical senior homeowner does not qualify for the program built for them.

That is a real decision with a real date, and the county cannot price it. Exemptions do not reduce what a district collects. They shift it onto everyone who is not exempt. Without parcel-level counts, deciding means guessing which neighbors absorb the shift. Nassau should publish the counts before the window opens. It costs nothing and it unlocks the other three.

Two of the four even earn the state money. Every Enhanced-to-Basic STAR transition is about $2,058 a year Albany stops paying, and every sale generates transfer tax.

I am a resident, not a lobbyist. The brief I built, at rvc-taxes.jeffpinto.com, has a letter builder for any Nassau address. It takes four minutes. A short letter naming a bill number, from someone who lives in the district, is one of the most useful things a resident can do.

---

## 3. Alternate opener slot (only if the Herald runs something before 8/25)

Insert **one** sentence ahead of the current first line, then delete the words "That number
sits under most of our school budget fights." so the count stays under 600:

> The Herald's coverage of [PIECE] this month put a local face on a countywide number: 61% of
> Nassau's 56 school districts lost enrollment over the past decade.

Rules for filling that slot: cite the Herald piece by its actual headline and date, verified
the day of submission. If no local coverage has run, ship the default opener unchanged. As of
2026-08-18 no Herald piece about this campaign has been confirmed.

---

## 4. Submission checklist

**Form:** <https://www.newsday.com/opinion/submit-your-essay-vnuwj0gk>

- [ ] Re-fetch the form page the morning of submission and confirm `data-max-word-count` is
      still 600. If it changed, re-trim before pasting.
- [ ] Paste the body only. No headline inside the body box; no markdown; straight quotes.
- [ ] Confirm the pasted body is **595 words** after any last edit.
- [ ] **Name:** Jeff Pinto
- [ ] **Community where you live:** `Rockville Centre` (the form's own field label). If a
      separate ZIP field appears, `11570`.
- [ ] **Never enter a street address**, in any field, and never leave a placeholder for one.
      Village and ZIP is the ceiling. Newsday says contact info is not disclosed, but the
      rule holds regardless.
- [ ] **Email:** jeff@bluecamelconsulting.com (the campaign's only contact route).
- [ ] **Phone:** Jeff's mobile if required. Not recorded in this repo.
- [ ] **Tagline / bio line** (if the form or a follow-up editor asks for one), resident
      framing, no consulting pitch:
      *"Jeff Pinto lives in Rockville Centre. He built rvc-taxes.jeffpinto.com, a nonpartisan
      brief and letter tool on Nassau school enrollment and senior housing turnover, as a
      resident project."*
- [ ] Same-day fact re-verify before sending (see section 5): H.R. 1340 status, S3309/A5288
      status, and that rvc-taxes.jeffpinto.com loads.
- [ ] After submitting, log the date here. Newsday only replies if interested, so no reply is
      not a rejection signal for at least a couple of weeks.

**Deliberate omissions**

- **No H.R. 1340 cosponsor count.** The count drifts and print lead time is unknown, so the
  op-ed names the bill and nothing else. Optional 7-word add if Jeff wants the sharper line
  and re-verifies it that morning: "My own representative is not a cosponsor."
- **No aggregate exemption-gap dollar figure**, anywhere. That number does not exist until
  Nassau publishes the parcel counts, which is the county ask in the piece.
- **No village FY27 rate figure (+7.18%).** It is a village-budget line and this piece is
  about schools. Available if an editor asks for more local texture.

---

## 5. Grounding table (every figure, ledger row, primary source)

| Claim as printed | Figure | Ledger row | Primary source | Verified |
|---|---|---|---|---|
| Nassau districts losing enrollment | 61% of 56 | `#f-61pct` | Nassau BOCES directory + LI Herald (Apr 2025) | 2026-07 |
| RVC position cuts and budget vote | 22 teaching + 40 TA cut; passed 1,915-1,195 | `#f-budget27` | LI Herald adoption + vote stories; district budget page | 2026-07 |
| Village median household income | $151,938 (2020-24) | `#f-hh-income` | ACS B19013 | 2026-07 |
| Senior-headed owner households | 28% (2,076 of 7,453) | `#f-senior-share` | ACS B25007 | 2026-07-18 |
| Levy cap vs inflation factor | 2.00% cap, 5th straight year, vs 2.63% | `#f-cap` | OSC release, Jan 2026 | 2026-07 |
| Age-in-place counter-stat | 68% of boomers plan to age in place | `#f-downsize-intent` | Freddie Mac "Silver Tsunami" release, 2024-12-19 | 2026-07-20 |
| Federal capital-gains lock-in | $250K single / $500K married, unindexed since 1997 | `#f-lockin` | AEI; NBER w25468; Minneapolis Fed (2024) | 2026-07 |
| H.R. 1340 | "More Homes on the Market Act": doubles and indexes the §121 exclusion | `#f-hr1340` | GPO GovInfo BILLSTATUS XML for 119-HR-1340 | **2026-08-18 (this session)** |
| S3309 / A5288 | S3309 cleared Senate Aging 7-0 in April 2026, died in Finance; A5288 never left committee | `#f-s3309` | nysenate.gov bill action histories | 2026-07-18 |
| Nassau parcel counts unpublished | no per-district, per-tier senior-exemption parcel count exists publicly | `#f-nassau-parcels` | data.ny.gov aa3i-eamx covers exemption-program counts only; the parcel/tier breakdown is the gap | 2026-07-20 |
| §467 income ceiling | $50,000 to $75,000 on 2027-07-01, local opt-in | `#f-467-75k` | RPTL §467(3)(a) statute text. **Cite the statute, never a chapter number.** | 2026-07-18 |
| Nassau top tier threshold | income at or below $47,000 | `#f-467-scale` | Nassau senior-exemption brochure (Rev. 3-26); DTF senior-exemption page | 2026-07 |
| Median senior-householder income | $79,722 (2020-24) | `#f-senior-income` | ACS B19049_005, geography `1600000US3663264` = **Rockville Centre village** | 2026-07 |
| Exemptions shift burden | exemptions shift the levy onto non-exempt parcels, they do not reduce district revenue | `#f-burden-shift` | OSC, Property Tax Exemptions | 2026-07 |
| STAR downsizing dividend | about $2,058/yr per Enhanced-to-Basic transition | `#f-dividend` | $3,147.01 − $1,089, DTF 2025 final credits | 2026-07-20 |
| Transfer tax on every sale | named without a figure | `#f-transfer` | DTF real-estate transfer tax (0.4%, seller-paid) | 2026-07 |

**Re-verified live this session (2026-08-18):** the GPO BILLSTATUS feed for 119-HR-1340
returns sponsor Rep. Jimmy Panetta (CA-19), 153 unique cosponsor bioguide IDs (matching the
ledger exactly), titles including "More Homes on the Market Act" and "To amend the Internal
Revenue Code of 1986 to increase the exclusion of gain from the sale of a principal
residence"; rvc-taxes.jeffpinto.com returns HTTP 200.

**Attribution correction worth keeping:** $79,722 is the **Rockville Centre** median for
households headed by someone 65 or older, not a Nassau County median. The draft says
"the median Rockville Centre household headed by someone 65 or older." Do not let an edit
turn it into a county figure.

---

## 6. Voice check

Per the published note: short sentences, no em dashes or en dashes anywhere in the body
(verified zero), passionate but factual, resident-not-vendor framing, no consulting mention,
no self-promotion beyond the one line naming the tool. The age-in-place guardrail appears
before any ask. The downsize claim carries its counter-stat in the same paragraph.
