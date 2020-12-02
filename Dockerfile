FROM ubuntu:20.04

MAINTAINER CapXuanCuong <capxuancuong@gmail.com>


ENV NAGIOSADMIN_PASS  nagios



RUN apt update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt install -y autoconf bc gawk dc build-essential gcc libc6 make wget unzip apache2 php libapache2-mod-php libgd-dev libmcrypt-dev make libssl-dev snmp libnet-snmp-perl gettext
RUN apt-get -y install supervisor && \
    mkdir -p /var/log/supervisor && \
    mkdir -p /etc/supervisor/conf.d
RUN wget https://github.com/NagiosEnterprises/nagioscore/archive/nagios-4.4.6.tar.gz
RUN tar xvf nagios-4.4.6.tar.gz
RUN ls -l
WORKDIR nagioscore-nagios-4.4.6
RUN ./configure --with-httpd-conf=/etc/apache2/sites-enabled 
RUN make all
RUN make install-groups-users
RUN usermod -a -G nagios www-data
RUN make install
RUN make install-daemoninit
RUN make install-commandmode
RUN make install-config
RUN make install-webconf
RUN a2enmod rewrite cgi
RUN htpasswd -b -c /usr/local/nagios/etc/htpasswd.users nagiosadmin ${NAGIOSADMIN_PASS}
RUN apt install -y  monitoring-plugins nagios-nrpe-plugin
RUN mkdir -p /usr/local/nagios/etc/monitors
RUN sed -i 's|\$USER1\$=/usr/local/nagios/libexec|\$USER1\$=/usr/lib/nagios/plugins|' /usr/local/nagios/etc/resource.cfg
RUN sed -i 's|#\s*cfg_dir=/usr/local/nagios/etc/routers|cfg_dir=/usr/local/nagios/etc/monitors|' /usr/local/nagios/etc/nagios.cfg 

COPY  ./supervisor.conf /etc/supervisor.conf
COPY ./supervisor-apache2.conf /etc/supervisor/conf.d/apache2.conf
#COPY ./supervisor-nagios.conf /etc/supervisor/conf.d/nagios.conf

EXPOSE 80

RUN supervisord -c /etc/supervisor.conf
