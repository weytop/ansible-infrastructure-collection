# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Antoine Thys - Weytop <athys@weytop.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright: 2024 Antoine Thys - Weytop <athys@weytop.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Shared utilities for Aptly modules
"""

from __future__ import absolute_import, division, print_function

import traceback
from typing import Optional, Dict, Any, List, Sequence

from ansible.module_utils.basic import missing_required_lib
from aptly_api.parts.repos import Repo
from aptly_api.parts.mirrors import Mirror

APTLY_API_IMP_ERR = None
try:
    from aptly_api import Client

    HAS_APTLY_API = True
except ImportError:
    Client = None
    APTLY_API_IMP_ERR = traceback.format_exc()
    HAS_APTLY_API = False


class AptlyError(Exception):
    """Base exception for Aptly-related errors"""

    pass


class AptlyClient:
    """Wrapper for Aptly API client with common functionality"""

    def __init__(self, module):
        self.module = module
        if not HAS_APTLY_API:
            module.fail_json(
                msg=missing_required_lib("aptly_api"), exception=APTLY_API_IMP_ERR
            )

        try:
            self.client = Client(module.params["endpoint"])
        except Exception as e:
            module.fail_json(msg=f"Failed to initialize Aptly client: {str(e)}")

    def handle_error(self, error: Exception, ignore_404: bool = False) -> str:
        """Common error handling for Aptly operations"""
        error_msg = str(error)
        if ignore_404 and "not found" in error_msg.lower():
            return error_msg
        self.module.fail_json(msg=f"Aptly API error: {error_msg}")

    def log_debug(self, message: str) -> None:
        """Log debug message if verbosity is high enough"""
        self.module.warn(f"DEBUG: {message}")


class AptlyRepo:
    """Helper class for repository operations"""

    def __init__(self, client: AptlyClient):
        self.client = client
        self._cache = {}

    @staticmethod
    def format_repo_info(repo: Repo) -> Dict[str, str]:
        """Format repository information into a consistent structure"""
        if not repo:
            return {}

        return {
            "name": repo.name,
            "comment": repo.comment or "",
            "default_distribution": repo.default_distribution or "",
            "default_component": repo.default_component or "main",
        }

    def get_repo(self, name: str, use_cache: bool = True) -> Optional[Repo]:
        """Get repository by name with optional caching"""
        if use_cache and name in self._cache:
            return self._cache[name]

        try:
            repos = self.client.client.repos.list()
            repo = next((r for r in repos if r.name == name), None)
            if use_cache and repo:
                self._cache[name] = repo
            return repo
        except Exception as e:
            self.client.handle_error(e)

    def create_repo(self, params: Dict[str, Any]) -> Repo:
        """Create a new repository"""
        try:
            return self.client.client.repos.create(
                params["name"],
                comment=params.get("comment"),
                default_distribution=params.get("distribution"),
                default_component=params.get("component", "main"),
            )
        except Exception as e:
            self.client.handle_error(e)

    def delete_repo(self, name: str) -> None:
        """Delete a repository"""
        try:
            self.client.client.repos.delete(name)
            self._cache.pop(name, None)
        except Exception as e:
            self.client.handle_error(e, ignore_404=True)

    @staticmethod
    def repo_needs_update(existing_repo: Repo, params: Dict[str, Any]) -> bool:
        """Check if repository needs to be updated"""
        return any(
            [
                existing_repo.comment != params.get("comment"),
                existing_repo.default_distribution != params.get("distribution"),
                existing_repo.default_component != (params.get("component") or "main"),
            ]
        )


class AptlyPublication:
    """Helper class for publication operations"""

    def __init__(self, client: AptlyClient):
        self.client = client

    # TODO: Implement this
    pass


class AptlySnapshot:
    """Helper class for snapshot operations"""

    def __init__(self, client: AptlyClient):
        self.client = client

    # TODO: Implement this
    pass


class AptlyPackage:
    """Helper class for package operations"""

    def __init__(self, client: AptlyClient):
        self.client = client

    # TODO: Implement this
    pass

class AptlyMirror:
    """Helper class for mirror operations"""

    def __init__(self, client: AptlyClient):
        self.client = client
        self._cache = {}

    @staticmethod
    def format_mirror_info(mirror: Mirror) -> Dict[str, Any]:
        """Format mirror information into a consistent structure"""
        if not mirror:
            return {}

        return {
            'name': mirror.name,
            'archive_url': mirror.archiveurl,
            'distribution': mirror.distribution or '',
            'components': mirror.components or [],
            'architectures': mirror.architectures or [],
            'download_sources': mirror.download_sources,
            'download_udebs': mirror.download_udebs,
            'download_installer': mirror.download_installer,
            'filter': mirror.filter or '',
            'filter_with_deps': mirror.filter_with_deps,
            'skip_component_check': mirror.skip_component_check,
            'skip_architecture_check': mirror.skip_architecture_check,
            'last_download_date': mirror.downloaddate or '',
            'status': mirror.status,
            'worker_pid': mirror.worker_pid
        }

    def get_mirror(self, name: str, use_cache: bool = True) -> Optional[Mirror]:
        """Get mirror by name with optional caching"""
        if use_cache and name in self._cache:
            return self._cache[name]

        try:
            mirror = self.client.client.mirrors.show(name)
            if use_cache:
                self._cache[name] = mirror
            return mirror
        except Exception as e:
            if "not found" not in str(e).lower():
                self.client.handle_error(e)
            return None

    def create_mirror(self, params: Dict[str, Any]) -> Mirror:
        """Create a new mirror"""
        try:
            mirror = self.client.client.mirrors.create(
                name=params['name'],
                archiveurl=params['archive_url'],
                distribution=params.get('distribution'),
                components=params.get('components'),
                architectures=params.get('architectures'),
                filter=params.get('filter'),
                download_sources=params.get('download_sources', False),
                download_udebs=params.get('download_udebs', False),
                download_installer=params.get('download_installer', False),
                filter_with_deps=params.get('filter_with_deps', False),
                skip_component_check=params.get('skip_component_check', False),
                skip_architecture_check=params.get('skip_architecture_check', False),
                ignore_signatures=params.get('ignore_signatures', False)
            )
            return mirror
        except Exception as e:
            self.client.handle_error(e)

    def update_mirror(self, name: str, params: Dict[str, Any]) -> None:
        """Update mirror configuration"""
        try:
            self.client.client.mirrors.edit(
                name=name,
                archiveurl=params.get('archive_url'),
                filter=params.get('filter'),
                architectures=params.get('architectures'),
                components=params.get('components'),
                filter_with_deps=params.get('filter_with_deps', False),
                download_sources=params.get('download_sources', False),
                download_udebs=params.get('download_udebs', False),
                skip_component_check=params.get('skip_component_check', False),
                ignore_signatures=params.get('ignore_signatures', False),
                force_update=params.get('force_update', False)
            )
            self._cache.pop(name, None)  # Invalider le cache après la mise à jour
        except Exception as e:
            self.client.handle_error(e)

    def delete_mirror(self, name: str) -> None:
        """Delete a mirror"""
        try:
            self.client.client.mirrors.delete(name)
            self._cache.pop(name, None)
        except Exception as e:
            if "not found" not in str(e).lower():
                self.client.handle_error(e)

    def sync_mirror(self, name: str, ignore_signatures: bool = False) -> None:
        """Synchronize mirror with its source"""
        try:
            self.client.client.mirrors.update(name, ignore_signatures=ignore_signatures)
        except Exception as e:
            self.client.handle_error(e)

    @staticmethod
    def mirror_needs_update(existing_mirror: Mirror, params: Dict[str, Any]) -> bool:
        """Check if mirror configuration needs to be updated"""
        return any([
            existing_mirror.archiveurl != params.get('archive_url'),
            existing_mirror.filter != params.get('filter'),
            existing_mirror.components != params.get('components'),
            existing_mirror.architectures != params.get('architectures'),
            existing_mirror.filter_with_deps != params.get('filter_with_deps', False),
            existing_mirror.download_sources != params.get('download_sources', False),
            existing_mirror.download_udebs != params.get('download_udebs', False),
            existing_mirror.skip_component_check != params.get('skip_component_check', False)
        ])

    def list_mirrors(self) -> List[Dict[str, Any]]:
        """List all mirrors with their details"""
        try:
            mirrors = self.client.client.mirrors.list()
            return [self.format_mirror_info(mirror) for mirror in mirrors]
        except Exception as e:
            self.client.handle_error(e)
            return []

    def list_packages(self, name: str, query: Optional[str] = None,
                      with_deps: bool = False, detailed: bool = False) -> Sequence[Any]:
        """List packages in a mirror"""
        try:
            return self.client.client.mirrors.list_packages(
                name, query=query, with_deps=with_deps, detailed=detailed
            )
        except Exception as e:
            self.client.handle_error(e)
            return []
