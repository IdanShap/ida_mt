from getpass import getpass
from os import system as sys
from os import path
from datetime import datetime


def identity_sharing():
    date = datetime.now()
    dir = "/var/tmp/ida_dbg/sharing/" + date.strftime("%d-%m-%y_%H-%M") + "/"
    if not path.isdir("/var/tmp/ida_dbg/sharing/"):
        sys("mkdir /var/tmp/ida_dbg/sharing/")

    sys("mkdir " + dir)
    sys("echo '# pdp connections pep -e' > " + dir + "ida_sharing.txt")
    sys("pdp connections pep -e >> " + dir + "ida_sharing.txt")
    sys("echo '# pdp network info' >> " + dir + "ida_sharing.txt")
    sys("pdp network info >> " + dir + "ida_sharing.txt")
    sys("echo '# pdp network registered' >> " + dir + "ida_sharing.txt")
    sys("pdp network registered >> " + dir + "ida_sharing.txt")
    sys("echo '# pep show pdp all -e' >> " + dir + "ida_sharing.txt")
    sys("pep show pdp all -e >> " + dir + "ida_sharing.txt")
    sys("echo '# pep show network pdp -e' >> " + dir + "ida_sharing.txt")
    sys("pep show network pdp -e >> " + dir + "ida_sharing.txt")
    sys("echo '# pep show network registration -e' >> " + dir + "ida_sharing.txt")
    sys("pep show network registration -e >> " + dir + "ida_sharing.txt")

    print("\n----All identity sharing information was saved to " + dir + "ida_sharing.txt")
    in_option = input("Would you like to review it now? (Yes=1 No=0) : ")
    try:
        if int(in_option) == 1:
            sys("cat " + dir + "ida_sharing.txt")
        if int(in_option) > 1:
            print("\n----Invalid input")
    except:
        print("\n----Invalid input")

    return 0


def ida_tables():
    date = datetime.now()
    dir = "/var/tmp/ida_dbg/tables/" + date.strftime("%d-%m-%y_%H-%M") + "/"
    if not path.isdir("/var/tmp/ida_dbg/tables/"):
        sys("mkdir /var/tmp/ida_dbg/tables/")

    in_option = input("\nFor capturing kernel tables press 1. For clearing kernel tables press 0: ")

    try:
        if int(in_option) == 1:
            sys("mkdir " + dir)
            print("\n----Saving kernel tables")
            sys("ida_tables_util -a > /dev/null")
            sys("mv ida_tab* " + dir)
            print("\n----The kernel tables were saved to: " + dir)
        elif int(in_option) == 0:
            sys("ida_tables_util -c")
        else:
            print("\n----Invalid input")
    except:
        print("\n----Invalid input")

    return 0


