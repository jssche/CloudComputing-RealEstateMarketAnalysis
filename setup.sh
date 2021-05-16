#!/usr/bin/env bash

. ./unimelb-comp90024-2021-grp-33-openrc.sh; ansible-playbook --ask-become-pass setup.yaml -i inventory/inventory.ini