#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

# SPDX-FileCopyrightText: 2024 Antoine Thys - Weytop <athys@weytop.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright: 2024 Antoine Thys - Weytop <athys@weytop.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

__metaclass__ = type

DOCUMENTATION = r"""
---
module: aptly_repository
short_description: Manage Aptly repositories
description:
    - Create, delete, and manage Aptly repositories using the Aptly API
    - Note that Aptly does not support modifying existing repositories.
      If you need to change repository settings, you must delete and recreate it.
    - Setting force=yes will automatically delete and recreate the repository if
      its configuration differs from the desired state.
    - BE CAREFUL - Using force=yes will the repository and its contents will be deleted!
requirements:
    - aptly_api
version_added: "1.3.0"
options:
    name:
        description:
            - Name of the repository
        type: str
        required: true
    state:
        description:
            - Desired state of the repository
        type: str
        choices: [ 'present', 'absent' ]
        default: present
    endpoint:
        description:
            - URL of the Aptly API endpoint
        type: str
        required: true
    distribution:
        description:
            - Default distribution for the repository
        type: str
    component:
        description:
            - Default component for the repository
        type: str
        default: main
    comment:
        description:
            - Comment for the repository
        type: str
    force:
        description:
            - If true, will delete and recreate the repository if its configuration
              differs from the desired state
            - WARNING - This will delete all packages in the repository!
        type: bool
        default: false
author:
    - Antoine Thys - Weytop (@thystips)
"""

EXAMPLES = r"""
# Create a new repository
- name: Create repository
  aptly_repository:
    name: myrepo
    endpoint: http://localhost:8000
    distribution: noble
    component: main
    comment: "My test repository"
    state: present

# Update repository configuration (will fail without force)
- name: Update repository
  aptly_repository:
    name: myrepo
    endpoint: http://localhost:8000
    distribution: jammy
    component: main
    comment: "Updated repository"
    state: present
    force: yes

# Remove a repository
- name: Remove repository
  aptly_repository:
    name: myrepo
    endpoint: http://localhost:8000
    state: absent
"""

RETURN = r"""
repository:
    description: Final state of the repository
    type: dict
    returned: always
    sample: {
        "name": "myrepo",
        "comment": "My test repository",
        "default_distribution": "noble",
        "default_component": "main",
        "needs_update": false
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ..module_utils.aptly import (
    AptlyClient,
    AptlyRepo,
)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            state=dict(type="str", default="present", choices=["present", "absent"]),
            endpoint=dict(type="str", required=True),
            distribution=dict(type="str"),
            component=dict(type="str", default="main"),
            comment=dict(type="str"),
            force=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )

    result = dict(changed=False, repository={}, needs_update=False)

    try:
        client = AptlyClient(module)
        repo_helper = AptlyRepo(client)

        if module.params["state"] == "present":
            # Vérifier si le repo existe
            existing_repo = repo_helper.get_repo(module.params["name"])

            if existing_repo:
                result["repository"] = repo_helper.format_repo_info(existing_repo)

                if repo_helper.repo_needs_update(existing_repo, module.params):
                    result["needs_update"] = True
                    if not module.params["force"]:
                        module.warn(
                            f"Repository '{module.params['name']}' exists but its configuration differs. "
                            "Use force: yes to delete and recreate it (WARNING: this will delete all packages!)"
                        )
                        module.exit_json(**result)

                    if not module.check_mode:
                        repo_helper.delete_repo(module.params["name"])
                        new_repo = repo_helper.create_repo(module.params)
                        result["repository"] = repo_helper.format_repo_info(new_repo)
                        result["changed"] = True
            else:
                if not module.check_mode:
                    try:
                        new_repo = repo_helper.create_repo(module.params)
                        result["repository"] = repo_helper.format_repo_info(new_repo)
                        result["changed"] = True
                    except Exception as e:
                        if "already exists" in str(e).lower():
                            existing_repo = repo_helper.get_repo(
                                module.params["name"], use_cache=False
                            )
                            if existing_repo:
                                result["repository"] = repo_helper.format_repo_info(
                                    existing_repo
                                )
                        else:
                            raise
                else:
                    result["changed"] = True
        else:  # state == 'absent'
            existing_repo = repo_helper.get_repo(module.params["name"])
            if existing_repo and not module.check_mode:
                repo_helper.delete_repo(module.params["name"])
                result["changed"] = True

    except Exception as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
