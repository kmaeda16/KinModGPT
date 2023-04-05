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
    cmd="python main.py -d $1 -s $2"
    echo $cmd
    $cmd
    echo
}

# example
model=example
description="$model/$model.txt"
sbml="$model/${model}_SBML_model.xml"
func $description $sbml

# decay
model=decay
description="../input/$model/$model.txt"
sbml="Results/$model/${model}_SBML_model.xml"
func $description $sbml

# hiv
model=hiv
description="../input/$model/$model.txt"
sbml="Results/$model/${model}_SBML_model.xml"
func $description $sbml

# three-step
model=three-step
description="../input/$model/$model.txt"
sbml="Results/$model/${model}_SBML_model.xml"
func $description $sbml

# heat_shock_response
echo python main.py -d '../input/heat_shock_response/heat_shock_response-1.txt ../input/heat_shock_response/heat_shock_response-2.txt' -s Results/heat_shock_response/heat_shock_response_SBML_model.xml

python main.py -d '../input/heat_shock_response/heat_shock_response-1.txt ../input/heat_shock_response/heat_shock_response-2.txt' -s Results/heat_shock_response/heat_shock_response_SBML_model.xml

echo
