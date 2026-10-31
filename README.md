# ssl-protocol-checker

Probe which TLS versions a server really negotiates (1.3 down to 1.0) and grade it A–F — servers still accepting old TLS get flagged.

## How to run

```sh
python3 main.py example.com 443
```

## Example output

```
TLSv1.3: supported
TLSv1.2: supported
TLSv1.1: rejected
TLSv1: rejected
Grade: A
```

Standard library only. Run the tests with `python3 -m unittest discover`.
