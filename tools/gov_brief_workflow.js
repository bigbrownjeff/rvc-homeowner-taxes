export const meta = {
  name: 'governance-brief-adversarial',
  description: 'Rank Nassau homeowner cost-reduction levers from the governance report, adversarially challenge, and outline brief(s)',
  phases: [
    { title: 'Synthesize', detail: 'lead strategist ranks the levers from the report' },
    { title: 'Challenge', detail: '4 adversaries attack the ranking from distinct lenses' },
    { title: 'Adjudicate', detail: 'judge synthesizes, decides ties, outlines brief(s)' },
  ],
}

const REPORT = '/Users/jeffpinto/Projects/rvc-homeowner-taxes/.claude/worktrees/validation-deck/docs/GOVERNANCE_REVIEW.md'

const LEVERS_SCHEMA = {
  type: 'object',
  required: ['summary', 'levers', 'topPick', 'equityAngle'],
  properties: {
    summary: { type: 'string' },
    levers: { type: 'array', minItems: 6, items: { type: 'object',
      required: ['name', 'mechanism', 'homeownerDollarImpact', 'countywideSavings', 'nonDollarBenefits', 'equityEffect', 'feasibility', 'feasibilityWhy', 'evidence', 'risks'],
      properties: {
        name: { type: 'string' },
        mechanism: { type: 'string' },
        homeownerDollarImpact: { type: 'string', description: 'est. annual dollars to a typical RVC or Town-of-Hempstead homeowner, or diffuse/none if only county-budget abstract' },
        countywideSavings: { type: 'string' },
        nonDollarBenefits: { type: 'string' },
        equityEffect: { type: 'string', description: 'reduces/worsens/neutral on school+housing segregation, with why and source' },
        feasibility: { type: 'string', enum: ['high', 'medium', 'low'] },
        feasibilityWhy: { type: 'string' },
        evidence: { type: 'string' },
        risks: { type: 'string' },
      } } },
    topPick: { type: 'string' },
    equityAngle: { type: 'string' },
  },
}

const CRITIQUE_SCHEMA = {
  type: 'object',
  required: ['lens', 'killShot', 'leversOverrated', 'leversUnderrated', 'equityCritique', 'ownTopThree', 'reasoning'],
  properties: {
    lens: { type: 'string' },
    killShot: { type: 'string', description: 'the single strongest objection to the lead ranking' },
    leversOverrated: { type: 'array', items: { type: 'string' } },
    leversUnderrated: { type: 'array', items: { type: 'string' } },
    equityCritique: { type: 'string' },
    ownTopThree: { type: 'array', items: { type: 'string' } },
    reasoning: { type: 'string' },
  },
}

const ADJ_SCHEMA = {
  type: 'object',
  required: ['finalVerdict', 'tieExists', 'briefs', 'rejected', 'confidence'],
  properties: {
    finalVerdict: { type: 'string' },
    tieExists: { type: 'boolean' },
    briefs: { type: 'array', minItems: 1, maxItems: 2, items: { type: 'object',
      required: ['title', 'thesis', 'audience', 'leadNumbers', 'asks', 'equityFraming', 'whyOverAlternatives'],
      properties: {
        title: { type: 'string' },
        thesis: { type: 'string' },
        audience: { type: 'string' },
        leadNumbers: { type: 'array', items: { type: 'string' }, description: 'validated figures with sources' },
        asks: { type: 'array', items: { type: 'string' } },
        equityFraming: { type: 'string' },
        whyOverAlternatives: { type: 'string' },
      } } },
    rejected: { type: 'array', items: { type: 'object', required: ['name', 'why'], properties: { name: { type: 'string' }, why: { type: 'string' } } } },
    confidence: { type: 'string' },
  },
}

