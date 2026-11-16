# Engineering Decisions

Maintain this document across backlogs. Entries in this sample are for BL-P001-000002; if an existing repository has decisions, append instead of overwriting prior entries.

---

### Decision: Group monthly receipt activity by supplier and product

**Decision ID:** `D001` (sample ID; use next unused ID when merging)
**Backlog:** `BL-P001-000002`
**Date:** `2026-11-16`

#### Context
Supplier receipts may contain multiple products and suppliers. An aggregate that combines them would misrepresent per-product quantities.

#### Decision
Report one row per Supplier_ID, Product_ID and receipt calendar month, using Receipt_Date to derive the month.

#### Reason
The grain aligns with the requested reporting objective and retains supplier-specific quantities while preserving product separation.

#### Alternatives Considered
Product-month-only grouping would lose supplier breakdowns; daily grouping would be finer than the requirement.

#### Consequences
Summary quantities cannot be interpreted as comparable measures across distinct products or units.

---

### Decision: Apply an inclusive calendar-date reporting window

**Decision ID:** `D002` (sample ID; use next unused ID when merging)
**Backlog:** `BL-P001-000002`
**Date:** `2026-11-16`

#### Context
The consumer must request start and end dates without accidentally excluding activity on the final reporting day.

#### Decision
Interpret date arguments as an inclusive start and inclusive end of calendar day.

#### Reason
Users expect records on both entered dates to contribute to a summary.

#### Alternatives Considered
Half-open timestamp intervals are convenient internally but should not alter the user-facing date semantics.

#### Consequences
Date-time records must be handled carefully so that the final calendar day is not lost.
