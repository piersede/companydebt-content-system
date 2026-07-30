#!/usr/bin/env python3
"""Company Debt page builder — CLI entry point.

Insolvency / editorial pages: content is authored in drafts/{wp_id}_{slug}.html
and this builder assembles the WordPress block payload from it. (The original
Business Expert credit-card rendering engine has been removed; it had no place
on an insolvency site.)

Usage:
    python scripts/build_page.py --page liquidation
    python scripts/build_page.py --page liquidation --preview
    python scripts/build_page.py --page liquidation --publish
    python scripts/build_page.py --page liquidation --publish --id 7669
    python scripts/build_page.py --list
"""

import argparse
import importlib
import json
import os
import sys
import tempfile
from pathlib import Path

# Add scripts/ to path so cc_builder is importable
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

from page_runtime_metadata import resolve_page_runtime_metadata
from runtime_pack_router import resolve_runtime_context


# ── Page registry ──────────────────────────────────────────────────────
# Maps slug to module path in cc_builder.data.pages

PAGE_REGISTRY = {
    # ── Insolvency pages ────────────────────────────────────────────────
    # Slim configs (slug, title, page_type, wp_page_id, verification_date).
    # Page-class routing for these slugs is in scripts/page_runtime_metadata.py
    # SLUG_PAGE_CLASS_OVERRIDES.
    'liquidation': 'cc_builder.data.pages.liquidation',
    'members-voluntary-liquidation': 'cc_builder.data.pages.members_voluntary_liquidation',
    'creditors-voluntary-liquidation': 'cc_builder.data.pages.creditors_voluntary_liquidation',
    'uk-insolvency-statistics': 'cc_builder.data.pages.uk_insolvency_statistics',
    'cant-pay-vat': 'cc_builder.data.pages.cant_pay_vat',
    'winding-up-petitions': 'cc_builder.data.pages.winding_up_petitions',
    'problems-paying-corporation-tax-hmrc': 'cc_builder.data.pages.problems_paying_corporation_tax_hmrc',
    # The insolvency data hub: lives at /data/ (page 79845, slug 'data').
    # Module file keeps its company_insolvency.py name; the page slug is 'data'.
    'data': 'cc_builder.data.pages.company_insolvency',
    'winding-up-petition-tracker': 'cc_builder.data.pages.winding_up_petition_tracker',
    'dissolutions-vs-insolvencies': 'cc_builder.data.pages.company_dissolutions_vs_insolvencies',
    'payment-practices-late-payment': 'cc_builder.data.pages.payment_practices_late_payment',
    'cvl-statistics': 'cc_builder.data.pages.cvl_statistics',
    'compulsory-liquidation-statistics': 'cc_builder.data.pages.compulsory_liquidation_statistics',
    'administration-statistics': 'cc_builder.data.pages.administration_statistics',
    'company-insolvencies-by-sector': 'cc_builder.data.pages.company_insolvencies_by_sector',
    'construction-insolvency-statistics': 'cc_builder.data.pages.construction_insolvency_statistics',
    'furniture-insolvency-statistics': 'cc_builder.data.pages.furniture_insolvency_statistics',
    'restaurant-insolvency-statistics': 'cc_builder.data.pages.restaurant_insolvency_statistics',
    'road-haulage-insolvency-statistics': 'cc_builder.data.pages.road_haulage_insolvency_statistics',
    'recruitment-agency-insolvency-statistics': 'cc_builder.data.pages.recruitment_agency_insolvency_statistics',
    'temporary-staffing-agency-insolvency-statistics': 'cc_builder.data.pages.temporary_staffing_agency_insolvency_statistics',
    'motor-vehicle-repair-insolvency-statistics': 'cc_builder.data.pages.motor_vehicle_repair_insolvency_statistics',
    'cleaning-company-insolvency-statistics': 'cc_builder.data.pages.cleaning_company_insolvency_statistics',
    'hotel-insolvency-statistics': 'cc_builder.data.pages.hotel_insolvency_statistics',
    'estate-agency-insolvency-statistics': 'cc_builder.data.pages.estate_agency_insolvency_statistics',
    'it-consultancy-insolvency-statistics': 'cc_builder.data.pages.it_consultancy_insolvency_statistics',
    'management-consultancy-insolvency-statistics': 'cc_builder.data.pages.management_consultancy_insolvency_statistics',
    'architectural-engineering-insolvency-statistics': 'cc_builder.data.pages.architectural_engineering_insolvency_statistics',
    'personal-care-services-insolvency-statistics': 'cc_builder.data.pages.personal_care_services_insolvency_statistics',
    'sports-facility-insolvency-statistics': 'cc_builder.data.pages.sports_facility_insolvency_statistics',
    'medical-dental-practice-insolvency-statistics': 'cc_builder.data.pages.medical_dental_practice_insolvency_statistics',
    'creative-arts-entertainment-insolvency-statistics': 'cc_builder.data.pages.creative_arts_entertainment_insolvency_statistics',
    'amusement-recreation-insolvency-statistics': 'cc_builder.data.pages.amusement_recreation_insolvency_statistics',
    'real-estate-letting-investment-insolvency-statistics': 'cc_builder.data.pages.real_estate_letting_investment_insolvency_statistics',
    'freight-forwarding-logistics-insolvency-statistics': 'cc_builder.data.pages.freight_forwarding_logistics_insolvency_statistics',
    'retail-insolvency-statistics': 'cc_builder.data.pages.retail_insolvency_statistics',
    'are-directors-personally-liable-for-company-debts': 'cc_builder.data.pages.are_directors_personally_liable_for_company_debts',
    # ── Sector pages (/sectors/*) — clean-rebuild programme, posts not pages ──
    'construction': 'cc_builder.data.pages.construction_sector',
    'garden-centres': 'cc_builder.data.pages.garden_centres_sector',
    'hotels': 'cc_builder.data.pages.hotels_sector',
    'care-homes': 'cc_builder.data.pages.care_homes_sector',
    'automotive': 'cc_builder.data.pages.automotive_sector',
    'retail': 'cc_builder.data.pages.retail_sector',
    'restaurants': 'cc_builder.data.pages.restaurants_sector',
    'recruitment': 'cc_builder.data.pages.recruitment_sector',
    'gyms': 'cc_builder.data.pages.gyms_sector',
    'leisure': 'cc_builder.data.pages.leisure_sector',
    'childcare': 'cc_builder.data.pages.childcare_sector',
    'charity': 'cc_builder.data.pages.charity_sector',
    'professional-services': 'cc_builder.data.pages.professional_services_sector',
    'events': 'cc_builder.data.pages.events_sector',
    'taxi-companies': 'cc_builder.data.pages.taxi_companies_sector',
    'cleaning-contractors': 'cc_builder.data.pages.cleaning_contractors_sector',
    'haulage': 'cc_builder.data.pages.haulage_sector',
    'dry-cleaning-laundry': 'cc_builder.data.pages.dry_cleaning_laundry_sector',
    'property': 'cc_builder.data.pages.property_sector',
    'entertainment': 'cc_builder.data.pages.entertainment_sector',
    'fish-chip': 'cc_builder.data.pages.fish_chip_sector',
    'schools': 'cc_builder.data.pages.schools_sector',
    'travel': 'cc_builder.data.pages.travel_sector',
    'manufacturing': 'cc_builder.data.pages.manufacturing_sector',
    'energy': 'cc_builder.data.pages.energy_sector',
    # ── Data-led article rebuilds (posts, not pages) ────────────────────
    'pub-closures-in-the-uk': 'cc_builder.data.pages.pub_closures_in_the_uk',
    'how-much-does-liquidation-cost': 'cc_builder.data.pages.how_much_does_liquidation_cost',
    # -- Adopted existing pages: HMRC pressure and enforcement (/hmrc/*) --
    'accelerated-payment-notices-apn': 'cc_builder.data.pages.accelerated_payment_notices_apn',
    'can-hmrc-shut-down-my-business': 'cc_builder.data.pages.can_hmrc_shut_down_my_business',
    'cant-pay-paye': 'cc_builder.data.pages.cant_pay_paye',
    'controlled-goods-agreement': 'cc_builder.data.pages.controlled_goods_agreement',
    'corporation-tax-penalties': 'cc_builder.data.pages.corporation_tax_penalties',
    'distraint-order-notice': 'cc_builder.data.pages.distraint_order_notice',
    'hmrc': 'cc_builder.data.pages.hmrc',
    'hmrc-compliance-checks': 'cc_builder.data.pages.hmrc_compliance_checks',
    'hmrc-criminal-investigations': 'cc_builder.data.pages.hmrc_criminal_investigations',
    'hmrc-debt-enforcement-hub': 'cc_builder.data.pages.hmrc_debt_enforcement_hub',
    'hmrc-enforcement-action': 'cc_builder.data.pages.hmrc_enforcement_action',
    'hmrc-follower-notice': 'cc_builder.data.pages.hmrc_follower_notice',
    'hmrc-fraud-investigations': 'cc_builder.data.pages.hmrc_fraud_investigations',
    'hmrc-offices-contact-guide': 'cc_builder.data.pages.hmrc_offices_contact_guide',
    'hmrc-penalties-investigations': 'cc_builder.data.pages.hmrc_penalties_investigations',
    'hmrc-tax-investigations': 'cc_builder.data.pages.hmrc_tax_investigations',
    'hmrc-threatening-letters': 'cc_builder.data.pages.hmrc_threatening_letters',
    'joint-and-several-liability-for-unpaid-vat': 'cc_builder.data.pages.joint_and_several_liability_for_unpaid_vat',
    'notice-of-enforcement': 'cc_builder.data.pages.notice_of_enforcement',
    'pay-hmrc-or-suppliers-first': 'cc_builder.data.pages.pay_hmrc_or_suppliers_first',
    'personal-liability-notices': 'cc_builder.data.pages.personal_liability_notices',
    'security-bond-notices': 'cc_builder.data.pages.security_bond_notices',
    'security-bonds': 'cc_builder.data.pages.security_bonds',
    'tax-penalties': 'cc_builder.data.pages.tax_penalties',
    'time-to-pay-hmrc': 'cc_builder.data.pages.time_to_pay_hmrc',
    'understanding-hmrc-debt-collection': 'cc_builder.data.pages.understanding_hmrc_debt_collection',
    'vat-penalties': 'cc_builder.data.pages.vat_penalties',
    'what-can-hmrc-bailiffs-take': 'cc_builder.data.pages.what_can_hmrc_bailiffs_take',
    'what-happens-if-hmrc-freezes-your-business-bank-account': 'cc_builder.data.pages.what_happens_if_hmrc_freezes_your_business_bank_account',
    'what-happens-if-hmrc-rejects-your-time-to-pay-arrangement': 'cc_builder.data.pages.what_happens_if_hmrc_rejects_your_time_to_pay_arrangement',
    'what-happens-if-hmrc-sends-bailiffs-to-a-business': 'cc_builder.data.pages.what_happens_if_hmrc_sends_bailiffs_to_a_business',
    'what-happens-if-you-ignore-hmrc-letters': 'cc_builder.data.pages.what_happens_if_you_ignore_hmrc_letters',
    # -- Adopted existing pages: Liquidation section (/liquidation/*) --
    'alternatives-to-company-liquidation': 'cc_builder.data.pages.alternatives_to_company_liquidation',
    'am-i-solvent': 'cc_builder.data.pages.am_i_solvent',
    'bailiffs-high-court-enforcement-officers': 'cc_builder.data.pages.bailiffs_high_court_enforcement_officers',
    'business-bank-account-in-liquidation': 'cc_builder.data.pages.business_bank_account_in_liquidation',
    'can-a-director-be-sued-personally-by-creditors': 'cc_builder.data.pages.can_a_director_be_sued_personally_by_creditors',
    'can-a-supplier-force-my-company-into-liquidation': 'cc_builder.data.pages.can_a_supplier_force_my_company_into_liquidation',
    'can-directors-go-to-prison-for-company-debt': 'cc_builder.data.pages.can_directors_go_to_prison_for_company_debt',
    'can-directors-pay-themselves-before-liquidation': 'cc_builder.data.pages.can_directors_pay_themselves_before_liquidation',
    'can-i-be-sued-after-my-company-is-dissolved': 'cc_builder.data.pages.can_i_be_sued_after_my_company_is_dissolved',
    'can-i-choose-my-liquidator': 'cc_builder.data.pages.can_i_choose_my_liquidator',
    'can-i-liquidate-a-dormant-company': 'cc_builder.data.pages.can_i_liquidate_a_dormant_company',
    'can-i-liquidate-my-company-with-a-bounce-back-loan': 'cc_builder.data.pages.can_i_liquidate_my_company_with_a_bounce_back_loan',
    'can-i-start-a-new-company-after-liquidating-my-old-one': 'cc_builder.data.pages.can_i_start_a_new_company_after_liquidating_my_old_one',
    'can-you-liquidate-to-avoid-paying-suppliers': 'cc_builder.data.pages.can_you_liquidate_to_avoid_paying_suppliers',
    'cant-afford-to-liquidate': 'cc_builder.data.pages.cant_afford_to_liquidate',
    'ccj-when-going-insolvent': 'cc_builder.data.pages.ccj_when_going_insolvent',
    'company-pensions-and-liquidation': 'cc_builder.data.pages.company_pensions_and_liquidation',
    'company-property-and-real-estate-in-liquidation': 'cc_builder.data.pages.company_property_and_real_estate_in_liquidation',
    'company-restoration-after-liquidation': 'cc_builder.data.pages.company_restoration_after_liquidation',
    'company-strike-off-and-dissolution': 'cc_builder.data.pages.company_strike_off_and_dissolution',
    'company-vehicles-and-equipment-in-liquidation': 'cc_builder.data.pages.company_vehicles_and_equipment_in_liquidation',
    'compulsory-liquidation': 'cc_builder.data.pages.compulsory_liquidation',
    'creditor-meetings-in-liquidation': 'cc_builder.data.pages.creditor_meetings_in_liquidation',
    'cva-vs-strike-off-vs-liquidation': 'cc_builder.data.pages.cva_vs_strike_off_vs_liquidation',
    'director-conduct-review': 'cc_builder.data.pages.director_conduct_review',
    'directors-conduct-report-2': 'cc_builder.data.pages.directors_conduct_report_2',
    'directors-responsibilities-after-a-company-is-struck-off': 'cc_builder.data.pages.directors_responsibilities_after_a_company_is_struck_off',
    'hmrc-as-a-creditor-in-liquidation': 'cc_builder.data.pages.hmrc_as_a_creditor_in_liquidation',
    'how-to-challenge-a-liquidators-decisions-or-fees': 'cc_builder.data.pages.how_to_challenge_a_liquidators_decisions_or_fees',
    'how-to-choose-the-right-insolvency-procedure': 'cc_builder.data.pages.how_to_choose_the_right_insolvency_procedure',
    'how-to-prepare-for-company-liquidation': 'cc_builder.data.pages.how_to_prepare_for_company_liquidation',
    'how-to-prove-your-debt-in-company-liquidation': 'cc_builder.data.pages.how_to_prove_your_debt_in_company_liquidation',
    'insolvency-checklist': 'cc_builder.data.pages.insolvency_checklist',
    'insolvency-myths-debunked': 'cc_builder.data.pages.insolvency_myths_debunked',
    'insolvency-vs-bankruptcy': 'cc_builder.data.pages.insolvency_vs_bankruptcy',
    'intellectual-property-and-trading-assets-in-liquidation': 'cc_builder.data.pages.intellectual_property_and_trading_assets_in_liquidation',
    'leases-and-contracts-in-liquidation': 'cc_builder.data.pages.leases_and_contracts_in_liquidation',
    'liquidating-a-charity-or-non-profit': 'cc_builder.data.pages.liquidating_a_charity_or_non_profit',
    'liquidating-a-company-with-no-assets-or-bank-account-uk': 'cc_builder.data.pages.liquidating_a_company_with_no_assets_or_bank_account_uk',
    'liquidating-a-group-company-or-holding-company-in-the-uk': 'cc_builder.data.pages.liquidating_a_group_company_or_holding_company_in_the_uk',
    'liquidating-a-limited-liability-partnership': 'cc_builder.data.pages.liquidating_a_limited_liability_partnership',
    'liquidation-deadlines-and-time-limits': 'cc_builder.data.pages.liquidation_deadlines_and_time_limits',
    'liquidation-vs-dissolution-strike-off': 'cc_builder.data.pages.liquidation_vs_dissolution_strike_off',
    'liquidators-powers-and-duties': 'cc_builder.data.pages.liquidators_powers_and_duties',
    'list-of-liquidation-documents': 'cc_builder.data.pages.list_of_liquidation_documents',
    'paying-staff-but-not-hmrc-before-liquidation': 'cc_builder.data.pages.paying_staff_but_not_hmrc_before_liquidation',
    'redundancy-payments-for-directors-in-an-mvl': 'cc_builder.data.pages.redundancy_payments_for_directors_in_an_mvl',
    'seek-insolvency-advice-before-missing-payments': 'cc_builder.data.pages.seek_insolvency_advice_before_missing_payments',
    'should-i-close-my-company-or-try-to-save-it': 'cc_builder.data.pages.should_i_close_my_company_or_try_to_save_it',
    'timeline': 'cc_builder.data.pages.timeline',
    'uk-insolvency-flowchart': 'cc_builder.data.pages.uk_insolvency_flowchart',
    'uk-insolvency-glossary': 'cc_builder.data.pages.uk_insolvency_glossary',
    'voluntary-liquidation': 'cc_builder.data.pages.voluntary_liquidation',
    'voluntary-vs-compulsory-liquidation': 'cc_builder.data.pages.voluntary_vs_compulsory_liquidation',
    'what-happens-after-company-liquidation': 'cc_builder.data.pages.what_happens_after_company_liquidation',
    'what-happens-if-a-creditor-takes-me-to-court': 'cc_builder.data.pages.what_happens_if_a_creditor_takes_me_to_court',
    'what-happens-if-a-director-hides-company-assets': 'cc_builder.data.pages.what_happens_if_a_director_hides_company_assets',
    'what-happens-if-a-director-resigns-before-liquidation': 'cc_builder.data.pages.what_happens_if_a_director_resigns_before_liquidation',
    'what-happens-if-a-director-transfers-assets-before-insolvency': 'cc_builder.data.pages.what_happens_if_a_director_transfers_assets_before_insolvency',
    'what-happens-if-i-stop-paying-company-debts': 'cc_builder.data.pages.what_happens_if_i_stop_paying_company_debts',
    'what-happens-to-directors-in-liquidation': 'cc_builder.data.pages.what_happens_to_directors_in_liquidation',
    'what-happens-to-employees': 'cc_builder.data.pages.what_happens_to_employees',
    'whats-the-risk-of-being-disqualified-as-a-director': 'cc_builder.data.pages.whats_the_risk_of_being_disqualified_as_a_director',
    'when-should-a-director-stop-trading': 'cc_builder.data.pages.when_should_a_director_stop_trading',
    'which-creditors-get-paid-first': 'cc_builder.data.pages.which_creditors_get_paid_first',
    'winding-up-petition-vs-compulsory-liquidation': 'cc_builder.data.pages.winding_up_petition_vs_compulsory_liquidation',
    # -- Adopted existing pages: Director advice (/advice/*) --
    'advice-hub': 'cc_builder.data.pages.advice_hub',
    'business-restructuring': 'cc_builder.data.pages.business_restructuring',
    'can-a-director-be-made-bankrupt-if-a-business-fails': 'cc_builder.data.pages.can_a_director_be_made_bankrupt_if_a_business_fails',
    'can-director-criminal-record': 'cc_builder.data.pages.can_director_criminal_record',
    'can-personal-assets-of-directors-be-seized-from-a-ltd-company': 'cc_builder.data.pages.can_personal_assets_of_directors_be_seized_from_a_ltd_company',
    'debt-management-guide': 'cc_builder.data.pages.debt_management_guide',
    'directors-disqualification': 'cc_builder.data.pages.directors_disqualification',
    'directors-duties-to-creditors': 'cc_builder.data.pages.directors_duties_to_creditors',
    'directors-personal-guarantees': 'cc_builder.data.pages.directors_personal_guarantees',
    'frozen-bank-account': 'cc_builder.data.pages.frozen_bank_account',
    'funding-options-for-smes-in-the-uk': 'cc_builder.data.pages.funding_options_for_smes_in_the_uk',
    'get-free-business-debt-advice': 'cc_builder.data.pages.get_free_business_debt_advice',
    'hmrcs-ir35-investigations-different': 'cc_builder.data.pages.hmrcs_ir35_investigations_different',
    'how-to-legally-take-money-out-of-a-limited-company': 'cc_builder.data.pages.how_to_legally_take_money_out_of_a_limited_company',
    'insolvency-advice-for-directors': 'cc_builder.data.pages.insolvency_advice_for_directors',
    'losing-house-if-company-goes-bust': 'cc_builder.data.pages.losing_house_if_company_goes_bust',
    'misfeasance': 'cc_builder.data.pages.misfeasance',
    'overdrawn-directors-loan-accounts': 'cc_builder.data.pages.overdrawn_directors_loan_accounts',
    'personal-guarantee-insurance': 'cc_builder.data.pages.personal_guarantee_insurance',
    'personal-liability-for-cbils-loans': 'cc_builder.data.pages.personal_liability_for_cbils_loans',
    'preventing-company-director-disputes': 'cc_builder.data.pages.preventing_company_director_disputes',
    'the-risks-of-signing-a-personal-guarantee': 'cc_builder.data.pages.the_risks_of_signing_a_personal_guarantee',
    'unenforceable-personal-guarantee': 'cc_builder.data.pages.unenforceable_personal_guarantee',
    'what-are-a-company-directors-duties-to-avoid-and-disclose-conflicts-of-interest': 'cc_builder.data.pages.what_are_a_company_directors_duties_to_avoid_and_disclose_conflicts_of_interest',
    'what-are-fixed-and-floating-charges': 'cc_builder.data.pages.what_are_fixed_and_floating_charges',
    'what-are-phoenix-companies': 'cc_builder.data.pages.what_are_phoenix_companies',
    'what-are-the-duties-and-responsibilities-of-a-company-director': 'cc_builder.data.pages.what_are_the_duties_and_responsibilities_of_a_company_director',
    'what-is-a-directors-responsibility-for-accountancy-errors': 'cc_builder.data.pages.what_is_a_directors_responsibility_for_accountancy_errors',
    'what-is-limited-liability': 'cc_builder.data.pages.what_is_limited_liability',
    'what-is-the-companies-act-2006': 'cc_builder.data.pages.what_is_the_companies_act_2006',
    'writing-off-a-directors-loan-account': 'cc_builder.data.pages.writing_off_a_directors_loan_account',
    # -- Adopted existing pages: Insolvency reference (/insolvency/*) --
    'antecedent-transactions': 'cc_builder.data.pages.antecedent_transactions',
    'business-recovery-services': 'cc_builder.data.pages.business_recovery_services',
    'can-we-trade-out-of-insolvency': 'cc_builder.data.pages.can_we_trade_out_of_insolvency',
    'can-you-sell-your-insolvent-company': 'cc_builder.data.pages.can_you_sell_your_insolvent_company',
    'cease-trading': 'cc_builder.data.pages.cease_trading',
    'check-if-a-company-is-insolvent': 'cc_builder.data.pages.check_if_a_company_is_insolvent',
    'creditor-negotiations': 'cc_builder.data.pages.creditor_negotiations',
    'creditors-guides-to-insolvency-practitioners-fees': 'cc_builder.data.pages.creditors_guides_to_insolvency_practitioners_fees',
    'creditors-meeting': 'cc_builder.data.pages.creditors_meeting',
    'dealing-with-creditor-pressure': 'cc_builder.data.pages.dealing_with_creditor_pressure',
    'find-a-liquidator-near-me': 'cc_builder.data.pages.find_a_liquidator_near_me',
    'how-to-reduce-insolvency-risk': 'cc_builder.data.pages.how_to_reduce_insolvency_risk',
    'how-to-save-a-struggling-business': 'cc_builder.data.pages.how_to_save_a_struggling_business',
    'insolvency-act-1986': 'cc_builder.data.pages.insolvency_act_1986',
    'insolvent-company-investigations': 'cc_builder.data.pages.insolvent_company_investigations',
    'insolvent-company-owes-me-money': 'cc_builder.data.pages.insolvent_company_owes_me_money',
    'limited-company-bankruptcy': 'cc_builder.data.pages.limited_company_bankruptcy',
    'lpa-receivership': 'cc_builder.data.pages.lpa_receivership',
    'personal-liability-spouses-business-debts': 'cc_builder.data.pages.personal_liability_spouses_business_debts',
    'personally-liabilty-of-company-secretary': 'cc_builder.data.pages.personally_liabilty_of_company_secretary',
    'preferential-non-preferential-creditors': 'cc_builder.data.pages.preferential_non_preferential_creditors',
    'preferential-payments-during-insolvency': 'cc_builder.data.pages.preferential_payments_during_insolvency',
    'rescue-your-business-from-insolvency': 'cc_builder.data.pages.rescue_your_business_from_insolvency',
    'retail-industry-insolvency-trends': 'cc_builder.data.pages.retail_industry_insolvency_trends',
    'secured-vs-unsecured-creditors': 'cc_builder.data.pages.secured_vs_unsecured_creditors',
    'shareholders-liable-company-debts': 'cc_builder.data.pages.shareholders_liable_company_debts',
    'statement-of-affairs': 'cc_builder.data.pages.statement_of_affairs',
    'stop-or-avoid-insolvency': 'cc_builder.data.pages.stop_or_avoid_insolvency',
    'transactions-at-undervalue': 'cc_builder.data.pages.transactions_at_undervalue',
    'validation-order': 'cc_builder.data.pages.validation_order',
    'what-are-the-warning-signs-of-an-insolvent-company': 'cc_builder.data.pages.what_are_the_warning_signs_of_an_insolvent_company',
    'what-happens-if-a-company-cannot-pay-its-debts': 'cc_builder.data.pages.what_happens_if_a_company_cannot_pay_its_debts',
    'what-is-a-creditor': 'cc_builder.data.pages.what_is_a_creditor',
    'what-is-a-freezing-order-or-injunction': 'cc_builder.data.pages.what_is_a_freezing_order_or_injunction',
    'what-is-a-high-court-writ': 'cc_builder.data.pages.what_is_a_high_court_writ',
    'what-is-an-individual-voluntary-arrangement': 'cc_builder.data.pages.what_is_an_individual_voluntary_arrangement',
    'what-is-an-insolvency-practitioner': 'cc_builder.data.pages.what_is_an_insolvency_practitioner',
    'what-is-the-insolvency-service': 'cc_builder.data.pages.what_is_the_insolvency_service',
    'what-is-wrongful-trading': 'cc_builder.data.pages.what_is_wrongful_trading',
    'what-to-do-about-customer-insolvency': 'cc_builder.data.pages.what_to_do_about_customer_insolvency',
    # -- Adopted existing pages: Cash-flow pressure and Bounce Back Loans --
    'biggest-struggles-for-small-business-owners': 'cc_builder.data.pages.biggest_struggles_for_small_business_owners',
    'bounce-back-loan-fraud': 'cc_builder.data.pages.bounce_back_loan_fraud',
    'bounce-back-loan-hub': 'cc_builder.data.pages.bounce_back_loan_hub',
    'can-i-lose-my-house-with-a-bounce-back-loan': 'cc_builder.data.pages.can_i_lose_my_house_with_a_bounce_back_loan',
    'cant-afford-to-pay-suppliers-what-are-the-options': 'cc_builder.data.pages.cant_afford_to_pay_suppliers_what_are_the_options',
    'cant-afford-to-repay-business-loan': 'cc_builder.data.pages.cant_afford_to_repay_business_loan',
    'cant-pay-a-commercial-lease-or-rent': 'cc_builder.data.pages.cant_pay_a_commercial_lease_or_rent',
    'cant-pay-a-company-mortgage': 'cc_builder.data.pages.cant_pay_a_company_mortgage',
    'cant-pay-business-energy': 'cc_builder.data.pages.cant_pay_business_energy',
    'cant-pay-business-rates': 'cc_builder.data.pages.cant_pay_business_rates',
    'cant-pay-coronavirus-business-interruption-loan-cbils': 'cc_builder.data.pages.cant_pay_coronavirus_business_interruption_loan_cbils',
    'cant-pay-staff-wages': 'cc_builder.data.pages.cant_pay_staff_wages',
    'challenge-a-statutory-demand': 'cc_builder.data.pages.challenge_a_statutory_demand',
    'company-cash-flow-problems': 'cc_builder.data.pages.company_cash_flow_problems',
    'company-is-having-financial-difficulties': 'cc_builder.data.pages.company_is_having_financial_difficulties',
    'directors-liability-for-bounce-back-loans': 'cc_builder.data.pages.directors_liability_for_bounce_back_loans',
    'dissolving-a-company-with-bounce-back-loan': 'cc_builder.data.pages.dissolving_a_company_with_bounce_back_loan',
    'what-happens-if-i-default': 'cc_builder.data.pages.what_happens_if_i_default',
    'what-is-a-statutory-demand-against-a-company': 'cc_builder.data.pages.what_is_a_statutory_demand_against_a_company',
    'when-employers-cant-afford-redundancy-payments': 'cc_builder.data.pages.when_employers_cant_afford_redundancy_payments',
    'why-debt-is-not-always-a-bad-thing-for-your-business': 'cc_builder.data.pages.why_debt_is_not_always_a_bad_thing_for_your_business',
    # -- Adopted existing pages: Rescue, administration, CVA and pre-pack --
    'advantages-and-disadvantages': 'cc_builder.data.pages.advantages_and_disadvantages',
    'company-administration': 'cc_builder.data.pages.company_administration',
    'company-rescue-solutions': 'cc_builder.data.pages.company_rescue_solutions',
    'company-voluntary-arrangement': 'cc_builder.data.pages.company_voluntary_arrangement',
    'company-voluntary-arrangement-vs-administration-which-to-choose': 'cc_builder.data.pages.company_voluntary_arrangement_vs_administration_which_to_choose',
    'director-guarantees-in-a-cva': 'cc_builder.data.pages.director_guarantees_in_a_cva',
    'light-touch-administration': 'cc_builder.data.pages.light_touch_administration',
    'making-employees-redundant-cva': 'cc_builder.data.pages.making_employees_redundant_cva',
    'notice-of-intention-to-appoint-administrators': 'cc_builder.data.pages.notice_of_intention_to_appoint_administrators',
    'partnership-voluntary-arrangements': 'cc_builder.data.pages.partnership_voluntary_arrangements',
    'pre-packs': 'cc_builder.data.pages.pre_packs',
    'pros-and-cons': 'cc_builder.data.pages.pros_and_cons',
    'receivership-mean-business': 'cc_builder.data.pages.receivership_mean_business',
    'use-a-cva-to-close-a-company': 'cc_builder.data.pages.use_a_cva_to_close_a_company',
    'vs-administrative-receivership': 'cc_builder.data.pages.vs_administrative_receivership',
    'vs-cva': 'cc_builder.data.pages.vs_cva',
    'vs-liquidation': 'cc_builder.data.pages.vs_liquidation',
    'what-happens-if-a-cva-fails-mid-term': 'cc_builder.data.pages.what_happens_if_a_cva_fails_mid_term',
    'what-is-a-pre-pack-administration': 'cc_builder.data.pages.what_is_a_pre_pack_administration',
    'when-a-cva-fails': 'cc_builder.data.pages.when_a_cva_fails',
    # -- Adopted existing pages: Sample letters (/sample-letters/*) --
    'cease-trading-template': 'cc_builder.data.pages.cease_trading_template',
    'hold-action-on-my-account': 'cc_builder.data.pages.hold_action_on_my_account',
    'i-cannot-afford-to-repay-my-debt': 'cc_builder.data.pages.i_cannot_afford_to_repay_my_debt',
    'i-have-no-knowledge-of-this-debt': 'cc_builder.data.pages.i_have_no_knowledge_of_this_debt',
    'i-need-more-information-about-this-debt': 'cc_builder.data.pages.i_need_more_information_about_this_debt',
    'request-a-reduced-monthly-payment': 'cc_builder.data.pages.request_a_reduced_monthly_payment',
    'sample-letters-hub': 'cc_builder.data.pages.sample_letters_hub',
    'tell-debt-collector-to-stop-contacting-you': 'cc_builder.data.pages.tell_debt_collector_to_stop_contacting_you',
    'write-off-my-debt': 'cc_builder.data.pages.write_off_my_debt',
    # -- Adopted existing pages: Hubs, sector distress pages and standalone guides --
    'business-debt-advice': 'cc_builder.data.pages.business_debt_advice',
    'care-home-insolvency': 'cc_builder.data.pages.care_home_insolvency',
    'charity-non-profit-insolvency': 'cc_builder.data.pages.charity_non_profit_insolvency',
    'chinese-takeaway': 'cc_builder.data.pages.chinese_takeaway',
    'closing-a-limited-company': 'cc_builder.data.pages.closing_a_limited_company',
    'company-rescue-recovery-hub': 'cc_builder.data.pages.company_rescue_recovery_hub',
    'construction-insolvency': 'cc_builder.data.pages.construction_insolvency',
    'county-court-judgements': 'cc_builder.data.pages.county_court_judgements',
    'dealing-with-an-hmrc-winding-up-petition': 'cc_builder.data.pages.dealing_with_an_hmrc_winding_up_petition',
    'debt-charities-uk': 'cc_builder.data.pages.debt_charities_uk',
    'debt-creditor-pressure-hub': 'cc_builder.data.pages.debt_creditor_pressure_hub',
    'director-protection-hub': 'cc_builder.data.pages.director_protection_hub',
    'director-redundancy': 'cc_builder.data.pages.director_redundancy',
    'energy-provider-insolvency': 'cc_builder.data.pages.energy_provider_insolvency',
    'hospitality-restaurant-insolvency': 'cc_builder.data.pages.hospitality_restaurant_insolvency',
    'insolvency-news-commentary': 'cc_builder.data.pages.insolvency_news_commentary',
    'insolvency-test': 'cc_builder.data.pages.insolvency_test',
    'manufacturing-insolvency': 'cc_builder.data.pages.manufacturing_insolvency',
    'mental-health-debt-stress-support': 'cc_builder.data.pages.mental_health_debt_stress_support',
    'professional-services-insolvency': 'cc_builder.data.pages.professional_services_insolvency',
    'sector-specific-insolvency': 'cc_builder.data.pages.sector_specific_insolvency',
    'transport-haulage-insolvency': 'cc_builder.data.pages.transport_haulage_insolvency',
}
def load_page_config(slug: str) -> dict:
    """Import page module and return its PAGE_CONFIG dict."""
    if slug not in PAGE_REGISTRY:
        print(f"ERROR: Unknown page '{slug}'")
        print(f"Available pages: {', '.join(sorted(PAGE_REGISTRY.keys()))}")
        sys.exit(1)

    module = importlib.import_module(PAGE_REGISTRY[slug])
    return module.PAGE_CONFIG


