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
        settings.setmodule(settings_module_path, priority='project')

        # 载入 scrapy_ddiy 的默认设置
        for name in dir(default_settings):
            if not name.isupper():
                continue
            default_value = getattr(default_settings, name)
            current_value = settings.get(name)
            if current_value:
                if isinstance(default_value, dict):
                    for k, v in default_value.items():
                        current_value[k] = current_value.get(k) or default_value.get(k)
            else:
                # 以 settings 中配置为最终配置
                settings.set(name, default_value)
        if os.environ.get('ENV_FLAG_DDIY') == 'online':
            # 载入 scrapy_ddiy 的线上设置，线上配置为最高优先级配置
            for name in dir(online_settings):
                if not name.isupper():
                    continue
                online_value = getattr(online_settings, name)
                current_value = settings.get(name)
                if isinstance(online_value, dict):
                    for k, v in online_value.items():
                        current_value[k] = online_value[k]

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
