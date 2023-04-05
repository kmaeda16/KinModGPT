## Contents

- **1. text-davinci-003_only** contains Pytnon scripts for the GPT-only approach with text-davinci-003.
- **2. gpt-3.5-turbo_only** contains Pytnon scripts for the GPT-only approach with gpt-3.5-turbo.
- **3. gpt-4_only** contains Pytnon scripts for the GPT-only approach with gpt-4.
- **4. KinModGPT_text-davinci-003** contains Python scripts for KinModGPT with text-davinci-003.
- **5. KinModGPT_gpt-3.5-turbo** contains Python scripts for KinModGPT with gpt-3.5-turbo.
- **6. KinModGPT_gpt-4** contains Python scripts for KinModGPT with gpt-4.
- **7. INDRA** contains Python scripts for INDRA.
- **input** contains model descriptions.
- **README.md** is what you are reading now.

## How to run the scripts for 1 - 6

1. Log in to the [Open AI](https://openai.com/api/login/) website and create an API key.
2. Use pip in Conda environment:
    1. conda create -n kinmodgpt python=3.7
    2. conda activate kinmodgpt
    3. pip install openai tellurium jinja2==3.0.0
3. Modify main.py to set your OpenAI API key.
4. Run RunMe.sh in each directory.

## How to run the script in 7
1. Use pip and conda in Conda environment:
    1. conda create -n indra python=3.8
    2. conda activate indra
    3. pip install git+https://github.com/sorgerlab/indra.git
    4. pip install python-libsbml
    5. conda install -c alubbock bionetgen
2. Run RunMe.sh.

===============  
Kazuhiro Maeda,  
Kyushu Institute of Technology
