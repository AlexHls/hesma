# HESMA Release Design Document

Created: 2026-05-05

HESMA, the Heidelberg Supernova Model Archive, is already in production at
hesma.h-its.org. This document captures the current alpha feature set, the
desired release direction, and a concrete backlog of bugs, technical debt, and
optimizations found by reading the codebase. It is intended as a living basis for
future release planning.

The main constraint for all work is production safety. The existing database and
mounted data directories must be treated as authoritative. Breaking changes are
acceptable only when the benefit is clear, the migration path is explicit, and a
tested rollback or recovery path exists.

## Current Product Shape

HESMA is a Django 5 application built from a Cookiecutter Django base. It has
three archive domains:

- Hydrodynamical simulations (`hesma.hydro`)
- Radiative-transfer simulations and synthetic observables (`hesma.rt`)
- Tracer-particle data for nuclear post-processing (`hesma.tracer`)

Supporting apps cover:

- Metadata: DOI and keyword management (`hesma.meta`)
- Public pages: home, FAQ, contact, upload selector, and user model overview
  (`hesma.pages`)
- User accounts and profile management (`hesma.users`)
- Deployment through Docker Compose with PostgreSQL, Redis, Traefik, nginx, and
  mounted `/data` storage
- Tests for models, forms, views, metadata helpers, users, and zip generation

The archive currently stores metadata in PostgreSQL while large model files live
on the filesystem under mounted storage directories:

- `/data/meta_data/`
- `/data/hydro_data/`
- `/data/tracer_data/`
- `/data/rt_data/`

## Existing Features

### Public Archive Browsing

- Public landing pages for hydro, RT, and tracer simulations.
- Latest-five sections and alphabetical model lists.
- Public detail pages with model description, reference, upload date, author,
  README link, and download actions.
- Home page with sticky and recent news.
- FAQ and contact pages.
- Legal notice and privacy pages.

### Upload And Ownership

- Authenticated users can access an upload selector.
- Upload access is intended to be controlled by Django groups:
  `hydro_user`, `tracer_user`, and `rt_user`.
- Model records store the uploading user.
- Detail pages expose edit/upload actions to owners for hydro and RT.
- "My Models" page lists simulations belonging to the current user.

### Data Types

- Hydro simulations can have 1D model files.
- RT simulations can have lightcurve and spectrum files.
- Hydro and RT files can be checked with `hesmapy` for format validity.
- Hydro and RT files can store precomputed Plotly JSON for interactive plots.
- Hydro and RT file models include thumbnail fields.
- Tracer simulations currently contain top-level metadata and README handling,
  but no concrete tracer data-file model exists in this codebase.

The current split into hydro, tracer, and RT simulations is historical. It is
useful as a user-facing classification, but it is not necessarily the right
long-term data model. A single physical supernova model or simulation campaign
may have hydrodynamic snapshots, tracer-particle outputs, radiative-transfer
calculations, derived 1D profiles, plots, and publication metadata attached to
the same underlying model.

### Downloads

- Per-model zip downloads for hydro and RT include metadata JSON, README, and
  associated data files.
- Tracer zip downloads include metadata JSON and README.
- Individual hydro 1D, RT lightcurve, and RT spectrum file downloads are
  available.
- README downloads are available for all three archive domains.

### Metadata

- DOI records store URL, author, title, and date.
- Keyword records are shared across archive domains.
- Upload/edit forms use modal DOI and keyword creation views.

### Operations

- Production Docker Compose stack is present.
- Production update script includes a database backup step before shutdown,
  rebuild, migration, and restart.
- Dedicated backup scripts exist for local and production databases.
- Redis cache is configured in production.
- HSTS, secure cookies, HTTPS redirect, and `ALLOWED_HOSTS` are configured for
  production.

## Release Goals

A full release should make HESMA dependable for three user groups:

- Researchers browsing and downloading model data.
- Approved contributors uploading and maintaining datasets.
- Administrators curating metadata, users, and operational health.

Release quality should mean:

- No unauthenticated or unauthorized write paths.
- Public downloads either succeed reliably or fail with clear 404/validation
  behavior.
- Data ingestion does not block request workers for long-running validation or
  plot generation.
- Archive metadata is searchable and filterable enough for scientific use.
- Dataset pages clearly expose citation, DOI, keywords, file contents, and
  data-format status.
- Users can discover models through queryable scientific metadata, not only
  through archive category pages.
