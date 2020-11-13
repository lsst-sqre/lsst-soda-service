"""Sphinx configuration file for an LSST stack package.

This configuration only affects single-package Sphinx documentation builds.
"""

from documenteer.sphinxconfig.stackconf import build_package_configs
import lsst.lsst_soda_service


_g = globals()
_g.update(build_package_configs(
    project_name='lsst-soda-service',
    version=lsst.lsst_soda_service.version.__version__))
