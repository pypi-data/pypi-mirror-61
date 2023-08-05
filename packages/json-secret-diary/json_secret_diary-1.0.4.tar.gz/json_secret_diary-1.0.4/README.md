# Secret Diary
My own project to manage my daily diary.

# How it works
The entire diary is based only on JSON text, everything is done with JSON.
Diary has 'public' infos and 'secret' infos, the secret part is encrypted with AES algorithm.

The public part is called 'summary', this will be usefull to help you to know what that page of diary talk about or specific infos.

No connection to internet required, new diary will be created if username is not recognized (obviously with a prompt to allow or deny).

Once you wrote you can't edit text (both public and private) but you can write without limits.

Password of your diary is stored in the same JSON file, the name is yout username setted at first start.

# Example of usage

All you need is to install the package from pip.

Import package and call the Diary class with username and Password, after that call the access() method and that's all!

