[![Build Status](https://travis-ci.org/mozilla/teach-api.svg)](https://travis-ci.org/mozilla/teach-api)
[![Shipping fast with zenHub](https://raw.githubusercontent.com/ZenHubIO/support/master/zenhub-badge.png)](https://zenhub.com)

This is a backend data store with a REST API for use by the
[teach website][teach].

## Requirements

* Python 2.7
* [pip and virtualenv](http://stackoverflow.com/q/4324558)

## Quick Start

```
virtualenv venv

# On Windows, replace the following line with 'venv\Scripts\activate'.
source venv/bin/activate

pip install -r requirements.minimal.txt
python manage.py syncdb
```

You will be asked if you want to create an administrative user.
Respond affirmatively, fill out the details, and then run:

```
python manage.py initgroups
python manage.py runserver
```

If you are running the Teach-API in a VM, and you wish to access the Django instance from outside the VM, you will need to have your VM use bridged networking (to make it part of your preexisting local network) and then use the following `runserver` command:

```
python manage.py runserver 0.0.0.0:8000
```

You can then access the server from the host machine on the VM's IP address. For example, if the VM has an IP `192.168.1.1`, the host machine can access the teach-api via `http://192.168.1.1:8000`

## Making a "staff" account, to use the `http://localhost:8000/admin` route

In order to use the admin route, you will need to clear a user account by ensuring `is_staff = 1`. If the webmaker login username that you want to use is the same as the administrative user, you're done. Otherwise, after signing in with your webmaker user account once, connect to the `db.sqlite3` database file in the root directory ([SQLite Manager](https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager/) for Firefox is highly recommended for working with Sqlite files), and in the `auth_users` table, update the record for your webmaker account such that `is_staff` has the value `1`.

You should now be able to load up the administrative view for the teach-api via http://localhost:8000/admin

## Environment Variables

Unlike traditional Django settings, we use environment variables
for configuration to be compliant with [twelve-factor][] apps.

**Note:** When an environment variable is described as representing a
boolean value, if the variable exists with *any* value (even the empty
string), the boolean is true; otherwise, it's false.

**Note:** When running `manage.py`, the following environment
variables are given default values: `SECRET_KEY`, `PORT`, `ORIGIN`.
`CORS_API_LOGIN_ORIGINS`. Also, `DEBUG` is enabled.

* `SECRET_KEY` is a large random value.
* `DEBUG` is a boolean value that indicates whether debugging is enabled
  (this should always be false in production).
* `PORT` is the port that the server binds to.
* `ORIGIN` is the origin of the server, as it appears
  to users. If `DEBUG` is enabled, this defaults to
  `http://localhost:PORT`. Otherwise, it must be defined.
* `ADMIN_PROTECTION_USERPASS` is an optional *username:password* value
  that can be used to provide extra protection for accessing the
  admin UI. That is, in addition to requiring staff permission to access the
  admin UI, they will also be prompted for this username and password via
  HTTP Basic Authentication.
* `DATABASE_URL` is the URL for the database. Defaults to a `sqlite://`
  URL pointing to `db.sqlite3` at the root of the repository. If this
  value is the name of another (all-caps) environment variable, e.g.
  `HEROKU_POSTGRESQL_AMBER_URL`, that variable's value will be used
  as the database URL.
* `SECURE_PROXY_SSL_HEADER` is an optional HTTP request header field name
  and value indicating that the request is actually secure. For example,
  Heroku deployments should set this to `X-Forwarded-Proto: https`.
* `DEFAULT_FROM_EMAIL` is the default email address to use for various
  automated correspondence from the site manager(s), such as password
  resets. Defaults to `webmaster@localhost`.
* `TEACH_STAFF_EMAILS` is a comma-separated list of email addresses
  representing people who should be emailed whenever a Webmaker Club
  is created, or something else notable (but also non-technical) is
  done on the site.
* `EMAIL_BACKEND_URL` is a URL representing the email backend to use.
  Examples include `console:`, `smtp://hostname:port`, and
  `smtp+tls://user:pass@hostname:port`. Mandrill can also be used
  via 'mandrill://your-mandrill-api-key', though this requires the
  [djrill][] package.
* `IDAPI_URL` is the URL of the Webmaker ID (OAuth2) server. Defaults
  to `https://id.webmaker.org`. If it is set to a value of the
  form `fake:username:email`, e.g. `fake:foo:foo@example.org`, and if
  `DEBUG` is true, then the given username/email will always be
  logged in when the OAuth2 authorize endpoint is contacted, which
  is useful for offline development.
* `IDAPI_CLIENT_ID` is the server's OAuth2 client ID.
* `IDAPI_CLIENT_SECRET` is the server's OAuth2 client secret.
* `CORS_API_LOGIN_ORIGINS` is a comma-separated list of origins that
  can submit Persona assertions to the API server in exchange for API
  tokens. It's also a list of origins that can delegate login to
  the API server and obtain API tokens. This list should not
  contain any whitespace. If `DEBUG` is enabled, any origin can
  submit Persona assertions or delegate login to the API server.
* `TEACH_SITE_URL` is the URL to the Teach site, used when sending
  emails to users, among other things. It defaults to
  https://teach.mozilla.org.
* `DISCOURSE_SSO_SECRET` is the SSO secret for Discourse single sign-on.
  For more information, see [discourse_sso/README.md][]. If empty or
  undefined, Discourse SSO functionality will be disabled.
* `DISCOURSE_SSO_ORIGIN` is the origin of your Discourse site. If
  `DISCOURSE_SSO_SECRET` is set, this must also be set.
* `CREDLY_API_KEY` Credly API key
  `CREDLY_APP_SECRET` Credly App Secret
   for more details see https://developers.credly.com/my-apps

### Deprecated Environment Variables

These will be removed at some point.

* `LOGINAPI_URL` is the URL of the Webmaker login API server.
  Defaults to `https://login.webmaker.org`.
* `LOGINAPI_AUTH` is the *username:password* pair that will be
  used to authenticate with the Webmaker login server, e.g.
  `john:1234`. This is needed for Persona-based authentication only.
* `BROWSERID_AUTOLOGIN_EMAIL` specifies an email address to auto-login
  as when Persona login buttons are clicked. It is useful for offline
  development and is only valid if `DEBUG` is true. Make sure an
  existing Django user account exists for the email associated with
  this address.

## Deployment

It's assumed that production deploys (i.e. where `DEBUG` is false)
are hosted over https. **The site will not work if it is hosted on
production over http.**

<!-- Links -->

  [teach]: https://github.com/mozilla/teach.webmaker.org
  [twelve-factor]: http://12factor.net/
  [djrill]: https://github.com/brack3t/Djrill
  [discourse_sso/README.md]: https://github.com/mozilla/teach-api/tree/master/discourse_sso#readme
