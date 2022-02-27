import re
from getpass import getpass
import urllib
import functools
import requests
from tabulate import tabulate

url = None


def assert_url(func):
    @functools.wraps(func)
    def ensure(*args, **kwargs):
        if not url:
            print("No URL set! Log in first")
            return
        return func(*args, **kwargs)

    return ensure


def help():
    print("HELP")


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
            urllib.parse.urljoin(url, "/register/"),
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
            urllib.parse.urljoin(url, "/login/"),
            data={"username": username, "password": password},
        )
        if resp.status_code == 200:
            print("Successfully logged in")
        else:
            print("Unable to log in")
    except Exception as e:
        print("Unable to login!")


@assert_url
def logout(sess):
    global url
    sess.get(urllib.parse.urljoin(url, "/logout/"))
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
                help()

            choice = input("> ")


if __name__ == "__main__":
    main_loop()
