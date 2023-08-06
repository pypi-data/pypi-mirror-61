# Local Variable Manager (lvmanager)
# What does it do?
This is a simple CLI script to encrypt, store, and set environmental variables such as certs, ,keys or tokens.
```shell script
usage: CLI for managing and maintaining tokens and key/certs.

optional arguments:
  -h, --help      show this help message and exit
  -add ADD        Adds a file to lcm [--name required]
  -delete DELETE  Delete a saved file [--name required]
  -setenv SETENV  Expose a saved file as an environmental variable [--name
                  required]
  -name NAME      Name to be used
  -ls             Display what currently stored
  -cleanup        Clean up exposed keys
  -e              Use encryption for values when storing or setting the
                  environment [LVMANAGER_PW is needed as an environmental
                  variable]
  -getkey         Get a new encryption key
```
### View stored files 
```shell script
lvmanager -ls
```
### Add
```shell script
lvmanager -add NAME_OF_FILE.key -name project/NAME
```
`lvmanager` will automatically create projects if they are already not created. 
The `-e` flag will encrypt data and will need the environmental variable `LV_MANAGER` to be configured.

Note: If you save a `.lvmanager` file, when you `setenv` the contents of the file will be exposed, not a pointer to the file.
### Delete
```shell script
lvmanager -delete project/NAME
```
### Export single variable
```shell script
lvmanager -setenv project/NAME -name APP_TOKEN -e 
```
`lvmanager` will expose the stored value NAME as APP_TOKEN and will copy the relevant commands to the clipboard to the user to manually set. 
The `-e` flag will encrypt data and will need the environmental variable `LV_MANAGER` to be configured.
### Export projects variables
```shell script
lvmanager -setenv project/ -e
```
`lvmanager` will expose all values under project/ as the NAME they are stored as (in uppercase).
The `-e` flag will encrypt data and will need the environmental variable `LV_MANAGER` to be configured.
### Get key
```shell script
lvmanager -getkey
```
The export command will be copied to the clipboard and will need to be set by the user. Don't lose this key!

## How to Install
You can install `lvmanager` through the setup.py file:
```shell script
python3 setup.py install
```
Pip config coming soon

## Example
0) Get and export key for encryption:
   ```shell script
    lvmanager -getkey
    ```
   And now in your clipboard you should be able to expose your key:
   ```shell script
    export LVMANAGER_PW=12345..
    ```
1) Add the key `test.key` as token under project/ with encryption enabled:
    ```shell script
    lvmanager -add token.lvmanager -name project/token -e
    ```
2) See what `lvmanager` has stored:
    ```shell script
    lvmanager -ls
    ```
   And we can see:
   ```shell script
    (venv) lvmanager -ls                  
    project/
        key.key
    ```
3) Expose our key and get the export command:
    ```shell script
    lvmanager -setenv project/key -name KEY -e
    ```
4) Export our environmental variable:
    ```shell script
    export KEY=some/path/to/.exposed/project/key.key
    ```
5) Delete our key from our database:
    ```shell script
    lvmanager -delete project/key
    ```
6) Clean up any un-encrypted data from the `.exposed` file:
    ```shell script
    lvmanager -cleanup
    ```