# ZAP by Checkmarx Scanning Report

ZAP by [Checkmarx](https://checkmarx.com/).


## Summary of Alerts

| Risk Level | Number of Alerts |
| --- | --- |
| High | 1 |
| Medium | 2 |
| Low | 1 |
| Informational | 6 |




## Insights

| Level | Reason | Site | Description | Statistic |
| --- | --- | --- | --- | --- |
| Low | Warning |  | ZAP warnings logged - see the zap.log file for details | 2    |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of responses with status code 2xx | 40 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of responses with status code 3xx | 4 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of responses with status code 4xx | 54 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with content type application/javascript | 1 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with content type application/json | 21 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with content type image/png | 1 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with content type image/svg+xml | 1 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with content type text/css | 5 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with content type text/html | 63 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with content type text/javascript | 5 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with method DELETE | 1 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with method GET | 89 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with method PATCH | 1 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with method POST | 6 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with method PUT | 1 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Count of total endpoints | 74    |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of slow responses | 100 % |




## Alerts

| Name | Risk Level | Number of Instances |
| --- | --- | --- |
| SQL Injection | High | 7 |
| CSP: Wildcard Directive | Medium | Systemic |
| CSP: style-src unsafe-inline | Medium | 1 |
| Timestamp Disclosure - Unix | Low | Systemic |
| Authentication Request Identified | Informational | 4 |
| Information Disclosure - Suspicious Comments | Informational | 3 |
| Modern Web Application | Informational | 1 |
| Re-examine Cache-control Directives | Informational | Systemic |
| Session Management Response Identified | Informational | 5 |
| User Controllable HTML Element Attribute (Potential XSS) | Informational | 15 |




## Alert Detail



### [ SQL Injection ](https://www.zaproxy.org/docs/alerts/40018/)



##### High (Medium)

### Description

SQL injection may be possible.

* URL: https://trackvault-3hpa.onrender.com/api/v1/avaliacoes/%3Ffaixa=10&minhas=true&page=12-2&page_size=10
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/avaliacoes/ (faixa,minhas,page,page_size)`
  * Method: `GET`
  * Parameter: `page`
  * Attack: `12-2`
  * Evidence: ``
  * Other Info: `The original page results were successfully replicated using the expression [12-2] as the parameter value
The parameter value being modified was stripped from the HTML output for the purposes of the comparison.`
* URL: https://trackvault-3hpa.onrender.com/api/v1/avaliacoes/%3Ffaixa=10&minhas=true&page=10&page_size=10%2527+AND+%25271%2527%253D%25271%2527+--+
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/avaliacoes/ (faixa,minhas,page,page_size)`
  * Method: `GET`
  * Parameter: `page_size`
  * Attack: `10' OR '1'='1' -- `
  * Evidence: ``
  * Other Info: `The page results were successfully manipulated using the boolean conditions [10' AND '1'='1' -- ] and [10' OR '1'='1' -- ]
The parameter value being modified was stripped from the HTML output for the purposes of the comparison.
Data was NOT returned for the original parameter.
The vulnerability was detected by successfully retrieving more data than originally returned, by manipulating the parameter.`
* URL: https://trackvault-3hpa.onrender.com/api/v1/colecoes/%3Fpage=10%2527+AND+%25271%2527%253D%25271%2527+--+&page_size=10
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/colecoes/ (page,page_size)`
  * Method: `GET`
  * Parameter: `page`
  * Attack: `10' AND '1'='1' -- `
  * Evidence: ``
  * Other Info: `The page results were successfully manipulated using the boolean conditions [10' AND '1'='1' -- ] and [10' AND '1'='2' -- ]
The parameter value being modified was stripped from the HTML output for the purposes of the comparison.
Data was returned for the original parameter.
The vulnerability was detected by successfully restricting the data originally returned, by manipulating the parameter.`
* URL: https://trackvault-3hpa.onrender.com/api/v1/colecoes/%3Fpage=10&page_size=12-2
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/colecoes/ (page,page_size)`
  * Method: `GET`
  * Parameter: `page_size`
  * Attack: `12-2`
  * Evidence: ``
  * Other Info: `The original page results were successfully replicated using the expression [12-2] as the parameter value
The parameter value being modified was stripped from the HTML output for the purposes of the comparison.`
* URL: https://trackvault-3hpa.onrender.com/api/v1/faixas/%3Fartista=artista&bpm_max=10&bpm_min=10&colecao=12-2&genero=blues&nota_min=1.2&ordem=artista&page=10&page_size=10&q=q
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,page,page_size,q)`
  * Method: `GET`
  * Parameter: `colecao`
  * Attack: `12-2`
  * Evidence: ``
  * Other Info: `The original page results were successfully replicated using the expression [12-2] as the parameter value
The parameter value being modified was stripped from the HTML output for the purposes of the comparison.`
* URL: https://trackvault-3hpa.onrender.com/api/v1/faixas/%3Fartista=artista&bpm_max=10&bpm_min=10&colecao=10&genero=blues&nota_min=1.2&ordem=artista&page=20%252F2&page_size=10&q=q
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,page,page_size,q)`
  * Method: `GET`
  * Parameter: `page`
  * Attack: `20/2`
  * Evidence: ``
  * Other Info: `The original page results were successfully replicated using the expression [20/2] as the parameter value
