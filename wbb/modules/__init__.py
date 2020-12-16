import importlib
from wbb import MOD_LOAD, MOD_NOLOAD, log

def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob
    # This generates a list of modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f)
        and f.endswith(".py")
        and not f.endswith("__init__.py")
        and not f.endswith("__main__.py")
    ]

    if MOD_LOAD or MOD_NOLOAD:
        to_Load = MOD_LOAD
        if to_Load:
            if not all(
                any(mod == module_name for module_name in all_modules)
                for mod in to_Load
            ):
                log.error("Invalid Module name!")
                quit(1)

        else:
            to_Load = all_modules

        if MOD_NOLOAD:
            log.info("No load: {}".format(MOD_NOLOAD))
            return [item for item in to_Load if item not in MOD_NOLOAD]

        return to_Load

    return all_modules


importlib.import_module("wbb.modules.__main__")
ALL_MODULES = sorted(__list_all_modules())
log.info("Modules loaded: %s", str(ALL_MODULES))
__all__ = ALL_MODULES + ["ALL_MODULES"]