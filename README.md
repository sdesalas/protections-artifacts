[![ATT&CK navigator coverage](https://img.shields.io/badge/ATT&CK-Navigator-red.svg)](https://ela.st/protections-artifacts-navigator)
<h1><img src="https://static-www.elastic.co/v3/assets/bltefdd0b53724fa2ce/blt786d938064f8c8be/5e0e7b96fb35e665aed32798/logo-endpoint-32-color.svg"/>  Protections Artifacts</h1>


Elastic Security prevents ransomware and malware, detects advanced threats, and arms responders with vital context. It’s free and open, ready for every endpoint.

Protections-Artifacts is the home of our detection logic (rules, yara, etc) for [Elastic Security for endpoint](https://www.elastic.co/security/endpoint-security). At Elastic, we believe that being open and transparent is critical for the success of us and our users. Check out our [blog post](https://www.elastic.co/blog/continued-leadership-in-open-and-transparent-security) if you are interested in additional background.

# Directory

Below you will find the artifacts we have opened in this repository:

| Folder | Description |
| ------ | ----------- |
| [`src/behavior/`](src/behavior/) | EQL based malicious behavior rules, as TOML (the source of the rules library) |
| [`src/yara/`](src/yara) | Yara rules for malware protection |
| [`src/ransomware/`](src/ransomware/) | Elastic ransomware protection artifact  |
| [`rules/`](rules/) | The behavior rules as a rules library: one YAML file per rule, generated from `src/behavior/` |
| [`scripts/`](scripts/) | Tooling that builds `rules/` from `src/behavior/` |

# Rules library

`rules/` holds the behavior rules in the layout of a rule library, so a consumer can read them like any other
library of prebuilt rules.

```
rules/
  manifest.yml                     package manifest (name, version, kibana.version condition)
  changelog.yml                    one entry per release, linked to its pull request or commit
  NOTICE.txt                       notice shipped with the package
  README.md                        the package description
  endpoint-logo-color-32px.svg     the package icon (the manifest's `icons`)
  windows/<rule file name>.yml
  linux/<rule file name>.yml
  macos/<rule file name>.yml
  cross-platform/<rule file name>.yml
scripts/
  convert_rules.py                 rebuilds rules/ from src/behavior/rules/
```

- Every folder under `rules/` holds rule files, and only those. The folder is the one the rule has in `src/behavior/rules/`. The package files stay directly in `rules/`.
- Each file holds one rule as `{ id, type: "security-rule", attributes }`. `id` is `<rule_id>_<version>`.
  `attributes` has the fields of the TOML file: the `[rule]` table with `id` renamed to `rule_id`, plus `actions`,
  `threat` and `internal`.
- Keys keep the order of the TOML file, multi-line fields (`description`, `query`) are literal blocks, and the data is identical to the
  TOML when parsed.
- The rule files in `rules/` are generated. Edit the TOML under `src/behavior/` and rebuild. The package files are edited by hand, and the manifest `version` is the latest release in `changelog.yml`.

```sh
python3 scripts/convert_rules.py
```

Python 3.11 or newer, standard library only. The script reports rule ids that appear in more than one file; a few
rules have a `cross-platform/` and a `macos/` variant with the same id and version.

# Questions? Problems? Suggestions?

If you would like you to provide feedback or contribute to this repository, please familiarize yourself with the applicable artifact’s readme and [open an issue](https://github.com/elastic/protections-artifacts/issues/new/choose) using one of the provided templates. We cannot accept pull requests at this time because this repository is automatically generated.

You can also reach us in our [Slack Workspace](https://www.elastic.co/blog/join-our-elastic-stack-workspace-on-slack) or in the [Security Discuss](https://discuss.elastic.co/c/security/) forum.

# License

Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one or more contributor license agreements. Licensed under the Elastic License 2.0; you may not use these artifacts except in compliance with the Elastic License 2.0

Contributors must sign a [Contributor License Agreement](https://www.elastic.co/contributor-agreement) before contributing code to any Elastic repositories.
