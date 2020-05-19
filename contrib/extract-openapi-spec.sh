#!/bin/bash
# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

set -e

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
cd "${SCRIPTPATH}/.."

output_file="$1"

if [ -n "${output_file}" ] ; then
    options="-o ${output_file}"
fi

virtualenv /tmp/wazo-router-confd-release-venv -p python3.7
source /tmp/wazo-router-confd-release-venv/bin/activate
pip install -e .
pip install pyyaml

python "${SCRIPTPATH}/extract-openapi-spec.py" ${options}
