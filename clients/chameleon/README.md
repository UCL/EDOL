generate chameleon pb2 schema python file with:

```bash
cd chameleon
protoc --python_out=generated/ --pyi_out=generated/  chameleon.proto
```

Thereafter, in order to get the access keys to the chameleon AWS services,

1. [Go to the login portal](https://ucl-cloud.awsapps.com/start/#/?tab=accounts).
2. Click on `serl-test` account.
3. Click on `Access keys` button. This should open a pop-up window with the access keys.
4. Copy the terminal commands under Option 1 and paste them in the terminal. This will set the access keys in the terminal session.

To run the chameleon data client, run the following command:

```bash
python data_client.py
```
