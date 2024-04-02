# Corner Cloud

Corner Cloud is a personal project in which I aim to understand the infrastructure, challenges, opportunities and state of the art of the Cloud Gaming industry. There are very few companies dedicated to it, and much of the code is not open source, so many key principles of the industry are a big mystery to me. It is important to keep in mind that cloud resources (GCloud, Aws, Azure ... ) are expensive, so an important goal of this project is to achieve the best possible optimisation, in order to be able to run expensive games on hardware resources while spending as little money as possible.

This monorepo contains the frontend and backend code for the main service, which provides authentication, session management, queueing and resource management for a correct allocation of resources. 

All code related to the infrastructure will be uploaded soon.

## Development diary

1 April 2024

- The first game has been installed. For this I have chosen nInvaders, which uses ncurses so it allows playing via SSH. This comes very handy since SSH is the only protocol available at the moment.
- The functionality of the virtual machine has been restricted as much as possible to the user. The user will not be able to interact with absolutely nothing inside the virtual machine, only play.
- A script has been made so that all newly created users, when starting an SSH connection, are redirected directly to the nInvaders game.
- Modified the .bashrc so that users are automatically disconnected from the session once they have interrupted the game.
- Users are shown a message thanking them for playing, and have the opportunity to return to the dashboard to choose another game (currently only nInvaders is available).

30 May and before

- Minimal infrastructure has been built to allow users to connect to the virtual machine terminal via SSH in the browser. For this, we have taken advantage of the open source project called Apache Guacamole. 
Apache Guacamole is an open-source clientless remote desktop gateway. It allows users to access their computers from anywhere using a web browser, without needing to install client software on the device from which they are accessing their computers. Apache guacamole comes in handy for enabling SSH or VNC connections. Enough for now.

- The virtual machine that users access is predefined, with all values hardcoded.

- I have built a web application using SvelteKit and Django to control the available users, sessions and games. 

- A microservice has been deployed that consumes the guacamole-lite library https://github.com/vadimpronin/guacamole-lite. This library allows us to start a websocket tunnel directly with the guacamole daemon named `guacd`. Basically it acts as the proxy between the web client (the user's browser accessing the Guacamole interface) and the remote desktop servers (such as those running VNC, RDP, or SSH services). 