def build_page(slug: str) -> tuple[str, dict]:
    """Build a single page and return (content, config)."""
    config = load_page_config(slug)
    page_type = config.get('page_type', '')

    if page_type in ('data_reference', 'definition', 'process_guide', 'hub'):
        # Insolvency and editorial pages: read content directly from the draft file.
        # Draft files live at drafts/{wp_page_id}_{slug}.html and contain WordPress
        # block content preceded by metadata comment lines (<!-- TITLE: ... --> etc.).
        wp_id = config.get('wp_page_id', '')
        slug = config.get('slug', '')
        draft_path = SCRIPTS_DIR.parent / 'drafts' / f'{wp_id}_{slug}.html'
        if not draft_path.exists():
            print(f"ERROR: Draft file not found: {draft_path}")
            sys.exit(1)
        raw = draft_path.read_text(encoding='utf-8')
        # Strip leading metadata comment lines and blank lines
        lines = raw.splitlines()
        content_lines = []
        past_header = False
        for line in lines:
            if not past_header:
                stripped = line.strip()
                if stripped.startswith('<!-- TITLE:') or stripped.startswith('<!-- POST ID:') or stripped.startswith('<!-- LINK:'):
                    continue
                if stripped == '' and not content_lines:
                    continue
                past_header = True
            content_lines.append(line)
        content = '\n'.join(content_lines).strip()
    else:
        print(f"ERROR: Unknown page type '{page_type}'")
        sys.exit(1)

    return content, config