- Hydro, tracer, and RT data can be linked when they belong to the same
  simulation, progenitor, explosion model, or publication.
- Production deployment, backup, restore, and migration steps are documented and
  rehearsed.
- Tests cover critical permissions, downloads, upload flows, and data migration
  behavior.

## Long-Term Archive Model

The key product concept should be a searchable collection of supernova models.
Hydro, tracer, and RT should be supported for all relevant simulations, but they
should become data-product types attached to a model rather than isolated top
level worlds.

A possible future structure:

- `Simulation` or `Model`: the canonical scientific object users search for and
  cite. It stores shared metadata such as name, aliases, description, authors,
  publications, DOI, keywords, progenitor information, explosion type, dimension,
  code, date, license, visibility, and owner.
- `DataProduct`: a typed attachment to a simulation. Product types include
  hydro snapshot, hydro 1D profile, tracer particles, RT lightcurve, RT
  spectrum, abundance table, initial conditions, derived plot, README, and
  miscellaneous supplementary file.
- `DataFile`: storage details for large raw files, including path, size,
  checksum, MIME type, format, compression, validation state, and provenance.
- `ProfileData` or `TabularData`: normalized database storage for small 1D
  profiles or simple tabular products, avoiding unnecessary file handling when
  the data is small enough to query and visualize directly.
- `MetadataValue` or explicit scientific metadata fields: structured values
  that support filtering by model type, progenitor mass, isotope set, time,
  wavelength range, viewing angle, dimensionality, code, metallicity, energy,
  ejecta mass, nickel mass, and similar domain-specific quantities.

This structure would allow one simulation page to show all associated hydro,
tracer, and RT products together. It would also allow cross-cutting search such
as "all Type Ia models with tracer data and RT spectra", "all 1D profiles for a
given publication", or "all models with a progenitor mass range and downloadable
lightcurves".

### Migration Strategy Toward A Unified Model

Because HESMA is already in production, this should be staged carefully:

- Keep existing hydro, tracer, and RT URLs working.
- Add a new canonical simulation/model layer without deleting the existing
  tables.
- Link existing `HydroSimulation`, `TracerSimulation`, and `RTSimulation`
  records to the new canonical object through nullable foreign keys.
- Backfill canonical records from existing production data.
- Make new search and detail pages read from the canonical layer while old
  detail pages redirect or present compatibility views.
- Only consider merging or removing historical tables after the new model has
  been used safely in production.

For the first release, a less disruptive alternative is to add a
`simulation_group` or `related_simulations` relation that links hydro, tracer,
and RT records belonging to the same physical model. This provides user-visible
value without requiring a major schema rewrite.

### Flexible Data Storage

The current implementation is geared toward 1D profiles and `hesmapy`
visualization. This is useful for quick plots, but the archive should support
multiple data scales:

- Large raw files: keep in mounted filesystem storage and track metadata in the
  database.
- Medium derived products: keep as files when they are naturally file-based, but
  store checksums, formats, and validation status.
- Small 1D profiles or tables: store directly in the database as structured
  arrays or rows when this improves querying, previewing, and plotting.
- Derived visualization data: cache generated Plotly JSON or thumbnails, but
  make it reproducible from the stored source product.

This does not require abandoning `hesmapy`. It should become one validator and
reader among several, used for supported formats while the database model stays
format-agnostic enough to grow.

## Planned And Recommended Features

### High Priority For Release

- Enforce server-side permissions on every upload, edit, metadata-create, and
  file-add view.
- Add owner checks for edit and child-file upload routes, not only template
  visibility.
- Add a real tracer data-file model and upload/download flow, or explicitly
  scope tracer to metadata-only for the first release.
- Add public search and filters across name, aliases, author, keyword, DOI,
  publication, archive/product type, date, and scientific metadata.
- Add a way to link hydro, tracer, and RT records that belong to the same
  physical simulation.
- Show DOI and keyword metadata on detail pages.
- Show attached data products on each model page, including whether hydro,
  tracer, and RT products exist.
- Make README optional paths safe everywhere, or make README required through a
  migration and data cleanup.
- Add dataset-level and file-level validation state to the UI.
- Add upload success redirects to the created/updated object instead of rendering
  static success pages with no object link.
- Add a release checklist covering backup, migration, smoke tests, and rollback.

### Medium Priority

- Add pagination to archive landing pages.
- Add stable, human-readable slugs while preserving existing integer ID URLs.
- Add structured metadata export endpoints, for example JSON metadata without
  downloading all files.