const GOAL = [
  'GOAL: find the best ways to REDUCE A NASSAU COUNTY (esp. Rockville Centre / Town of Hempstead) HOMEOWNER TOTAL TAX BILL',
  'by eliminating redundancy and inefficiency in the overlapping web of taxing districts — focused on school/education taxes',
  '(the largest slice, ~60-65% of a LI bill) but covering special districts, assessment, and town/village/county layers too.',
  'ALSO weigh NON-DOLLAR benefits, the user named priority being to "erase racism" — i.e., the racial DESEGREGATION co-benefit',
  'of governance reform. Long Island is among the most segregated suburban regions in the US and its fragmented ~56-district',
  'school map is widely documented as encoding that segregation (anchor on: ERASE Racism (the Long Island org), Newsday 2019',
  '"Long Island Divided" investigation, EdBuild "Fault Lines" report on how district borders segregate, and academic work on',
  'consolidation-vs-segregation). Treat desegregation as a CONTESTED remedy: consolidation can reduce segregation OR can harm',
  'majority-minority districts (closures fall on them first, dilution of Black/Latino local control). Be honest about that tension.',
].join(' ')

phase('Synthesize')
const leadPrompt = 'You are a lead public-finance strategist. Read the file ' + REPORT + ' IN FULL (use the Read tool). Then ' + GOAL +
  '\n\nProduce 6-9 candidate levers, RANKED best-to-worst for the goal, each populated per the required schema. Be concrete with dollars — use the report VERIFIED figures (e.g., special districts $946/household 2004 and 31% of town special-district revenue; commissioner-run sanitation up to 3x town-run, ~$18M/yr recoverable in Hempstead, $23.8-35.7M county-wide; Nassau 2017 CWSSI $130.5M first-year savings; the 1938 county guarantee ~$89.2M FY2024; Duncombe-Yinger consolidation cost curves — ~31.5% savings doubling a 300-pupil district but only ~14.4% at 1,500 and near-zero at Nassau ~3,700 average; NYSED reorganization incentive operating + building aid). CLEARLY distinguish levers that put dollars back in an individual homeowner pocket from levers that only produce diffuse county-budget savings. For equityEffect on each lever, be specific and sourced — use WebSearch/WebFetch to ground the segregation claims (ERASE Racism, Newsday Long Island Divided, EdBuild Fault Lines). Note where the dollar-maximizing lever and the equity-maximizing lever DIVERGE. Also write your full analysis to /tmp/rvc-extract/findings/gov-lead.md before returning the structured object.'
const lead = await agent(leadPrompt, { schema: LEVERS_SCHEMA, label: 'lead-strategist', agentType: 'general-purpose' })

