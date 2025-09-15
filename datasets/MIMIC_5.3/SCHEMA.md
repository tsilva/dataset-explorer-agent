MIMIC OMOP CDM v5.3 — Data Dictionary

Overview

- Source: CSV files under `datasets/MIMIC_5.3/` representing the OMOP Common Data Model (CDM) v5.3.
- Scope: This dictionary reflects the discovered headers and standard OMOP v5.3 definitions.
- Types: `integer` (64-bit), `number` (floating), `string`, `date` (YYYY-MM-DD), `datetime` (YYYY-MM-DD HH:MM:SS). Empty fields indicate NULL.
- Keys: For each table, primary keys (PK) and foreign keys (FK) are noted where applicable.
- Concepts: Any column ending in `_concept_id` is an FK to `concept.concept_id` unless explicitly noted.
- De-identification: Dates are shifted (as seen in samples), and identifiers are hashed/large 64-bit integers.

Notes

- Headers are taken directly from the files; a few vocabulary tables use `..._DATE` capitalization in the header — they still represent `date` types.
- Some administrative tables (e.g., `cdm_source`, `metadata`) have no formal PK; they typically contain one or a few rows of metadata.
- Many IDs in event tables are 64-bit integers; ensure downstream systems use `BIGINT` or equivalent.

Table: person

- Description: One record per patient.
- PK: `person_id`
- Columns:
  - `person_id` (integer, PK) — Person identifier.
  - `gender_concept_id` (integer, FK) — Standard gender concept.
  - `year_of_birth` (integer) — Year of birth.
  - `month_of_birth` (integer) — Month of birth (1–12).
  - `day_of_birth` (integer) — Day of birth (1–31).
  - `birth_datetime` (datetime) — Timestamp of birth if available.
  - `race_concept_id` (integer, FK) — Standard race concept.
  - `ethnicity_concept_id` (integer, FK) — Standard ethnicity concept.
  - `location_id` (integer, FK to `location.location_id`) — Current/last known location.
  - `provider_id` (integer, FK to `provider.provider_id`) — Primary provider.
  - `care_site_id` (integer, FK to `care_site.care_site_id`) — Primary care site.
  - `person_source_value` (string) — Source system person identifier.
  - `gender_source_value` (string) — Source gender value.
  - `gender_source_concept_id` (integer, FK) — Source gender concept.
  - `race_source_value` (string) — Source race value.
  - `race_source_concept_id` (integer, FK) — Source race concept.
  - `ethnicity_source_value` (string) — Source ethnicity value.
  - `ethnicity_source_concept_id` (integer, FK) — Source ethnicity concept.

Table: observation_period

- Description: Continuous spans of observable time per person.
- PK: `observation_period_id`
- Columns:
  - `observation_period_id` (integer, PK) — Observation period identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `observation_period_start_date` (date) — Observation start.
  - `observation_period_end_date` (date) — Observation end.
  - `period_type_concept_id` (integer, FK) — Mechanism by which the period was derived.

Table: visit_occurrence

- Description: In-person or virtual care encounters.
- PK: `visit_occurrence_id`
- Columns:
  - `visit_occurrence_id` (integer, PK) — Visit identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `visit_concept_id` (integer, FK) — Visit concept (e.g., inpatient, outpatient, ER).
  - `visit_start_date` (date) — Visit start date.
  - `visit_start_datetime` (datetime) — Visit start timestamp.
  - `visit_end_date` (date) — Visit end date.
  - `visit_end_datetime` (datetime) — Visit end timestamp.
  - `visit_type_concept_id` (integer, FK) — Source/derivation type of the visit.
  - `provider_id` (integer, FK to `provider.provider_id`) — Attending provider.
  - `care_site_id` (integer, FK to `care_site.care_site_id`) — Care site of the visit.
  - `visit_source_value` (string) — Source visit value.
  - `visit_source_concept_id` (integer, FK) — Source visit concept.
  - `admitting_source_concept_id` (integer, FK) — Source of admission concept.
  - `admitting_source_value` (string) — Source of admission value.
  - `discharge_to_concept_id` (integer, FK) — Discharge disposition concept.
  - `discharge_to_source_value` (string) — Source discharge disposition.
  - `preceding_visit_occurrence_id` (integer, FK self) — Previous related visit.

