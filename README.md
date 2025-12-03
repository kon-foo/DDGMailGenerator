## DuckDuckGo E-Mail Generator

A simple wrapper around the DuckDuckGo E-Mail Protection endpoint. That allows me to safe it as a bookmark and generate new e-mail addresses on the fly, without havig to install the DuckDuckGo Browser Extension/ without having to install the DuckDuckGo App on Android. NOTICE: No authentication included: do not expose to the internet.

## HowTo

1. Generate a [DuckDuckGo Email Protection](https://duckduckgo.com/email/) account.
2. (Temporarily) install the Browser extension.
3. Navigate to the [Form to generate a new e-mail address](https://duckduckgo.com/email/settings/autofill).
4. Inspect the Network tab in the Browser DevTools to extract the Authorization Header.
5. Safe it to the .env file, prefixing it with your account in uppercase. E.g. if you account is foo@duck.com, the .env file should contain `BEARER_FOO=<token>`. Do not include the "Bearer ..." prefix.
6. Build/run the Docker container
7. Navigate to localhost:5000/generate?account=foo to generate a new e-mail address.
