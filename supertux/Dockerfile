# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV USER=root

# Update and install necessary packages
RUN apt-get update && apt-get install -y \
    xfce4 \
    xfce4-goodies \
    tightvncserver \
    wget \
    xterm \
    curl \
    dbus-x11 \
    x11-xserver-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up the VNC server
RUN mkdir -p ~/.vnc \
    && echo "root" | vncpasswd -f > ~/.vnc/passwd \
    && chmod 600 ~/.vnc/passwd

# Configure VNC server to use Xfce desktop
RUN echo "#!/bin/sh\n\
xrdb $HOME/.Xresources\n\
startxfce4 &" > ~/.vnc/xstartup \
    && chmod +x ~/.vnc/xstartup

# Expose the VNC port
EXPOSE 5901

# Cleanup old lock files and start the VNC server
CMD ["/bin/sh", "-c", "rm -rf /tmp/.X* && vncserver :1 -geometry 1280x800 -depth 24 && tail -f /root/.vnc/*.log"]
