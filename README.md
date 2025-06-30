<div align="center">

# asdf-zls [![Build](https://github.com/zigcc/asdf-zls/actions/workflows/build.yml/badge.svg)](https://github.com/zigcc/asdf-zls/actions/workflows/build.yml)

[ZLS](https://zigtools.org/zls/install/) plugin for the [asdf version manager](https://asdf-vm.com).

</div>

# Dependencies

- `bash`, `python3`, `tar`, and [POSIX utilities](https://pubs.opengroup.org/onlinepubs/9699919799/idx/utilities.html).
- asdf 0.16+

# Install

First add asdf-zls as plugin:

```shell
asdf plugin add zls https://github.com/zigcc/asdf-zls.git
```

Then use `asdf-zls` to install zls:

```shell
# Show all installable versions
asdf list all zls

# Install specific version
asdf install zls 0.14.1

# Set a version globally (on your ~/.tool-versions file)
asdf set --home zig 0.14.1

# Now zls commands are available
zls --version
```

Check [asdf](https://github.com/asdf-vm/asdf) readme for more instructions on how to
install & manage versions.

# License

See [LICENSE](LICENSE) © [zigcc](https://github.com/zigcc/)
