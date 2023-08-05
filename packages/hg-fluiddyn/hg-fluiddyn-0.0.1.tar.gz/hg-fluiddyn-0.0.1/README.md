# hg-fluiddyn, a small Mercurial extension for the FluidDyn project

## What we would like to provide

- [x] check that the topic, evolve and rebase extensions are activated,

- [x] check paths for FluidDyn packages and automatically modify them if
needed,

  - `default = ssh://hg@foss.heptapod.net/fluiddyn/fluid???`
  - `bitbucket = ssh://hg@bitbucket.org/fluiddyn/fluid???` (only for maintainers)

- [ ] for maintainers:

  - [x] check that hg-git is activated,

  - [ ] a command for Github mirroring.

- [x] black pre-commit hook (better with Python >= 3.6),

- [ ] commands similar to fluiddevops

## Example of configuration for this extension (in `~/.hgrc`)

```raw

[fluiddyn]
root = ~/Dev
maintainer = 1

```