Table: visit_detail

- Description: Sub-visit segments within a visit (e.g., bed/ward moves).
- PK: `visit_detail_id`
- Columns:
  - `visit_detail_id` (integer, PK) — Visit detail identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `visit_detail_concept_id` (integer, FK) — Concept for sub-visit type.
  - `visit_detail_start_date` (date) — Detail start date.
  - `visit_detail_start_datetime` (datetime) — Detail start timestamp.
  - `visit_detail_end_date` (date) — Detail end date.
  - `visit_detail_end_datetime` (datetime) — Detail end timestamp.
  - `visit_detail_type_concept_id` (integer, FK) — Derivation type of the record.
  - `provider_id` (integer, FK to `provider.provider_id`) — Provider.
  - `care_site_id` (integer, FK to `care_site.care_site_id`) — Care site.
  - `admitting_source_concept_id` (integer, FK) — Admission source concept.
  - `discharge_to_concept_id` (integer, FK) — Discharge destination concept.
  - `preceding_visit_detail_id` (integer, FK self) — Previous related detail.
  - `visit_detail_source_value` (string) — Source value for detail.
  - `visit_detail_source_concept_id` (integer, FK) — Source concept for detail.
  - `admitting_source_value` (string) — Source admission value.
  - `discharge_to_source_value` (string) — Source discharge value.
  - `visit_detail_parent_id` (integer, FK self) — Parent detail when hierarchical.
  - `visit_occurrence_id` (integer, FK to `visit_occurrence.visit_occurrence_id`) — Owning visit.

Table: condition_occurrence

- Description: Conditions (diagnoses) recorded for a person.
- PK: `condition_occurrence_id`
- Columns:
  - `condition_occurrence_id` (integer, PK) — Condition record identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `condition_concept_id` (integer, FK) — Standard condition concept.
  - `condition_start_date` (date) — Onset/start date.
  - `condition_start_datetime` (datetime) — Onset/start timestamp.
  - `condition_end_date` (date) — Resolution/end date.
  - `condition_end_datetime` (datetime) — Resolution/end timestamp.
  - `condition_type_concept_id` (integer, FK) — Source/derivation type of condition.
  - `stop_reason` (string) — Reason treatment stopped (if applicable).
  - `provider_id` (integer, FK to `provider.provider_id`) — Provider.
  - `visit_occurrence_id` (integer, FK to `visit_occurrence.visit_occurrence_id`) — Visit context.
  - `visit_detail_id` (integer, FK to `visit_detail.visit_detail_id`) — Sub-visit context.
  - `condition_source_value` (string) — Source condition value (e.g., ICD code).
  - `condition_source_concept_id` (integer, FK) — Source condition concept.
  - `condition_status_source_value` (string) — Source status value (e.g., rule-out).
  - `condition_status_concept_id` (integer, FK) — Status concept.

Table: drug_exposure

- Description: Drug exposures (prescriptions, administrations, dispensings).
- PK: `drug_exposure_id`
- Columns:
  - `drug_exposure_id` (integer, PK) — Drug exposure identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `drug_concept_id` (integer, FK) — Standard drug concept.
  - `drug_exposure_start_date` (date) — Exposure start date.
  - `drug_exposure_start_datetime` (datetime) — Exposure start timestamp.
  - `drug_exposure_end_date` (date) — Exposure end date.
  - `drug_exposure_end_datetime` (datetime) — Exposure end timestamp.
  - `verbatim_end_date` (date) — End date as recorded.
  - `drug_type_concept_id` (integer, FK) — Derivation/source type.
  - `stop_reason` (string) — Reason medication stopped.
  - `refills` (integer) — Number of refills.
  - `quantity` (number) — Quantity supplied/administered.
  - `days_supply` (integer) — Days supplied.
  - `sig` (string) — Directions for use free-text.
  - `route_concept_id` (integer, FK) — Route concept (e.g., oral, IV).
  - `lot_number` (string) — Lot number.
  - `provider_id` (integer, FK to `provider.provider_id`) — Provider.
  - `visit_occurrence_id` (integer, FK to `visit_occurrence.visit_occurrence_id`) — Visit context.
  - `visit_detail_id` (integer, FK to `visit_detail.visit_detail_id`) — Sub-visit context.
  - `drug_source_value` (string) — Source drug value/code.
  - `drug_source_concept_id` (integer, FK) — Source drug concept.
  - `route_source_value` (string) — Source route value.
  - `dose_unit_source_value` (string) — Source dose unit value.

