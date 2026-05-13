
hostname >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
date >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
echo "====================== PV-FS-PATHs-VGs-Lvs ========================="  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
lspv -u >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
df -g >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
lspath  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
lsvg -o  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
lvlstmajor  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
ls -l /dev/*vg*  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
ls -l /dev | grep "\->"  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
lsvg |awk '{print "lsvg -l "$1}'  | ksh >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
lspv -u | awk 'BEGIN{
    "hostname" | getline myhost
    printf "%-30s %-15s %-10s %-14s %-14s %-14s %-12s %-20s %-14s %-40s %-10s\n\n", "Hostname", "Disk", "Paths", "Capacity(GB)", "VG_Name", "Reserve_Policy","Queue_depth", "PVID", "Storage_Type", "Disk_SeriNo", "LUN_Status"
}{
    "lsattr -El "$1" | grep reserve_policy | cut -d\" \" -f 3" | getline policy
"lsattr -El "$1" | grep queue_depth | cut -d\" \" -f 6" | getline queue_depth
    "odmget -q \"name="$1" and attribute=unique_id\" CuAt | grep -i value | cut -d\"=\" -f2" | getline diskID
    "lsdev -l "$1" -r description | cut -d\" \" -f1" | getline manufacture
    "lspath -l "$1" | grep -ci enable" | getline numberOfpath
    "bootinfo -s "$1 | getline capacity
    LUN_Status = ($3 == "None" ? "standalone" : ($3 == "altinst_rootvg" ? "standalone" : $4))
    printf "%-30s %-15s %-10s %-14s %-14s %-14s %-12s %-20s %-14s %-40s %-10s\n", myhost, $1, numberOfpath, (capacity / 1024), $3, policy, queue_depth, $2, manufacture, substr(diskID, 3, (length(diskID) - 3)), LUN_Status
}' >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
echo "========================= HACMP ================================="  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
/usr/es/sbin/cluster/utilities/clRGinfo >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
/usr/es/sbin/cluster/utilities/cllsnode  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
/usr/es/sbin/cluster/utilities/clshowsrv -v  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
echo "======================= ADAPTERs ==================================="  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
ifconfig -a >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
lsdev -Cc adapter  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
lscfg -vpl fcs0  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
lscfg -vpl fcs1  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
echo vfcs | kdb | grep fcs  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
echo "=========================================================="  >> /root/$(hostname)_$(date +"%m%d%Y_%H%M").txt
