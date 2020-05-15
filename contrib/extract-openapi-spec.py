# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import yaml

from fastapi.openapi.utils import get_openapi
from wazo_router_confd.app import get_app

argparser = argparse.ArgumentParser(
    description='Extract wazo-router-confd OpenAPI spec'
)
argparser.add_argument(
    '--output', '-o', help='Output file where the OpenAPI spec should be extracted',
)
args = argparser.parse_args()

app = get_app({'database_uri': 'postgres://', 'redis_uri': ''})
spec = get_openapi(title='wazo-router-confd', version='1.0', routes=app.routes)

if args.output:
    with open(args.output, 'w') as f:
        yaml.dump(spec, f)
else:
    print(yaml.dump(spec), end='')
