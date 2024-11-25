#!/usr/bin/python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Antoine Thys - Weytop <athys@weytop.com>
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.aptly import (
    AptlyClient, AptlyMirror
)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: aptly_mirror
short_description: Manage Aptly mirrors
description:
    - Create, delete, and manage Aptly mirrors using the Aptly API
    - Requires aptly_api Python package (not yet released with mirror support)
requirements:
    - aptly_api (with mirror support)
version_added: "1.3.0"
options:
    name:
        description:
            - Name of the mirror
        type: str
        required: true
    state:
        description:
            - Desired state of the mirror
        type: str
        choices: [ 'present', 'absent' ]
        default: present
    endpoint:
        description:
            - URL of the Aptly API endpoint
        type: str
        required: true
    archive_url:
        description:
            - URL of the repository to mirror
        type: str
    distribution:
        description:
            - Distribution to mirror (e.g., 'stable', 'jammy')
        type: str
    components:
        description:
            - List of components to mirror (e.g., ['main', 'contrib'])
        type: list
        elements: str
    architectures:
        description:
            - List of architectures to mirror (e.g., ['amd64', 'arm64'])
        type: list
        elements: str
    filter:
        description:
            - Package filter expression
        type: str
    download_sources:
        description:
            - Whether to download source packages
        type: bool
        default: false
    download_udebs:
        description:
            - Whether to download .udeb packages
        type: bool
        default: false
    download_installer:
        description:
            - Whether to download additional not packaged installer files
            - Can't be changed after creation
        type: bool
        default: false
    sync:
        description:
            - Whether to sync the mirror after creation/update
            - CAUTION: database stay locked until end of sync
            - WARNING: buggy option, launch sync but ansible timeout, fix or remove required
        type: bool
        default: false
    force:
        description:
            - Force update of existing mirror configuration
            - WARNING: buggy option, remove mirror, fix required
        type: bool
        default: false
    ignore_signatures:
        description:
            - Whether to ignore GPG signature verification
        type: bool
        default: false
author:
    - Antoine Thys - Weytop (@thystips)
"""

EXAMPLES = r"""
- name: Create Debian mirror
  aptly_mirror:
    name: debian-stable
    endpoint: http://localhost:8000
    archive_url: http://deb.debian.org/debian
    distribution: stable
    components: ['main', 'contrib']
    architectures: ['amd64']
    state: present
    sync: true

- name: Remove mirror
  aptly_mirror:
    name: debian-stable
    endpoint: http://localhost:8000
    state: absent
"""

RETURN = r"""
mirror:
    description: Final state of the mirror
    type: dict
    returned: always
    sample: {
        "name": "debian-stable",
        "archive_url": "http://deb.debian.org/debian",
        "distribution": "stable",
        "components": ["main", "contrib"],
        "architectures": ["amd64"],
        "download_sources": false,
        "download_udebs": false,
        "last_download_date": "2024-03-25 10:30:45",
        "status": 0
    }
"""


def ensure_present(module: AnsibleModule, aptly: AptlyMirror) -> dict:
    """Ensure that the mirror exists with the correct configuration"""
    result = {
        'changed': False,
        'mirror': {},
        'needs_update': False
    }

    name = module.params['name']

    try:
        # Check if mirror exists
        existing_mirror = aptly.get_mirror(name)

        if existing_mirror:
            result['mirror'] = aptly.format_mirror_info(existing_mirror)

            if aptly.mirror_needs_update(existing_mirror, module.params):
                if not module.params.get('force', False):
                    module.warn(
                        f"Mirror '{name}' exists but its configuration differs. "
                        "Use force: true to update the configuration."
                    )
                    result['needs_update'] = True
                    return result

                if not module.check_mode:
                    aptly.delete_mirror(name)
                    result['changed'] = True

        if not existing_mirror and not module.check_mode:
            new_mirror = aptly.create_mirror(module.params)
            result['changed'] = True
            result['mirror'] = aptly.format_mirror_info(new_mirror)

            # Sync if asked
            if module.params.get('sync', False):
                aptly.sync_mirror(name, module.params.get('ignore_signatures', False))

    except Exception as e:
        module.fail_json(msg=str(e))

    return result


def ensure_absent(module: AnsibleModule, aptly: AptlyMirror) -> dict:
    """Ensure that the mirror does not exist"""
    result = {'changed': False}

    if not module.check_mode:
        existing_mirror = aptly.get_mirror(module.params['name'])
        if existing_mirror:
            aptly.delete_mirror(module.params['name'])
            result['changed'] = True

    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent']),
            endpoint=dict(type='str', required=True),
            archive_url=dict(type='str'),
            distribution=dict(type='str'),
            components=dict(type='list', elements='str'),
            architectures=dict(type='list', elements='str'),
            filter=dict(type='str'),
            download_sources=dict(type='bool', default=False),
            download_udebs=dict(type='bool', default=False),
            download_installer=dict(type='bool', default=False),
            sync=dict(type='bool', default=False),
            force=dict(type='bool', default=False),
            ignore_signatures=dict(type='bool', default=False)
        ),
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ['archive_url'])
        ]
    )

    try:
        client = AptlyClient(module)
        aptly = AptlyMirror(client)

        if module.params['state'] == 'present':
            result = ensure_present(module, aptly)
        else:
            result = ensure_absent(module, aptly)

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=f"Unexpected error: {str(e)}")


if __name__ == '__main__':
    main()
