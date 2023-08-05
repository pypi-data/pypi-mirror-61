#    Copyright 2018 - 2020 Alexey Stepanov aka penguinolog.

#    Copyright 2013 - 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""SSH client helper based on Paramiko. Extended API helpers."""

__all__ = ("SSHClient",)

# Standard Library
import os
import posixpath

# Local Implementation
from ._ssh_client_base import SSHClientBase


class SSHClient(SSHClientBase):
    """SSH Client helper."""

    __slots__ = ()

    def __enter__(self) -> "SSHClient":  # pylint: disable=useless-super-delegation
        """Get context manager.

        :return: SSHClient instance with entered context
        :rtype: SSHClient
        """
        return super().__enter__()

    @staticmethod
    def _path_esc(path: str) -> str:
        """Escape space character in the path.

        :param path: path to be escaped
        :type path: str
        :return: path with escaped spaces
        :rtype: str
        """
        return path.replace(" ", r"\ ")

    def mkdir(self, path: str) -> None:
        """Run 'mkdir -p path' on remote.

        :param path: path to create
        :type path: str
        """
        if self.exists(path):
            return
        # noinspection PyTypeChecker
        self.execute(f"mkdir -p {self._path_esc(path)}\n")

    def rm_rf(self, path: str) -> None:
        """Run 'rm -rf path' on remote.

        :param path: path to remove
        :type path: str
        """
        # noinspection PyTypeChecker
        self.execute(f"rm -rf {self._path_esc(path)}")

    def upload(self, source: str, target: str) -> None:
        """Upload file(s) from source to target using SFTP session.

        :param source: local path
        :type source: str
        :param target: remote path
        :type target: str
        """
        self.logger.debug(f"Copying '{source}' -> '{target}'")

        if self.isdir(target):
            target = posixpath.join(target, os.path.basename(source))

        source = os.path.expanduser(source)
        if not os.path.isdir(source):
            self._sftp.put(source, target)
            return

        for rootdir, _, files in os.walk(source):
            targetdir: str = os.path.normpath(os.path.join(target, os.path.relpath(rootdir, source))).replace("\\", "/")

            self.mkdir(targetdir)

            for entry in files:
                local_path: str = os.path.normpath(os.path.join(rootdir, entry))
                remote_path: str = posixpath.join(targetdir, entry)
                if self.exists(remote_path):
                    self._sftp.unlink(remote_path)
                self._sftp.put(local_path, remote_path)

    def download(self, destination: str, target: str) -> bool:
        """Download file(s) to target from destination.

        :param destination: remote path
        :type destination: str
        :param target: local path
        :type target: str
        :return: downloaded file present on local filesystem
        :rtype: bool
        """
        self.logger.debug(f"Copying '{destination}' -> '{target}' from remote to local host")

        if os.path.isdir(target):
            target = posixpath.join(target, os.path.basename(destination))

        if not self.isdir(destination):
            if self.exists(destination):
                self._sftp.get(destination, target)
            else:
                self.logger.debug(f"Can't download {destination} because it does not exist")
        else:
            self.logger.debug(f"Can't download {destination} because it is a directory")
        return os.path.exists(target)
