#!/usr/bin/env python3
# coding: utf-8

import os
import random
import platform
import sys
import urllib.request
from urllib.error import HTTPError
from urllib.parse import urljoin
import json
import hashlib
import logging

INDEX_URL = os.getenv("ASDF_ZLS_INDEX_URL", "https://builds.zigtools.org/index.json")
HTTP_TIMEOUT = int(os.getenv("ASDF_ZLS_HTTP_TIMEOUT", "30"))

OS_MAPPING = {
    "darwin": "macos",
}
ARCH_MAPPING = {
    "i386": "x86",
    "i686": "x86",
    "amd64": "x86_64",
    "arm64": "aarch64",
}

USER_AGENT = "asdf-zls (https://github.com/zigcc/adsf-zls.git)"

def http_get(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        return urllib.request.urlopen(req, timeout=HTTP_TIMEOUT)
    except HTTPError as e:
        body = e.read().decode("utf-8")
        if 'application/json' in e.headers.get('content-type'):
            msg = json.loads(body)['message']
        else:
            msg = f"{url} access failed, code:{e.code}, reason:{e.reason}, body:{body}"

        raise Exception(msg)

def fetch_index():
    with http_get(INDEX_URL) as response:
        body = response.read().decode("utf-8")
        return json.loads(body)


def query_version(zig_version):
    url = f'https://releases.zigtools.org/v1/zls/select-version?zig_version={zig_version}&compatibility=full'
    with http_get(url) as response:
        body = response.read().decode("utf-8")
        return json.loads(body)

def all_versions(index):
    versions = [k for k in index.keys()]
    versions.sort(key=lambda v: tuple(map(int, v.split("."))))
    return versions


def download_and_check(url, out_file, expected_shasum, total_size):
    logging.info(f"Begin download tarball({total_size}) from {url} to {out_file}...")
    chunk_size = 1024 * 1024 # 1M chunks
    sha256_hash = hashlib.sha256()
    with http_get(url) as response:
        read_size = 0
        with open(out_file, "wb") as f:
            while True:
                chunk = response.read(chunk_size)
                read_size += len(chunk)
                progress_percentage = (read_size / total_size) * 100 if total_size > 0 else 0
                logging.info(f'Downloaded: {read_size}/{total_size} bytes ({progress_percentage:.2f}%)')
                if not chunk:
                    break  # eof
                sha256_hash.update(chunk)
                f.write(chunk)

    actual = sha256_hash.hexdigest()
    if actual != expected_shasum:
        raise Exception(
            f"Shasum not match, expected:{expected_shasum}, actual:{actual}"
        )


def download(version, out_file):
    links = query_version(version)
    os_name = platform.system().lower()
    arch = platform.machine().lower()
    os_name = OS_MAPPING.get(os_name, os_name)
    arch = ARCH_MAPPING.get(arch, arch)
    link_key = f"{arch}-{os_name}"
    if link_key not in links:
        raise Exception(f"No tarball link for {link_key} in {version}")

    tarball_url = links[link_key]["tarball"]
    tarball_shasum = links[link_key]["shasum"]
    tarball_size = int(links[link_key]["size"])
    download_and_check(tarball_url, out_file, tarball_shasum, tarball_size)


def main(args):
    command = args[0] if args else "all-versions"
    if command == "all-versions":
        versions = all_versions(fetch_index())
        print(" ".join(versions))
    elif command == "latest-version":
        versions = all_versions(fetch_index())
        print(versions[-1])
    elif command == "download":
        download(args[1], args[2])
    else:
        logging.error(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
    main(sys.argv[1:])
