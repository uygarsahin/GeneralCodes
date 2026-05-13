lspv -u | awk 'BEGIN{
    "hostname" | getline myhost
    printf "%-30s %-15s %-10s %-14s %-14s %-14s %-12s %-20s %-14s %-40s %-10s\n\n", "Hostname", "Disk", "Paths", "Capacity(GB)", "VG_Name", "Reserve_Policy","Queue_depth", "PVID", "Storage_Type", "Disk_SeriNo", "LUN_Status"
}{
    "lsattr -El "$1" | grep reserve_policy | cut -d\" \" -f 3" | getline policy
"lsattr -El "$1" | grep queue_depth | cut -d\" \" -f 6" | getline queue_depth
    "odmget -q \"name="$1" and attribute=unique_id\" CuAt | grep -i value | cut -d\"=\" -f2" | getline diskID
    "lsdev -l "$1" -r description | cut -d\" \" -f1" | getline manufacture
    "lspath -l "$1" | grep -ci enable" | getline numberOfpath
    "sudo bootinfo -s "$1 | getline capacity
    LUN_Status = ($3 == "None" ? "standalone" : ($3 == "altinst_rootvg" ? "standalone" : $4))
    printf "%-30s %-15s %-10s %-14s %-14s %-14s %-12s %-20s %-14s %-40s %-10s\n", myhost, $1, numberOfpath, (capacity / 1024), $3, policy, queue_depth, $2, manufacture, substr(diskID, 3, (length(diskID) - 3)), LUN_Status
}'