The parameter value being modified was stripped from the HTML output for the purposes of the comparison.`
* URL: https://trackvault-3hpa.onrender.com/api/v1/faixas/%3Fartista=artista&bpm_max=10&bpm_min=10&colecao=10&genero=blues&nota_min=1.2&ordem=artista&page=10&page_size=12-2&q=q
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,page,page_size,q)`
  * Method: `GET`
  * Parameter: `page_size`
  * Attack: `12-2`
  * Evidence: ``
  * Other Info: `The original page results were successfully replicated using the expression [12-2] as the parameter value
The parameter value being modified was stripped from the HTML output for the purposes of the comparison.`


Instances: 7

### Solution

Do not trust client side input, even if there is client side validation in place.
In general, type check all data on the server side.
If the application uses JDBC, use PreparedStatement or CallableStatement, with parameters passed by '?'
If the application uses ASP, use ADO Command Objects with strong type checking and parameterized queries.
If database Stored Procedures can be used, use them.
Do *not* concatenate strings into queries in the stored procedure, or use 'exec', 'exec immediate', or equivalent functionality!
Do not create dynamic SQL queries using simple string concatenation.
Escape all data received from the client.
Apply an 'allow list' of allowed characters, or a 'deny list' of disallowed characters in user input.
Apply the principle of least privilege by using the least privileged database user possible.
In particular, avoid using the 'sa' or 'db-owner' database users. This does not eliminate SQL injection, but minimizes its impact.
Grant the minimum database access that is necessary for the application.

### Reference


* [ https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)


#### CWE Id: [ 89 ](https://cwe.mitre.org/data/definitions/89.html)


#### WASC Id: 19

#### Source ID: 1

### [ CSP: Wildcard Directive ](https://www.zaproxy.org/docs/alerts/10055/)



##### Medium (High)

### Description

Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks. Including (but not limited to) Cross Site Scripting (XSS), and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.

* URL: https://trackvault-3hpa.onrender.com
  * Node Name: `https://trackvault-3hpa.onrender.com`
  * Method: `GET`
  * Parameter: `content-security-policy`
  * Attack: ``
  * Evidence: `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'`
  * Other Info: `The following directives either allow wildcard sources (or ancestors), are not defined, or are overly broadly defined:
img-src`
* URL: https://trackvault-3hpa.onrender.com/api
  * Node Name: `https://trackvault-3hpa.onrender.com/api`
  * Method: `GET`
  * Parameter: `content-security-policy`
  * Attack: ``
  * Evidence: `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'`
  * Other Info: `The following directives either allow wildcard sources (or ancestors), are not defined, or are overly broadly defined:
img-src`
* URL: https://trackvault-3hpa.onrender.com/api/v1
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1`
  * Method: `GET`
  * Parameter: `content-security-policy`
  * Attack: ``
  * Evidence: `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'`
  * Other Info: `The following directives either allow wildcard sources (or ancestors), are not defined, or are overly broadly defined:
img-src`
* URL: https://trackvault-3hpa.onrender.com/api/v1/avaliacoes
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/avaliacoes`
  * Method: `GET`
  * Parameter: `content-security-policy`
  * Attack: ``
  * Evidence: `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'`
  * Other Info: `The following directives either allow wildcard sources (or ancestors), are not defined, or are overly broadly defined:
img-src`
* URL: https://trackvault-3hpa.onrender.com/sitemap.xml
  * Node Name: `https://trackvault-3hpa.onrender.com/sitemap.xml`
  * Method: `GET`
  * Parameter: `content-security-policy`
  * Attack: ``
  * Evidence: `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'`
  * Other Info: `The following directives either allow wildcard sources (or ancestors), are not defined, or are overly broadly defined:
img-src`

