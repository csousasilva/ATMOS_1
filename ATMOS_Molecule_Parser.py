from ATMOS_Molecule import Molecule

class Molecule_Parser:
    def molecules_for(self, molecule_data, functional_data):
        missing_functional_codes = set()
        molecules = {}
        for molecule_code, molecule_functionals in molecule_data.iteritems():
            molecule = Molecule(molecule_code)

            for functional_tuple in molecule_functionals:
                if '#' in functional_tuple[0]:

                    functional_code = functional_tuple[0]

                    if functional_data.keys().__contains__(functional_code):
                        functional = functional_data[functional_code]
                        functional_incidence = functional_tuple[1]
                        molecule.addFunctional(functional, functional_incidence)
                    else:
                        missing_functional_codes.add(functional_code)

            molecules[molecule_code] = molecule
        print "These are missing", list(missing_functional_codes)
        return molecules
