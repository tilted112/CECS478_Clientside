# CECS478 Client Application E2E encrypted chat
Client application for an E2E encrypted chat. As part of the class CECS478 by Team us, Jaime Park and Till Behrendt
## Getting Started
This is an introduction how to run the client application.
### Installation
Clone this repository to your computer and execute the client.py file with a python compiler of your choice. (Recommend by us is [Spyder IDE](https://www.spyder-ide.org/))
### Generate your public-private key pair

### Signup
To signup you just have to think of a username for yourself. Your chatpartner has to know your username in order to chat with you. You also assign a password to your user. If you done so and you got a confirmation that your singup was successful, you are ready to chat.
### Signin
To signin remeber your username and password and hit signin. Now you can type in the username of your chatpartner. Also make sure to type in the correct name of your private key and the name of the public key of your chatpartner.
**Important**
The files containing the public and private keys have to be in the same folder as the application files client.py and so on. Example: If your private key is named 'private_key.pem' you type in the entry field 'private_key.pem'.
### Chat
Now that you have typed in all necessary information you can start the chat by simply hitting the button 'Start chat'.
A new window will pop open with a entry field at the very bottom. That is where you type in the messages. To send a message hit the <Return> key on the keyboard. 
If you want to end the chat just hit the 'End Chat' button.