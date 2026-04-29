
#!/bin/bash
set -e

# Update system
dnf update -y

# Install packages
dnf install -y httpd php php-mysqlnd php-gd php-intl \
php-xml php-soap php-zip php-opcache git amazon-efs-utils

# Enable and start Apache
systemctl enable --now httpd

# Create and mount EFS
mkdir -p /var/moodledata

mount -t efs -o tls fs-0eaa78f89260719d1:/ /var/moodledata
echo "fs-0eaa78f89260719d1:/ /var/moodledata efs _netdev,tls 0 0" >> /etc/fstab

chown -R apache:apache /var/moodledata
chmod 770 /var/moodledata

# Install Moodle
cd /var/www
git clone https://github.com/moodle/moodle.git
cd moodle
git checkout MOODLE_502_STABLE
chown -R apache:apache /var/www/moodle

# Apache VirtualHost config
cat > /etc/httpd/conf.d/moodle.conf <<'EOF'
<VirtualHost *:80>
    DocumentRoot /var/www/moodle
    <Directory /var/www/moodle>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
EOF

# Restart Apache
systemctl restart httpd
