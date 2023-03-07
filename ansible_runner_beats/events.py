import os
import json
import sys
import socket
from datetime import datetime
import pylogbeat
from pylogbeat import PyLogBeatClient
import logging

logger = logging.getLogger("ansible-runner")

configuration_keys = {
    "runner_beats_host": None,
    "runner_beats_port": None,
    "runner_beats_ssl_cert": "",
    "runner_beats_ssl_key": "",
    "runner_beats_ssl_ca": "",
    "runner_beats_custom_fields": {},
}


def send_event(host, port, message, certificate=None, key=None, ca=None):
    with PyLogBeatClient(
        host,
        int(port),
        timeout=10,
        ssl_enable=True if certificate and key else False,
        ssl_verify=True if ca else False,
        keyfile=key,
        certfile=certificate,
        ca_certs=ca,
    ) as client:
        client.send([message])


def get_configuration(runner_config):
    def get_conf(conf, default=None):
        r = os.getenv(  # Get variable from environment first
            conf.upper(),
            runner_config.settings.get(
                conf, default
            ),  # Instead, get variable form ansible-runner config or get default
        )

        try:
            if r:
                r = json.loads(r)  # Eval json from string for env vars
        except (ValueError, TypeError):
            pass

        return r

    configuration = dict()

    for c, v in configuration_keys.items():
        configuration[c] = get_conf(c, default=v)

    return configuration


def status_handler(runner_config, data):
    plugin_config = get_configuration(runner_config)
    if (
        plugin_config["runner_beats_host"] is not None
        and plugin_config["runner_beats_port"] is not None
    ):
        message = {
            "@timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
            "type": "ansible-runner",
        }
        # raise Exception(plugin_config["runner_beats_custom_fields"])
        message["fields"] = data

        if plugin_config["runner_beats_custom_fields"]:
            from deepmerge import Merger

            custom_merger = Merger(
                # pass in a list of tuple, with the
                # strategies you are looking to apply
                # to each type.
                [(list, ["append"]), (dict, ["merge"]), (set, ["union"])],
                # next, choose the fallback strategies,
                # applied to all other types:
                ["override"],
                # finally, choose the strategies in
                # the case where the types conflict:
                ["use_existing"],
            )

            message = custom_merger.merge(
                plugin_config["runner_beats_custom_fields"], message
            )

        try:
            if os.environ.get("RUNNER_BEATS_TIMEDOUT") != "true":
                send_event(
                    plugin_config["runner_beats_host"],
                    plugin_config["runner_beats_port"],
                    message,
                    certificate=plugin_config["runner_beats_ssl_cert"],
                    key=plugin_config["runner_beats_ssl_key"],
                    ca=plugin_config["runner_beats_ssl_ca"],
                )
        except (TimeoutError, socket.timeout) as e:
            os.environ["RUNNER_BEATS_TIMEDOUT"] = "true"
            print(
                f"Connection to {plugin_config['runner_beats_host']}:{plugin_config['runner_beats_port']} timed out!\n{e}",
                file=sys.stderr,
            )
        except (
            ConnectionResetError,
            pylogbeat.ConnectionException,
        ) as e:
            print(
                f"{e} ({plugin_config['runner_beats_host']}:{plugin_config['runner_beats_port']})",
                file=sys.stderr,
            )
    else:
        logger.info("Beats Plugin Skipped")


def event_handler(runner_config, data):
    status_handler(runner_config, data)
