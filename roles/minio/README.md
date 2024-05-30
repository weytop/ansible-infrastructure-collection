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
minio_server_addr: ":9091"
```

The Minio server listen address.

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
minio_access_key: ""
minio_secret_key: ""
```

Minio access and secret keys.

```yaml
minio_install_server: true
minio_install_client: true
```

Switches to disable minio server and/or minio client installation.

## Dependencies

None.

## Example Playbook

```yaml
- name: "Install Minio"
  hosts: all
  become: yes
  roles:
    - { role: atosatto.minio }
  vars:
    minio_server_datadirs: [ "/minio-test" ]
```

## License

MIT for original code from atosatto/ansible-minio, GPL-3.0 for the modifications.
