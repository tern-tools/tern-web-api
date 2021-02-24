#!/bin/sh
#
# SPDX-License-Identifier: BSD-2-Clause
#
# Script to run Tern web ui within a prebuilt Docker container
# Assume the Tern Docker container exists on the host
# It will run a docker container in privileged mode and hostnetwork,
# then listen on port 127.0.0.1:5000
#
# Usage: ./docker_run_web.sh <tern image>
# Example: ./docker_run_web.sh tern-api

docker run --privileged --network host -e FLASK_APP=/web/app.py --device /dev/fuse -v /var/run/docker.sock:/var/run/docker.sock -it $1 run
