<div align="center">

# adsf-zls [![Build](https://github.com/zigcc/adsf-zls/actions/workflows/build.yml/badge.svg)](https://github.com/zigcc/adsf-zls/actions/workflows/build.yml)

[zls](https://zigtools.org/zls/install/) plugin for the [asdf version manager](https://asdf-vm.com).

</div>

# Dependencies

- `bash`, `python3`, `tar`, and [POSIX utilities](https://pubs.opengroup.org/onlinepubs/9699919799/idx/utilities.html).
- asdf 0.16+

# Install

First add adsf-zls as plugin:

```shell
asdf plugin add zls https://github.com/zigcc/adsf-zls.git
```

Then use `adsf-zls` to install zls:

```shell
# Show all installable versions
asdf list all zig

# Install specific version
asdf install zig latest

# Set a version globally (on your ~/.tool-versions file)
asdf set --home zig latest

# Now adsf-zls commands are available
zig version
```

Check [asdf](https://github.com/asdf-vm/asdf) readme for more instructions on how to
install & manage versions.

# License

See [LICENSE](LICENSE) © [zigcc](https://github.com/zigcc/)
