import os
import time
import sys
import argparse
import openai


# ===== talk_to_GPT ===== #
def talk_to_GPT(instruction,model_description,api_key_path):

    openai.api_key_path = api_key_path

    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
         {
             "role": "system",
             "content": instruction
         },
         {
             "role": "user",
             "content": model_description
         },
     ],
      temperature=0, # No randomness
      max_tokens=2048,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    return response


# ===== GPT_only ===== #
def GPT_only(instruction,model_desctription_list,api_key_path,verbose=1):

  if verbose > 0:
    print("========== Conversation log ==========")
    sys.stdout.flush()

  model_description = ''
  for md in model_desctription_list:
    model_description += md

  response   = talk_to_GPT(instruction,model_description,api_key_path)
  sbml_model = response["choices"][0]["message"]["content"]

  prompt = instruction + model_description

  if verbose > 0:
    print(prompt+sbml_model)
    print("======================================")

  return(prompt,response,sbml_model)


start_time = time.time()

# ===== Handle arguments ===== #
parser = argparse.ArgumentParser()
parser.add_argument('-i','--instruction',  help='Name of input file of instruction',         required=True)
parser.add_argument('-d','--description',  help='Name(s) of input file(s) of model description', required=True)
parser.add_argument('-c','--conversation', help='Name of output file of whole conversation', required=False)
parser.add_argument('-s','--sbml',         help='Name of output file of SBML model',         required=False)

args = parser.parse_args()

instruction_filename = args.instruction
model_desctription_filenames = args.description
conversation_log_filename   = args.conversation
sbml_model_filename = args.sbml


# ===== Read input files ===== #
with open(instruction_filename) as f:
    instruction = f.read()

model_desctription_list = []
for filename in model_desctription_filenames.split():
    with open(filename.strip()) as f:
        model_desctription_list.append(f.read())


# ===== GPT_only ===== #
api_key_path = os.path.expanduser('~') + '/.API keys/OpenAI.txt' # CHANGE HERE TO SET YOUR API KEY
prompt,response,sbml_model = GPT_only(instruction,model_desctription_list,api_key_path)


# ===== Write output files ===== #
if conversation_log_filename is not None:
    dirname = os.path.dirname(conversation_log_filename).strip()
    if dirname != '':
        os.makedirs(dirname, exist_ok=True)
    with open(conversation_log_filename,'w') as f:
        out = prompt + sbml_model + '\n####\n'
        f.write(out)

if sbml_model_filename is not None:
    dirname = os.path.dirname(sbml_model_filename).strip()
    if dirname != '':
        os.makedirs(dirname, exist_ok=True)
    with open(sbml_model_filename,'w') as f:
        f.write(sbml_model)


end_time = time.time()
process_time = end_time - start_time
print('Process time: {:.3f}'.format(process_time))