- Add per-file size, checksum, MIME type, original filename, and format version.
- Add structured scientific metadata fields for query filters. Initial fields
  should be chosen with domain users, but likely include simulation dimension,
  model class, progenitor/ejecta properties, code, data-product type,
  publication, and availability of hydro/tracer/RT outputs.
- Add direct database storage for small 1D profile or tabular products, with an
  export path that preserves the current file-download expectation.
- Generate thumbnails and Plotly JSON asynchronously.
- Add admin dashboards for invalid files, missing files, missing README files,
  and orphaned data.
- Add citation guidance per model, including DOIs and BibTeX-style metadata.
- Add a moderation/review state for contributed uploads before public listing.
- Add data-license metadata.
- Add sitemap and basic SEO metadata for public archive pages.
- Improve home page and archive copy for spelling, consistency, and scientific
  clarity.

### Later Enhancements

- Public API for model discovery and metadata.
- Unified canonical simulation/model pages that aggregate hydro, tracer, RT, and
  derived products.
- Bulk upload workflow for larger datasets.
- Download manifest and checksum verification.
- Dataset versioning and change history.
- Cross-links and dependency/provenance chains between hydro, tracer, and RT
  products from the same simulation campaign.
- DOI enrichment from Crossref/DataCite/arXiv where possible.
- Background job queue for validation, thumbnails, plot JSON, and large zip
  preparation.
- Metrics for downloads, upload failures, validation failures, and 500 errors.

## Production Data And Migration Policy

Prefer additive database changes:

- Add nullable fields first.
- Backfill existing data with management commands.
- Add constraints only after data is clean.
- Keep old URLs working when introducing slugs or new routes.
- Avoid renaming fields unless the release contains a clear migration and
  compatibility plan.

Before production migration:

- Take a verified database backup.
- Snapshot or verify `/var/www/hesma_data`.
- Run migrations against a restored production-like database locally.
- Run test suite and a manual smoke test of home, archive listings, detail pages,
  login, upload selector, model download, README download, and contact form.
- Deploy during a low-traffic window.

## Bugs And Risks Found In Code Review

### Fixed: write views are now protected server-side

Status: fixed in the first critical-bug implementation pass.

The hydro, RT, and tracer upload/edit views now enforce server-side access
control:

- Top-level upload views require login and the matching uploader group
  (`hydro_user`, `rt_user`, or `tracer_user`).
- Edit views require login and ownership of the edited simulation.
- Hydro and RT child-file upload views require the matching uploader group and
  ownership of the parent simulation.
- DOI and keyword modal create views now require the matching uploader group.

Implementation notes:

- Shared helpers live in `hesma/utils/permissions.py`.
- Focused regression tests were added for unauthenticated users, users without
  the required group, and non-owner edits/uploads.
- Docker test pipeline passed after this change.

### Fixed: tracer edit button is owner-only

Status: fixed in the first critical-bug implementation pass.

`hesma/templates/tracer/detail.html` now mirrors hydro and RT behavior: only the
simulation owner sees the edit button. The view also enforces ownership
server-side.

### Fixed: upload selector no longer 500s when groups are missing

Status: fixed in the first critical-bug implementation pass.

Previously, `hesma/templatetags/auth_extras.py` used `Group.objects.get`, so
missing groups raised `Group.DoesNotExist` while rendering
`hesma/templates/pages/upload.html`. The README says these groups must be
created manually.

`has_group` now checks membership through the user's group relation and returns
`False` when the group is absent. A regression test confirms the upload selector
renders when no upload groups exist.

Remaining optional hardening: add a data migration or management command to
create the expected upload groups during setup.

### High: child-file download routes do not verify parent ownership

Hydro and RT file download views fetch the file object by file ID only:

- `hesma/hydro/views.py:139`
- `hesma/rt/views.py:183`
- `hesma/rt/views.py:198`

The parent simulation ID in the URL is ignored. A mismatched URL can download a
file from another simulation if the child file ID is known.

Recommended fix: fetch through the parent relation, as the interactive plot
views already do.

### High: optional README fields are treated as mandatory

The models allow blank README files, but download and zip views access
`obj.readme.path` without checking whether a file exists:

- `hesma/hydro/views.py:49`
- `hesma/hydro/views.py:88`
- `hesma/rt/views.py:49`
- `hesma/rt/views.py:100`
- `hesma/tracer/views.py:47`

Recommended fix: either require README files with a migration after cleaning
existing records, or make all download and zip paths skip missing README files
and return 404 for direct README downloads.

