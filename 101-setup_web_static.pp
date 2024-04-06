# Sets up your web servers for the deployment of web_static.


$nginx_conf = "server {
    listen 80 default_server;
    listen [::]:80 default_server;

    add_header X-Served-By ${hostname};

    root /var/www/html;

    # Add index.php to the list if you are using PHP
    index index.html index.htm index.nginx-debian.html;

    server_name _;
    # newpath
    location /hbnb_static {
        alias /data/web_static/current/;
    }
    location / {
        # First attempt to serve request as file, then
        # as directory, then fall back to displaying a 404.
        try_files $uri $uri/ =404;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

    error_page 404 /custom_404.html;
    location = /custom_404.html {
        root /var/www/html/;
        internal;
    }
}"

file {'/data/web_static/releases/test/index.html':
    ensure  => 'file',
    content => 'hello world',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    require => File['/data/web_static/releases/test'],
}

# Create all the folders in the path /data/web_static/releases/test/ if they don’t exist
file {'/data/web_static/releases/test':
    ensure  => 'directory',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    require => File['/data/web_static/releases'],
}

# Create all the folders in the path /data/web_static/shared/ if they don’t exist
file {'/data/web_static':
    ensure  => 'directory',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    require => File['/data'],
}

# Create all the folders in the path /data/web_static/releases/ if they don’t exist
file {'/data/web_static/releases':
    ensure  => 'directory',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    require => File['/data/web_static'],
}

# Create all the folders in the path /data/web_static/shared/ if they don’t exist
file {'/data/web_static/shared':
    ensure  => 'directory',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    require => File['/data/web_static'],
}

# Create all the folders in the path /data/web_static/current/ if they don’t exist
file {'/data/web_static/current':
    ensure  => 'link',
    owner   => 'ubuntu',
    group   => 'ubuntu',
    target  => '/data/web_static/releases/test',
    require => File['/data/web_static'],
}

# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder
file {'/data':
    ensure => 'directory',
    owner  => 'ubuntu',
    group  => 'ubuntu',
}

file {'/etc/nginx/sites-available/default':
    ensure  => 'file',
    content => $nginx_conf,
    require => Package['nginx'],
    notify  => Service['nginx'],
    replace => true,
}

#install nginx web server
package { 'nginx':
    ensure => 'installed',
}

#start nginx web server
service { 'nginx':
    ensure => 'running',
    enable => true,
}
