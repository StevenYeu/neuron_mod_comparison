from importlib import util, import_module


def main():
    files_paths = ['./netpyne_inputs/m1/v101/netParams.py', './netpyne_inputs/m1/v103/netParams.py']
    # pkgs = [import_module(file_path, 'net') for file_path in files_paths]
    sepcs = [util.spec_from_file_location('m1',file_name) for file_name in files_paths]

    for spec in sepcs:
        mod = util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print(dir(mod))



if  __name__ == "__main__":
    main()
