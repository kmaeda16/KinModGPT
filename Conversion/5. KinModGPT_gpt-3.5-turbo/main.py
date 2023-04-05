import os
import time
import argparse
import KinModGPT as kmg


start_time = time.time()

# ===== Handle arguments ===== #
parser = argparse.ArgumentParser()
parser.add_argument('-i','--instruction',  help='Name of input file of instruction',         required=True)
parser.add_argument('-d','--description',  help='Name(s) of input file(s) of model description', required=True)
parser.add_argument('-c','--conversation', help='Name of output file of whole conversation', required=False)
parser.add_argument('-a','--antimony',     help='Name of output file of Antimony model',     required=False)
parser.add_argument('-s','--sbml',         help='Name of output file of SBML model',         required=False)

args = parser.parse_args()

instruction_filename = args.instruction
model_desctription_filenames = args.description
conversation_log_filename   = args.conversation
ant_model_filename  = args.antimony
sbml_model_filename = args.sbml


# ===== Read input files ===== #
with open(instruction_filename) as f:
    instruction = f.read()

model_desctription_list = []
for filename in model_desctription_filenames.split():
    with open(filename.strip()) as f:
        model_desctription_list.append(f.read())


# ===== KinModGPT ===== #
api_key_path = os.path.expanduser('~') + '/.API keys/OpenAI.txt' # CHANGE HERE TO SET YOUR API KEY
prompt_list,response_list,GPT_output,ant_model,sbml_model = kmg.KinModGPT(instruction,model_desctription_list,api_key_path)


# ===== Write output files ===== #
if conversation_log_filename is not None:
    dirname = os.path.dirname(conversation_log_filename).strip()
    if dirname != '':
        os.makedirs(dirname, exist_ok=True)
    with open(conversation_log_filename,'w') as f:
        for prompt, response in zip(prompt_list, response_list):
            out = prompt+response["choices"][0]["message"]["content"]+'\n####\n'
            f.write(out)

if ant_model_filename is not None:
    dirname = os.path.dirname(ant_model_filename).strip()
    if dirname != '':
        os.makedirs(dirname, exist_ok=True)
    with open(ant_model_filename,'w') as f:
        f.write(ant_model)

if sbml_model_filename is not None:
    dirname = os.path.dirname(sbml_model_filename).strip()
    if dirname != '':
        os.makedirs(dirname, exist_ok=True)
    with open(sbml_model_filename,'w') as f:
        f.write(sbml_model)


end_time = time.time()
process_time = end_time - start_time
print('Process time: {:.3f}'.format(process_time))