Table: procedure_occurrence

- Description: Procedures performed on a person.
- PK: `procedure_occurrence_id`
- Columns:
  - `procedure_occurrence_id` (integer, PK) — Procedure record identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `procedure_concept_id` (integer, FK) — Standard procedure concept.
  - `procedure_date` (date) — Procedure date.
  - `procedure_datetime` (datetime) — Procedure timestamp.
  - `procedure_type_concept_id` (integer, FK) — Derivation/source type.
  - `modifier_concept_id` (integer, FK) — Modifier concept (if any).
  - `quantity` (number) — Quantity/number of procedures.
  - `provider_id` (integer, FK to `provider.provider_id`) — Provider.
  - `visit_occurrence_id` (integer, FK to `visit_occurrence.visit_occurrence_id`) — Visit context.
  - `visit_detail_id` (integer, FK to `visit_detail.visit_detail_id`) — Sub-visit context.
  - `procedure_source_value` (string) — Source procedure value/code.
  - `procedure_source_concept_id` (integer, FK) — Source procedure concept.
  - `modifier_source_value` (string) — Source modifier value.

Table: device_exposure

- Description: Uses or application of medical devices.
- PK: `device_exposure_id`
- Columns:
  - `device_exposure_id` (integer, PK) — Device exposure identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `device_concept_id` (integer, FK) — Standard device concept.
  - `device_exposure_start_date` (date) — Start date.
  - `device_exposure_start_datetime` (datetime) — Start timestamp.
  - `device_exposure_end_date` (date) — End date.
  - `device_exposure_end_datetime` (datetime) — End timestamp.
  - `device_type_concept_id` (integer, FK) — Derivation/source type.
  - `unique_device_id` (string) — Device identifier (e.g., UDI-DI).
  - `quantity` (number) — Quantity/duration as applicable.
  - `provider_id` (integer, FK to `provider.provider_id`) — Provider.
  - `visit_occurrence_id` (integer, FK to `visit_occurrence.visit_occurrence_id`) — Visit context.
  - `visit_detail_id` (integer, FK to `visit_detail.visit_detail_id`) — Sub-visit context.
  - `device_source_value` (string) — Source device value.
  - `device_source_concept_id` (integer, FK) — Source device concept.

Table: measurement

- Description: Structured measurements and test results.
- PK: `measurement_id`
- Columns:
  - `measurement_id` (integer, PK) — Measurement identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `measurement_concept_id` (integer, FK) — Standard measurement concept.
  - `measurement_date` (date) — Date of measurement.
  - `measurement_datetime` (datetime) — Timestamp of measurement.
  - `measurement_time` (string) — Time-of-day text if used.
  - `measurement_type_concept_id` (integer, FK) — Derivation/source type.
  - `operator_concept_id` (integer, FK) — Operator (e.g., ‘<’, ‘=’) concept.
  - `value_as_number` (number) — Numeric value.
  - `value_as_concept_id` (integer, FK) — Categorical value concept.
  - `unit_concept_id` (integer, FK) — Unit concept.
  - `range_low` (number) — Reference range low.
  - `range_high` (number) — Reference range high.
  - `provider_id` (integer, FK to `provider.provider_id`) — Provider.
  - `visit_occurrence_id` (integer, FK to `visit_occurrence.visit_occurrence_id`) — Visit context.
  - `visit_detail_id` (integer, FK to `visit_detail.visit_detail_id`) — Sub-visit context.
  - `measurement_source_value` (string) — Source test code/value.
  - `measurement_source_concept_id` (integer, FK) — Source measurement concept.
  - `unit_source_value` (string) — Source unit text.
  - `value_source_value` (string) — Source value text.

