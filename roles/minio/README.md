<!--
SPDX-FileCopyrightText: 2024 ThysTips <contact@thystips.net>
SPDX-FileCopyrightText: 2024 Weytop
SPDX-FileContributor: ThysTips <contact@thystips.net>

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Ansible Role: Minio

Install and configure the [Minio](https://minio.io/) S3 compatible object storage server Debian/Ubuntu.

Copy of repository [atosatto/ansible-minio](https://github.com/atosatto/ansible-minio) with some modifications.

## Requirements

None.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yaml
minio_server_bin: /usr/local/bin/minio
minio_client_bin: /usr/local/bin/mc
```

Installation path of the Minio server and client binaries.

```yaml
minio_server_release: ""
minio_client_release: ""
```

Release to install for both server and client; lastest if the default.
Can be 'RELEASE.2019-06-27T21-13-50Z' for instance.

```yaml
minio_user: minio
minio_group: minio
minio_usergroup_manage: true
```

Name and group of the user running the minio server. Without explicitly
disabling `minio_usergroup_manage: false` this role will create/update this
user and group. The created/updated user will be installed/updated as a system
user.

```yaml
minio_server_envfile: /etc/default/minio
```

Path to the file containing the minio server configuration ENV variables.

```yaml
minio_server_ip: ""
```

The Minio server listen address.

```yaml
minio_server_port: "9000"
```

The Minio server listen port.

```yaml
minio_server_addr: "{{ minio_server_ip }}:{{ minio_server_port }}"
```

The Minio server listen address and port construct with `minio_server_ip` and `minio_server_port`.

```yaml
minio_console_ip: ""
minio_console_port: "9001"
minio_console_addr: "{{ minio_console_ip }}:{{ minio_console_port }}"
```

Same as above but for the Minio web console.

```yaml
minio_server_url: ""
```

The Minio server URL used by Minio console to communicate with the server.

```yaml
minio_browser_redirect_url: ""
```

The Minio server URL for browser console access.

```yaml
minio_server_datadirs:
  - /var/lib/minio
```

Directories of the folder containing the minio server data

```yaml
minio_server_make_datadirs: true
```

Create directories from `minio_server_datadirs`

```yaml
minio_server_cluster_nodes: [ ]
```

Set a list of nodes to create a [distributed cluster](https://docs.minio.io/docs/distributed-minio-quickstart-guide).

In this mode, ansible will create your server datadirs, but use this list for the server startup. Note you will need a number of disks to satisfy Minio's distributed storage requirements.

Example:

```yaml
minio_server_datadirs:
  - '/minio-data'
  - ...
minio_server_cluster_nodes:
  - 'https://server1/minio-data'
  - 'https://server2/minio-data'
  - 'https://server3/minio-data'
  - ...
```

```yaml
minio_server_env_extra: ""
```

Additional environment variables to be set in Minio server environment

```yaml
minio_server_opts: ""
```

Additional CLI options that must be appended to the minio server start command.

```yaml
minio_root_user: ""
minio_root_password: ""
```

Minio root user and password (replace access and secret keys).
Username must be at least 3 characters long and password must be at least 8 characters long.

```yaml
minio_install_server: true
minio_configure_server: true
minio_install_client: true
```

Switches to disable minio server and/or minio client installation or configuration.

```yaml
minio_install_source: download
```

Installation source for Minio server and client. Can be `download` (Github release) or `repo` (distribution repository).
WARNING: Switching between `download` and `repo` will not uninstall the previous installation and may cause conflicts.

```yaml
minio_upgrade: true
```

Upgrade Minio server and client if already installed from repository.

```yaml
minio_region: us-east-1
```

Region used by Minio server.

## Dependencies

None.

## Example Playbook

```yaml
- name: "Install Minio"
  hosts: all
  become: yes
  roles:
    - { role: weytop.infrastructure.minio, tags: minio }
  vars:
    minio_server_datadirs: [ "/minio-test" ]
    minio_root_user: "minio"
    minio_root_password: "minio"
```

## License

MIT for original code from atosatto/ansible-minio, GPL-3.0 for the modifications.
