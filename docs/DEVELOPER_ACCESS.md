# Developer access

How to switch on **developer mode**, which opens every section of ThaiBridge in
your browser, whatever your level or plan, so you can check any page.

The page is deliberately **not linked from the menu**: visitors kept seeing
"Developer Login" in the Account menu. It still works at its address.

## Links

| Where | Address |
|---|---|
| Live site | **https://thaibridge.smoald.com/developer-login** |
| On your PC (`flask run`) | http://127.0.0.1:5000/developer-login |

Tip: bookmark the live link in your browser.

## How to use it

1. Open the link above.
2. Enter the developer password.
3. You're taken back into the site with every section open. The developer switch
   lives in **this browser's session** only, so it doesn't change your account,
   and other browsers or devices aren't affected.

## Where the password lives

The password is **never** in this repository (it is public).

- **Live site:** Render dashboard → service **thaibridge-ai** → **Environment** →
  `DEVELOPER_PASSWORD`. After changing it, redeploy so the new value is used.
- **On your PC:** `DEVELOPER_PASSWORD=...` in your local `.env` file (see
  `.env.example`).

If `DEVELOPER_PASSWORD` isn't set at all, the page simply sends you to the home
page and developer mode can't be switched on. That is on purpose: there is no
fallback password (`tests/test_developer_mode.py` checks this).

## Good to know

- **Wrong passwords are rate-limited:** 5 tries per 15 minutes, 20 per hour. If
  you get locked out, wait and try again.
- Only wrong attempts count; a correct password always works.
- Nothing on the site links to this page, and a test keeps it that way
  (`test_menu_does_not_advertise_developer_login`).
