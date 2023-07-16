# IDA Multi-Tool

A multi-tool to troubleshoot and debug Identity Awareness blade issues in Check Point gateways.
 
## Usage

Make sure to use ida_mt_r81_20.py for Gaia R81.20 and above, as it uses Python 3
For lower versions user ida_mt.py

To start the script run: 

```bash
python ida_mt.py
```

You will be presented with the following menu:

```bash
------------------IDA Multi-Tool--------------------

Please choose option:
        0 - Exit.
        1 - Identity Sharing.
        2 - IDA tables.
        3 - LDAP
        4 - Test AD connectivity
        5 - IDA debugging
Your choice:
```

#### Options:
1. Collects all Identity Sharing related info that might be needed for investigation (except PDP/PEP debugs)
2. Selection between 2 operation - clearing the IDA kernel tables or dumping them into csv files
3. Allows performing LDAP search 
4. Preforms AD connectivity test that includes LDAP/DCE_RPC/DCOM/WMI
5. Collects extended PDP and PEP debugs, and also VPN related info (if selected in the prompt) 

All the collected files are located in /var/tmp/ida_debug
The folder structure is:
```bash
/var/tmp/ida_debug/debug/<date>/
/var/tmp/ida_debug/sharing/<date>/
/var/tmp/ida_debug/ldap/<date>/
/var/tmp/ida_debug/tables/<date>/
```



