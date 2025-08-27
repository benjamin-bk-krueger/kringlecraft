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

## Server mode

The application can also be made available on the internet. This means that it also has the full range of functions (multi-user, shared links, mails, etc.)

### 1. Create user

On a server, processes should not run under root, so we create a separate user for the application.

``` bash
# as root
useradd -g kringle -m -u 3000 kringle
groupadd -g 3000 kringle
```

### 2. Clone GIT repository

``` bash
# as root
su - kringle
# as user kringle
git clone https://github.com/benjamin-bk-krueger/kringlecraft
```

### 3. Create services

A suitable service config must be created so that the application starts up every time.

``` bash
# as root
# the paths in the service file need to be changed if you want to use a different user/path
cp kringlecraft/srv/uwsgi-kringlecraft.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable uwsgi-kringlecraft
```

### 4. Modify Apache config

The application requires a web server that acts as a proxy.  
The file kringlecraft/srv/apache.conf shows how the configuration can look. Paths, domain names and SSL certificates must be adapted to your own setup.  

### 5. Configure the application

The following configuration parameters must be customized:  

``` bash
cat kringlecraft/cfg/kringle.json
{
  "version": 1,
  "app": {
    "mode": "server",
    "release": "1.2.0",
    "date": "2024-07-10",
    "mail_enable": "true",
    "mail_sender": "mail@craft.kringle.info",
    "mail_admin": "admin-mailbox@craft.kringle.info",
    "mail_server": "localhost",
    "www_server": "https://craft.kringle.info"
  },
  "secret": {
    "key": "secret-key-goes-here"
  }
}
```

- mail_enable: Set to true or false if a mail server is to be used.
- mail_sender: Enter sender address - customize to your own domain
- mail_admin: Enter recipient's address - this is where e-mails, e.g. from the contact form, are sent
- mail_server: IP or hostname of mail server
- www_server: Customize to your own domain (necessary to build valid links)
- key: Choose your own private and secret key (used for CSRF protection for example)

### 6. Install package dependencies

The application requires a few libraries that can be easily installed using pip (in the venv).

``` bash
# as user kringle
kringle@www:~$ cd kringlecraft/
kringle@www:~/kringlecraft$

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 7. Create admin user

A first user can be created as follows:

``` cmd
# as user kringle
python3 bin/basic_inserts.py

(see local installation)
```

### 8. Start the application

The application should now be ready. First, the application must be started and, if necessary (the first time), the modified Apache config loaded

``` bash
# as root
systemctl reload apache2
systemctl start  uwsgi-kringlecraft
```

### 9. Troubleshooting

If something is not working, it is worth analyzing the Apache logs or the wsgi logs

``` bash
tail /var/log/apache2/kringle_error.log
systemctl -f status  uwsgi-kringlecraft
```

### 10. Backup 

All data is either stored in the SQLite database or as static files in the file system. These should be backed up and can also be copied to another location.

``` bash
kringle@www:~/kringlecraft$ ls -l kringlecraft/db/ kringlecraft/static/uploads/
```
