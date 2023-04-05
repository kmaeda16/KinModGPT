#!/bin/sh

# Display system information
echo $0
echo

date "+%Y/%m/%d %H:%M:%S"
echo

hostname
echo

conda info
conda list --export
pip freeze
conda env export > env.yml
echo



func(){
    cmd="python main.py -i $1 -d $2 -c $3 -a $4 -s $5"
    echo $cmd
    $cmd
    echo
}

instruction=Instruction.txt


# decay
model=decay
description="../input/$model/$model.txt"
conversation="Results/$model/${model}_conversation_log.txt"
antimony="Results/$model/${model}_Antimony_model.txt"
sbml="Results/$model/${model}_SBML_model.xml"
func $instruction $description $conversation $antimony $sbml

# hiv
model=hiv
description="../input/$model/$model.txt"
conversation="Results/$model/${model}_conversation_log.txt"
antimony="Results/$model/${model}_Antimony_model.txt"
sbml="Results/$model/${model}_SBML_model.xml"
func $instruction $description $conversation $antimony $sbml

# three-step
model=three-step
description="../input/$model/$model.txt"
conversation="Results/$model/${model}_conversation_log.txt"
antimony="Results/$model/${model}_Antimony_model.txt"
sbml="Results/$model/${model}_SBML_model.xml"
func $instruction $description $conversation $antimony $sbml

# heat_shock_response
echo python main.py -i Instruction.txt -d '../input/heat_shock_response/heat_shock_response-1.txt ../input/heat_shock_response/heat_shock_response-2.txt' -c Results/heat_shock_response/heat_shock_response_conversation_log.txt -a Results/heat_shock_response/heat_shock_response_Antimony_model.txt -s Results/heat_shock_response/heat_shock_response_SBML_model.xml

python main.py -i Instruction.txt -d '../input/heat_shock_response/heat_shock_response-1.txt ../input/heat_shock_response/heat_shock_response-2.txt' -c Results/heat_shock_response/heat_shock_response_conversation_log.txt -a Results/heat_shock_response/heat_shock_response_Antimony_model.txt -s Results/heat_shock_response/heat_shock_response_SBML_model.xml

echo