Table: observation

- Description: Generic clinical facts not captured elsewhere.
- PK: `observation_id`
- Columns:
  - `observation_id` (integer, PK) — Observation identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `observation_concept_id` (integer, FK) — Standard observation concept.
  - `observation_date` (date) — Observation date.
  - `observation_datetime` (datetime) — Observation timestamp.
  - `observation_type_concept_id` (integer, FK) — Derivation/source type.
  - `value_as_number` (number) — Numeric value.
  - `value_as_string` (string) — Text value.
  - `value_as_concept_id` (integer, FK) — Categorical value concept.
  - `qualifier_concept_id` (integer, FK) — Qualifier concept.
  - `unit_concept_id` (integer, FK) — Unit concept.
  - `provider_id` (integer, FK to `provider.provider_id`) — Provider.
  - `visit_occurrence_id` (integer, FK to `visit_occurrence.visit_occurrence_id`) — Visit context.
  - `visit_detail_id` (integer, FK to `visit_detail.visit_detail_id`) — Sub-visit context.
  - `observation_source_value` (string) — Source observation value.
  - `observation_source_concept_id` (integer, FK) — Source observation concept.
  - `unit_source_value` (string) — Source unit text.
  - `qualifier_source_value` (string) — Source qualifier text.

Table: specimen

- Description: Biological specimens obtained from persons.
- PK: `specimen_id`
- Columns:
  - `specimen_id` (integer, PK) — Specimen identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `specimen_concept_id` (integer, FK) — Specimen type concept (e.g., blood).
  - `specimen_type_concept_id` (integer, FK) — Derivation/source type.
  - `specimen_date` (date) — Collection date.
  - `specimen_datetime` (datetime) — Collection timestamp.
  - `quantity` (number) — Quantity collected.
  - `unit_concept_id` (integer, FK) — Unit concept.
  - `anatomic_site_concept_id` (integer, FK) — Body site concept.
  - `disease_status_concept_id` (integer, FK) — Disease status concept.
  - `specimen_source_id` (string) — Source specimen identifier.
  - `specimen_source_value` (string) — Source specimen value.
  - `unit_source_value` (string) — Source unit text.
  - `anatomic_site_source_value` (string) — Source body site text.
  - `disease_status_source_value` (string) — Source disease status text.

Table: note

- Description: Unstructured clinical notes.
- PK: `note_id`
- Columns:
  - `note_id` (integer, PK) — Note identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `note_date` (date) — Note date.
  - `note_datetime` (datetime) — Note timestamp.
  - `note_type_concept_id` (integer, FK) — Note type concept (e.g., discharge summary).
  - `note_class_concept_id` (integer, FK) — Note class concept (structure/format).
  - `note_title` (string) — Title of the note.
  - `note_text` (string) — Full note text.
  - `encoding_concept_id` (integer, FK) — Text encoding concept (e.g., UTF-8).
  - `language_concept_id` (integer, FK) — Language concept.
  - `provider_id` (integer, FK to `provider.provider_id`) — Authoring provider.
  - `visit_occurrence_id` (integer, FK to `visit_occurrence.visit_occurrence_id`) — Visit context.
  - `visit_detail_id` (integer, FK to `visit_detail.visit_detail_id`) — Sub-visit context.
  - `note_source_value` (string) — Source note value.

Table: note_nlp

