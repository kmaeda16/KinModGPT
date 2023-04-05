# See https://github.com/sorgerlab/indra/blob/master/doc/tutorials/nl_modeling.rst
import os
import time
import argparse
from indra.sources import trips
from indra.assemblers.pysb import PysbAssembler


start_time = time.time()

# ===== Handle arguments ===== #
parser = argparse.ArgumentParser()
parser.add_argument('-d','--description', help='Name(s) of input file(s) of model description', required=True)
parser.add_argument('-s','--sbml',        help='Name of output file of SBML model',         required=True)

args = parser.parse_args()
model_desctription_filenames = args.description
sbml_model_filename = args.sbml

# ===== Read input files ===== #
model_desctription = ''
for filename in model_desctription_filenames.split():
    with open(filename.strip()) as f:
        model_desctription += f.read()

print(model_desctription)

tp = trips.process_text(model_desctription)

for st in tp.statements:
    print('%s with evidence "%s"' % (st, st.evidence[0].text))

pa = PysbAssembler()
pa.add_statements(tp.statements)
pa.make_model(policies='two_step')

for monomer in pa.model.monomers:
    print(monomer)

for rule in pa.model.rules:
    print(rule)

for parameter in pa.model.parameters:
    print(parameter)

for annotation in pa.model.annotations:
    print(annotation)

# ===== Write output files ===== #
dirname = os.path.dirname(sbml_model_filename).strip()
if dirname != '':
    os.makedirs(dirname, exist_ok=True)
pa.export_model('sbml',sbml_model_filename)


end_time = time.time()
process_time = end_time - start_time
print('Process time: {:.3f}'.format(process_time))
