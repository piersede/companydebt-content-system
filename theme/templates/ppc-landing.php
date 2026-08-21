<?php
/**
 * Template Name: PPC Landing
 *
 * Server-side build of the "CompanyDebt PPC Landing" design handoff
 * (design_handoff_companydebt_ppc). One template drives four ad-intent
 * variants. The prototype switched intent in the browser with a JS object and
 * a dev-only preview bar; that is gone here. The intent is resolved from the
 * page slug in PHP and only that intent's copy is rendered, so each ad group
 * gets a real, crawlable, single-purpose page:
 *
 *   ppc-liquidate-company    -> cvl
 *   ppc-company-debt         -> company_debt
 *   ppc-hmrc-debt            -> hmrc
 *   ppc-winding-up-petition  -> winding_up
 *
 * An unknown slug falls back to the 'cvl' intent.
 *
 * WHAT CHANGED FROM THE PROTOTYPE (deliberate, do not "restore"):
 *
 *  1. CVL FEES. The prototype published a four-to-seven-thousand-plus-VAT range
 *     for the practitioner fee. That is a banned drift pattern (see
 *     data/statutory_fees.json -> cvl_practitioner_fee) and
 *     scripts/check_statutory_fees.py fails on it. Canonical figures used
 *     here: practitioner fee £3,500 plus VAT (standard fixed fee, straightforward
 *     case), disbursements £500 to £1,500. NOTE: £4,000-£5,000 is the
 *     EX-VAT total. data/statutory_fees.json calls that key cvl_all_in, which
 *     is a misleading name (docs/open-items.md item 5). The published figure
 *     must be £4,800 to £6,000 once VAT is added, matching page 65614.
 *     Both the Fees section and the "How Much Does a CVL Cost?" FAQ use them.
 *
 *  2. REGULATOR WORDING. In the UK, individual insolvency practitioners hold
 *     licences; firms do not. The trust bar no longer says the brand is
 *     "licensed and regulated by" the IPA and ICAEW. It now attributes the
 *     licences to the named practitioners, first-party ("our insolvency
 *     practitioners"). Company Debt is itself a licensed insolvency practice
 *     and must never be described as referring or introducing directors to
 *     third-party practitioners.
 *
 *  3. FOOTER "MEMBERS OF" ICAS. Removed. Nothing in repo canon supports an
 *     ICAS membership claim and the two named practitioners are licensed by
 *     the IPA and the ICAEW only.
 *
 *  4. Christopher Andersen is plain text, never linked to /author/chris-andersen/
 *     (verified 404).
 *
 *  5. The same-day callback line and the practitioner quote are owner-approved.
 *     Every "PENDING CLIENT APPROVAL" flag (.ph-flag) is stripped.
 *
 *  6. The 5-step Assessment form variant and the dev preview bar are out of
 *     scope and are not present in this file at all.
 *
 * THE FORM is a Gravity Form, rendered the same way templates/quick-quote.php
 * renders GF40 — via do_shortcode(). The form id comes from the WordPress
 * option 'cd_ppc_form_id' so it can be set per environment without a code
 * change. The resolved intent is handed to the form through field_values so
 * every lead records which ad intent produced it.
 *
 * The theme's own header, search form and footer are suppressed by CSS for
 * this template only. This page is a self-contained ad landing page with its
 * own header and footer, and the theme chrome would duplicate both. header.php
 * only suppresses its masthead for three named landing templates and is not
 * edited here.
 *
 * @package CompanyDebt
 */

get_header();

/* -------------------------------------------------------------------------
 * Intent data. Transcribed from the prototype's INTENTS object.
 * ---------------------------------------------------------------------- */
$cd_ppc_intents = array(
	'cvl' => array(
		'eyebrow'      => 'CONFIDENTIAL ADVICE FOR UK LIMITED COMPANY DIRECTORS',
		'h1'           => 'Need to Liquidate Your Company?',
		'p1'           => "If the company can no longer pay its debts, we can explain whether a Creditors' Voluntary Liquidation (CVL) is the right next step. That includes what happens to the debts, what it costs and whether you could be personally affected.",
		'sit'          => 'close',
		'show_context' => false,
		'ctx_eyebrow'  => 'Is This Similar to Your Situation?',
		'ctx_h2'       => 'Is This Similar to Your Situation?',
		'ctx_html'     => '',
		'faq_first'    => 0,
	),
	'company_debt' => array(
		'eyebrow'      => 'CONFIDENTIAL ADVICE FOR UK LIMITED COMPANY DIRECTORS',
		'h1'           => "Need to Close a Company That Can't Pay Its Debts?",
		'p1'           => 'If the company can no longer keep up with HMRC, suppliers, lenders or other creditors, we can explain whether voluntary liquidation is the right next step. That includes what happens to the debts and whether you could be personally affected.',
		'sit'          => 'cantpay',
		'show_context' => true,
		'ctx_eyebrow'  => 'Company Debt',
		'ctx_h2'       => 'How Do You Know When the Company Has Reached the End of the Road?',
		'ctx_html'     => '<p class="lead">A difficult month does not necessarily mean a company needs to be liquidated. But persistent inability to pay HMRC, staff, suppliers, lenders or other liabilities can indicate a much more serious problem.</p>
<p class="bodytext">The question is whether the company has a realistic route back to being able to meet its liabilities, or whether continuing to trade is simply allowing the debt position to worsen.</p>
<p class="bodytext">You do not need to make that judgement alone.</p>
<a class="btn btn--solid cd-ppc-cta-gap" href="#formCard">Request a Confidential Call</a>',
		'faq_first'    => 1,
	),
	'hmrc' => array(
		'eyebrow'      => 'SPECIALIST HELP WITH COMPANY HMRC DEBT',
		'h1'           => "Can't Pay HMRC?",
		'p1'           => "If VAT, PAYE or Corporation Tax arrears have become unmanageable, we can explain your options confidentially. That includes whether Creditors' Voluntary Liquidation should be considered and what it would mean for the company and for you.",
		'sit'          => 'cantpay',
		'show_context' => true,
		'ctx_eyebrow'  => 'HMRC Debt',
		'ctx_h2'       => "What Happens If Your Company Can't Pay HMRC?",
		'ctx_html'     => '<p class="lead">HMRC is often one of the largest creditors when a company reaches financial difficulty. Arrears can include VAT, PAYE, National Insurance and Corporation Tax.</p>
<p class="bodytext">If the company cannot realistically clear the arrears while also meeting its ongoing liabilities, the wider solvency of the business needs to be considered.</p>
<p class="bodytext">A CVL can bring an insolvent company to an orderly close and allows its debts to be dealt with through the formal insolvency process. Whether that is appropriate depends on the circumstances of the company.</p>
<a class="btn btn--solid cd-ppc-cta-gap" href="#formCard">Request a Confidential Call</a>',
		'faq_first'    => 4,
	),
	'winding_up' => array(
		'eyebrow'      => 'URGENT ADVICE FOR LIMITED COMPANY DIRECTORS',
		'h1'           => 'Facing a Winding-Up Petition?',
		'p1'           => "If a winding-up petition has been presented, or you've been threatened with one, we can explain what it means for the company and for you, and whether voluntary liquidation should now be considered.",
		'sit'          => 'legal',
		'show_context' => true,
		'ctx_eyebrow'  => 'Winding-Up Petition',
		'ctx_h2'       => 'A Winding-Up Petition Changes the Situation',
		'ctx_html'     => '<p class="lead">A winding-up petition is serious. If the court ultimately makes a winding-up order, the company can be placed into compulsory liquidation.</p>
<p class="bodytext">If a petition has already been presented, you should understand the company\'s position and the remaining options as soon as possible.</p>
<p class="bodytext">Depending on the circumstances, directors may need to consider whether taking control through a voluntary liquidation process is appropriate rather than waiting for events to be dictated by a creditor.</p>
<a class="btn btn--solid cd-ppc-cta-gap" href="#formCard">Request a Confidential Call</a>',
		'faq_first'    => 0,
	),
);

/* One page per ad intent. Matched by slug so it stays correct across
 * environments (no post IDs baked in). */
