<!-- This file is written in Markdown! Use a viewer (or view on [github](https://github.com/georgeahill/comp3011cw1/blob/main/client/readme.md))-->


# 1. Hosting information 

The domain name is `sc18gah.pythonanywhere.com` \
The admin page is at `sc18gah.pythonanywhere.com/admin/` \
The admin username is `ammar` and the password is `ammar` \
The 2 students I set up are called `student1` and `student2` with matching passwords `student1` and `student2`

If you type anything wrong you will be shown the help grid above. Ensure your client is at least 120 characters wide for correct format!!

# 2. Using the Client

Run the client code (`python app.py`), then either type `help` at the prompt or read the below:

<!-- This is in a comment to ensure markdown still works nicely, but is easier on the eyes in .txt mode
+--------------------------------------------------------+-------------------------------------------------------------+
| Command Syntax                                         | Description                                                 |
+========================================================+=============================================================+
| help                                                   | Display this help text                                      |
+--------------------------------------------------------+-------------------------------------------------------------+
| register                                               | This is used to allow a user to register to the service     |
|                                                        | using a username, email and a password. When the command is |
|                                                        | invoked, the program prompts the user to enter the          |
|                                                        | username, email, and password of the new user.              |
+--------------------------------------------------------+-------------------------------------------------------------+
| login <url>                                            | This command is used to log in to the service. Invoking     |
|                                                        | this command will prompt the user to enter a username and   |
|                                                        | password which are then sent to the service for             |
|                                                        | authentication                                              |
+--------------------------------------------------------+-------------------------------------------------------------+
| logout                                                 | This causes the user to logout from the current session     |
+--------------------------------------------------------+-------------------------------------------------------------+
| list                                                   | This is used to view a list of all module instances and the |
|                                                        | professor(s) teaching each of them (Option 1)               |
+--------------------------------------------------------+-------------------------------------------------------------+
| view                                                   | This command is used to view the rating of all professors   |
|                                                        | (Option 2)                                                  |
+--------------------------------------------------------+-------------------------------------------------------------+
| average <professor_code> <module_code>                 | This command is used to view the average rating of a        |
|                                                        | certain professor in a certain module (Option 3)            |
+--------------------------------------------------------+-------------------------------------------------------------+
| rate <prof_code> <mod_code> <year> <semester> <rating> | This is used to rate the teaching of a certain professor in |
|                                                        | a certain module instance (Option 4). Year is a 4 digit     |
|                                                        | year, semester is either 1 or 2, rating is an integer       |
|                                                        | between 1 and 5 inclusive                                   |
+--------------------------------------------------------+-------------------------------------------------------------+ -->
<!-- This below is the markdown version! If reading as a txt, feel free to skip to the next section -->

| Command Syntax                                         | Description                                                                                                                                                                                                                           |
|--------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| help                                                   | Display this help text                                                                                                                                                                                                               |
| register                                               | This is used to allow a user to register to the service<br />using a username, email and a password. When the command is<br />invoked, the program prompts the user to enter the<br />username, email, and password of the new user. |
| login *url*                                            | This command is used to log in to the service. Invoking<br />this command will prompt the user to enter a username and<br />password which are then sent to the service for<br />authentication                                      |
| logout                                                 | This causes the user to logout from the current session                                                                                                                                                                              |
| list                                                   | This is used to view a list of all module instances and the<br />professor(s) teaching each of them (Option 1)                                                                                                                       |
| view                                                   | This command is used to view the rating of all professors<br />(Option 2)                                                                                                                                                            |
| average *professor_code* *module_code*                 | This command is used to view the average rating of a<br />certain professor in a certain module (Option 3)                                                                                                                           |
| rate *prof_code* *mod_code* *year* *semester* *rating* | This is used to rate the teaching of a certain professor in<br />a certain module instance (Option 4). Year is a 4 digit<br />year, semester is either 1 or 2, rating is an integer<br />between 1 and 5 inclusive                   |

