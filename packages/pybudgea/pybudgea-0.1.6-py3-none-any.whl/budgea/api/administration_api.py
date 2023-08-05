# coding: utf-8

"""
    Budgea API Documentation

    # Budgea Development Guides  Welcome to **Budgea**'s documentation.  This documentation is intended to get you up-and-running with our APIs and advise on the implementation of some regulatory aspects of your application, following the DSP2's guidelines.  ## Getting Started **IMPORTANT** Depending on your status with regard of the DSP2 regulation, **agent** or **partner**, you may call our APIs or simply use our Webview and callbacks to get the financial data of your users. As an **agent**, you are allowed to call directly our APIs and implement your own form to get the user's credentials. As a **partner**, you cannot manipulate the credentials, and have to delegate this step to us through our webview.  The sections below will document how to use our APIs, make sure you have the **agent** status to do so. For the **partner**, please refer to the section *Webview* and *Callbacks* of this documentation.  ### Overview Your API is a REST API which requires a communication through https to send and receive JSON documents. During your tests, we recommend to make calls to the API with curl or any other HTTP client of your choice. You can watch a video demonstration on this [URL](https://asciinema.org/a/FsaFyt3WAPyDm7sfaZPkwal3V). For the examples we'll use the demo API with address `https://demo.biapi.pro`, you should change that name to your API's name.  ### Hello World Let's start by calling the service `/banks` which lists all available banks. ``` curl https://demo.biapi.pro/2.0/banks/ ``` To log in to a bank webpage, you'll need to know for a given bank, the fields your user should fill in the form. Let's call a  specific bank and ask for an additional resource *fields*. ``` curl https://demo.biapi.pro/2.0/banks/59?expand=fields ``` The response here concerns only 1 bank (since we specified an id) and the resource _Fields_ is added to the response thanks to the query parameter `expand`.  To get more interesting things done, you'll need to send authenticated requests.  ### Authentication The way to authenticate is by passing the `Authorization: Bearer <token>` header in your request. At the setup a _manage token_ have been generated, you can use this token for now, when creating your user we'll see how to generate a user's token. ``` curl https://demo.biapi.pro/2.0/config \\   -H 'Authorization: Bearer <token>' ``` This endpoint will list all the parameters you can change to adapt Budgea to your needs.  We've covered the very first calls. Before diving deeper, let's see some general information about the APIs.  ## Abstract  ### API URL `https://demo.biapi.pro/2.0`  ### Requests format Data format: **application/x-www-form-urlencoded** or **application/json** (suggested)  Additional headers: Authorization: User's token (private)  ### Responses format Data format: **application/json** ([http://www.json.org](http://www.json.org/)) Charset: **UTF-8**  ### Resources Each call on an endpoint will return resources. The main resources are: | Resource            | Description                                                                                                           | | ---------------------|:------------------------------------------------------------------------------------------------------------------   | |Users                 |Represent a user                                                                                                      | |Connection            |A set of data used to authenticate on a website (usually a login and password). There is 1 connection for each website| |Account               |A bank account contained in a connection                                                                              | |Transaction           |An entry in a bank account                                                                                            | |Investment            |An asset in a bank account                                                                                            |  The chain of resources is as follow: **Users ∈ Connections ∈ Accounts ∈ Transactions or Investments**  ### RESTful API  This API is RESTful, which means it is stateless and each resource is accessed with an unique URI.  Several HTTP methods are available:  | Method                  | Description                    | | ------------------------|:-------------------------------| | GET /resources          | List resources                 | | GET /resources/{ID}     | Get a resource from its ID     | | POST /resources         | Create a new resource          | | POST /resources/{ID}    | Update a resource              | | PUT /resources  /{ID}   | Update a resource              | | DELETE /resources       | Remove every resources         | | DELETE /resources/{ID}  | Delete a resource              |   Each resource can contain sub-resources, for example: `/users/me/connections/2/accounts/23/transactions/48`  ### HTTP response codes  | Code        | Message               | Description                                                                                   | | ----------- |:---------------------:|-----------------------------------------------------------------------------------------------| | 200         | OK                    |Default response when a GET or POST request has succeed                                        | | 202         | Accepted              |For a new connection this code means it is necessary to provide complementary information (2FA)| | 204         | No content            |Default response when a POST request succeed without content                                   | | 400         | Bad request           |Supplied parameters are incorrect                                                              | | 403         | Forbidden             |Invalid token                                                                                  | | 500         | Internal Servor Error |Server error                                                                                   | | 503         | Service Unavailable   |Service is temporarily unavailable                                                             |  ### Errors management In case an error occurs (code 4xx or 5xx), the response can contain a JSON object describing this error: ```json {    \"code\": \"authFailure\",    \"message\": \"Wrong password\"  // Optional } ``` If an error is displayed on the website, Its content is returned in error_message field. The list of all possible errors is listed further down this page.  ### Authentication A user is authenticated by an access_token which is sent by the API during a call on one of the authentication services, and can be supplied with this header: `Authorization: Bearer YYYYYYYYYYYYYYYYYYYYYYYYYYY`   There are two user levels:      - Normal user, which can only access to his own accounts     - Administrator, with extended rights  ### Default filters During a call to an URI which lists resources, some filters can be passed as query parameters:  | Parameter   | Type      | Description                                               | | ----------- |:---------:|-----------------------------------------------------------| | offset      | Integer   |Offset of the first returned resource                      | | limit       | Integer   |Limit number of results                                    | | min_date    | Date      |Minimal date (if supported by service), format: YYYY-MM-DD | | max_date    | Date      |Maximal date (if supported by service), format: YYYY-MM-DD |  ### Extend requests During a GET on a set of resources or on a unique resource, it is possible to add a parameter expand to the request to extend relations with other resources:  `GET /2.0/users/me/accounts/123?expand=transactions[category],connection`  ```json {    \"id\" : 123    \"name\" : \"Compte chèque\"    \"balance\" : 1561.15    \"transactions\" : [       {          \"id\" : 9849,          \"simplified_wording\" : \"HALL'S BEER\",          \"value\" : -513.20,          ...          \"category\" : {             \"id\" : 561,             \"name\" : \"Sorties / Bar\",             ...          }        },        ...    ],    \"id_user\" : 1,    \"connection\" : {       \"id\" : 1518,       \"id_bank\" : 41,       \"id_user\" : 1,       \"error\" : null,       ...    } } ```  ### Request example ```http GET /2.0/banks?offset=0&limit=10&expand=fields Host: demo.biapi.pro Accept: application/json Authorization: Bearer <token> ``` ```http HTTP/1.1 200 OK Content-Type: application/json Content-Length: 3026 Server: Apache Date: Fri, 14 Mar 2014 08:24:02 GMT  {    \"banks\" : [       {          \"id_weboob\" : \"bnporc\",          \"name\" : \"BNP Paribas\",          \"id\" : 3,          \"hidden\" : false,          \"fields\" : [             {                \"id\" : 1,                \"id_bank\" : 3,                \"regex\" : \"^[0-9]{5,10}$\",                \"name\" : \"login\",                \"type\" : \"text\",                \"label\" : \"Numéro client\"             },             {                \"id\" : 2,                \"id_bank\" : 3,                \"regex\" : \"^[0-9]{6}$\",                \"name\" : \"password\",                \"type\" : \"password\",                \"label\" : \"Code secret\"             }          ]       },       ...    ]    \"total\" : 41 } ```  ### Constants #### List of bank account types | Type          |Description                        | | -----------   |-----------------------------------| | checking      |Checking account                   | | savings       |Savings account                    | | deposit       |Deposit accounts                   | | loan          |Loan                               | | market        | Market accounts                   | | joint         |Joint account                      | | card          |Card                               | | lifeinsurance |Life insurance accounts            | | pee           |Plan Épargne Entreprise            | | perco         |Plan Épargne Retraite              | | article83     |Article 83                         | | rsp           |Réserve spéciale de participation  | | pea           |Plan d'épargne en actions          | | capitalisation|Contrat de capitalisation          | | perp          |Plan d'épargne retraite populaire  | | madelin       |Contrat retraite Madelin           | | unknown       |Inconnu                            |  #### List of transaction types  | Type         |Description                        | | -----------  |-----------------------------------| |transfer      |Transfers                          | |order         |Orders                             | |check         |Checks                             | |deposit       |Cash deposit                       | |payback       |Payback                            | |withdrawal    |Withdrawal                         | |loan_payment  |Loan payment                       | |bank          |Bank fees                          | |card          |Card operation                     | |deferred_card |Deferred card operation            | |card_summary  |Mensual debit of a deferred card   |  #### List of synchronization errors ##### Error on Connection object The error field may take one of the below values in case of error when accessing the user space.  | Error                      |Description                                                                                       | | -----------------------    |--------------------------------------------------------------------------------------------------| |wrongpass                   |The authentication on website has failed                                                          | |additionalInformationNeeded |Additional information is needed such as an OTP                                                  | |websiteUnavailable          |The website is unavailable, for instance we get a HTTP 503 response when requesting the website   | |actionNeeded                |An action is needed on the website by the user, scraping is blocked                               | |SCARequired                |An SCA process must be done by updating the connection                               | |decoupled                  |Requires a user validation (ex: digital key)| |passwordExpired                   |The password has expired and needs to be changed on the website.                                                         | |webauthRequired                |A complete authentication process is required by update the connection via redirect                            | |bug                         |A bug has occurred during the synchronization. An alert has been sent to Budget Insight           |  #### Error on Account object Errors can be filled at the account level in case we access the user's dashboard but some account related data cannot be retrieved. For instance, we may not access the transactions or investments for a specific account. Getting an error during an account synchronization does not impact the scraping of other acccounts.  | Error                      |Description                                                                                       | | -----------------------    |--------------------------------------------------------------------------------------------------| |websiteUnavailable          |The website or a page is unavailable                                                              | |actionNeeded                |An action is needed on the website by the user, scraping is blocked                               | |bug                         |A bug has occurred during the synchronization. An alert has been sent to Budget Insight           |  Now you know the basics of Budgea API - Basic call to retrieve resources - Add query parameters to aplly filters - Expand resources - Authenticated calls  We're good for the basics! Now let's see how to integrate Budgea in your app and create your first user.  ## Integrate Budgea *(protocol or Webview)* ### The workflow Users of your application exist in the Budgea API. Every User is identified by an access_token which is the shared secret between your application and our API.  The workflow is as below: 1. The user is on your application and wants to share his bank accounts or invoices. 2. A call is made **client side** (browser's javascript or desktop application) to create a temporarily token which will be used to make API calls. 3. A form is built, allowing the user to select the connector to use (bank or provider, depending on context). Every connector requires different kind of credentials. 4. A call on the API is made with the temporarily token to add a **Connection** with the credentials supplied by user. 5. In case of success, the user chooses what bank accounts (**Account**) or subscriptions (**Subscription**) he wants to share with your application. 6. When he validates the share, the temporarily token is transmitted to your server. This one will call the Budgea API with this token to get a permanent token.  **Note** In case your application works without a server (for example a desktop application), the permanent token can be obtained on the 1st step, by supplying a client_secret to /auth/init and the step 6 is omitted. To get more information, read the protocol.  There are 3 steps to integrate Budgea in your application: 1. Provide a way for your users to share their credentials with you 2. Get the data scraped from Budgea 3. Be sure to follow the good practices before going into production  ### Get credentials from users You have 2 options here: - Integrate the Budget Insight's Webview, a turnkey solution to get user's credentials - Create your own form following the protocol (must have the *agent* status)  ### Budgea webview  The Budgea webview complements REST API endpoints with web-based services to handle sensitive or complex operations: - add a connection (to a bank or a provider), or edit/repare access to a connection; - manage connections (add/remove/edit); - edit and validate bank transfers (alpha preview).  Usage of the webview is mandatory if you don't hold an Agent status, since you are not allowed to use API endpoints carrying user credentials, and optional otherwise.  #### Implementation guidelines  ##### Base URL  The base URL of all services must be customized:   `https://{{domain}}.biapi.pro/2.0/auth/webview/`   `https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/`   - `{{domain}}`: substitute with you API domain; - `{{lang}}`: optionally specify the language of the webview, `en` or `fr` (if not specified, an automatic redirection will be performed following the language of the browser).  ##### Browser integration  Services available as part of the webview are designed as parameterized URLs intended to be opened in a web browser. A callback URI must be specified by callers to be notified at the end of the operation flow, similar to OAuth 2 specification.  You are encouraged to integrate web-based steps in your product following UX best practices: - in a web environment, perform a full-page redirect to the URL (using either [HTTP redirect](https://developer.mozilla.org/fr/docs/Web/HTTP/Status/302) or [scripting](https://developer.mozilla.org/fr/docs/Web/API/Location)), and avoid new tabs or popups; - in a native Android app, prefer opening the default browser or relying on [Chrome Custom Tabs](https://developer.chrome.com/multidevice/android/customtabs) to integrating a WebView; - in a native iOS app, prefer using a [SFSafariViewController](https://developer.apple.com/documentation/safariservices/sfsafariviewcontroller) to integrating a WKWebView.  ##### Callback handling  Most flows redirect to a callback URI at the end of the process. Query parameters are added to the URI to identify successful or failed operations.  Successful parameters are specific to each flow. In case of an error, the following parameters are added:  | Parameter | Description | | - | - | | `error` | An lowercase string error code identifying the kind of error that occurred. When the parameter is not present, the response is successful. | | `error_description` | A longer string description of the error (not intended for user display). |  Common error codes include:  | Code | Description | | - | - | | `access_denied` | The user explicitly cancelled the flow. | | `server_error` | Oops, a technical failure occurred during the process. |  **Forward compatibility requirement**: Additional error codes may be added in the future to describe specific cases. When implementing error codes handling, always fallback to a generic case for unknown codes.  ##### Browser compatibility  The webview is designed and tested to work with browsers supported by the Angular framework:   https://angular.io/guide/browser-support  ##### Privacy / GDPR status  The webview itself does not use any kind of long-term data persistence mechanism such as cookies or local storage, but some authentication or authorization steps may delegate to third-party web services that may implement them.  #### Configuration  You can configure the appearance and behaviour of the webview by configuring the associated *Client Application* in the console:  | Key | Format | Description | | - | - | - | | `primary_color` | String | Optional. An accent color (hexadecimal string without '#' prefix) to personalize the UI elements of the webview. If absent, the default color is grey. | | `redirect_uri` | String | Optional. A recommended security whitelist configuration. The `redirect_uri` parameter sent to any endpoint of the webview is checked against the configuration, if any. | | `config.disable_connector_hints` | Boolean | Optional. This flags hides the list of most-used entries in the connector selection step. The default is `false`, i.e. the list is shown. | | `config.use_app_layout` | Boolean | Optional. Use this flag to enable presenting your log as an app icon. The default value is ` false`, i.e. the logo is shown in the top bar of the UI. | | `config.disable_accounts_pre_check` | Boolean | Optional. An optional boolean flag to prevent bank accounts to be automatically pre-checked when the user enters the activation step. The default value is ` false`, i.e. the bank accounts are pre-checked. |  #### Endpoints reference  ##### Add connection flow ``` https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/connect ```  This flow allows an end-user to add a new connection to the API. The flow handles the following steps: - selecting a connector; - authenticating & authorizing with the connector, by collecting credentials or delegating; - managing consent to aggregate accounts/subscriptions; - collecting required information for professional accounts.  ###### Endpoint parameters  | Parameter | Description | | - | - | | `client_id` | Required. The ID of the requesting client application. You can manage client applications of your domain in the admin console. | | `redirect_uri` | Required. An absolute callback URI. The webview will redirect to it at the end of the flow. | | `code` | Optional. A user-scoped temporary code to use with the Budgea API.<br>If you don't provide a code, a new anonymous user will be created before the connection is added, and you will be returned an access token code scoped to it with the success callback. | | `state` | Optional. An opaque string parameter that you can use to carry state across the flow. The parameter will be set \"as is\" on the callback URI. Make sure that the `state` you provide is properly URL-encoded. | | `connector_ids` | Optional. A comma-separated list of connector IDs available to pick from.<br>If the parameter is omitted, all active connectors are available.<br>If you pass a single value, the user is not prompted to choose the connector.<br>This parameter is mutually exclusive with `connector_uuids`. | | `connector_uuids` | Optional. A comma-separated list of connector UUIDs available to pick from.<br>If the parameter is omitted, all active connectors are available.<br>If you pass a single value, the user is not prompted to choose the connector.<br>This parameter is mutually exclusive with `connector_ids`. | | `connector_capabilities` | Optional. A comma-separated list of capabilities to filter available connectors.<br>If the parameter is omitted, `bank` is inferred.<br>If multiple values are provided, only connectors that expose all the requested capabilities are available.<br>To request a bank connection, use `bank`.<br>To request a provider connection, use `document`. | | `account_ibans` | Optional. A comma-separated list of IBANs to filter accounts available for activation in a bank connection context. Other accounts will not be selectable. | | `account_types` | Optional. A comma-separated list of account types to filter accounts available for activation in a bank connection context. Other accounts will not be selectable. | | `account_usages` | Optional. A comma-separated list of account usages to filter accounts available for activation in a bank connection context. Other accounts will not be selectable. |  ###### Successful callback parameters  | Parameter | Description | | - | - | | `connection_id` | The id of the newly created connection. Please note that when redirecting to the callback URI, the accounts and/or subscriptions are available in the API, but bank transactions or documents may still be syncing in background. | | `code` | Optional. If a `code` was *not* initially specified, an API code that you must exchange to obtain a permanent access token associated with the newly-created anonymous user holding the connection. The parameter is URL-encoded, make sure to handle it accordingly. | | `state` | Optional. Identical to the `state` parameter that was initially specified. |  ###### Additional error codes  | Code | Description | | - | - | | `tos_declined` | The end-user refused to validate the terms of service. |  ##### Re-auth / edit connection credentials flow  ``` https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/reconnect ```  This flow allows an end-user to re-authenticate against a bank or a provider in order to recover an existing connection, or to completely reset credentials associated with a connection.  ###### Endpoint parameters  | Parameter | Description | | - | - | | `client_id` | Required. The ID of the requesting client application. You can manage client applications of your domain in the admin console. | | `redirect_uri` | Required. An absolute callback URI. The webview will redirect to it at the end of the flow. | | `code` | Required. A user-scoped temporary code to use with the Budgea API. | | `connection_id` | Required. The id of the existing connection. | | `state` | Optional. An opaque string parameter that you can use to carry state across the flow. The parameter will be set \"as is\" on the callback URI. Make sure that the `state` you provide is properly URL-encoded. | | `reset_credentials` | Optional. In the default mode (`false`), the service will try to recover the connection and prompt the user only with outdated or transient information (new password, OTP...).<br>Set the parameter to `true` to force resetting all the credentials associated with the connection. This parameter may not apply to all connectors. |  ###### Successful callback parameters  This flow adds no parameter to the callback URI in case of success, except from `state`.  ##### Manage connections  ``` https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/manage ``` This flow allows an end-user to manage the connections associated with his account in the API. The user can add new connections, remove existing ones, fix connection errors, reset credentials or activate/deactivate bank accounts.  Support of `redirect_uri` in this flow is optional, as it can be integrated or presented as a terminal step, without relying on a final redirection.  ###### Endpoint parameters  | Parameter | Description | | - | - | | `client_id` | Required. The ID of the requesting client application. You can manage client applications of your domain in the admin console. | | `code` | Required. A user-scoped temporary code to use with the Budgea API. | | `redirect_uri` | Optional. An absolute callback URI. When provided, the webview will display a close button that redirects to it. | | `state` | Optional. An opaque string parameter that you can use to carry state across the flow when providing a `redirect_uri`. The parameter will be set \"as is\" on the callback URI. Make sure that the `state` you provide is properly URL-encoded. | | `connector_capabilities` | Optional. A comma-separated list of capabilities to filter available connectors when adding a new connection.<br>If the parameter is omitted, `bank` is inferred.<br>If multiple values are provided, only connectors that expose all the requested capabilities are available.<br>To request a bank connection, use `bank`.<br>To request a provider connection, use `document`. | | `account_types` | Optional. A comma-separated list of account types to filter accounts available for activation on adding a new bank connection or updating existing connections. Other accounts will not be selectable. | | `account_usages` | Optional. A comma-separated list of account usages to filter accounts available for activation in a bank connection context. Other accounts will not be selectable. |  ###### Callback parameters  This flow adds no parameter to the callback URI, except from `state`.  ##### Execute a bank transfer (preview)  **Disclaimer**: Transfer or payment services are available as a preview, protocols and parameters are subject to change in upcoming beta/final releases.  ``` https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/transfer ``` This flow allows an end-user to execute a bank transfer. The flow handles the following steps: - if the transfer is not already created, all steps to authenticate with a bank, select the recipient, the emitter account, the amount and label; - executing the transfer, including managing SCAs for recipient registration and/or transfer validation.  ###### Endpoint parameters  | Parameter | Description | | - | - | | `client_id` | Required. The ID of the requesting client application. You can manage client applications of your domain in the admin console. | | `redirect_uri` | Required. An absolute callback URI. The webview will redirect to it at the end of the flow. | | `code` | Required. A user-scoped temporary code to use with the Budgea API.<br>If you don't provide a code, a new anonymous user will be created before a connection is added and the transfer is executed, and you will be returned an access token code scoped to it with the success callback. | | `state` | Optional. An opaque string parameter that you can use to carry state across the flow. The parameter will be set \"as is\" on the callback URI. Make sure that the `state` you provide is properly URL-encoded. | | `transfer_id`| Optional. The ID of an prepared transfer to be validated in the webview. The user cannot edit anything on the transfer before validation. |  ###### Successfull callback parameters  | Parameter | Description | | - | - | | `transfer_id` | The ID of the transfer that was created and executed. | | `code` | Optional. If a `code` was *not* initially specified, an API code that you can exchange to obtain a permanent access token associated with the newly-created anonymous user holding the transfer. The parameter is URL-encoded, make sure to handle it accordingly. | | `state` | Optional. Identical to the `state` parameter that was initially specified. |  ###### Additional error codes  | Code | Description | | - | - | | `tos_declined` | The end-user refused to validate the terms of service. |  #### Migrating from v3  We provide a full backward compatibility layer with current implementations of the webview v3 to ease the transition. All endpoints remains accessible, with the same parameters and callback behaviour. Migration instructions are provided below.  *The v3 compatibility mode is expected to be removed on 31 December 2019.* You should migrate your implementation a soon as possible to new endpoints and parameters.  ##### Add connection flow / Edit connection credentials   ``` /connect/select ```  This endpoint has been superseded by `/connect` (no suffix) for adding a new connection, and `/reconnect` for resetting or updating an existing connection.  | Endpoint parameter | Migration instructions | | - | - | | `client_id` | No change. | | `redirect_uri`, `state` | No change. | | `response_type` | This parameter is not used anymore. | | `id_connector`, `connectors` | Superseded by `connector_ids` sent to the `/connect` endpoint. | | `types` | Superseded by `connector_capabilities` sent to the `/connect` endpoint.<br>Use`connector_capabilities=bank` (bank connection) or `connector_capabilities=document` (provider connection). | | `id_connection` | Superseded by `connection_id` sent to the `/reconnect` endpoint. |  Passing the code or access token as an URL fragment is no longer supported, use the `code` query parameter.  | Callback parameter | Migration instructions | | - | - | | `id_connection` | Superseded by `connection_id`.<br>In the `/reconnect` flow, this parameter is not returned anymore. | | `code` | Still named `code`, but in the `/connect` flow the parameter is now **only** added if an anonymous user was created, i.e. the `code` parameter was **not** provided as a query parameter or fragment.<br>In the `/reconnect` flow, this parameter is not returned anymore. | | `state` | No change. |  ##### Manage connections  ``` /accounts ```  This endpoint has been superseded by `/manage`, that now fully allows users to add/remove connections, reset their credentials or recover from error states.  | Endpoint parameter | Migration instructions | | - | - | | `client_id` | No change. | | `redirect_uri`, `state` | No change, these parameters are now optional. | | `response_type` | This parameter is not used anymore. | | `types` | Superseded by `connector_capabilities`.<br>Use`connector_capabilities=bank` (bank connection) or `connector_capabilities=document` (provider connection). |  Passing the code or access token as an URL fragment is no longer supported, use the `code` query parameter.  | Callback parameter | Migration instructions | | - | - | | `code` | This parameter is not returned anymore. | | `state` | No change. |  ##### Behaviour change  In v3, the `/accounts` flow used to redirect to the `redirect_uri` after a connection addition. This is no longer the case in v4, where redirection is only performed when the user explicitly closes the flow. If you need to perform actions when a connection is added or removed, you should rely on webhooks.  #### Protocol This section describes the protocol used to set bank and provider accounts of a user, in case you don't want to use the webview.  The idea is to call the following services client-side (with AJAX in case of a web application), to ensure the bank and providers credentials will not be sent to your servers.  1. /auth/init ```http POST /auth/init ``` ```json {    \"auth_token\" : \"fBqjMZbYddebUGlkR445JKPA6pCoRaGb\",    \"type\" : \"temporary\",    \"expires_in\" : 1800,    \"id_user\": 1 } ``` This service creates a temporarily token, to use in the \"Authorization\" header in next calls to the API  The returned token has a life-time of 30 minutes, and should be transfered to the API then (cf Permanent Token), so that your server can get a permanent access_token.  It is possible to generate a permanent token immediately, by calling the service with the manage_token, or by supply parameters client_id and client_secret.  2. /banks or /providers ```http GET /banks?expand=fields Authorization: Bearer <token> ``` ```json {    \"hidden\" : false,          \"charged\" : true,          \"name\" : \"American Express\",          \"id\" : 30,          \"fields\" : [             {                \"values\" : [                   {                      \"label\" : \"Particuliers/Professionnels\",                      \"value\" : \"pp\"                   },                   {                      \"value\" : \"ent\",                      \"label\" : \"Entreprises\"                   }                ],                \"label\" : \"Type de compte\",                \"regex\" : null,                \"name\" : \"website\",                \"type\" : \"list\"             },             {                \"type\" : \"password\",                \"label\" : \"Code secret\",                \"name\" : \"password\",                \"regex\" : \"^[0-9]{6}$\"             }          ],       },       ...    ],    \"total\" : 44, } ``` You get a list of connectors, and all associated fields needed to build the form at step 3. You can also use that list to show to your user, all available banks.  3. /users/me/connections Make a POST request and supply the id_bank (ID of the chosen bank) or id_provider (ID of provider), and all requested fields as key/value parameters. For example: ```http POST /users/me/connections Authorization: Bearer <token> -F login=12345678 -F password=123456 -F id_bank=59 ``` You can get the following return codes:  |Code           |Description                                                  | |---------------|------------------------------------------------------------ | |200            |The connection has succeed and has been created              | |202            |It is necessary to provide complementary information. This occurs on the first connection on some kind of Boursorama accounts for example, where a SMS is sent to the customer. It is necessary to ask the user to fill fields requested in the fields, and do a POST again on /users/me/connections/ID, with the connection ID in id_connection. | |400            |Unable to connect to the website, the field error in the JSON can be **websiteUnavailable** or **wrongpass**  | |403            |Invalid token                                                |  4. Activate accounts The accounts the user wants to aggregate must be activated before any transaction or investment is retrieved. Several accounts can be activated in 1 request by separating the account ids with commas. ```http PUT /users/me/connections/<id_connection>/accounts/<id_account>?all ```  5. Permanent token If the user validates the share of his accounts, it is necessary to transform the temporary code to a permanent access_token (so that the user won't expire).  To do that, make a POST request on /auth/token/access with the following parameters: |Parameter            |Description                                                     | |---------------------|----------------------------------------------------------------| |code                 |The temporarily token which will let you get the access_token   | |client_id            |The ID of your client application                               | |client_secret        |The secret of your client application                           |  ```json POST /auth/token/access  {    \"client_id\" : 17473055,    \"client_secret\" : \"54tHJHjvodbANVzaRtcLzlHGXQiOgw80\",    \"code\" : \"fBqjMZbYddebUGlkR445JKPA6pCoRaGb\" } ``` ```http HTTP/1.1 200 OK  {    \"access_token\" : \"7wBPuFfb1Hod82f1+KNa0AmrkIuQ3h1G\",    \"token_type\":\"Bearer\" } ```  ### Update accounts Another important call is when a user wants to add/remove connections to banks or providers, or to change the password on one of them, it is advised to give him a temporarily code from the permanent access_token, with the following call (using the access_token as bearer): ```http POST /auth/token/code Authorization: Bearer <token> ``` ```json {    \"code\" : \"/JiDppWgbmc+5ztHIUJtHl0ynYfw682Z\",    \"type\" : \"temporary\",    \"expires_in\" : 1800, } ``` Its life-time is 30 minutes, and let the browser to list connections and accounts, via `GET /users/me/connections?expand=accounts` for example.   To update the password of a connection, you can do a POST on the *connection* resource, with the field *password* in the data. The new credentials are checked to make sure they are valid, and the return codes are the same as when adding a connection.  ## Getting the data (Webhooks) You have created your users and their connections, now it's time to get the data. There are 2 ways to retrieve it, the 2 can be complementary: - make regular calls to the API - use the webhooks (recommended)  ### Manual Synchronization It is possible to do a manual synchronization of a user. We recommend to use this method in case the user wants fresh data after logging in.  To trigger the synchronization, call the API as below: `PUT /users/ID/connections` The following call is blocking until the synchronization is terminated.  Even if it is not recommended, it's possible to fetch synchronously new data. To do that, you can use the *expand* parameter: ` /users/ID/connections?expand=accounts[transactions,investments[type]],subscriptions` ```json {    \"connections\" : [       {          \"accounts\" : [             {                \"balance\" : 7481.01,                \"currency\" : {                   \"symbol\" : \"€\",                   \"id\" : \"EUR\",                   \"prefix\" : false                },                \"deleted\" : null,                \"display\" : true,                \"formatted_balance\" : \"7 481,01 €\",                \"iban\" : \"FR76131048379405300290000016\",                \"id\" : 17,                \"id_connection\" : 7,                \"investments\" : [                   {                      \"code\" : \"FR0010330902\",                      \"description\" : \"\",                      \"diff\" : -67.86,                      \"id\" : 55,                      \"id_account\" : 19,                      \"id_type\" : 1,                      \"label\" : \"Agressor PEA\",                      \"portfolio_share\" : 0.48,                      \"prev_diff\" : 2019.57,                      \"quantity\" : 7.338,                      \"type\" : {                         \"color\" : \"AABBCC\",                         \"id\" : 1,                         \"name\" : \"Fonds action\"                      },                      \"unitprice\" : 488.98,                      \"unitvalue\" : 479.73,                      \"valuation\" : 3520.28                   }                ],                \"last_update\" : \"2015-07-04 15:17:30\",                \"name\" : \"Compte chèque\",                \"number\" : \"3002900000\",                \"transactions\" : [                   {                      \"active\" : true,                      \"application_date\" : \"2015-06-17\",                      \"coming\" : false,                      \"comment\" : null,                      \"commission\" : null,                      \"country\" : null,                      \"date\" : \"2015-06-18\",                      \"date_scraped\" : \"2015-07-04 15:17:30\",                      \"deleted\" : null,                      \"documents_count\" : 0,                      \"formatted_value\" : \"-16,22 €\",                      \"id\" : 309,                      \"id_account\" : 17,                      \"id_category\" : 9998,                      \"id_cluster\" : null,                      \"last_update\" : \"2015-07-04 15:17:30\",                      \"new\" : true,                      \"original_currency\" : null,                      \"original_value\" : null,                      \"original_wording\" : \"FACTURE CB HALL'S BEER\",                      \"rdate\" : \"2015-06-17\",                      \"simplified_wording\" : \"HALL'S BEER\",                      \"state\" : \"parsed\",                      \"stemmed_wording\" : \"HALL'S BEER\",                      \"type\" : \"card\",                      \"value\" : -16.22,                      \"wording\" : \"HALL'S BEER\"                   }                ],                \"type\" : \"checking\"             }          ],          \"error\" : null,          \"expire\" : null,          \"id\" : 7,          \"id_user\" : 7,          \"id_bank\" : 41,          \"last_update\" : \"2015-07-04 15:17:31\"       }    ],    \"total\" : 1, } ```  ### Background synchronizations & Webhooks Webhooks are callbacks sent to your server, when an event is triggered during a synchronization. Synchronizations are automatic, the frequency can be set using the configuration key `autosync.frequency`. Using webhooks allows you to get the most up-to-date data of your users, after each synchronization.  The automatic synchronization makes it possible to recover new bank entries, or new invoices, at a given frequency. You have the possibility to add webhooks on several events, and choose to receive each one on a distinct URL. To see the list of available webhooks you can call the endpoint hereunder: ``` curl https://demo.biapi.pro/2.0/webhooks_events \\   -H 'Authorization: Bearer <token>' ```  The background synchronizations for each user are independent, and their plannings are spread over the day so that they do not overload any website.  Once the synchronization of a user is over, a POST request is sent on the callback URL you have defined, including all webhook data. A typical json sent to your server is as below: ```http POST /callback HTTP/1.1 Host: example.org Content-Length: 959 Accept-Encoding: gzip, deflate, compress Accept: */* User-Agent: Budgea API/2.0 Content-Type: application/json; charset=utf-8 Authorization: Bearer sl/wuqgD2eOo+4Zf9FjvAz3YJgU+JKsJ  {    \"connections\" : [       {          \"accounts\" : [             {                \"balance\" : 7481.01,                \"currency\" : {                   \"symbol\" : \"€\",                   \"id\" : \"EUR\",                   \"prefix\" : false                },                \"deleted\" : null,                \"display\" : true,                \"formatted_balance\" : \"7 481,01 €\",                \"iban\" : \"FR76131048379405300290000016\",                \"id\" : 17,                \"id_connection\" : 7,                \"investments\" : [                   {                      \"code\" : \"FR0010330902\",                      \"description\" : \"\",                      \"diff\" : -67.86,                      \"id\" : 55,                      \"id_account\" : 19,                      \"id_type\" : 1,                      \"label\" : \"Agressor PEA\",                      \"portfolio_share\" : 0.48,                      \"prev_diff\" : 2019.57,                      \"quantity\" : 7.338,                      \"type\" : {                         \"color\" : \"AABBCC\",                         \"id\" : 1,                         \"name\" : \"Fonds action\"                      },                      \"unitprice\" : 488.98,                      \"unitvalue\" : 479.73,                      \"valuation\" : 3520.28                   }                ],                \"last_update\" : \"2015-07-04 15:17:30\",                \"name\" : \"Compte chèque\",                \"number\" : \"3002900000\",                \"transactions\" : [                   {                      \"active\" : true,                      \"application_date\" : \"2015-06-17\",                      \"coming\" : false,                      \"comment\" : null,                      \"commission\" : null,                      \"country\" : null,                      \"date\" : \"2015-06-18\",                      \"date_scraped\" : \"2015-07-04 15:17:30\",                      \"deleted\" : null,                      \"documents_count\" : 0,                      \"formatted_value\" : \"-16,22 €\",                      \"id\" : 309,                      \"id_account\" : 17,                      \"id_category\" : 9998,                      \"id_cluster\" : null,                      \"last_update\" : \"2015-07-04 15:17:30\",                      \"new\" : true,                      \"original_currency\" : null,                      \"original_value\" : null,                      \"original_wording\" : \"FACTURE CB HALL'S BEER\",                      \"rdate\" : \"2015-06-17\",                      \"simplified_wording\" : \"HALL'S BEER\",                      \"state\" : \"parsed\",                      \"stemmed_wording\" : \"HALL'S BEER\",                      \"type\" : \"card\",                      \"value\" : -16.22,                      \"wording\" : \"HALL'S BEER\"                   }                ],                \"type\" : \"checking\"             }          ],          \"bank\" : {             \"id_weboob\" : \"ing\",             \"charged\" : true,             \"name\" : \"ING Direct\",             \"id\" : 7,             \"hidden\" : false          },          \"error\" : null,          \"expire\" : null,          \"id\" : 7,          \"id_user\" : 7,          \"id_bank\" : 41,          \"last_update\" : \"2015-07-04 15:17:31\"       }    ],    \"total\" : 1,    \"user\" : {       \"signin\" : \"2015-07-04 15:17:29\",       \"id\" : 7,       \"platform\" : \"sharedAccess\"    } } ``` The authentication on the callback is made with the access_token of the user (which is a shared secret between your server and the Budgea API).  When you are in production, it is needed to define a HTTPS URL using a valid certificate, delivered by a recognized authority. If this is not the case, you can contact us to add your CA (Certificate Authority) to our PKI (Public Key Infrastructure).  Important: it is necessary to send back a HTTP 200 code, without what we consider that data is not correctly taken into account on your system, and it will be sent again at the next user synchronization.  ## Guidelines for production Now you should have integrated the API inside your application. Make sure your Webhooks URLs are in HTTPS, if so you can enable the production state of the API.  To make things great, here are some good practices, please check you have respected them: - You have provided to your users a way to configure their accounts - You have provided to your users a way to change their account passwords - You consider the **error** field of Connections, to alert the user in case the state is **wrongpass** - You map IDs of Accounts, Subscriptions, Transactions and Documents in your application, to be sure to correctly match them - When the deleted field is set on a bank transaction, you delete it in your database - You don't loop on all users to launch synchronizations, this might saturate the service  If you have questions about above points, please contact us. Otherwise, you can put into production!  ### Going further If you want to raise the bar for your app and add features such as the ability to do transfers, get invoices, aggregate patrimony and more, please refer to the sections below. We'll discuss complementary APIs building upon the aggregation, allowing for the best of financial apps.  ## Budgea API Pay This API allows for the emition of transfers between the aggregated accounts. Just like the simple aggregation, BI provides a webview or a protocol to follow, to implement this feature.  ### API pay protocol This section describes how the transfer and recipient protocol work, in case you don't want to integrate the webview. The idea is to do following calls client side (with AJAX in case of a web application), so that the interaction with the Budgea API is transparent.  #### Executing a transfer 1. /auth/token/code If you do calls client side, get a new temporary code for the user, from the access_token. This will prevent security issues. ``` curl -d '' \\   https://demo.biapi.pro/2.0/auth/token/code \\   -H 'Authorization: Bearer <token>' ``` ```json {    \"code\": \"/JiDppWgbmc+5ztHIUJtHl0ynYfw682Z\",    \"type\": \"temporary\",    \"expires_in\": 1800 } ``` The returned token has a life-time of 30 minutes.  2. /users/me/accounts?able_to_transfer=1 List all the accounts that can do transfers. Authenticate the call with the code you got at step 1. ``` curl https://demo.biapi.pro/2.0/users/me/accounts?able_to_transfer=1 \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' ``` ```json {   \"accounts\" : [       {          \"display\" : true,          \"balance\" : 2893.36,          \"id_type\" : 2,          \"number\" : \"****1572\",          \"type\" : \"checking\",          \"deleted\" : null,          \"bic\" : \"BNPAFRPPXXX\",          \"bookmarked\" : false,          \"coming\" : -2702.74,          \"id_user\" : 1,          \"original_name\" : \"Compte de chèques\",          \"currency\" : {             \"symbol\" : \"€\",             \"id\" : \"EUR\",             \"prefix\" : false          },          \"name\" : \"lol\",          \"iban\" : \"FR7630004012550000041157244\",          \"last_update\" : \"2016-12-28 12:31:04\",          \"id\" : 723,          \"formatted_balance\" : \"2893,36 €\",          \"able_to_transfer\" : true,          \"id_connection\" : 202       }    ],    \"total\" : 1 } ```  3. /users/me/accounts/ID/recipients List all available recipients for a given account. ``` curl https://demo.biapi.pro/2.0/users/me/accounts/723/recipients?limit=1 \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' ``` ```json {   \"total\" : 27,    \"recipients\" : [       {          \"bank_name\" : \"BNP PARIBAS\",          \"bic\" : \"BNPAFRPPXXX\",          \"category\" : \"Interne\",          \"deleted\" : null,          \"enabled_at\" : \"2016-10-31 18:52:53\",          \"expire\" : null,          \"iban\" : \"FR7630004012550003027641744\",          \"id\" : 1,          \"id_account\" : 1,          \"id_target_account\" : 2,          \"label\" : \"Livret A\",          \"last_update\" : \"2016-12-05 12:07:24\",          \"time_scraped\" : \"2016-10-31 18:52:54\",          \"webid\" : \"2741588268268091098819849694548441184167285851255682796371\"       }    ] } ```  4. /users/me/accounts/ID/recipients/ID/transfers Create the transfer ``` curl \\   https://demo.biapi.pro/2.0/users/me/accounts/1/recipients/1/transfers \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' \\   -F amount=10, \\   -F label=\"Test virement\", \\   -F exec_date=\"2018-09-12\" // optional ``` ```json {    \"account_iban\" : \"FR7630004012550000041157244\",    \"amount\" : 10,    \"currency\" : {       \"id\" : \"EUR\",       \"prefix\" : false,       \"symbol\" : \"€\"    },    \"exec_date\" : \"2018-09-12\",    \"fees\" : null    \"formatted_amount\" : \"10,00 €\",    \"id\" : 22,    \"id_account\" : 1,,    \"id_recipient\" : 1,    \"label\" : \"Test virement\",    \"recipient_iban\" : \"FR7630004012550003027641744\",    \"register_date\" : \"2018-09-12 10:34:59\",    \"state\" : \"created\",    \"webid\" : null } ```  5. /users/me/transfers/ID Execute the transfer ``` curl \\   https://demo.biapi.pro/2.0/users/me/transfers/22 \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' \\   -F validated=true ``` ```json {    \"account_iban\" : \"FR7630004012550000041157244\",    \"amount\" : 10,    \"currency\" : {       \"id\" : \"EUR\",       \"prefix\" : false,       \"symbol\" : \"€\"    },    \"exec_date\" : \"2016-12-19\",    \"fees\" : null,    \"fields\" : [       {          \"label\" : \"Code secret BNP Paribas\",          \"type\" : \"password\",          \"regex\" : \"^[0-9]{6}$\",          \"name\" : \"password\"       }    ],    \"formatted_amount\" : \"10,00 €\",    \"id\" : 22,    \"id_account\" : 1,    \"id_recipient\" : 1,    \"label\" : \"Test virement\",    \"recipient_iban\" : \"FR7630004012550003027641744\",    \"register_date\" : \"2016-12-19 10:34:59\",    \"state\" : \"created\",    \"webid\" : null } ``` Here, an authentication step asks user to enter his bank password. The transfer can be validated with:  ``` curl \\   https://demo.biapi.pro/2.0/users/me/transfers/22 \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' \\   -F validated=true \\   -F password=\"123456\" ``` ```json {    \"account_iban\" : \"FR7630004012550000041157244\",    \"currency\" : {       \"id\" : \"EUR\",       \"prefix\" : false,       \"symbol\" : \"€\"    },    \"amount\" : 10,    \"exec_date\" : \"2016-12-19\",    \"fees\" : 0,    \"formatted_amount\" : \"10,00 €\",    \"id\" : 22,    \"id_account\" : 1,    \"id_recipient\" : 1,    \"label\" : \"Test virement\",    \"recipient_iban\" : \"FR7630004012550003027641744\",    \"register_date\" : \"2016-12-19 10:34:59\",    \"state\" : \"pending\",    \"webid\" : \"ZZ10C4FKSNP05TK95\" } ``` The field state is changed to *pending*, telling that the transfer has been correctly executed on the bank. A connection synchronization is then launched, to find the bank transaction in the movements history. In this case, the transfer state will be changed to *done*.  #### Adding a recipient 1. /auth/token/code Get a temporary token for the user. Same procedure than step 1 for a transfer.  2. /users/me/accounts?able_to_transfer=1 List accounts allowing transfers. Same procedure than step 2 for a transfer.  3. /users/me/accounts/ID/recipients/ Add a new recipient. ``` curl \\   https://demo.biapi.pro/2.0/users/me/accounts/1/recipients \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' \\   -F iban=FR7613048379405300290000355 \\   -F label=\"Papa\", \\   -F category=\"Famille\" // optional ``` ```json {    \"bank_name\" : \"BNP PARIBAS\",    \"bic\" : \"BNPAFRPPXXX\",    \"category\" : \"Famille\",    \"deleted\" : null,    \"enabled_at\" : null,    \"expire\" : \"2017-04-29 16:56:20\",    \"fields\" : [       {          \"label\" : \"Veuillez entrer le code reçu par SMS\",          \"type\" : \"password\",          \"regex\" : \"^[0-9]{6}$\",          \"name\" : \"sms\"       }    ],    \"iban\" : \"FR7613048379405300290000355\",    \"id\" : 2,    \"id_account\" : 1,    \"id_target_account\" : null,    \"label\" : \"Papa\",    \"last_update\" : \"2017-04-29 16:26:20\",    \"time_scraped\" : null,    \"webid\" : null } ``` It is necessary to post on the object Recipient with the requested fields (here sms), until the add is validated: ``` curl \\   https://demo.biapi.pro/2.0/users/me/accounts/1/recipients/2 \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' \\   -F sms=\"123456\" ``` ```json {    \"bank_name\" : \"BNP PARIBAS\",    \"bic\" : \"BNPAFRPPXXX\",    \"category\" : \"Famille\",    \"deleted\" : null,    \"enabled_at\" : \"2017-05-01 00:00:00\",    \"expire\" : null,    \"iban\" : \"FR7613048379405300290000355\",    \"id\" : 2,    \"id_account\" : 1,    \"id_target_account\" : null,    \"label\" : \"Papa\",    \"last_update\" : \"2017-04-29 16:26:20\",    \"time_scraped\" : null,    \"webid\" : \"2741588268268091098819849694548441184167285851255682796371\" } ``` If the field enabled_at is in the future, it means that it isn't possible yet to execute a transfer, as the bank requires to wait a validation period.  ### API Pay Webview This section describes how to integrate the webview of the Budgea Pay API inside your application, to let your users do transfers to their recipients.  #### User redirection To redirect the user to the webview, it is necessary to build a URI authenticated with a temporary token. This can be done from our library, or by calling the endpoint `/auth/token/code` (see the protocol section for an example). If the parameter **redirect_uri** is supplied, the user will be redirected to that page once the transfer is done.  #### List of pages Here are a list a pages you may call to redirect your user directly on a page of the process: |Path                                 |Description of the page                                                           | |-------------------------------------|----------------------------------------------------------------------------------| |/transfers                           |List Transfers                                                                    | |/transfers/accounts                  |List emitter accounts                                                             | |/transfers/accounts/id/recipients    |List recipients                                                                   | |/transfers/accounts/id/recipients/id |Initialization of a transfer between the account and the recipient                | |/transfers/id                        |Detail of a given transfer                                                        |  ## Deprecated  This section lists all the deprecated features in Budgea API. The associated date is the date of its removal. **Do not use them**.  ### Key Investments (**2019-06-24**)  Adding a temporary new key \"all_investments\" that will include deleted investments in the **webhooks**.  ### No automatic expand on User objects (**2019-07-30**) In the API responses, by default, User objects won't display the keys \"config\", \"alert_settings\" and \"invites\" anymore. You will still be able to access this data by expanding the request. Example: GET /users/me/?expand=alert_settings,config  ### Renaming of \"type\" field for jwt tokens (**2019-07-30**) For user's tokens in the jwt format, the \"type\" field will be renamed from \"shared_access\" to \"sharedAccess\".   # noqa: E501

    The version of the OpenAPI document: 2.0
    Contact: rienafairefr@gmail.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from budgea.api_client import ApiClient
from budgea.exceptions import (
    ApiTypeError,
    ApiValueError
)


class AdministrationApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def clients_get(self, **kwargs):  # noqa: E501
        """List clients  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Merchants
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.clients_get_with_http_info(**kwargs)  # noqa: E501

    def clients_get_with_http_info(self, **kwargs):  # noqa: E501
        """List clients  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Merchants, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method clients_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/clients', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Merchants',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def clients_id_client_delete(self, id_client, **kwargs):  # noqa: E501
        """Delete a client  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_id_client_delete(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Client
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.clients_id_client_delete_with_http_info(id_client, **kwargs)  # noqa: E501

    def clients_id_client_delete_with_http_info(self, id_client, **kwargs):  # noqa: E501
        """Delete a client  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_id_client_delete_with_http_info(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Client, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_client', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method clients_id_client_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_client' is set
        if ('id_client' not in local_var_params or
                local_var_params['id_client'] is None):
            raise ApiValueError("Missing the required parameter `id_client` when calling `clients_id_client_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_client' in local_var_params:
            path_params['id_client'] = local_var_params['id_client']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/clients/{id_client}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Client',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def clients_id_client_get(self, id_client, **kwargs):  # noqa: E501
        """Get information about a client  # noqa: E501

        If you use the manage_token or a configuration token, you will get also the client secret.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_id_client_get(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Client
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.clients_id_client_get_with_http_info(id_client, **kwargs)  # noqa: E501

    def clients_id_client_get_with_http_info(self, id_client, **kwargs):  # noqa: E501
        """Get information about a client  # noqa: E501

        If you use the manage_token or a configuration token, you will get also the client secret.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_id_client_get_with_http_info(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Client, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_client', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method clients_id_client_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_client' is set
        if ('id_client' not in local_var_params or
                local_var_params['id_client'] is None):
            raise ApiValueError("Missing the required parameter `id_client` when calling `clients_id_client_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_client' in local_var_params:
            path_params['id_client'] = local_var_params['id_client']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/clients/{id_client}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Client',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def clients_id_client_logo_delete(self, id_client, **kwargs):  # noqa: E501
        """Delete the client logo  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_id_client_logo_delete(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: File
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.clients_id_client_logo_delete_with_http_info(id_client, **kwargs)  # noqa: E501

    def clients_id_client_logo_delete_with_http_info(self, id_client, **kwargs):  # noqa: E501
        """Delete the client logo  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_id_client_logo_delete_with_http_info(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(File, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_client', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method clients_id_client_logo_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_client' is set
        if ('id_client' not in local_var_params or
                local_var_params['id_client'] is None):
            raise ApiValueError("Missing the required parameter `id_client` when calling `clients_id_client_logo_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_client' in local_var_params:
            path_params['id_client'] = local_var_params['id_client']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/clients/{id_client}/logo', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='File',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def clients_id_client_logo_post(self, id_client, **kwargs):  # noqa: E501
        """Update the client logo  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_id_client_logo_post(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: File
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.clients_id_client_logo_post_with_http_info(id_client, **kwargs)  # noqa: E501

    def clients_id_client_logo_post_with_http_info(self, id_client, **kwargs):  # noqa: E501
        """Update the client logo  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_id_client_logo_post_with_http_info(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(File, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_client', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method clients_id_client_logo_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_client' is set
        if ('id_client' not in local_var_params or
                local_var_params['id_client'] is None):
            raise ApiValueError("Missing the required parameter `id_client` when calling `clients_id_client_logo_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_client' in local_var_params:
            path_params['id_client'] = local_var_params['id_client']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/clients/{id_client}/logo', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='File',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def clients_id_client_put(self, id_client, **kwargs):  # noqa: E501
        """Update a client  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_id_client_put(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param str config: custom config about the client
        :param str description: text to display as a default description
        :param str description_banks: text to display as a description for banks
        :param str description_providers: text to display as a description for providers
        :param bool generate_keys: set a rsa key pair for the client, which make it possible to generate a jwt user token using this client. No effect if the client already has a set of keys(default: False)
        :param str name: name of client
        :param str primary_color: hexadecimal code of the client primary color (e.g F45B9A)
        :param bool pro: Wether the client should display the company manager page
        :param str redirect_uris: list of allowed redirect uris
        :param str secondary_color: hexadecimal code of the client secondary color (e.g F45B9A)
        :param bool secret: reset the secret
        :param bool update_config: update the custom information about the client instead of replacing the existing one (default: True)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Client
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.clients_id_client_put_with_http_info(id_client, **kwargs)  # noqa: E501

    def clients_id_client_put_with_http_info(self, id_client, **kwargs):  # noqa: E501
        """Update a client  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_id_client_put_with_http_info(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param str config: custom config about the client
        :param str description: text to display as a default description
        :param str description_banks: text to display as a description for banks
        :param str description_providers: text to display as a description for providers
        :param bool generate_keys: set a rsa key pair for the client, which make it possible to generate a jwt user token using this client. No effect if the client already has a set of keys(default: False)
        :param str name: name of client
        :param str primary_color: hexadecimal code of the client primary color (e.g F45B9A)
        :param bool pro: Wether the client should display the company manager page
        :param str redirect_uris: list of allowed redirect uris
        :param str secondary_color: hexadecimal code of the client secondary color (e.g F45B9A)
        :param bool secret: reset the secret
        :param bool update_config: update the custom information about the client instead of replacing the existing one (default: True)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Client, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_client', 'expand', 'config', 'description', 'description_banks', 'description_providers', 'generate_keys', 'name', 'primary_color', 'pro', 'redirect_uris', 'secondary_color', 'secret', 'update_config']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method clients_id_client_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_client' is set
        if ('id_client' not in local_var_params or
                local_var_params['id_client'] is None):
            raise ApiValueError("Missing the required parameter `id_client` when calling `clients_id_client_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_client' in local_var_params:
            path_params['id_client'] = local_var_params['id_client']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'config' in local_var_params:
            form_params.append(('config', local_var_params['config']))  # noqa: E501
        if 'description' in local_var_params:
            form_params.append(('description', local_var_params['description']))  # noqa: E501
        if 'description_banks' in local_var_params:
            form_params.append(('description_banks', local_var_params['description_banks']))  # noqa: E501
        if 'description_providers' in local_var_params:
            form_params.append(('description_providers', local_var_params['description_providers']))  # noqa: E501
        if 'generate_keys' in local_var_params:
            form_params.append(('generate_keys', local_var_params['generate_keys']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'primary_color' in local_var_params:
            form_params.append(('primary_color', local_var_params['primary_color']))  # noqa: E501
        if 'pro' in local_var_params:
            form_params.append(('pro', local_var_params['pro']))  # noqa: E501
        if 'redirect_uris' in local_var_params:
            form_params.append(('redirect_uris', local_var_params['redirect_uris']))  # noqa: E501
        if 'secondary_color' in local_var_params:
            form_params.append(('secondary_color', local_var_params['secondary_color']))  # noqa: E501
        if 'secret' in local_var_params:
            form_params.append(('secret', local_var_params['secret']))  # noqa: E501
        if 'update_config' in local_var_params:
            form_params.append(('update_config', local_var_params['update_config']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/clients/{id_client}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Client',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def clients_post(self, **kwargs):  # noqa: E501
        """Create a client  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param str config: custom config about the client
        :param bool generate_keys: if True, generate a rsa pair of keys so the client can be used to generate jwt user tokens (default: False)
        :param str name: name of client
        :param str redirect_uris: list of allowed redirect uris
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Client
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.clients_post_with_http_info(**kwargs)  # noqa: E501

    def clients_post_with_http_info(self, **kwargs):  # noqa: E501
        """Create a client  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clients_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param str config: custom config about the client
        :param bool generate_keys: if True, generate a rsa pair of keys so the client can be used to generate jwt user tokens (default: False)
        :param str name: name of client
        :param str redirect_uris: list of allowed redirect uris
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Client, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['expand', 'config', 'generate_keys', 'name', 'redirect_uris']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method clients_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'config' in local_var_params:
            form_params.append(('config', local_var_params['config']))  # noqa: E501
        if 'generate_keys' in local_var_params:
            form_params.append(('generate_keys', local_var_params['generate_keys']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'redirect_uris' in local_var_params:
            form_params.append(('redirect_uris', local_var_params['redirect_uris']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/clients', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Client',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def config_get(self, **kwargs):  # noqa: E501
        """Get configuration of the API.  # noqa: E501

        <br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.config_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str search: limit the results to keys matching the given value
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.config_get_with_http_info(**kwargs)  # noqa: E501

    def config_get_with_http_info(self, **kwargs):  # noqa: E501
        """Get configuration of the API.  # noqa: E501

        <br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.config_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str search: limit the results to keys matching the given value
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['search']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method config_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'search' in local_var_params:
            query_params.append(('search', local_var_params['search']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/config', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def config_logs_get(self, **kwargs):  # noqa: E501
        """Get configuration change history of the API.  # noqa: E501

        <br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.config_logs_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str search: limit the results to keys matching the given value
        :param str type: type of change done on the configuration
        :param date min_date: minimal date of the change
        :param date max_date: maximum date of the change
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConfigLogs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.config_logs_get_with_http_info(**kwargs)  # noqa: E501

    def config_logs_get_with_http_info(self, **kwargs):  # noqa: E501
        """Get configuration change history of the API.  # noqa: E501

        <br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.config_logs_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str search: limit the results to keys matching the given value
        :param str type: type of change done on the configuration
        :param date min_date: minimal date of the change
        :param date max_date: maximum date of the change
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ConfigLogs, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['search', 'type', 'min_date', 'max_date', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method config_logs_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'search' in local_var_params:
            query_params.append(('search', local_var_params['search']))  # noqa: E501
        if 'type' in local_var_params:
            query_params.append(('type', local_var_params['type']))  # noqa: E501
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/config/logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConfigLogs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def config_post(self, **kwargs):  # noqa: E501
        """Set a configuration value on the API.  # noqa: E501

        Request: { \"connection.disable_new\": \"0\", \"search\": \"connection.disable_new\" }<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.config_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str search: limit the results to keys matching the given value
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.config_post_with_http_info(**kwargs)  # noqa: E501

    def config_post_with_http_info(self, **kwargs):  # noqa: E501
        """Set a configuration value on the API.  # noqa: E501

        Request: { \"connection.disable_new\": \"0\", \"search\": \"connection.disable_new\" }<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.config_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str search: limit the results to keys matching the given value
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(object, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['search']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method config_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'search' in local_var_params:
            query_params.append(('search', local_var_params['search']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/config', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def merchants_get(self, **kwargs):  # noqa: E501
        """List clients  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.merchants_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Merchants
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.merchants_get_with_http_info(**kwargs)  # noqa: E501

    def merchants_get_with_http_info(self, **kwargs):  # noqa: E501
        """List clients  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.merchants_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Merchants, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method merchants_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/merchants', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Merchants',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def merchants_id_client_logo_delete(self, id_client, **kwargs):  # noqa: E501
        """Delete the client logo  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.merchants_id_client_logo_delete(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: File
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.merchants_id_client_logo_delete_with_http_info(id_client, **kwargs)  # noqa: E501

    def merchants_id_client_logo_delete_with_http_info(self, id_client, **kwargs):  # noqa: E501
        """Delete the client logo  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.merchants_id_client_logo_delete_with_http_info(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(File, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_client', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method merchants_id_client_logo_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_client' is set
        if ('id_client' not in local_var_params or
                local_var_params['id_client'] is None):
            raise ApiValueError("Missing the required parameter `id_client` when calling `merchants_id_client_logo_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_client' in local_var_params:
            path_params['id_client'] = local_var_params['id_client']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/merchants/{id_client}/logo', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='File',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def merchants_id_client_logo_post(self, id_client, **kwargs):  # noqa: E501
        """Update the client logo  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.merchants_id_client_logo_post(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: File
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.merchants_id_client_logo_post_with_http_info(id_client, **kwargs)  # noqa: E501

    def merchants_id_client_logo_post_with_http_info(self, id_client, **kwargs):  # noqa: E501
        """Update the client logo  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.merchants_id_client_logo_post_with_http_info(id_client, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_client: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(File, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_client', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method merchants_id_client_logo_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_client' is set
        if ('id_client' not in local_var_params or
                local_var_params['id_client'] is None):
            raise ApiValueError("Missing the required parameter `id_client` when calling `merchants_id_client_logo_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_client' in local_var_params:
            path_params['id_client'] = local_var_params['id_client']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/merchants/{id_client}/logo', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='File',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def merchants_post(self, iban, name, redirect_uris, **kwargs):  # noqa: E501
        """Create a merchant. Needs a user identified in bearer to be used  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.merchants_post(iban, name, redirect_uris, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str iban: payments initiated by this merchant will be done to this IBAN (required)
        :param str name: name of merchant (required)
        :param str redirect_uris: list of allowed redirect uris (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Client
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.merchants_post_with_http_info(iban, name, redirect_uris, **kwargs)  # noqa: E501

    def merchants_post_with_http_info(self, iban, name, redirect_uris, **kwargs):  # noqa: E501
        """Create a merchant. Needs a user identified in bearer to be used  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.merchants_post_with_http_info(iban, name, redirect_uris, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str iban: payments initiated by this merchant will be done to this IBAN (required)
        :param str name: name of merchant (required)
        :param str redirect_uris: list of allowed redirect uris (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Client, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['iban', 'name', 'redirect_uris', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method merchants_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'iban' is set
        if ('iban' not in local_var_params or
                local_var_params['iban'] is None):
            raise ApiValueError("Missing the required parameter `iban` when calling `merchants_post`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in local_var_params or
                local_var_params['name'] is None):
            raise ApiValueError("Missing the required parameter `name` when calling `merchants_post`")  # noqa: E501
        # verify the required parameter 'redirect_uris' is set
        if ('redirect_uris' not in local_var_params or
                local_var_params['redirect_uris'] is None):
            raise ApiValueError("Missing the required parameter `redirect_uris` when calling `merchants_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'iban' in local_var_params:
            form_params.append(('iban', local_var_params['iban']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'redirect_uris' in local_var_params:
            form_params.append(('redirect_uris', local_var_params['redirect_uris']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/merchants', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Client',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def monitoring_get(self, **kwargs):  # noqa: E501
        """get performances stats on this instance  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.monitoring_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int period: number on days on which stats on synchronization have to be done per worker (Default: 1)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.monitoring_get_with_http_info(**kwargs)  # noqa: E501

    def monitoring_get_with_http_info(self, **kwargs):  # noqa: E501
        """get performances stats on this instance  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.monitoring_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int period: number on days on which stats on synchronization have to be done per worker (Default: 1)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['period']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method monitoring_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'period' in local_var_params:
            query_params.append(('period', local_var_params['period']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/monitoring', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def test_sync_post(self, **kwargs):  # noqa: E501
        """Test synchronization on a random connection.  # noqa: E501

        It can be used to test receiving data on your webhooks.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.test_sync_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.test_sync_post_with_http_info(**kwargs)  # noqa: E501

    def test_sync_post_with_http_info(self, **kwargs):  # noqa: E501
        """Test synchronization on a random connection.  # noqa: E501

        It can be used to test receiving data on your webhooks.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.test_sync_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method test_sync_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/test/sync', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def test_webhooks_post(self, **kwargs):  # noqa: E501
        """Test synchronization on a random connection.  # noqa: E501

        It can be used to test receiving data on your webhooks.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.test_webhooks_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.test_webhooks_post_with_http_info(**kwargs)  # noqa: E501

    def test_webhooks_post_with_http_info(self, **kwargs):  # noqa: E501
        """Test synchronization on a random connection.  # noqa: E501

        It can be used to test receiving data on your webhooks.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.test_webhooks_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method test_webhooks_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/test/webhooks', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_auth_delete(self, **kwargs):  # noqa: E501
        """Deletes all webhook authentication types  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_auth_delete(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AuthProvider
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_auth_delete_with_http_info(**kwargs)  # noqa: E501

    def webhooks_auth_delete_with_http_info(self, **kwargs):  # noqa: E501
        """Deletes all webhook authentication types  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_auth_delete_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AuthProvider, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_auth_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/auth', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AuthProvider',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_auth_get(self, **kwargs):  # noqa: E501
        """Get webhooks authentication types  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_auth_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: WebhooksAuth
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_auth_get_with_http_info(**kwargs)  # noqa: E501

    def webhooks_auth_get_with_http_info(self, **kwargs):  # noqa: E501
        """Get webhooks authentication types  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_auth_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(WebhooksAuth, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_auth_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/auth', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WebhooksAuth',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_auth_id_auth_delete(self, id_auth, **kwargs):  # noqa: E501
        """Deletes the webhook authentication type  # noqa: E501

        Updates the deleted field with the date of the deletion<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_auth_id_auth_delete(id_auth, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_auth: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AuthProvider
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_auth_id_auth_delete_with_http_info(id_auth, **kwargs)  # noqa: E501

    def webhooks_auth_id_auth_delete_with_http_info(self, id_auth, **kwargs):  # noqa: E501
        """Deletes the webhook authentication type  # noqa: E501

        Updates the deleted field with the date of the deletion<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_auth_id_auth_delete_with_http_info(id_auth, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_auth: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AuthProvider, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_auth', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_auth_id_auth_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_auth' is set
        if ('id_auth' not in local_var_params or
                local_var_params['id_auth'] is None):
            raise ApiValueError("Missing the required parameter `id_auth` when calling `webhooks_auth_id_auth_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_auth' in local_var_params:
            path_params['id_auth'] = local_var_params['id_auth']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/auth/{id_auth}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AuthProvider',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_auth_id_auth_post(self, id_auth, name, type, **kwargs):  # noqa: E501
        """Updates the webhook authentication type  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_auth_id_auth_post(id_auth, name, type, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_auth: (required)
        :param str name: The name of the authentication process to differentiate (required)
        :param int type: The type of the authentication process (oauth, certificate, token, etc...) (required)
        :param str expand:
        :param str config: The authentication process configuration. A dict containing either the certificate
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AuthProvider
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_auth_id_auth_post_with_http_info(id_auth, name, type, **kwargs)  # noqa: E501

    def webhooks_auth_id_auth_post_with_http_info(self, id_auth, name, type, **kwargs):  # noqa: E501
        """Updates the webhook authentication type  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_auth_id_auth_post_with_http_info(id_auth, name, type, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_auth: (required)
        :param str name: The name of the authentication process to differentiate (required)
        :param int type: The type of the authentication process (oauth, certificate, token, etc...) (required)
        :param str expand:
        :param str config: The authentication process configuration. A dict containing either the certificate
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AuthProvider, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_auth', 'name', 'type', 'expand', 'config']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_auth_id_auth_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_auth' is set
        if ('id_auth' not in local_var_params or
                local_var_params['id_auth'] is None):
            raise ApiValueError("Missing the required parameter `id_auth` when calling `webhooks_auth_id_auth_post`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in local_var_params or
                local_var_params['name'] is None):
            raise ApiValueError("Missing the required parameter `name` when calling `webhooks_auth_id_auth_post`")  # noqa: E501
        # verify the required parameter 'type' is set
        if ('type' not in local_var_params or
                local_var_params['type'] is None):
            raise ApiValueError("Missing the required parameter `type` when calling `webhooks_auth_id_auth_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_auth' in local_var_params:
            path_params['id_auth'] = local_var_params['id_auth']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'config' in local_var_params:
            form_params.append(('config', local_var_params['config']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'type' in local_var_params:
            form_params.append(('type', local_var_params['type']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/auth/{id_auth}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AuthProvider',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_auth_id_auth_put(self, id_auth, name, type, **kwargs):  # noqa: E501
        """Updates the webhook authentication type  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_auth_id_auth_put(id_auth, name, type, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_auth: (required)
        :param str name: The name of the authentication process to differentiate (required)
        :param int type: The type of the authentication process (oauth, certificate, token, etc...) (required)
        :param str expand:
        :param str config: The authentication process configuration. A dict containt either the certificate
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AuthProvider
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_auth_id_auth_put_with_http_info(id_auth, name, type, **kwargs)  # noqa: E501

    def webhooks_auth_id_auth_put_with_http_info(self, id_auth, name, type, **kwargs):  # noqa: E501
        """Updates the webhook authentication type  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_auth_id_auth_put_with_http_info(id_auth, name, type, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_auth: (required)
        :param str name: The name of the authentication process to differentiate (required)
        :param int type: The type of the authentication process (oauth, certificate, token, etc...) (required)
        :param str expand:
        :param str config: The authentication process configuration. A dict containt either the certificate
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AuthProvider, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_auth', 'name', 'type', 'expand', 'config']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_auth_id_auth_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_auth' is set
        if ('id_auth' not in local_var_params or
                local_var_params['id_auth'] is None):
            raise ApiValueError("Missing the required parameter `id_auth` when calling `webhooks_auth_id_auth_put`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in local_var_params or
                local_var_params['name'] is None):
            raise ApiValueError("Missing the required parameter `name` when calling `webhooks_auth_id_auth_put`")  # noqa: E501
        # verify the required parameter 'type' is set
        if ('type' not in local_var_params or
                local_var_params['type'] is None):
            raise ApiValueError("Missing the required parameter `type` when calling `webhooks_auth_id_auth_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_auth' in local_var_params:
            path_params['id_auth'] = local_var_params['id_auth']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'config' in local_var_params:
            form_params.append(('config', local_var_params['config']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'type' in local_var_params:
            form_params.append(('type', local_var_params['type']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/auth/{id_auth}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AuthProvider',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_auth_post(self, name, type, **kwargs):  # noqa: E501
        """Adds a new webhook authentication type  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_auth_post(name, type, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: The name of the authentication process to differentiate (required)
        :param int type: The type of the authentication process (oauth, certificate, token, etc...) (required)
        :param str expand:
        :param str config: The authentication process configuration. A dict contains either the certificate
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AuthProvider
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_auth_post_with_http_info(name, type, **kwargs)  # noqa: E501

    def webhooks_auth_post_with_http_info(self, name, type, **kwargs):  # noqa: E501
        """Adds a new webhook authentication type  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_auth_post_with_http_info(name, type, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: The name of the authentication process to differentiate (required)
        :param int type: The type of the authentication process (oauth, certificate, token, etc...) (required)
        :param str expand:
        :param str config: The authentication process configuration. A dict contains either the certificate
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AuthProvider, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['name', 'type', 'expand', 'config']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_auth_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'name' is set
        if ('name' not in local_var_params or
                local_var_params['name'] is None):
            raise ApiValueError("Missing the required parameter `name` when calling `webhooks_auth_post`")  # noqa: E501
        # verify the required parameter 'type' is set
        if ('type' not in local_var_params or
                local_var_params['type'] is None):
            raise ApiValueError("Missing the required parameter `type` when calling `webhooks_auth_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'config' in local_var_params:
            form_params.append(('config', local_var_params['config']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'type' in local_var_params:
            form_params.append(('type', local_var_params['type']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/auth', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AuthProvider',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_delete(self, **kwargs):  # noqa: E501
        """Deletes all webhooks  # noqa: E501

        Updates the deleted field with the date of the deletion<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_delete(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Webhook
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_delete_with_http_info(**kwargs)  # noqa: E501

    def webhooks_delete_with_http_info(self, **kwargs):  # noqa: E501
        """Deletes all webhooks  # noqa: E501

        Updates the deleted field with the date of the deletion<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_delete_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Webhook, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Webhook',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_get(self, **kwargs):  # noqa: E501
        """Get webhooks  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: WebHookAddToData
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_get_with_http_info(**kwargs)  # noqa: E501

    def webhooks_get_with_http_info(self, **kwargs):  # noqa: E501
        """Get webhooks  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(WebHookAddToData, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WebHookAddToData',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_id_webhook_add_to_data_delete(self, id_webhook, **kwargs):  # noqa: E501
        """delete all entries  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_add_to_data_delete(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Webhook
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_id_webhook_add_to_data_delete_with_http_info(id_webhook, **kwargs)  # noqa: E501

    def webhooks_id_webhook_add_to_data_delete_with_http_info(self, id_webhook, **kwargs):  # noqa: E501
        """delete all entries  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_add_to_data_delete_with_http_info(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Webhook, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_webhook', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_id_webhook_add_to_data_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_webhook' is set
        if ('id_webhook' not in local_var_params or
                local_var_params['id_webhook'] is None):
            raise ApiValueError("Missing the required parameter `id_webhook` when calling `webhooks_id_webhook_add_to_data_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_webhook' in local_var_params:
            path_params['id_webhook'] = local_var_params['id_webhook']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/{id_webhook}/add_to_data', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Webhook',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_id_webhook_add_to_data_get(self, id_webhook, **kwargs):  # noqa: E501
        """retrieve the list of the value to add in webhooks when sending the requested webhook  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_add_to_data_get(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: WebHookAddToData
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_id_webhook_add_to_data_get_with_http_info(id_webhook, **kwargs)  # noqa: E501

    def webhooks_id_webhook_add_to_data_get_with_http_info(self, id_webhook, **kwargs):  # noqa: E501
        """retrieve the list of the value to add in webhooks when sending the requested webhook  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_add_to_data_get_with_http_info(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(WebHookAddToData, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_webhook', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_id_webhook_add_to_data_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_webhook' is set
        if ('id_webhook' not in local_var_params or
                local_var_params['id_webhook'] is None):
            raise ApiValueError("Missing the required parameter `id_webhook` when calling `webhooks_id_webhook_add_to_data_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_webhook' in local_var_params:
            path_params['id_webhook'] = local_var_params['id_webhook']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/{id_webhook}/add_to_data', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WebHookAddToData',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_id_webhook_add_to_data_key_delete(self, id_webhook, key, **kwargs):  # noqa: E501
        """delete the requested entry  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_add_to_data_key_delete(id_webhook, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str key: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Webhook
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_id_webhook_add_to_data_key_delete_with_http_info(id_webhook, key, **kwargs)  # noqa: E501

    def webhooks_id_webhook_add_to_data_key_delete_with_http_info(self, id_webhook, key, **kwargs):  # noqa: E501
        """delete the requested entry  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_add_to_data_key_delete_with_http_info(id_webhook, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str key: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Webhook, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_webhook', 'key', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_id_webhook_add_to_data_key_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_webhook' is set
        if ('id_webhook' not in local_var_params or
                local_var_params['id_webhook'] is None):
            raise ApiValueError("Missing the required parameter `id_webhook` when calling `webhooks_id_webhook_add_to_data_key_delete`")  # noqa: E501
        # verify the required parameter 'key' is set
        if ('key' not in local_var_params or
                local_var_params['key'] is None):
            raise ApiValueError("Missing the required parameter `key` when calling `webhooks_id_webhook_add_to_data_key_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_webhook' in local_var_params:
            path_params['id_webhook'] = local_var_params['id_webhook']  # noqa: E501
        if 'key' in local_var_params:
            path_params['key'] = local_var_params['key']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/{id_webhook}/add_to_data/{key}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Webhook',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_id_webhook_add_to_data_key_get(self, id_webhook, key, **kwargs):  # noqa: E501
        """retrieve the value to add in the requested webhook for the requested name  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_add_to_data_key_get(id_webhook, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str key: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Webhook
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_id_webhook_add_to_data_key_get_with_http_info(id_webhook, key, **kwargs)  # noqa: E501

    def webhooks_id_webhook_add_to_data_key_get_with_http_info(self, id_webhook, key, **kwargs):  # noqa: E501
        """retrieve the value to add in the requested webhook for the requested name  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_add_to_data_key_get_with_http_info(id_webhook, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str key: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Webhook, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_webhook', 'key', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_id_webhook_add_to_data_key_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_webhook' is set
        if ('id_webhook' not in local_var_params or
                local_var_params['id_webhook'] is None):
            raise ApiValueError("Missing the required parameter `id_webhook` when calling `webhooks_id_webhook_add_to_data_key_get`")  # noqa: E501
        # verify the required parameter 'key' is set
        if ('key' not in local_var_params or
                local_var_params['key'] is None):
            raise ApiValueError("Missing the required parameter `key` when calling `webhooks_id_webhook_add_to_data_key_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_webhook' in local_var_params:
            path_params['id_webhook'] = local_var_params['id_webhook']  # noqa: E501
        if 'key' in local_var_params:
            path_params['key'] = local_var_params['key']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/{id_webhook}/add_to_data/{key}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Webhook',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_id_webhook_add_to_data_key_post(self, id_webhook, key, **kwargs):  # noqa: E501
        """upate the requested field to store in user config when calling the endpoint  # noqa: E501

        For each parameter, a value will be added in the webhook data. Use the key to set the name of the field. The values that can be added are to be found in the user configuration.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_add_to_data_key_post(id_webhook, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str key: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Webhook
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_id_webhook_add_to_data_key_post_with_http_info(id_webhook, key, **kwargs)  # noqa: E501

    def webhooks_id_webhook_add_to_data_key_post_with_http_info(self, id_webhook, key, **kwargs):  # noqa: E501
        """upate the requested field to store in user config when calling the endpoint  # noqa: E501

        For each parameter, a value will be added in the webhook data. Use the key to set the name of the field. The values that can be added are to be found in the user configuration.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_add_to_data_key_post_with_http_info(id_webhook, key, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str key: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Webhook, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_webhook', 'key', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_id_webhook_add_to_data_key_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_webhook' is set
        if ('id_webhook' not in local_var_params or
                local_var_params['id_webhook'] is None):
            raise ApiValueError("Missing the required parameter `id_webhook` when calling `webhooks_id_webhook_add_to_data_key_post`")  # noqa: E501
        # verify the required parameter 'key' is set
        if ('key' not in local_var_params or
                local_var_params['key'] is None):
            raise ApiValueError("Missing the required parameter `key` when calling `webhooks_id_webhook_add_to_data_key_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_webhook' in local_var_params:
            path_params['id_webhook'] = local_var_params['id_webhook']  # noqa: E501
        if 'key' in local_var_params:
            path_params['key'] = local_var_params['key']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/{id_webhook}/add_to_data/{key}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Webhook',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_id_webhook_add_to_data_post(self, id_webhook, **kwargs):  # noqa: E501
        """Setup a field to store in user config when calling the endpoint  # noqa: E501

        For each parameter, a value will be added in the webhook data. Use the key to set the name of the field. The values that can be added are to be found in the user configuration.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_add_to_data_post(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Webhook
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_id_webhook_add_to_data_post_with_http_info(id_webhook, **kwargs)  # noqa: E501

    def webhooks_id_webhook_add_to_data_post_with_http_info(self, id_webhook, **kwargs):  # noqa: E501
        """Setup a field to store in user config when calling the endpoint  # noqa: E501

        For each parameter, a value will be added in the webhook data. Use the key to set the name of the field. The values that can be added are to be found in the user configuration.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_add_to_data_post_with_http_info(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Webhook, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_webhook', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_id_webhook_add_to_data_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_webhook' is set
        if ('id_webhook' not in local_var_params or
                local_var_params['id_webhook'] is None):
            raise ApiValueError("Missing the required parameter `id_webhook` when calling `webhooks_id_webhook_add_to_data_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_webhook' in local_var_params:
            path_params['id_webhook'] = local_var_params['id_webhook']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/{id_webhook}/add_to_data', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Webhook',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_id_webhook_delete(self, id_webhook, **kwargs):  # noqa: E501
        """Deletes a webhook  # noqa: E501

        Updates the deleted field with the date of the deletion<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_delete(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Webhook
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_id_webhook_delete_with_http_info(id_webhook, **kwargs)  # noqa: E501

    def webhooks_id_webhook_delete_with_http_info(self, id_webhook, **kwargs):  # noqa: E501
        """Deletes a webhook  # noqa: E501

        Updates the deleted field with the date of the deletion<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_delete_with_http_info(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Webhook, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_webhook', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_id_webhook_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_webhook' is set
        if ('id_webhook' not in local_var_params or
                local_var_params['id_webhook'] is None):
            raise ApiValueError("Missing the required parameter `id_webhook` when calling `webhooks_id_webhook_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_webhook' in local_var_params:
            path_params['id_webhook'] = local_var_params['id_webhook']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/{id_webhook}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Webhook',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_id_webhook_logs_get(self, id_webhook, **kwargs):  # noqa: E501
        """Get webhooks logs.  # noqa: E501

        Get logs of the webhooks.<br><br>By default, it selects logs for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_logs_get(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param int id_user: limit number of results to this user
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal (inclusive) date
        :param date max_date: maximum (inclusive) date
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: WebHookLogs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_id_webhook_logs_get_with_http_info(id_webhook, **kwargs)  # noqa: E501

    def webhooks_id_webhook_logs_get_with_http_info(self, id_webhook, **kwargs):  # noqa: E501
        """Get webhooks logs.  # noqa: E501

        Get logs of the webhooks.<br><br>By default, it selects logs for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_logs_get_with_http_info(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param int id_user: limit number of results to this user
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal (inclusive) date
        :param date max_date: maximum (inclusive) date
        :param str expand:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(WebHookLogs, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_webhook', 'id_user', 'limit', 'offset', 'min_date', 'max_date', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_id_webhook_logs_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_webhook' is set
        if ('id_webhook' not in local_var_params or
                local_var_params['id_webhook'] is None):
            raise ApiValueError("Missing the required parameter `id_webhook` when calling `webhooks_id_webhook_logs_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_webhook' in local_var_params:
            path_params['id_webhook'] = local_var_params['id_webhook']  # noqa: E501

        query_params = []
        if 'id_user' in local_var_params:
            query_params.append(('id_user', local_var_params['id_user']))  # noqa: E501
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/{id_webhook}/logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='WebHookLogs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_id_webhook_post(self, id_webhook, **kwargs):  # noqa: E501
        """Updates a webhook  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_post(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str expand:
        :param str deleted: a date to delete the webhook or 'null' to enable it
        :param str event: The webhook event
        :param int id_auth: The webhook authentication process to use
        :param int id_service: The service ID to associate with the webhook
        :param int id_user: The user ID to associate with the webhook
        :param str url: The webhook callback url
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Webhook
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_id_webhook_post_with_http_info(id_webhook, **kwargs)  # noqa: E501

    def webhooks_id_webhook_post_with_http_info(self, id_webhook, **kwargs):  # noqa: E501
        """Updates a webhook  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_post_with_http_info(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str expand:
        :param str deleted: a date to delete the webhook or 'null' to enable it
        :param str event: The webhook event
        :param int id_auth: The webhook authentication process to use
        :param int id_service: The service ID to associate with the webhook
        :param int id_user: The user ID to associate with the webhook
        :param str url: The webhook callback url
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Webhook, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_webhook', 'expand', 'deleted', 'event', 'id_auth', 'id_service', 'id_user', 'url']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_id_webhook_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_webhook' is set
        if ('id_webhook' not in local_var_params or
                local_var_params['id_webhook'] is None):
            raise ApiValueError("Missing the required parameter `id_webhook` when calling `webhooks_id_webhook_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_webhook' in local_var_params:
            path_params['id_webhook'] = local_var_params['id_webhook']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'deleted' in local_var_params:
            form_params.append(('deleted', local_var_params['deleted']))  # noqa: E501
        if 'event' in local_var_params:
            form_params.append(('event', local_var_params['event']))  # noqa: E501
        if 'id_auth' in local_var_params:
            form_params.append(('id_auth', local_var_params['id_auth']))  # noqa: E501
        if 'id_service' in local_var_params:
            form_params.append(('id_service', local_var_params['id_service']))  # noqa: E501
        if 'id_user' in local_var_params:
            form_params.append(('id_user', local_var_params['id_user']))  # noqa: E501
        if 'url' in local_var_params:
            form_params.append(('url', local_var_params['url']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/{id_webhook}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Webhook',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_id_webhook_put(self, id_webhook, **kwargs):  # noqa: E501
        """Updates a webhook  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_put(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str expand:
        :param str deleted: a date to delete the webhook or 'null' to enable it
        :param str event: The webhook event
        :param int id_auth: The webhook authentication process to use
        :param int id_service: The service ID to associate with the webhook
        :param int id_user: The user ID to associate with the webhook
        :param str url: The webhook callback url
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Webhook
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_id_webhook_put_with_http_info(id_webhook, **kwargs)  # noqa: E501

    def webhooks_id_webhook_put_with_http_info(self, id_webhook, **kwargs):  # noqa: E501
        """Updates a webhook  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_id_webhook_put_with_http_info(id_webhook, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_webhook: (required)
        :param str expand:
        :param str deleted: a date to delete the webhook or 'null' to enable it
        :param str event: The webhook event
        :param int id_auth: The webhook authentication process to use
        :param int id_service: The service ID to associate with the webhook
        :param int id_user: The user ID to associate with the webhook
        :param str url: The webhook callback url
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Webhook, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_webhook', 'expand', 'deleted', 'event', 'id_auth', 'id_service', 'id_user', 'url']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_id_webhook_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_webhook' is set
        if ('id_webhook' not in local_var_params or
                local_var_params['id_webhook'] is None):
            raise ApiValueError("Missing the required parameter `id_webhook` when calling `webhooks_id_webhook_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_webhook' in local_var_params:
            path_params['id_webhook'] = local_var_params['id_webhook']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'deleted' in local_var_params:
            form_params.append(('deleted', local_var_params['deleted']))  # noqa: E501
        if 'event' in local_var_params:
            form_params.append(('event', local_var_params['event']))  # noqa: E501
        if 'id_auth' in local_var_params:
            form_params.append(('id_auth', local_var_params['id_auth']))  # noqa: E501
        if 'id_service' in local_var_params:
            form_params.append(('id_service', local_var_params['id_service']))  # noqa: E501
        if 'id_user' in local_var_params:
            form_params.append(('id_user', local_var_params['id_user']))  # noqa: E501
        if 'url' in local_var_params:
            form_params.append(('url', local_var_params['url']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks/{id_webhook}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Webhook',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def webhooks_post(self, **kwargs):  # noqa: E501
        """Adds a new webhook  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param str event: The webhook event
        :param str id_auth: The webhook authentication process to use (its ID or its name)
        :param int id_service: The service ID to associate with the webhook
        :param int id_user: The user ID to associate with the webhook
        :param str params: The webhook parameters as an object with three keys: type, key and value
        :param str url: The webhook callback url
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Webhook
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.webhooks_post_with_http_info(**kwargs)  # noqa: E501

    def webhooks_post_with_http_info(self, **kwargs):  # noqa: E501
        """Adds a new webhook  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.webhooks_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param str event: The webhook event
        :param str id_auth: The webhook authentication process to use (its ID or its name)
        :param int id_service: The service ID to associate with the webhook
        :param int id_user: The user ID to associate with the webhook
        :param str params: The webhook parameters as an object with three keys: type, key and value
        :param str url: The webhook callback url
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Webhook, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['expand', 'event', 'id_auth', 'id_service', 'id_user', 'params', 'url']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method webhooks_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'event' in local_var_params:
            form_params.append(('event', local_var_params['event']))  # noqa: E501
        if 'id_auth' in local_var_params:
            form_params.append(('id_auth', local_var_params['id_auth']))  # noqa: E501
        if 'id_service' in local_var_params:
            form_params.append(('id_service', local_var_params['id_service']))  # noqa: E501
        if 'id_user' in local_var_params:
            form_params.append(('id_user', local_var_params['id_user']))  # noqa: E501
        if 'params' in local_var_params:
            form_params.append(('params', local_var_params['params']))  # noqa: E501
        if 'url' in local_var_params:
            form_params.append(('url', local_var_params['url']))  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/webhooks', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Webhook',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
