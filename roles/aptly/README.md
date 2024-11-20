<!--
SPDX-FileCopyrightText: 2024 Weytop

SPDX-License-Identifier: GPL-3.0-or-later
-->

Aptly
=========

Role to install [aptly](https://www.aptly.info).

Requirements
------------

This role install Aptly's and Ansible's dependencies.
Feel free to override `aptly_install_packages` variable which contains :

- aptly
- gnupg2
- inoticoming
- curl
- acl

Role Variables
--------------

See [defaults/main.yml](defaults/main.yml) for the list of variables and their default values.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
- hosts: repo
  roles:
    - role: weytop.infrastructure.aptly
      vars:
        aptly_repositories:
          - name: stable
            comment: APP stable repository
            distribution: noble
```

License
-------

GPL-3.0-or-later

Author Information
------------------

This role was created in 2024 by [Weytop](https://github.com/weytop).
