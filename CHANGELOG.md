# 2.1.0 - 2025-04-02

## New Features
- Add roles for DNS architecture

## Chores
- update CHANGELOG.md for 2.0.0 [skip ci]

# 2.0.0 - 2025-01-27

## New Features
- Add role aptly
- Add module for gpg keys adding
- **aptly:** Add requests for repository creation
- **aptly:** Add mirrors

## Build System
- Lint only on default branch

## Build System
- Replace pipenv by poetry

## Chores
- update CHANGELOG.md for 1.2.1 [skip ci]
- **deps:** bump cryptography in the pip group across 1 directory
- fix some licenses
- **deps:** bump the pip group across 1 directory with 2 updates
- Add missing dependencies for CI
- Update python dependencies
- dump version 2.0.0

## Refacto
- fix hosts file
- Update reuse GA
- Fix some lint issues and disable sanity check
- **aptly:** Remove old repo creation code
- **aptly:** Aptly role

## Security
- Update pipenv dependencies for security fixes

## BREAKING CHANGES
- due to [c78fea](https://github.com/weytop/ansible-infrastructure-collection/commit/c78fea4679fcb5aff02ba2b4831820e68388e3a3): Replace pipenv by poetry

Replace pipenv by poetry

# 1.2.1 - 2024-08-28

## New Features
- add role hosts_file

## Bugfixes
- release ref naming

## Chores
- update CHANGELOG.md for 1.2.0 [skip ci]

# 1.2.0 - 2024-06-18

## New Features
- **role:** Add role oncall_docker

## Bugfixes
- Remove handlers from ca_certificates role
- sanity tests on licence
- github ci
- release and workflow order and exec

## Chores
- Update CHANGELOG.md
- fix license
- changelog regression

# 1.0.0 - 2024-04-22

### New Features

- Initial release
- Migrate existing Ansible roles to collections