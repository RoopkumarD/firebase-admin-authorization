This python script allows admins to add custom claim to a user account and also add user email to
roles collection for firestore authorization

Install below module to run this script
```
pip install click
pip install firebase_admin
```

Then generate service account keys by going to
```
project settings > service account tab > create new private key button
```
save the json file as credential.json in this directory

**Note**: After using the script, please delete the credential.json file for security purposes.
For later use you can re-generate keys by following same above step

Now run the script
```
python3 auth.py --help
```
For usage and listing all the subcommand available
