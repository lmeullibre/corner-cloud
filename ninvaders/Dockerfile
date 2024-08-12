# Use an official Ubuntu base image
FROM ubuntu:20.04

# Set the environment variable to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && apt-get install -y \
    ninvaders \
    openssh-server \
    xinetd \
    supervisor

# Set up the SSH server
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config

# Create the restricted shell script
RUN echo '#!/bin/bash' > /usr/local/bin/restricted_shell.sh
RUN echo '/usr/games/ninvaders' >> /usr/local/bin/restricted_shell.sh
RUN echo 'logout' >> /usr/local/bin/restricted_shell.sh
RUN chmod +x /usr/local/bin/restricted_shell.sh

# Set the restricted shell as the login shell for root
RUN chsh -s /usr/local/bin/restricted_shell.sh root

# Configure supervisord
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose the SSH port
EXPOSE 22

# Start the services
CMD ["/usr/bin/supervisord"]