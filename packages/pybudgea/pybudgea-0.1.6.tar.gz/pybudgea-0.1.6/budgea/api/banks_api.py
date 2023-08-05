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


class BanksApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def account_types_get(self, **kwargs):  # noqa: E501
        """Get account types  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.account_types_get(async_req=True)
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
        :return: UserAccountTypes
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.account_types_get_with_http_info(**kwargs)  # noqa: E501

    def account_types_get_with_http_info(self, **kwargs):  # noqa: E501
        """Get account types  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.account_types_get_with_http_info(async_req=True)
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
        :return: tuple(UserAccountTypes, status_code(int), headers(HTTPHeaderDict))
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
                    " to method account_types_get" % key
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
            '/account_types', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAccountTypes',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def account_types_id_account_type_get(self, id_account_type, **kwargs):  # noqa: E501
        """Get an account type  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.account_types_id_account_type_get(id_account_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_account_type: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AccountType
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.account_types_id_account_type_get_with_http_info(id_account_type, **kwargs)  # noqa: E501

    def account_types_id_account_type_get_with_http_info(self, id_account_type, **kwargs):  # noqa: E501
        """Get an account type  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.account_types_id_account_type_get_with_http_info(id_account_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_account_type: (required)
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
        :return: tuple(AccountType, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_account_type', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method account_types_id_account_type_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_account_type' is set
        if ('id_account_type' not in local_var_params or
                local_var_params['id_account_type'] is None):
            raise ApiValueError("Missing the required parameter `id_account_type` when calling `account_types_id_account_type_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_account_type' in local_var_params:
            path_params['id_account_type'] = local_var_params['id_account_type']  # noqa: E501

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
            '/account_types/{id_account_type}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AccountType',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def banks_categories_id_category_delete(self, id_category, **kwargs):  # noqa: E501
        """Delete the supplied category  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_categories_id_category_delete(id_category, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_category: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectorCategory
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.banks_categories_id_category_delete_with_http_info(id_category, **kwargs)  # noqa: E501

    def banks_categories_id_category_delete_with_http_info(self, id_category, **kwargs):  # noqa: E501
        """Delete the supplied category  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_categories_id_category_delete_with_http_info(id_category, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_category: (required)
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
        :return: tuple(ConnectorCategory, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_category', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method banks_categories_id_category_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_category' is set
        if ('id_category' not in local_var_params or
                local_var_params['id_category'] is None):
            raise ApiValueError("Missing the required parameter `id_category` when calling `banks_categories_id_category_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_category' in local_var_params:
            path_params['id_category'] = local_var_params['id_category']  # noqa: E501

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
            '/banks/categories/{id_category}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectorCategory',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def banks_categories_id_category_post(self, id_category, name, **kwargs):  # noqa: E501
        """Edit a bank categories  # noqa: E501

        Edit the name for the supplied category.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_categories_id_category_post(id_category, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_category: (required)
        :param str name: new name for the supplied category (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectorCategory
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.banks_categories_id_category_post_with_http_info(id_category, name, **kwargs)  # noqa: E501

    def banks_categories_id_category_post_with_http_info(self, id_category, name, **kwargs):  # noqa: E501
        """Edit a bank categories  # noqa: E501

        Edit the name for the supplied category.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_categories_id_category_post_with_http_info(id_category, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_category: (required)
        :param str name: new name for the supplied category (required)
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
        :return: tuple(ConnectorCategory, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_category', 'name', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method banks_categories_id_category_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_category' is set
        if ('id_category' not in local_var_params or
                local_var_params['id_category'] is None):
            raise ApiValueError("Missing the required parameter `id_category` when calling `banks_categories_id_category_post`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in local_var_params or
                local_var_params['name'] is None):
            raise ApiValueError("Missing the required parameter `name` when calling `banks_categories_id_category_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_category' in local_var_params:
            path_params['id_category'] = local_var_params['id_category']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501

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
            '/banks/categories/{id_category}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectorCategory',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def banks_categories_post(self, name, **kwargs):  # noqa: E501
        """Create bank categories  # noqa: E501

        It requires the name of the category to be created<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_categories_post(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: name of the category to be created (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectorCategory
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.banks_categories_post_with_http_info(name, **kwargs)  # noqa: E501

    def banks_categories_post_with_http_info(self, name, **kwargs):  # noqa: E501
        """Create bank categories  # noqa: E501

        It requires the name of the category to be created<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_categories_post_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: name of the category to be created (required)
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
        :return: tuple(ConnectorCategory, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['name', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method banks_categories_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'name' is set
        if ('name' not in local_var_params or
                local_var_params['name'] is None):
            raise ApiValueError("Missing the required parameter `name` when calling `banks_categories_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501

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
            '/banks/categories', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectorCategory',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def banks_get(self, **kwargs):  # noqa: E501
        """Get list of connectors  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_get(async_req=True)
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
        :return: Banks
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.banks_get_with_http_info(**kwargs)  # noqa: E501

    def banks_get_with_http_info(self, **kwargs):  # noqa: E501
        """Get list of connectors  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_get_with_http_info(async_req=True)
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
        :return: tuple(Banks, status_code(int), headers(HTTPHeaderDict))
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
                    " to method banks_get" % key
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
            '/banks', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Banks',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def banks_id_connector_connections_get(self, id_connector, **kwargs):  # noqa: E501
        """Get a subset of id_connection with the largest diversity of account  # noqa: E501

        By default, it selects a set of 3 connections.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_id_connector_connections_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param int range: the length of the connection subset
        :param int type: to target a specific account type which will be
        :param int occurrences: require at least N accounts of the targeted
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderConnections
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.banks_id_connector_connections_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def banks_id_connector_connections_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get a subset of id_connection with the largest diversity of account  # noqa: E501

        By default, it selects a set of 3 connections.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_id_connector_connections_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param int range: the length of the connection subset
        :param int type: to target a specific account type which will be
        :param int occurrences: require at least N accounts of the targeted
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
        :return: tuple(ProviderConnections, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'range', 'type', 'occurrences', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method banks_id_connector_connections_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `banks_id_connector_connections_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

        query_params = []
        if 'range' in local_var_params:
            query_params.append(('range', local_var_params['range']))  # noqa: E501
        if 'type' in local_var_params:
            query_params.append(('type', local_var_params['type']))  # noqa: E501
        if 'occurrences' in local_var_params:
            query_params.append(('occurrences', local_var_params['occurrences']))  # noqa: E501
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
            '/banks/{id_connector}/connections', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderConnections',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def banks_id_connector_logos_get(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_id_connector_logos_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderLogos
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.banks_id_connector_logos_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def banks_id_connector_logos_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_id_connector_logos_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ProviderLogos, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method banks_id_connector_logos_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `banks_id_connector_logos_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/banks/{id_connector}/logos', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderLogos',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def banks_id_connector_logos_main_get(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_id_connector_logos_main_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderLogos
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.banks_id_connector_logos_main_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def banks_id_connector_logos_main_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_id_connector_logos_main_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ProviderLogos, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method banks_id_connector_logos_main_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `banks_id_connector_logos_main_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/banks/{id_connector}/logos/main', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderLogos',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def banks_id_connector_logos_thumbnail_get(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_id_connector_logos_thumbnail_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderLogos
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.banks_id_connector_logos_thumbnail_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def banks_id_connector_logos_thumbnail_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_id_connector_logos_thumbnail_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ProviderLogos, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method banks_id_connector_logos_thumbnail_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `banks_id_connector_logos_thumbnail_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/banks/{id_connector}/logos/thumbnail', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderLogos',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def banks_id_connector_sources_get(self, id_connector, **kwargs):  # noqa: E501
        """Get list of connector sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_id_connector_sources_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderSources
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.banks_id_connector_sources_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def banks_id_connector_sources_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get list of connector sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.banks_id_connector_sources_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ProviderSources, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method banks_id_connector_sources_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `banks_id_connector_sources_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/banks/{id_connector}/sources', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderSources',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def categories_get(self, **kwargs):  # noqa: E501
        """Get all categories  # noqa: E501

        Ressource to get all existing categories<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.categories_get(async_req=True)
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
        :return: Categories
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.categories_get_with_http_info(**kwargs)  # noqa: E501

    def categories_get_with_http_info(self, **kwargs):  # noqa: E501
        """Get all categories  # noqa: E501

        Ressource to get all existing categories<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.categories_get_with_http_info(async_req=True)
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
        :return: tuple(Categories, status_code(int), headers(HTTPHeaderDict))
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
                    " to method categories_get" % key
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
            '/categories', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Categories',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def categories_keywords_id_keyword_delete(self, id_keyword, **kwargs):  # noqa: E501
        """Delete a particular key-value pair on a transaction.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.categories_keywords_id_keyword_delete(id_keyword, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_keyword: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Keyword
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.categories_keywords_id_keyword_delete_with_http_info(id_keyword, **kwargs)  # noqa: E501

    def categories_keywords_id_keyword_delete_with_http_info(self, id_keyword, **kwargs):  # noqa: E501
        """Delete a particular key-value pair on a transaction.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.categories_keywords_id_keyword_delete_with_http_info(id_keyword, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_keyword: (required)
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
        :return: tuple(Keyword, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_keyword', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method categories_keywords_id_keyword_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_keyword' is set
        if ('id_keyword' not in local_var_params or
                local_var_params['id_keyword'] is None):
            raise ApiValueError("Missing the required parameter `id_keyword` when calling `categories_keywords_id_keyword_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_keyword' in local_var_params:
            path_params['id_keyword'] = local_var_params['id_keyword']  # noqa: E501

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
            '/categories/keywords/{id_keyword}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Keyword',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def categories_keywords_post(self, **kwargs):  # noqa: E501
        """Add a new keyword associated with a category in the database.  # noqa: E501

        If the keyword already exists the keyword is not added. Used for the categorization of transactions.<br><br>Form params: - id_category (integer): a reference towards the category associated with the keyword - keyword (string): the searched keyword - income (bool): 1 if the associated category represents an income else 0 - priority (integer): sets the priority for the keyword, used when categorizing<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.categories_keywords_post(async_req=True)
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
        :return: Keyword
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.categories_keywords_post_with_http_info(**kwargs)  # noqa: E501

    def categories_keywords_post_with_http_info(self, **kwargs):  # noqa: E501
        """Add a new keyword associated with a category in the database.  # noqa: E501

        If the keyword already exists the keyword is not added. Used for the categorization of transactions.<br><br>Form params: - id_category (integer): a reference towards the category associated with the keyword - keyword (string): the searched keyword - income (bool): 1 if the associated category represents an income else 0 - priority (integer): sets the priority for the keyword, used when categorizing<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.categories_keywords_post_with_http_info(async_req=True)
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
        :return: tuple(Keyword, status_code(int), headers(HTTPHeaderDict))
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
                    " to method categories_keywords_post" % key
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
            '/categories/keywords', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Keyword',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def categorize_post(self, type, value, wording, **kwargs):  # noqa: E501
        """categorize transactions without storing them  # noqa: E501

        It requires an array of transaction dictionaries. Any fields of transactions that are not required will be kept in the response. The response contains the list of transactions with two more fields: id_category and state (it indicates how the transaction has been categorized)<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.categorize_post(type, value, wording, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str type: type of the transaction (default: unknown) (required)
        :param int value: value of the transaction (required)
        :param str wording: label of the transaction (required)
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
        return self.categorize_post_with_http_info(type, value, wording, **kwargs)  # noqa: E501

    def categorize_post_with_http_info(self, type, value, wording, **kwargs):  # noqa: E501
        """categorize transactions without storing them  # noqa: E501

        It requires an array of transaction dictionaries. Any fields of transactions that are not required will be kept in the response. The response contains the list of transactions with two more fields: id_category and state (it indicates how the transaction has been categorized)<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.categorize_post_with_http_info(type, value, wording, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str type: type of the transaction (default: unknown) (required)
        :param int value: value of the transaction (required)
        :param str wording: label of the transaction (required)
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

        all_params = ['type', 'value', 'wording']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method categorize_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'type' is set
        if ('type' not in local_var_params or
                local_var_params['type'] is None):
            raise ApiValueError("Missing the required parameter `type` when calling `categorize_post`")  # noqa: E501
        # verify the required parameter 'value' is set
        if ('value' not in local_var_params or
                local_var_params['value'] is None):
            raise ApiValueError("Missing the required parameter `value` when calling `categorize_post`")  # noqa: E501
        # verify the required parameter 'wording' is set
        if ('wording' not in local_var_params or
                local_var_params['wording'] is None):
            raise ApiValueError("Missing the required parameter `wording` when calling `categorize_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'type' in local_var_params:
            form_params.append(('type', local_var_params['type']))  # noqa: E501
        if 'value' in local_var_params:
            form_params.append(('value', local_var_params['value']))  # noqa: E501
        if 'wording' in local_var_params:
            form_params.append(('wording', local_var_params['wording']))  # noqa: E501

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
            '/categorize', 'POST',
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

    def connections_get(self, **kwargs):  # noqa: E501
        """Get connections without a user  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connections_get(async_req=True)
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
        :return: ProviderConnections
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connections_get_with_http_info(**kwargs)  # noqa: E501

    def connections_get_with_http_info(self, **kwargs):  # noqa: E501
        """Get connections without a user  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connections_get_with_http_info(async_req=True)
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
        :return: tuple(ProviderConnections, status_code(int), headers(HTTPHeaderDict))
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
                    " to method connections_get" % key
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
            '/connections', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderConnections',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connections_id_connection_logs_get(self, id_connection, **kwargs):  # noqa: E501
        """Get connection logs  # noqa: E501

        Get logs about connections.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connections_id_connection_logs_get(id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connection: (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param int state: state of user
        :param str period: period to group logs
        :param int id_user: ID of a user
        :param int id_connection2: ID of a connection
        :param int id_connector: ID of a connector
        :param bool charged: consider only logs for charged connectors
        :param int id_source: ID of a source
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectionLogs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connections_id_connection_logs_get_with_http_info(id_connection, **kwargs)  # noqa: E501

    def connections_id_connection_logs_get_with_http_info(self, id_connection, **kwargs):  # noqa: E501
        """Get connection logs  # noqa: E501

        Get logs about connections.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connections_id_connection_logs_get_with_http_info(id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connection: (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param int state: state of user
        :param str period: period to group logs
        :param int id_user: ID of a user
        :param int id_connection2: ID of a connection
        :param int id_connector: ID of a connector
        :param bool charged: consider only logs for charged connectors
        :param int id_source: ID of a source
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
        :return: tuple(ConnectionLogs, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connection', 'limit', 'offset', 'min_date', 'max_date', 'state', 'period', 'id_user', 'id_connection2', 'id_connector', 'charged', 'id_source', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connections_id_connection_logs_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `connections_id_connection_logs_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'state' in local_var_params:
            query_params.append(('state', local_var_params['state']))  # noqa: E501
        if 'period' in local_var_params:
            query_params.append(('period', local_var_params['period']))  # noqa: E501
        if 'id_user' in local_var_params:
            query_params.append(('id_user', local_var_params['id_user']))  # noqa: E501
        if 'id_connection2' in local_var_params:
            query_params.append(('id_connection', local_var_params['id_connection2']))  # noqa: E501
        if 'id_connector' in local_var_params:
            query_params.append(('id_connector', local_var_params['id_connector']))  # noqa: E501
        if 'charged' in local_var_params:
            query_params.append(('charged', local_var_params['charged']))  # noqa: E501
        if 'id_source' in local_var_params:
            query_params.append(('id_source', local_var_params['id_source']))  # noqa: E501
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
            '/connections/{id_connection}/logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectionLogs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connections_id_connection_sources_get(self, id_connection, **kwargs):  # noqa: E501
        """Get connection sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connections_id_connection_sources_get(id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connection: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserAccountSources
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connections_id_connection_sources_get_with_http_info(id_connection, **kwargs)  # noqa: E501

    def connections_id_connection_sources_get_with_http_info(self, id_connection, **kwargs):  # noqa: E501
        """Get connection sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connections_id_connection_sources_get_with_http_info(id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connection: (required)
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
        :return: tuple(UserAccountSources, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connection', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connections_id_connection_sources_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `connections_id_connection_sources_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

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
            '/connections/{id_connection}/sources', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAccountSources',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connections_id_connection_sources_id_source_delete(self, id_connection, id_source, **kwargs):  # noqa: E501
        """Disable a connection source  # noqa: E501

        This will make it so the specified source will not be synchronized anymore.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connections_id_connection_sources_id_source_delete(id_connection, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connection: (required)
        :param int id_source: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectionSource
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connections_id_connection_sources_id_source_delete_with_http_info(id_connection, id_source, **kwargs)  # noqa: E501

    def connections_id_connection_sources_id_source_delete_with_http_info(self, id_connection, id_source, **kwargs):  # noqa: E501
        """Disable a connection source  # noqa: E501

        This will make it so the specified source will not be synchronized anymore.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connections_id_connection_sources_id_source_delete_with_http_info(id_connection, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connection: (required)
        :param int id_source: (required)
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
        :return: tuple(ConnectionSource, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connection', 'id_source', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connections_id_connection_sources_id_source_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `connections_id_connection_sources_id_source_delete`")  # noqa: E501
        # verify the required parameter 'id_source' is set
        if ('id_source' not in local_var_params or
                local_var_params['id_source'] is None):
            raise ApiValueError("Missing the required parameter `id_source` when calling `connections_id_connection_sources_id_source_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_source' in local_var_params:
            path_params['id_source'] = local_var_params['id_source']  # noqa: E501

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
            '/connections/{id_connection}/sources/{id_source}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectionSource',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connections_id_connection_sources_id_source_post(self, id_connection, id_source, **kwargs):  # noqa: E501
        """Enable connection source  # noqa: E501

        This will make it so the specified source will be able to be synchronized.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connections_id_connection_sources_id_source_post(id_connection, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connection: (required)
        :param int id_source: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectionSource
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connections_id_connection_sources_id_source_post_with_http_info(id_connection, id_source, **kwargs)  # noqa: E501

    def connections_id_connection_sources_id_source_post_with_http_info(self, id_connection, id_source, **kwargs):  # noqa: E501
        """Enable connection source  # noqa: E501

        This will make it so the specified source will be able to be synchronized.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connections_id_connection_sources_id_source_post_with_http_info(id_connection, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connection: (required)
        :param int id_source: (required)
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
        :return: tuple(ConnectionSource, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connection', 'id_source', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connections_id_connection_sources_id_source_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `connections_id_connection_sources_id_source_post`")  # noqa: E501
        # verify the required parameter 'id_source' is set
        if ('id_source' not in local_var_params or
                local_var_params['id_source'] is None):
            raise ApiValueError("Missing the required parameter `id_source` when calling `connections_id_connection_sources_id_source_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_source' in local_var_params:
            path_params['id_source'] = local_var_params['id_source']  # noqa: E501

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
            '/connections/{id_connection}/sources/{id_source}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectionSource',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connections_id_connection_sources_id_source_put(self, id_connection, id_source, **kwargs):  # noqa: E501
        """Enable connection source  # noqa: E501

        This will make it so the specified source will be able to be synchronized.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connections_id_connection_sources_id_source_put(id_connection, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connection: (required)
        :param int id_source: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectionSource
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connections_id_connection_sources_id_source_put_with_http_info(id_connection, id_source, **kwargs)  # noqa: E501

    def connections_id_connection_sources_id_source_put_with_http_info(self, id_connection, id_source, **kwargs):  # noqa: E501
        """Enable connection source  # noqa: E501

        This will make it so the specified source will be able to be synchronized.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connections_id_connection_sources_id_source_put_with_http_info(id_connection, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connection: (required)
        :param int id_source: (required)
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
        :return: tuple(ConnectionSource, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connection', 'id_source', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connections_id_connection_sources_id_source_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `connections_id_connection_sources_id_source_put`")  # noqa: E501
        # verify the required parameter 'id_source' is set
        if ('id_source' not in local_var_params or
                local_var_params['id_source'] is None):
            raise ApiValueError("Missing the required parameter `id_source` when calling `connections_id_connection_sources_id_source_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_source' in local_var_params:
            path_params['id_source'] = local_var_params['id_source']  # noqa: E501

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
            '/connections/{id_connection}/sources/{id_source}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectionSource',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_get(self, **kwargs):  # noqa: E501
        """Get list of connectors  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_get(async_req=True)
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
        :return: Connectors
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_get_with_http_info(**kwargs)  # noqa: E501

    def connectors_get_with_http_info(self, **kwargs):  # noqa: E501
        """Get list of connectors  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_get_with_http_info(async_req=True)
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
        :return: tuple(Connectors, status_code(int), headers(HTTPHeaderDict))
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
                    " to method connectors_get" % key
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
            '/connectors', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Connectors',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_id_connector_logos_get(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderLogos
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_id_connector_logos_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def connectors_id_connector_logos_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ProviderLogos, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connectors_id_connector_logos_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `connectors_id_connector_logos_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/connectors/{id_connector}/logos', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderLogos',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_id_connector_logos_id_logo_delete(self, id_connector, id_logo, **kwargs):  # noqa: E501
        """Delete a single Logo object.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_id_logo_delete(id_connector, id_logo, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param int id_logo: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectorLogo
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_id_connector_logos_id_logo_delete_with_http_info(id_connector, id_logo, **kwargs)  # noqa: E501

    def connectors_id_connector_logos_id_logo_delete_with_http_info(self, id_connector, id_logo, **kwargs):  # noqa: E501
        """Delete a single Logo object.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_id_logo_delete_with_http_info(id_connector, id_logo, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param int id_logo: (required)
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
        :return: tuple(ConnectorLogo, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'id_logo', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connectors_id_connector_logos_id_logo_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `connectors_id_connector_logos_id_logo_delete`")  # noqa: E501
        # verify the required parameter 'id_logo' is set
        if ('id_logo' not in local_var_params or
                local_var_params['id_logo'] is None):
            raise ApiValueError("Missing the required parameter `id_logo` when calling `connectors_id_connector_logos_id_logo_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501
        if 'id_logo' in local_var_params:
            path_params['id_logo'] = local_var_params['id_logo']  # noqa: E501

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
            '/connectors/{id_connector}/logos/{id_logo}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectorLogo',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_id_connector_logos_id_logo_put(self, id_connector, id_logo, **kwargs):  # noqa: E501
        """Create or Update a connector Logo.  # noqa: E501

        This endpoint creates or update a connector logo. This logo is a mapping between a file (/file route) and a connector (/connectors route) or a provider (/providers route).<br><br>Form params: - id_file (integer): The id of the file to link with that connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_id_logo_put(id_connector, id_logo, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param int id_logo: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectorLogo
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_id_connector_logos_id_logo_put_with_http_info(id_connector, id_logo, **kwargs)  # noqa: E501

    def connectors_id_connector_logos_id_logo_put_with_http_info(self, id_connector, id_logo, **kwargs):  # noqa: E501
        """Create or Update a connector Logo.  # noqa: E501

        This endpoint creates or update a connector logo. This logo is a mapping between a file (/file route) and a connector (/connectors route) or a provider (/providers route).<br><br>Form params: - id_file (integer): The id of the file to link with that connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_id_logo_put_with_http_info(id_connector, id_logo, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param int id_logo: (required)
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
        :return: tuple(ConnectorLogo, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'id_logo', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connectors_id_connector_logos_id_logo_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `connectors_id_connector_logos_id_logo_put`")  # noqa: E501
        # verify the required parameter 'id_logo' is set
        if ('id_logo' not in local_var_params or
                local_var_params['id_logo'] is None):
            raise ApiValueError("Missing the required parameter `id_logo` when calling `connectors_id_connector_logos_id_logo_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501
        if 'id_logo' in local_var_params:
            path_params['id_logo'] = local_var_params['id_logo']  # noqa: E501

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
            '/connectors/{id_connector}/logos/{id_logo}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectorLogo',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_id_connector_logos_main_get(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_main_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderLogos
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_id_connector_logos_main_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def connectors_id_connector_logos_main_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_main_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ProviderLogos, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connectors_id_connector_logos_main_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `connectors_id_connector_logos_main_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/connectors/{id_connector}/logos/main', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderLogos',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_id_connector_logos_post(self, id_connector, **kwargs):  # noqa: E501
        """Create a connector Logo  # noqa: E501

        This endpoint creates a connector logo. You can either pass a file to as a parameter to insert and link it with the connector or pass an id_file to link a connector with an existing file. Will fail if the file is already linked with that connector.<br><br>Form params: - id_file (integer): The id of the file to link with that connector. - img (string): Path to the image to link with that connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_post(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectorLogo
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_id_connector_logos_post_with_http_info(id_connector, **kwargs)  # noqa: E501

    def connectors_id_connector_logos_post_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Create a connector Logo  # noqa: E501

        This endpoint creates a connector logo. You can either pass a file to as a parameter to insert and link it with the connector or pass an id_file to link a connector with an existing file. Will fail if the file is already linked with that connector.<br><br>Form params: - id_file (integer): The id of the file to link with that connector. - img (string): Path to the image to link with that connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_post_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ConnectorLogo, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connectors_id_connector_logos_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `connectors_id_connector_logos_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/connectors/{id_connector}/logos', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectorLogo',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_id_connector_logos_put(self, id_connector, **kwargs):  # noqa: E501
        """Create or Update a connector Logo  # noqa: E501

        This endpoint creates or update a connector logo. This logo is a mapping between a file (/file route) and a connector (/connectors route) or a provider (/providers route).<br><br>Form params: - id_file (integer): The id of the file to link with that connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_put(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectorLogo
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_id_connector_logos_put_with_http_info(id_connector, **kwargs)  # noqa: E501

    def connectors_id_connector_logos_put_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Create or Update a connector Logo  # noqa: E501

        This endpoint creates or update a connector logo. This logo is a mapping between a file (/file route) and a connector (/connectors route) or a provider (/providers route).<br><br>Form params: - id_file (integer): The id of the file to link with that connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_put_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ConnectorLogo, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connectors_id_connector_logos_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `connectors_id_connector_logos_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/connectors/{id_connector}/logos', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectorLogo',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_id_connector_logos_thumbnail_get(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_thumbnail_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderLogos
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_id_connector_logos_thumbnail_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def connectors_id_connector_logos_thumbnail_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_logos_thumbnail_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ProviderLogos, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connectors_id_connector_logos_thumbnail_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `connectors_id_connector_logos_thumbnail_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/connectors/{id_connector}/logos/thumbnail', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderLogos',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_id_connector_put(self, id_connector, **kwargs):  # noqa: E501
        """Edit the provided connector  # noqa: E501

        <br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_put(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param str auth_mechanism: the authentication mechanism to use for this connector
        :param bool hidden: to enable  or disable connector (bank or provider)
        :param str id_categories: one or several comma separated categories to map to the given connector (or null to map no category)
        :param int sync_frequency: Allows you to overload global sync_frequency param
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Connector
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_id_connector_put_with_http_info(id_connector, **kwargs)  # noqa: E501

    def connectors_id_connector_put_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Edit the provided connector  # noqa: E501

        <br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_put_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param str auth_mechanism: the authentication mechanism to use for this connector
        :param bool hidden: to enable  or disable connector (bank or provider)
        :param str id_categories: one or several comma separated categories to map to the given connector (or null to map no category)
        :param int sync_frequency: Allows you to overload global sync_frequency param
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Connector, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand', 'auth_mechanism', 'hidden', 'id_categories', 'sync_frequency']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connectors_id_connector_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `connectors_id_connector_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'auth_mechanism' in local_var_params:
            form_params.append(('auth_mechanism', local_var_params['auth_mechanism']))  # noqa: E501
        if 'hidden' in local_var_params:
            form_params.append(('hidden', local_var_params['hidden']))  # noqa: E501
        if 'id_categories' in local_var_params:
            form_params.append(('id_categories', local_var_params['id_categories']))  # noqa: E501
        if 'sync_frequency' in local_var_params:
            form_params.append(('sync_frequency', local_var_params['sync_frequency']))  # noqa: E501

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
            '/connectors/{id_connector}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Connector',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_id_connector_sources_get(self, id_connector, **kwargs):  # noqa: E501
        """Get list of connector sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_sources_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderSources
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_id_connector_sources_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def connectors_id_connector_sources_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get list of connector sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_sources_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ProviderSources, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connectors_id_connector_sources_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `connectors_id_connector_sources_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/connectors/{id_connector}/sources', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderSources',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_id_connector_sources_id_source_put(self, id_connector, id_source, **kwargs):  # noqa: E501
        """Edit the provided connector source  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_sources_id_source_put(id_connector, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param int id_source: (required)
        :param str expand:
        :param str auth_mechanism: the authentication mechanism to use for this connector source
        :param datetime disabled: to enable or disable connector source
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectorSource
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_id_connector_sources_id_source_put_with_http_info(id_connector, id_source, **kwargs)  # noqa: E501

    def connectors_id_connector_sources_id_source_put_with_http_info(self, id_connector, id_source, **kwargs):  # noqa: E501
        """Edit the provided connector source  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_id_connector_sources_id_source_put_with_http_info(id_connector, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param int id_source: (required)
        :param str expand:
        :param str auth_mechanism: the authentication mechanism to use for this connector source
        :param datetime disabled: to enable or disable connector source
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ConnectorSource, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'id_source', 'expand', 'auth_mechanism', 'disabled']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connectors_id_connector_sources_id_source_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `connectors_id_connector_sources_id_source_put`")  # noqa: E501
        # verify the required parameter 'id_source' is set
        if ('id_source' not in local_var_params or
                local_var_params['id_source'] is None):
            raise ApiValueError("Missing the required parameter `id_source` when calling `connectors_id_connector_sources_id_source_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501
        if 'id_source' in local_var_params:
            path_params['id_source'] = local_var_params['id_source']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'auth_mechanism' in local_var_params:
            form_params.append(('auth_mechanism', local_var_params['auth_mechanism']))  # noqa: E501
        if 'disabled' in local_var_params:
            form_params.append(('disabled', local_var_params['disabled']))  # noqa: E501

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
            '/connectors/{id_connector}/sources/{id_source}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectorSource',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_post(self, login, name, password, **kwargs):  # noqa: E501
        """Request a new connector  # noqa: E501

        Send a request to add a new connector<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_post(login, name, password, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str login: Users login (required)
        :param str name: Name of the bank or provider (required)
        :param str password: Users password (required)
        :param str expand:
        :param str comment: Optionnal comment
        :param str email: Email of the user
        :param bool sendmail: if set, send an email to user
        :param str types: Type of connector, eg. banks or providers
        :param str url: Url of the bank
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Connector
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_post_with_http_info(login, name, password, **kwargs)  # noqa: E501

    def connectors_post_with_http_info(self, login, name, password, **kwargs):  # noqa: E501
        """Request a new connector  # noqa: E501

        Send a request to add a new connector<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_post_with_http_info(login, name, password, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str login: Users login (required)
        :param str name: Name of the bank or provider (required)
        :param str password: Users password (required)
        :param str expand:
        :param str comment: Optionnal comment
        :param str email: Email of the user
        :param bool sendmail: if set, send an email to user
        :param str types: Type of connector, eg. banks or providers
        :param str url: Url of the bank
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Connector, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['login', 'name', 'password', 'expand', 'comment', 'email', 'sendmail', 'types', 'url']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connectors_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'login' is set
        if ('login' not in local_var_params or
                local_var_params['login'] is None):
            raise ApiValueError("Missing the required parameter `login` when calling `connectors_post`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in local_var_params or
                local_var_params['name'] is None):
            raise ApiValueError("Missing the required parameter `name` when calling `connectors_post`")  # noqa: E501
        # verify the required parameter 'password' is set
        if ('password' not in local_var_params or
                local_var_params['password'] is None):
            raise ApiValueError("Missing the required parameter `password` when calling `connectors_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'comment' in local_var_params:
            form_params.append(('comment', local_var_params['comment']))  # noqa: E501
        if 'email' in local_var_params:
            form_params.append(('email', local_var_params['email']))  # noqa: E501
        if 'login' in local_var_params:
            form_params.append(('login', local_var_params['login']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'password' in local_var_params:
            form_params.append(('password', local_var_params['password']))  # noqa: E501
        if 'sendmail' in local_var_params:
            form_params.append(('sendmail', local_var_params['sendmail']))  # noqa: E501
        if 'types' in local_var_params:
            form_params.append(('types', local_var_params['types']))  # noqa: E501
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
            '/connectors', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Connector',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def connectors_put(self, **kwargs):  # noqa: E501
        """Enable/disable several connectors  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_put(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param bool hidden: to enable  or disable connector (bank or provider)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Connector
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.connectors_put_with_http_info(**kwargs)  # noqa: E501

    def connectors_put_with_http_info(self, **kwargs):  # noqa: E501
        """Enable/disable several connectors  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.connectors_put_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str expand:
        :param bool hidden: to enable  or disable connector (bank or provider)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Connector, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['expand', 'hidden']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method connectors_put" % key
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
        if 'hidden' in local_var_params:
            form_params.append(('hidden', local_var_params['hidden']))  # noqa: E501

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
            '/connectors', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Connector',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def invoicing_get(self, **kwargs):  # noqa: E501
        """Get invoicing data for a given period (default is the current month).  # noqa: E501

        You can get all the invoicing data or just specific ones by using the available parameters.<br><br>If no parameters are specified, no invoicing data is returned.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.invoicing_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param str users_synced: the number of user synchronized during the period
        :param str users_bank: the number of user of the Bank API synchronized during the period
        :param str users_bill:  the number of user of the Bill API synchronized during the period
        :param str accounts_synced: the number of accounts synchronized during the period
        :param str subscriptions_synced: the number of subscriptions synchronized during the period
        :param str connections_synced: the number of connections synchronized during the period
        :param str connections_account: the number of Bank API connections synchronized during the period
        :param str transfers_synced: the number of transfers done during the period
        :param str all: get all the invoicing data at once
        :param str detail: get full ids list instead of numbers
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
        return self.invoicing_get_with_http_info(**kwargs)  # noqa: E501

    def invoicing_get_with_http_info(self, **kwargs):  # noqa: E501
        """Get invoicing data for a given period (default is the current month).  # noqa: E501

        You can get all the invoicing data or just specific ones by using the available parameters.<br><br>If no parameters are specified, no invoicing data is returned.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.invoicing_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param str users_synced: the number of user synchronized during the period
        :param str users_bank: the number of user of the Bank API synchronized during the period
        :param str users_bill:  the number of user of the Bill API synchronized during the period
        :param str accounts_synced: the number of accounts synchronized during the period
        :param str subscriptions_synced: the number of subscriptions synchronized during the period
        :param str connections_synced: the number of connections synchronized during the period
        :param str connections_account: the number of Bank API connections synchronized during the period
        :param str transfers_synced: the number of transfers done during the period
        :param str all: get all the invoicing data at once
        :param str detail: get full ids list instead of numbers
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

        all_params = ['min_date', 'max_date', 'users_synced', 'users_bank', 'users_bill', 'accounts_synced', 'subscriptions_synced', 'connections_synced', 'connections_account', 'transfers_synced', 'all', 'detail']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method invoicing_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'users_synced' in local_var_params:
            query_params.append(('users_synced', local_var_params['users_synced']))  # noqa: E501
        if 'users_bank' in local_var_params:
            query_params.append(('users_bank', local_var_params['users_bank']))  # noqa: E501
        if 'users_bill' in local_var_params:
            query_params.append(('users_bill', local_var_params['users_bill']))  # noqa: E501
        if 'accounts_synced' in local_var_params:
            query_params.append(('accounts_synced', local_var_params['accounts_synced']))  # noqa: E501
        if 'subscriptions_synced' in local_var_params:
            query_params.append(('subscriptions_synced', local_var_params['subscriptions_synced']))  # noqa: E501
        if 'connections_synced' in local_var_params:
            query_params.append(('connections_synced', local_var_params['connections_synced']))  # noqa: E501
        if 'connections_account' in local_var_params:
            query_params.append(('connections_account', local_var_params['connections_account']))  # noqa: E501
        if 'transfers_synced' in local_var_params:
            query_params.append(('transfers_synced', local_var_params['transfers_synced']))  # noqa: E501
        if 'all' in local_var_params:
            query_params.append(('all', local_var_params['all']))  # noqa: E501
        if 'detail' in local_var_params:
            query_params.append(('detail', local_var_params['detail']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/invoicing', 'GET',
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

    def logs_get(self, **kwargs):  # noqa: E501
        """Get connection logs  # noqa: E501

        Get logs about connections.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.logs_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param int state: state of user
        :param str period: period to group logs
        :param int id_user: ID of a user
        :param int id_connection: ID of a connection
        :param int id_connector: ID of a connector
        :param bool charged: consider only logs for charged connectors
        :param int id_source: ID of a source
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectionLogs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.logs_get_with_http_info(**kwargs)  # noqa: E501

    def logs_get_with_http_info(self, **kwargs):  # noqa: E501
        """Get connection logs  # noqa: E501

        Get logs about connections.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.logs_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param int state: state of user
        :param str period: period to group logs
        :param int id_user: ID of a user
        :param int id_connection: ID of a connection
        :param int id_connector: ID of a connector
        :param bool charged: consider only logs for charged connectors
        :param int id_source: ID of a source
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
        :return: tuple(ConnectionLogs, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['limit', 'offset', 'min_date', 'max_date', 'state', 'period', 'id_user', 'id_connection', 'id_connector', 'charged', 'id_source', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method logs_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'state' in local_var_params:
            query_params.append(('state', local_var_params['state']))  # noqa: E501
        if 'period' in local_var_params:
            query_params.append(('period', local_var_params['period']))  # noqa: E501
        if 'id_user' in local_var_params:
            query_params.append(('id_user', local_var_params['id_user']))  # noqa: E501
        if 'id_connection' in local_var_params:
            query_params.append(('id_connection', local_var_params['id_connection']))  # noqa: E501
        if 'id_connector' in local_var_params:
            query_params.append(('id_connector', local_var_params['id_connector']))  # noqa: E501
        if 'charged' in local_var_params:
            query_params.append(('charged', local_var_params['charged']))  # noqa: E501
        if 'id_source' in local_var_params:
            query_params.append(('id_source', local_var_params['id_source']))  # noqa: E501
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
            '/logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectionLogs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def providers_get(self, **kwargs):  # noqa: E501
        """Get list of connectors  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.providers_get(async_req=True)
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
        :return: Providers
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.providers_get_with_http_info(**kwargs)  # noqa: E501

    def providers_get_with_http_info(self, **kwargs):  # noqa: E501
        """Get list of connectors  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.providers_get_with_http_info(async_req=True)
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
        :return: tuple(Providers, status_code(int), headers(HTTPHeaderDict))
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
                    " to method providers_get" % key
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
            '/providers', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Providers',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def providers_id_connector_connections_get(self, id_connector, **kwargs):  # noqa: E501
        """Get a random subset of provider's id_connection  # noqa: E501

        By default, it selects a set of 3 connections.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.providers_id_connector_connections_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param int range: the length of the connection subset
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderConnections
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.providers_id_connector_connections_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def providers_id_connector_connections_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get a random subset of provider's id_connection  # noqa: E501

        By default, it selects a set of 3 connections.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.providers_id_connector_connections_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param int range: the length of the connection subset
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
        :return: tuple(ProviderConnections, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'range', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method providers_id_connector_connections_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `providers_id_connector_connections_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

        query_params = []
        if 'range' in local_var_params:
            query_params.append(('range', local_var_params['range']))  # noqa: E501
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
            '/providers/{id_connector}/connections', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderConnections',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def providers_id_connector_logos_get(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.providers_id_connector_logos_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderLogos
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.providers_id_connector_logos_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def providers_id_connector_logos_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.providers_id_connector_logos_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ProviderLogos, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method providers_id_connector_logos_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `providers_id_connector_logos_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/providers/{id_connector}/logos', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderLogos',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def providers_id_connector_logos_main_get(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.providers_id_connector_logos_main_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderLogos
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.providers_id_connector_logos_main_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def providers_id_connector_logos_main_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.providers_id_connector_logos_main_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ProviderLogos, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method providers_id_connector_logos_main_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `providers_id_connector_logos_main_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/providers/{id_connector}/logos/main', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderLogos',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def providers_id_connector_logos_thumbnail_get(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.providers_id_connector_logos_thumbnail_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderLogos
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.providers_id_connector_logos_thumbnail_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def providers_id_connector_logos_thumbnail_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get all links to the files associated with this connector.  # noqa: E501

        This endpoint returns all links to files associated with this connector.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.providers_id_connector_logos_thumbnail_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ProviderLogos, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method providers_id_connector_logos_thumbnail_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `providers_id_connector_logos_thumbnail_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/providers/{id_connector}/logos/thumbnail', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderLogos',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def providers_id_connector_sources_get(self, id_connector, **kwargs):  # noqa: E501
        """Get list of connector sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.providers_id_connector_sources_get(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderSources
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.providers_id_connector_sources_get_with_http_info(id_connector, **kwargs)  # noqa: E501

    def providers_id_connector_sources_get_with_http_info(self, id_connector, **kwargs):  # noqa: E501
        """Get list of connector sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.providers_id_connector_sources_get_with_http_info(id_connector, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int id_connector: (required)
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
        :return: tuple(ProviderSources, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_connector', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method providers_id_connector_sources_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_connector' is set
        if ('id_connector' not in local_var_params or
                local_var_params['id_connector'] is None):
            raise ApiValueError("Missing the required parameter `id_connector` when calling `providers_id_connector_sources_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_connector' in local_var_params:
            path_params['id_connector'] = local_var_params['id_connector']  # noqa: E501

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
            '/providers/{id_connector}/sources', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderSources',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_account_types_get(self, id_user, **kwargs):  # noqa: E501
        """Get account types  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_account_types_get(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserAccountTypes
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_account_types_get_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_account_types_get_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Get account types  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_account_types_get_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        :return: tuple(UserAccountTypes, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_account_types_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_account_types_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

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
            '/users/{id_user}/account_types', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAccountTypes',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_account_types_id_account_type_get(self, id_user, id_account_type, **kwargs):  # noqa: E501
        """Get an account type  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_account_types_id_account_type_get(id_user, id_account_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account_type: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AccountType
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_account_types_id_account_type_get_with_http_info(id_user, id_account_type, **kwargs)  # noqa: E501

    def users_id_user_account_types_id_account_type_get_with_http_info(self, id_user, id_account_type, **kwargs):  # noqa: E501
        """Get an account type  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_account_types_id_account_type_get_with_http_info(id_user, id_account_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account_type: (required)
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
        :return: tuple(AccountType, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account_type', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_account_types_id_account_type_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_account_types_id_account_type_get`")  # noqa: E501
        # verify the required parameter 'id_account_type' is set
        if ('id_account_type' not in local_var_params or
                local_var_params['id_account_type'] is None):
            raise ApiValueError("Missing the required parameter `id_account_type` when calling `users_id_user_account_types_id_account_type_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account_type' in local_var_params:
            path_params['id_account_type'] = local_var_params['id_account_type']  # noqa: E501

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
            '/users/{id_user}/account_types/{id_account_type}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AccountType',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_delete(self, id_user, **kwargs):  # noqa: E501
        """Delete all accounts  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_delete(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Account
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_delete_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_accounts_delete_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Delete all accounts  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_delete_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        :return: tuple(Account, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

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
            '/users/{id_user}/accounts', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Account',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_get(self, id_user, **kwargs):  # noqa: E501
        """Get accounts list.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_get(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserAccounts
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_get_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_accounts_get_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Get accounts list.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_get_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        :return: tuple(UserAccounts, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

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
            '/users/{id_user}/accounts', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAccounts',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_categories_get(self, id_user, id_account, **kwargs):  # noqa: E501
        """Get the category  # noqa: E501

        Ressource to get categories for the user's transactions<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_categories_get(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
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
        return self.users_id_user_accounts_id_account_categories_get_with_http_info(id_user, id_account, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_categories_get_with_http_info(self, id_user, id_account, **kwargs):  # noqa: E501
        """Get the category  # noqa: E501

        Ressource to get categories for the user's transactions<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_categories_get_with_http_info(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
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

        all_params = ['id_user', 'id_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_categories_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_categories_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_categories_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/users/{id_user}/accounts/{id_account}/categories', 'GET',
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

    def users_id_user_accounts_id_account_delete(self, id_user, id_account, **kwargs):  # noqa: E501
        """Delete an account.  # noqa: E501

        It deletes a specific account.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_delete(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Account
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_delete_with_http_info(id_user, id_account, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_delete_with_http_info(self, id_user, id_account, **kwargs):  # noqa: E501
        """Delete an account.  # noqa: E501

        It deletes a specific account.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_delete_with_http_info(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
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
        :return: tuple(Account, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_delete`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Account',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_delta_get(self, id_user, id_account, **kwargs):  # noqa: E501
        """Get deltas of accounts  # noqa: E501

        Get account delta between sums of transactions and difference of account balance for the given period.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_delta_get(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param str period: period to group logs
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
        return self.users_id_user_accounts_id_account_delta_get_with_http_info(id_user, id_account, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_delta_get_with_http_info(self, id_user, id_account, **kwargs):  # noqa: E501
        """Get deltas of accounts  # noqa: E501

        Get account delta between sums of transactions and difference of account balance for the given period.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_delta_get_with_http_info(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param str period: period to group logs
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

        all_params = ['id_user', 'id_account', 'min_date', 'max_date', 'period']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_delta_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_delta_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_delta_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

        query_params = []
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'period' in local_var_params:
            query_params.append(('period', local_var_params['period']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/users/{id_user}/accounts/{id_account}/delta', 'GET',
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

    def users_id_user_accounts_id_account_logs_get(self, id_user, id_account, **kwargs):  # noqa: E501
        """Get accounts logs.  # noqa: E501

        Get logs of account. By default, it selects logs for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_logs_get(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
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
        :return: UserConnectionAccountLogs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_logs_get_with_http_info(id_user, id_account, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_logs_get_with_http_info(self, id_user, id_account, **kwargs):  # noqa: E501
        """Get accounts logs.  # noqa: E501

        Get logs of account. By default, it selects logs for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_logs_get_with_http_info(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
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
        :return: tuple(UserConnectionAccountLogs, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'limit', 'offset', 'min_date', 'max_date', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_logs_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_logs_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_logs_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

        query_params = []
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
            '/users/{id_user}/accounts/{id_account}/logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserConnectionAccountLogs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_put(self, id_user, id_account, **kwargs):  # noqa: E501
        """Update an account  # noqa: E501

        It updates a specific account<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_put(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param str expand:
        :param float balance: Balance of the account
        :param bool bookmarked: If the account is bookmarked
        :param bool disabled: If the account is disabled (not synchronized)
        :param bool display: If the account is displayed
        :param str iban: IBAN of the account
        :param str name: Label of the account
        :param str usage: Usage of the account : PRIV, ORGA or ASSO
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Account
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_put_with_http_info(id_user, id_account, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_put_with_http_info(self, id_user, id_account, **kwargs):  # noqa: E501
        """Update an account  # noqa: E501

        It updates a specific account<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_put_with_http_info(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param str expand:
        :param float balance: Balance of the account
        :param bool bookmarked: If the account is bookmarked
        :param bool disabled: If the account is disabled (not synchronized)
        :param bool display: If the account is displayed
        :param str iban: IBAN of the account
        :param str name: Label of the account
        :param str usage: Usage of the account : PRIV, ORGA or ASSO
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Account, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'expand', 'balance', 'bookmarked', 'disabled', 'display', 'iban', 'name', 'usage']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_put`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'balance' in local_var_params:
            form_params.append(('balance', local_var_params['balance']))  # noqa: E501
        if 'bookmarked' in local_var_params:
            form_params.append(('bookmarked', local_var_params['bookmarked']))  # noqa: E501
        if 'disabled' in local_var_params:
            form_params.append(('disabled', local_var_params['disabled']))  # noqa: E501
        if 'display' in local_var_params:
            form_params.append(('display', local_var_params['display']))  # noqa: E501
        if 'iban' in local_var_params:
            form_params.append(('iban', local_var_params['iban']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'usage' in local_var_params:
            form_params.append(('usage', local_var_params['usage']))  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Account',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_sources_get(self, id_user, id_account, **kwargs):  # noqa: E501
        """Get account sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_sources_get(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserAccountSources
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_sources_get_with_http_info(id_user, id_account, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_sources_get_with_http_info(self, id_user, id_account, **kwargs):  # noqa: E501
        """Get account sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_sources_get_with_http_info(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
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
        :return: tuple(UserAccountSources, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_sources_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_sources_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_sources_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/sources', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAccountSources',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactions_delete(self, id_user, id_account, **kwargs):  # noqa: E501
        """Delete transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_delete(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Transaction
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactions_delete_with_http_info(id_user, id_account, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactions_delete_with_http_info(self, id_user, id_account, **kwargs):  # noqa: E501
        """Delete transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_delete_with_http_info(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
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
        :return: tuple(Transaction, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactions_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactions_delete`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactions_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/transactions', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Transaction',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactions_get(self, id_user, id_account, **kwargs):  # noqa: E501
        """Get transactions  # noqa: E501

        Get list of transactions.<br><br>By default, it selects transactions for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_get(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal (inclusive) date
        :param date max_date: maximum (inclusive) date
        :param bool income: filter on income or expenditures
        :param bool deleted: display only deleted transactions
        :param bool all: display all transactions, including deleted ones
        :param datetime last_update: get only transactions updated after the specified datetime
        :param str wording: filter transactions containing the given string
        :param float min_value: minimal (inclusive) value
        :param float max_value: maximum (inclusive) value
        :param str search: search in labels, dates, values and categories
        :param str value: \"XX|-XX\" or \"±XX\"
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserConnectionAccountTransactions
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactions_get_with_http_info(id_user, id_account, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactions_get_with_http_info(self, id_user, id_account, **kwargs):  # noqa: E501
        """Get transactions  # noqa: E501

        Get list of transactions.<br><br>By default, it selects transactions for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_get_with_http_info(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal (inclusive) date
        :param date max_date: maximum (inclusive) date
        :param bool income: filter on income or expenditures
        :param bool deleted: display only deleted transactions
        :param bool all: display all transactions, including deleted ones
        :param datetime last_update: get only transactions updated after the specified datetime
        :param str wording: filter transactions containing the given string
        :param float min_value: minimal (inclusive) value
        :param float max_value: maximum (inclusive) value
        :param str search: search in labels, dates, values and categories
        :param str value: \"XX|-XX\" or \"±XX\"
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
        :return: tuple(UserConnectionAccountTransactions, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'limit', 'offset', 'min_date', 'max_date', 'income', 'deleted', 'all', 'last_update', 'wording', 'min_value', 'max_value', 'search', 'value', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactions_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactions_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactions_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'income' in local_var_params:
            query_params.append(('income', local_var_params['income']))  # noqa: E501
        if 'deleted' in local_var_params:
            query_params.append(('deleted', local_var_params['deleted']))  # noqa: E501
        if 'all' in local_var_params:
            query_params.append(('all', local_var_params['all']))  # noqa: E501
        if 'last_update' in local_var_params:
            query_params.append(('last_update', local_var_params['last_update']))  # noqa: E501
        if 'wording' in local_var_params:
            query_params.append(('wording', local_var_params['wording']))  # noqa: E501
        if 'min_value' in local_var_params:
            query_params.append(('min_value', local_var_params['min_value']))  # noqa: E501
        if 'max_value' in local_var_params:
            query_params.append(('max_value', local_var_params['max_value']))  # noqa: E501
        if 'search' in local_var_params:
            query_params.append(('search', local_var_params['search']))  # noqa: E501
        if 'value' in local_var_params:
            query_params.append(('value', local_var_params['value']))  # noqa: E501
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
            '/users/{id_user}/accounts/{id_account}/transactions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserConnectionAccountTransactions',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactions_id_transaction_informations_delete(self, id_user, id_account, id_transaction, **kwargs):  # noqa: E501
        """Delete all arbitrary key-value pairs of a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_id_transaction_informations_delete(id_user, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactions_id_transaction_informations_delete_with_http_info(id_user, id_account, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactions_id_transaction_informations_delete_with_http_info(self, id_user, id_account, id_transaction, **kwargs):  # noqa: E501
        """Delete all arbitrary key-value pairs of a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_id_transaction_informations_delete_with_http_info(id_user, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'id_transaction', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactions_id_transaction_informations_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_delete`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_delete`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/transactions/{id_transaction}/informations', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactions_id_transaction_informations_get(self, id_user, id_account, id_transaction, **kwargs):  # noqa: E501
        """List all arbitrary key-value pairs on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_id_transaction_informations_get(id_user, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserConnectionTransactionInformations
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactions_id_transaction_informations_get_with_http_info(id_user, id_account, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactions_id_transaction_informations_get_with_http_info(self, id_user, id_account, id_transaction, **kwargs):  # noqa: E501
        """List all arbitrary key-value pairs on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_id_transaction_informations_get_with_http_info(id_user, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
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
        :return: tuple(UserConnectionTransactionInformations, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'id_transaction', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactions_id_transaction_informations_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_get`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/transactions/{id_transaction}/informations', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserConnectionTransactionInformations',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_delete(self, id_user, id_account, id_transaction, id_information, **kwargs):  # noqa: E501
        """Delete a particular key-value pair on a transaction.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_delete(id_user, id_account, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_delete_with_http_info(id_user, id_account, id_transaction, id_information, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_delete_with_http_info(self, id_user, id_account, id_transaction, id_information, **kwargs):  # noqa: E501
        """Delete a particular key-value pair on a transaction.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_delete_with_http_info(id_user, id_account, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'id_transaction', 'id_information', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501
        # verify the required parameter 'id_information' is set
        if ('id_information' not in local_var_params or
                local_var_params['id_information'] is None):
            raise ApiValueError("Missing the required parameter `id_information` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501
        if 'id_information' in local_var_params:
            path_params['id_information'] = local_var_params['id_information']  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/transactions/{id_transaction}/informations/{id_information}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_get(self, id_user, id_account, id_transaction, id_information, **kwargs):  # noqa: E501
        """Get a particular arbitrary key-value pair on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_get(id_user, id_account, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_get_with_http_info(id_user, id_account, id_transaction, id_information, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_get_with_http_info(self, id_user, id_account, id_transaction, id_information, **kwargs):  # noqa: E501
        """Get a particular arbitrary key-value pair on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_get_with_http_info(id_user, id_account, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'id_transaction', 'id_information', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_get`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_get`")  # noqa: E501
        # verify the required parameter 'id_information' is set
        if ('id_information' not in local_var_params or
                local_var_params['id_information'] is None):
            raise ApiValueError("Missing the required parameter `id_information` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_id_information_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501
        if 'id_information' in local_var_params:
            path_params['id_information'] = local_var_params['id_information']  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/transactions/{id_transaction}/informations/{id_information}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactions_id_transaction_informations_put(self, id_user, id_account, id_transaction, **kwargs):  # noqa: E501
        """Add or edit transaction arbitrary key-value pairs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_id_transaction_informations_put(id_user, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactions_id_transaction_informations_put_with_http_info(id_user, id_account, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactions_id_transaction_informations_put_with_http_info(self, id_user, id_account, id_transaction, **kwargs):  # noqa: E501
        """Add or edit transaction arbitrary key-value pairs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_id_transaction_informations_put_with_http_info(id_user, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'id_transaction', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactions_id_transaction_informations_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_put`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_put`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_accounts_id_account_transactions_id_transaction_informations_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/transactions/{id_transaction}/informations', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactions_id_transaction_put(self, id_user, id_account, id_transaction, **kwargs):  # noqa: E501
        """Edit a transaction meta-data  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_id_transaction_put(id_user, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param bool active: if false, transaction isn't considered in analyzisis endpoints (like /balances)
        :param date application_date: change application date of the transaction
        :param str comment: change comment
        :param int id_category: ID of the associated category
        :param str wording: user rewording of the transaction
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Transaction
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactions_id_transaction_put_with_http_info(id_user, id_account, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactions_id_transaction_put_with_http_info(self, id_user, id_account, id_transaction, **kwargs):  # noqa: E501
        """Edit a transaction meta-data  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_id_transaction_put_with_http_info(id_user, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param bool active: if false, transaction isn't considered in analyzisis endpoints (like /balances)
        :param date application_date: change application date of the transaction
        :param str comment: change comment
        :param int id_category: ID of the associated category
        :param str wording: user rewording of the transaction
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Transaction, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'id_transaction', 'expand', 'active', 'application_date', 'comment', 'id_category', 'wording']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactions_id_transaction_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactions_id_transaction_put`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactions_id_transaction_put`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_accounts_id_account_transactions_id_transaction_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'active' in local_var_params:
            form_params.append(('active', local_var_params['active']))  # noqa: E501
        if 'application_date' in local_var_params:
            form_params.append(('application_date', local_var_params['application_date']))  # noqa: E501
        if 'comment' in local_var_params:
            form_params.append(('comment', local_var_params['comment']))  # noqa: E501
        if 'id_category' in local_var_params:
            form_params.append(('id_category', local_var_params['id_category']))  # noqa: E501
        if 'wording' in local_var_params:
            form_params.append(('wording', local_var_params['wording']))  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/transactions/{id_transaction}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Transaction',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactions_post(self, id_user, id_account, date, original_wording, value, **kwargs):  # noqa: E501
        """Create transactions  # noqa: E501

        Create transactions for the supplied account or the account whose id is given with form parameters. It requires an array of transaction dictionaries.<br><br><br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_post(id_user, id_account, date, original_wording, value, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param date date: date of the transaction (required)
        :param str original_wording: label of the transaction (required)
        :param int value: vallue of the transaction (required)
        :param str expand:
        :param bool active: 1 if the transaction should be taken into account by pfm services (default: 1)
        :param bool coming: 1 if the transaction has already been debited (default: 0)
        :param datetime date_scraped: date on which the transaction has been found for the first time. YYYY-MM-DD HH:MM:SS(default: now)
        :param int id_account: account of the transaction. If not supplied, it has to be given in the route
        :param date rdate: realisation date of the transaction (default: value of date)
        :param str state: nature of the transaction (default: new)
        :param str type: type of the transaction (default: unknown)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Transaction
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactions_post_with_http_info(id_user, id_account, date, original_wording, value, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactions_post_with_http_info(self, id_user, id_account, date, original_wording, value, **kwargs):  # noqa: E501
        """Create transactions  # noqa: E501

        Create transactions for the supplied account or the account whose id is given with form parameters. It requires an array of transaction dictionaries.<br><br><br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactions_post_with_http_info(id_user, id_account, date, original_wording, value, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param date date: date of the transaction (required)
        :param str original_wording: label of the transaction (required)
        :param int value: vallue of the transaction (required)
        :param str expand:
        :param bool active: 1 if the transaction should be taken into account by pfm services (default: 1)
        :param bool coming: 1 if the transaction has already been debited (default: 0)
        :param datetime date_scraped: date on which the transaction has been found for the first time. YYYY-MM-DD HH:MM:SS(default: now)
        :param int id_account: account of the transaction. If not supplied, it has to be given in the route
        :param date rdate: realisation date of the transaction (default: value of date)
        :param str state: nature of the transaction (default: new)
        :param str type: type of the transaction (default: unknown)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Transaction, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'date', 'original_wording', 'value', 'expand', 'active', 'coming', 'date_scraped', 'id_account', 'rdate', 'state', 'type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactions_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactions_post`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactions_post`")  # noqa: E501
        # verify the required parameter 'date' is set
        if ('date' not in local_var_params or
                local_var_params['date'] is None):
            raise ApiValueError("Missing the required parameter `date` when calling `users_id_user_accounts_id_account_transactions_post`")  # noqa: E501
        # verify the required parameter 'original_wording' is set
        if ('original_wording' not in local_var_params or
                local_var_params['original_wording'] is None):
            raise ApiValueError("Missing the required parameter `original_wording` when calling `users_id_user_accounts_id_account_transactions_post`")  # noqa: E501
        # verify the required parameter 'value' is set
        if ('value' not in local_var_params or
                local_var_params['value'] is None):
            raise ApiValueError("Missing the required parameter `value` when calling `users_id_user_accounts_id_account_transactions_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'active' in local_var_params:
            form_params.append(('active', local_var_params['active']))  # noqa: E501
        if 'coming' in local_var_params:
            form_params.append(('coming', local_var_params['coming']))  # noqa: E501
        if 'date' in local_var_params:
            form_params.append(('date', local_var_params['date']))  # noqa: E501
        if 'date_scraped' in local_var_params:
            form_params.append(('date_scraped', local_var_params['date_scraped']))  # noqa: E501
        if 'id_account' in local_var_params:
            form_params.append(('id_account', local_var_params['id_account']))  # noqa: E501
        if 'original_wording' in local_var_params:
            form_params.append(('original_wording', local_var_params['original_wording']))  # noqa: E501
        if 'rdate' in local_var_params:
            form_params.append(('rdate', local_var_params['rdate']))  # noqa: E501
        if 'state' in local_var_params:
            form_params.append(('state', local_var_params['state']))  # noqa: E501
        if 'type' in local_var_params:
            form_params.append(('type', local_var_params['type']))  # noqa: E501
        if 'value' in local_var_params:
            form_params.append(('value', local_var_params['value']))  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/transactions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Transaction',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactionsclusters_get(self, id_user, id_account, **kwargs):  # noqa: E501
        """Get clustered transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactionsclusters_get(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserAccountTransactionsclusters
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactionsclusters_get_with_http_info(id_user, id_account, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactionsclusters_get_with_http_info(self, id_user, id_account, **kwargs):  # noqa: E501
        """Get clustered transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactionsclusters_get_with_http_info(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
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
        :return: tuple(UserAccountTransactionsclusters, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactionsclusters_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactionsclusters_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactionsclusters_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/transactionsclusters', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAccountTransactionsclusters',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_delete(self, id_user, id_account, id_transactionscluster, **kwargs):  # noqa: E501
        """Delete a clustered transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_delete(id_user, id_account, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transactionscluster: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionsCluster
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_delete_with_http_info(id_user, id_account, id_transactionscluster, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_delete_with_http_info(self, id_user, id_account, id_transactionscluster, **kwargs):  # noqa: E501
        """Delete a clustered transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_delete_with_http_info(id_user, id_account, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transactionscluster: (required)
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
        :return: tuple(TransactionsCluster, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'id_transactionscluster', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_delete`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_delete`")  # noqa: E501
        # verify the required parameter 'id_transactionscluster' is set
        if ('id_transactionscluster' not in local_var_params or
                local_var_params['id_transactionscluster'] is None):
            raise ApiValueError("Missing the required parameter `id_transactionscluster` when calling `users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transactionscluster' in local_var_params:
            path_params['id_transactionscluster'] = local_var_params['id_transactionscluster']  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/transactionsclusters/{id_transactionscluster}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsCluster',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_put(self, id_user, id_account, id_transactionscluster, **kwargs):  # noqa: E501
        """Edit a clustered transaction  # noqa: E501

        Form params : - next_date (date): Date of transaction - mean_amount (decimal): Mean Amount - wording (string): name of transaction - id_account (id): related account - id_category (id): related category - enabled (bool): is enabled<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_put(id_user, id_account, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transactionscluster: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionsCluster
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_put_with_http_info(id_user, id_account, id_transactionscluster, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_put_with_http_info(self, id_user, id_account, id_transactionscluster, **kwargs):  # noqa: E501
        """Edit a clustered transaction  # noqa: E501

        Form params : - next_date (date): Date of transaction - mean_amount (decimal): Mean Amount - wording (string): name of transaction - id_account (id): related account - id_category (id): related category - enabled (bool): is enabled<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_put_with_http_info(id_user, id_account, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param int id_transactionscluster: (required)
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
        :return: tuple(TransactionsCluster, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'id_transactionscluster', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_put`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_put`")  # noqa: E501
        # verify the required parameter 'id_transactionscluster' is set
        if ('id_transactionscluster' not in local_var_params or
                local_var_params['id_transactionscluster'] is None):
            raise ApiValueError("Missing the required parameter `id_transactionscluster` when calling `users_id_user_accounts_id_account_transactionsclusters_id_transactionscluster_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transactionscluster' in local_var_params:
            path_params['id_transactionscluster'] = local_var_params['id_transactionscluster']  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/transactionsclusters/{id_transactionscluster}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsCluster',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_id_account_transactionsclusters_post(self, id_user, id_account, **kwargs):  # noqa: E501
        """Create clustered transaction  # noqa: E501

        Form params : - next_date (date) required: Date of transaction - mean_amount (decimal) required: Mean Amount - wording (string) required: name of transaction - id_account (id) required: related account<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactionsclusters_post(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionsCluster
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_id_account_transactionsclusters_post_with_http_info(id_user, id_account, **kwargs)  # noqa: E501

    def users_id_user_accounts_id_account_transactionsclusters_post_with_http_info(self, id_user, id_account, **kwargs):  # noqa: E501
        """Create clustered transaction  # noqa: E501

        Form params : - next_date (date) required: Date of transaction - mean_amount (decimal) required: Mean Amount - wording (string) required: name of transaction - id_account (id) required: related account<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_id_account_transactionsclusters_post_with_http_info(id_user, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_account: (required)
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
        :return: tuple(TransactionsCluster, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_account', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_id_account_transactionsclusters_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_id_account_transactionsclusters_post`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_accounts_id_account_transactionsclusters_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

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
            '/users/{id_user}/accounts/{id_account}/transactionsclusters', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsCluster',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_post(self, id_user, name, **kwargs):  # noqa: E501
        """Create an account  # noqa: E501

        This endpoint creates an account related to a connection or not.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_post(id_user, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str name: name of account (required)
        :param str expand:
        :param float balance: balance of account
        :param str iban: IBAN of account
        :param int id_connection: the connection to attach to the account
        :param str id_currency: the currency of the account (default: 'EUR')
        :param str number: number of account
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Account
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_post_with_http_info(id_user, name, **kwargs)  # noqa: E501

    def users_id_user_accounts_post_with_http_info(self, id_user, name, **kwargs):  # noqa: E501
        """Create an account  # noqa: E501

        This endpoint creates an account related to a connection or not.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_post_with_http_info(id_user, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str name: name of account (required)
        :param str expand:
        :param float balance: balance of account
        :param str iban: IBAN of account
        :param int id_connection: the connection to attach to the account
        :param str id_currency: the currency of the account (default: 'EUR')
        :param str number: number of account
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Account, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'name', 'expand', 'balance', 'iban', 'id_connection', 'id_currency', 'number']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_post`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in local_var_params or
                local_var_params['name'] is None):
            raise ApiValueError("Missing the required parameter `name` when calling `users_id_user_accounts_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'balance' in local_var_params:
            form_params.append(('balance', local_var_params['balance']))  # noqa: E501
        if 'iban' in local_var_params:
            form_params.append(('iban', local_var_params['iban']))  # noqa: E501
        if 'id_connection' in local_var_params:
            form_params.append(('id_connection', local_var_params['id_connection']))  # noqa: E501
        if 'id_currency' in local_var_params:
            form_params.append(('id_currency', local_var_params['id_currency']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'number' in local_var_params:
            form_params.append(('number', local_var_params['number']))  # noqa: E501

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
            '/users/{id_user}/accounts', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Account',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_accounts_put(self, id_user, **kwargs):  # noqa: E501
        """Update many accounts at once  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_put(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Account
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_accounts_put_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_accounts_put_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Update many accounts at once  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_accounts_put_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        :return: tuple(Account, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_accounts_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_accounts_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

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
            '/users/{id_user}/accounts', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Account',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_alerts_get(self, id_user, **kwargs):  # noqa: E501
        """Get alerts  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_alerts_get(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserAlerts
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_alerts_get_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_alerts_get_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Get alerts  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_alerts_get_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        :return: tuple(UserAlerts, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_alerts_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_alerts_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

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
            '/users/{id_user}/alerts', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAlerts',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_categories_full_get(self, id_user, **kwargs):  # noqa: E501
        """Get the category  # noqa: E501

        Ressource to get categories<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_categories_full_get(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserCategoriesFull
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_categories_full_get_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_categories_full_get_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Get the category  # noqa: E501

        Ressource to get categories<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_categories_full_get_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        :return: tuple(UserCategoriesFull, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_categories_full_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_categories_full_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

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
            '/users/{id_user}/categories/full', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserCategoriesFull',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_categories_full_id_full_delete(self, id_user, id_full, **kwargs):  # noqa: E501
        """Delete a user-created transaction category  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_categories_full_id_full_delete(id_user, id_full, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_full: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Category
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_categories_full_id_full_delete_with_http_info(id_user, id_full, **kwargs)  # noqa: E501

    def users_id_user_categories_full_id_full_delete_with_http_info(self, id_user, id_full, **kwargs):  # noqa: E501
        """Delete a user-created transaction category  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_categories_full_id_full_delete_with_http_info(id_user, id_full, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_full: (required)
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
        :return: tuple(Category, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_full', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_categories_full_id_full_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_categories_full_id_full_delete`")  # noqa: E501
        # verify the required parameter 'id_full' is set
        if ('id_full' not in local_var_params or
                local_var_params['id_full'] is None):
            raise ApiValueError("Missing the required parameter `id_full` when calling `users_id_user_categories_full_id_full_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_full' in local_var_params:
            path_params['id_full'] = local_var_params['id_full']  # noqa: E501

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
            '/users/{id_user}/categories/full/{id_full}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Category',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_categories_full_id_full_put(self, id_user, id_full, **kwargs):  # noqa: E501
        """Modify a user-created category  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_categories_full_id_full_put(id_user, id_full, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_full: (required)
        :param str expand:
        :param str accountant_account: Accountant account number.
        :param str hide: Hide (but not delete) a category. Must be 0, 1 or toggle.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Category
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_categories_full_id_full_put_with_http_info(id_user, id_full, **kwargs)  # noqa: E501

    def users_id_user_categories_full_id_full_put_with_http_info(self, id_user, id_full, **kwargs):  # noqa: E501
        """Modify a user-created category  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_categories_full_id_full_put_with_http_info(id_user, id_full, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_full: (required)
        :param str expand:
        :param str accountant_account: Accountant account number.
        :param str hide: Hide (but not delete) a category. Must be 0, 1 or toggle.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Category, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_full', 'expand', 'accountant_account', 'hide']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_categories_full_id_full_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_categories_full_id_full_put`")  # noqa: E501
        # verify the required parameter 'id_full' is set
        if ('id_full' not in local_var_params or
                local_var_params['id_full'] is None):
            raise ApiValueError("Missing the required parameter `id_full` when calling `users_id_user_categories_full_id_full_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_full' in local_var_params:
            path_params['id_full'] = local_var_params['id_full']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'accountant_account' in local_var_params:
            form_params.append(('accountant_account', local_var_params['accountant_account']))  # noqa: E501
        if 'hide' in local_var_params:
            form_params.append(('hide', local_var_params['hide']))  # noqa: E501

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
            '/users/{id_user}/categories/full/{id_full}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Category',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_categories_full_post(self, id_user, **kwargs):  # noqa: E501
        """Create a new transaction category  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_categories_full_post(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param str accountant_account: Accountant account number.
        :param str color: Color of the category.
        :param int id_parent_category: ID of the parent category.
        :param int id_parent_category_in_menu: ID of the parent category to be displayed.
        :param bool income: Is an income category. If null, this is both an income and an expense category.
        :param str name: Name of the category.
        :param bool refundable: This category accepts opposite sign of transactions.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Category
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_categories_full_post_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_categories_full_post_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Create a new transaction category  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_categories_full_post_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param str accountant_account: Accountant account number.
        :param str color: Color of the category.
        :param int id_parent_category: ID of the parent category.
        :param int id_parent_category_in_menu: ID of the parent category to be displayed.
        :param bool income: Is an income category. If null, this is both an income and an expense category.
        :param str name: Name of the category.
        :param bool refundable: This category accepts opposite sign of transactions.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Category, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'expand', 'accountant_account', 'color', 'id_parent_category', 'id_parent_category_in_menu', 'income', 'name', 'refundable']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_categories_full_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_categories_full_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'accountant_account' in local_var_params:
            form_params.append(('accountant_account', local_var_params['accountant_account']))  # noqa: E501
        if 'color' in local_var_params:
            form_params.append(('color', local_var_params['color']))  # noqa: E501
        if 'id_parent_category' in local_var_params:
            form_params.append(('id_parent_category', local_var_params['id_parent_category']))  # noqa: E501
        if 'id_parent_category_in_menu' in local_var_params:
            form_params.append(('id_parent_category_in_menu', local_var_params['id_parent_category_in_menu']))  # noqa: E501
        if 'income' in local_var_params:
            form_params.append(('income', local_var_params['income']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'refundable' in local_var_params:
            form_params.append(('refundable', local_var_params['refundable']))  # noqa: E501

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
            '/users/{id_user}/categories/full', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Category',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_categories_get(self, id_user, **kwargs):  # noqa: E501
        """Get the category  # noqa: E501

        Ressource to get categories for the user's transactions<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_categories_get(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        return self.users_id_user_categories_get_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_categories_get_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Get the category  # noqa: E501

        Ressource to get categories for the user's transactions<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_categories_get_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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

        all_params = ['id_user']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_categories_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_categories_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/users/{id_user}/categories', 'GET',
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

    def users_id_user_connections_delete(self, id_user, **kwargs):  # noqa: E501
        """Delete all connections  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_delete(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Connection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_delete_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_connections_delete_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Delete all connections  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_delete_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        :return: tuple(Connection, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

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
            '/users/{id_user}/connections', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Connection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_get(self, id_user, **kwargs):  # noqa: E501
        """Get connections  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_get(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ProviderConnections
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_get_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_connections_get_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Get connections  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_get_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        :return: tuple(ProviderConnections, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

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
            '/users/{id_user}/connections', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ProviderConnections',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_delete(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Delete all accounts  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_delete(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Account
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_delete_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_delete_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Delete all accounts  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_delete_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
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
        :return: tuple(Account, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_delete`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Account',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_get(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Get accounts list.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_get(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserAccounts
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_get_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_get_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Get accounts list.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_get_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
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
        :return: tuple(UserAccounts, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAccounts',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_categories_get(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Get the category  # noqa: E501

        Ressource to get categories for the user's transactions<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_categories_get(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
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
        return self.users_id_user_connections_id_connection_accounts_id_account_categories_get_with_http_info(id_user, id_connection, id_account, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_categories_get_with_http_info(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Get the category  # noqa: E501

        Ressource to get categories for the user's transactions<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_categories_get_with_http_info(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
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

        all_params = ['id_user', 'id_connection', 'id_account']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_categories_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_categories_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_categories_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_categories_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/categories', 'GET',
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

    def users_id_user_connections_id_connection_accounts_id_account_delete(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Delete an account.  # noqa: E501

        It deletes a specific account.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_delete(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Account
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_delete_with_http_info(id_user, id_connection, id_account, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_delete_with_http_info(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Delete an account.  # noqa: E501

        It deletes a specific account.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_delete_with_http_info(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
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
        :return: tuple(Account, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_delete`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_delete`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Account',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_delta_get(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Get deltas of accounts  # noqa: E501

        Get account delta between sums of transactions and difference of account balance for the given period.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_delta_get(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param str period: period to group logs
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
        return self.users_id_user_connections_id_connection_accounts_id_account_delta_get_with_http_info(id_user, id_connection, id_account, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_delta_get_with_http_info(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Get deltas of accounts  # noqa: E501

        Get account delta between sums of transactions and difference of account balance for the given period.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_delta_get_with_http_info(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param str period: period to group logs
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

        all_params = ['id_user', 'id_connection', 'id_account', 'min_date', 'max_date', 'period']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_delta_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_delta_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_delta_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_delta_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

        query_params = []
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'period' in local_var_params:
            query_params.append(('period', local_var_params['period']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/delta', 'GET',
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

    def users_id_user_connections_id_connection_accounts_id_account_logs_get(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Get accounts logs.  # noqa: E501

        Get logs of account. By default, it selects logs for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_logs_get(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
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
        :return: UserConnectionAccountLogs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_logs_get_with_http_info(id_user, id_connection, id_account, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_logs_get_with_http_info(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Get accounts logs.  # noqa: E501

        Get logs of account. By default, it selects logs for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_logs_get_with_http_info(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
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
        :return: tuple(UserConnectionAccountLogs, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'limit', 'offset', 'min_date', 'max_date', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_logs_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_logs_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_logs_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_logs_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

        query_params = []
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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserConnectionAccountLogs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_put(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Update an account  # noqa: E501

        It updates a specific account<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_put(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param str expand:
        :param float balance: Balance of the account
        :param bool bookmarked: If the account is bookmarked
        :param bool disabled: If the account is disabled (not synchronized)
        :param bool display: If the account is displayed
        :param str iban: IBAN of the account
        :param str name: Label of the account
        :param str usage: Usage of the account : PRIV, ORGA or ASSO
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Account
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_put_with_http_info(id_user, id_connection, id_account, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_put_with_http_info(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Update an account  # noqa: E501

        It updates a specific account<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_put_with_http_info(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param str expand:
        :param float balance: Balance of the account
        :param bool bookmarked: If the account is bookmarked
        :param bool disabled: If the account is disabled (not synchronized)
        :param bool display: If the account is displayed
        :param str iban: IBAN of the account
        :param str name: Label of the account
        :param str usage: Usage of the account : PRIV, ORGA or ASSO
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Account, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'expand', 'balance', 'bookmarked', 'disabled', 'display', 'iban', 'name', 'usage']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_put`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_put`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'balance' in local_var_params:
            form_params.append(('balance', local_var_params['balance']))  # noqa: E501
        if 'bookmarked' in local_var_params:
            form_params.append(('bookmarked', local_var_params['bookmarked']))  # noqa: E501
        if 'disabled' in local_var_params:
            form_params.append(('disabled', local_var_params['disabled']))  # noqa: E501
        if 'display' in local_var_params:
            form_params.append(('display', local_var_params['display']))  # noqa: E501
        if 'iban' in local_var_params:
            form_params.append(('iban', local_var_params['iban']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'usage' in local_var_params:
            form_params.append(('usage', local_var_params['usage']))  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Account',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_sources_get(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Get account sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_sources_get(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserAccountSources
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_sources_get_with_http_info(id_user, id_connection, id_account, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_sources_get_with_http_info(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Get account sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_sources_get_with_http_info(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
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
        :return: tuple(UserAccountSources, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_sources_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_sources_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_sources_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_sources_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/sources', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAccountSources',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactions_delete(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Delete transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_delete(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Transaction
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactions_delete_with_http_info(id_user, id_connection, id_account, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactions_delete_with_http_info(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Delete transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_delete_with_http_info(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
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
        :return: tuple(Transaction, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactions_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_delete`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_delete`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactions', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Transaction',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactions_get(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Get transactions  # noqa: E501

        Get list of transactions.<br><br>By default, it selects transactions for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_get(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal (inclusive) date
        :param date max_date: maximum (inclusive) date
        :param bool income: filter on income or expenditures
        :param bool deleted: display only deleted transactions
        :param bool all: display all transactions, including deleted ones
        :param datetime last_update: get only transactions updated after the specified datetime
        :param str wording: filter transactions containing the given string
        :param float min_value: minimal (inclusive) value
        :param float max_value: maximum (inclusive) value
        :param str search: search in labels, dates, values and categories
        :param str value: \"XX|-XX\" or \"±XX\"
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserConnectionAccountTransactions
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactions_get_with_http_info(id_user, id_connection, id_account, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactions_get_with_http_info(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Get transactions  # noqa: E501

        Get list of transactions.<br><br>By default, it selects transactions for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_get_with_http_info(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal (inclusive) date
        :param date max_date: maximum (inclusive) date
        :param bool income: filter on income or expenditures
        :param bool deleted: display only deleted transactions
        :param bool all: display all transactions, including deleted ones
        :param datetime last_update: get only transactions updated after the specified datetime
        :param str wording: filter transactions containing the given string
        :param float min_value: minimal (inclusive) value
        :param float max_value: maximum (inclusive) value
        :param str search: search in labels, dates, values and categories
        :param str value: \"XX|-XX\" or \"±XX\"
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
        :return: tuple(UserConnectionAccountTransactions, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'limit', 'offset', 'min_date', 'max_date', 'income', 'deleted', 'all', 'last_update', 'wording', 'min_value', 'max_value', 'search', 'value', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactions_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'income' in local_var_params:
            query_params.append(('income', local_var_params['income']))  # noqa: E501
        if 'deleted' in local_var_params:
            query_params.append(('deleted', local_var_params['deleted']))  # noqa: E501
        if 'all' in local_var_params:
            query_params.append(('all', local_var_params['all']))  # noqa: E501
        if 'last_update' in local_var_params:
            query_params.append(('last_update', local_var_params['last_update']))  # noqa: E501
        if 'wording' in local_var_params:
            query_params.append(('wording', local_var_params['wording']))  # noqa: E501
        if 'min_value' in local_var_params:
            query_params.append(('min_value', local_var_params['min_value']))  # noqa: E501
        if 'max_value' in local_var_params:
            query_params.append(('max_value', local_var_params['max_value']))  # noqa: E501
        if 'search' in local_var_params:
            query_params.append(('search', local_var_params['search']))  # noqa: E501
        if 'value' in local_var_params:
            query_params.append(('value', local_var_params['value']))  # noqa: E501
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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserConnectionAccountTransactions',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_delete(self, id_user, id_connection, id_account, id_transaction, **kwargs):  # noqa: E501
        """Delete all arbitrary key-value pairs of a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_delete(id_user, id_connection, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_delete_with_http_info(id_user, id_connection, id_account, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_delete_with_http_info(self, id_user, id_connection, id_account, id_transaction, **kwargs):  # noqa: E501
        """Delete all arbitrary key-value pairs of a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_delete_with_http_info(id_user, id_connection, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'id_transaction', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_delete`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_delete`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_delete`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactions/{id_transaction}/informations', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_get(self, id_user, id_connection, id_account, id_transaction, **kwargs):  # noqa: E501
        """List all arbitrary key-value pairs on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_get(id_user, id_connection, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserConnectionTransactionInformations
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_get_with_http_info(id_user, id_connection, id_account, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_get_with_http_info(self, id_user, id_connection, id_account, id_transaction, **kwargs):  # noqa: E501
        """List all arbitrary key-value pairs on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_get_with_http_info(id_user, id_connection, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
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
        :return: tuple(UserConnectionTransactionInformations, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'id_transaction', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_get`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactions/{id_transaction}/informations', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserConnectionTransactionInformations',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_delete(self, id_user, id_connection, id_account, id_transaction, id_information, **kwargs):  # noqa: E501
        """Delete a particular key-value pair on a transaction.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_delete(id_user, id_connection, id_account, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_delete_with_http_info(id_user, id_connection, id_account, id_transaction, id_information, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_delete_with_http_info(self, id_user, id_connection, id_account, id_transaction, id_information, **kwargs):  # noqa: E501
        """Delete a particular key-value pair on a transaction.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_delete_with_http_info(id_user, id_connection, id_account, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'id_transaction', 'id_information', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501
        # verify the required parameter 'id_information' is set
        if ('id_information' not in local_var_params or
                local_var_params['id_information'] is None):
            raise ApiValueError("Missing the required parameter `id_information` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501
        if 'id_information' in local_var_params:
            path_params['id_information'] = local_var_params['id_information']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactions/{id_transaction}/informations/{id_information}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_get(self, id_user, id_connection, id_account, id_transaction, id_information, **kwargs):  # noqa: E501
        """Get a particular arbitrary key-value pair on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_get(id_user, id_connection, id_account, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_get_with_http_info(id_user, id_connection, id_account, id_transaction, id_information, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_get_with_http_info(self, id_user, id_connection, id_account, id_transaction, id_information, **kwargs):  # noqa: E501
        """Get a particular arbitrary key-value pair on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_get_with_http_info(id_user, id_connection, id_account, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'id_transaction', 'id_information', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_get`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_get`")  # noqa: E501
        # verify the required parameter 'id_information' is set
        if ('id_information' not in local_var_params or
                local_var_params['id_information'] is None):
            raise ApiValueError("Missing the required parameter `id_information` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_id_information_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501
        if 'id_information' in local_var_params:
            path_params['id_information'] = local_var_params['id_information']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactions/{id_transaction}/informations/{id_information}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_put(self, id_user, id_connection, id_account, id_transaction, **kwargs):  # noqa: E501
        """Add or edit transaction arbitrary key-value pairs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_put(id_user, id_connection, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_put_with_http_info(id_user, id_connection, id_account, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_put_with_http_info(self, id_user, id_connection, id_account, id_transaction, **kwargs):  # noqa: E501
        """Add or edit transaction arbitrary key-value pairs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_put_with_http_info(id_user, id_connection, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'id_transaction', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_put`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_put`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_put`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_informations_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactions/{id_transaction}/informations', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_put(self, id_user, id_connection, id_account, id_transaction, **kwargs):  # noqa: E501
        """Edit a transaction meta-data  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_put(id_user, id_connection, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param bool active: if false, transaction isn't considered in analyzisis endpoints (like /balances)
        :param date application_date: change application date of the transaction
        :param str comment: change comment
        :param int id_category: ID of the associated category
        :param str wording: user rewording of the transaction
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Transaction
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_put_with_http_info(id_user, id_connection, id_account, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_put_with_http_info(self, id_user, id_connection, id_account, id_transaction, **kwargs):  # noqa: E501
        """Edit a transaction meta-data  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_put_with_http_info(id_user, id_connection, id_account, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param bool active: if false, transaction isn't considered in analyzisis endpoints (like /balances)
        :param date application_date: change application date of the transaction
        :param str comment: change comment
        :param int id_category: ID of the associated category
        :param str wording: user rewording of the transaction
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Transaction, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'id_transaction', 'expand', 'active', 'application_date', 'comment', 'id_category', 'wording']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_put`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_put`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_put`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_id_transaction_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'active' in local_var_params:
            form_params.append(('active', local_var_params['active']))  # noqa: E501
        if 'application_date' in local_var_params:
            form_params.append(('application_date', local_var_params['application_date']))  # noqa: E501
        if 'comment' in local_var_params:
            form_params.append(('comment', local_var_params['comment']))  # noqa: E501
        if 'id_category' in local_var_params:
            form_params.append(('id_category', local_var_params['id_category']))  # noqa: E501
        if 'wording' in local_var_params:
            form_params.append(('wording', local_var_params['wording']))  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactions/{id_transaction}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Transaction',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactions_post(self, id_user, id_connection, id_account, date, original_wording, value, **kwargs):  # noqa: E501
        """Create transactions  # noqa: E501

        Create transactions for the supplied account or the account whose id is given with form parameters. It requires an array of transaction dictionaries.<br><br><br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_post(id_user, id_connection, id_account, date, original_wording, value, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param date date: date of the transaction (required)
        :param str original_wording: label of the transaction (required)
        :param int value: vallue of the transaction (required)
        :param str expand:
        :param bool active: 1 if the transaction should be taken into account by pfm services (default: 1)
        :param bool coming: 1 if the transaction has already been debited (default: 0)
        :param datetime date_scraped: date on which the transaction has been found for the first time. YYYY-MM-DD HH:MM:SS(default: now)
        :param int id_account: account of the transaction. If not supplied, it has to be given in the route
        :param date rdate: realisation date of the transaction (default: value of date)
        :param str state: nature of the transaction (default: new)
        :param str type: type of the transaction (default: unknown)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Transaction
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactions_post_with_http_info(id_user, id_connection, id_account, date, original_wording, value, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactions_post_with_http_info(self, id_user, id_connection, id_account, date, original_wording, value, **kwargs):  # noqa: E501
        """Create transactions  # noqa: E501

        Create transactions for the supplied account or the account whose id is given with form parameters. It requires an array of transaction dictionaries.<br><br><br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactions_post_with_http_info(id_user, id_connection, id_account, date, original_wording, value, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param date date: date of the transaction (required)
        :param str original_wording: label of the transaction (required)
        :param int value: vallue of the transaction (required)
        :param str expand:
        :param bool active: 1 if the transaction should be taken into account by pfm services (default: 1)
        :param bool coming: 1 if the transaction has already been debited (default: 0)
        :param datetime date_scraped: date on which the transaction has been found for the first time. YYYY-MM-DD HH:MM:SS(default: now)
        :param int id_account: account of the transaction. If not supplied, it has to be given in the route
        :param date rdate: realisation date of the transaction (default: value of date)
        :param str state: nature of the transaction (default: new)
        :param str type: type of the transaction (default: unknown)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Transaction, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'date', 'original_wording', 'value', 'expand', 'active', 'coming', 'date_scraped', 'id_account', 'rdate', 'state', 'type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactions_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_post`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_post`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_post`")  # noqa: E501
        # verify the required parameter 'date' is set
        if ('date' not in local_var_params or
                local_var_params['date'] is None):
            raise ApiValueError("Missing the required parameter `date` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_post`")  # noqa: E501
        # verify the required parameter 'original_wording' is set
        if ('original_wording' not in local_var_params or
                local_var_params['original_wording'] is None):
            raise ApiValueError("Missing the required parameter `original_wording` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_post`")  # noqa: E501
        # verify the required parameter 'value' is set
        if ('value' not in local_var_params or
                local_var_params['value'] is None):
            raise ApiValueError("Missing the required parameter `value` when calling `users_id_user_connections_id_connection_accounts_id_account_transactions_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'active' in local_var_params:
            form_params.append(('active', local_var_params['active']))  # noqa: E501
        if 'coming' in local_var_params:
            form_params.append(('coming', local_var_params['coming']))  # noqa: E501
        if 'date' in local_var_params:
            form_params.append(('date', local_var_params['date']))  # noqa: E501
        if 'date_scraped' in local_var_params:
            form_params.append(('date_scraped', local_var_params['date_scraped']))  # noqa: E501
        if 'id_account' in local_var_params:
            form_params.append(('id_account', local_var_params['id_account']))  # noqa: E501
        if 'original_wording' in local_var_params:
            form_params.append(('original_wording', local_var_params['original_wording']))  # noqa: E501
        if 'rdate' in local_var_params:
            form_params.append(('rdate', local_var_params['rdate']))  # noqa: E501
        if 'state' in local_var_params:
            form_params.append(('state', local_var_params['state']))  # noqa: E501
        if 'type' in local_var_params:
            form_params.append(('type', local_var_params['type']))  # noqa: E501
        if 'value' in local_var_params:
            form_params.append(('value', local_var_params['value']))  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Transaction',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_get(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Get clustered transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_get(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserAccountTransactionsclusters
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_get_with_http_info(id_user, id_connection, id_account, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_get_with_http_info(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Get clustered transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_get_with_http_info(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
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
        :return: tuple(UserAccountTransactionsclusters, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_get`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactionsclusters', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAccountTransactionsclusters',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_delete(self, id_user, id_connection, id_account, id_transactionscluster, **kwargs):  # noqa: E501
        """Delete a clustered transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_delete(id_user, id_connection, id_account, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transactionscluster: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionsCluster
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_delete_with_http_info(id_user, id_connection, id_account, id_transactionscluster, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_delete_with_http_info(self, id_user, id_connection, id_account, id_transactionscluster, **kwargs):  # noqa: E501
        """Delete a clustered transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_delete_with_http_info(id_user, id_connection, id_account, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transactionscluster: (required)
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
        :return: tuple(TransactionsCluster, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'id_transactionscluster', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_delete`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_delete`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_delete`")  # noqa: E501
        # verify the required parameter 'id_transactionscluster' is set
        if ('id_transactionscluster' not in local_var_params or
                local_var_params['id_transactionscluster'] is None):
            raise ApiValueError("Missing the required parameter `id_transactionscluster` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transactionscluster' in local_var_params:
            path_params['id_transactionscluster'] = local_var_params['id_transactionscluster']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactionsclusters/{id_transactionscluster}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsCluster',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_put(self, id_user, id_connection, id_account, id_transactionscluster, **kwargs):  # noqa: E501
        """Edit a clustered transaction  # noqa: E501

        Form params : - next_date (date): Date of transaction - mean_amount (decimal): Mean Amount - wording (string): name of transaction - id_account (id): related account - id_category (id): related category - enabled (bool): is enabled<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_put(id_user, id_connection, id_account, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transactionscluster: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionsCluster
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_put_with_http_info(id_user, id_connection, id_account, id_transactionscluster, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_put_with_http_info(self, id_user, id_connection, id_account, id_transactionscluster, **kwargs):  # noqa: E501
        """Edit a clustered transaction  # noqa: E501

        Form params : - next_date (date): Date of transaction - mean_amount (decimal): Mean Amount - wording (string): name of transaction - id_account (id): related account - id_category (id): related category - enabled (bool): is enabled<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_put_with_http_info(id_user, id_connection, id_account, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param int id_transactionscluster: (required)
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
        :return: tuple(TransactionsCluster, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'id_transactionscluster', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_put`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_put`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_put`")  # noqa: E501
        # verify the required parameter 'id_transactionscluster' is set
        if ('id_transactionscluster' not in local_var_params or
                local_var_params['id_transactionscluster'] is None):
            raise ApiValueError("Missing the required parameter `id_transactionscluster` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_id_transactionscluster_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501
        if 'id_transactionscluster' in local_var_params:
            path_params['id_transactionscluster'] = local_var_params['id_transactionscluster']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactionsclusters/{id_transactionscluster}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsCluster',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_post(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Create clustered transaction  # noqa: E501

        Form params : - next_date (date) required: Date of transaction - mean_amount (decimal) required: Mean Amount - wording (string) required: name of transaction - id_account (id) required: related account<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_post(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionsCluster
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_post_with_http_info(id_user, id_connection, id_account, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_post_with_http_info(self, id_user, id_connection, id_account, **kwargs):  # noqa: E501
        """Create clustered transaction  # noqa: E501

        Form params : - next_date (date) required: Date of transaction - mean_amount (decimal) required: Mean Amount - wording (string) required: name of transaction - id_account (id) required: related account<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_post_with_http_info(id_user, id_connection, id_account, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_account: (required)
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
        :return: tuple(TransactionsCluster, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_account', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_post`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_post`")  # noqa: E501
        # verify the required parameter 'id_account' is set
        if ('id_account' not in local_var_params or
                local_var_params['id_account'] is None):
            raise ApiValueError("Missing the required parameter `id_account` when calling `users_id_user_connections_id_connection_accounts_id_account_transactionsclusters_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_account' in local_var_params:
            path_params['id_account'] = local_var_params['id_account']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts/{id_account}/transactionsclusters', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsCluster',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_post(self, id_user, id_connection, name, **kwargs):  # noqa: E501
        """Create an account  # noqa: E501

        This endpoint creates an account related to a connection or not.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_post(id_user, id_connection, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str name: name of account (required)
        :param str expand:
        :param float balance: balance of account
        :param str iban: IBAN of account
        :param int id_connection: the connection to attach to the account
        :param str id_currency: the currency of the account (default: 'EUR')
        :param str number: number of account
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Account
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_post_with_http_info(id_user, id_connection, name, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_post_with_http_info(self, id_user, id_connection, name, **kwargs):  # noqa: E501
        """Create an account  # noqa: E501

        This endpoint creates an account related to a connection or not.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_post_with_http_info(id_user, id_connection, name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str name: name of account (required)
        :param str expand:
        :param float balance: balance of account
        :param str iban: IBAN of account
        :param int id_connection: the connection to attach to the account
        :param str id_currency: the currency of the account (default: 'EUR')
        :param str number: number of account
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Account, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'name', 'expand', 'balance', 'iban', 'id_connection', 'id_currency', 'number']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_post`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_post`")  # noqa: E501
        # verify the required parameter 'name' is set
        if ('name' not in local_var_params or
                local_var_params['name'] is None):
            raise ApiValueError("Missing the required parameter `name` when calling `users_id_user_connections_id_connection_accounts_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'balance' in local_var_params:
            form_params.append(('balance', local_var_params['balance']))  # noqa: E501
        if 'iban' in local_var_params:
            form_params.append(('iban', local_var_params['iban']))  # noqa: E501
        if 'id_connection' in local_var_params:
            form_params.append(('id_connection', local_var_params['id_connection']))  # noqa: E501
        if 'id_currency' in local_var_params:
            form_params.append(('id_currency', local_var_params['id_currency']))  # noqa: E501
        if 'name' in local_var_params:
            form_params.append(('name', local_var_params['name']))  # noqa: E501
        if 'number' in local_var_params:
            form_params.append(('number', local_var_params['number']))  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Account',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_accounts_put(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Update many accounts at once  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_put(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Account
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_accounts_put_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_accounts_put_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Update many accounts at once  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_accounts_put_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
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
        :return: tuple(Account, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_accounts_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_accounts_put`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_accounts_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/accounts', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Account',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_delete(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Delete a connection.  # noqa: E501

        This endpoint deletes a connection and all related accounts and transactions.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_delete(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Connection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_delete_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_delete_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Delete a connection.  # noqa: E501

        This endpoint deletes a connection and all related accounts and transactions.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_delete_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
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
        :return: tuple(Connection, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_delete`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Connection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_informations_get(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Get connection additionnal informations  # noqa: E501

        <br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_informations_get(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserConnectionInformations
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_informations_get_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_informations_get_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Get connection additionnal informations  # noqa: E501

        <br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_informations_get_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
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
        :return: tuple(UserConnectionInformations, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_informations_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_informations_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_informations_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/informations', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserConnectionInformations',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_logs_get(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Get connection logs  # noqa: E501

        Get logs about connections.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_logs_get(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param int state: state of user
        :param str period: period to group logs
        :param int id_user2: ID of a user
        :param int id_connection2: ID of a connection
        :param int id_connector: ID of a connector
        :param bool charged: consider only logs for charged connectors
        :param int id_source: ID of a source
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectionLogs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_logs_get_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_logs_get_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Get connection logs  # noqa: E501

        Get logs about connections.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_logs_get_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param int state: state of user
        :param str period: period to group logs
        :param int id_user2: ID of a user
        :param int id_connection2: ID of a connection
        :param int id_connector: ID of a connector
        :param bool charged: consider only logs for charged connectors
        :param int id_source: ID of a source
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
        :return: tuple(ConnectionLogs, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'limit', 'offset', 'min_date', 'max_date', 'state', 'period', 'id_user2', 'id_connection2', 'id_connector', 'charged', 'id_source', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_logs_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_logs_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_logs_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'state' in local_var_params:
            query_params.append(('state', local_var_params['state']))  # noqa: E501
        if 'period' in local_var_params:
            query_params.append(('period', local_var_params['period']))  # noqa: E501
        if 'id_user2' in local_var_params:
            query_params.append(('id_user', local_var_params['id_user2']))  # noqa: E501
        if 'id_connection2' in local_var_params:
            query_params.append(('id_connection', local_var_params['id_connection2']))  # noqa: E501
        if 'id_connector' in local_var_params:
            query_params.append(('id_connector', local_var_params['id_connector']))  # noqa: E501
        if 'charged' in local_var_params:
            query_params.append(('charged', local_var_params['charged']))  # noqa: E501
        if 'id_source' in local_var_params:
            query_params.append(('id_source', local_var_params['id_source']))  # noqa: E501
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
            '/users/{id_user}/connections/{id_connection}/logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectionLogs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_post(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Update a connection.  # noqa: E501

        Give new parameters to change on the configuration of this connection (for example \"password\").<br><br>It tests connection to website, and if it fails, a 400 response is given with the error code \"wrongpass\" or \"websiteUnavailable\".<br><br>You can also supply meta-parameters on connection, like 'active' or 'expire'.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_post(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str expand:
        :param bool active: Set if the connection synchronisation is active
        :param bool decoupled: Try to update a connection with the decoupled error
        :param datetime expire: Set expiration of the connection to this date
        :param str login: Set login to this new login
        :param str password: Set password to this new password
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Connection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_post_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_post_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Update a connection.  # noqa: E501

        Give new parameters to change on the configuration of this connection (for example \"password\").<br><br>It tests connection to website, and if it fails, a 400 response is given with the error code \"wrongpass\" or \"websiteUnavailable\".<br><br>You can also supply meta-parameters on connection, like 'active' or 'expire'.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_post_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str expand:
        :param bool active: Set if the connection synchronisation is active
        :param bool decoupled: Try to update a connection with the decoupled error
        :param datetime expire: Set expiration of the connection to this date
        :param str login: Set login to this new login
        :param str password: Set password to this new password
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Connection, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'expand', 'active', 'decoupled', 'expire', 'login', 'password']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_post`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'active' in local_var_params:
            form_params.append(('active', local_var_params['active']))  # noqa: E501
        if 'decoupled' in local_var_params:
            form_params.append(('decoupled', local_var_params['decoupled']))  # noqa: E501
        if 'expire' in local_var_params:
            form_params.append(('expire', local_var_params['expire']))  # noqa: E501
        if 'login' in local_var_params:
            form_params.append(('login', local_var_params['login']))  # noqa: E501
        if 'password' in local_var_params:
            form_params.append(('password', local_var_params['password']))  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Connection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_put(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Force synchronisation of a connection.  # noqa: E501

        We suggest to pass parameter expand=accounts[transactions] to get all *new* and *updated* transactions.<br><br>Query params: - expand (string): fields to expand - last_update (dateTime): if supplied, get transactions inserted since this date<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_put(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Connection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_put_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_put_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Force synchronisation of a connection.  # noqa: E501

        We suggest to pass parameter expand=accounts[transactions] to get all *new* and *updated* transactions.<br><br>Query params: - expand (string): fields to expand - last_update (dateTime): if supplied, get transactions inserted since this date<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_put_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
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
        :return: tuple(Connection, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_put`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Connection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_sources_get(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Get connection sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_sources_get(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserAccountSources
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_sources_get_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_sources_get_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Get connection sources  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_sources_get_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
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
        :return: tuple(UserAccountSources, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_sources_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_sources_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_sources_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/sources', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAccountSources',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_sources_id_source_delete(self, id_user, id_connection, id_source, **kwargs):  # noqa: E501
        """Disable a connection source  # noqa: E501

        This will make it so the specified source will not be synchronized anymore.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_sources_id_source_delete(id_user, id_connection, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_source: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectionSource
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_sources_id_source_delete_with_http_info(id_user, id_connection, id_source, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_sources_id_source_delete_with_http_info(self, id_user, id_connection, id_source, **kwargs):  # noqa: E501
        """Disable a connection source  # noqa: E501

        This will make it so the specified source will not be synchronized anymore.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_sources_id_source_delete_with_http_info(id_user, id_connection, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_source: (required)
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
        :return: tuple(ConnectionSource, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_source', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_sources_id_source_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_sources_id_source_delete`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_sources_id_source_delete`")  # noqa: E501
        # verify the required parameter 'id_source' is set
        if ('id_source' not in local_var_params or
                local_var_params['id_source'] is None):
            raise ApiValueError("Missing the required parameter `id_source` when calling `users_id_user_connections_id_connection_sources_id_source_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_source' in local_var_params:
            path_params['id_source'] = local_var_params['id_source']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/sources/{id_source}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectionSource',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_sources_id_source_post(self, id_user, id_connection, id_source, **kwargs):  # noqa: E501
        """Enable connection source  # noqa: E501

        This will make it so the specified source will be able to be synchronized.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_sources_id_source_post(id_user, id_connection, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_source: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectionSource
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_sources_id_source_post_with_http_info(id_user, id_connection, id_source, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_sources_id_source_post_with_http_info(self, id_user, id_connection, id_source, **kwargs):  # noqa: E501
        """Enable connection source  # noqa: E501

        This will make it so the specified source will be able to be synchronized.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_sources_id_source_post_with_http_info(id_user, id_connection, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_source: (required)
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
        :return: tuple(ConnectionSource, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_source', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_sources_id_source_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_sources_id_source_post`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_sources_id_source_post`")  # noqa: E501
        # verify the required parameter 'id_source' is set
        if ('id_source' not in local_var_params or
                local_var_params['id_source'] is None):
            raise ApiValueError("Missing the required parameter `id_source` when calling `users_id_user_connections_id_connection_sources_id_source_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_source' in local_var_params:
            path_params['id_source'] = local_var_params['id_source']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/sources/{id_source}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectionSource',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_sources_id_source_put(self, id_user, id_connection, id_source, **kwargs):  # noqa: E501
        """Enable connection source  # noqa: E501

        This will make it so the specified source will be able to be synchronized.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_sources_id_source_put(id_user, id_connection, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_source: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectionSource
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_sources_id_source_put_with_http_info(id_user, id_connection, id_source, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_sources_id_source_put_with_http_info(self, id_user, id_connection, id_source, **kwargs):  # noqa: E501
        """Enable connection source  # noqa: E501

        This will make it so the specified source will be able to be synchronized.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_sources_id_source_put_with_http_info(id_user, id_connection, id_source, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_source: (required)
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
        :return: tuple(ConnectionSource, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_source', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_sources_id_source_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_sources_id_source_put`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_sources_id_source_put`")  # noqa: E501
        # verify the required parameter 'id_source' is set
        if ('id_source' not in local_var_params or
                local_var_params['id_source'] is None):
            raise ApiValueError("Missing the required parameter `id_source` when calling `users_id_user_connections_id_connection_sources_id_source_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_source' in local_var_params:
            path_params['id_source'] = local_var_params['id_source']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/sources/{id_source}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectionSource',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactions_delete(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Delete transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_delete(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Transaction
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactions_delete_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactions_delete_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Delete transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_delete_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
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
        :return: tuple(Transaction, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactions_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactions_delete`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactions_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/transactions', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Transaction',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactions_get(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Get transactions  # noqa: E501

        Get list of transactions.<br><br>By default, it selects transactions for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_get(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal (inclusive) date
        :param date max_date: maximum (inclusive) date
        :param bool income: filter on income or expenditures
        :param bool deleted: display only deleted transactions
        :param bool all: display all transactions, including deleted ones
        :param datetime last_update: get only transactions updated after the specified datetime
        :param str wording: filter transactions containing the given string
        :param float min_value: minimal (inclusive) value
        :param float max_value: maximum (inclusive) value
        :param str search: search in labels, dates, values and categories
        :param str value: \"XX|-XX\" or \"±XX\"
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserConnectionAccountTransactions
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactions_get_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactions_get_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Get transactions  # noqa: E501

        Get list of transactions.<br><br>By default, it selects transactions for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_get_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal (inclusive) date
        :param date max_date: maximum (inclusive) date
        :param bool income: filter on income or expenditures
        :param bool deleted: display only deleted transactions
        :param bool all: display all transactions, including deleted ones
        :param datetime last_update: get only transactions updated after the specified datetime
        :param str wording: filter transactions containing the given string
        :param float min_value: minimal (inclusive) value
        :param float max_value: maximum (inclusive) value
        :param str search: search in labels, dates, values and categories
        :param str value: \"XX|-XX\" or \"±XX\"
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
        :return: tuple(UserConnectionAccountTransactions, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'limit', 'offset', 'min_date', 'max_date', 'income', 'deleted', 'all', 'last_update', 'wording', 'min_value', 'max_value', 'search', 'value', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactions_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactions_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactions_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'income' in local_var_params:
            query_params.append(('income', local_var_params['income']))  # noqa: E501
        if 'deleted' in local_var_params:
            query_params.append(('deleted', local_var_params['deleted']))  # noqa: E501
        if 'all' in local_var_params:
            query_params.append(('all', local_var_params['all']))  # noqa: E501
        if 'last_update' in local_var_params:
            query_params.append(('last_update', local_var_params['last_update']))  # noqa: E501
        if 'wording' in local_var_params:
            query_params.append(('wording', local_var_params['wording']))  # noqa: E501
        if 'min_value' in local_var_params:
            query_params.append(('min_value', local_var_params['min_value']))  # noqa: E501
        if 'max_value' in local_var_params:
            query_params.append(('max_value', local_var_params['max_value']))  # noqa: E501
        if 'search' in local_var_params:
            query_params.append(('search', local_var_params['search']))  # noqa: E501
        if 'value' in local_var_params:
            query_params.append(('value', local_var_params['value']))  # noqa: E501
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
            '/users/{id_user}/connections/{id_connection}/transactions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserConnectionAccountTransactions',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactions_id_transaction_informations_delete(self, id_user, id_connection, id_transaction, **kwargs):  # noqa: E501
        """Delete all arbitrary key-value pairs of a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_id_transaction_informations_delete(id_user, id_connection, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactions_id_transaction_informations_delete_with_http_info(id_user, id_connection, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactions_id_transaction_informations_delete_with_http_info(self, id_user, id_connection, id_transaction, **kwargs):  # noqa: E501
        """Delete all arbitrary key-value pairs of a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_id_transaction_informations_delete_with_http_info(id_user, id_connection, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transaction: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_transaction', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactions_id_transaction_informations_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_delete`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_delete`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/transactions/{id_transaction}/informations', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactions_id_transaction_informations_get(self, id_user, id_connection, id_transaction, **kwargs):  # noqa: E501
        """List all arbitrary key-value pairs on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_id_transaction_informations_get(id_user, id_connection, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserConnectionTransactionInformations
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactions_id_transaction_informations_get_with_http_info(id_user, id_connection, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactions_id_transaction_informations_get_with_http_info(self, id_user, id_connection, id_transaction, **kwargs):  # noqa: E501
        """List all arbitrary key-value pairs on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_id_transaction_informations_get_with_http_info(id_user, id_connection, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transaction: (required)
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
        :return: tuple(UserConnectionTransactionInformations, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_transaction', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactions_id_transaction_informations_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_get`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/transactions/{id_transaction}/informations', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserConnectionTransactionInformations',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_delete(self, id_user, id_connection, id_transaction, id_information, **kwargs):  # noqa: E501
        """Delete a particular key-value pair on a transaction.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_delete(id_user, id_connection, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_delete_with_http_info(id_user, id_connection, id_transaction, id_information, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_delete_with_http_info(self, id_user, id_connection, id_transaction, id_information, **kwargs):  # noqa: E501
        """Delete a particular key-value pair on a transaction.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_delete_with_http_info(id_user, id_connection, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_transaction', 'id_information', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501
        # verify the required parameter 'id_information' is set
        if ('id_information' not in local_var_params or
                local_var_params['id_information'] is None):
            raise ApiValueError("Missing the required parameter `id_information` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501
        if 'id_information' in local_var_params:
            path_params['id_information'] = local_var_params['id_information']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/transactions/{id_transaction}/informations/{id_information}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_get(self, id_user, id_connection, id_transaction, id_information, **kwargs):  # noqa: E501
        """Get a particular arbitrary key-value pair on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_get(id_user, id_connection, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_get_with_http_info(id_user, id_connection, id_transaction, id_information, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_get_with_http_info(self, id_user, id_connection, id_transaction, id_information, **kwargs):  # noqa: E501
        """Get a particular arbitrary key-value pair on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_get_with_http_info(id_user, id_connection, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_transaction', 'id_information', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_get`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_get`")  # noqa: E501
        # verify the required parameter 'id_information' is set
        if ('id_information' not in local_var_params or
                local_var_params['id_information'] is None):
            raise ApiValueError("Missing the required parameter `id_information` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_id_information_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501
        if 'id_information' in local_var_params:
            path_params['id_information'] = local_var_params['id_information']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/transactions/{id_transaction}/informations/{id_information}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactions_id_transaction_informations_put(self, id_user, id_connection, id_transaction, **kwargs):  # noqa: E501
        """Add or edit transaction arbitrary key-value pairs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_id_transaction_informations_put(id_user, id_connection, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactions_id_transaction_informations_put_with_http_info(id_user, id_connection, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactions_id_transaction_informations_put_with_http_info(self, id_user, id_connection, id_transaction, **kwargs):  # noqa: E501
        """Add or edit transaction arbitrary key-value pairs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_id_transaction_informations_put_with_http_info(id_user, id_connection, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transaction: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_transaction', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactions_id_transaction_informations_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_put`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_put`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_connections_id_connection_transactions_id_transaction_informations_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/transactions/{id_transaction}/informations', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactions_id_transaction_put(self, id_user, id_connection, id_transaction, **kwargs):  # noqa: E501
        """Edit a transaction meta-data  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_id_transaction_put(id_user, id_connection, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param bool active: if false, transaction isn't considered in analyzisis endpoints (like /balances)
        :param date application_date: change application date of the transaction
        :param str comment: change comment
        :param int id_category: ID of the associated category
        :param str wording: user rewording of the transaction
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Transaction
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactions_id_transaction_put_with_http_info(id_user, id_connection, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactions_id_transaction_put_with_http_info(self, id_user, id_connection, id_transaction, **kwargs):  # noqa: E501
        """Edit a transaction meta-data  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_id_transaction_put_with_http_info(id_user, id_connection, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transaction: (required)
        :param str expand:
        :param bool active: if false, transaction isn't considered in analyzisis endpoints (like /balances)
        :param date application_date: change application date of the transaction
        :param str comment: change comment
        :param int id_category: ID of the associated category
        :param str wording: user rewording of the transaction
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Transaction, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_transaction', 'expand', 'active', 'application_date', 'comment', 'id_category', 'wording']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactions_id_transaction_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactions_id_transaction_put`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactions_id_transaction_put`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_connections_id_connection_transactions_id_transaction_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'active' in local_var_params:
            form_params.append(('active', local_var_params['active']))  # noqa: E501
        if 'application_date' in local_var_params:
            form_params.append(('application_date', local_var_params['application_date']))  # noqa: E501
        if 'comment' in local_var_params:
            form_params.append(('comment', local_var_params['comment']))  # noqa: E501
        if 'id_category' in local_var_params:
            form_params.append(('id_category', local_var_params['id_category']))  # noqa: E501
        if 'wording' in local_var_params:
            form_params.append(('wording', local_var_params['wording']))  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/transactions/{id_transaction}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Transaction',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactions_post(self, id_user, id_connection, date, original_wording, value, **kwargs):  # noqa: E501
        """Create transactions  # noqa: E501

        Create transactions for the supplied account or the account whose id is given with form parameters. It requires an array of transaction dictionaries.<br><br><br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_post(id_user, id_connection, date, original_wording, value, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param date date: date of the transaction (required)
        :param str original_wording: label of the transaction (required)
        :param int value: vallue of the transaction (required)
        :param str expand:
        :param bool active: 1 if the transaction should be taken into account by pfm services (default: 1)
        :param bool coming: 1 if the transaction has already been debited (default: 0)
        :param datetime date_scraped: date on which the transaction has been found for the first time. YYYY-MM-DD HH:MM:SS(default: now)
        :param int id_account: account of the transaction. If not supplied, it has to be given in the route
        :param date rdate: realisation date of the transaction (default: value of date)
        :param str state: nature of the transaction (default: new)
        :param str type: type of the transaction (default: unknown)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Transaction
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactions_post_with_http_info(id_user, id_connection, date, original_wording, value, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactions_post_with_http_info(self, id_user, id_connection, date, original_wording, value, **kwargs):  # noqa: E501
        """Create transactions  # noqa: E501

        Create transactions for the supplied account or the account whose id is given with form parameters. It requires an array of transaction dictionaries.<br><br><br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactions_post_with_http_info(id_user, id_connection, date, original_wording, value, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param date date: date of the transaction (required)
        :param str original_wording: label of the transaction (required)
        :param int value: vallue of the transaction (required)
        :param str expand:
        :param bool active: 1 if the transaction should be taken into account by pfm services (default: 1)
        :param bool coming: 1 if the transaction has already been debited (default: 0)
        :param datetime date_scraped: date on which the transaction has been found for the first time. YYYY-MM-DD HH:MM:SS(default: now)
        :param int id_account: account of the transaction. If not supplied, it has to be given in the route
        :param date rdate: realisation date of the transaction (default: value of date)
        :param str state: nature of the transaction (default: new)
        :param str type: type of the transaction (default: unknown)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Transaction, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'date', 'original_wording', 'value', 'expand', 'active', 'coming', 'date_scraped', 'id_account', 'rdate', 'state', 'type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactions_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactions_post`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactions_post`")  # noqa: E501
        # verify the required parameter 'date' is set
        if ('date' not in local_var_params or
                local_var_params['date'] is None):
            raise ApiValueError("Missing the required parameter `date` when calling `users_id_user_connections_id_connection_transactions_post`")  # noqa: E501
        # verify the required parameter 'original_wording' is set
        if ('original_wording' not in local_var_params or
                local_var_params['original_wording'] is None):
            raise ApiValueError("Missing the required parameter `original_wording` when calling `users_id_user_connections_id_connection_transactions_post`")  # noqa: E501
        # verify the required parameter 'value' is set
        if ('value' not in local_var_params or
                local_var_params['value'] is None):
            raise ApiValueError("Missing the required parameter `value` when calling `users_id_user_connections_id_connection_transactions_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'active' in local_var_params:
            form_params.append(('active', local_var_params['active']))  # noqa: E501
        if 'coming' in local_var_params:
            form_params.append(('coming', local_var_params['coming']))  # noqa: E501
        if 'date' in local_var_params:
            form_params.append(('date', local_var_params['date']))  # noqa: E501
        if 'date_scraped' in local_var_params:
            form_params.append(('date_scraped', local_var_params['date_scraped']))  # noqa: E501
        if 'id_account' in local_var_params:
            form_params.append(('id_account', local_var_params['id_account']))  # noqa: E501
        if 'original_wording' in local_var_params:
            form_params.append(('original_wording', local_var_params['original_wording']))  # noqa: E501
        if 'rdate' in local_var_params:
            form_params.append(('rdate', local_var_params['rdate']))  # noqa: E501
        if 'state' in local_var_params:
            form_params.append(('state', local_var_params['state']))  # noqa: E501
        if 'type' in local_var_params:
            form_params.append(('type', local_var_params['type']))  # noqa: E501
        if 'value' in local_var_params:
            form_params.append(('value', local_var_params['value']))  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/transactions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Transaction',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactionsclusters_get(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Get clustered transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactionsclusters_get(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserAccountTransactionsclusters
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactionsclusters_get_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactionsclusters_get_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Get clustered transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactionsclusters_get_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
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
        :return: tuple(UserAccountTransactionsclusters, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactionsclusters_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactionsclusters_get`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactionsclusters_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/transactionsclusters', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAccountTransactionsclusters',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_delete(self, id_user, id_connection, id_transactionscluster, **kwargs):  # noqa: E501
        """Delete a clustered transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_delete(id_user, id_connection, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transactionscluster: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionsCluster
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_delete_with_http_info(id_user, id_connection, id_transactionscluster, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_delete_with_http_info(self, id_user, id_connection, id_transactionscluster, **kwargs):  # noqa: E501
        """Delete a clustered transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_delete_with_http_info(id_user, id_connection, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transactionscluster: (required)
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
        :return: tuple(TransactionsCluster, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_transactionscluster', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_delete`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_delete`")  # noqa: E501
        # verify the required parameter 'id_transactionscluster' is set
        if ('id_transactionscluster' not in local_var_params or
                local_var_params['id_transactionscluster'] is None):
            raise ApiValueError("Missing the required parameter `id_transactionscluster` when calling `users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_transactionscluster' in local_var_params:
            path_params['id_transactionscluster'] = local_var_params['id_transactionscluster']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/transactionsclusters/{id_transactionscluster}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsCluster',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_put(self, id_user, id_connection, id_transactionscluster, **kwargs):  # noqa: E501
        """Edit a clustered transaction  # noqa: E501

        Form params : - next_date (date): Date of transaction - mean_amount (decimal): Mean Amount - wording (string): name of transaction - id_account (id): related account - id_category (id): related category - enabled (bool): is enabled<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_put(id_user, id_connection, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transactionscluster: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionsCluster
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_put_with_http_info(id_user, id_connection, id_transactionscluster, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_put_with_http_info(self, id_user, id_connection, id_transactionscluster, **kwargs):  # noqa: E501
        """Edit a clustered transaction  # noqa: E501

        Form params : - next_date (date): Date of transaction - mean_amount (decimal): Mean Amount - wording (string): name of transaction - id_account (id): related account - id_category (id): related category - enabled (bool): is enabled<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_put_with_http_info(id_user, id_connection, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param int id_transactionscluster: (required)
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
        :return: tuple(TransactionsCluster, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'id_transactionscluster', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_put`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_put`")  # noqa: E501
        # verify the required parameter 'id_transactionscluster' is set
        if ('id_transactionscluster' not in local_var_params or
                local_var_params['id_transactionscluster'] is None):
            raise ApiValueError("Missing the required parameter `id_transactionscluster` when calling `users_id_user_connections_id_connection_transactionsclusters_id_transactionscluster_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501
        if 'id_transactionscluster' in local_var_params:
            path_params['id_transactionscluster'] = local_var_params['id_transactionscluster']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/transactionsclusters/{id_transactionscluster}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsCluster',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_id_connection_transactionsclusters_post(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Create clustered transaction  # noqa: E501

        Form params : - next_date (date) required: Date of transaction - mean_amount (decimal) required: Mean Amount - wording (string) required: name of transaction - id_account (id) required: related account<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactionsclusters_post(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionsCluster
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_id_connection_transactionsclusters_post_with_http_info(id_user, id_connection, **kwargs)  # noqa: E501

    def users_id_user_connections_id_connection_transactionsclusters_post_with_http_info(self, id_user, id_connection, **kwargs):  # noqa: E501
        """Create clustered transaction  # noqa: E501

        Form params : - next_date (date) required: Date of transaction - mean_amount (decimal) required: Mean Amount - wording (string) required: name of transaction - id_account (id) required: related account<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_id_connection_transactionsclusters_post_with_http_info(id_user, id_connection, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_connection: (required)
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
        :return: tuple(TransactionsCluster, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_connection', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_id_connection_transactionsclusters_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_id_connection_transactionsclusters_post`")  # noqa: E501
        # verify the required parameter 'id_connection' is set
        if ('id_connection' not in local_var_params or
                local_var_params['id_connection'] is None):
            raise ApiValueError("Missing the required parameter `id_connection` when calling `users_id_user_connections_id_connection_transactionsclusters_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_connection' in local_var_params:
            path_params['id_connection'] = local_var_params['id_connection']  # noqa: E501

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
            '/users/{id_user}/connections/{id_connection}/transactionsclusters', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsCluster',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_connections_post(self, id_user, **kwargs):  # noqa: E501
        """Add a new connection.  # noqa: E501

        Create a new connection to a given bank or provider. You have to give all needed parameters (use /banks/ID/fields or /providers/ID/fields to get them).<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_post(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str source: optional comma-separated list of sources to use for the connection synchronization
        :param str expand:
        :param str connector_uuid: optional uuid of the connector (replaces id_connector)
        :param int id_connector: ID of the connector
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Connection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_connections_post_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_connections_post_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Add a new connection.  # noqa: E501

        Create a new connection to a given bank or provider. You have to give all needed parameters (use /banks/ID/fields or /providers/ID/fields to get them).<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_connections_post_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str source: optional comma-separated list of sources to use for the connection synchronization
        :param str expand:
        :param str connector_uuid: optional uuid of the connector (replaces id_connector)
        :param int id_connector: ID of the connector
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Connection, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'source', 'expand', 'connector_uuid', 'id_connector']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_connections_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_connections_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

        query_params = []
        if 'source' in local_var_params:
            query_params.append(('source', local_var_params['source']))  # noqa: E501
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'connector_uuid' in local_var_params:
            form_params.append(('connector_uuid', local_var_params['connector_uuid']))  # noqa: E501
        if 'id_connector' in local_var_params:
            form_params.append(('id_connector', local_var_params['id_connector']))  # noqa: E501

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
            '/users/{id_user}/connections', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Connection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_forecast_get(self, id_user, **kwargs):  # noqa: E501
        """Get forecast  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_forecast_get(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        return self.users_id_user_forecast_get_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_forecast_get_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Get forecast  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_forecast_get_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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

        all_params = ['id_user']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_forecast_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_forecast_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # Authentication setting
        auth_settings = ['Authorization']  # noqa: E501

        return self.api_client.call_api(
            '/users/{id_user}/forecast', 'GET',
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

    def users_id_user_logs_get(self, id_user, **kwargs):  # noqa: E501
        """Get connection logs  # noqa: E501

        Get logs about connections.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_logs_get(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param int state: state of user
        :param str period: period to group logs
        :param int id_user2: ID of a user
        :param int id_connection: ID of a connection
        :param int id_connector: ID of a connector
        :param bool charged: consider only logs for charged connectors
        :param int id_source: ID of a source
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ConnectionLogs
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_logs_get_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_logs_get_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Get connection logs  # noqa: E501

        Get logs about connections.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_logs_get_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal date
        :param date max_date: maximum date
        :param int state: state of user
        :param str period: period to group logs
        :param int id_user2: ID of a user
        :param int id_connection: ID of a connection
        :param int id_connector: ID of a connector
        :param bool charged: consider only logs for charged connectors
        :param int id_source: ID of a source
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
        :return: tuple(ConnectionLogs, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'limit', 'offset', 'min_date', 'max_date', 'state', 'period', 'id_user2', 'id_connection', 'id_connector', 'charged', 'id_source', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_logs_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_logs_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'state' in local_var_params:
            query_params.append(('state', local_var_params['state']))  # noqa: E501
        if 'period' in local_var_params:
            query_params.append(('period', local_var_params['period']))  # noqa: E501
        if 'id_user2' in local_var_params:
            query_params.append(('id_user', local_var_params['id_user2']))  # noqa: E501
        if 'id_connection' in local_var_params:
            query_params.append(('id_connection', local_var_params['id_connection']))  # noqa: E501
        if 'id_connector' in local_var_params:
            query_params.append(('id_connector', local_var_params['id_connector']))  # noqa: E501
        if 'charged' in local_var_params:
            query_params.append(('charged', local_var_params['charged']))  # noqa: E501
        if 'id_source' in local_var_params:
            query_params.append(('id_source', local_var_params['id_source']))  # noqa: E501
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
            '/users/{id_user}/logs', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ConnectionLogs',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactions_delete(self, id_user, **kwargs):  # noqa: E501
        """Delete transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_delete(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Transaction
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactions_delete_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_transactions_delete_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Delete transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_delete_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        :return: tuple(Transaction, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactions_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactions_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

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
            '/users/{id_user}/transactions', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Transaction',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactions_get(self, id_user, **kwargs):  # noqa: E501
        """Get transactions  # noqa: E501

        Get list of transactions.<br><br>By default, it selects transactions for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_get(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal (inclusive) date
        :param date max_date: maximum (inclusive) date
        :param bool income: filter on income or expenditures
        :param bool deleted: display only deleted transactions
        :param bool all: display all transactions, including deleted ones
        :param datetime last_update: get only transactions updated after the specified datetime
        :param str wording: filter transactions containing the given string
        :param float min_value: minimal (inclusive) value
        :param float max_value: maximum (inclusive) value
        :param str search: search in labels, dates, values and categories
        :param str value: \"XX|-XX\" or \"±XX\"
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserConnectionAccountTransactions
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactions_get_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_transactions_get_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Get transactions  # noqa: E501

        Get list of transactions.<br><br>By default, it selects transactions for the last month. You can use \"min_date\" and \"max_date\" to change boundary dates.<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_get_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int limit: limit number of results
        :param int offset: offset of first result
        :param date min_date: minimal (inclusive) date
        :param date max_date: maximum (inclusive) date
        :param bool income: filter on income or expenditures
        :param bool deleted: display only deleted transactions
        :param bool all: display all transactions, including deleted ones
        :param datetime last_update: get only transactions updated after the specified datetime
        :param str wording: filter transactions containing the given string
        :param float min_value: minimal (inclusive) value
        :param float max_value: maximum (inclusive) value
        :param str search: search in labels, dates, values and categories
        :param str value: \"XX|-XX\" or \"±XX\"
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
        :return: tuple(UserConnectionAccountTransactions, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'limit', 'offset', 'min_date', 'max_date', 'income', 'deleted', 'all', 'last_update', 'wording', 'min_value', 'max_value', 'search', 'value', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactions_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactions_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

        query_params = []
        if 'limit' in local_var_params:
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'offset' in local_var_params:
            query_params.append(('offset', local_var_params['offset']))  # noqa: E501
        if 'min_date' in local_var_params:
            query_params.append(('min_date', local_var_params['min_date']))  # noqa: E501
        if 'max_date' in local_var_params:
            query_params.append(('max_date', local_var_params['max_date']))  # noqa: E501
        if 'income' in local_var_params:
            query_params.append(('income', local_var_params['income']))  # noqa: E501
        if 'deleted' in local_var_params:
            query_params.append(('deleted', local_var_params['deleted']))  # noqa: E501
        if 'all' in local_var_params:
            query_params.append(('all', local_var_params['all']))  # noqa: E501
        if 'last_update' in local_var_params:
            query_params.append(('last_update', local_var_params['last_update']))  # noqa: E501
        if 'wording' in local_var_params:
            query_params.append(('wording', local_var_params['wording']))  # noqa: E501
        if 'min_value' in local_var_params:
            query_params.append(('min_value', local_var_params['min_value']))  # noqa: E501
        if 'max_value' in local_var_params:
            query_params.append(('max_value', local_var_params['max_value']))  # noqa: E501
        if 'search' in local_var_params:
            query_params.append(('search', local_var_params['search']))  # noqa: E501
        if 'value' in local_var_params:
            query_params.append(('value', local_var_params['value']))  # noqa: E501
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
            '/users/{id_user}/transactions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserConnectionAccountTransactions',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactions_id_transaction_informations_delete(self, id_user, id_transaction, **kwargs):  # noqa: E501
        """Delete all arbitrary key-value pairs of a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_id_transaction_informations_delete(id_user, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transaction: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactions_id_transaction_informations_delete_with_http_info(id_user, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_transactions_id_transaction_informations_delete_with_http_info(self, id_user, id_transaction, **kwargs):  # noqa: E501
        """Delete all arbitrary key-value pairs of a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_id_transaction_informations_delete_with_http_info(id_user, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transaction: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_transaction', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactions_id_transaction_informations_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactions_id_transaction_informations_delete`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_transactions_id_transaction_informations_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

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
            '/users/{id_user}/transactions/{id_transaction}/informations', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactions_id_transaction_informations_get(self, id_user, id_transaction, **kwargs):  # noqa: E501
        """List all arbitrary key-value pairs on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_id_transaction_informations_get(id_user, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transaction: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserConnectionTransactionInformations
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactions_id_transaction_informations_get_with_http_info(id_user, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_transactions_id_transaction_informations_get_with_http_info(self, id_user, id_transaction, **kwargs):  # noqa: E501
        """List all arbitrary key-value pairs on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_id_transaction_informations_get_with_http_info(id_user, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transaction: (required)
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
        :return: tuple(UserConnectionTransactionInformations, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_transaction', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactions_id_transaction_informations_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactions_id_transaction_informations_get`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_transactions_id_transaction_informations_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

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
            '/users/{id_user}/transactions/{id_transaction}/informations', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserConnectionTransactionInformations',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactions_id_transaction_informations_id_information_delete(self, id_user, id_transaction, id_information, **kwargs):  # noqa: E501
        """Delete a particular key-value pair on a transaction.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_id_transaction_informations_id_information_delete(id_user, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactions_id_transaction_informations_id_information_delete_with_http_info(id_user, id_transaction, id_information, **kwargs)  # noqa: E501

    def users_id_user_transactions_id_transaction_informations_id_information_delete_with_http_info(self, id_user, id_transaction, id_information, **kwargs):  # noqa: E501
        """Delete a particular key-value pair on a transaction.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_id_transaction_informations_id_information_delete_with_http_info(id_user, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_transaction', 'id_information', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactions_id_transaction_informations_id_information_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501
        # verify the required parameter 'id_information' is set
        if ('id_information' not in local_var_params or
                local_var_params['id_information'] is None):
            raise ApiValueError("Missing the required parameter `id_information` when calling `users_id_user_transactions_id_transaction_informations_id_information_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501
        if 'id_information' in local_var_params:
            path_params['id_information'] = local_var_params['id_information']  # noqa: E501

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
            '/users/{id_user}/transactions/{id_transaction}/informations/{id_information}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactions_id_transaction_informations_id_information_get(self, id_user, id_transaction, id_information, **kwargs):  # noqa: E501
        """Get a particular arbitrary key-value pair on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_id_transaction_informations_id_information_get(id_user, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactions_id_transaction_informations_id_information_get_with_http_info(id_user, id_transaction, id_information, **kwargs)  # noqa: E501

    def users_id_user_transactions_id_transaction_informations_id_information_get_with_http_info(self, id_user, id_transaction, id_information, **kwargs):  # noqa: E501
        """Get a particular arbitrary key-value pair on a transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_id_transaction_informations_id_information_get_with_http_info(id_user, id_transaction, id_information, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transaction: (required)
        :param int id_information: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_transaction', 'id_information', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactions_id_transaction_informations_id_information_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactions_id_transaction_informations_id_information_get`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_transactions_id_transaction_informations_id_information_get`")  # noqa: E501
        # verify the required parameter 'id_information' is set
        if ('id_information' not in local_var_params or
                local_var_params['id_information'] is None):
            raise ApiValueError("Missing the required parameter `id_information` when calling `users_id_user_transactions_id_transaction_informations_id_information_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501
        if 'id_information' in local_var_params:
            path_params['id_information'] = local_var_params['id_information']  # noqa: E501

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
            '/users/{id_user}/transactions/{id_transaction}/informations/{id_information}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactions_id_transaction_informations_put(self, id_user, id_transaction, **kwargs):  # noqa: E501
        """Add or edit transaction arbitrary key-value pairs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_id_transaction_informations_put(id_user, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transaction: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionInformation
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactions_id_transaction_informations_put_with_http_info(id_user, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_transactions_id_transaction_informations_put_with_http_info(self, id_user, id_transaction, **kwargs):  # noqa: E501
        """Add or edit transaction arbitrary key-value pairs  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_id_transaction_informations_put_with_http_info(id_user, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transaction: (required)
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
        :return: tuple(TransactionInformation, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_transaction', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactions_id_transaction_informations_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactions_id_transaction_informations_put`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_transactions_id_transaction_informations_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

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
            '/users/{id_user}/transactions/{id_transaction}/informations', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionInformation',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactions_id_transaction_put(self, id_user, id_transaction, **kwargs):  # noqa: E501
        """Edit a transaction meta-data  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_id_transaction_put(id_user, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transaction: (required)
        :param str expand:
        :param bool active: if false, transaction isn't considered in analyzisis endpoints (like /balances)
        :param date application_date: change application date of the transaction
        :param str comment: change comment
        :param int id_category: ID of the associated category
        :param str wording: user rewording of the transaction
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Transaction
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactions_id_transaction_put_with_http_info(id_user, id_transaction, **kwargs)  # noqa: E501

    def users_id_user_transactions_id_transaction_put_with_http_info(self, id_user, id_transaction, **kwargs):  # noqa: E501
        """Edit a transaction meta-data  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_id_transaction_put_with_http_info(id_user, id_transaction, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transaction: (required)
        :param str expand:
        :param bool active: if false, transaction isn't considered in analyzisis endpoints (like /balances)
        :param date application_date: change application date of the transaction
        :param str comment: change comment
        :param int id_category: ID of the associated category
        :param str wording: user rewording of the transaction
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Transaction, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_transaction', 'expand', 'active', 'application_date', 'comment', 'id_category', 'wording']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactions_id_transaction_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactions_id_transaction_put`")  # noqa: E501
        # verify the required parameter 'id_transaction' is set
        if ('id_transaction' not in local_var_params or
                local_var_params['id_transaction'] is None):
            raise ApiValueError("Missing the required parameter `id_transaction` when calling `users_id_user_transactions_id_transaction_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_transaction' in local_var_params:
            path_params['id_transaction'] = local_var_params['id_transaction']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'active' in local_var_params:
            form_params.append(('active', local_var_params['active']))  # noqa: E501
        if 'application_date' in local_var_params:
            form_params.append(('application_date', local_var_params['application_date']))  # noqa: E501
        if 'comment' in local_var_params:
            form_params.append(('comment', local_var_params['comment']))  # noqa: E501
        if 'id_category' in local_var_params:
            form_params.append(('id_category', local_var_params['id_category']))  # noqa: E501
        if 'wording' in local_var_params:
            form_params.append(('wording', local_var_params['wording']))  # noqa: E501

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
            '/users/{id_user}/transactions/{id_transaction}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Transaction',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactions_post(self, id_user, date, original_wording, value, **kwargs):  # noqa: E501
        """Create transactions  # noqa: E501

        Create transactions for the supplied account or the account whose id is given with form parameters. It requires an array of transaction dictionaries.<br><br><br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_post(id_user, date, original_wording, value, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param date date: date of the transaction (required)
        :param str original_wording: label of the transaction (required)
        :param int value: vallue of the transaction (required)
        :param str expand:
        :param bool active: 1 if the transaction should be taken into account by pfm services (default: 1)
        :param bool coming: 1 if the transaction has already been debited (default: 0)
        :param datetime date_scraped: date on which the transaction has been found for the first time. YYYY-MM-DD HH:MM:SS(default: now)
        :param int id_account: account of the transaction. If not supplied, it has to be given in the route
        :param date rdate: realisation date of the transaction (default: value of date)
        :param str state: nature of the transaction (default: new)
        :param str type: type of the transaction (default: unknown)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Transaction
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactions_post_with_http_info(id_user, date, original_wording, value, **kwargs)  # noqa: E501

    def users_id_user_transactions_post_with_http_info(self, id_user, date, original_wording, value, **kwargs):  # noqa: E501
        """Create transactions  # noqa: E501

        Create transactions for the supplied account or the account whose id is given with form parameters. It requires an array of transaction dictionaries.<br><br><br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactions_post_with_http_info(id_user, date, original_wording, value, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param date date: date of the transaction (required)
        :param str original_wording: label of the transaction (required)
        :param int value: vallue of the transaction (required)
        :param str expand:
        :param bool active: 1 if the transaction should be taken into account by pfm services (default: 1)
        :param bool coming: 1 if the transaction has already been debited (default: 0)
        :param datetime date_scraped: date on which the transaction has been found for the first time. YYYY-MM-DD HH:MM:SS(default: now)
        :param int id_account: account of the transaction. If not supplied, it has to be given in the route
        :param date rdate: realisation date of the transaction (default: value of date)
        :param str state: nature of the transaction (default: new)
        :param str type: type of the transaction (default: unknown)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Transaction, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'date', 'original_wording', 'value', 'expand', 'active', 'coming', 'date_scraped', 'id_account', 'rdate', 'state', 'type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactions_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactions_post`")  # noqa: E501
        # verify the required parameter 'date' is set
        if ('date' not in local_var_params or
                local_var_params['date'] is None):
            raise ApiValueError("Missing the required parameter `date` when calling `users_id_user_transactions_post`")  # noqa: E501
        # verify the required parameter 'original_wording' is set
        if ('original_wording' not in local_var_params or
                local_var_params['original_wording'] is None):
            raise ApiValueError("Missing the required parameter `original_wording` when calling `users_id_user_transactions_post`")  # noqa: E501
        # verify the required parameter 'value' is set
        if ('value' not in local_var_params or
                local_var_params['value'] is None):
            raise ApiValueError("Missing the required parameter `value` when calling `users_id_user_transactions_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

        query_params = []
        if 'expand' in local_var_params:
            query_params.append(('expand', local_var_params['expand']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'active' in local_var_params:
            form_params.append(('active', local_var_params['active']))  # noqa: E501
        if 'coming' in local_var_params:
            form_params.append(('coming', local_var_params['coming']))  # noqa: E501
        if 'date' in local_var_params:
            form_params.append(('date', local_var_params['date']))  # noqa: E501
        if 'date_scraped' in local_var_params:
            form_params.append(('date_scraped', local_var_params['date_scraped']))  # noqa: E501
        if 'id_account' in local_var_params:
            form_params.append(('id_account', local_var_params['id_account']))  # noqa: E501
        if 'original_wording' in local_var_params:
            form_params.append(('original_wording', local_var_params['original_wording']))  # noqa: E501
        if 'rdate' in local_var_params:
            form_params.append(('rdate', local_var_params['rdate']))  # noqa: E501
        if 'state' in local_var_params:
            form_params.append(('state', local_var_params['state']))  # noqa: E501
        if 'type' in local_var_params:
            form_params.append(('type', local_var_params['type']))  # noqa: E501
        if 'value' in local_var_params:
            form_params.append(('value', local_var_params['value']))  # noqa: E501

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
            '/users/{id_user}/transactions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Transaction',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactionsclusters_get(self, id_user, **kwargs):  # noqa: E501
        """Get clustered transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactionsclusters_get(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: UserAccountTransactionsclusters
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactionsclusters_get_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_transactionsclusters_get_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Get clustered transactions  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactionsclusters_get_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        :return: tuple(UserAccountTransactionsclusters, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactionsclusters_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactionsclusters_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

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
            '/users/{id_user}/transactionsclusters', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserAccountTransactionsclusters',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactionsclusters_id_transactionscluster_delete(self, id_user, id_transactionscluster, **kwargs):  # noqa: E501
        """Delete a clustered transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactionsclusters_id_transactionscluster_delete(id_user, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transactionscluster: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionsCluster
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactionsclusters_id_transactionscluster_delete_with_http_info(id_user, id_transactionscluster, **kwargs)  # noqa: E501

    def users_id_user_transactionsclusters_id_transactionscluster_delete_with_http_info(self, id_user, id_transactionscluster, **kwargs):  # noqa: E501
        """Delete a clustered transaction  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactionsclusters_id_transactionscluster_delete_with_http_info(id_user, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transactionscluster: (required)
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
        :return: tuple(TransactionsCluster, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_transactionscluster', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactionsclusters_id_transactionscluster_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactionsclusters_id_transactionscluster_delete`")  # noqa: E501
        # verify the required parameter 'id_transactionscluster' is set
        if ('id_transactionscluster' not in local_var_params or
                local_var_params['id_transactionscluster'] is None):
            raise ApiValueError("Missing the required parameter `id_transactionscluster` when calling `users_id_user_transactionsclusters_id_transactionscluster_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_transactionscluster' in local_var_params:
            path_params['id_transactionscluster'] = local_var_params['id_transactionscluster']  # noqa: E501

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
            '/users/{id_user}/transactionsclusters/{id_transactionscluster}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsCluster',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactionsclusters_id_transactionscluster_put(self, id_user, id_transactionscluster, **kwargs):  # noqa: E501
        """Edit a clustered transaction  # noqa: E501

        Form params : - next_date (date): Date of transaction - mean_amount (decimal): Mean Amount - wording (string): name of transaction - id_account (id): related account - id_category (id): related category - enabled (bool): is enabled<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactionsclusters_id_transactionscluster_put(id_user, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transactionscluster: (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionsCluster
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactionsclusters_id_transactionscluster_put_with_http_info(id_user, id_transactionscluster, **kwargs)  # noqa: E501

    def users_id_user_transactionsclusters_id_transactionscluster_put_with_http_info(self, id_user, id_transactionscluster, **kwargs):  # noqa: E501
        """Edit a clustered transaction  # noqa: E501

        Form params : - next_date (date): Date of transaction - mean_amount (decimal): Mean Amount - wording (string): name of transaction - id_account (id): related account - id_category (id): related category - enabled (bool): is enabled<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactionsclusters_id_transactionscluster_put_with_http_info(id_user, id_transactionscluster, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param int id_transactionscluster: (required)
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
        :return: tuple(TransactionsCluster, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'id_transactionscluster', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactionsclusters_id_transactionscluster_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactionsclusters_id_transactionscluster_put`")  # noqa: E501
        # verify the required parameter 'id_transactionscluster' is set
        if ('id_transactionscluster' not in local_var_params or
                local_var_params['id_transactionscluster'] is None):
            raise ApiValueError("Missing the required parameter `id_transactionscluster` when calling `users_id_user_transactionsclusters_id_transactionscluster_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501
        if 'id_transactionscluster' in local_var_params:
            path_params['id_transactionscluster'] = local_var_params['id_transactionscluster']  # noqa: E501

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
            '/users/{id_user}/transactionsclusters/{id_transactionscluster}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsCluster',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def users_id_user_transactionsclusters_post(self, id_user, **kwargs):  # noqa: E501
        """Create clustered transaction  # noqa: E501

        Form params : - next_date (date) required: Date of transaction - mean_amount (decimal) required: Mean Amount - wording (string) required: name of transaction - id_account (id) required: related account<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactionsclusters_post(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
        :param str expand:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: TransactionsCluster
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.users_id_user_transactionsclusters_post_with_http_info(id_user, **kwargs)  # noqa: E501

    def users_id_user_transactionsclusters_post_with_http_info(self, id_user, **kwargs):  # noqa: E501
        """Create clustered transaction  # noqa: E501

        Form params : - next_date (date) required: Date of transaction - mean_amount (decimal) required: Mean Amount - wording (string) required: name of transaction - id_account (id) required: related account<br><br>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.users_id_user_transactionsclusters_post_with_http_info(id_user, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str id_user: Hint: you can use 'me' or 'all' (required)
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
        :return: tuple(TransactionsCluster, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['id_user', 'expand']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method users_id_user_transactionsclusters_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'id_user' is set
        if ('id_user' not in local_var_params or
                local_var_params['id_user'] is None):
            raise ApiValueError("Missing the required parameter `id_user` when calling `users_id_user_transactionsclusters_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id_user' in local_var_params:
            path_params['id_user'] = local_var_params['id_user']  # noqa: E501

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
            '/users/{id_user}/transactionsclusters', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsCluster',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
