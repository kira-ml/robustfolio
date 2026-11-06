# Data Licences and Redistribution Record — robustfolio

**Version:** 1.0
**Status:** Active
**Created:** 2026-11-06
**Last Updated:** 2026-11-06
**Owner:** Ken Ira Lacson Talingting
**Related decision:** `decision_log.md` DEC-20261106-042
**Related policy:** [`open_source_and_license_policy.md`](open_source_and_license_policy.md) v1.2 §2

This is a provenance and compliance record, **not legal advice**. It states what the
upstream terms say as read on 2026-11-06, what this repository does with each input,
and the conservative disposition the owner adopted. A lawyer's opinion could differ;
the project has chosen the narrower permission, not the wider one.

---

## 1. What is distributed, and what is not

**No third-party market data is redistributed by this repository or by its GitHub
releases.** The repository publishes code, documentation, derived tables, figures,
and identity digests. The frozen input snapshots remain local research artefacts.

The data files named below exist inside a local snapshot directory. They are not
committed to git, not attached to a release, and not served from the repository.

| File or artefact | Source | Governing terms | Redistributed? | Disposition |
|---|---|---|---|---|
| `prices_raw.parquet`, `actions.parquet` | Yahoo Finance, retrieved through `yfinance` on 2026-10-17 | [Yahoo Terms of Service](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html); [`yfinance` README](https://github.com/ranaroussi/yfinance) | **No** | Local only. Removed from the `v1.0.0` and `v1.1` releases on 2026-11-06. |
| `rf_dgs1mo.parquet` | FRED series `DGS1MO` (1-month US Treasury constant-maturity yield) | [FRED Terms of Use](https://fred.stlouisfed.org/legal/); [FRED API terms](https://fred.stlouisfed.org/docs/api/terms_of_use.html) | **No** | Local only. Removed with the snapshot archive. |
| `universe_pit.csv` | Fund issuers' fact sheets (SPDR, iShares), re-expressed by this project | Issuer website terms; the content is instrument metadata | **No** (the snapshot copy) | The public candidate list in `notes/pit_candidates_2026-10-17.csv` contains tickers and eligibility dates, not prices. |
| `manifest.json`, `quality_report.md` | This project | MIT | Yes, where published | Project-authored metadata. |
| `outcomes.csv`, `decisions.csv`, `country-sample/` tables | This project, computed from the snapshot | MIT for the project's authorship; inherits the data's provenance | **Yes** | Derived statistics and verdicts. They contain no raw price or yield observations. |
| `NOTICE.txt` | This project | MIT | Only inside a local archive | A provenance statement. It is not a licence and does not grant redistribution rights. |

---

## 2. Yahoo Finance

The prices and corporate actions were collected with the `yfinance` library. The
Yahoo Terms of Service restrict automated access and collection, and do not grant a
redistribution right. The operative concern is not only whether the data can be
*read*; it is whether a copy may be *published*.

Relevant language, as read on 2026-11-06:

> access or collect data … using any automated means … for any purpose without our
> express, prior permission.

The `yfinance` project's own README states that it is intended for personal use
only. That is a statement about the library, not a licence from Yahoo, and it does
not authorise this project to redistribute the resulting data.

**Disposition:** the snapshot is not published. The project does not rely on a
`NOTICE.txt`, attribution, or non-commercial use as a substitute for permission. A
notice is a statement about provenance; it cannot cure a missing licence.

---

## 3. FRED

The risk-free series is FRED `DGS1MO`. The underlying series is US government data,
and earlier versions of this project described it as "effectively public domain".
That description was too broad for the *service*: FRED's terms separately restrict
what a user may do with FRED content.

Relevant language, as read on 2026-11-06:

> Store, cache, or archive any portion of the FRED Services or FRED Content;
> provide any stored, cached, or archived portion … to any third party.

**Disposition:** the FRED-derived file is treated as not redistributable. It is not
published separately, and it is not included in any published archive. The
correction is recorded because the earlier "public domain" sentence was relied on in
the policy and in the release notes; it should not be repeated.

---

## 4. What changed on 2026-11-06

The project had published the frozen snapshots as release assets, with a
`NOTICE.txt`, on the theory that a non-commercial verification copy was permissible.
That theory did not survive a terms review: neither Yahoo nor FRED grants a
redistribution right, and a notice is not a licence.

Actions taken:

1. The `v1.1` release assets were deleted: the country snapshot archive and its
   `.sha256.txt` companion.
2. The `v1.0.0` release assets were deleted: the first-sample snapshot archive and
   its `.sha256` companion.
3. Both release bodies now state that the archive was removed and why.
4. The policy was revised to v1.2: **do not redistribute third-party data**.
5. The README, paper, published-run notes, reproduction request, and packaging
   notice no longer instruct a reader to download an archive.

The local archives in `dist/` are retained only for the owner's own verification.
They are gitignored and must not be uploaded again without a written licence that
permits redistribution.

---

## 5. What a reader can still check

The published tables, the code, the frozen configuration, and the verifier remain
available. The verifier still compares a fresh run against the committed tables, but
it needs a snapshot archive as input. Because the archives are not distributed, a
third party cannot run that end-to-end check from this repository alone.

That is a real degradation, and it is documented as one rather than hidden. The
alternative — publishing data the project has no right to publish — would make the
repository less honest, not more reproducible.

The identity of the input is retained so a reader can tell which snapshot produced
the numbers:

| Sample | Snapshot id | Bundle hash (data) | Archive SHA-256 (withdrawn distribution) |
|---|---|---|---|
| First sample (US ETFs) | `yahoo-usetf-2007-01-01_2026-09-30-2026-10-17-2ad06139` | `2ad0613913df9065b62ba2291abc391402c1eb13d36937ba8c2bbc09d637d707` | `7a3fc20991b664099ada44a308dfde57d8080994ff498e2f5a0dd98f2ecab77d` |
| Country sample | `yahoo-countryetf-1998-01-01_2026-09-30-2026-11-05-269a4565` | `269a45651ec04755b7954e8e99db7dc15f6bee92d4fe5a5e0707a67ce95de26c` | `d8bf3b43603f192c77b0a4e0f26223c64e70dce2aed17fb2ba2fe67f47a572ef` |

The archive digest identifies the **distribution** (data plus `NOTICE.txt`); the
bundle hash identifies the **data**. They are deliberately different (finding F31).
Because the notice template was revised on 2026-11-06 to say "not for
redistribution", a newly packed archive has a different archive digest while the
bundle hash and snapshot id stay the same. The owner's local re-packs are
`64ec80774730b5740f76c114fdebeae728f92862bd7a8165804ef0de2cf33093` (US ETFs) and
`591b7a7494ac6e858e9b8daefa15c59d044aa374d1efbce94b2f0ef8d9b554de` (country ETFs);
they are **not** published and must not be treated as distribution records. The
values in the table above identify the withdrawn distributions, not a download.

---

## 6. Review trigger

Re-examine this record if:

- Yahoo, FRED, or an issuer changes its terms;
- the owner obtains written permission, or a licensed data substitute, that permits
  redistribution;
- a third party objects to any published artefact;
- a new data source is added to the pipeline.

Any change to the disposition requires a new `decision_log.md` entry. The default is
**do not redistribute** until a licence says otherwise.