- Description: NLP-derived annotations from notes.
- PK: `note_nlp_id`
- Columns:
  - `note_nlp_id` (integer, PK) — NLP annotation identifier.
  - `note_id` (integer, FK to `note.note_id`) — Source note.
  - `section_concept_id` (integer, FK) — Section concept (e.g., medications section).
  - `snippet` (string) — Short context around the match.
  - `offset` (string) — Character offset or range in note text.
  - `lexical_variant` (string) — Matched text.
  - `note_nlp_concept_id` (integer, FK) — Standard concept derived by NLP.
  - `note_nlp_source_concept_id` (integer, FK) — Source concept derived by NLP.
  - `nlp_system` (string) — NLP system name/version.
  - `nlp_date` (date) — NLP execution date.
  - `nlp_datetime` (datetime) — NLP execution timestamp.
  - `term_exists` (string) — Presence assertion (e.g., present/absent).
  - `term_temporal` (string) — Temporal context (e.g., history/current).
  - `term_modifiers` (string) — Additional qualifiers.

Table: death

- Description: Date and cause of death.
- PK: `person_id` (one-or-zero record per person)
- Columns:
  - `person_id` (integer, PK & FK to `person.person_id`) — Person who died.
  - `death_date` (date) — Date of death.
  - `death_datetime` (datetime) — Timestamp of death.
  - `death_type_concept_id` (integer, FK) — Source/derivation type of death record.
  - `cause_concept_id` (integer, FK) — Cause of death concept.
  - `cause_source_value` (string) — Source cause value.
  - `cause_source_concept_id` (integer, FK) — Source cause concept.

Table: payer_plan_period

- Description: Spans of payer and plan enrollment.
- PK: `payer_plan_period_id`
- Columns:
  - `payer_plan_period_id` (integer, PK) — Enrollment period identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `payer_plan_period_start_date` (date) — Start date.
  - `payer_plan_period_end_date` (date) — End date.
  - `payer_concept_id` (integer, FK) — Payer concept.
  - `payer_source_value` (string) — Source payer value.
  - `payer_source_concept_id` (integer, FK) — Source payer concept.
  - `plan_concept_id` (integer, FK) — Plan concept.
  - `plan_source_value` (string) — Source plan value.
  - `plan_source_concept_id` (integer, FK) — Source plan concept.
  - `sponsor_concept_id` (integer, FK) — Sponsor concept.
  - `sponsor_source_value` (string) — Source sponsor value.
  - `sponsor_source_concept_id` (integer, FK) — Source sponsor concept.
  - `family_source_value` (string) — Family coverage identifier.
  - `stop_reason_concept_id` (integer, FK) — Stop reason concept.
  - `stop_reason_source_value` (string) — Source stop reason value.
  - `stop_reason_source_concept_id` (integer, FK) — Source stop reason concept.

Table: condition_era

- Description: Aggregated spans of the same condition concept for a person.
- PK: `condition_era_id`
- Columns:
  - `condition_era_id` (integer, PK) — Condition era identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `condition_concept_id` (integer, FK) — Condition concept.
  - `condition_era_start_date` (date) — Era start.
  - `condition_era_end_date` (date) — Era end.
  - `condition_occurrence_count` (integer) — Number of underlying occurrences.

Table: drug_era

- Description: Aggregated spans of drug exposure for a specific drug concept.
- PK: `drug_era_id`
- Columns:
  - `drug_era_id` (integer, PK) — Drug era identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `drug_concept_id` (integer, FK) — Drug concept.
  - `drug_era_start_date` (date) — Era start.
  - `drug_era_end_date` (date) — Era end.
  - `drug_exposure_count` (integer) — Number of underlying exposures.
  - `gap_days` (integer) — Days between exposures within the era.

Table: dose_era

- Description: Aggregated spans of a drug exposure at a specific dose and unit.
- PK: `dose_era_id`
- Columns:
  - `dose_era_id` (integer, PK) — Dose era identifier.
  - `person_id` (integer, FK to `person.person_id`) — Person.
  - `drug_concept_id` (integer, FK) — Drug concept.
  - `unit_concept_id` (integer, FK) — Dose unit concept.
  - `dose_value` (number) — Dose value.
  - `dose_era_start_date` (date) — Era start.
  - `dose_era_end_date` (date) — Era end.

Table: cost

