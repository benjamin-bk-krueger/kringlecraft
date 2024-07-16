# Modes of operation

There are two ways to run the application. On the one hand, it can be used locally on any client computer on which Python is installed. On the other hand, it can also be made available on the internet.

## Client mode

The easiest way to use it is on a local client. The only requirement is a current Python installation. The following steps must be carried out:

### 1. Clone GIT repository
``` cmd
C:\Temp>git clone https://github.com/benjamin-bk-krueger/kringlecraft
Cloning into 'kringlecraft'...
...
Resolving deltas: 100% (1041/1041), done.

C:\Temp>
```

Alternatively, a ZIP file can be downloaded directly: [KringleCraft ZIP](https://github.com/benjamin-bk-krueger/kringlecraft/archive/refs/heads/main.zip)

### 2. Install package dependencies

The application requires a few libraries that can be easily installed using pip (in the venv).

``` cmd
C:\Temp>cd kringlecraft

C:\Temp\kringlecraft>"c:\Program Files\Python312\python.exe" -m venv venv

C:\Temp\kringlecraft>.\venv\Scripts\activate

(venv) C:\Temp\kringlecraft>pip install -r requirements.txt
...
[notice] A new release of pip is available: 23.2.1 -> 24.1.2
[notice] To update, run: python.exe -m pip install --upgrade pip

(venv) C:\Temp\kringlecraft>
```

### 3. Create admin user

A first user can be created as follows:

``` cmd
(venv) C:\Temp\kringlecraft>cd kringlecraft\bin

(venv) C:\Temp\kringlecraft\kringlecraft\bin>python basic_inserts.py
INFO: Connecting to DB with sqlite:///C:\Temp\kringlecraft\kringlecraft\db\kringlecraft.sqlite
Name: Han Solo
Email: han@solo.de
Password: testtest

(venv) C:\Temp\kringlecraft\kringlecraft\bin>
```

### 4. Start the application

This is easily done via the main script:

``` cmd
(venv) C:\Temp\kringlecraft>cd kringlecraft

(venv) C:\Temp\kringlecraft\kringlecraft>python app.py
CONFIG key: mode, value: standalone
CONFIG key: release, value: 1.2.0
CONFIG key: date, value: 2024-07-10
CONFIG key: mail_enable, value: false
CONFIG key: mail_sender, value: mail@localhost
CONFIG key: mail_admin, value: admin@localhost
CONFIG key: mail_server, value: localhost
CONFIG key: www_server, value: http://127.0.0.1:5006
SECRET key: key, value: ********
INFO: Connecting to DB with sqlite:///C:\Temp\kringlecraft\kringlecraft\db\kringlecraft.sqlite
 * Serving Flask app 'app'
 * Debug mode: off
```

It can be terminated simply by pressing CTRL-C.  

Now you can navigate to http://127.0.0.1:5006 to get things started.

