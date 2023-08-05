# -*- coding: utf-8 -*-
import os


class PathHelper:
    project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), "../../"))
    project_log = None
    project_cfg = None

    @classmethod
    def set_project_root(cls, root_path):
        cls.project_root = os.path.realpath(root_path)

    @classmethod
    def get_project_root(cls):
        return cls.project_root

    @classmethod
    def get_project_log(cls):
        if cls.project_log is None:
            return os.path.join(cls.project_root, 'log')
        else:
            return cls.project_log

    @classmethod
    def get_project_cfg(cls):
        if cls.project_cfg is None:
            for one_cfg_name in ['cfg', 'config', 'conf']:
                cfg_path = os.path.join(cls.project_root, one_cfg_name)
                if os.path.exists(cfg_path):
                    cls.project_cfg = cfg_path
                    return cfg_path
            return os.path.join(cls.project_root, 'conf')
        else:
            return cls.project_cfg
