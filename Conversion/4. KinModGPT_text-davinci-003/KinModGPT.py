import os
import sys
import openai
import tellurium as te


# ===== talk_to_GPT ===== #
def talk_to_GPT(prompt,api_key_path):

    openai.api_key_path = api_key_path

    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0, # No randomness
      max_tokens=2048,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    return response


# ===== clean_GPT_output ===== #
def clean_GPT_output(GPT_output):

  cleaned = ''

  for line in GPT_output.splitlines():

    line = line.strip()

    if line != '' and ( line[0] == '-' or line[0] == '•' or line[0] == '*'):
        cleaned += line[1:].strip() + '\n'

    if ':' in line:
      line = line.split(':')[-1]

  return(cleaned)


# ===== KinModGPT ===== #
def KinModGPT(instruction,model_desctription_list,api_key_path,verbose=1):

  prompt_list = []
  response_list = []
  GPT_output = ''

  if verbose > 0:
    print("========== Conversation log ==========")
    sys.stdout.flush()

  for model_description in model_desctription_list:

    prompt   = instruction + model_description
    response = talk_to_GPT(prompt,api_key_path)

    if verbose > 0:
      print(prompt+response.choices[0].text,end='\n####\n')
      sys.stdout.flush()

    prompt_list.append(prompt)
    response_list.append(response)
    GPT_output += response.choices[0].text + '\n'
  
  ant_model  = clean_GPT_output(GPT_output)

  if verbose > 0:
    print("============== Antimony ==============")
    print(ant_model)
    
  sbml_model = te.antimonyToSBML(ant_model)

  if verbose > 0:
    print("================ SBML ================")
    print(sbml_model)
    print("======================================")

  return(prompt_list,response_list,GPT_output,ant_model,sbml_model)


# ===== KinModGPT ===== #
def test_KinModGPT():
  api_key_path = os.path.expanduser('~') + '/.API keys/OpenAI.txt' # CHANGE HERE TO SET YOUR API KEY
  instruction = '''You are a program that converts biochemical reactions written in natural language into Antimony language. First, remember the following conversion rules.

# Conversion rules
| Natural language | Antimony language | 
| E catalyzes the conversion of X to Y | X -> Y ; kcat_E_X_Y * E * X / ( Km_E_X_Y + X ) ; kcat_E_X_Y = 1 ; Km_E_X_Y = 1; E = 1 |
| X is produced (or transcribed) | -> X ; km_X ; km_X  = 1 |
| Expression of X is repressed (or negatively regulated or downregulated) by R | -> X ; km_X_R * K_X_R ^ n_X_R / ( K_X_R ^ n_X_R + R ^ n_X_R ) ; km_X_R = 1 ; K_X_R = 1 ; n_X_R = 1 |
| Expression of X is activated (or positively regulated or upregulated) by A | -> X ; km_X_A * A ^ n_X_A / ( K_X_A ^ n_X_A + A ^ n_X_A ) ; km_X_A = 1 ; K_X_A = 1 ; n_X_A = 1 |
| Y is translated from X | -> Y ; kp_X_Y * X ; kp_X_Y = 1 |
| X degrades (or decays) | X -> ; kdeg_X * X ; kdeg_X = 1 |
| X (concentration) is Y M (or mM or uM or nM or pM) | X = Y |

# Examples
"The expression of G is negatively regulated by R." is converted into "-> G ; km_G_R * K_G_R ^ n_G_R / ( K_G_R ^ n_G_R + R ^ n_G_R ) ; km_G_R = 1 ; K_G_R = 1 ; n_G_R = 1"
"G is upregulated by A." is converted into "-> G ; km_G_A * A ^ n_G_A / ( K_G_A ^ n_G_A + A ^ n_G_A ) ; km_G_A = 1 ; K_G_A = 1 ; n_G_A = 1"

Using the conversion rules provided, convert the biochemical reactions listed below into Antimony language. After converting each reaction, create a bullet point list that includes all the resulting expressions. In the list, show one reaction per line. No need to provide further explanations, just present the list. Start each line with '-'.


'''
  model_desctription_list = ['Protein P decays. The initial concentration is 1 mM.']
  KinModGPT(instruction,model_desctription_list,api_key_path)
  

# ============ Main ============ #
if __name__ == "__main__":
    test_KinModGPT()
