#!/bin/bash
# validates packages installed
username=$SUDO_USER
if [ "$EUID" -ne 0 ]
then 
    echo '--+ THIS MUST BE EXECUTED WITH SUDO +--'
    echo '--+ You can also install sqlite3    +--'
    echo '--+ and conda by yourself on this   +--'
    echo '--+ system                          +--'
    exit 1
fi

if [ command -v conda --version &> /dev/null ];
then   
    wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh -O conda.sh
    bash conda.sh -b -p /home/$username/anaconda3
    rm -f conda.sh
    /home/$username/anaconda3/bin/conda init bash
    source /home/$username/.bashrc
    echo 'conda lastest version ... [OK]'
fi

if [ $(dpkg-query -W -f='${Status}' sqlite3 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
    apt-get install sqlite3;
    echo 'sqlite3 installed ... [OK]'
else 
    echo 'sqlite3 installed ... [OK]'
fi


/home/$username/anaconda3/bin/conda init bash
export PATH="/home/$username/anaconda3/bin:$PATH"
source /home/$username/.bashrc

if ! conda info --envs | grep -q bcg_project; then
    conda env create -f ./python/environment.yaml
fi
source activate base
conda init
conda activate bcg_project
cd ./python
python3 script.py
conda deactivate 

exit 0

    

