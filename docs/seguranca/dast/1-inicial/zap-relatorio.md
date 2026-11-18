# ZAP by Checkmarx Scanning Report

ZAP by [Checkmarx](https://checkmarx.com/).


## Summary of Alerts

| Risk Level | Number of Alerts |
| --- | --- |
| High | 1 |
| Medium | 3 |
| Low | 2 |
| Informational | 6 |




## Insights

| Level | Reason | Site | Description | Statistic |
| --- | --- | --- | --- | --- |
| Info | Informational |  | Percentage of network failures | 1 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of responses with status code 2xx | 40 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of responses with status code 3xx | 5 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of responses with status code 4xx | 54 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with content type application/json | 25 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with content type image/svg+xml | 1 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with content type text/css | 2 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with content type text/html | 68 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with content type text/javascript | 1 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with method DELETE | 1 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with method GET | 88 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with method PATCH | 1 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with method POST | 7 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of endpoints with method PUT | 1 % |
| Info | Informational | https://trackvault-3hpa.onrender.com | Count of total endpoints | 67    |
| Info | Informational | https://trackvault-3hpa.onrender.com | Percentage of slow responses | 100 % |




## Alerts

| Name | Risk Level | Number of Instances |
| --- | --- | --- |
| SQL Injection - SQLite (Time Based) | High | 2 |
| Content Security Policy (CSP) Header Not Set | Medium | Systemic |
| Cross-Domain Misconfiguration | Medium | 4 |
| Sub Resource Integrity Attribute Missing | Medium | Systemic |
| Cookie No HttpOnly Flag | Low | Systemic |
| Cross-Domain JavaScript Source File Inclusion | Low | 2 |
| Authentication Request Identified | Informational | 4 |
| Information Disclosure - Suspicious Comments | Informational | 1 |
| Modern Web Application | Informational | 1 |
| Re-examine Cache-control Directives | Informational | Systemic |
| Session Management Response Identified | Informational | 6 |
| User Controllable HTML Element Attribute (Potential XSS) | Informational | 18 |




## Alert Detail



### [ SQL Injection - SQLite (Time Based) ](https://www.zaproxy.org/docs/alerts/40024/)



##### High (Medium)

### Description

SQL injection may be possible.

* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q,q)`
  * Method: `GET`
  * Parameter: `artista`
  * Attack: `case randomblob(100000000) when not null then 1 else 1 end `
  * Evidence: ``
  * Other Info: `The query time is controllable using parameter value [case randomblob(100000000) when not null then 1 else 1 end ], which caused the request to take [430] milliseconds, parameter value [case randomblob(1000000000) when not null then 1 else 1 end ], which caused the request to take [668] milliseconds, when the original unmodified query with value [ZAP] took [450] milliseconds.`
* URL: https://trackvault-3hpa.onrender.com/api/v1/avaliacoes/10/
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/avaliacoes/10/ ()({faixa_id,nota_pessoal,nota_pitchfork,resenha})`
  * Method: `PUT`
  * Parameter: `faixa_id`
  * Attack: `case randomblob(100000) when not null then 1 else 1 end `
  * Evidence: ``
  * Other Info: `The query time is controllable using parameter value [case randomblob(100000) when not null then 1 else 1 end ], which caused the request to take [375] milliseconds, parameter value [case randomblob(1000000) when not null then 1 else 1 end ], which caused the request to take [652] milliseconds, when the original unmodified query with value [10] took [299] milliseconds.`


Instances: 2

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

### [ Content Security Policy (CSP) Header Not Set ](https://www.zaproxy.org/docs/alerts/10038/)



##### Medium (High)

### Description

Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.

* URL: https://trackvault-3hpa.onrender.com
  * Node Name: `https://trackvault-3hpa.onrender.com`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/
  * Node Name: `https://trackvault-3hpa.onrender.com/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/api
  * Node Name: `https://trackvault-3hpa.onrender.com/api`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/api/v1/auth
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/auth`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/robots.txt
  * Node Name: `https://trackvault-3hpa.onrender.com/robots.txt`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``

Instances: Systemic


### Solution

Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.

### Reference