$cd_ppc_slug_map = array(
	'ppc-liquidate-company'   => 'cvl',
	'ppc-company-debt'        => 'company_debt',
	'ppc-hmrc-debt'           => 'hmrc',
	'ppc-winding-up-petition' => 'winding_up',
);

$cd_ppc_slug = (string) get_post_field( 'post_name', get_the_ID() );
$cd_ppc_key  = isset( $cd_ppc_slug_map[ $cd_ppc_slug ] ) ? $cd_ppc_slug_map[ $cd_ppc_slug ] : 'cvl';
$cd_ppc      = $cd_ppc_intents[ $cd_ppc_key ];

/* The eyebrow above the contextual block is suppressed when it would just
 * repeat its own H2 (the prototype did the same, in JS). */
$cd_ppc_ctx_eyebrow_redundant = ( strtolower( trim( $cd_ppc['ctx_eyebrow'] ) ) === strtolower( trim( $cd_ppc['ctx_h2'] ) ) );

/* -------------------------------------------------------------------------
 * FAQs. Transcribed from the prototype's FAQS array, with the CVL fee answer
 * corrected to the canonical figures in data/statutory_fees.json.
 * The array keys are the ORIGINAL prototype indices and must stay stable —
 * the "Questions Directors Usually Want Answered" list deep-links by index.
 * ---------------------------------------------------------------------- */
$cd_ppc_faqs = array(
	0 => array(
		'q' => 'What Happens to Company Debts in a CVL?',
		'a' => "The company's debts are dealt with through the liquidation. Creditors submit claims to the liquidator and, where funds are available, distributions are made according to insolvency law. At the end of the process the company is normally dissolved. Company debts do not automatically transfer to the directors personally, although there are important exceptions.",
	),
	1 => array(
		'q' => "Will I Personally Have to Pay My Company's Debts?",
		'a' => "Usually, no. A limited company is a separate legal entity. However, personal guarantees, an overdrawn director's loan account, certain transactions or issues relating to director conduct can create personal exposure. We can discuss these with you before you decide how to proceed.",
	),
	2 => array(
		'q' => 'How Much Does a CVL Cost?',
		'a' => 'The initial consultation is free. If the company enters formal liquidation, our practitioner fee is £3,500 plus VAT. That is a standard fixed fee for a straightforward case. On top of that there are disbursements, which are necessary third-party costs such as the bond, Gazette notices and Companies House filings, and these typically add £500 to £1,500. Once VAT is added, most straightforward cases come to roughly £4,800 to £6,000. The expected total is explained clearly before you formally instruct us.',
	),
	3 => array(
		'q' => 'Can I Be a Company Director Again After Liquidation?',
		'a' => 'Normally, yes. Being the director of a company that enters liquidation does not by itself prevent you from becoming or remaining a director of another company. Restrictions can apply in some circumstances, including where a director is disqualified.',
	),
	4 => array(
		'q' => 'What Happens If My Company Owes HMRC?',
		'a' => 'HMRC is treated as a creditor of the company. Tax debts such as VAT, PAYE and Corporation Tax can be included in the insolvency process. Your individual circumstances still need to be reviewed, particularly where there may be personal guarantees, director liabilities or other issues.',
	),
	5 => array(
		'q' => 'Does Speaking to CompanyDebt Mean I Have Agreed to Liquidate?',
		'a' => 'No. The initial consultation is about understanding your company\'s position and the available options. You are not committed to a CVL simply because you have spoken to us.',
	),
);

/* Server-side reorder: the intent's most relevant question leads and is the
 * one open on load. Original indices are preserved as data-idx. */
$cd_ppc_faq_first = isset( $cd_ppc_faqs[ $cd_ppc['faq_first'] ] ) ? (int) $cd_ppc['faq_first'] : 0;
$cd_ppc_faq_order = array( $cd_ppc_faq_first );
foreach ( array_keys( $cd_ppc_faqs ) as $cd_ppc_i ) {
	if ( (int) $cd_ppc_i !== $cd_ppc_faq_first ) {
		$cd_ppc_faq_order[] = (int) $cd_ppc_i;
	}
}

/* Deep links from the "Questions Directors Usually Want Answered" list into
 * the accordion. Index = original FAQ index, not display position. */
$cd_ppc_qlist = array(
	array( 'label' => "What happens to the company's debts?", 'idx' => 0 ),
	array( 'label' => 'How much will liquidation cost?', 'idx' => 2 ),
	array( 'label' => 'Will I become personally responsible for anything?', 'idx' => 1 ),
	array( 'label' => 'What happens to personal guarantees?', 'idx' => 1 ),
	array( 'label' => "What happens if I have an overdrawn director's loan account?", 'idx' => 1 ),
	array( 'label' => 'Can I start or run another company afterwards?', 'idx' => 3 ),
);

/* -------------------------------------------------------------------------
 * Assets and constants.
 * ---------------------------------------------------------------------- */
$cd_ppc_assets = '/wp-content/themes/company-debt-webpigment/assets/ppc';
$cd_ppc_tel    = '0800 074 6757';
$cd_ppc_telraw = '08000746757';

/* Gravity Form id lives in an option so it can differ between staging and
 * live without touching this file. Set it with:
 *   wp option update cd_ppc_form_id <id>
 */
/*
 * The option is the preferred source, but it lives in wp_options, and a
 * staging-to-live database push may legitimately leave wp_options behind (it
 * carries far more than this one value). Without a fallback the live page
 * would render its "form not configured" placeholder, which on a paid landing
 * page means a page with no lead capture at all.
 *
 * 47 is the id the form was created with on staging. Live's highest form id
 * was 46 at the time of writing, so the form travels to live keeping id 47 and
 * this default stays correct. Override per environment with the option, or
 * with the filter if the ids ever diverge.
 */
$cd_ppc_form_id = get_option( 'cd_ppc_form_id' );
if ( ! $cd_ppc_form_id ) {
	$cd_ppc_form_id = 47;
}
$cd_ppc_form_id = (int) apply_filters( 'cd_ppc_form_id', $cd_ppc_form_id );
?>

<style id="cd-ppc-styles">
/* ─────────────────────────────────────────────────────────────────────────
   CompanyDebt PPC landing page.

   Every rule is scoped under .cd-ppc so nothing here can leak into the rest
   of the site, and the theme-defence block at the top of this file re-states
   the resets the theme would otherwise win on (the theme ships high-specificity
   `body.page ... h2 / p` rules that add padding and margins).

   Design tokens are taken verbatim from the handoff README. Do not tune them.
   ───────────────────────────────────────────────────────────────────────── */

/* Theme chrome suppression. This page is a self-contained ad landing page
   with its own header and footer. */
body.page-template-ppc-landing #masthead,
body.page-template-ppc-landing .mobile-action-bar,
body.page-template-ppc-landing #search-form,
body.page-template-ppc-landing #colophon { display: none !important; }
body.page-template-ppc-landing { overflow-x: hidden; }
body.page-template-ppc-landing #page.site { max-width: none; padding: 0; }

/* Theme defence: neutralise inherited heading/paragraph/list spacing.
   Kept at (0,1,1), one class plus one element, so it matches the prototype's
   own page-scoped element reset. Every component rule below carries two classes
   (0,2,0) or more and therefore still wins on specificity. Do not raise this
   selector to `body.page-template-ppc-landing .cd-ppc p`: at (0,2,1) it beats
   the component spacing rules and the whole page collapses. */
.cd-ppc h1,
.cd-ppc h2,
.cd-ppc h3,
.cd-ppc h4,
.cd-ppc p,
.cd-ppc ul,
.cd-ppc ol,
.cd-ppc li,
.cd-ppc blockquote,
.cd-ppc figure { margin: 0; padding: 0; }
.cd-ppc h1,
.cd-ppc h2,
.cd-ppc h3 { text-transform: none; }

