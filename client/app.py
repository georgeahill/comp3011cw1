import re
from getpass import getpass
import urllib
import functools
import requests
from tabulate import tabulate
import textwrap

url = None


def assert_url(func):
    @functools.wraps(func)
    def ensure(*args, **kwargs):
        if not url:
            print("No URL set! Log in first")
            return
        return func(*args, **kwargs)

    return ensure


def help(is_mistake = False):
    headers = ["Command Syntax", "Description"]
    help_table = [
        ["help", "Display this help text"],
        ["register", "This is used to allow a user to register to the service using a username, email and a password. When the command is invoked, the program prompts the user to enter the username, email, and password of the new user."],
        ["login <url>", "This command is used to log in to the service. Invoking this command will prompt the user to enter a username and password which are then sent to the service for authentication"],
        ["logout", "This causes the user to logout from the current session"],
        ["list", "This is used to view a list of all module instances and the professor(s) teaching each of them (Option 1)"],
        ["view", "This command is used to view the rating of all professors (Option 2)"],
        ["average <professor_code> <module_code>", "This command is used to view the average rating of a certain professor in a certain module (Option 3)"],
        ["rate <prof_code> <mod_code> <year> <semester> <rating>", "This is used to rate the teaching of a certain professor in a certain module instance (Option 4). Year is a 4 digit year, semester is either 1 or 2, rating is an integer between 1 and 5 inclusive"],
    ]

    # 59 for a line limit of 120 chars
    help_table = [[a, '\n'.join(textwrap.wrap(b, width=59))] for a, b in help_table]

    if is_mistake:
        print("\nLooks like you may have entered an invalid command!\nUsage:\n")
    print(tabulate(help_table, headers=headers, tablefmt='grid'))


def get_creds_from_user():
    username = input("\tUsername:\n\t> ")
    password = getpass("\tPassword:\n\t> ")
    return username, password


def converturl(url):
    if url.startswith("http://www."):
        return "http://" + url[len("http://www.") :]
    if url.startswith("www."):
        return "http://" + url[len("www.") :]
    if not url.startswith("http://"):
        return "http://" + url
    return url


def register(sess):
    global url
    url = input("\tURL\n\t> ")
    url = converturl(url)
    username, password = get_creds_from_user()
    email = input("\tEmail\n\t> ")

    try:
        resp = sess.post(
            urllib.parse.urljoin(url, "/account/register/"),
            data={"username": username, "password": password, "email": email},
        )
        if resp.status_code == 200:
            print("Successfully registered")
        else:
            print("Unable to register")
    except requests.exceptions.ConnectionError:
        print("Unable to connect! Please try a different command")
        return


def login(sess, _url):
    global url
    url = converturl(_url)
    username, password = get_creds_from_user()
    try:
        resp = sess.post(
            urllib.parse.urljoin(url, "/account/login/"),
            data={"username": username, "password": password},
        )
        if resp.status_code == 200:
            print("Successfully logged in")
        else:
            print("Unable to log in", resp.status_code)
    except Exception as e:
        print("Unable to login!")


@assert_url
def logout(sess):
    global url
    try:
        sess.get(urllib.parse.urljoin(url, "/account/logout/"))
    except:
        print("Error logging out!")
    url = None
    print("Successfully logged out")


@assert_url
def list(sess):
    resp = sess.get(urllib.parse.urljoin(url, "/api/modules/"))
    if resp.status_code == 200:
        print(
            tabulate(
                [[a, b, c, d, "\n".join(e)] for a, b, c, d, e in resp.json()],
                headers=[
                    "Module Code",
                    "Module Title",
                    "Year",
                    "Semester",
                    "Professor(s)",
                ],
            )
        )
    else:
        print("Something went wrong. Please try again", resp.status_code)


@assert_url
def view(sess):
    resp = sess.get(urllib.parse.urljoin(url, "/api/rating/"))
    if resp.status_code == 200:
        print("\n".join(resp.json()))
    else:
        print("Something went wrong. Please try again", resp.status_code)


@assert_url
def average(sess, professor_id, module_code):
    resp = sess.get(
        urllib.parse.urljoin(url, f"/api/rating/{professor_id}/module/{module_code}/")
    )
    if resp.status_code == 200:
        print(resp.json())
    else:
        print("Something went wrong. Please try again", resp.status_code)


@assert_url
def rate(sess, professor_id, module_code, year, semester, rating):
    resp = sess.post(
        urllib.parse.urljoin(url, f"/api/rating/{professor_id}/module/{module_code}/"),
        data={"year": year, "semester": semester, "rating": rating},
    )
    if resp.status_code == 200:
        print("Successfully rated")
    else:
        print("Something went wrong. Please try again", resp.status_code)


valid_choices = {
    "help": help,
    "register": register,
    "login ([a-zA-Z0-9\.\-\:]+)": login,
    "logout": logout,
    "list": list,
    "view": view,
    "average ([a-zA-Z0-9]+) ([a-zA-Z0-9]+)": average,
    "rate ([a-zA-Z0-9]+) ([a-zA-Z0-9]+) (\d{4}) ([12]) ([12345])": rate,
}


def main_loop():
    choice = input("> ")
    with requests.Session() as sess:
        while choice not in ("q", "quit", "exit", "-1"):
            processed_command = False
            for pattern, cmd in valid_choices.items():
                if m := re.match(pattern, choice):
                    cmd(sess, *m.groups())
                    processed_command = True
                    break
            if not processed_command:
                help(True)

            choice = input("> ")


if __name__ == "__main__":
    main_loop()
