Bottle PyJWT
============

This is a **bottle** plugin to use the *JWT* library

Quick Start
-----------

The **bottle-pyjwt** plugin allows to use token authentication using the java *jwt* standard

    from bottle import route, install
    from bottle.ext.jwt import JwtPlugin

    validate = lambda auth, auth_role: auth == auth_role

    app.install(JwtPlugin(validate, "my secret", fail_redirect="/login"))

    @route("/", auth="any values and types")
    def example():
        return "OK"

Changelog
---------

See [Changelog](CHANGELOG.md)

License
-------

See [Licencia](LICENSE.txt)