- Description: Costs and charges associated with clinical events.
- PK: `cost_id`
- Columns:
  - `cost_id` (integer, PK) — Cost record identifier.
  - `cost_event_id` (integer) — Identifier of the event being costed (ID in the domain table).
  - `cost_domain_id` (string) — Domain of the event (e.g., Visit, Procedure, Drug).
  - `cost_type_concept_id` (integer, FK) — Derivation/source type of cost.
  - `currency_concept_id` (integer, FK) — Currency concept (e.g., USD).
  - `total_charge` (number) — Billed charge.
  - `total_cost` (number) — Cost to provider.
  - `total_paid` (number) — Total amount paid.
  - `paid_by_payer` (number) — Amount paid by payer.
  - `paid_by_patient` (number) — Amount paid by patient.
  - `paid_patient_copay` (number) — Copay amount.
  - `paid_patient_coinsurance` (number) — Coinsurance amount.
  - `paid_patient_deductible` (number) — Deductible amount.
  - `paid_by_primary` (number) — Amount paid by primary payer.
  - `paid_ingredient_cost` (number) — Ingredient cost (drugs).
  - `paid_dispensing_fee` (number) — Dispensing fee (drugs).
  - `payer_plan_period_id` (integer, FK to `payer_plan_period.payer_plan_period_id`) — Related coverage period.
  - `amount_allowed` (number) — Allowed amount.
  - `revenue_code_concept_id` (integer, FK) — Revenue code concept.
  - `revenue_code_source_value` (string) — Source revenue code.
  - `drg_concept_id` (integer, FK) — Diagnosis related group concept.
  - `drg_source_value` (string) — Source DRG code/value.

Table: care_site

- Description: Physical location of care delivery units (e.g., wards, clinics).
- PK: `care_site_id`
- Columns:
  - `care_site_id` (integer, PK) — Care site identifier.
  - `care_site_name` (string) — Name of care site.
  - `place_of_service_concept_id` (integer, FK) — PoS concept.
  - `location_id` (integer, FK to `location.location_id`) — Location record.
  - `care_site_source_value` (string) — Source care site value.
  - `place_of_service_source_value` (string) — Source PoS value.

Table: provider

- Description: Individual care providers.
- PK: `provider_id`
- Columns:
  - `provider_id` (integer, PK) — Provider identifier.
  - `provider_name` (string) — Provider name.
  - `npi` (string) — National Provider Identifier.
  - `dea` (string) — DEA number.
  - `specialty_concept_id` (integer, FK) — Specialty concept.
  - `care_site_id` (integer, FK to `care_site.care_site_id`) — Affiliated care site.
  - `year_of_birth` (integer) — Provider year of birth.
  - `gender_concept_id` (integer, FK) — Gender concept.
  - `provider_source_value` (string) — Source provider identifier.
  - `specialty_source_value` (string) — Source specialty value.
  - `specialty_source_concept_id` (integer, FK) — Source specialty concept.
  - `gender_source_value` (string) — Source gender value.
  - `gender_source_concept_id` (integer, FK) — Source gender concept.

Table: location

- Description: Geographic locations (non-clinical addresses/areas).
- PK: `location_id`
- Columns:
  - `location_id` (integer, PK) — Location identifier.
  - `address_1` (string) — Address line 1.
  - `address_2` (string) — Address line 2.
  - `city` (string) — City.
  - `state` (string) — State/region.
  - `zip` (string) — Postal code.
  - `county` (string) — County.
  - `location_source_value` (string) — Source location value.

Table: observation (administrative) — metadata

- File: `metadata.csv`
- Description: CDM metadata elements and values.
- PK: none (logical uniqueness by combination of fields)
- Columns:
  - `metadata_concept_id` (integer, FK) — Metadata element concept.
  - `metadata_type_concept_id` (integer, FK) — Type of metadata.
  - `name` (string) — Metadata name/key.
  - `value_as_string` (string) — Value.
  - `value_as_concept_id` (integer, FK) — Value concept.
  - `metadata_date` (date) — Effective date.
  - `metadata_datetime` (datetime) — Effective timestamp.

Table: cdm_source