def main():
    parser = argparse.ArgumentParser(
        description='Company Debt Credit Card Page Builder'
    )
    parser.add_argument(
        '--page', type=str,
        help='Page slug to build (e.g. low-apr, cashback)'
    )
    parser.add_argument(
        '--list', action='store_true',
        help='List all registered pages'
    )
    parser.add_argument(
        '--preview', action='store_true',
        help='Also generate a preview HTML file'
    )
    parser.add_argument(
        '--publish', action='store_true',
        help='Push to WordPress staging after building'
    )
    parser.add_argument(
        '--id', type=int, default=None,
        help='WP page/post ID to update (overrides config wp_page_id)'
    )
    parser.add_argument(
        '--show-runtime-packs', action='store_true',
        help='Show the system-decided runtime context for the requested page and task'
    )
    parser.add_argument(
        '--task', type=str, default='build',
        help='Task name for runtime context inspection (default: build)'
    )
    parser.add_argument(
        '--page-class', type=str, default=None,
        help='Optional Company Debt page class for runtime context inspection'
    )
    parser.add_argument(
        '--freshness-tier', type=str, default=None,
        help='Optional freshness tier for runtime context inspection'
    )
    args = parser.parse_args()

    if args.list:
        print('Registered pages:')
        for slug in sorted(PAGE_REGISTRY.keys()):
            config = load_page_config(slug)
            runtime_metadata = resolve_page_runtime_metadata(config, slug=config.get('slug', slug))
            wp_id = config.get('wp_page_id', '?')
            print(
                f'  {slug}  (WP ID: {wp_id}, type: {config.get("page_type", "?")}, '
                f'page_class: {runtime_metadata.page_class or "?"}, '
                f'freshness: {runtime_metadata.freshness_tier or "?"})'
            )
        return

    if not args.page:
        parser.print_help()
        sys.exit(1)

    config = load_page_config(args.page)
    runtime_metadata = resolve_page_runtime_metadata(config, slug=config.get('slug', args.page))

    if args.show_runtime_packs:
        runtime = resolve_runtime_context(
            args.task,
            page_type=config.get('page_type'),
            page_class=args.page_class or runtime_metadata.page_class,
            freshness_tier=args.freshness_tier or runtime_metadata.freshness_tier,
            slug=config.get('slug', args.page),
        )
        print('System-decided runtime context:')
        print(json.dumps(runtime, indent=2))

    # Build
    print(f'Building page: {args.page}')
    content, config = build_page(args.page)

    block_count = content.count('<!-- wp:')
    print(f'Generated {block_count} blocks, {len(content):,} chars')

    # Editorial / insolvency pages go through the Bernstein pipeline gate, not a
    # build-time assembler check.
    print(f'  (editorial page type: {config.get("page_type")}; quality gating via Bernstein)')

    # sector_statistics pages (the SIC-sector data family, e.g. furniture,
    # construction) carry a REAL automated gate — not just this printed claim.
    # Run it here and block --publish on a hard-fail, same discipline as the
    # bernstein.js gate for guide pages, calibrated for this page shape.
    gate_passed = True
    if runtime_metadata.page_class == 'sector_statistics':
        from sector_data_audit import audit_file, print_report
        draft_path = SCRIPTS_DIR.parent / 'drafts' / f"{config.get('wp_page_id')}_{config.get('slug')}.html"
        audit = audit_file(draft_path)
        print_report(audit)
        gate_passed = audit.gate_passed
        if not gate_passed:
            print(f'  SECTOR DATA GATE: FAIL ({audit.score}/{audit.max_score}) — see failures above.')
        else:
            print(f'  SECTOR DATA GATE: PASS ({audit.score}/{audit.max_score})')

    if args.publish and not gate_passed:
        print('ERROR: sector_statistics gate failed — publish blocked. Fix the flagged checks and rebuild.')
        sys.exit(1)

    # Write JSON output
    out_path = os.path.join(tempfile.gettempdir(), f'wp_push_{args.page}.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'content': content}, f, ensure_ascii=False)
    print(f'Written to {out_path}')

    # Preview
    if args.preview:
        preview_dir = SCRIPTS_DIR.parent / 'preview'
        preview_dir.mkdir(exist_ok=True)
        preview_path = preview_dir / f'{config["slug"]}.html'
        # Minimal preview wrapper
        preview_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{config["title"]}</title>
<meta name="description" content="{config.get("meta_description", "")}">
</head>
<body data-slug="{config["slug"]}">
<article class="entry-content container">
{content}
</article>
</body>
</html>'''
        with open(preview_path, 'w', encoding='utf-8') as f:
            f.write(preview_html)
        print(f'Preview: {preview_path}')

    # Publish
    if args.publish:
        from wp_publish import get_credentials, push_to_wordpress, create_authenticated_session
        creds = get_credentials(prod=False)

        wp_id = args.id or config.get('wp_page_id')
        if not wp_id:
            print('ERROR: No WP page ID. Use --id or set wp_page_id in page config.')
            sys.exit(1)

        # Build metadata excerpt to replace the theme deck/subtitle
        verify_date = config.get('verification_date', '')
        excerpt = f'Last reviewed {verify_date}' if verify_date else ''

        article = {
            'title': config['title'],
            'slug': config['slug'],
            'content': content,
            'meta_description': config.get('meta_description', ''),
            'category_name': '',
            'excerpt': excerpt,
        }

        push_to_wordpress(article, creds, status='publish', post_id=wp_id, post_type='pages')


if __name__ == '__main__':
    main()