/* ── Tokens ─────────────────────────────────────────────────────────────── */
.cd-ppc {
	--navy: #0a1f44;
	--navy-2: #0d2a57;
	--accent: #0f4c81;
	--accent-soft: #e8f1f8;
	--orange: #c25200;
	--text: #101828;
	--soft: #3d4757;
	--muted: #5b6675;
	--line: #e4e7ec;
	--line-2: #eef0f3;
	--band: #e8edf6;
	--white: #fff;
	--green: #166534;
	--radius: 14px;
	--shadow: 0 18px 48px rgba(10, 31, 68, .08);
	--w-content: 1140px;
	--w-text: 720px;
	-webkit-text-size-adjust: 100%;
	background: var(--white);
	color: var(--text);
	font: 400 17px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
.cd-ppc *, .cd-ppc *::before, .cd-ppc *::after { box-sizing: border-box; }
.cd-ppc img, .cd-ppc svg { max-width: 100%; }
.cd-ppc a { color: var(--accent); text-decoration: none; }
.cd-ppc a:hover { color: #0b3a63; text-decoration: underline; text-underline-offset: 3px; }
.cd-ppc h1, .cd-ppc h2, .cd-ppc h3 { letter-spacing: -.02em; text-wrap: pretty; }
.cd-ppc p { text-wrap: pretty; }

/* ── Layout ─────────────────────────────────────────────────────────────── */
.cd-ppc .wrap { width: 100%; max-width: var(--w-content); margin: 0 auto; padding: 0 24px; }
.cd-ppc .wrap--text { max-width: 720px; }
.cd-ppc .text-cap { max-width: var(--w-text); }
.cd-ppc .grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
@media (max-width: 1023px) { .cd-ppc .grid3 { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 639px) { .cd-ppc .grid3 { grid-template-columns: 1fr; } }
.cd-ppc .grid4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
@media (max-width: 1023px) { .cd-ppc .grid4 { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 639px) { .cd-ppc .grid4 { grid-template-columns: 1fr; } }

/* ── Type ───────────────────────────────────────────────────────────────── */
.cd-ppc .eyebrow { font-size: 12.5px; font-weight: 750; letter-spacing: .1em; text-transform: uppercase; color: var(--accent); }
.cd-ppc .h2 { font-size: clamp(30px, 3.4vw, 38px); line-height: 1.15; font-weight: 750; color: var(--navy); max-width: var(--w-text); }
.cd-ppc .h2--gap { margin-top: 10px; }
.cd-ppc .lead { font-size: 20px; line-height: 1.6; color: var(--navy); font-weight: 500; max-width: var(--w-text); margin-top: 14px; }
.cd-ppc .bodytext { font-size: 17px; line-height: 1.65; color: var(--soft); max-width: var(--w-text); margin-top: 14px; }
.cd-ppc .section--navy .bodytext { color: #c8d6e8; }
.cd-ppc .section--navy .eyebrow { color: #9fc2e8; }
.cd-ppc .section--navy .h2 { color: #fff; }

/* ── Buttons ────────────────────────────────────────────────────────────── */
.cd-ppc .btn {
	display: inline-flex; align-items: center; justify-content: center; gap: 9px;
	min-height: 56px; padding: 0 28px; border-radius: 12px;
	font-size: 17px; font-weight: 700; border: 1px solid transparent;
	cursor: pointer; font-family: inherit;
	transition: filter .14s ease, background .14s ease;
}
.cd-ppc .btn--solid { background: var(--orange); color: #fff; }
.cd-ppc .btn--solid:hover { background: #a84700; color: #fff; text-decoration: none; }
.cd-ppc .btn--ghost { background: #fff; color: var(--navy); border-color: #c3cddb; }
.cd-ppc .btn--ghost:hover { background: #f4f7fb; border-color: var(--navy); color: var(--navy); text-decoration: none; }
/* Replaces the prototype's inline style="margin-top:…" on section CTAs. */
.cd-ppc .cd-ppc-cta-gap { margin-top: 8px; }
.cd-ppc .cd-ppc-cta-18 { margin-top: 18px; }
.cd-ppc .cd-ppc-cta-26 { margin-top: 26px; }
.cd-ppc .cd-ppc-cta-32 { margin-top: 32px; }

/* ── Sections ───────────────────────────────────────────────────────────── */
.cd-ppc .section { padding: 64px 0; border-top: 1px solid var(--line-2); }
.cd-ppc .section--band { background: var(--band); }
.cd-ppc .section--navy { background: var(--navy); color: #fff; border-top: 0; }
.cd-ppc .section--navy .lead, .cd-ppc .section--navy p { color: #c8d6e8; }
.cd-ppc .reassure, .cd-ppc .finalcta { padding: 112px 0; }

/* ── Header ─────────────────────────────────────────────────────────────── */
.cd-ppc header.ppc { background: #fff; border-bottom: 1px solid var(--line); }
.cd-ppc .ppc__in { display: flex; align-items: center; gap: 20px; min-height: 76px; flex-wrap: wrap; }
.cd-ppc .ppc__brand { display: flex; flex-direction: column; line-height: 1.15; }
.cd-ppc .ppc__brand b { font-size: 21px; font-weight: 800; color: var(--navy); letter-spacing: -.02em; }
.cd-ppc .ppc__brand span { font-size: 12.5px; color: var(--muted); font-weight: 600; }
.cd-ppc .ppc__right { margin-left: auto; display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }
.cd-ppc .ppc__prefer { text-align: right; line-height: 1.3; }
.cd-ppc .ppc__prefer small { display: block; color: var(--muted); font-size: 12.5px; font-weight: 600; }
.cd-ppc .ppc__prefer a { font-size: 19px; font-weight: 800; color: var(--navy); }
.cd-ppc .ppc__call { background: var(--navy); color: #fff; }
.cd-ppc .ppc__call:hover { filter: brightness(1.2); color: #fff; }

/* ── Hero ───────────────────────────────────────────────────────────────── */
.cd-ppc .hero { background: var(--band); padding: 56px 0 64px; border-bottom: 1px solid var(--line); }
.cd-ppc .hero__grid { display: grid; grid-template-columns: 1.1fr .9fr; gap: 56px; align-items: start; }
.cd-ppc .hero h1 { margin: 18px 0 0; font-size: clamp(38px, 5.2vw, 56px); line-height: 1.05; font-weight: 800; letter-spacing: -.03em; color: var(--navy); }
.cd-ppc .hero__p { margin-top: 18px; font-size: 18.5px; line-height: 1.7; color: var(--soft); }
.cd-ppc .hero__p + .hero__p { margin-top: 12px; }
.cd-ppc .trustline { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 24px; font-size: 15px; font-weight: 700; color: var(--navy); }
.cd-ppc .trustline span { display: inline-flex; align-items: center; gap: 7px; }
.cd-ppc .trustline span::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--green); }
.cd-ppc .hero__reassure { margin-top: 14px; font-size: 15.5px; font-weight: 700; color: var(--navy); }
.cd-ppc .hero__tel { margin-top: 22px; font-size: 16.5px; color: var(--soft); }
.cd-ppc .hero__tel a { font-weight: 800; color: var(--navy); }
.cd-ppc .hero__tel--tight { margin-top: 14px; }
.cd-ppc .hero__proof { margin-top: 28px; display: flex; flex-direction: column; gap: 16px; }
.cd-ppc .hero__practitioner-row { display: flex; align-items: center; gap: 10px; }
.cd-ppc .hero__practitioner-row img { flex: none; width: 40px; height: 40px; border-radius: 50%; object-fit: cover; display: block; }
.cd-ppc .hero__practitioner { font-size: 14px; color: var(--muted); }
.cd-ppc .rate--flush { margin-top: 0; }

/* ── Form card ──────────────────────────────────────────────────────────── */
.cd-ppc .card { background: #fff; border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); padding: 32px; }
.cd-ppc .card h2 { font-size: 23px; font-weight: 800; color: var(--navy); }
.cd-ppc .card .sub { margin-top: 8px; font-size: 15px; color: var(--muted); }
.cd-ppc .opts { display: grid; gap: 10px; margin-top: 20px; }
.cd-ppc .opt { display: block; position: relative; }
.cd-ppc .opt input { position: absolute; opacity: 0; }
.cd-ppc .opt span { display: block; padding: 14px 16px; border: 1.5px solid #d7dee8; border-radius: 10px; font-size: 15.5px; font-weight: 600; color: var(--text); cursor: pointer; transition: border-color .12s, background .12s; }
.cd-ppc .opt input:checked + span { border-color: var(--accent); background: var(--accent-soft); color: var(--navy); }
.cd-ppc .card .btn { width: 100%; margin-top: 20px; }
.cd-ppc .field { display: grid; gap: 6px; margin-bottom: 14px; }
.cd-ppc .field label { font-size: 13px; font-weight: 650; color: var(--soft); }
.cd-ppc .field input { width: 100%; min-height: 50px; padding: 12px 14px; border: 1px solid #cfd6e0; border-radius: 9px; font-family: inherit; font-size: 16px; color: var(--text); }
.cd-ppc .field input:focus { outline: 2px solid var(--accent); outline-offset: 1px; border-color: var(--accent); }
.cd-ppc .microcopy { font-size: 14px; color: var(--muted); margin-top: 10px; line-height: 1.6; }
.cd-ppc .microcopy--callback { margin-top: 10px; color: var(--accent); font-weight: 650; }
.cd-ppc .step { display: none; }
.cd-ppc .step.is-active { display: block; }
.cd-ppc .back { background: none; border: 0; font-size: 14px; font-weight: 700; color: var(--accent); cursor: pointer; padding: 0; margin-bottom: 14px; }

/* Gravity Forms sits inside the card. Match the prototype's field styling so
   the GF markup inherits the design rather than the theme's form styles. */
.cd-ppc .cd-ppc-form { margin-top: 20px; }
.cd-ppc .cd-ppc-form .gform_wrapper { margin: 0; }
.cd-ppc .cd-ppc-form .gform_fields { display: grid; gap: 6px; }
.cd-ppc .cd-ppc-form .gfield { margin-bottom: 14px; }
.cd-ppc .cd-ppc-form .gfield_label { font-size: 13px; font-weight: 650; color: var(--soft); display: block; margin-bottom: 6px; }
.cd-ppc .cd-ppc-form input[type="text"],
.cd-ppc .cd-ppc-form input[type="tel"],
.cd-ppc .cd-ppc-form input[type="email"],
.cd-ppc .cd-ppc-form textarea,
.cd-ppc .cd-ppc-form select {
	width: 100%; min-height: 50px; padding: 12px 14px;
	border: 1px solid #cfd6e0; border-radius: 9px;
	font-family: inherit; font-size: 16px; color: var(--text); background: #fff;
}
.cd-ppc .cd-ppc-form input:focus,
.cd-ppc .cd-ppc-form textarea:focus,
.cd-ppc .cd-ppc-form select:focus { outline: 2px solid var(--accent); outline-offset: 1px; border-color: var(--accent); }
.cd-ppc .cd-ppc-form .gform_button {
	width: 100%; margin-top: 20px; min-height: 56px; padding: 0 28px;
	border-radius: 12px; border: 1px solid transparent;
	background: var(--orange); color: #fff;
	font-family: inherit; font-size: 17px; font-weight: 700; cursor: pointer;
}
.cd-ppc .cd-ppc-form .gform_button:hover { background: #a84700; }
.cd-ppc .cd-ppc-form-missing { margin-top: 20px; padding: 16px; border: 1px dashed #cfd6e0; border-radius: 9px; font-size: 14px; color: var(--muted); }

/* ── Trust bar ──────────────────────────────────────────────────────────── */
.cd-ppc .tbar { background: #F7F8FA; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); padding: 44px 0 48px; }
.cd-ppc .tbar__tier { padding: 0; }
.cd-ppc .tbar__label { text-align: left; font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: #8a94a3; margin-bottom: 20px; }
.cd-ppc .tbar__marks { display: flex; justify-content: flex-start; align-items: center; gap: 44px; flex-wrap: wrap; }
.cd-ppc .tbar__mark { min-height: 44px; display: flex; align-items: center; width: auto; }
.cd-ppc .tbar__mark img { height: 30px; width: auto; object-fit: contain; display: block; }
/* Names the licence holders. Firms do not hold IP licences; individuals do. */
.cd-ppc .tstrip { margin: 40px 0 0; }
.cd-ppc .ticon { width: 26px; height: 26px; color: #6B7280; margin-bottom: 12px; }
.cd-ppc .titem b { display: block; font-size: 20px; font-weight: 750; color: var(--navy); }
.cd-ppc .titem p { margin-top: 6px; font-size: 15px; color: var(--muted); line-height: 1.55; }
@media (max-width: 640px) {
	.cd-ppc .tbar__marks { display: grid; grid-template-columns: 1fr 1fr; gap: 24px 32px; justify-items: start; }
}

/* ── Reviews ────────────────────────────────────────────────────────────── */
.cd-ppc .rate { display: flex; align-items: center; gap: 10px; margin-top: 10px; font-weight: 700; color: var(--navy); flex-wrap: wrap; }
.cd-ppc .rate img { height: 20px; width: 36px; object-fit: contain; display: inline-block; vertical-align: middle; }
.cd-ppc .stars { color: #f5b301; letter-spacing: 2px; font-size: 18px; }
.cd-ppc .rcards { margin-top: 36px; }
.cd-ppc .rcard { background: #fff; border: 1px solid var(--line); border-radius: var(--radius); padding: 24px; }
.cd-ppc .rcard .stars { font-size: 14px; margin-bottom: 10px; display: block; }
.cd-ppc .rcard p { font-size: 15.5px; line-height: 1.65; color: var(--text); }
.cd-ppc .rcard b { display: block; margin-top: 14px; font-size: 14px; color: var(--muted); }

/* ── Reassurance band ───────────────────────────────────────────────────── */
.cd-ppc .reassure { text-align: left; }
.cd-ppc .reassure .lead { margin: 14px 0 0; color: #c8d6e8; }
.cd-ppc .reassure .btn { margin-top: 26px; }
.cd-ppc .reassure__quote { margin-top: 36px; display: flex; flex-direction: column; align-items: flex-start; gap: 14px; }
.cd-ppc .reassure__quote img { width: 56px; height: 56px; border-radius: 50%; object-fit: cover; display: block; }
.cd-ppc .reassure__quote blockquote { margin: 0; max-width: 560px; font-size: 19px; line-height: 1.6; color: #fff; font-weight: 500; font-style: normal; }
.cd-ppc .reassure__byline { margin-top: 2px; font-size: 14px; color: #9fb3cc; }
.cd-ppc .reassure__note { margin-top: 22px; font-size: 16px; font-weight: 700; color: #fff; }
/* .section--navy p sets #c8d6e8; the two notes and the byline are exceptions. */
.cd-ppc .section--navy p.reassure__note { color: #fff; }
.cd-ppc .section--navy p.reassure__byline { color: #9fb3cc; }

/* ── Process ────────────────────────────────────────────────────────────── */
.cd-ppc .psteps { margin-top: 48px; position: relative; }
.cd-ppc .psteps::before { content: ""; position: absolute; top: 27px; left: 0; right: 0; height: 1px; background: var(--line); }
.cd-ppc .pstep { position: relative; }
.cd-ppc .pstep__num { display: inline-flex; align-items: center; justify-content: center; width: 54px; height: 54px; border: 1.5px solid var(--accent); border-radius: 50%; font-size: 19px; font-weight: 700; color: var(--accent); background: #fff; position: relative; z-index: 1; }
.cd-ppc .pstep h3 { margin-top: 16px; font-size: 20px; font-weight: 750; color: var(--navy); }
.cd-ppc .pstep p { margin-top: 8px; }

/* ── Consequence cards ──────────────────────────────────────────────────── */
.cd-ppc .c6 { margin-top: 36px; }
.cd-ppc .c6 .c { background: var(--band); border: 1px solid var(--line); border-left: 3px solid var(--accent); border-radius: var(--radius); padding: 18px 20px; }
.cd-ppc .c6 h3 { font-size: 20px; font-weight: 750; color: var(--navy); }
.cd-ppc .c6 p { margin-top: 10px; }
.cd-ppc .take { display: block; font-size: 20px; font-weight: 600; color: var(--navy); line-height: 1.4; }
.cd-ppc .detail { display: block; margin-top: 6px; font-size: 15px; color: var(--soft); line-height: 1.6; font-weight: 400; }
.cd-ppc .closing { margin-top: 28px; font-size: 16.5px; color: var(--soft); font-weight: 600; }

.cd-ppc .qlist__head { margin-top: 32px; font-size: 20px; font-weight: 750; color: var(--navy); }

/* ── Question list ──────────────────────────────────────────────────────── */
.cd-ppc .qlist { margin-top: 20px; border-top: 1px solid var(--line); }
@media (min-width: 640px) { .cd-ppc .qlist { display: grid; grid-template-columns: 1fr 1fr; column-gap: 32px; } }
.cd-ppc .qrow { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 18px 4px; border-bottom: 1px solid var(--line); font-size: 17px; font-weight: 600; color: var(--navy); text-decoration: none; }
.cd-ppc .qrow:hover { background: var(--band); text-decoration: none; color: var(--navy); }
.cd-ppc .qrow .chev { flex: none; color: var(--accent); font-size: 15px; }

/* ── Practitioners ──────────────────────────────────────────────────────── */
.cd-ppc .pcards { margin-top: 36px; }
.cd-ppc .pcard { display: flex; gap: 18px; align-items: flex-start; border: 1px solid var(--line); border-radius: var(--radius); padding: 22px; }
.cd-ppc .pcard img { width: 96px; height: 96px; border-radius: 16px; flex: none; display: block; object-fit: cover; }
.cd-ppc .pcard h3 { font-size: 20px; font-weight: 750; color: var(--navy); }
.cd-ppc .pcard .role { font-size: 14px; font-weight: 650; color: var(--accent); margin-top: 2px; }
.cd-ppc .pcard .meta { font-size: 14px; color: var(--muted); margin-top: 6px; }
.cd-ppc .pcard p.bio { margin-top: 10px; font-size: 15px; color: var(--soft); line-height: 1.6; }

/* ── Fees ───────────────────────────────────────────────────────────────── */
.cd-ppc .feegrid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 32px; }
.cd-ppc .feecard { border: 1px solid var(--line); border-radius: var(--radius); padding: 26px; background: #fff; }
.cd-ppc .feecard b.amt { display: block; font-size: 30px; font-weight: 800; color: var(--navy); margin-top: 8px; }
.cd-ppc .feecard .lbl { font-size: 14px; font-weight: 700; color: var(--muted); text-transform: uppercase; letter-spacing: .06em; }
.cd-ppc .feecard .fine { display: block; margin-top: 10px; font-size: 15px; line-height: 1.6; color: var(--soft); }
.cd-ppc .section--navy .feecard .lbl { color: var(--muted); }
.cd-ppc .section--navy .feecard .fine { color: var(--soft); }
/* Colour comes from the token path: on a navy band `.section--navy p` resolves
   to the body-on-navy tint, exactly as every other paragraph there does. */
.cd-ppc .feenote { margin-top: 20px; font-size: 17px; color: var(--text); line-height: 1.7; max-width: var(--w-text); }

/* ── FAQ ────────────────────────────────────────────────────────────────── */
.cd-ppc .faq { margin-top: 36px; }
.cd-ppc .faq__item { border-bottom: 1px solid var(--line); }
.cd-ppc .faq__h { margin: 0; font: inherit; letter-spacing: normal; }
.cd-ppc .faq__q { width: 100%; display: flex; align-items: center; justify-content: space-between; gap: 20px; min-height: 64px; padding: 18px 0; background: none; border: 0; cursor: pointer; text-align: left; font-family: inherit; font-size: 20px; font-weight: 700; color: var(--navy); }
.cd-ppc .faq__sign { flex: none; width: 26px; height: 26px; border-radius: 50%; background: var(--accent-soft); color: var(--accent); display: grid; place-items: center; font-size: 16px; font-weight: 700; transition: transform .14s ease; }
.cd-ppc .faq__a { display: none; padding: 0 0 22px; max-width: var(--w-text); font-size: 15.5px; line-height: 1.7; color: var(--soft); }
.cd-ppc .faq__item.open .faq__a { display: block; }
.cd-ppc .faq__item.open .faq__sign { transform: rotate(45deg); }

/* ── Final CTA ──────────────────────────────────────────────────────────── */
.cd-ppc .finalcta { text-align: left; background: var(--band); }
.cd-ppc .finalcta .lead { margin: 16px 0 0; }
.cd-ppc .finalcta__row { display: flex; gap: 14px; justify-content: flex-start; margin-top: 28px; flex-wrap: wrap; }
.cd-ppc .finalcta small { display: block; margin-top: 18px; color: var(--muted); font-size: 14px; }
.cd-ppc .finalcta__note, .cd-ppc .finalcta__response { margin-top: 16px; font-size: 15px; font-weight: 650; color: var(--navy); }

/* ── Footer ─────────────────────────────────────────────────────────────── */
.cd-ppc .foot { background: #071630; color: #a3b6cd; padding: 44px 0; font-size: 14px; line-height: 1.75; }
.cd-ppc .foot a { color: #c8d6e8; }
.cd-ppc .foot p { margin-top: 10px; max-width: 80ch; }
.cd-ppc .foot strong { color: #fff; }

/* ── Mobile sticky CTA ──────────────────────────────────────────────────── */
.cd-ppc .sticky { position: fixed; left: 0; right: 0; bottom: 0; display: none; gap: 10px; padding: 10px 14px; background: #fff; border-top: 1px solid var(--line); box-shadow: 0 -6px 24px rgba(10, 31, 68, .12); z-index: 70; }
.cd-ppc .sticky.show { display: flex; }
.cd-ppc .sticky a, .cd-ppc .sticky button { flex: 1; min-height: 50px; border-radius: 10px; font-size: 15px; font-weight: 750; display: flex; align-items: center; justify-content: center; gap: 6px; border: 1px solid transparent; font-family: inherit; cursor: pointer; }
.cd-ppc .sticky .call { background: var(--navy); color: #fff; }
.cd-ppc .sticky .req { background: var(--orange); color: #fff; }
.cd-ppc .sticky a:hover { text-decoration: none; color: #fff; }

@media (max-width: 900px) {
	.cd-ppc .hero__grid { grid-template-columns: 1fr; }
	.cd-ppc .ppc__right { margin-left: 0; width: 100%; justify-content: space-between; }
	.cd-ppc .feegrid { grid-template-columns: 1fr; }
	.cd-ppc .section { padding: 48px 0; }
	.cd-ppc .reassure, .cd-ppc .finalcta { padding: 72px 0; }
}
</style>

<div class="cd-ppc" data-intent="<?php echo esc_attr( $cd_ppc_key ); ?>">

	<header class="ppc">
		<div class="wrap ppc__in">
			<div class="ppc__brand"><b>CompanyDebt</b><span>Licensed Insolvency Practitioners</span></div>
			<div class="ppc__right">
				<div class="ppc__prefer"><small>Prefer to speak now?</small><a href="tel:<?php echo esc_attr( $cd_ppc_telraw ); ?>"><?php echo esc_html( $cd_ppc_tel ); ?></a></div>
				<a class="btn ppc__call" href="tel:<?php echo esc_attr( $cd_ppc_telraw ); ?>">Call Now</a>
			</div>
		</div>
	</header>

	<!-- HERO -->
	<section class="hero">
		<div class="wrap hero__grid">
			<div>
				<p class="eyebrow"><?php echo esc_html( $cd_ppc['eyebrow'] ); ?></p>
				<h1><?php echo esc_html( $cd_ppc['h1'] ); ?></h1>
				<p class="hero__p"><?php echo esc_html( $cd_ppc['p1'] ); ?></p>
				<div class="trustline"><span>Free initial consultation</span><span>Confidential</span><span>No obligation</span></div>
				<p class="hero__reassure">You don't need to make any decisions on the first call.</p>
				<p class="hero__tel">Prefer to talk? Call <a href="tel:<?php echo esc_attr( $cd_ppc_telraw ); ?>"><?php echo esc_html( $cd_ppc_tel ); ?></a></p>
				<div class="hero__proof">
					<div class="rate rate--flush"><span class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 4.9 out of 5 on Reviews.io</div>
					<div class="hero__practitioner-row">
						<img src="<?php echo esc_url( $cd_ppc_assets . '/chris-andersen.webp' ); ?>" width="40" height="40" loading="eager" decoding="async" alt="Christopher Andersen, Licensed Insolvency Practitioner at Company Debt">
						<p class="hero__practitioner">Christopher Andersen, Licensed Insolvency Practitioner, IP No. 16070</p>
					</div>
				</div>
			</div>

			<!-- Lead capture. Fields are NOT hand-rolled: the Gravity Form owns
			     them, exactly as templates/quick-quote.php does with GF40. -->
			<div class="card" id="formCard">
				<h2>Tell Us What's Happening</h2>
				<p class="sub">Tell us the closest description of your company's situation and how to reach you.</p>

				<div class="cd-ppc-form">
				<?php if ( $cd_ppc_form_id ) : ?>
					<?php
					// field_values passes the ad intent through to the entry so
					// every lead records which ad group produced it. 'intent' is
					// the page slug; 'situation' is the matching situation value
					// from the design's step-1 radio set.
					$cd_ppc_field_values = 'intent=' . rawurlencode( $cd_ppc_slug ) . '&situation=' . rawurlencode( $cd_ppc['sit'] );
					echo do_shortcode(
						sprintf(
							'[gravityform id="%d" title="false" description="false" ajax="true" field_values="%s"]',
							(int) $cd_ppc_form_id,
							// NOT esc_attr(): this is a shortcode string, not an HTML
							// attribute. esc_attr() would turn the '&' separator into
							// '&#038;', which shortcode_parse_atts() does not decode,
							// so Gravity Forms would read a junk 'situation' key.
							// The two values are already rawurlencode()d above.
							$cd_ppc_field_values
						)
					);
					?>
				<?php else : ?>
					<!-- Gravity Form not configured. Set the form id with:
					     wp option update cd_ppc_form_id <form-id>
					     Until then this card renders without a form. -->
					<p class="cd-ppc-form-missing">The enquiry form is not configured on this environment yet.</p>
				<?php endif; ?>
				</div>

				<p class="microcopy microcopy--callback">Call before 5pm and we will call you back the same day.</p>
				<p class="microcopy">The initial consultation is free and there is no obligation to proceed.</p>
				<p class="microcopy">We'll use these details to contact you about your enquiry. See our <a href="/privacy-policy/">Privacy Policy</a> for more information.</p>
				<p class="hero__tel hero__tel--tight">Rather speak now? Call <a href="tel:<?php echo esc_attr( $cd_ppc_telraw ); ?>"><?php echo esc_html( $cd_ppc_tel ); ?></a></p>
			</div>
		</div>
	</section>

	<!-- TRUST BAR -->
	<section class="tbar">
		<div class="wrap">
			<div class="tbar__tier">
				<p class="tbar__label">Our insolvency practitioners are licensed by</p>
				<div class="tbar__marks">
					<a class="tbar__mark" href="https://www.insolvency-practitioners.org.uk/directory" target="_blank" rel="noopener" aria-label="Insolvency Practitioners Association register (opens in a new tab)">
						<img src="<?php echo esc_url( $cd_ppc_assets . '/ipa.png' ); ?>" width="89" height="30" loading="lazy" decoding="async" alt="Insolvency Practitioners Association">
					</a>
					<a class="tbar__mark" href="https://find.icaew.com/" target="_blank" rel="noopener" aria-label="ICAEW register (opens in a new tab)">
						<img src="<?php echo esc_url( $cd_ppc_assets . '/icaew.png' ); ?>" width="60" height="30" loading="lazy" decoding="async" alt="Institute of Chartered Accountants in England and Wales">
					</a>
				</div>
				<!-- No named-licence line here. The label above already scopes the marks to
				     our practitioners rather than to the brand, which was the regulatory
				     overstatement being fixed. The full statement is stated once in the
				     footer, and per practitioner on the practitioner cards. Repeating it
				     here was redundant. -->
			</div>
			<div class="tstrip grid4">
				<div class="titem"><svg class="ticon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true" focusable="false"><circle cx="12" cy="9" r="6"></circle><path d="M8.2 14.5 6.5 22l5.5-3 5.5 3-1.7-7.5"></path></svg><b>Licensed Insolvency Practitioners</b><p>Specialist advice for UK limited companies.</p></div>
				<div class="titem"><svg class="ticon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true" focusable="false"><path d="M4 5h16v11H8l-4 4V5Z"></path></svg><b>Free Initial Consultation</b><p>Understand your position before deciding what to do.</p></div>
				<div class="titem"><svg class="ticon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true" focusable="false"><circle cx="12" cy="8" r="4"></circle><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"></path></svg><b>Director-Focused Advice</b><p>Understand what company insolvency could mean for you personally.</p></div>
				<div class="titem"><svg class="ticon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true" focusable="false"><rect x="5" y="11" width="14" height="10" rx="2"></rect><path d="M8 11V7a4 4 0 0 1 8 0v4"></path></svg><b>Confidential</b><p>Making an enquiry does not put your company into liquidation.</p></div>
			</div>
		</div>
	</section>

	<!-- REVIEWS -->
	<section class="section section--band">
		<div class="wrap">
			<p class="eyebrow">Reviews</p>
			<h2 class="h2 h2--gap">Trusted by Directors Who've Been Here Before</h2>
			<p class="lead">Company insolvency is stressful enough without unclear advice. Our job is to explain your position plainly and help you understand what happens next.</p>
			<div class="rate">
				<!-- The Reviews.io score below is hard-coded, not fetched. Captured 2026-08-21.
				     Re-check it periodically and update this date, or it will drift out of step
				     with the live Reviews.io rating. The same figure appears in the hero. -->
				<span class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 4.9 out of 5 on <a href="https://www.reviews.io/" target="_blank" rel="noopener">Reviews.io</a>
				<img src="<?php echo esc_url( $cd_ppc_assets . '/reviewsio.png' ); ?>" width="36" height="20" loading="lazy" decoding="async" alt="Reviews.io">
			</div>
			<div class="rcards grid3">
				<div class="rcard"><span class="stars" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span><p>"After deciding to liquidate my company, I need expert advice... Their team guided me through the process from start to finish, providing me with all the knowledge and support I needed..."</p><b>Angela &middot; 14 May 2026 &middot; Reviews.io</b></div>
				<div class="rcard"><span class="stars" aria-label="5 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span><p>"I highly recommend Company Debt, I needed help with HMRC circumstances, they really took on board my struggles and guided me through everything, always kept me in the loop..."</p><b>Dan &middot; 2 April 2026 &middot; Reviews.io</b></div>
				<div class="rcard"><span class="stars" aria-label="4 out of 5 stars">&#9733;&#9733;&#9733;&#9733;&#9734;</span><p>"After a very stressful period during our business financial crisis... the team at Company Debt was our salvation. They helped us every step of the way to resolve our financial difficulties..."</p><b>Marcus &middot; 19 February 2026 &middot; Reviews.io</b></div>
			</div>
		</div>
	</section>

	<!-- REASSURANCE BAND -->
	<section class="section section--navy reassure">
		<div class="wrap wrap--text">
			<h2 class="h2">Talking to Us Doesn't Commit You to Liquidation</h2>
			<p class="lead">The first call is just that, a conversation.</p>
			<p class="bodytext">We'll ask what has happened, help you understand whether the company is insolvent and explain whether voluntary liquidation looks appropriate.</p>
			<p class="reassure__note">You don't have to decide anything on the call.</p>
			<div class="reassure__quote">
				<img src="<?php echo esc_url( $cd_ppc_assets . '/chris-andersen.webp' ); ?>" width="56" height="56" loading="lazy" decoding="async" alt="Christopher Andersen, Licensed Insolvency Practitioner at Company Debt">
				<blockquote>"Most of the directors I speak to have been putting off the call for months. Almost all of them say afterwards that they wish they had made it sooner."</blockquote>
				<p class="reassure__byline">Christopher Andersen, Licensed Insolvency Practitioner, IP No. 16070</p>
			</div>
			<!-- Accuracy: the FIRST call is answered by an answering service, so the
			     practitioners are not pulled off casework. Confirmed by the owner on
			     2026-08-21. The advice stage is with a licensed IP, and that is what
			     this line may claim. Do not restore "You will speak to a licensed
			     insolvency practitioner" here: this sits beside the hero form, so a
			     reader takes it as a promise about the call they are about to request. -->
			<p class="reassure__note">Your first call takes a few details. The advice itself comes from a licensed insolvency practitioner, not a call centre.</p>
			<a class="btn btn--solid cd-ppc-cta-26" href="#formCard">Request a Confidential Call</a>
		</div>
	</section>

	<!-- PROCESS -->
	<section class="section section--band">
		<div class="wrap">
			<p class="eyebrow">The Process</p>
			<h2 class="h2 h2--gap">What Happens When You Contact Us?</h2>
			<div class="psteps grid3">
				<div class="pstep"><span class="pstep__num" aria-hidden="true">01</span><h3>Tell Us What's Going On</h3><p><b class="take">You don't need to know which insolvency procedure you need.</b> <span class="detail">Explain the debts, creditor pressure and what has happened so far.</span></p></div>
				<div class="pstep"><span class="pstep__num" aria-hidden="true">02</span><h3>We'll Explain Where You Stand</h3><p><b class="take">We'll explain whether CVL appears appropriate and what it could mean for the company and for you.</b> <span class="detail">That conversation is with a licensed insolvency practitioner, not a call centre.</span></p></div>
				<div class="pstep"><span class="pstep__num" aria-hidden="true">03</span><h3>You Decide What to Do</h3><p><b class="take">Taking advice does not commit you to liquidation.</b> <span class="detail">We won't start anything unless you decide to proceed.</span></p></div>
			</div>
			<a class="btn btn--solid cd-ppc-cta-32" href="#formCard">Request a Confidential Call</a>
		</div>
	</section>

	<!-- DIRECTOR CONSEQUENCES -->
	<section class="section">
		<div class="wrap">
			<p class="eyebrow">Director Consequences</p>
			<h2 class="h2 h2--gap">Will I Be Personally Liable for Company Debts?</h2>
			<p class="lead">Usually, company debts remain the responsibility of the limited company rather than the director personally.</p>
			<p class="bodytext">There are some important exceptions. For example, we may need to look at:</p>
			<div class="c6 grid3">
				<div class="c"><h3>Personal Guarantees</h3><p><b class="take">Borrowing you have personally guaranteed.</b></p></div>
				<div class="c"><h3>Director's Loan Accounts</h3><p><b class="take">Money you owe to the company.</b></p></div>
				<div class="c"><h3>Certain Transactions Before Liquidation</h3><p><b class="take">Some transactions may need to be reviewed as part of the insolvency process.</b></p></div>
			</div>
			<p class="closing">If you're worried about something you've done as a director, tell us. The purpose of the first conversation is to understand the position, not to judge you.</p>
			<a class="btn btn--solid cd-ppc-cta-18" href="#formCard">Request a Confidential Call</a>
		</div>
	</section>

	<!-- CVL EXPLAINER + QUESTION LIST -->
	<section class="section section--band">
		<div class="wrap">
			<div class="text-cap">
				<p class="eyebrow">Creditors' Voluntary Liquidation</p>
				<h2 class="h2 h2--gap">What Is a CVL?</h2>
				<p class="lead">A Creditors' Voluntary Liquidation (CVL) is a way of formally closing a company that can no longer pay its debts.</p>
				<p class="bodytext">A licensed insolvency practitioner deals with the company's assets, creditors and closure.</p>
				<h3 class="qlist__head">Questions Directors Usually Want Answered</h3>
			</div>
			<div class="qlist">
				<?php foreach ( $cd_ppc_qlist as $cd_ppc_q ) : ?>
				<a class="qrow" href="#faqList" data-openfaq="<?php echo esc_attr( $cd_ppc_q['idx'] ); ?>"><?php echo esc_html( $cd_ppc_q['label'] ); ?><span class="chev" aria-hidden="true">&#8250;</span></a>
				<?php endforeach; ?>
			</div>
			<div class="text-cap">
				<p class="closing">These are exactly the issues we can discuss during the initial consultation.</p>
				<a class="btn btn--solid cd-ppc-cta-18" href="#formCard">Request a Confidential Call</a>
			</div>
		</div>
	</section>

	<!-- PRACTITIONERS -->
	<section class="section">
		<div class="wrap">
			<p class="eyebrow">Who You'll Speak To</p>
			<h2 class="h2 h2--gap">Speak to People Who Deal With Company Insolvency Every Day</h2>
			<p class="lead">CompanyDebt is operated by insolvency professionals specialising in limited companies and their directors.</p>
			<div class="pcards grid3">
				<div class="pcard">
					<img src="<?php echo esc_url( $cd_ppc_assets . '/chris-andersen.webp' ); ?>" width="96" height="96" loading="lazy" decoding="async" alt="Christopher Andersen, Licensed Insolvency Practitioner at Company Debt">
					<div>
						<h3>Christopher Andersen</h3>
						<p class="role">Licensed Insolvency Practitioner</p>
						<p class="meta">IP No. 16070 &middot; Licensed by the Insolvency Practitioners Association (IPA)</p>
						<p class="bio">Christopher is a licensed insolvency practitioner with experience advising directors of financially distressed and insolvent companies.</p>
					</div>
				</div>
				<div class="pcard">
					<img src="<?php echo esc_url( $cd_ppc_assets . '/nicki-meadows.jpg' ); ?>" width="96" height="96" loading="lazy" decoding="async" alt="Nicola Meadows, Licensed Insolvency Practitioner at Company Debt">
					<div>
						<h3>Nicola Meadows</h3>
						<p class="role">Licensed Insolvency Practitioner</p>
						<p class="meta">IP No. 9184 &middot; Licensed by the Institute of Chartered Accountants in England and Wales (ICAEW)</p>
						<p class="bio">Nicola is a licensed insolvency practitioner with experience advising directors of financially distressed and insolvent companies.</p>
					</div>
				</div>
			</div>
		</div>
	</section>

	<!-- FEES. Figures are canonical: data/statutory_fees.json (cvl_practitioner_fee,
	     cvl_disbursements, cvl_all_in). Do not restore the old range. -->
	<section class="section section--navy">
		<div class="wrap">
			<div class="text-cap">
				<p class="eyebrow">Fees</p>
				<h2 class="h2 h2--gap">How Much Does a CVL Cost?</h2>
				<div class="feegrid">
					<div class="feecard">
						<span class="lbl">Initial consultation</span>
						<b class="amt">&pound;0</b>
						<span class="fine">Free, confidential and with no obligation to proceed.</span>
					</div>
					<div class="feecard">
						<span class="lbl">CVL practitioner fee</span>
						<b class="amt">&pound;3,500 + VAT</b>
						<span class="fine">Our standard fixed fee for a straightforward case. Disbursements of &pound;500 to &pound;1,500 apply on top, so a straightforward CVL usually comes to roughly &pound;4,800 to &pound;6,000 once VAT is added.</span>
					</div>
				</div>
				<p class="feenote">Disbursements are necessary third-party costs, such as the bond, Gazette notices, the Companies House filing and statutory mailings. The exact cost depends on the circumstances of the company. <b>We'll explain the expected total cost clearly before you decide whether to proceed.</b></p>
			</div>
		</div>
	</section>

	<?php if ( $cd_ppc['show_context'] ) : ?>
	<!-- CONTEXTUAL BLOCK. Rendered only for intents that carry one; omitted
	     entirely on the CVL page, where it would repeat the hero. -->
	<section class="section" id="contextual">
		<div class="wrap">
			<?php if ( ! $cd_ppc_ctx_eyebrow_redundant ) : ?>
			<p class="eyebrow"><?php echo esc_html( $cd_ppc['ctx_eyebrow'] ); ?></p>
			<?php endif; ?>
			<h2 class="h2 h2--gap"><?php echo esc_html( $cd_ppc['ctx_h2'] ); ?></h2>
			<div><?php echo wp_kses_post( $cd_ppc['ctx_html'] ); ?></div>
		</div>
	</section>
	<?php endif; ?>

	<!-- FAQ. Order is resolved server-side; data-idx keeps the ORIGINAL index
	     so the question list above can deep-link to the right answer. -->
	<section class="section section--band">
		<div class="wrap">
			<p class="eyebrow">Frequently Asked Questions</p>
			<h2 class="h2 h2--gap">Questions Directors Often Ask</h2>
			<div class="faq" id="faqList">
				<?php foreach ( $cd_ppc_faq_order as $cd_ppc_pos => $cd_ppc_idx ) : ?>
					<?php
					$cd_ppc_faq  = $cd_ppc_faqs[ $cd_ppc_idx ];
					$cd_ppc_open = ( 0 === $cd_ppc_pos );
					$cd_ppc_qid  = 'cd-ppc-faq-q-' . $cd_ppc_idx;
					$cd_ppc_aid  = 'cd-ppc-faq-a-' . $cd_ppc_idx;
					?>
				<div class="faq__item<?php echo $cd_ppc_open ? ' open' : ''; ?>" data-idx="<?php echo esc_attr( $cd_ppc_idx ); ?>">
					<h3 class="faq__h">
						<button type="button" class="faq__q" id="<?php echo esc_attr( $cd_ppc_qid ); ?>" aria-expanded="<?php echo $cd_ppc_open ? 'true' : 'false'; ?>" aria-controls="<?php echo esc_attr( $cd_ppc_aid ); ?>">
							<?php echo esc_html( $cd_ppc_faq['q'] ); ?><span class="faq__sign" aria-hidden="true">+</span>
						</button>
					</h3>
					<div class="faq__a" id="<?php echo esc_attr( $cd_ppc_aid ); ?>" role="region" aria-labelledby="<?php echo esc_attr( $cd_ppc_qid ); ?>">
						<?php echo wp_kses_post( $cd_ppc_faq['a'] ); ?>
					</div>
				</div>
				<?php endforeach; ?>
			</div>
		</div>
	</section>

	<!-- FINAL CTA -->
	<section class="section finalcta" id="form">
		<div class="wrap wrap--text">
			<h2 class="h2">Find Out Where You Stand</h2>
			<p class="lead">You don't need to work this out on your own.</p>
			<p class="bodytext">Tell us what is happening with the company. We'll explain whether voluntary liquidation looks appropriate, what would happen next and anything you need to know about your own position.</p>
			<div class="trustline"><span>Free initial consultation</span><span>Confidential</span><span>No obligation</span></div>
			<p class="hero__reassure">You don't have to make a decision on the first call.</p>
			<div class="finalcta__row">
				<a class="btn btn--solid" href="#formCard">Request a Confidential Call</a>
				<a class="btn btn--ghost" href="tel:<?php echo esc_attr( $cd_ppc_telraw ); ?>">Call <?php echo esc_html( $cd_ppc_tel ); ?></a>
			</div>
			<p class="finalcta__response">Call before 5pm and we will call you back the same day.</p>
			<small>Taking advice does not commit you to liquidation.</small>
		</div>
	</section>

	<!-- FOOTER -->
	<footer class="foot">
		<div class="wrap">
			<p><strong>CompanyDebt Ltd</strong> &middot; <?php echo esc_html( $cd_ppc_tel ); ?> &middot; info@companydebt.com &middot; Level 18, 40 Bank Street, London, E14 5NR</p>
			<p>Company Debt is a trading name of Company Debt Ltd, registered in England &amp; Wales, company number 06352368. Company Debt Ltd is affiliated with AABRS Limited, a firm of Insolvency Practitioners. Christopher Andersen (IP No. 16070) is licensed to act as an Insolvency Practitioner in the UK by the Insolvency Practitioners Association. Nicola Meadows (IP No. 9184) is licensed to act as an Insolvency Practitioner in the UK by the Institute of Chartered Accountants in England and Wales.</p>
			<p><a href="/privacy-policy/">Privacy Policy</a> &middot; <a href="/terms-conditions/">Terms and Conditions</a> &middot; <a href="/cookie-policy/">Cookie Policy</a></p>
			<!-- ICAS "Members of" line removed: unverified claim, awaiting compliance confirmation -->
		</div>
	</footer>

	<!-- MOBILE STICKY CTA (shown below 900px once the hero has scrolled past) -->
	<div class="sticky" id="cdPpcSticky">
		<a class="call" href="tel:<?php echo esc_attr( $cd_ppc_telraw ); ?>">Call Now</a>
		<button type="button" class="req" id="cdPpcStickyReq">Request a Call</button>
	</div>

</div><!-- .cd-ppc -->

<script id="cd-ppc-behaviour">
/* Ported from the prototype: FAQ accordion, the question-list deep link and
 * the mobile sticky CTA. The intent switcher, the form-variant switcher and
 * the assessment/localStorage code are deliberately absent. */
document.addEventListener('DOMContentLoaded', function () {
	var root = document.querySelector('.cd-ppc');
	if (!root) { return; }

	/* The theme header is hidden on this template, so there is nothing sticky
	 * to scroll clear of. The prototype's 96px offset cleared its dev bar. */
	var SCROLL_OFFSET = 0;

	function setOpen(item, open) {
		if (!item) { return; }
		item.classList.toggle('open', open);
		var btn = item.querySelector('.faq__q');
		if (btn) { btn.setAttribute('aria-expanded', open ? 'true' : 'false'); }
	}

	/* Close every panel except the one passed in. The handoff spec calls this a
	 * single-open accordion (README section 13), so opening one must shut the
	 * rest. Without this the page can end up with all six panels open, which
	 * buries the final CTA far below the fold. */
	function closeOthers(keep) {
		root.querySelectorAll('.faq__item.open').forEach(function (other) {
			if (other !== keep) { setOpen(other, false); }
		});
	}

	/* FAQ accordion, single-open */
	root.querySelectorAll('.faq__q').forEach(function (btn) {
		btn.addEventListener('click', function () {
			var item = btn.closest('.faq__item');
			if (!item) { return; }
			var willOpen = !item.classList.contains('open');
			if (willOpen) { closeOthers(item); }
			setOpen(item, willOpen);
		});
	});

	/* "Questions Directors Usually Want Answered" deep link */
	function openFaq(idx) {
		var item = root.querySelector('.faq__item[data-idx="' + idx + '"]');
		if (!item) { return; }
		closeOthers(item);
		setOpen(item, true);
		var y = item.getBoundingClientRect().top + window.pageYOffset - SCROLL_OFFSET;
		window.scrollTo({ top: y, behavior: 'smooth' });
	}

	root.querySelectorAll('.qrow[data-openfaq]').forEach(function (row) {
		row.addEventListener('click', function (e) {
			e.preventDefault();
			openFaq(row.getAttribute('data-openfaq'));
		});
	});

	/* Mobile sticky CTA bar */
	var hero = root.querySelector('.hero');
	var sticky = document.getElementById('cdPpcSticky');
	if (hero && sticky) {
		var onScroll = function () {
			var past = window.scrollY > hero.offsetTop + hero.offsetHeight;
			sticky.classList.toggle('show', past && window.innerWidth <= 900);
		};
		window.addEventListener('scroll', onScroll, { passive: true });
		window.addEventListener('resize', onScroll);
		onScroll();
	}

	var stickyReq = document.getElementById('cdPpcStickyReq');
	var formCard = document.getElementById('formCard');
	if (stickyReq && formCard) {
		stickyReq.addEventListener('click', function () {
			var y = formCard.getBoundingClientRect().top + window.pageYOffset - SCROLL_OFFSET;
			window.scrollTo({ top: y, behavior: 'smooth' });
			formCard.style.outline = '2px solid #c25200';
			setTimeout(function () { formCard.style.outline = ''; }, 900);
		});
	}
});
</script>

<?php
get_footer();