### High: zip response construction is likely incorrect for non-streaming use

`hesma/utils/zip_generator.py:56` passes a generator to `HttpResponse`. Django
may consume this into content, but this pattern is unclear and can be fragile
for large files. Tracer zip creation uses an in-memory `BytesIO` instead,
creating inconsistent behavior.

Recommended fix: use `FileResponse` or `StreamingHttpResponse` consistently for
large archives, and use a shared zip utility for tracer, hydro, and RT.

### High: expensive validation and plot generation happen during uploads

Hydro and RT upload views call `hesmapy` validation and optional Plotly JSON
generation directly in the request:

- `hesma/hydro/views.py:123`
- `hesma/hydro/views.py:125`
- `hesma/rt/views.py:135`
- `hesma/rt/views.py:137`
- `hesma/rt/views.py:153`
- `hesma/rt/views.py:155`

For large scientific files this risks timeouts, worker exhaustion, and poor user
feedback.

Recommended fix: store the upload immediately, then process validation,
thumbnail, and plot generation in a background job. If a queue is too large a
change for the first release, add clear request timeouts, progress-free "pending"
states, and size limits first.

### Medium: duplicate domain code will slow feature work

Hydro, RT, and tracer repeat many fields and view patterns. Hydro and RT file
models also repeat validation, plot, thumbnail, and recent-date methods.

Recommended fix: avoid disruptive inheritance migrations for now. First extract
shared view/helper functions and tests. Consider abstract base models later only
if the schema impact is worth it.

### Medium: `News.was_published_recently` compares `DateField` to datetime

`hesma/pages/models.py:39` compares a `date` value to `timezone.now()`, a
datetime. This can raise or behave incorrectly depending on execution path.

Recommended fix: compare against `timezone.localdate()`.

### Medium: base template includes duplicate and mixed Bootstrap assets

`hesma/templates/base.html` includes Bootstrap 5 from CDN, local Bootstrap JS,
Popper, `bootstrap.bundle`, Bootstrap 4 modal form assets, Bootstrap 5 modal
form assets, and both minified and non-minified modal scripts. This increases
page weight and risks JavaScript conflicts.

Recommended fix: standardize on Bootstrap 5 assets only, keep one modal-form
integration, and load Plotly only on pages that render plots.

### Medium: cookie-consent inline template appears malformed

The inline script in `hesma/templates/base.html:80` to `hesma/templates/base.html:114`
contains spaced Django template delimiters like `{ % for ... % }`, which appear
to render as literal JavaScript rather than template control flow.

Recommended fix: simplify and test cookie banner rendering in a browser and with
template tests.

### Medium: public text contains typos

The home page contains user-visible typos:

- `Heidelber` should be `Heidelberg` at `hesma/templates/pages/home.html:16`.
- `HEASMA` should be `HESMA` at `hesma/templates/pages/home.html:21`.

Recommended fix: correct copy and scan the site for similar issues before
release.

### Medium: DOI field naming is unusual

The simulation models define a many-to-many field as `doi = ... name="DOI"`.
This means the Python attribute is `DOI`, while the source code visually suggests
`doi`. Existing migrations and templates may depend on this.

Recommended fix: defer a field rename until there is a migration plan. In the
short term, encapsulate DOI display in helpers/templates and document the current
field name.

### Medium: metadata create views have invalid edit success URLs

Several metadata modal create views use `reverse_lazy("hydro:hydro_edit")`,
`reverse_lazy("rt:rt_edit")`, or `reverse_lazy("tracer:tracer_edit")` without the
required object ID. These paths likely fail or cannot redirect correctly from an
edit modal.

Recommended fix: include the current object ID in modal URLs or redirect back to
the request path.

### Low: README storage documentation does not match current settings

README says storage directories can be configured through environment variables
such as `META_DATA_DIR`, but `config/settings/base.py` currently hard-codes
`/data/meta_data/`, `/data/hydro_data/`, `/data/tracer_data/`, and `/data/rt_data/`.

Recommended fix: either restore environment-driven storage paths or update the
README to match the production reality.

## Code Optimization Opportunities

- Replace repeated function-based views with shared service functions for:
  loading simulations, building zip metadata, downloading files, checking
  ownership, and handling upload success.
- Use `get_object_or_404` instead of manual `try`/`except` or raw `.get()` where
  missing objects should become 404s.
