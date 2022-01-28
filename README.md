# README

## Disclaimer:
This is a project that I work on as a hobby.

PLEASE OBEY the rule by Fudan and **MAUNALLY summit PAFD everyday**. 

Thank you.

---

## Features:

* Automatically summit PAFD everyday at 01:00 UTC, that is 9 a.m. GMT+8. _There might be delays due to github server._

* send wechat messages to notify the success of PAFD summit (pushkey needed)

* along with remaining dorm electricity within the message

* numerous BUGS that are beyond my ability to fix

    * `Network is unreachable` in action, causing complete failure
    * UIS might not be connected, causing complete failure _(to be fixed)_
    * dorm electricity API by Fudan might be down _(fixed)_
    * and so on......

---

## How to use:
To begin with, create a github account and fork this repository.

It is better to create a pushkey to send wechat messages.

Please go to https://sct.ftqq.com/ and create a pushkey according to the website's instructions.



Then, open the repository that you fork and go to `settings` > `secrets` > `new repository secret`, and type in `your student ID`, `password` and `pushkey` (if available) as follows:

```
NAME: STD_ID
VALUE: {your student ID}

NAME: PASSWORD
VALUE: {your password}

NAME: PUSHKEY_SCT
VALUE: {your pushkey}
```

Finally, go to `Actions` and enable `auto` workflow

And it will do its job everyday.
