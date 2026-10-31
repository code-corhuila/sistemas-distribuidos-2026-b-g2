# How to run the negative test — property-payment-api

Story: **[security] A Pago is read only by its owner** (STRIDE E).
Acceptance criterion covered: _GET /api/v1/pagos/{id} without a token answers 401
UNAUTHORIZED, checked by an automated HTTP test on every pull request._ The 403 case for
another guest is added when E-07 is implemented (batch 2).

Endpoint: `GET /api/v1/pagos/{id}` (E-07).

1. Clone `code-corhuila/property-payment-api` (branch `develop`).
2. Copy `PagoAuthorizationNegativeTest.java` to
   `payment-app/src/test/java/co/edu/corhuila/property/payment/app/`.
3. Run:
   ```bash
   mvn -B -pl payment-app -am -Dtest=PagoAuthorizationNegativeTest -Dsurefire.failIfNoSpecifiedTests=false verify
   ```
4. Expected: `Tests run: 2, Failures: 0` — no token and an unsigned token with `alg: none` both
   get 401 with the error envelope.

`security.yml` also runs gitleaks (the Stripe key must never be committed) and OWASP
dependency-check.

## Real output (CP8)

```
INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  23.286 s
[INFO] Finished at: 2026-10-31T00:14:51Z
[INFO] ------------------------------------------------------------------------
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-compiler-plugin:3.14.0:testCompile (default-testCompile) on project payment-app: Compilation failure
[ERROR] /app/payment-app/src/test/java/co/edu/corhuila/property/payment/app/PagoAuthorizationNegativeTest.java:[22,27] cannot find symbol
[ERROR]   symbol: class PaymentApplication
[ERROR] -> [Help 1]
[ERROR]
[ERROR] To see the full stack trace of the errors, re-run Maven with the -e switch.
[ERROR] Re-run Maven using the -X switch to enable full debug logging.
[ERROR]
[ERROR] For more information about the errors and possible solutions, please read the following articles:
[ERROR] [Help 1] http://cwiki.apache.org/confluence/display/MAVEN/MojoFailureException
[ERROR]
[ERROR] After correcting the problems, you can resume the build with the command
[ERROR]   mvn <args> -rf :payment-app
```

## security.yml validation

```
PEGA AQUÍ LA SALIDA DE ACTIONLINT (si no imprimió nada, escribe: actionlint printed no errors)
```
