<!--
SPDX-FileCopyrightText: 2024 ThysTips <contact@thystips.net>
SPDX-FileCopyrightText: 2024 Weytop
SPDX-FileContributor: ThysTips <contact@thystips.net>

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Tempo

Role to install and configure Tempo, a high-performance, easy-to-operate, and cost-effective distributed tracing system.

_Based on [Mimir role](https://github.com/grafana/grafana-ansible-collection/tree/main/roles/mimir) from [Grafana Ansible Collection](https://github.com/grafana/grafana-ansible-collection/tree/main) on MIT license._

## Requirements

No specific requirements.

## Role Variables

The role uses the following variables:

- `tempo_version`: Version of Tempo to install. Default: `latest`
- `tempo_download_url_rpm`: URL to download the Tempo RPM package. Default to Github release corresponding to `tempo_version`.
- `tempo_download_url_deb`: URL to download the Tempo DEB package. Default to Github release corresponding to `tempo_version`.

- `__tempo_arch`: Architecture to use for the download URL. Default to `amd64`.
- `tempo_arch_mapping`: Mapping between Ansible architecture and Tempo architecture (`vars/main.yml`).

Some variables permit overriding common configuration options for Tempo:

- `tempo_working_path`: Path where Tempo will store its data. Default: `/var/tempo`
- `tempo_http_listen_port`: Port on which Tempo will listen for HTTP requests. Default: `3200`
- `tempo_http_listen_address`: Address on which Tempo will listen for HTTP requests. Default: `0.0.0.0` (All interfaces)
- `tempo_log_level`: Log level for Tempo. Default: `warn`

- `tempo_stream_over_http_enabled`: Streaming service over HTTP instead of GRPC. Default: `false` (see [Tempo documentation](https://grafana.com/docs/tempo/latest/api_docs/#tempo-grpc-api)).

Other parameters are from [Tempo documentation](https://grafana.com/docs/tempo/latest/configuration/) with `tempo_` prefix.
Example: `tempo_metrics_generator` section is `metrics_generator` section in Tempo configuration file.

## Dependencies

No dependencies.

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
- name: Install and configure Tempo
  hosts: monitoring
  roles:
    - role: weytop.infrastructure.tempo
      tempo_server.grpc_listen_port: 9097
      tempo_memberlist.bind_port: 7947
```

## License

GPL 3.0 or later

## Author Information

Written by ThysTips <contact@thystips.net> for Weytop <https://weytop.com>.