def ldap():
    print("")
    sys("pdp nested_groups status")
    sys("pdp nested_groups show")
    print("\nChange LDAP query method to (or type 0 to exit): "
          "\n\t1 - Recursive query until all nesting levels found " \
          "\n\t2 - Per user - with 1 LDAP search queries all the user groups (require Global Catalog DC) " \
          "\n\t3 - Per group - 1 query for each group in access roles, to check if the user is in it" \
          "\n\t4 - Per user - with with 1 LDAP search queries all the user groups (same as mode 2, but no GC)"
    option_in = input("Choice: ")
    try:
        if int(option_in) == 1:
            sys("pdp nested_groups __set_state 1")
        if int(option_in) == 2:
            sys("pdp nested_groups __set_state 2")
        if int(option_in) == 3:
            sys("pdp nested_groups __set_state 3")
        if int(option_in) == 4:
            sys("pdp nested_groups __set_state 4")
        else:
            print("\n----Invalid input")
    except:
        print("\n----Invalid input")

    return 0


def adConnectivity():
    date = datetime.now()
    dir = "/var/tmp/ida_dbg/adconnectivity/" + date.strftime("%d-%m-%y_%H-%M") + "/"
    if not path.isdir("/var/tmp/ida_dbg/adconnectivity/"):
        sys("mkdir /var/tmp/ida_dbg/adconnectivity/")

    domainName = input("\nEnter the domain name (ex. domain.com) : ")
    dcIP = input("\nEnter the IP of one of the domain controllers : ")
    userName = input("\nEnter the name of the user from the AU : ")
    userPassword = getpass()

    sys("test_ad_connectivity -v -o tested_ad.txt -d " + domainName + " -i " + dcIP + " -u " + userName + " -c '" + userPassword + "' &")
    # sys("cp $FWDIR/tmp/tested_ad.txt " + dir)
    # print "The file saved at " + dir + "tested_ad.txt"


def ida_debugging():
    date = datetime.now()
    dir = "/var/tmp/ida_dbg/debug/" + date.strftime("%d-%m-%y_%H-%M") + "/"
    if not path.isdir("/var/tmp/ida_dbg/debug/"):
        sys("mkdir /var/tmp/ida_dbg/debug/")

    while 1:
        isVPN = input("\nAre you debugging Remote Access VPN identity source? y/n ")
        if isVPN == "y" or isVPN == "Y":
            isVPN = 1
            break
        elif isVPN == "n" or isVPN == "N":
            isVPN = 0
            break
        else:
            continue

    print("\n----Initializing debug - please wait")
    sys("mkdir " + dir)
    sys("fw debug fwd on PDP_LOG_SIZE=50000000")
    sys("fw debug fwd on PDP_NUM_LOGS=100")
    sys("fw debug fwd on PEP_LOG_SIZE=50000000")
    sys("fw debug fwd on PEP_NUM_LOGS=100")
    sys("fw kill pdpd ; fw kill pepd ; sleep 10")
    sys("pdp debug on > /dev/null")
    sys("pdp debug rotate > /dev/null")
    sys("pep debug on > /dev/null")
    sys("pep debug rotate > /dev/null")
    sys("rm $FWDIR/log/p?pd.elg.*")
    sys("pdp debug set all all > /dev/null")
    sys("pep debug set all all > /dev/null")
    if isVPN:
        sys("vpn debug trunc ALL=5 > /dev/null")
        sys("ike debug trunc ALL=5 > /dev/null")
        sys("vpn debug on > /dev/null")
        sys("ike debug on > /dev/null")
        sys("vpn debug on TDERROR_ALL_ALL=5 > /dev/null")
        sys("tail -f $FWDIR/log/vpnd.elg > " + dir + " &")

    input("\n----Debug started - replicate the issue - to stop debugging press Enter")

    sys("pdp debug unset all all > /dev/null")
    sys("pep debug unset all all > /dev/null")
    sys("cp $FWDIR/log/pdpd* " + dir)
    sys("cp $FWDIR/log/pepd* " + dir)
    if isVPN:
        sys("vpn debug off")
        sys("ike debug off")
        sys("cp $FWDIR/log/ike* " + dir)
        sys("cp $FWDIR/log/vpn* " + dir)
    sys("fw debug fwd on PDP_LOG_SIZE=10000000")
    sys("fw debug fwd on PDP_NUM_LOGS=10")
    sys("fw debug fwd on PEP_LOG_SIZE=10000000")
    sys("fw debug fwd on PEP_NUM_LOGS=10")
    print("\n----Stopping debug - please wait")
    sys("fw kill pdpd ; fw kill pepd ; sleep 10")
    print("\n----Debug done - outputs saved to " + dir)

    return 0


def main_loop():
    if not path.isdir("/var/tmp/ida_dbg/"):
        sys("mkdir /var/tmp/ida_dbg/")

    print("\n------------------IDA Multi-Tool--------------------")
    looping = 1
    while int(looping):
        print("\nPlease choose option:"
              "\n\t0 - Exit."
              "\n\t1 - Identity Sharing."
              "\n\t2 - IDA tables."
              "\n\t3 - LDAP"
              "\n\t4 - Test AD connectivity"
              "\n\t5 - IDA debugging")
        option = int(0)
        option = input("Your choice: ")

        try:
            if int(option) == 0:
                looping = 0
            elif int(option) == 1:
                identity_sharing()
            elif int(option) == 2:
                ida_tables()
            elif int(option) == 3:
                ldap()
            elif int(option) == 4:
                adConnectivity()
            elif int(option) == 5:
                ida_debugging()
            else:
                print("\n----Invalid input")
        except:
            print("\n----Invalid input")


if __name__ == "__main__":
    main_loop()
else:
    print("This is standalone script")
