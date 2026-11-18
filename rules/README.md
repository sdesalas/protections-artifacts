# Elastic Defend Behavior Protection Rules

The behavior protection rules are the prebuilt [EQL](https://www.elastic.co/guide/en/elasticsearch/reference/current/eql.html)
rules that run on the endpoint in [Elastic Defend](https://www.elastic.co/security/endpoint-security). They pair
post-execution analytics with response actions, such as killing a process or a process tree, to stop malicious behavior
on Windows, macOS and Linux hosts. Each rule is mapped to a [MITRE ATT&CK](https://attack.mitre.org/) tactic, technique
and subtechnique.

Rules are grouped by platform in the `windows`, `macos`, `linux` and `cross-platform` folders. Each file holds one rule:
its identity (`rule_id` and `version`), the EQL `query`, its response `actions`, and the minimum Elastic Defend version
it needs (`min_endpoint_version`).

The rules are also published as TOML in [`src/behavior`](https://github.com/elastic/protections-artifacts/tree/main/src/behavior)
of the protections-artifacts repository, together with the yara and ransomware artifacts.
