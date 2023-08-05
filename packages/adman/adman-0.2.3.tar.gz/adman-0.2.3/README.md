adman
=====
A tool for performing some automated Active Directory management.

This tool performs various maintenance tasks against an Active Directory:
- Assignment of `uidNumber`/`gidNumber` attributes for users and groups
- *Future:* Home directory creation / management
- *Future:* UPN suffix consistency


Adman can run on any Linux system; the host system does not even need to be
joined to the domain. Adman typically runs with a dedicated user (e.g.
`domain-janitor`) and uses a Kerberos keytab, rather than password-based authentication.

Adman assigns UID/GID numbers sequentially from a user-defined range, and stores
the next-highest value in the `msSFU30MaxUidNumber`/`msSFU30MaxGidNumber`
attributes in LDAP. This ensures that even if users/groups are removed, UID/GID
values will not be re-used.


# Getting Started

## Installation
Where possible, it is preferable to install Python packages using your Linux
distribution's package manager, rather than from PyPI (using pip). This helps
avoid package conflicts.

The following Python packages are required:
- `setuptools` -- For installation
- [`python-ldap`](https://www.python-ldap.org)
- [`dnspython`](http://www.dnspython.org)
- [`PyYAML`](https://pyyaml.org)

Also, your system must have the GSSAPI module for SASL authentication.

Debian:
```
apt install python3-setuptools python3-ldap python3-dnspython python3-yaml libsasl2-modules-gssapi-mit
```
*Note: `python3-ldap` is only available in Debian Buster.*

Fedora:
```
dnf install python3-setuptools python3-ldap python3-dns python3-pyyaml cyrus-sasl-gssapi
```

Then install adman:
```
tar xf adman-*.tar.gz
cd adman-*
python3 setup.py install
```


## Domain Janitor setup

### Samba

Create the domain-janitor user and set its password to not expire:
```
samba-tool user create domain-janitor --random-password
samba-tool user setexpiry --noexpiry domain-janitor
```

Add the user to `Domain Admins`:
```
samba-tool group addmembers 'Domain Admins' domain-janitor
```

Export the user's Kerberos keytab:
```
samba-tool domain exportkeytab --principal='domain-janitor' domain-janitor.keytab
```

### Windows
TODO



## Configuration
By default, Adman looks for its config file at:
- `/etc/adman/config.yml` when run as `root`
- `~/.config/adman/config.yml` when run as a normal user

To configure:
- Copy `example_config.yml` to the appropriate path.
- Edit the configuration options as necessary.
  - At a minimum, the `domain` field needs to be updated.
- Copy the expored keytab to the path specified in `config.yml`
  (this defaults to `domain-janitor.keytab` in the same directory).
  - **Ensure that `domain-janitor.keytab` is carefully protected!**


## First run

First the state fields need initialized:
```
adman -c adman_config.yml state init
```

Now user / group IDs can be assigned:
```
# adman -c adman_config.yml assign
```


## Run automatically
Note that `adman` will likely be installed in a path not normally searched by `cron`,
so we use the full path (`which adman`).

To assign IDs every minute, run `crontab -e` and add this line:
```
*/1 * * * * 	/usr/local/bin/adman -c /etc/adman_config.yml --changelog /var/log/adman_changes.log assign
```



# Troubleshooting

### No worthy mechs found
```
ldap.AUTH_UNKNOWN: {'desc': 'Unknown authentication method', 'errno': 22, 'info': 'SASL(-4): no mechanism available: No worthy mechs found'}
```

You need to install the GSSAPI SASL modules. On Debian:
```
apt install libsasl2-modules-gssapi-mit
```


### Insufficient access
```
ldap.INSUFFICIENT_ACCESS: {'desc': 'Insufficient access', 'info': '00002098: Object CN=adtest,CN=ypservers,CN=ypServ30,CN=RpcServices,CN=System,DC=ad-test,DC=vx has no write property access\n'}
```

The user needs to be a member of `Domain Admins`.

Once this change has been made, you must remove the stale credential cache. E.g.:
```
rm /tmp/domain-janitor.cc
```

### Server not found in Kerberos database
```
SASL: GSSAPI Error: Unspecified GSS failure. Minor code may provide more information (Server not found in Kerberos database).
```

Various problems can lead to this error. One common case I've encountered is
that a reverse DNS (PTR) record does not exist for the DC(s).
