# malware-project
## ML Code
### Text CLassifier
1. Run "fullTextClassifierML" file to get words.json and cleaned dataset file.
2. Run "finalTextClassifierModel" file to get two pickles file for backend.
3. Copy Pickle files along with words.json to backend application path "Server/backend/models".
### URL Classifier
1. Run "URLFeatureExtraction" file to get url features file "urldata.csv" but it takes lot of time.
2. Run "URLModel" file to get pickle for backend.
3. Copy Pickle file to backend application path "Server/backend/models".
## Frontend Code
1. Install create-expo-app using "npm install -g create-expo-app"
2. Run "npm install"
3. Go to frontend application run "npx expo start"\
## Backend Code
1. Open a terminal on a linux machine and run the following commands to install MiniConda:
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
```
2. Close and re-open the terminal, then run the following command to create a conda environment:
```
echo y | conda create -n se-env python=3.9.12
```
3. Activate the environment by running this command:
```
conda activate se-env
```
4. Create a .env file in the malware-project\smishguard-backend\ folder and configure the following variables:
```
EXTERNAL_IP="localhost" #Enter the VM's External IP Address (Can be found on AWS instance info)
INTERNAL_IP="localhost" #Enter the VM's Internal IP Address (Can be found on AWS instance info)
```
5. The server can be started by running the following command in malware-project\smishguard-backend\Server\:
```
sh start_server.sh
```