- Description: Provenance for the CDM instance.
- PK: none (typically single row)
- Columns:
  - `cdm_source_name` (string) — Name of the CDM source.
  - `cdm_source_abbreviation` (string) — Short name.
  - `cdm_holder` (string) — Organization holding the CDM.
  - `source_description` (string) — Description of source data.
  - `source_documentation_reference` (string) — Link/reference to docs.
  - `cdm_etl_reference` (string) — ETL process reference.
  - `source_release_date` (date) — Source data release date.
  - `cdm_release_date` (date) — CDM build date.
  - `cdm_version` (string) — CDM version (e.g., 5.3.1).
  - `vocabulary_version` (string) — Vocabulary bundle version.

Table: note and NLP relationships — fact_relationship

- File: `fact_relationship.csv`
- Description: Relationships between facts across domains.
- PK: none (rows are typically unique by full combination)
- Columns:
  - `domain_concept_id_1` (integer, FK) — Domain concept of the first fact.
  - `fact_id_1` (integer) — Identifier of the first fact (ID within its domain table).
  - `domain_concept_id_2` (integer, FK) — Domain concept of the second fact.
  - `fact_id_2` (integer) — Identifier of the second fact.
  - `relationship_concept_id` (integer, FK) — Relationship concept (e.g., ‘Is a’).

Table: cohort

- Description: Patient membership and time spans for cohort definitions.
- PK: none (logical key: `cohort_definition_id` + `subject_id` + `cohort_start_date`)
- Columns:
  - `cohort_definition_id` (integer, FK to `cohort_definition.cohort_definition_id`) — Cohort definition.
  - `subject_id` (integer, FK to `person.person_id`) — Person in cohort.
  - `cohort_start_date` (date) — Entry date into cohort.
  - `cohort_end_date` (date) — Exit date from cohort.

Table: cohort_attribute

- Description: Attributes attached to cohort membership episodes.
- PK: none (logical uniqueness by episode + attribute)
- Columns:
  - `cohort_definition_id` (integer, FK to `cohort_definition.cohort_definition_id`) — Cohort definition.
  - `subject_id` (integer, FK to `person.person_id`) — Person in cohort.
  - `cohort_start_date` (date) — Episode start date.
  - `cohort_end_date` (date) — Episode end date.
  - `attribute_definition_id` (integer, FK to `attribute_definition.attribute_definition_id`) — Attribute definition.
  - `value_as_number` (number) — Numeric value.
  - `value_as_concept_id` (integer, FK) — Concept value.

Table: cohort_definition

- Description: Definitions/specifications for cohorts.
- PK: `cohort_definition_id`
- Columns:
  - `cohort_definition_id` (integer, PK) — Cohort definition identifier.
  - `cohort_definition_name` (string) — Name.
  - `cohort_definition_description` (string) — Description.
  - `definition_type_concept_id` (integer, FK) — Definition type concept.
  - `cohort_definition_syntax` (string) — Serialized specification (e.g., JSON, SQL).
  - `subject_concept_id` (integer, FK) — Domain of subjects (typically Person).
  - `cohort_initiation_date` (date) — Date cohort becomes valid for use.

Table: attribute_definition

- Description: Definitions for cohort attribute values.
- PK: `attribute_definition_id`
- Columns:
  - `attribute_definition_id` (integer, PK) — Attribute definition identifier.
  - `attribute_name` (string) — Name.
  - `attribute_description` (string) — Description.
  - `attribute_type_concept_id` (integer, FK) — Type concept of attribute.
  - `attribute_syntax` (string) — Serialized specification.

Table: condition_era/drug_era dose linkage — dose_era

- See separate dose_era section above; included here for cross-reference with eras.

Table: vocabulary — concept

