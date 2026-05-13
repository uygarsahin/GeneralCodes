Server STATUS
 ├─ powered_on
 │    ├─ poweroff → powered_off
 │    │              └─ rename (state:decom)
 │    ├─ poweron  → no-op
 │    └─ delete   → FAIL
 │
 ├─ powered_off
 │    ├─ poweron  → cleanup → powered_on
 │    ├─ poweroff → rename (noop state-wise)
 │    └─ delete   → delete → verify → deleted
 │
 ├─ not_found_in_console
 │    ├─ poweroff → skip
 │    ├─ poweron  → skip
 │    └─ delete   → skip
 │
 ├─ console_error
 │    └─ ALL OPS → FAIL
 │
 └─ unknown
      └─ ALL OPS → FAIL