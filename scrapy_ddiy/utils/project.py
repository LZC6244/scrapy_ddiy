# -*- coding: utf-8 -*-
import os
import pickle
import warnings

from scrapy.settings import Settings
from scrapy.utils.conf import init_env
from scrapy.utils.project import ENVVAR
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy_ddiy.ddiy_settings import default_settings, online_settings

"""
根据 scrapy.utils.project 进行重写
配置优先级：online_settings > settings > default_settings
"""


def get_project_settings():
    if ENVVAR not in os.environ:
        project = os.environ.get('SCRAPY_PROJECT', 'default')
        init_env(project)

    settings = Settings()
    settings_module_path = os.environ.get(ENVVAR)
    if settings_module_path:
        _update_settings(settings, default_settings)
        settings.setmodule(settings_module_path, priority='project')
        if os.environ.get('ENV_FLAG_DDIY') == 'online':
            _update_settings(settings, online_settings)

    pickled_settings = os.environ.get("SCRAPY_PICKLED_SETTINGS_TO_OVERRIDE")
    if pickled_settings:
        warnings.warn("Use of environment variable "
                      "'SCRAPY_PICKLED_SETTINGS_TO_OVERRIDE' "
                      "is deprecated.", ScrapyDeprecationWarning)
        settings.setdict(pickle.loads(pickled_settings), priority='project')

    scrapy_envvars = {k[7:]: v for k, v in os.environ.items() if
                      k.startswith('SCRAPY_')}
    valid_envvars = {
        'CHECK',
        'PICKLED_SETTINGS_TO_OVERRIDE',
        'PROJECT',
        'PYTHON_SHELL',
        'SETTINGS_MODULE',
    }
    setting_envvars = {k for k in scrapy_envvars if k not in valid_envvars}
    if setting_envvars:
        setting_envvar_list = ', '.join(sorted(setting_envvars))
        warnings.warn(
            'Use of environment variables prefixed with SCRAPY_ to override '
            'settings is deprecated. The following environment variables are '
            'currently defined: {}'.format(setting_envvar_list),
            ScrapyDeprecationWarning
        )
    settings.setdict(scrapy_envvars, priority='project')

    project_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
    current_path = os.getcwd()
    if not current_path.startswith(project_path):
        raise EnvironmentError(
            f'The program runs in a non-project path (current_path:{current_path} => project_path:{project_path})')
    return settings


def _update_settings(settings: Settings, new_settings):
    """
    更新框架配置
    :param settings: type is module
    :param new_settings: default_settings, online_settings, ...
    :return:
    """
    for name in dir(new_settings):
        if not name.isupper():
            continue
        new_value = getattr(new_settings, name)
        current_value = settings.get(name)
        if not current_value or not isinstance(new_value, dict):
            settings.set(name, new_value)
        else:
            for k, v in new_value.items():
                current_value[k] = new_value[k]
