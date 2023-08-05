#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from builtins import object
import os
import sys
import random
import logging
import argparse
import copy
import codecs
import re

from jinja2 import Environment, FileSystemLoader
import six

from coshed.bundy import PATTERN_VALID_APP_NAME
from coshed.bundy import REGEX_VALID_APP_NAME
from coshed.wolfication_template_contents import TEMPLATES_CONTENT

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

TEMPLATE_ARGS = dict(
    app_root=os.path.abspath(os.getcwd()),
    brand_name=None,
    project_root=os.path.abspath(os.getcwd()),
)

TEMPLATE_ARGS['static_folder'] = os.path.join(
    TEMPLATE_ARGS['app_root'], 'static')

CONFIGURATION_FOLDERS = dict(
    uwsgi_vassals='/etc/uwsgi-emperor/vassals',
    nginx_sites_available='/etc/nginx/sites-available',
    nginx_sites_enabled='/etc/nginx/sites-enabled',
)

CONFIGURATION_FOLDERS_CENTOS = dict(
    uwsgi_vassals='/etc/uwsgi.d',
    nginx_conf_d='/etc/nginx/conf.d',
)


class Wolfication(object):
    def __init__(self, app_name, listen_port=None, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.dry_run = kwargs.get("dry_run", False)
        self.do_init = kwargs.get("do_init", False)

        if listen_port is None:
            listen_port = random.randint(23000, 60000)
        else:
            listen_port = int(listen_port)

        if not re.match(REGEX_VALID_APP_NAME, app_name):
            self.log.warning("Invalid app name {!r}, "
                             "valid names regular expression is {!s}".format(
                app_name, PATTERN_VALID_APP_NAME))
            raise ValueError("Invalid app name")

        self.template_args = {
            "app_name": app_name,
            "listen_port": listen_port,
            "index_file": 'index.{:s}.json'.format(app_name)
        }
        self.template_args.update(TEMPLATE_ARGS)

        for key in kwargs:
            self.template_args[key] = kwargs[key]

        if self.template_args['brand_name'] is None:
            self.template_args['brand_name'] = app_name

        self.project_root = self.template_args['project_root']
        self.template_args['contrib_root'] = os.path.abspath(
            os.path.join(self.project_root, 'contrib')
        )

        sys.path.insert(0, self.project_root)

        self.templates_root = os.path.abspath(
            os.path.join(self.template_args['contrib_root'], 'templates/webapp')
        )

        self.template_args['templates_root'] = self.templates_root

        for key, value in sorted(six.iteritems(self.template_args)):
            self.log.info("{key:20}: {value}".format(key=key, value=value))

        self.env = Environment(loader=FileSystemLoader(self.templates_root))

    def skeleton_app(self):
        template = self.env.get_template('skeletor.py')
        return template.render(**self.template_args)

    def nginx_site(self):
        template = self.env.get_template('nginx/site.conf.jinja2')
        return template.render(**self.template_args)

    def uwsgi_vassal(self):
        template = self.env.get_template('uwsgi-emperor/app.ini.jinja2')
        return template.render(**self.template_args)

    def _dump(self, path, content, overwrite=False):
        if os.path.exists(path) and not overwrite:
            raise IOError("existis: {!s}".format(path))

        with codecs.open(path, "wb", 'utf-8') as tgt:
            tgt.write(content)

    def instructor(self, spec, configuration_folders=None):
        if configuration_folders is None:
            configuration_folders = CONFIGURATION_FOLDERS

        merged = copy.copy(configuration_folders)

        for key in spec:
            merged[key] = spec[key][0]

        merged['nginx_config_bname'] = os.path.basename(merged['nginx_config'])

        messages = [
            '#' * 80,
            '# Installation instructions ...',
            '#' * 80,
            'ln -s {uwsgi_config} {uwsgi_vassals}'.format(**merged),
        ]

        if 'nginx_sites_available' in merged:
            messages.append(
                'ln -s {nginx_config} {nginx_sites_available}'.format(
                    **merged))
            messages.append(
                'ln -s '
                '{nginx_sites_available}/{nginx_config_bname} '
                '{nginx_sites_enabled}'.format(**merged))
        else:
            messages.append(
                'ln -s {nginx_config} {nginx_conf_d}'.format(**merged))

        for msg in messages:
            self.log.info(msg)

    def _initialise_environment(self):
        roots = (
        'project_root', 'templates_root', 'contrib_root', 'static_folder')

        for root_key in roots:
            root_dir = self.template_args[root_key]

            if not os.path.isdir(root_dir):
                self.log.warning("Missing folder {!s}: {!s}".format(
                    root_key, root_dir))
                os.makedirs(root_dir)
        for rel_path, content in six.iteritems(TEMPLATES_CONTENT):
            abs_path = os.path.join(self.template_args['templates_root'],
                                    rel_path)

            if not os.path.isfile(abs_path):
                rel_folder = os.path.dirname(rel_path)
                abs_folder = os.path.join(self.template_args['templates_root'],
                                          rel_folder)
                os.makedirs(abs_folder, exist_ok=True)

            with open(abs_path, "w") as tgt:
                tgt.write(content)

    def persist(self):
        if self.do_init:
            self._initialise_environment()

        spec = dict(
            nginx_config=('{contrib_root}/nginx/{app_name}.conf'.format(
                **self.template_args), self.nginx_site),
            uwsgi_config=('{contrib_root}/uwsgi-emperor/{app_name}.ini'.format(
                **self.template_args), self.uwsgi_vassal),
            app=('{project_root}/{app_name}.py'.format(
                **self.template_args), self.skeleton_app),
        )

        self.log.info(
            "Creating {app_name} on port {listen_port} with "
            "app_root {app_root}".format(**self.template_args))

        if self.dry_run:
            self.log.info("DRY RUN.")

        for target, func in list(spec.values()):
            if self.dry_run:
                self.log.info("WOULD write {!s}".format(target))
                continue

            self.log.debug(target)
            target_parent = os.path.dirname(target)
            if not os.path.isdir(target_parent):
                os.makedirs(target_parent)
            self._dump(target, func(), overwrite=self.template_args['force'])
        self.instructor(spec, self.template_args['configuration_folders'])


def cli_stub():
    description = "Webapp skeleton generator"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('app_name', metavar='APP',
                        help='web application name')

    parser.add_argument(
        '-n', '--dry-run', action='store_true',
        dest="dry_run",
        default=False, help="Dry run mode")

    parser.add_argument(
        '-f', '--force', action='store_true',
        dest="force",
        default=False, help="force mode (overwrites stuff etc.)")

    parser.add_argument(
        '-p', '--port', default=None, type=int,
        help="listening port", dest="listen_port"
    )

    parser.add_argument(
        '--platform-centos', default=CONFIGURATION_FOLDERS,
        action="store_const",
        const=CONFIGURATION_FOLDERS_CENTOS,
        help="Use CentOS platform configuration defaults",
        dest="configuration_folders"
    )

    parser.add_argument(
        '-i', '--init', action='store_true',
        dest="do_init",
        default=False, help="Initialise environment")

    params_group = parser.add_argument_group("More Parameters")
    for key in TEMPLATE_ARGS:
        params_group.add_argument(
            '--{:s}'.format(key), default=TEMPLATE_ARGS[key],
            help="{:s}. Default is %(default)s".format(key),
            dest=key
        )

    cli_args = parser.parse_args()

    try:
        wolfication = Wolfication(**vars(cli_args))
    except ValueError as vexc:
        sys.exit(1)

    wolfication.persist()