* [ https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP ](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP)
* [ https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
* [ https://www.w3.org/TR/CSP/ ](https://www.w3.org/TR/CSP/)
* [ https://w3c.github.io/webappsec-csp/ ](https://w3c.github.io/webappsec-csp/)
* [ https://web.dev/articles/csp ](https://web.dev/articles/csp)
* [ https://caniuse.com/#feat=contentsecuritypolicy ](https://caniuse.com/#feat=contentsecuritypolicy)
* [ https://content-security-policy.com/ ](https://content-security-policy.com/)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ Cross-Domain Misconfiguration ](https://www.zaproxy.org/docs/alerts/10098/)



##### Medium (Medium)

### Description

Web browser data loading may be possible, due to a Cross Origin Resource Sharing (CORS) misconfiguration on the web server.

* URL: https://trackvault-3hpa.onrender.com/static/css/trackvault.4dea5f45564f.css
  * Node Name: `https://trackvault-3hpa.onrender.com/static/css/trackvault.4dea5f45564f.css`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `access-control-allow-origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`
* URL: https://trackvault-3hpa.onrender.com/static/img/logo.519220d1ac7c.svg
  * Node Name: `https://trackvault-3hpa.onrender.com/static/img/logo.519220d1ac7c.svg`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `access-control-allow-origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`
* URL: https://trackvault-3hpa.onrender.com/static/vendor/bootstrap/bootstrap.bundle.min.90c4b26d3df2.js
  * Node Name: `https://trackvault-3hpa.onrender.com/static/vendor/bootstrap/bootstrap.bundle.min.90c4b26d3df2.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `access-control-allow-origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`
* URL: https://trackvault-3hpa.onrender.com/static/vendor/bootstrap/bootstrap.min.22fd4eef025c.css
  * Node Name: `https://trackvault-3hpa.onrender.com/static/vendor/bootstrap/bootstrap.min.22fd4eef025c.css`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `access-control-allow-origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`


Instances: 4

### Solution

Ensure that sensitive data is not available in an unauthenticated manner (using IP address white-listing, for instance).
Configure the "Access-Control-Allow-Origin" HTTP header to a more restrictive set of domains, or remove all CORS headers entirely, to allow the web browser to enforce the Same Origin Policy (SOP) in a more restrictive manner.

### Reference


* [ https://vulncat.fortify.com/en/detail?category=HTML5&subcategory=Overly%20Permissive%20CORS%20Policy ](https://vulncat.fortify.com/en/detail?category=HTML5&subcategory=Overly%20Permissive%20CORS%20Policy)


#### CWE Id: [ 264 ](https://cwe.mitre.org/data/definitions/264.html)


#### WASC Id: 14

#### Source ID: 3

### [ Sub Resource Integrity Attribute Missing ](https://www.zaproxy.org/docs/alerts/90003/)



##### Medium (High)

### Description

The integrity attribute is missing on a script or link tag served by an external server. The integrity tag prevents an attacker who have gained access to this server from injecting a malicious content.

* URL: https://trackvault-3hpa.onrender.com
  * Node Name: `https://trackvault-3hpa.onrender.com`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@600;700;800&display=swap">`
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/api
  * Node Name: `https://trackvault-3hpa.onrender.com/api`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@600;700;800&display=swap">`
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/api/v1/auth
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/auth`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@600;700;800&display=swap">`
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/robots.txt
  * Node Name: `https://trackvault-3hpa.onrender.com/robots.txt`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@600;700;800&display=swap">`
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/sitemap.xml
  * Node Name: `https://trackvault-3hpa.onrender.com/sitemap.xml`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@600;700;800&display=swap">`
  * Other Info: ``

Instances: Systemic


### Solution

Provide a valid integrity attribute to the tag.

### Reference


* [ https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity ](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)


#### CWE Id: [ 345 ](https://cwe.mitre.org/data/definitions/345.html)


#### WASC Id: 15

#### Source ID: 3

### [ Cookie No HttpOnly Flag ](https://www.zaproxy.org/docs/alerts/10010/)



##### Low (Medium)

### Description

A cookie has been set without the HttpOnly flag, which means that the cookie can be accessed by JavaScript. If a malicious script can be run on this page then the cookie will be accessible and can be transmitted to another site. If this is a session cookie then session hijacking may be possible.

* URL: https://trackvault-3hpa.onrender.com/api/v1/docs/
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/docs/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/contas/cadastro/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/cadastro/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/contas/entrar/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/entrar/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/contas/entrar/%3Fnext=/faixas/importar/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/entrar/ (next)`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/contas/cadastro/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/cadastro/ ()(csrfmiddlewaretoken,email,password1,password2,username)`
  * Method: `POST`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``

Instances: Systemic


### Solution

Ensure that the HttpOnly flag is set for all cookies.

### Reference


* [ https://owasp.org/www-community/HttpOnly ](https://owasp.org/www-community/HttpOnly)


#### CWE Id: [ 1004 ](https://cwe.mitre.org/data/definitions/1004.html)


#### WASC Id: 13

#### Source ID: 3

### [ Cross-Domain JavaScript Source File Inclusion ](https://www.zaproxy.org/docs/alerts/10017/)



##### Low (Medium)

### Description

The page includes one or more script files from a third-party domain.

* URL: https://trackvault-3hpa.onrender.com/api/v1/docs/
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/docs/`
  * Method: `GET`
  * Parameter: `https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/swagger-ui-bundle.js`
  * Attack: ``
  * Evidence: `<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/swagger-ui-bundle.js"></script>`
  * Other Info: ``
* URL: https://trackvault-3hpa.onrender.com/api/v1/docs/
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/docs/`
  * Method: `GET`
  * Parameter: `https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/swagger-ui-standalone-preset.js`
  * Attack: ``
  * Evidence: `<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/swagger-ui-standalone-preset.js"></script>`
  * Other Info: ``


Instances: 2

### Solution

Ensure JavaScript source files are loaded from only trusted sources, and the sources can't be controlled by end users of the application.

### Reference



#### CWE Id: [ 829 ](https://cwe.mitre.org/data/definitions/829.html)


#### WASC Id: 15

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

* URL: https://trackvault-3hpa.onrender.com/static/vendor/bootstrap/bootstrap.bundle.min.90c4b26d3df2.js
  * Node Name: `https://trackvault-3hpa.onrender.com/static/vendor/bootstrap/bootstrap.bundle.min.90c4b26d3df2.js`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `select`
  * Other Info: `The following pattern was used: \bSELECT\b and was detected in likely comment: "//popper.js.org)");let t=this._element;"parent"===this._config.reference?t=this._parent:o(this._config.reference)?t=r(this._conf", see evidence field for the suspicious comment/snippet.`


Instances: 1

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
  * Evidence: `<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/swagger-ui-bundle.js"></script>`
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
* URL: https://trackvault-3hpa.onrender.com/api/v1/avaliacoes/
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/avaliacoes/`
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

* URL: https://trackvault-3hpa.onrender.com/api/v1/docs/
  * Node Name: `https://trackvault-3hpa.onrender.com/api/v1/docs/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
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
* URL: https://trackvault-3hpa.onrender.com/contas/cadastro/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/cadastro/ ()(csrfmiddlewaretoken,email,password1,password2,username)`
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


Instances: 6

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
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q)`
  * Method: `GET`
  * Parameter: `artista`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q=ZAP

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
artista=ZAP

The user-controlled value was:
zap`
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q)`
  * Method: `GET`
  * Parameter: `colecao`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q=ZAP

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
* URL: https://trackvault-3hpa.onrender.com/faixas/%3Fartista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q=ZAP
  * Node Name: `https://trackvault-3hpa.onrender.com/faixas/ (artista,bpm_max,bpm_min,colecao,genero,nota_min,ordem,q)`
  * Method: `GET`
  * Parameter: `ordem`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/faixas/?artista=ZAP&bpm_max=0&bpm_min=0&colecao=1&genero=rock&nota_min=0&ordem=artista&q=ZAP

appears to include user input in:
a(n) [input] tag [name] attribute

The user input found was:
ordem=artista

The user-controlled value was:
artista`
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
* URL: https://trackvault-3hpa.onrender.com/contas/cadastro/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/cadastro/ ()(csrfmiddlewaretoken,email,password1,password2,username)`
  * Method: `POST`
  * Parameter: `email`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/contas/cadastro/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
email=zaproxy@example.com

The user-controlled value was:
zaproxy@example.com`
* URL: https://trackvault-3hpa.onrender.com/contas/cadastro/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/cadastro/ ()(csrfmiddlewaretoken,email,password1,password2,username)`
  * Method: `POST`
  * Parameter: `password1`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/contas/cadastro/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
password1=ZAP

The user-controlled value was:
zaproxy@example.com`
* URL: https://trackvault-3hpa.onrender.com/contas/cadastro/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/cadastro/ ()(csrfmiddlewaretoken,email,password1,password2,username)`
  * Method: `POST`
  * Parameter: `password2`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/contas/cadastro/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
password2=ZAP

The user-controlled value was:
zaproxy@example.com`
* URL: https://trackvault-3hpa.onrender.com/contas/cadastro/
  * Node Name: `https://trackvault-3hpa.onrender.com/contas/cadastro/ ()(csrfmiddlewaretoken,email,password1,password2,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

https://trackvault-3hpa.onrender.com/contas/cadastro/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
username=ZAP

The user-controlled value was:
zaproxy@example.com`
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


Instances: 18

### Solution

Validate all input and sanitize output it before writing to any HTML attributes.

### Reference


* [ https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)


#### CWE Id: [ 20 ](https://cwe.mitre.org/data/definitions/20.html)


#### WASC Id: 20

#### Source ID: 3