phase('Challenge')
const LENSES = [
  { key: 'fiscal-skeptic', prompt: 'You are a SKEPTICAL public-finance economist. Your job is to puncture optimistic savings claims. Attack the lead ranking: are the savings overstated? Account for transition costs, salary/benefit leveling-up to the highest contract on merger, the Duncombe-Yinger diseconomies at Nassau ~3,700-pupil average district size, and the fact that the 1938 county guarantee means school districts are held harmless from over-assessment so assessment-accuracy reform may not flow to their levies. The acid test: which levers ACTUALLY reduce a homeowner bill rather than shuffle costs or produce one-time/diffuse savings? Re-rank on real, recurring, homeowner-visible dollars.' },
  { key: 'political-realist', prompt: 'You are a hard-nosed Long Island political operative. Your job is to kill anything that cannot pass. Attack the lead ranking on feasibility: EVERY documented LI school merger attempt failed (Tuckahoe-Southampton voted down 2013/2014; Elwood rebuffed by all five neighbors 2010-11); the Jan 2025 NYSED regionalization rule — mere planning — triggered a delegation-wide revolt; home rule, community identity, superintendents/unions, and the school-tax-as-property-value premium all resist consolidation. What can ACTUALLY happen in a 2-3 year horizon (shared services, BOCES expansion, special-district consolidation by referendum, transparency mandates) vs. what is a decade-long fantasy? Re-rank by political feasibility and name the realistic vehicle for each.' },
  { key: 'equity-critic', prompt: 'You are a racial-equity analyst who is DEEPLY SKEPTICAL that efficiency reforms help Black and Latino Long Islanders — and equally skeptical of leaving the segregated status quo. Long Island is among the most segregated suburbs in America; its district map encodes that (Newsday Long Island Divided 2019; ERASE Racism reports; EdBuild Fault Lines). Interrogate EACH lever: does it actually desegregate, or merely reshuffle? Could consolidation-for-savings become a Trojan horse that closes schools in majority-minority districts first, dilutes Black/Latino political control of their districts, or redirects savings into tax cuts for wealthy white districts rather than equity? Conversely, which lever (boundary/enrollment reform, controlled-choice, county-wide or regional districting, BOCES magnet programs) would MOST reduce segregation — and is that the same lever as the dollar-maximizing one, or a different brief entirely? Use WebSearch/WebFetch to ground every claim. Be rigorous and non-tendentious; cite.' },
  { key: 'homeowner-advocate', prompt: 'You are an RVC homeowner who only cares about your own bill and your neighbors. Strip every idealistic or county-abstract item. For a specific Rockville Centre homeowner (school ~62% of a ~$15K total bill) and a typical unincorporated Town-of-Hempstead homeowner (who pays the special-district layers villages do not), rank the levers by ACTUAL dollars back in pocket within a realistic horizon, with rough $/home. Kill anything whose savings never reach a tax bill. Tell me the 2-3 things that would most lower MY bill, in order, with numbers.' },
]
const critiques = (await parallel(LENSES.map((L) => () => {
  const p = L.prompt +
    '\n\nThe full governance report is at ' + REPORT + ' (Read it if you need to verify a claim).' +
    '\n\nTHE LEAD STRATEGIST RANKING TO CHALLENGE (JSON):\n' + JSON.stringify(lead) +
    '\n\nReturn the required schema. Be specific — name the exact levers you think are overrated/underrated and land one clear kill shot. Also write your critique to /tmp/rvc-extract/findings/gov-critique-' + L.key + '.md before returning.'
  return agent(p, { schema: CRITIQUE_SCHEMA, label: 'challenge:' + L.key, phase: 'Challenge', agentType: 'general-purpose' })
}))).filter(Boolean)

phase('Adjudicate')
const adjPrompt = 'You are the adjudicator. ' + GOAL +
  '\n\nYou have the lead strategist ranking and four adversarial critiques. Weigh them honestly — the critiques are meant to be right where they are right. Produce a DECISION-USEFUL verdict for a homeowner-advocate who will turn this into a public brief.' +
  '\n\nDecide the central question: is there ONE clearly best path, or a GENUINE TIE between two DISTINCT strategies that each deserve their own brief? The likely fault line: the DOLLAR-maximizing path (likely special-district / shared-services consolidation — biggest verified, passable savings) vs. the EQUITY-maximizing path (likely school-boundary / enrollment / regional-districting reform — biggest desegregation effect but harder and contested). If those genuinely diverge in lever, audience, and ask, output TWO briefs. If one path dominates on both axes, output ONE. Do not manufacture a tie; do not collapse a real one.' +
  '\n\nFor each brief give: a sharp title; a one-paragraph thesis; the audience; 4-6 LEAD NUMBERS (validated, with source — pull from the report verified figures); 3-5 concrete asks; an equityFraming paragraph that is responsible, evidence-based, and preserves the consolidation-is-double-edged nuance (no tendentious claims; cite ERASE Racism / Newsday / EdBuild where used); and a whyOverAlternatives paragraph. List rejected levers with one-line reasons. State your confidence and key uncertainties.' +
  '\n\nLEAD RANKING (JSON):\n' + JSON.stringify(lead) +
  '\n\nADVERSARIAL CRITIQUES (JSON array):\n' + JSON.stringify(critiques) +
  '\n\nWrite the complete plan (the brief outline(s), rejected levers, and a short rationale referencing which critiques moved you) to /tmp/rvc-extract/findings/gov-brief-plan.md, then return the structured object.'
const adj = await agent(adjPrompt, { schema: ADJ_SCHEMA, label: 'adjudicator', agentType: 'general-purpose' })

log('Adjudication: tieExists=' + adj.tieExists + ', briefs=' + adj.briefs.length)
return { tieExists: adj.tieExists, briefCount: adj.briefs.length, briefs: adj.briefs, rejected: adj.rejected, finalVerdict: adj.finalVerdict }
