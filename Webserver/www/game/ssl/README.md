# XAMPP Domain and SSL Setup
Setup instructions and files for local secure domains using XAMPP.

## Add domain to Windows hosts file
Add domain to hosts file located at `C:\Windows\System32\drivers\etc\hosts`.

```
127.0.0.1 	localhost # Enabled by default
127.0.0.1 	subdomain.localhost
127.0.0.1 	customdomain
```

## Generate SSL Certificate
Move the .conf and .bat file to `XAMPP/apache/crt` folder.

Modify the .conf file, replacing `commonName_default` and `DNS.1` with your domain name.

Add any subdomains as necessary with additional `DNS.#` entries.

Run the batch file.

## Install SSL Certificate
Open the generated .crt file and click Install Certificate... > Local Machine > Place all certificates in the following store > Trusted Root Certification Authorities.

## Add domain to XAMPP vhosts
Add domain to the vhosts file located at `XAMPP/apache/conf/extra/httpd-vhosts.conf`

```
# HTTP
<VirtualHost *:80>
DocumentRoot "[insert document root here]"
ServerName localhost
ServerAlias localhost
</VirtualHost>
<VirtualHost *:443>

# HTTPS
DocumentRoot "[insert document root here]"
ServerName localhost
ServerAlias localhost
SSLEngine on
SSLCertificateFile "crt/localhost/server.crt"
SSLCertificateKeyFile "crt/localhost/server.key"
</VirtualHost>

# HTTP
<VirtualHost *:80>
DocumentRoot "[insert document root here]"
ServerName subdomain.localhost
ServerAlias subdomain.localhost
</VirtualHost>

# HTTPS
<VirtualHost *:443>
DocumentRoot "[insert document root here]"
ServerName subdomain.localhost
ServerAlias subdomain.localhost
SSLEngine on
SSLCertificateFile "crt/localhost/server.crt"
SSLCertificateKeyFile "crt/localhost/server.key"
</VirtualHost>

<Directory "[insert document root here]">
    Options Indexes FollowSymLinks Includes ExecCGI
    AllowOverride All
    Require all granted
</Directory>
```