- File: `concept.csv`
- Description: Standardized concepts (clinical codes) across vocabularies.
- PK: `concept_id`
- Columns:
  - `concept_id` (integer, PK) — Concept identifier.
  - `concept_name` (string) — Human-readable name.
  - `domain_id` (string) — Domain of the concept (e.g., Condition, Drug).
  - `vocabulary_id` (string) — Vocabulary source (e.g., SNOMED, RxNorm).
  - `concept_class_id` (string) — Concept class within vocabulary.
  - `standard_concept` (string) — Standard status flag (e.g., ‘S’, ‘C’, or NULL).
  - `concept_code` (string) — Code in the source vocabulary.
  - `valid_start_DATE` (date) — Start of validity.
  - `valid_end_DATE` (date) — End of validity.
  - `invalid_reason` (string) — Reason if invalid (e.g., ‘D’ deprecated).

Table: vocabulary — concept_relationship

- File: `concept_relationship.csv`
- Description: Relationships between concepts.
- PK: none (rows typically unique by `concept_id_1`, `concept_id_2`, `relationship_id`, and/or validity range)
- Columns:
  - `concept_id_1` (integer, FK to `concept.concept_id`) — First concept.
  - `concept_id_2` (integer, FK to `concept.concept_id`) — Second concept.
  - `relationship_id` (string) — Relationship type (e.g., Maps to, Is a).
  - `valid_start_DATE` (date) — Start of validity.
  - `valid_end_DATE` (date) — End of validity.
  - `invalid_reason` (string) — Reason if invalid.

Table: vocabulary — vocabulary

- File: `vocabulary.csv`
- Description: Vocabulary metadata.
- PK: `vocabulary_id`
- Columns:
  - `vocabulary_id` (string, PK) — Vocabulary identifier.
  - `vocabulary_name` (string) — Vocabulary name.
  - `vocabulary_reference` (string) — Reference/source of vocabulary.
  - `vocabulary_version` (string) — Version string.
  - `vocabulary_concept_id` (integer, FK to `concept.concept_id`) — Concept for this vocabulary.

Table: location/care site/provider linkage — care_site, provider, location

- See individual sections above; included here for cross-reference.

Table: device/specimen linkage — device_exposure, specimen

- See individual sections above; included here for cross-reference.

Table: note tables — note, note_nlp

- See individual sections above; included here for cross-reference.

Additional Tables Present

- `cohort.csv` — See cohort section.
- `metadata.csv` — See metadata section.
- `cdm_source.csv` — See cdm_source section.

Constraints Summary (Foreign Keys)

- Common FKs to `person.person_id`: in `visit_occurrence`, `visit_detail`, `condition_occurrence`, `drug_exposure`, `procedure_occurrence`, `device_exposure`, `measurement`, `observation`, `specimen`, `payer_plan_period`.
- Common FKs to `visit_occurrence.visit_occurrence_id`: in `visit_detail`, `condition_occurrence`, `drug_exposure`, `procedure_occurrence`, `device_exposure`, `measurement`, `observation`, `note`.
- Common FKs to `visit_detail.visit_detail_id`: in `condition_occurrence`, `drug_exposure`, `procedure_occurrence`, `device_exposure`, `measurement`, `observation`, `note`.
- Provider/care site/location FKs: `provider.provider_id` referenced by many clinical tables; `care_site.care_site_id` referenced by `visit_occurrence`, `visit_detail`, `provider`, `person`; `location.location_id` referenced by `person`, `care_site`.
- Concept FKs: any `_concept_id` typically references `concept.concept_id` (e.g., condition, drug, route, unit, type concepts).

Implementation Notes

- Load order suggestion: `concept`/`vocabulary` → `location`/`care_site`/`provider` → `person` → `observation_period` → `visit_occurrence` → `visit_detail` → clinical facts (`condition_occurrence`, `drug_exposure`, `procedure_occurrence`, `device_exposure`, `measurement`, `observation`, `specimen`, `note`, `note_nlp`) → eras (`condition_era`, `drug_era`, `dose_era`) → `payer_plan_period`, `death`, `cost` → utilities (`fact_relationship`, `metadata`, `cdm_source`, cohorts).
- ID sizes: Treat IDs as 64-bit; avoid 32-bit integer types.
- Date handling: Dates may be shifted; do not mix `date` and `datetime` columns when loading to strongly typed stores.

