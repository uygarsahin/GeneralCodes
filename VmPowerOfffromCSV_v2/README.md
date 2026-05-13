├── collections
│   └── requirements.yml
├── input.json
├── main.yml
├── README.md
├── tasks
│   ├── vc_ops.yml
│   └── vm_ops.yml
└── vars
    ├── main.yml
    └── vault.yml
=================================
csv_input
↓
validate ✅
↓
parse ✅
↓
vm_targets ✅
↓
grouped_targets ✅
↓
vc_ops ✅
↓
vm_ops ✅
↓
final_results ✅