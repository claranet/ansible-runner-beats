# Ansible Runner beats Event Emitter
[![Maintainer](https://img.shields.io/badge/maintained%20by-claranet-e00000?style=flat-square)](https://www.claranet.fr/)
[![License](https://img.shields.io/github/license/claranet/ansible-runner-beats?style=flat-square)](LICENSE)
[![Release](https://img.shields.io/pypi/v/ansible-runner-beats?style=flat-square)](https://pypi.org/project/ansible-runner-beats/#history)

This project is a plugin for [Ansible Runner](https://github.com/ansible/ansible-runner) that allows emitting Ansible status and events to Logstash through the Beats protocol. This can allow `Runner` to notify other systems as Ansible jobs are run and to deliver key events to that system if it's interested.

It is useful to send data to Logstash through the Beats protocol.

This plugin is inspired by [ansible-runner-http](https://github.com/ansible/ansible-runner-http) licensed under Apache License 2.0


## :zap: Installation

```bash
python3 -m pip install ansible-runner-beats
```


## :gear: Variables

Runner config              | Environment variable       | Default value
---------------------------|----------------------------|----------------------------
runner_beats_host          | RUNNER_BEATS_HOST          | None
runner_beats_port          | RUNNER_BEATS_PORT          | None
runner_beats_ssl_cert      | RUNNER_BEATS_SSL_CERT      | ""
runner_beats_ssl_key       | RUNNER_BEATS_SSL_KEY       | ""
runner_beats_ssl_ca        | RUNNER_BEATS_SSL_CA        | ""
runner_beats_custom_fields | RUNNER_BEATS_CUSTOM_FIELDS | {}

The plugin also register an environment variable named `RUNNER_BEATS_TIMEDOUT` if the beats endpoint is not available

## :copyright: [License](LICENSE)

[Mozilla Public License Version 2.0](https://www.mozilla.org/en-US/MPL/2.0/)
