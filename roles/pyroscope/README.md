<!--
SPDX-FileCopyrightText: 2024 ThysTips <contact@thystips.net>
SPDX-FileCopyrightText: 2024 Weytop
SPDX-FileContributor: ThysTips <contact@thystips.net>

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Pyroscope

Role to install and configure Pyroscope for profiling.

_Based on [Mimir role](https://github.com/grafana/grafana-ansible-collection/tree/main/roles/mimir) from [Grafana Ansible Collection](https://github.com/grafana/grafana-ansible-collection/tree/main) on MIT license._

## Requirements

No specific requirements.

## Role Variables

The role uses the following variables:

- `pyroscope_version`: Version of Pyroscope to install. Default: `latest`
- `pyroscope_download_url_rpm`: URL to download the Pyroscope RPM package. Default to Github release corresponding to `pyroscope_version`.
- `pyroscope_download_url_deb`: URL to download the Pyroscope DEB package. Default to Github release corresponding to `pyroscope_version`.

- `__pyroscope_arch`: Architecture to use for the download URL. Default to `amd64`.
- `pyroscope_arch_mapping`: Mapping between Ansible architecture and Pyroscope architecture (`vars/main.yml`).

Some variables permit overriding common configuration options for Pyroscope:

- `pyroscope_working_path`: Path where Pyroscope will store its data. Default: `/var/pyroscope`
- `pyroscope_http_listen_port`: Port on which Pyroscope will listen for HTTP requests. Default: `3200`
- `pyroscope_http_listen_address`: Address on which Pyroscope will listen for HTTP requests. Default: `0.0.0.0` (All interfaces)
- `pyroscope_log_level`: Log level for Pyroscope. Default: `warn`
- `pyroscope_analytics_reporting`: Enable or disable analytics reporting. Default: `true`

Other parameters are from [Pyroscope documentation](https://grafana.com/docs/pyroscope/latest/configuration/) with `pyroscope_` prefix.
Example: `pyroscope_distributor` section is `distributor` section in Pyroscope configuration file.

## Dependencies

No dependencies.

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
- name: Install and configure Pyroscope
  hosts: monitoring
  roles:
    - role: weytop.infrastructure.pyroscope
      pyroscope_server.grpc_listen_port: 9098
      pyroscope_memberlist.bind_port: 7948
```

## License

GPL 3.0 or later

## Author Information

Written by ThysTips <contact@thystips.net> for Weytop <https://weytop.com>.
