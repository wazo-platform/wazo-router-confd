# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from configparser import ConfigParser, Error as ConfigParserError
from typing import Optional

import click
import uvicorn  # type: ignore

from .app import get_app


@click.command()
@click.option(
    "-c", "--config-file", type=click.Path(), help="Path to the configuration file"
)
@click.option(
    "--host",
    type=str,
    default="127.0.0.1",
    help="Bind socket to this host",
    show_default=True,
)
@click.option(
    "--port", type=int, default=9600, help="Bind socket to this port", show_default=True
)
@click.option(
    "--advertise-host",
    type=str,
    default="127.0.0.1",
    help="IP address or hostname to be advertised in Consul",
    show_default=True,
)
@click.option(
    "--advertise-port",
    type=int,
    default=9600,
    help="Port to be advertised in Consul",
    show_default=True,
)
@click.option(
    "--consul-uri",
    type=str,
    default=None,
    help="Consul agent URI, used to obtain environment configurations and perform service discovery",
    show_default=True,
)
@click.option(
    "--database-uri",
    type=str,
    default="postgresql://wazo:wazo@localhost/wazo",
    help="SQLAlchemy database URI, overwrites the configuration obtained from the Consul agent",
    show_default=True,
)
@click.option(
    "--database-upgrade",
    is_flag=True,
    default=True,
    help="Run database migrations at startup",
    show_default=True,
)
@click.option(
    "--redis-uri",
    type=str,
    default="redis://localhost",
    help="REDIS URI, overwrites the configuration obtained from the Consul agent",
    show_default=True,
)
@click.option(
    "--wazo-auth/--no-wazo-auth",
    default=False,
    help='enable wazo-auth based authentication and authorization, requires wazo-auth-url',
)
@click.option(
    "--wazo-auth-url",
    type=str,
    default="https://localhost:9497/api/auth/0.1",
    help="URL of the wazo-auth service, if set requires authentication to use the API",
    show_default=True,
)
@click.option(
    "--wazo-auth-cert",
    type=str,
    default=None,
    help="Path of the X509 certificate to verify when communicatin with the wazo-auth service",
    show_default=True,
)
@click.option(
    "--debug", is_flag=True, default=False, help="Enable debug mode", hidden=True
)
def main(
    config_file: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    advertise_host: Optional[str] = None,
    advertise_port: Optional[int] = None,
    consul_uri: Optional[str] = None,
    database_uri: Optional[str] = None,
    database_upgrade: bool = True,
    redis_uri: Optional[str] = None,
    wazo_auth: bool = False,
    wazo_auth_url: Optional[str] = None,
    wazo_auth_cert: Optional[str] = None,
    debug: bool = False,
    auto_envvar_prefix: Optional[str] = None,
):
    config = dict(
        host=host,
        port=port,
        advertise_host=advertise_host,
        advertise_port=advertise_port,
        consul_uri=consul_uri,
        database_uri=database_uri,
        database_upgrade=database_upgrade,
        redis_uri=redis_uri,
        wazo_auth=wazo_auth,
        wazo_auth_url=wazo_auth_url,
        wazo_auth_cert=wazo_auth_cert,
        debug=debug,
    )
    if config_file is not None:
        parser = ConfigParser()
        try:
            parser.read(config_file)
        except ConfigParserError:
            raise click.UsageError("Invalid configuration file")
        for k, v in parser['DEFAULT'].items():
            config[k] = v
    app = get_app(config)
    log_level = "info" if not config['debug'] else "debug"
    uvicorn.run(app, host=config['host'], port=config['port'], log_level=log_level)


def main_with_env():
    main(auto_envvar_prefix="WAZO_ROUTER_CONFD")
