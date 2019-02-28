# Documenmtation for registration API

## Introduction

This documentation explains how to register a user. The API is based on HTTP.

## Request

The request should be sent to [https://devpsu.whmhammer.com/cgi/register.py](https://devpsu.whmhammer.com/cgi/register.py) using **POST** method with the following parameters:

### `username` (REQUIRED)

The username of the account to be create. The username should contain only alphabetical and digital characters. the length of the username should be no longer than 64 characters. Every account has a unique, changable username.

### `salt` (REQUIRED)

The "salt" to be used to hash the password. During regiustration, a 32-digit string containing only alphabetical and digital characters should be randomly generated by the front end as the "salt".

### `password_hash` (REQUIRED)

The 128-digit **hexadecimal digestion** of the **sha512** hash of the concatenation of the "salt" and the raw password.

### `email` (REQUIRED)

The email address of the user. The maximal acceptable length is 64 characters.

### `family_name` (OPTIONAL)

The last name of a person in US, positioning may vary in different cultures. The maximum acceptable leangth is 32 characters.

### `given_name` (OPTIONAL)

The first name of a person in US, positioning may vary in different cultures. The maximum acceptable length is 32 characters.

## Response

The response is always in `application/json`.

- `status` indicates the status of the registration. Here is a list of all possible values (case sensitive):

    - `success`

    - `use POST method`

    - `missing parameter`

    - `illegal username`

    - `use 32-digit alnum salt`

    - `use sha512`

    - `illegal email address`

    - `true name too long`

    - `email address already been registered`

    - `username already been registered`

    - `unexpected error`

The user information is written to the database only when `status` is `success`. The user will receive an email containing a verification URL. By visiting the URL, the user verifies his or her registration. It is only after verification that a user can access his or her account.

## Sample front-end implementation

### Python3

<pre><code>
import requests as rq
from hashlib import sha512
from random import choice
from string import ascii_letters,digits

rand32=lambda :"".join([choice(ascii_letters+digits) for i in range(32)])

username="username"
password="password"
email="johndoe@e.mail"
family_name="Doe"
given_name="John"

salt=rand32()
s=bytes(salt+password,"ascii")
h=sha512(s)

data={
    "username":username,
    "salt":salt,
    "hash":h.hexdigest(),
    "email":email,
    "family_name":family_name,
    "given_name":given_name
}

r=rq.post("https://devpsu.whmhammer.com/cgi/register.py",data)

print(r.json())
</code></pre>