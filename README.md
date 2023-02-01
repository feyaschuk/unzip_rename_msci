# unzip_rename_msci

### Description:

The script decompresses a file that is received in a "raw" folder in Azure Blob Storage and has a specific prefix.
Extracts the files, renames them, if the feed name is too short(0 symbol) or too long(more then 50 symbols). Saves exracted files in specified container/dropdir/msci/esg. 


### How to use: 
* Clone the repository and go to it on the command line:

```bash
git clone https://github.com/feyaschuk/unzip_rename_msci.git
```
```bash
cd unzip_rename_msci
```

* Create and activate virtual environment:
```bash
python3 -m venv env
```
```bash
source env/bin/activate (MAC OC, Linux) // source venv/Scripts/activate (Windows)
```
```bash
python3 -m pip install --upgrade pip
```

* Install dependencies from requirements.txt file:
```bash
pip install -r requirements.txt
```

* Add your SecretCredentials in row in file "unzip_if_multiple.py"
```bash
token_credential = ClientSecretCredential("{tenant-id}", "{client-id}", "{client-secret}"
```

* Run the program:
```bash
python unzip_rename_msci.py

#### Example of usage:
```bash
python unzip_rename_msci.py
```
