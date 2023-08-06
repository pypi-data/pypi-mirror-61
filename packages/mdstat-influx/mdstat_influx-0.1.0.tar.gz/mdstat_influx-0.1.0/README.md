# mdstat-influx

read mdstat and format for line messages

Includes a script mdstat-influx.py.  When run, it outputs messages in a line format.

Example:

```
$ mdstat-influx.py
mdstat,device_name=md0,raid_level=raid5,hostname=tinfoil disks=3i,faulty_disks=0i,replacement_disks=0i,spare_disks=0i,faulty_pct=0.0
mdstat,device_name=md1,raid_level=raid5,hostname=tinfoil disks=3i,faulty_disks=0i,replacement_disks=0i,spare_disks=0i,faulty_pct=0.0
```
