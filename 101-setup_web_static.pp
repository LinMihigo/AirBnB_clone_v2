# web_static.pp
exec { 'apt-update':
  command => '/usr/bin/apt-get -y update',
  before  => Package['nginx'],
}

package { 'nginx':
  ensure => installed,
}

file { ['/data', '/data/web_static', '/data/web_static/releases']:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { ['/data/web_static/releases/test', '/data/web_static/shared']:
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases'],  # Explicit dependency
}

file { '/data/web_static/releases/test/index.html':
  content => "<html>\n\t<head>\n\t</head>\n\t<body>\nALX\n\t</body>\n</html>\n",
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
}

file { '/etc/nginx/sites-available/default':
  content => @("END"/L),
    server {
      listen 80 default_server;
      listen [::]:80 default_server;
      add_header X-Served-By ${::hostname};
      root /var/www/html;
      index index.html index.htm;
      error_page 404 /404.html;
      location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html index.htm;
      }
      location = /404.html { internal; }
    }
    |-END
  notify => Service['nginx'],
}

service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