- Use `select_related("user")` and `prefetch_related("keywords", "DOI")` on
  listing/detail views once metadata is displayed.
- Add indexes for common search/filter fields after search requirements are
  defined.
- Store file metadata at upload time to avoid repeated filesystem calls.
- Add content-disposition filename quoting for names with spaces or special
  characters.
- Close files consistently or use Django `FileResponse`.
- Move Plotly loading out of the base template and into interactive plot pages.
- Add lint/test coverage for templates to catch malformed template tags.

## Test Gaps To Close Before Release

- Unauthorized upload and edit attempts for every archive domain. Initial
  regression tests added and passing for critical write paths.
- Group-permission checks for hydro/tracer/RT uploads. Initial regression tests
  added and passing.
- Owner-only edit and child-file upload behavior. Initial regression tests added
  and passing.
- Missing README behavior.
- Missing file behavior.
- Mismatched parent/child download URLs.
- DOI and keyword modal behavior on edit pages. Upload-page metadata create
  permissions are covered; edit-page redirect behavior still needs coverage.
- Contact form behavior with mocked email success and failure.
- Cookie banner template rendering.
- Realistic `hesmapy` validation behavior with small fixture files or mocks.
- Migration tests for any release-critical schema changes.

## Suggested Release Roadmap

### Phase 1: Stabilize Current Production Behavior

- Add server-side auth, group, and owner checks. Done for hydro, tracer, RT, and
  metadata create write paths.
- Fix missing group handling. Done for upload selector rendering.
- Fix tracer edit visibility. Done.
- Fix parent/child download lookup.
- Make README downloads safe.
- Correct home page typos.
- Add tests for the above. Initial permission tests are done and passing in the
  Docker pipeline.

This phase should be mostly non-breaking and can be deployed with low migration
risk.

### Phase 2: Make Data Discoverable And Trustworthy

- Display DOI and keyword metadata on detail pages.
- Add search, filters, and pagination.
- Add first-pass scientific metadata filters that work across hydro, tracer, and
  RT simulations.
- Add explicit related-simulation links so hydro, tracer, and RT records from the
  same model can be discovered together.
- Add validation state display.
- Add file size/checksum metadata.
- Add better metadata JSON export.
- Improve archive copy and citation guidance.

This phase may include additive migrations.

### Phase 3: Improve Upload And Processing Architecture

- Introduce a canonical model/simulation layer or a transitional grouping layer
  for hydro, tracer, and RT products.
- Add data-product abstractions for hydro snapshots, tracer data, RT lightcurves,
  RT spectra, and small directly stored profiles.
- Introduce background processing for validation, plot JSON, and thumbnails.
- Add upload review/moderation if public contributions are expected.
- Add operational dashboards for invalid/missing files.
- Consolidate duplicate code paths.

This phase may require a queue service and larger operational changes.

### Phase 4: Full Release Polish

- Add API endpoints or documented JSON exports.
- Add dataset versioning or change history.
- Add bulk upload and manifest workflow.
- Add richer provenance views showing how RT calculations or tracer outputs
  relate to hydro simulations.
- Add monitoring, metrics, and release runbooks.
- Run production-like restore and deployment rehearsal.

## Open Decisions

- Should tracer data remain metadata-only for the first release, or should it get
  concrete tracer file models now?
- Should HESMA introduce a new canonical `Simulation`/`Model` table, or should
  the first release use a lighter relation that links existing hydro, tracer,
  and RT records?
- Which metadata should be required, optional, and free-form for search? This
  should be decided with scientific users before adding strict constraints.
- Which 1D profile/table data is small and regular enough to store directly in
  PostgreSQL, and which data should always remain file-backed?
- Should uploads be private/reviewed until approved, or immediately public?
- Is user self-registration desired for release, or should accounts be
  administrator-created?
- Should README files become mandatory?
- Which metadata fields are scientifically required for every simulation?
- Should old integer URLs remain canonical, or should slugs become canonical
  while integer URLs redirect?
- Which file formats and `hesmapy` versions should be supported at release?

## Definition Of Release Ready

HESMA can be considered release-ready when:

- Critical and high-priority bugs above are fixed or explicitly accepted.
- Permission tests cover all write paths.
- Public browsing, downloads, uploads, edits, contact form, and admin workflows
  pass smoke testing against production-like data.
- A backup and restore has been tested.
- Any migrations have been run successfully on a restored production database.
- Known limitations are documented in user-facing docs or release notes.
- The release process is repeatable by following a checked-in runbook.
