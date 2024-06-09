from pathlib import Path
from nmodl import dsl, visitor, ast
import sys

import nmodl


def main():

    inputs_files = "lsh_test/mod_test"
    file_one = sys.argv[1]
    # files = [join(inputs_files,f) for f in listdir(inputs_files) if isfile(join(inputs_files, f))]
    # docs = [(f,Path(f).read_text()) for f in files]
    # first_file = docs[0][1]
    lookup = visitor.AstLookupVisitor()

    first_file = Path(file_one).read_text()
    driver = dsl.NmodlDriver()
    modast = driver.parse_string(first_file)
    states = lookup.lookup(modast, ast.AstNodeType.UNIT_BLOCK)

    if len(states) < 1:
        print("mod file has no unit block")

    for state in states:
        units = nmodl.to_nmodl(state).split("\n")
        if len(units) <= 2:
            print("no units")
            break
        units = [u.strip() for u in units[1:len(units)-1]]
        units.sort()
        print('\n'.join(units))
        




if __name__ == "__main__":
    main()