Instances: Systemic


### Solution

Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.

### Reference


* [ https://www.w3.org/TR/CSP/ ](https://www.w3.org/TR/CSP/)
* [ https://caniuse.com/#search=content+security+policy ](https://caniuse.com/#search=content+security+policy)
* [ https://content-security-policy.com/ ](https://content-security-policy.com/)
* [ https://github.com/HtmlUnit/htmlunit-csp ](https://github.com/HtmlUnit/htmlunit-csp)
* [ https://web.dev/articles/csp#resource-options ](https://web.dev/articles/csp#resource-options)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ CSP: style-src unsafe-inline ](https://www.zaproxy.org/docs/alerts/10055/)



##### Medium (High)

### Description

Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks. Including (but not limited to) Cross Site Scripting (XSS), and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.

* URL: https://trackvault-3hpa.onrender.com/api/v1/docs/
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/docs/`
  * Method: `GET`
  * Parameter: `content-security-policy`
  * Attack: ``
  * Evidence: `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'`
  * Other Info: `style-src includes unsafe-inline.`


Instances: 1

### Solution

Ensure that your web server, application server, load balancer, etc. is properly configured to set the Content-Security-Policy header.

### Reference


* [ https://www.w3.org/TR/CSP/ ](https://www.w3.org/TR/CSP/)
* [ https://caniuse.com/#search=content+security+policy ](https://caniuse.com/#search=content+security+policy)
* [ https://content-security-policy.com/ ](https://content-security-policy.com/)
* [ https://github.com/HtmlUnit/htmlunit-csp ](https://github.com/HtmlUnit/htmlunit-csp)
* [ https://web.dev/articles/csp#resource-options ](https://web.dev/articles/csp#resource-options)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ Timestamp Disclosure - Unix ](https://www.zaproxy.org/docs/alerts/10096/)



##### Low (Low)

### Description

A timestamp was disclosed by the application/web server. - Unix

* URL: https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.a90d4e3f4b86.js
  * Node Name: `https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.a90d4e3f4b86.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `1518500249`
  * Other Info: `1518500249, which evaluates to: 2018-02-13 03:37:29.`
* URL: https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.a90d4e3f4b86.js
  * Node Name: `https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.a90d4e3f4b86.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `1732584193`
  * Other Info: `1732584193, which evaluates to: 2024-11-25 22:23:13.`
* URL: https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.a90d4e3f4b86.js
  * Node Name: `https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.a90d4e3f4b86.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `1750603025`
  * Other Info: `1750603025, which evaluates to: 2025-06-22 11:37:05.`
* URL: https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.a90d4e3f4b86.js
  * Node Name: `https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.a90d4e3f4b86.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `1859775393`
  * Other Info: `1859775393, which evaluates to: 2028-12-07 01:16:33.`
* URL: https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.a90d4e3f4b86.js
  * Node Name: `https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.a90d4e3f4b86.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `1894007588`
  * Other Info: `1894007588, which evaluates to: 2030-01-07 06:13:08.`

Instances: Systemic


### Solution

Manually confirm that the timestamp data is not sensitive, and that the data cannot be aggregated to disclose exploitable patterns.

### Reference


* [ https://cwe.mitre.org/data/definitions/200.html ](https://cwe.mitre.org/data/definitions/200.html)


#### CWE Id: [ 497 ](https://cwe.mitre.org/data/definitions/497.html)


#### WASC Id: 13

#### Source ID: 3

### [ Authentication Request Identified ](https://www.zaproxy.org/docs/alerts/10111/)



##### Informational (Low)

### Description

The given request has been identified as an authentication request. The 'Other Info' field contains a set of key=value lines which identify any relevant fields. If the request is in a context which has an Authentication Method set to "Auto-Detect" then this rule will change the authentication to match the request identified.

* URL: https://trackvault-3hpa.onrender.com/api/v1/auth/token/
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/auth/token/ ()({email,password})`
  * Method: `POST`
  * Parameter: `email`
  * Attack: ``
  * Evidence: `password`
  * Other Info: `userParam=email
userValue=curador@exemplo.com
passwordParam=password`
* URL: https://trackvault-3hpa.onrender.com/contas/cadastro/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/cadastro/ ()(csrfmiddlewaretoken,email,password1,password2,username)`
  * Method: `POST`
  * Parameter: `email`
  * Attack: ``
  * Evidence: `password1`
  * Other Info: `userParam=email
userValue=zaproxy@example.com
passwordParam=password1
referer=https://trackvault-3hpa.onrender.com/contas/cadastro/
csrfToken=csrfmiddlewaretoken`
* URL: https://trackvault-3hpa.onrender.com/contas/entrar/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/entrar/ ()(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: `password`
  * Other Info: `userParam=username
userValue=foo-bar@example.com
passwordParam=password
referer=https://trackvault-3hpa.onrender.com/contas/entrar/
csrfToken=csrfmiddlewaretoken`
* URL: https://trackvault-3hpa.onrender.com/contas/entrar/%3Fnext=/faixas/importar/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/entrar/ (next)(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: `password`
  * Other Info: `userParam=username
userValue=foo-bar@example.com
passwordParam=password
referer=https://trackvault-3hpa.onrender.com/contas/entrar/?next=/faixas/importar/
csrfToken=csrfmiddlewaretoken`


Instances: 4

### Solution

This is an informational alert rather than a vulnerability and so there is nothing to fix.

### Reference


* [ https://www.zaproxy.org/docs/desktop/addons/authentication-helper/auth-req-id/ ](https://www.zaproxy.org/docs/desktop/addons/authentication-helper/auth-req-id/)



#### Source ID: 3

### [ Information Disclosure - Suspicious Comments ](https://www.zaproxy.org/docs/alerts/10027/)



##### Informational (Low)

### Description

The response appears to contain suspicious comments which may help an attacker.

* URL: https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-bundle.37aa30ada62e.js
  * Node Name: `https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-bundle.37aa30ada62e.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `query`
  * Other Info: `The following pattern was used: \bQUERY\b and was detected in likely comment: "//","$"),U=COMMENT("/\\*","\\*/"),V=COMMENT("#","$"),Y={className:"number",begin:w,relevance:0},Z={className:"number",begin:x,re", see evidence field for the suspicious comment/snippet.`
* URL: https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.a90d4e3f4b86.js
  * Node Name: `https://trackvault-3hpa.onrender.com/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-standalone-preset.a90d4e3f4b86.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `select`
  * Other Info: `The following pattern was used: \bSELECT\b and was detected in likely comment: "//github.com/zloirock/core-js/blob/v3.40.0/LICENSE",source:"https://github.com/zloirock/core-js"})},5816(t,e,r){"use strict";var", see evidence field for the suspicious comment/snippet.`
* URL: https://trackvault-3hpa.onrender.com/static/vendor/bootstrap/bootstrap.bundle.min.90c4b26d3df2.js
  * Node Name: `https://trackvault-3hpa.onrender.com/static/vendor/bootstrap/bootstrap.bundle.min.90c4b26d3df2.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `select`
  * Other Info: `The following pattern was used: \bSELECT\b and was detected in likely comment: "//popper.js.org)");let t=this._element;"parent"===this._config.reference?t=this._parent:o(this._config.reference)?t=r(this._conf", see evidence field for the suspicious comment/snippet.`


Instances: 3

### Solution

Remove all comments that return information that may help an attacker and fix any underlying problems they refer to.

### Reference



#### CWE Id: [ 615 ](https://cwe.mitre.org/data/definitions/615.html)


#### WASC Id: 13

#### Source ID: 3

### [ Modern Web Application ](https://www.zaproxy.org/docs/alerts/10109/)



##### Informational (Medium)

### Description

The application appears to be a modern web application. If you need to explore it automatically then the Ajax Spider may well be more effective than the standard one.

* URL: https://trackvault-3hpa.onrender.com/api/v1/docs/
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/docs/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<script src="/static/drf_spectacular_sidecar/swagger-ui-dist/swagger-ui-bundle.37aa30ada62e.js"></script>`
  * Other Info: `No links have been found while there are scripts, which is an indication that this is a modern web application.`


Instances: 1

### Solution

This is an informational alert and so no changes are required.

### Reference




#### Source ID: 3

### [ Re-examine Cache-control Directives ](https://www.zaproxy.org/docs/alerts/10015/)



##### Informational (Low)

### Description

The cache-control header has not been set properly or is missing, allowing the browser and proxies to cache content. For static assets like css, js, or image files this might be intended, however, the resources should be reviewed to ensure that no sensitive content will be cached.

* URL: https://trackvault-3hpa.onrender.com
  * Node Name: `https://trackvault-3hpa.onrender.com`
  * Method: `GET`
  * Parameter: `cache-control`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/
  * Node Name: `https://trackvault-3hpa.onrender.com/`
  * Method: `GET`
  * Parameter: `cache-control`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/api/v1/faixas/10/
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/faixas/10/`
  * Method: `GET`
  * Parameter: `cache-control`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/api/v1/schema/
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/schema/`
  * Method: `GET`
  * Parameter: `cache-control`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/colecoes/
  * Node Name: `https://trackvault-3hpa.onrender.com/colecoes/`
  * Method: `GET`
  * Parameter: `cache-control`
  * Attack: ``
  * Evidence: ``
  * Other Info: ``

Instances: Systemic


### Solution

For secure content, ensure the cache-control HTTP header is set with "no-cache, no-store, must-revalidate". If an asset should be cached consider setting the directives "public, max-age, immutable".

### Reference


* [ https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#web-content-caching ](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html#web-content-caching)
* [ https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control ](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control)
* [ https://grayduck.mn/2021/09/13/cache-control-recommendations/ ](https://grayduck.mn/2021/09/13/cache-control-recommendations/)


#### CWE Id: [ 525 ](https://cwe.mitre.org/data/definitions/525.html)


#### WASC Id: 13

#### Source ID: 3

### [ Session Management Response Identified ](https://www.zaproxy.org/docs/alerts/10112/)



##### Informational (Medium)

### Description

The given response has been identified as containing a session management token. The 'Other Info' field contains a set of header tokens that can be used in the Header Based Session Management Method. If the request is in a context which has a Session Management Method set to "Auto-Detect" then this rule will change the session management to use the tokens identified.

* URL: https://trackvault-3hpa.onrender.com/contas/cadastro/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/cadastro/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: https://trackvault-3hpa.onrender.com/contas/entrar/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/entrar/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: https://trackvault-3hpa.onrender.com/contas/entrar/%3Fnext=/faixas/importar/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/entrar/ (next)`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: https://trackvault-3hpa.onrender.com/contas/entrar/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/entrar/ ()(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: https://trackvault-3hpa.onrender.com/contas/entrar/%3Fnext=/faixas/importar/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/entrar/ (next)(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`


Instances: 5

### Solution

This is an informational alert rather than a vulnerability and so there is nothing to fix.

### Reference


* [ https://www.zaproxy.org/docs/desktop/addons/authentication-helper/session-mgmt-id/ ](https://www.zaproxy.org/docs/desktop/addons/authentication-helper/session-mgmt-id/)



#### Source ID: 3

### [ User Controllable HTML Element Attribute (Potential XSS) ](https://www.zaproxy.org/docs/alerts/10031/)



##### Informational (Low)

### Description

This check looks at user-supplied input in query string parameters and POST data to identify where certain HTML attribute values might be controlled. This provides hot-spot detection for XSS (cross-site scripting) that will require further review by a security analyst to determine exploitability.

* URL: https://trackvault-3hpa.onrender.com/contas/entrar/%3Fnext=/faixas/importar/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/entrar/ (next)`
  * Method: `GET`
  * Parameter: `next`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/contas/entrar/?next=/faixas/importar/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
next=/faixas/importar/

The user-controlled value was:
/faixas/importar/`
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=recentes&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q)`
  * Method: `GET`
  * Parameter: `artista`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=recentes&q=ZAP

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
artista=ZAP

The user-controlled value was:
zap`
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=recentes&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q)`
  * Method: `GET`
  * Parameter: `colecao`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=recentes&q=ZAP

appears to include user input in:
a(n) [meta] tag [content] attribute

The user input found was:
colecao=1

The user-controlled value was:
width=device-width, initial-scale=1`
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=recentes&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q)`
  * Method: `GET`
  * Parameter: `genero`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=recentes&q=ZAP

appears to include user input in:
a(n) [option] tag [value] attribute

The user input found was:
genero=rock

The user-controlled value was:
rock`
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=recentes&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q)`
  * Method: `GET`
  * Parameter: `ordem`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=recentes&q=ZAP

appears to include user input in:
a(n) [option] tag [value] attribute

The user input found was:
ordem=recentes

The user-controlled value was:
recentes`
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=recentes&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q)`
  * Method: `GET`
  * Parameter: `q`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=recentes&q=ZAP

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
q=ZAP

The user-controlled value was:
zap`
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q,q)`
  * Method: `GET`
  * Parameter: `artista`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q&q=ZAP

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
artista=ZAP

The user-controlled value was:
zap`
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q,q)`
  * Method: `GET`
  * Parameter: `colecao`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q&q=ZAP

appears to include user input in:
a(n) [meta] tag [content] attribute

The user input found was:
colecao=1

The user-controlled value was:
width=device-width, initial-scale=1`
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q,q)`
  * Method: `GET`
  * Parameter: `genero`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q&q=ZAP

appears to include user input in:
a(n) [option] tag [value] attribute

The user input found was:
genero=rock

The user-controlled value was:
rock`
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q,q)`
  * Method: `GET`
  * Parameter: `ordem`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q&q=ZAP

appears to include user input in:
a(n) [input] tag [name] attribute

The user input found was:
ordem=artista

The user-controlled value was:
artista`
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q,q)`
  * Method: `GET`
  * Parameter: `q`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q&q=ZAP

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
q=ZAP

The user-controlled value was:
zap`
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fordem=recentes
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (ordem)`
  * Method: `GET`
  * Parameter: `ordem`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?ordem=recentes

appears to include user input in:
a(n) [option] tag [value] attribute

The user input found was:
ordem=recentes

The user-controlled value was:
recentes`
* URL: https://trackvault-3hpa.onrender.com/contas/entrar/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/entrar/ ()(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/contas/entrar/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
username=foo-bar@example.com

The user-controlled value was:
foo-bar@example.com`
* URL: https://trackvault-3hpa.onrender.com/contas/entrar/%3Fnext=/faixas/importar/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/entrar/ (next)(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: `next`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/contas/entrar/?next=/faixas/importar/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
next=/faixas/importar/

The user-controlled value was:
/faixas/importar/`
* URL: https://trackvault-3hpa.onrender.com/contas/entrar/%3Fnext=/faixas/importar/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/entrar/ (next)(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/contas/entrar/?next=/faixas/importar/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
username=foo-bar@example.com

The user-controlled value was:
foo-bar@example.com`


Instances: 15

### Solution

Validate all input and sanitize output it before writing to any HTML attributes.

### Reference


* [ https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)


#### CWE Id: [ 20 ](https://cwe.mitre.org/data/definitions/20.html)


#### WASC Id: 20

#### Source ID: 3


