# coding: utf-8

"""
    Budgea API Documentation

    # Budgea Development Guides  Welcome to **Budgea**'s documentation.  This documentation is intended to get you up-and-running with our APIs and advise on the implementation of some regulatory aspects of your application, following the DSP2's guidelines.  ## Getting Started **IMPORTANT** Depending on your status with regard of the DSP2 regulation, **agent** or **partner**, you may call our APIs or simply use our Webview and callbacks to get the financial data of your users. As an **agent**, you are allowed to call directly our APIs and implement your own form to get the user's credentials. As a **partner**, you cannot manipulate the credentials, and have to delegate this step to us through our webview.  The sections below will document how to use our APIs, make sure you have the **agent** status to do so. For the **partner**, please refer to the section *Webview* and *Callbacks* of this documentation.  ### Overview Your API is a REST API which requires a communication through https to send and receive JSON documents. During your tests, we recommend to make calls to the API with curl or any other HTTP client of your choice. You can watch a video demonstration on this [URL](https://asciinema.org/a/FsaFyt3WAPyDm7sfaZPkwal3V). For the examples we'll use the demo API with address `https://demo.biapi.pro`, you should change that name to your API's name.  ### Hello World Let's start by calling the service `/banks` which lists all available banks. ``` curl https://demo.biapi.pro/2.0/banks/ ``` To log in to a bank webpage, you'll need to know for a given bank, the fields your user should fill in the form. Let's call a  specific bank and ask for an additional resource *fields*. ``` curl https://demo.biapi.pro/2.0/banks/59?expand=fields ``` The response here concerns only 1 bank (since we specified an id) and the resource _Fields_ is added to the response thanks to the query parameter `expand`.  To get more interesting things done, you'll need to send authenticated requests.  ### Authentication The way to authenticate is by passing the `Authorization: Bearer <token>` header in your request. At the setup a _manage token_ have been generated, you can use this token for now, when creating your user we'll see how to generate a user's token. ``` curl https://demo.biapi.pro/2.0/config \\   -H 'Authorization: Bearer <token>' ``` This endpoint will list all the parameters you can change to adapt Budgea to your needs.  We've covered the very first calls. Before diving deeper, let's see some general information about the APIs.  ## Abstract  ### API URL `https://demo.biapi.pro/2.0`  ### Requests format Data format: **application/x-www-form-urlencoded** or **application/json** (suggested)  Additional headers: Authorization: User's token (private)  ### Responses format Data format: **application/json** ([http://www.json.org](http://www.json.org/)) Charset: **UTF-8**  ### Resources Each call on an endpoint will return resources. The main resources are: | Resource            | Description                                                                                                           | | ---------------------|:------------------------------------------------------------------------------------------------------------------   | |Users                 |Represent a user                                                                                                      | |Connection            |A set of data used to authenticate on a website (usually a login and password). There is 1 connection for each website| |Account               |A bank account contained in a connection                                                                              | |Transaction           |An entry in a bank account                                                                                            | |Investment            |An asset in a bank account                                                                                            |  The chain of resources is as follow: **Users ∈ Connections ∈ Accounts ∈ Transactions or Investments**  ### RESTful API  This API is RESTful, which means it is stateless and each resource is accessed with an unique URI.  Several HTTP methods are available:  | Method                  | Description                    | | ------------------------|:-------------------------------| | GET /resources          | List resources                 | | GET /resources/{ID}     | Get a resource from its ID     | | POST /resources         | Create a new resource          | | POST /resources/{ID}    | Update a resource              | | PUT /resources  /{ID}   | Update a resource              | | DELETE /resources       | Remove every resources         | | DELETE /resources/{ID}  | Delete a resource              |   Each resource can contain sub-resources, for example: `/users/me/connections/2/accounts/23/transactions/48`  ### HTTP response codes  | Code        | Message               | Description                                                                                   | | ----------- |:---------------------:|-----------------------------------------------------------------------------------------------| | 200         | OK                    |Default response when a GET or POST request has succeed                                        | | 202         | Accepted              |For a new connection this code means it is necessary to provide complementary information (2FA)| | 204         | No content            |Default response when a POST request succeed without content                                   | | 400         | Bad request           |Supplied parameters are incorrect                                                              | | 403         | Forbidden             |Invalid token                                                                                  | | 500         | Internal Servor Error |Server error                                                                                   | | 503         | Service Unavailable   |Service is temporarily unavailable                                                             |  ### Errors management In case an error occurs (code 4xx or 5xx), the response can contain a JSON object describing this error: ```json {    \"code\": \"authFailure\",    \"message\": \"Wrong password\"  // Optional } ``` If an error is displayed on the website, Its content is returned in error_message field. The list of all possible errors is listed further down this page.  ### Authentication A user is authenticated by an access_token which is sent by the API during a call on one of the authentication services, and can be supplied with this header: `Authorization: Bearer YYYYYYYYYYYYYYYYYYYYYYYYYYY`   There are two user levels:      - Normal user, which can only access to his own accounts     - Administrator, with extended rights  ### Default filters During a call to an URI which lists resources, some filters can be passed as query parameters:  | Parameter   | Type      | Description                                               | | ----------- |:---------:|-----------------------------------------------------------| | offset      | Integer   |Offset of the first returned resource                      | | limit       | Integer   |Limit number of results                                    | | min_date    | Date      |Minimal date (if supported by service), format: YYYY-MM-DD | | max_date    | Date      |Maximal date (if supported by service), format: YYYY-MM-DD |  ### Extend requests During a GET on a set of resources or on a unique resource, it is possible to add a parameter expand to the request to extend relations with other resources:  `GET /2.0/users/me/accounts/123?expand=transactions[category],connection`  ```json {    \"id\" : 123    \"name\" : \"Compte chèque\"    \"balance\" : 1561.15    \"transactions\" : [       {          \"id\" : 9849,          \"simplified_wording\" : \"HALL'S BEER\",          \"value\" : -513.20,          ...          \"category\" : {             \"id\" : 561,             \"name\" : \"Sorties / Bar\",             ...          }        },        ...    ],    \"id_user\" : 1,    \"connection\" : {       \"id\" : 1518,       \"id_bank\" : 41,       \"id_user\" : 1,       \"error\" : null,       ...    } } ```  ### Request example ```http GET /2.0/banks?offset=0&limit=10&expand=fields Host: demo.biapi.pro Accept: application/json Authorization: Bearer <token> ``` ```http HTTP/1.1 200 OK Content-Type: application/json Content-Length: 3026 Server: Apache Date: Fri, 14 Mar 2014 08:24:02 GMT  {    \"banks\" : [       {          \"id_weboob\" : \"bnporc\",          \"name\" : \"BNP Paribas\",          \"id\" : 3,          \"hidden\" : false,          \"fields\" : [             {                \"id\" : 1,                \"id_bank\" : 3,                \"regex\" : \"^[0-9]{5,10}$\",                \"name\" : \"login\",                \"type\" : \"text\",                \"label\" : \"Numéro client\"             },             {                \"id\" : 2,                \"id_bank\" : 3,                \"regex\" : \"^[0-9]{6}$\",                \"name\" : \"password\",                \"type\" : \"password\",                \"label\" : \"Code secret\"             }          ]       },       ...    ]    \"total\" : 41 } ```  ### Constants #### List of bank account types | Type          |Description                        | | -----------   |-----------------------------------| | checking      |Checking account                   | | savings       |Savings account                    | | deposit       |Deposit accounts                   | | loan          |Loan                               | | market        | Market accounts                   | | joint         |Joint account                      | | card          |Card                               | | lifeinsurance |Life insurance accounts            | | pee           |Plan Épargne Entreprise            | | perco         |Plan Épargne Retraite              | | article83     |Article 83                         | | rsp           |Réserve spéciale de participation  | | pea           |Plan d'épargne en actions          | | capitalisation|Contrat de capitalisation          | | perp          |Plan d'épargne retraite populaire  | | madelin       |Contrat retraite Madelin           | | unknown       |Inconnu                            |  #### List of transaction types  | Type         |Description                        | | -----------  |-----------------------------------| |transfer      |Transfers                          | |order         |Orders                             | |check         |Checks                             | |deposit       |Cash deposit                       | |payback       |Payback                            | |withdrawal    |Withdrawal                         | |loan_payment  |Loan payment                       | |bank          |Bank fees                          | |card          |Card operation                     | |deferred_card |Deferred card operation            | |card_summary  |Mensual debit of a deferred card   |  #### List of synchronization errors ##### Error on Connection object The error field may take one of the below values in case of error when accessing the user space.  | Error                      |Description                                                                                       | | -----------------------    |--------------------------------------------------------------------------------------------------| |wrongpass                   |The authentication on website has failed                                                          | |additionalInformationNeeded |Additional information is needed such as an OTP                                                  | |websiteUnavailable          |The website is unavailable, for instance we get a HTTP 503 response when requesting the website   | |actionNeeded                |An action is needed on the website by the user, scraping is blocked                               | |SCARequired                |An SCA process must be done by updating the connection                               | |decoupled                  |Requires a user validation (ex: digital key)| |passwordExpired                   |The password has expired and needs to be changed on the website.                                                         | |webauthRequired                |A complete authentication process is required by update the connection via redirect                            | |bug                         |A bug has occurred during the synchronization. An alert has been sent to Budget Insight           |  #### Error on Account object Errors can be filled at the account level in case we access the user's dashboard but some account related data cannot be retrieved. For instance, we may not access the transactions or investments for a specific account. Getting an error during an account synchronization does not impact the scraping of other acccounts.  | Error                      |Description                                                                                       | | -----------------------    |--------------------------------------------------------------------------------------------------| |websiteUnavailable          |The website or a page is unavailable                                                              | |actionNeeded                |An action is needed on the website by the user, scraping is blocked                               | |bug                         |A bug has occurred during the synchronization. An alert has been sent to Budget Insight           |  Now you know the basics of Budgea API - Basic call to retrieve resources - Add query parameters to aplly filters - Expand resources - Authenticated calls  We're good for the basics! Now let's see how to integrate Budgea in your app and create your first user.  ## Integrate Budgea *(protocol or Webview)* ### The workflow Users of your application exist in the Budgea API. Every User is identified by an access_token which is the shared secret between your application and our API.  The workflow is as below: 1. The user is on your application and wants to share his bank accounts or invoices. 2. A call is made **client side** (browser's javascript or desktop application) to create a temporarily token which will be used to make API calls. 3. A form is built, allowing the user to select the connector to use (bank or provider, depending on context). Every connector requires different kind of credentials. 4. A call on the API is made with the temporarily token to add a **Connection** with the credentials supplied by user. 5. In case of success, the user chooses what bank accounts (**Account**) or subscriptions (**Subscription**) he wants to share with your application. 6. When he validates the share, the temporarily token is transmitted to your server. This one will call the Budgea API with this token to get a permanent token.  **Note** In case your application works without a server (for example a desktop application), the permanent token can be obtained on the 1st step, by supplying a client_secret to /auth/init and the step 6 is omitted. To get more information, read the protocol.  There are 3 steps to integrate Budgea in your application: 1. Provide a way for your users to share their credentials with you 2. Get the data scraped from Budgea 3. Be sure to follow the good practices before going into production  ### Get credentials from users You have 2 options here: - Integrate the Budget Insight's Webview, a turnkey solution to get user's credentials - Create your own form following the protocol (must have the *agent* status)  ### Budgea webview  The Budgea webview complements REST API endpoints with web-based services to handle sensitive or complex operations: - add a connection (to a bank or a provider), or edit/repare access to a connection; - manage connections (add/remove/edit); - edit and validate bank transfers (alpha preview).  Usage of the webview is mandatory if you don't hold an Agent status, since you are not allowed to use API endpoints carrying user credentials, and optional otherwise.  #### Implementation guidelines  ##### Base URL  The base URL of all services must be customized:   `https://{{domain}}.biapi.pro/2.0/auth/webview/`   `https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/`   - `{{domain}}`: substitute with you API domain; - `{{lang}}`: optionally specify the language of the webview, `en` or `fr` (if not specified, an automatic redirection will be performed following the language of the browser).  ##### Browser integration  Services available as part of the webview are designed as parameterized URLs intended to be opened in a web browser. A callback URI must be specified by callers to be notified at the end of the operation flow, similar to OAuth 2 specification.  You are encouraged to integrate web-based steps in your product following UX best practices: - in a web environment, perform a full-page redirect to the URL (using either [HTTP redirect](https://developer.mozilla.org/fr/docs/Web/HTTP/Status/302) or [scripting](https://developer.mozilla.org/fr/docs/Web/API/Location)), and avoid new tabs or popups; - in a native Android app, prefer opening the default browser or relying on [Chrome Custom Tabs](https://developer.chrome.com/multidevice/android/customtabs) to integrating a WebView; - in a native iOS app, prefer using a [SFSafariViewController](https://developer.apple.com/documentation/safariservices/sfsafariviewcontroller) to integrating a WKWebView.  ##### Callback handling  Most flows redirect to a callback URI at the end of the process. Query parameters are added to the URI to identify successful or failed operations.  Successful parameters are specific to each flow. In case of an error, the following parameters are added:  | Parameter | Description | | - | - | | `error` | An lowercase string error code identifying the kind of error that occurred. When the parameter is not present, the response is successful. | | `error_description` | A longer string description of the error (not intended for user display). |  Common error codes include:  | Code | Description | | - | - | | `access_denied` | The user explicitly cancelled the flow. | | `server_error` | Oops, a technical failure occurred during the process. |  **Forward compatibility requirement**: Additional error codes may be added in the future to describe specific cases. When implementing error codes handling, always fallback to a generic case for unknown codes.  ##### Browser compatibility  The webview is designed and tested to work with browsers supported by the Angular framework:   https://angular.io/guide/browser-support  ##### Privacy / GDPR status  The webview itself does not use any kind of long-term data persistence mechanism such as cookies or local storage, but some authentication or authorization steps may delegate to third-party web services that may implement them.  #### Configuration  You can configure the appearance and behaviour of the webview by configuring the associated *Client Application* in the console:  | Key | Format | Description | | - | - | - | | `primary_color` | String | Optional. An accent color (hexadecimal string without '#' prefix) to personalize the UI elements of the webview. If absent, the default color is grey. | | `redirect_uri` | String | Optional. A recommended security whitelist configuration. The `redirect_uri` parameter sent to any endpoint of the webview is checked against the configuration, if any. | | `config.disable_connector_hints` | Boolean | Optional. This flags hides the list of most-used entries in the connector selection step. The default is `false`, i.e. the list is shown. | | `config.use_app_layout` | Boolean | Optional. Use this flag to enable presenting your log as an app icon. The default value is ` false`, i.e. the logo is shown in the top bar of the UI. | | `config.disable_accounts_pre_check` | Boolean | Optional. An optional boolean flag to prevent bank accounts to be automatically pre-checked when the user enters the activation step. The default value is ` false`, i.e. the bank accounts are pre-checked. |  #### Endpoints reference  ##### Add connection flow ``` https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/connect ```  This flow allows an end-user to add a new connection to the API. The flow handles the following steps: - selecting a connector; - authenticating & authorizing with the connector, by collecting credentials or delegating; - managing consent to aggregate accounts/subscriptions; - collecting required information for professional accounts.  ###### Endpoint parameters  | Parameter | Description | | - | - | | `client_id` | Required. The ID of the requesting client application. You can manage client applications of your domain in the admin console. | | `redirect_uri` | Required. An absolute callback URI. The webview will redirect to it at the end of the flow. | | `code` | Optional. A user-scoped temporary code to use with the Budgea API.<br>If you don't provide a code, a new anonymous user will be created before the connection is added, and you will be returned an access token code scoped to it with the success callback. | | `state` | Optional. An opaque string parameter that you can use to carry state across the flow. The parameter will be set \"as is\" on the callback URI. Make sure that the `state` you provide is properly URL-encoded. | | `connector_ids` | Optional. A comma-separated list of connector IDs available to pick from.<br>If the parameter is omitted, all active connectors are available.<br>If you pass a single value, the user is not prompted to choose the connector.<br>This parameter is mutually exclusive with `connector_uuids`. | | `connector_uuids` | Optional. A comma-separated list of connector UUIDs available to pick from.<br>If the parameter is omitted, all active connectors are available.<br>If you pass a single value, the user is not prompted to choose the connector.<br>This parameter is mutually exclusive with `connector_ids`. | | `connector_capabilities` | Optional. A comma-separated list of capabilities to filter available connectors.<br>If the parameter is omitted, `bank` is inferred.<br>If multiple values are provided, only connectors that expose all the requested capabilities are available.<br>To request a bank connection, use `bank`.<br>To request a provider connection, use `document`. | | `account_ibans` | Optional. A comma-separated list of IBANs to filter accounts available for activation in a bank connection context. Other accounts will not be selectable. | | `account_types` | Optional. A comma-separated list of account types to filter accounts available for activation in a bank connection context. Other accounts will not be selectable. | | `account_usages` | Optional. A comma-separated list of account usages to filter accounts available for activation in a bank connection context. Other accounts will not be selectable. |  ###### Successful callback parameters  | Parameter | Description | | - | - | | `connection_id` | The id of the newly created connection. Please note that when redirecting to the callback URI, the accounts and/or subscriptions are available in the API, but bank transactions or documents may still be syncing in background. | | `code` | Optional. If a `code` was *not* initially specified, an API code that you must exchange to obtain a permanent access token associated with the newly-created anonymous user holding the connection. The parameter is URL-encoded, make sure to handle it accordingly. | | `state` | Optional. Identical to the `state` parameter that was initially specified. |  ###### Additional error codes  | Code | Description | | - | - | | `tos_declined` | The end-user refused to validate the terms of service. |  ##### Re-auth / edit connection credentials flow  ``` https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/reconnect ```  This flow allows an end-user to re-authenticate against a bank or a provider in order to recover an existing connection, or to completely reset credentials associated with a connection.  ###### Endpoint parameters  | Parameter | Description | | - | - | | `client_id` | Required. The ID of the requesting client application. You can manage client applications of your domain in the admin console. | | `redirect_uri` | Required. An absolute callback URI. The webview will redirect to it at the end of the flow. | | `code` | Required. A user-scoped temporary code to use with the Budgea API. | | `connection_id` | Required. The id of the existing connection. | | `state` | Optional. An opaque string parameter that you can use to carry state across the flow. The parameter will be set \"as is\" on the callback URI. Make sure that the `state` you provide is properly URL-encoded. | | `reset_credentials` | Optional. In the default mode (`false`), the service will try to recover the connection and prompt the user only with outdated or transient information (new password, OTP...).<br>Set the parameter to `true` to force resetting all the credentials associated with the connection. This parameter may not apply to all connectors. |  ###### Successful callback parameters  This flow adds no parameter to the callback URI in case of success, except from `state`.  ##### Manage connections  ``` https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/manage ``` This flow allows an end-user to manage the connections associated with his account in the API. The user can add new connections, remove existing ones, fix connection errors, reset credentials or activate/deactivate bank accounts.  Support of `redirect_uri` in this flow is optional, as it can be integrated or presented as a terminal step, without relying on a final redirection.  ###### Endpoint parameters  | Parameter | Description | | - | - | | `client_id` | Required. The ID of the requesting client application. You can manage client applications of your domain in the admin console. | | `code` | Required. A user-scoped temporary code to use with the Budgea API. | | `redirect_uri` | Optional. An absolute callback URI. When provided, the webview will display a close button that redirects to it. | | `state` | Optional. An opaque string parameter that you can use to carry state across the flow when providing a `redirect_uri`. The parameter will be set \"as is\" on the callback URI. Make sure that the `state` you provide is properly URL-encoded. | | `connector_capabilities` | Optional. A comma-separated list of capabilities to filter available connectors when adding a new connection.<br>If the parameter is omitted, `bank` is inferred.<br>If multiple values are provided, only connectors that expose all the requested capabilities are available.<br>To request a bank connection, use `bank`.<br>To request a provider connection, use `document`. | | `account_types` | Optional. A comma-separated list of account types to filter accounts available for activation on adding a new bank connection or updating existing connections. Other accounts will not be selectable. | | `account_usages` | Optional. A comma-separated list of account usages to filter accounts available for activation in a bank connection context. Other accounts will not be selectable. |  ###### Callback parameters  This flow adds no parameter to the callback URI, except from `state`.  ##### Execute a bank transfer (preview)  **Disclaimer**: Transfer or payment services are available as a preview, protocols and parameters are subject to change in upcoming beta/final releases.  ``` https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/transfer ``` This flow allows an end-user to execute a bank transfer. The flow handles the following steps: - if the transfer is not already created, all steps to authenticate with a bank, select the recipient, the emitter account, the amount and label; - executing the transfer, including managing SCAs for recipient registration and/or transfer validation.  ###### Endpoint parameters  | Parameter | Description | | - | - | | `client_id` | Required. The ID of the requesting client application. You can manage client applications of your domain in the admin console. | | `redirect_uri` | Required. An absolute callback URI. The webview will redirect to it at the end of the flow. | | `code` | Required. A user-scoped temporary code to use with the Budgea API.<br>If you don't provide a code, a new anonymous user will be created before a connection is added and the transfer is executed, and you will be returned an access token code scoped to it with the success callback. | | `state` | Optional. An opaque string parameter that you can use to carry state across the flow. The parameter will be set \"as is\" on the callback URI. Make sure that the `state` you provide is properly URL-encoded. | | `transfer_id`| Optional. The ID of an prepared transfer to be validated in the webview. The user cannot edit anything on the transfer before validation. |  ###### Successfull callback parameters  | Parameter | Description | | - | - | | `transfer_id` | The ID of the transfer that was created and executed. | | `code` | Optional. If a `code` was *not* initially specified, an API code that you can exchange to obtain a permanent access token associated with the newly-created anonymous user holding the transfer. The parameter is URL-encoded, make sure to handle it accordingly. | | `state` | Optional. Identical to the `state` parameter that was initially specified. |  ###### Additional error codes  | Code | Description | | - | - | | `tos_declined` | The end-user refused to validate the terms of service. |  #### Migrating from v3  We provide a full backward compatibility layer with current implementations of the webview v3 to ease the transition. All endpoints remains accessible, with the same parameters and callback behaviour. Migration instructions are provided below.  *The v3 compatibility mode is expected to be removed on 31 December 2019.* You should migrate your implementation a soon as possible to new endpoints and parameters.  ##### Add connection flow / Edit connection credentials   ``` /connect/select ```  This endpoint has been superseded by `/connect` (no suffix) for adding a new connection, and `/reconnect` for resetting or updating an existing connection.  | Endpoint parameter | Migration instructions | | - | - | | `client_id` | No change. | | `redirect_uri`, `state` | No change. | | `response_type` | This parameter is not used anymore. | | `id_connector`, `connectors` | Superseded by `connector_ids` sent to the `/connect` endpoint. | | `types` | Superseded by `connector_capabilities` sent to the `/connect` endpoint.<br>Use`connector_capabilities=bank` (bank connection) or `connector_capabilities=document` (provider connection). | | `id_connection` | Superseded by `connection_id` sent to the `/reconnect` endpoint. |  Passing the code or access token as an URL fragment is no longer supported, use the `code` query parameter.  | Callback parameter | Migration instructions | | - | - | | `id_connection` | Superseded by `connection_id`.<br>In the `/reconnect` flow, this parameter is not returned anymore. | | `code` | Still named `code`, but in the `/connect` flow the parameter is now **only** added if an anonymous user was created, i.e. the `code` parameter was **not** provided as a query parameter or fragment.<br>In the `/reconnect` flow, this parameter is not returned anymore. | | `state` | No change. |  ##### Manage connections  ``` /accounts ```  This endpoint has been superseded by `/manage`, that now fully allows users to add/remove connections, reset their credentials or recover from error states.  | Endpoint parameter | Migration instructions | | - | - | | `client_id` | No change. | | `redirect_uri`, `state` | No change, these parameters are now optional. | | `response_type` | This parameter is not used anymore. | | `types` | Superseded by `connector_capabilities`.<br>Use`connector_capabilities=bank` (bank connection) or `connector_capabilities=document` (provider connection). |  Passing the code or access token as an URL fragment is no longer supported, use the `code` query parameter.  | Callback parameter | Migration instructions | | - | - | | `code` | This parameter is not returned anymore. | | `state` | No change. |  ##### Behaviour change  In v3, the `/accounts` flow used to redirect to the `redirect_uri` after a connection addition. This is no longer the case in v4, where redirection is only performed when the user explicitly closes the flow. If you need to perform actions when a connection is added or removed, you should rely on webhooks.  #### Protocol This section describes the protocol used to set bank and provider accounts of a user, in case you don't want to use the webview.  The idea is to call the following services client-side (with AJAX in case of a web application), to ensure the bank and providers credentials will not be sent to your servers.  1. /auth/init ```http POST /auth/init ``` ```json {    \"auth_token\" : \"fBqjMZbYddebUGlkR445JKPA6pCoRaGb\",    \"type\" : \"temporary\",    \"expires_in\" : 1800,    \"id_user\": 1 } ``` This service creates a temporarily token, to use in the \"Authorization\" header in next calls to the API  The returned token has a life-time of 30 minutes, and should be transfered to the API then (cf Permanent Token), so that your server can get a permanent access_token.  It is possible to generate a permanent token immediately, by calling the service with the manage_token, or by supply parameters client_id and client_secret.  2. /banks or /providers ```http GET /banks?expand=fields Authorization: Bearer <token> ``` ```json {    \"hidden\" : false,          \"charged\" : true,          \"name\" : \"American Express\",          \"id\" : 30,          \"fields\" : [             {                \"values\" : [                   {                      \"label\" : \"Particuliers/Professionnels\",                      \"value\" : \"pp\"                   },                   {                      \"value\" : \"ent\",                      \"label\" : \"Entreprises\"                   }                ],                \"label\" : \"Type de compte\",                \"regex\" : null,                \"name\" : \"website\",                \"type\" : \"list\"             },             {                \"type\" : \"password\",                \"label\" : \"Code secret\",                \"name\" : \"password\",                \"regex\" : \"^[0-9]{6}$\"             }          ],       },       ...    ],    \"total\" : 44, } ``` You get a list of connectors, and all associated fields needed to build the form at step 3. You can also use that list to show to your user, all available banks.  3. /users/me/connections Make a POST request and supply the id_bank (ID of the chosen bank) or id_provider (ID of provider), and all requested fields as key/value parameters. For example: ```http POST /users/me/connections Authorization: Bearer <token> -F login=12345678 -F password=123456 -F id_bank=59 ``` You can get the following return codes:  |Code           |Description                                                  | |---------------|------------------------------------------------------------ | |200            |The connection has succeed and has been created              | |202            |It is necessary to provide complementary information. This occurs on the first connection on some kind of Boursorama accounts for example, where a SMS is sent to the customer. It is necessary to ask the user to fill fields requested in the fields, and do a POST again on /users/me/connections/ID, with the connection ID in id_connection. | |400            |Unable to connect to the website, the field error in the JSON can be **websiteUnavailable** or **wrongpass**  | |403            |Invalid token                                                |  4. Activate accounts The accounts the user wants to aggregate must be activated before any transaction or investment is retrieved. Several accounts can be activated in 1 request by separating the account ids with commas. ```http PUT /users/me/connections/<id_connection>/accounts/<id_account>?all ```  5. Permanent token If the user validates the share of his accounts, it is necessary to transform the temporary code to a permanent access_token (so that the user won't expire).  To do that, make a POST request on /auth/token/access with the following parameters: |Parameter            |Description                                                     | |---------------------|----------------------------------------------------------------| |code                 |The temporarily token which will let you get the access_token   | |client_id            |The ID of your client application                               | |client_secret        |The secret of your client application                           |  ```json POST /auth/token/access  {    \"client_id\" : 17473055,    \"client_secret\" : \"54tHJHjvodbANVzaRtcLzlHGXQiOgw80\",    \"code\" : \"fBqjMZbYddebUGlkR445JKPA6pCoRaGb\" } ``` ```http HTTP/1.1 200 OK  {    \"access_token\" : \"7wBPuFfb1Hod82f1+KNa0AmrkIuQ3h1G\",    \"token_type\":\"Bearer\" } ```  ### Update accounts Another important call is when a user wants to add/remove connections to banks or providers, or to change the password on one of them, it is advised to give him a temporarily code from the permanent access_token, with the following call (using the access_token as bearer): ```http POST /auth/token/code Authorization: Bearer <token> ``` ```json {    \"code\" : \"/JiDppWgbmc+5ztHIUJtHl0ynYfw682Z\",    \"type\" : \"temporary\",    \"expires_in\" : 1800, } ``` Its life-time is 30 minutes, and let the browser to list connections and accounts, via `GET /users/me/connections?expand=accounts` for example.   To update the password of a connection, you can do a POST on the *connection* resource, with the field *password* in the data. The new credentials are checked to make sure they are valid, and the return codes are the same as when adding a connection.  ## Getting the data (Webhooks) You have created your users and their connections, now it's time to get the data. There are 2 ways to retrieve it, the 2 can be complementary: - make regular calls to the API - use the webhooks (recommended)  ### Manual Synchronization It is possible to do a manual synchronization of a user. We recommend to use this method in case the user wants fresh data after logging in.  To trigger the synchronization, call the API as below: `PUT /users/ID/connections` The following call is blocking until the synchronization is terminated.  Even if it is not recommended, it's possible to fetch synchronously new data. To do that, you can use the *expand* parameter: ` /users/ID/connections?expand=accounts[transactions,investments[type]],subscriptions` ```json {    \"connections\" : [       {          \"accounts\" : [             {                \"balance\" : 7481.01,                \"currency\" : {                   \"symbol\" : \"€\",                   \"id\" : \"EUR\",                   \"prefix\" : false                },                \"deleted\" : null,                \"display\" : true,                \"formatted_balance\" : \"7 481,01 €\",                \"iban\" : \"FR76131048379405300290000016\",                \"id\" : 17,                \"id_connection\" : 7,                \"investments\" : [                   {                      \"code\" : \"FR0010330902\",                      \"description\" : \"\",                      \"diff\" : -67.86,                      \"id\" : 55,                      \"id_account\" : 19,                      \"id_type\" : 1,                      \"label\" : \"Agressor PEA\",                      \"portfolio_share\" : 0.48,                      \"prev_diff\" : 2019.57,                      \"quantity\" : 7.338,                      \"type\" : {                         \"color\" : \"AABBCC\",                         \"id\" : 1,                         \"name\" : \"Fonds action\"                      },                      \"unitprice\" : 488.98,                      \"unitvalue\" : 479.73,                      \"valuation\" : 3520.28                   }                ],                \"last_update\" : \"2015-07-04 15:17:30\",                \"name\" : \"Compte chèque\",                \"number\" : \"3002900000\",                \"transactions\" : [                   {                      \"active\" : true,                      \"application_date\" : \"2015-06-17\",                      \"coming\" : false,                      \"comment\" : null,                      \"commission\" : null,                      \"country\" : null,                      \"date\" : \"2015-06-18\",                      \"date_scraped\" : \"2015-07-04 15:17:30\",                      \"deleted\" : null,                      \"documents_count\" : 0,                      \"formatted_value\" : \"-16,22 €\",                      \"id\" : 309,                      \"id_account\" : 17,                      \"id_category\" : 9998,                      \"id_cluster\" : null,                      \"last_update\" : \"2015-07-04 15:17:30\",                      \"new\" : true,                      \"original_currency\" : null,                      \"original_value\" : null,                      \"original_wording\" : \"FACTURE CB HALL'S BEER\",                      \"rdate\" : \"2015-06-17\",                      \"simplified_wording\" : \"HALL'S BEER\",                      \"state\" : \"parsed\",                      \"stemmed_wording\" : \"HALL'S BEER\",                      \"type\" : \"card\",                      \"value\" : -16.22,                      \"wording\" : \"HALL'S BEER\"                   }                ],                \"type\" : \"checking\"             }          ],          \"error\" : null,          \"expire\" : null,          \"id\" : 7,          \"id_user\" : 7,          \"id_bank\" : 41,          \"last_update\" : \"2015-07-04 15:17:31\"       }    ],    \"total\" : 1, } ```  ### Background synchronizations & Webhooks Webhooks are callbacks sent to your server, when an event is triggered during a synchronization. Synchronizations are automatic, the frequency can be set using the configuration key `autosync.frequency`. Using webhooks allows you to get the most up-to-date data of your users, after each synchronization.  The automatic synchronization makes it possible to recover new bank entries, or new invoices, at a given frequency. You have the possibility to add webhooks on several events, and choose to receive each one on a distinct URL. To see the list of available webhooks you can call the endpoint hereunder: ``` curl https://demo.biapi.pro/2.0/webhooks_events \\   -H 'Authorization: Bearer <token>' ```  The background synchronizations for each user are independent, and their plannings are spread over the day so that they do not overload any website.  Once the synchronization of a user is over, a POST request is sent on the callback URL you have defined, including all webhook data. A typical json sent to your server is as below: ```http POST /callback HTTP/1.1 Host: example.org Content-Length: 959 Accept-Encoding: gzip, deflate, compress Accept: */* User-Agent: Budgea API/2.0 Content-Type: application/json; charset=utf-8 Authorization: Bearer sl/wuqgD2eOo+4Zf9FjvAz3YJgU+JKsJ  {    \"connections\" : [       {          \"accounts\" : [             {                \"balance\" : 7481.01,                \"currency\" : {                   \"symbol\" : \"€\",                   \"id\" : \"EUR\",                   \"prefix\" : false                },                \"deleted\" : null,                \"display\" : true,                \"formatted_balance\" : \"7 481,01 €\",                \"iban\" : \"FR76131048379405300290000016\",                \"id\" : 17,                \"id_connection\" : 7,                \"investments\" : [                   {                      \"code\" : \"FR0010330902\",                      \"description\" : \"\",                      \"diff\" : -67.86,                      \"id\" : 55,                      \"id_account\" : 19,                      \"id_type\" : 1,                      \"label\" : \"Agressor PEA\",                      \"portfolio_share\" : 0.48,                      \"prev_diff\" : 2019.57,                      \"quantity\" : 7.338,                      \"type\" : {                         \"color\" : \"AABBCC\",                         \"id\" : 1,                         \"name\" : \"Fonds action\"                      },                      \"unitprice\" : 488.98,                      \"unitvalue\" : 479.73,                      \"valuation\" : 3520.28                   }                ],                \"last_update\" : \"2015-07-04 15:17:30\",                \"name\" : \"Compte chèque\",                \"number\" : \"3002900000\",                \"transactions\" : [                   {                      \"active\" : true,                      \"application_date\" : \"2015-06-17\",                      \"coming\" : false,                      \"comment\" : null,                      \"commission\" : null,                      \"country\" : null,                      \"date\" : \"2015-06-18\",                      \"date_scraped\" : \"2015-07-04 15:17:30\",                      \"deleted\" : null,                      \"documents_count\" : 0,                      \"formatted_value\" : \"-16,22 €\",                      \"id\" : 309,                      \"id_account\" : 17,                      \"id_category\" : 9998,                      \"id_cluster\" : null,                      \"last_update\" : \"2015-07-04 15:17:30\",                      \"new\" : true,                      \"original_currency\" : null,                      \"original_value\" : null,                      \"original_wording\" : \"FACTURE CB HALL'S BEER\",                      \"rdate\" : \"2015-06-17\",                      \"simplified_wording\" : \"HALL'S BEER\",                      \"state\" : \"parsed\",                      \"stemmed_wording\" : \"HALL'S BEER\",                      \"type\" : \"card\",                      \"value\" : -16.22,                      \"wording\" : \"HALL'S BEER\"                   }                ],                \"type\" : \"checking\"             }          ],          \"bank\" : {             \"id_weboob\" : \"ing\",             \"charged\" : true,             \"name\" : \"ING Direct\",             \"id\" : 7,             \"hidden\" : false          },          \"error\" : null,          \"expire\" : null,          \"id\" : 7,          \"id_user\" : 7,          \"id_bank\" : 41,          \"last_update\" : \"2015-07-04 15:17:31\"       }    ],    \"total\" : 1,    \"user\" : {       \"signin\" : \"2015-07-04 15:17:29\",       \"id\" : 7,       \"platform\" : \"sharedAccess\"    } } ``` The authentication on the callback is made with the access_token of the user (which is a shared secret between your server and the Budgea API).  When you are in production, it is needed to define a HTTPS URL using a valid certificate, delivered by a recognized authority. If this is not the case, you can contact us to add your CA (Certificate Authority) to our PKI (Public Key Infrastructure).  Important: it is necessary to send back a HTTP 200 code, without what we consider that data is not correctly taken into account on your system, and it will be sent again at the next user synchronization.  ## Guidelines for production Now you should have integrated the API inside your application. Make sure your Webhooks URLs are in HTTPS, if so you can enable the production state of the API.  To make things great, here are some good practices, please check you have respected them: - You have provided to your users a way to configure their accounts - You have provided to your users a way to change their account passwords - You consider the **error** field of Connections, to alert the user in case the state is **wrongpass** - You map IDs of Accounts, Subscriptions, Transactions and Documents in your application, to be sure to correctly match them - When the deleted field is set on a bank transaction, you delete it in your database - You don't loop on all users to launch synchronizations, this might saturate the service  If you have questions about above points, please contact us. Otherwise, you can put into production!  ### Going further If you want to raise the bar for your app and add features such as the ability to do transfers, get invoices, aggregate patrimony and more, please refer to the sections below. We'll discuss complementary APIs building upon the aggregation, allowing for the best of financial apps.  ## Budgea API Pay This API allows for the emition of transfers between the aggregated accounts. Just like the simple aggregation, BI provides a webview or a protocol to follow, to implement this feature.  ### API pay protocol This section describes how the transfer and recipient protocol work, in case you don't want to integrate the webview. The idea is to do following calls client side (with AJAX in case of a web application), so that the interaction with the Budgea API is transparent.  #### Executing a transfer 1. /auth/token/code If you do calls client side, get a new temporary code for the user, from the access_token. This will prevent security issues. ``` curl -d '' \\   https://demo.biapi.pro/2.0/auth/token/code \\   -H 'Authorization: Bearer <token>' ``` ```json {    \"code\": \"/JiDppWgbmc+5ztHIUJtHl0ynYfw682Z\",    \"type\": \"temporary\",    \"expires_in\": 1800 } ``` The returned token has a life-time of 30 minutes.  2. /users/me/accounts?able_to_transfer=1 List all the accounts that can do transfers. Authenticate the call with the code you got at step 1. ``` curl https://demo.biapi.pro/2.0/users/me/accounts?able_to_transfer=1 \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' ``` ```json {   \"accounts\" : [       {          \"display\" : true,          \"balance\" : 2893.36,          \"id_type\" : 2,          \"number\" : \"****1572\",          \"type\" : \"checking\",          \"deleted\" : null,          \"bic\" : \"BNPAFRPPXXX\",          \"bookmarked\" : false,          \"coming\" : -2702.74,          \"id_user\" : 1,          \"original_name\" : \"Compte de chèques\",          \"currency\" : {             \"symbol\" : \"€\",             \"id\" : \"EUR\",             \"prefix\" : false          },          \"name\" : \"lol\",          \"iban\" : \"FR7630004012550000041157244\",          \"last_update\" : \"2016-12-28 12:31:04\",          \"id\" : 723,          \"formatted_balance\" : \"2893,36 €\",          \"able_to_transfer\" : true,          \"id_connection\" : 202       }    ],    \"total\" : 1 } ```  3. /users/me/accounts/ID/recipients List all available recipients for a given account. ``` curl https://demo.biapi.pro/2.0/users/me/accounts/723/recipients?limit=1 \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' ``` ```json {   \"total\" : 27,    \"recipients\" : [       {          \"bank_name\" : \"BNP PARIBAS\",          \"bic\" : \"BNPAFRPPXXX\",          \"category\" : \"Interne\",          \"deleted\" : null,          \"enabled_at\" : \"2016-10-31 18:52:53\",          \"expire\" : null,          \"iban\" : \"FR7630004012550003027641744\",          \"id\" : 1,          \"id_account\" : 1,          \"id_target_account\" : 2,          \"label\" : \"Livret A\",          \"last_update\" : \"2016-12-05 12:07:24\",          \"time_scraped\" : \"2016-10-31 18:52:54\",          \"webid\" : \"2741588268268091098819849694548441184167285851255682796371\"       }    ] } ```  4. /users/me/accounts/ID/recipients/ID/transfers Create the transfer ``` curl \\   https://demo.biapi.pro/2.0/users/me/accounts/1/recipients/1/transfers \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' \\   -F amount=10, \\   -F label=\"Test virement\", \\   -F exec_date=\"2018-09-12\" // optional ``` ```json {    \"account_iban\" : \"FR7630004012550000041157244\",    \"amount\" : 10,    \"currency\" : {       \"id\" : \"EUR\",       \"prefix\" : false,       \"symbol\" : \"€\"    },    \"exec_date\" : \"2018-09-12\",    \"fees\" : null    \"formatted_amount\" : \"10,00 €\",    \"id\" : 22,    \"id_account\" : 1,,    \"id_recipient\" : 1,    \"label\" : \"Test virement\",    \"recipient_iban\" : \"FR7630004012550003027641744\",    \"register_date\" : \"2018-09-12 10:34:59\",    \"state\" : \"created\",    \"webid\" : null } ```  5. /users/me/transfers/ID Execute the transfer ``` curl \\   https://demo.biapi.pro/2.0/users/me/transfers/22 \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' \\   -F validated=true ``` ```json {    \"account_iban\" : \"FR7630004012550000041157244\",    \"amount\" : 10,    \"currency\" : {       \"id\" : \"EUR\",       \"prefix\" : false,       \"symbol\" : \"€\"    },    \"exec_date\" : \"2016-12-19\",    \"fees\" : null,    \"fields\" : [       {          \"label\" : \"Code secret BNP Paribas\",          \"type\" : \"password\",          \"regex\" : \"^[0-9]{6}$\",          \"name\" : \"password\"       }    ],    \"formatted_amount\" : \"10,00 €\",    \"id\" : 22,    \"id_account\" : 1,    \"id_recipient\" : 1,    \"label\" : \"Test virement\",    \"recipient_iban\" : \"FR7630004012550003027641744\",    \"register_date\" : \"2016-12-19 10:34:59\",    \"state\" : \"created\",    \"webid\" : null } ``` Here, an authentication step asks user to enter his bank password. The transfer can be validated with:  ``` curl \\   https://demo.biapi.pro/2.0/users/me/transfers/22 \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' \\   -F validated=true \\   -F password=\"123456\" ``` ```json {    \"account_iban\" : \"FR7630004012550000041157244\",    \"currency\" : {       \"id\" : \"EUR\",       \"prefix\" : false,       \"symbol\" : \"€\"    },    \"amount\" : 10,    \"exec_date\" : \"2016-12-19\",    \"fees\" : 0,    \"formatted_amount\" : \"10,00 €\",    \"id\" : 22,    \"id_account\" : 1,    \"id_recipient\" : 1,    \"label\" : \"Test virement\",    \"recipient_iban\" : \"FR7630004012550003027641744\",    \"register_date\" : \"2016-12-19 10:34:59\",    \"state\" : \"pending\",    \"webid\" : \"ZZ10C4FKSNP05TK95\" } ``` The field state is changed to *pending*, telling that the transfer has been correctly executed on the bank. A connection synchronization is then launched, to find the bank transaction in the movements history. In this case, the transfer state will be changed to *done*.  #### Adding a recipient 1. /auth/token/code Get a temporary token for the user. Same procedure than step 1 for a transfer.  2. /users/me/accounts?able_to_transfer=1 List accounts allowing transfers. Same procedure than step 2 for a transfer.  3. /users/me/accounts/ID/recipients/ Add a new recipient. ``` curl \\   https://demo.biapi.pro/2.0/users/me/accounts/1/recipients \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' \\   -F iban=FR7613048379405300290000355 \\   -F label=\"Papa\", \\   -F category=\"Famille\" // optional ``` ```json {    \"bank_name\" : \"BNP PARIBAS\",    \"bic\" : \"BNPAFRPPXXX\",    \"category\" : \"Famille\",    \"deleted\" : null,    \"enabled_at\" : null,    \"expire\" : \"2017-04-29 16:56:20\",    \"fields\" : [       {          \"label\" : \"Veuillez entrer le code reçu par SMS\",          \"type\" : \"password\",          \"regex\" : \"^[0-9]{6}$\",          \"name\" : \"sms\"       }    ],    \"iban\" : \"FR7613048379405300290000355\",    \"id\" : 2,    \"id_account\" : 1,    \"id_target_account\" : null,    \"label\" : \"Papa\",    \"last_update\" : \"2017-04-29 16:26:20\",    \"time_scraped\" : null,    \"webid\" : null } ``` It is necessary to post on the object Recipient with the requested fields (here sms), until the add is validated: ``` curl \\   https://demo.biapi.pro/2.0/users/me/accounts/1/recipients/2 \\   -H 'Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z' \\   -F sms=\"123456\" ``` ```json {    \"bank_name\" : \"BNP PARIBAS\",    \"bic\" : \"BNPAFRPPXXX\",    \"category\" : \"Famille\",    \"deleted\" : null,    \"enabled_at\" : \"2017-05-01 00:00:00\",    \"expire\" : null,    \"iban\" : \"FR7613048379405300290000355\",    \"id\" : 2,    \"id_account\" : 1,    \"id_target_account\" : null,    \"label\" : \"Papa\",    \"last_update\" : \"2017-04-29 16:26:20\",    \"time_scraped\" : null,    \"webid\" : \"2741588268268091098819849694548441184167285851255682796371\" } ``` If the field enabled_at is in the future, it means that it isn't possible yet to execute a transfer, as the bank requires to wait a validation period.  ### API Pay Webview This section describes how to integrate the webview of the Budgea Pay API inside your application, to let your users do transfers to their recipients.  #### User redirection To redirect the user to the webview, it is necessary to build a URI authenticated with a temporary token. This can be done from our library, or by calling the endpoint `/auth/token/code` (see the protocol section for an example). If the parameter **redirect_uri** is supplied, the user will be redirected to that page once the transfer is done.  #### List of pages Here are a list a pages you may call to redirect your user directly on a page of the process: |Path                                 |Description of the page                                                           | |-------------------------------------|----------------------------------------------------------------------------------| |/transfers                           |List Transfers                                                                    | |/transfers/accounts                  |List emitter accounts                                                             | |/transfers/accounts/id/recipients    |List recipients                                                                   | |/transfers/accounts/id/recipients/id |Initialization of a transfer between the account and the recipient                | |/transfers/id                        |Detail of a given transfer                                                        |  ## Deprecated  This section lists all the deprecated features in Budgea API. The associated date is the date of its removal. **Do not use them**.  ### Key Investments (**2019-06-24**)  Adding a temporary new key \"all_investments\" that will include deleted investments in the **webhooks**.  ### No automatic expand on User objects (**2019-07-30**) In the API responses, by default, User objects won't display the keys \"config\", \"alert_settings\" and \"invites\" anymore. You will still be able to access this data by expanding the request. Example: GET /users/me/?expand=alert_settings,config  ### Renaming of \"type\" field for jwt tokens (**2019-07-30**) For user's tokens in the jwt format, the \"type\" field will be renamed from \"shared_access\" to \"sharedAccess\".   # noqa: E501

    The version of the OpenAPI document: 2.0
    Contact: rienafairefr@gmail.com
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "pybudgea"
VERSION = "0.1.6"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Budgea API Documentation",
    author_email="rienafairefr@gmail.com",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Budgea API Documentation"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description="""\
    This is pybudgea, an autogenerated package to access Budget Insight API

    https://www.budget-insight.com/budgea-api

    Here is the original Budget Insight Swagger info.description:

    # Budgea Development Guides

Welcome to **Budgea**&#39;s documentation.

This documentation is intended to get you up-and-running with our APIs and advise on the implementation of some regulatory aspects of your application, following the DSP2&#39;s guidelines.

## Getting Started
**IMPORTANT**
Depending on your status with regard of the DSP2 regulation, **agent** or **partner**, you may call our APIs or simply use our Webview and callbacks to get the financial data of your users.
As an **agent**, you are allowed to call directly our APIs and implement your own form to get the user&#39;s credentials.
As a **partner**, you cannot manipulate the credentials, and have to delegate this step to us through our webview.

The sections below will document how to use our APIs, make sure you have the **agent** status to do so.
For the **partner**, please refer to the section *Webview* and *Callbacks* of this documentation.

### Overview
Your API is a REST API which requires a communication through https to send and receive JSON documents.
During your tests, we recommend to make calls to the API with curl or any other HTTP client of your choice.
You can watch a video demonstration on this [URL](https://asciinema.org/a/FsaFyt3WAPyDm7sfaZPkwal3V).
For the examples we&#39;ll use the demo API with address &#x60;https://demo.biapi.pro&#x60;, you should change that name to your API&#39;s name.

### Hello World
Let&#39;s start by calling the service &#x60;/banks&#x60; which lists all available banks.
&#x60;&#x60;&#x60;
curl https://demo.biapi.pro/2.0/banks/
&#x60;&#x60;&#x60;
To log in to a bank webpage, you&#39;ll need to know for a given bank, the fields your user should fill in the form.
Let&#39;s call a  specific bank and ask for an additional resource *fields*.
&#x60;&#x60;&#x60;
curl https://demo.biapi.pro/2.0/banks/59?expand&#x3D;fields
&#x60;&#x60;&#x60;
The response here concerns only 1 bank (since we specified an id) and the resource _Fields_ is added to the response thanks to the query parameter &#x60;expand&#x60;.

To get more interesting things done, you&#39;ll need to send authenticated requests.

### Authentication
The way to authenticate is by passing the &#x60;Authorization: Bearer &lt;token&gt;&#x60; header in your request.
At the setup a _manage token_ have been generated, you can use this token for now, when creating your user we&#39;ll see how to generate a user&#39;s token.
&#x60;&#x60;&#x60;
curl https://demo.biapi.pro/2.0/config \
  -H &#39;Authorization: Bearer &lt;token&gt;&#39;
&#x60;&#x60;&#x60;
This endpoint will list all the parameters you can change to adapt Budgea to your needs.

We&#39;ve covered the very first calls. Before diving deeper, let&#39;s see some general information about the APIs.

## Abstract

### API URL
&#x60;https://demo.biapi.pro/2.0&#x60;

### Requests format
Data format: **application/x-www-form-urlencoded** or **application/json** (suggested)

Additional headers: Authorization: User&#39;s token (private)

### Responses format
Data format: **application/json** ([http://www.json.org](http://www.json.org/))
Charset: **UTF-8**

### Resources
Each call on an endpoint will return resources. The main resources are:
| Resource            | Description                                                                                                           |
| ---------------------|:------------------------------------------------------------------------------------------------------------------   |
|Users                 |Represent a user                                                                                                      |
|Connection            |A set of data used to authenticate on a website (usually a login and password). There is 1 connection for each website|
|Account               |A bank account contained in a connection                                                                              |
|Transaction           |An entry in a bank account                                                                                            |
|Investment            |An asset in a bank account                                                                                            |

The chain of resources is as follow: **Users ∈ Connections ∈ Accounts ∈ Transactions or Investments**

### RESTful API

This API is RESTful, which means it is stateless and each resource is accessed with an unique URI.

Several HTTP methods are available:

| Method                  | Description                    |
| ------------------------|:-------------------------------|
| GET /resources          | List resources                 |
| GET /resources/{ID}     | Get a resource from its ID     |
| POST /resources         | Create a new resource          |
| POST /resources/{ID}    | Update a resource              |
| PUT /resources  /{ID}   | Update a resource              |
| DELETE /resources       | Remove every resources         |
| DELETE /resources/{ID}  | Delete a resource              |


Each resource can contain sub-resources, for example:
&#x60;/users/me/connections/2/accounts/23/transactions/48&#x60;

### HTTP response codes

| Code        | Message               | Description                                                                                   |
| ----------- |:---------------------:|-----------------------------------------------------------------------------------------------|
| 200         | OK                    |Default response when a GET or POST request has succeed                                        |
| 202         | Accepted              |For a new connection this code means it is necessary to provide complementary information (2FA)|
| 204         | No content            |Default response when a POST request succeed without content                                   |
| 400         | Bad request           |Supplied parameters are incorrect                                                              |
| 403         | Forbidden             |Invalid token                                                                                  |
| 500         | Internal Servor Error |Server error                                                                                   |
| 503         | Service Unavailable   |Service is temporarily unavailable                                                             |

### Errors management
In case an error occurs (code 4xx or 5xx), the response can contain a JSON object describing this error:
&#x60;&#x60;&#x60;json
{
   &quot;code&quot;: &quot;authFailure&quot;,
   &quot;message&quot;: &quot;Wrong password&quot;  // Optional
}
&#x60;&#x60;&#x60;
If an error is displayed on the website, Its content is returned in error_message field.
The list of all possible errors is listed further down this page.

### Authentication
A user is authenticated by an access_token which is sent by the API during a call on one of the authentication services, and can be supplied with this header:
&#x60;Authorization: Bearer YYYYYYYYYYYYYYYYYYYYYYYYYYY&#x60;

 There are two user levels:

    - Normal user, which can only access to his own accounts
    - Administrator, with extended rights

### Default filters
During a call to an URI which lists resources, some filters can be passed as query parameters:

| Parameter   | Type      | Description                                               |
| ----------- |:---------:|-----------------------------------------------------------|
| offset      | Integer   |Offset of the first returned resource                      |
| limit       | Integer   |Limit number of results                                    |
| min_date    | Date      |Minimal date (if supported by service), format: YYYY-MM-DD |
| max_date    | Date      |Maximal date (if supported by service), format: YYYY-MM-DD |

### Extend requests
During a GET on a set of resources or on a unique resource, it is possible to add a parameter expand to the request to extend relations with other resources:

&#x60;GET /2.0/users/me/accounts/123?expand&#x3D;transactions[category],connection&#x60;

&#x60;&#x60;&#x60;json
{
   &quot;id&quot; : 123
   &quot;name&quot; : &quot;Compte chèque&quot;
   &quot;balance&quot; : 1561.15
   &quot;transactions&quot; : [
      {
         &quot;id&quot; : 9849,
         &quot;simplified_wording&quot; : &quot;HALL&#39;S BEER&quot;,
         &quot;value&quot; : -513.20,
         ...
         &quot;category&quot; : {
            &quot;id&quot; : 561,
            &quot;name&quot; : &quot;Sorties / Bar&quot;,
            ...
         }
       },
       ...
   ],
   &quot;id_user&quot; : 1,
   &quot;connection&quot; : {
      &quot;id&quot; : 1518,
      &quot;id_bank&quot; : 41,
      &quot;id_user&quot; : 1,
      &quot;error&quot; : null,
      ...
   }
}
&#x60;&#x60;&#x60;

### Request example
&#x60;&#x60;&#x60;http
GET /2.0/banks?offset&#x3D;0&amp;limit&#x3D;10&amp;expand&#x3D;fields
Host: demo.biapi.pro
Accept: application/json
Authorization: Bearer &lt;token&gt;
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 3026
Server: Apache
Date: Fri, 14 Mar 2014 08:24:02 GMT

{
   &quot;banks&quot; : [
      {
         &quot;id_weboob&quot; : &quot;bnporc&quot;,
         &quot;name&quot; : &quot;BNP Paribas&quot;,
         &quot;id&quot; : 3,
         &quot;hidden&quot; : false,
         &quot;fields&quot; : [
            {
               &quot;id&quot; : 1,
               &quot;id_bank&quot; : 3,
               &quot;regex&quot; : &quot;^[0-9]{5,10}$&quot;,
               &quot;name&quot; : &quot;login&quot;,
               &quot;type&quot; : &quot;text&quot;,
               &quot;label&quot; : &quot;Numéro client&quot;
            },
            {
               &quot;id&quot; : 2,
               &quot;id_bank&quot; : 3,
               &quot;regex&quot; : &quot;^[0-9]{6}$&quot;,
               &quot;name&quot; : &quot;password&quot;,
               &quot;type&quot; : &quot;password&quot;,
               &quot;label&quot; : &quot;Code secret&quot;
            }
         ]
      },
      ...
   ]
   &quot;total&quot; : 41
}
&#x60;&#x60;&#x60;

### Constants
#### List of bank account types
| Type          |Description                        |
| -----------   |-----------------------------------|
| checking      |Checking account                   |
| savings       |Savings account                    |
| deposit       |Deposit accounts                   |
| loan          |Loan                               |
| market        | Market accounts                   |
| joint         |Joint account                      |
| card          |Card                               |
| lifeinsurance |Life insurance accounts            |
| pee           |Plan Épargne Entreprise            |
| perco         |Plan Épargne Retraite              |
| article83     |Article 83                         |
| rsp           |Réserve spéciale de participation  |
| pea           |Plan d&#39;épargne en actions          |
| capitalisation|Contrat de capitalisation          |
| perp          |Plan d&#39;épargne retraite populaire  |
| madelin       |Contrat retraite Madelin           |
| unknown       |Inconnu                            |

#### List of transaction types

| Type         |Description                        |
| -----------  |-----------------------------------|
|transfer      |Transfers                          |
|order         |Orders                             |
|check         |Checks                             |
|deposit       |Cash deposit                       |
|payback       |Payback                            |
|withdrawal    |Withdrawal                         |
|loan_payment  |Loan payment                       |
|bank          |Bank fees                          |
|card          |Card operation                     |
|deferred_card |Deferred card operation            |
|card_summary  |Mensual debit of a deferred card   |

#### List of synchronization errors
##### Error on Connection object
The error field may take one of the below values in case of error when accessing the user space.

| Error                      |Description                                                                                       |
| -----------------------    |--------------------------------------------------------------------------------------------------|
|wrongpass                   |The authentication on website has failed                                                          |
|additionalInformationNeeded |Additional information is needed such as an OTP                                                  |
|websiteUnavailable          |The website is unavailable, for instance we get a HTTP 503 response when requesting the website   |
|actionNeeded                |An action is needed on the website by the user, scraping is blocked                               |
|SCARequired                |An SCA process must be done by updating the connection                               |
|decoupled                  |Requires a user validation (ex: digital key)|
|passwordExpired                   |The password has expired and needs to be changed on the website.                                                         |
|webauthRequired                |A complete authentication process is required by update the connection via redirect                            |
|bug                         |A bug has occurred during the synchronization. An alert has been sent to Budget Insight           |

#### Error on Account object
Errors can be filled at the account level in case we access the user&#39;s dashboard but some account related data cannot be retrieved.
For instance, we may not access the transactions or investments for a specific account.
Getting an error during an account synchronization does not impact the scraping of other acccounts.

| Error                      |Description                                                                                       |
| -----------------------    |--------------------------------------------------------------------------------------------------|
|websiteUnavailable          |The website or a page is unavailable                                                              |
|actionNeeded                |An action is needed on the website by the user, scraping is blocked                               |
|bug                         |A bug has occurred during the synchronization. An alert has been sent to Budget Insight           |

Now you know the basics of Budgea API
- Basic call to retrieve resources
- Add query parameters to aplly filters
- Expand resources
- Authenticated calls

We&#39;re good for the basics! Now let&#39;s see how to integrate Budgea in your app and create your first user.

## Integrate Budgea *(protocol or Webview)*
### The workflow
Users of your application exist in the Budgea API.
Every User is identified by an access_token which is the shared secret between your application and our API.

The workflow is as below:
1. The user is on your application and wants to share his bank accounts or invoices.
2. A call is made **client side** (browser&#39;s javascript or desktop application) to create a temporarily token which will be used to make API calls.
3. A form is built, allowing the user to select the connector to use (bank or provider, depending on context). Every connector requires different kind of credentials.
4. A call on the API is made with the temporarily token to add a **Connection** with the credentials supplied by user.
5. In case of success, the user chooses what bank accounts (**Account**) or subscriptions (**Subscription**) he wants to share with your application.
6. When he validates the share, the temporarily token is transmitted to your server. This one will call the Budgea API with this token to get a permanent token.

**Note**
In case your application works without a server (for example a desktop application), the permanent token can be obtained on the 1st step, by supplying a client_secret to /auth/init and the step 6 is omitted. To get more information, read the protocol.

There are 3 steps to integrate Budgea in your application:
1. Provide a way for your users to share their credentials with you
2. Get the data scraped from Budgea
3. Be sure to follow the good practices before going into production

### Get credentials from users
You have 2 options here:
- Integrate the Budget Insight&#39;s Webview, a turnkey solution to get user&#39;s credentials
- Create your own form following the protocol (must have the *agent* status)

### Budgea webview

The Budgea webview complements REST API endpoints with web-based services to handle sensitive or complex operations:
- add a connection (to a bank or a provider), or edit/repare access to a connection;
- manage connections (add/remove/edit);
- edit and validate bank transfers (alpha preview).

Usage of the webview is mandatory if you don&#39;t hold an Agent status, since you are not allowed to use API endpoints carrying user credentials, and optional otherwise.

#### Implementation guidelines

##### Base URL

The base URL of all services must be customized:  
&#x60;https://{{domain}}.biapi.pro/2.0/auth/webview/&#x60;  
&#x60;https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/&#x60;  
- &#x60;{{domain}}&#x60;: substitute with you API domain;
- &#x60;{{lang}}&#x60;: optionally specify the language of the webview, &#x60;en&#x60; or &#x60;fr&#x60; (if not specified, an automatic redirection will be performed following the language of the browser).

##### Browser integration

Services available as part of the webview are designed as parameterized URLs intended to be opened in a web browser. A callback URI must be specified by callers to be notified at the end of the operation flow, similar to OAuth 2 specification.

You are encouraged to integrate web-based steps in your product following UX best practices:
- in a web environment, perform a full-page redirect to the URL (using either [HTTP redirect](https://developer.mozilla.org/fr/docs/Web/HTTP/Status/302) or [scripting](https://developer.mozilla.org/fr/docs/Web/API/Location)), and avoid new tabs or popups;
- in a native Android app, prefer opening the default browser or relying on [Chrome Custom Tabs](https://developer.chrome.com/multidevice/android/customtabs) to integrating a WebView;
- in a native iOS app, prefer using a [SFSafariViewController](https://developer.apple.com/documentation/safariservices/sfsafariviewcontroller) to integrating a WKWebView.

##### Callback handling

Most flows redirect to a callback URI at the end of the process. Query parameters are added to the URI to identify successful or failed operations.

Successful parameters are specific to each flow. In case of an error, the following parameters are added:

| Parameter | Description |
| - | - |
| &#x60;error&#x60; | An lowercase string error code identifying the kind of error that occurred. When the parameter is not present, the response is successful. |
| &#x60;error_description&#x60; | A longer string description of the error (not intended for user display). |

Common error codes include:

| Code | Description |
| - | - |
| &#x60;access_denied&#x60; | The user explicitly cancelled the flow. |
| &#x60;server_error&#x60; | Oops, a technical failure occurred during the process. |

**Forward compatibility requirement**: Additional error codes may be added in the future to describe specific cases. When implementing error codes handling, always fallback to a generic case for unknown codes.

##### Browser compatibility

The webview is designed and tested to work with browsers supported by the Angular framework:  
https://angular.io/guide/browser-support

##### Privacy / GDPR status

The webview itself does not use any kind of long-term data persistence mechanism such as cookies or local storage, but some authentication or authorization steps may delegate to third-party web services that may implement them.

#### Configuration

You can configure the appearance and behaviour of the webview by configuring the associated *Client Application* in the console:

| Key | Format | Description |
| - | - | - |
| &#x60;primary_color&#x60; | String | Optional. An accent color (hexadecimal string without &#39;#&#39; prefix) to personalize the UI elements of the webview. If absent, the default color is grey. |
| &#x60;redirect_uri&#x60; | String | Optional. A recommended security whitelist configuration. The &#x60;redirect_uri&#x60; parameter sent to any endpoint of the webview is checked against the configuration, if any. |
| &#x60;config.disable_connector_hints&#x60; | Boolean | Optional. This flags hides the list of most-used entries in the connector selection step. The default is &#x60;false&#x60;, i.e. the list is shown. |
| &#x60;config.use_app_layout&#x60; | Boolean | Optional. Use this flag to enable presenting your log as an app icon. The default value is &#x60; false&#x60;, i.e. the logo is shown in the top bar of the UI. |
| &#x60;config.disable_accounts_pre_check&#x60; | Boolean | Optional. An optional boolean flag to prevent bank accounts to be automatically pre-checked when the user enters the activation step. The default value is &#x60; false&#x60;, i.e. the bank accounts are pre-checked. |

#### Endpoints reference

##### Add connection flow
&#x60;&#x60;&#x60;
https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/connect
&#x60;&#x60;&#x60;

This flow allows an end-user to add a new connection to the API. The flow handles the following steps:
- selecting a connector;
- authenticating &amp; authorizing with the connector, by collecting credentials or delegating;
- managing consent to aggregate accounts/subscriptions;
- collecting required information for professional accounts.

###### Endpoint parameters

| Parameter | Description |
| - | - |
| &#x60;client_id&#x60; | Required. The ID of the requesting client application. You can manage client applications of your domain in the admin console. |
| &#x60;redirect_uri&#x60; | Required. An absolute callback URI. The webview will redirect to it at the end of the flow. |
| &#x60;code&#x60; | Optional. A user-scoped temporary code to use with the Budgea API.&lt;br&gt;If you don&#39;t provide a code, a new anonymous user will be created before the connection is added, and you will be returned an access token code scoped to it with the success callback. |
| &#x60;state&#x60; | Optional. An opaque string parameter that you can use to carry state across the flow. The parameter will be set &quot;as is&quot; on the callback URI. Make sure that the &#x60;state&#x60; you provide is properly URL-encoded. |
| &#x60;connector_ids&#x60; | Optional. A comma-separated list of connector IDs available to pick from.&lt;br&gt;If the parameter is omitted, all active connectors are available.&lt;br&gt;If you pass a single value, the user is not prompted to choose the connector.&lt;br&gt;This parameter is mutually exclusive with &#x60;connector_uuids&#x60;. |
| &#x60;connector_uuids&#x60; | Optional. A comma-separated list of connector UUIDs available to pick from.&lt;br&gt;If the parameter is omitted, all active connectors are available.&lt;br&gt;If you pass a single value, the user is not prompted to choose the connector.&lt;br&gt;This parameter is mutually exclusive with &#x60;connector_ids&#x60;. |
| &#x60;connector_capabilities&#x60; | Optional. A comma-separated list of capabilities to filter available connectors.&lt;br&gt;If the parameter is omitted, &#x60;bank&#x60; is inferred.&lt;br&gt;If multiple values are provided, only connectors that expose all the requested capabilities are available.&lt;br&gt;To request a bank connection, use &#x60;bank&#x60;.&lt;br&gt;To request a provider connection, use &#x60;document&#x60;. |
| &#x60;account_ibans&#x60; | Optional. A comma-separated list of IBANs to filter accounts available for activation in a bank connection context. Other accounts will not be selectable. |
| &#x60;account_types&#x60; | Optional. A comma-separated list of account types to filter accounts available for activation in a bank connection context. Other accounts will not be selectable. |
| &#x60;account_usages&#x60; | Optional. A comma-separated list of account usages to filter accounts available for activation in a bank connection context. Other accounts will not be selectable. |

###### Successful callback parameters

| Parameter | Description |
| - | - |
| &#x60;connection_id&#x60; | The id of the newly created connection. Please note that when redirecting to the callback URI, the accounts and/or subscriptions are available in the API, but bank transactions or documents may still be syncing in background. |
| &#x60;code&#x60; | Optional. If a &#x60;code&#x60; was *not* initially specified, an API code that you must exchange to obtain a permanent access token associated with the newly-created anonymous user holding the connection. The parameter is URL-encoded, make sure to handle it accordingly. |
| &#x60;state&#x60; | Optional. Identical to the &#x60;state&#x60; parameter that was initially specified. |

###### Additional error codes

| Code | Description |
| - | - |
| &#x60;tos_declined&#x60; | The end-user refused to validate the terms of service. |

##### Re-auth / edit connection credentials flow

&#x60;&#x60;&#x60;
https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/reconnect
&#x60;&#x60;&#x60;

This flow allows an end-user to re-authenticate against a bank or a provider in order to recover an existing connection, or to completely reset credentials associated with a connection.

###### Endpoint parameters

| Parameter | Description |
| - | - |
| &#x60;client_id&#x60; | Required. The ID of the requesting client application. You can manage client applications of your domain in the admin console. |
| &#x60;redirect_uri&#x60; | Required. An absolute callback URI. The webview will redirect to it at the end of the flow. |
| &#x60;code&#x60; | Required. A user-scoped temporary code to use with the Budgea API. |
| &#x60;connection_id&#x60; | Required. The id of the existing connection. |
| &#x60;state&#x60; | Optional. An opaque string parameter that you can use to carry state across the flow. The parameter will be set &quot;as is&quot; on the callback URI. Make sure that the &#x60;state&#x60; you provide is properly URL-encoded. |
| &#x60;reset_credentials&#x60; | Optional. In the default mode (&#x60;false&#x60;), the service will try to recover the connection and prompt the user only with outdated or transient information (new password, OTP...).&lt;br&gt;Set the parameter to &#x60;true&#x60; to force resetting all the credentials associated with the connection. This parameter may not apply to all connectors. |

###### Successful callback parameters

This flow adds no parameter to the callback URI in case of success, except from &#x60;state&#x60;.

##### Manage connections

&#x60;&#x60;&#x60;
https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/manage
&#x60;&#x60;&#x60;
This flow allows an end-user to manage the connections associated with his account in the API. The user can add new connections, remove existing ones, fix connection errors, reset credentials or activate/deactivate bank accounts.

Support of &#x60;redirect_uri&#x60; in this flow is optional, as it can be integrated or presented as a terminal step, without relying on a final redirection.

###### Endpoint parameters

| Parameter | Description |
| - | - |
| &#x60;client_id&#x60; | Required. The ID of the requesting client application. You can manage client applications of your domain in the admin console. |
| &#x60;code&#x60; | Required. A user-scoped temporary code to use with the Budgea API. |
| &#x60;redirect_uri&#x60; | Optional. An absolute callback URI. When provided, the webview will display a close button that redirects to it. |
| &#x60;state&#x60; | Optional. An opaque string parameter that you can use to carry state across the flow when providing a &#x60;redirect_uri&#x60;. The parameter will be set &quot;as is&quot; on the callback URI. Make sure that the &#x60;state&#x60; you provide is properly URL-encoded. |
| &#x60;connector_capabilities&#x60; | Optional. A comma-separated list of capabilities to filter available connectors when adding a new connection.&lt;br&gt;If the parameter is omitted, &#x60;bank&#x60; is inferred.&lt;br&gt;If multiple values are provided, only connectors that expose all the requested capabilities are available.&lt;br&gt;To request a bank connection, use &#x60;bank&#x60;.&lt;br&gt;To request a provider connection, use &#x60;document&#x60;. |
| &#x60;account_types&#x60; | Optional. A comma-separated list of account types to filter accounts available for activation on adding a new bank connection or updating existing connections. Other accounts will not be selectable. |
| &#x60;account_usages&#x60; | Optional. A comma-separated list of account usages to filter accounts available for activation in a bank connection context. Other accounts will not be selectable. |

###### Callback parameters

This flow adds no parameter to the callback URI, except from &#x60;state&#x60;.

##### Execute a bank transfer (preview)

**Disclaimer**: Transfer or payment services are available as a preview, protocols and parameters are subject to change in upcoming beta/final releases.

&#x60;&#x60;&#x60;
https://{{domain}}.biapi.pro/2.0/auth/webview/{{lang}}/transfer
&#x60;&#x60;&#x60;
This flow allows an end-user to execute a bank transfer. The flow handles the following steps:
- if the transfer is not already created, all steps to authenticate with a bank, select the recipient, the emitter account, the amount and label;
- executing the transfer, including managing SCAs for recipient registration and/or transfer validation.

###### Endpoint parameters

| Parameter | Description |
| - | - |
| &#x60;client_id&#x60; | Required. The ID of the requesting client application. You can manage client applications of your domain in the admin console. |
| &#x60;redirect_uri&#x60; | Required. An absolute callback URI. The webview will redirect to it at the end of the flow. |
| &#x60;code&#x60; | Required. A user-scoped temporary code to use with the Budgea API.&lt;br&gt;If you don&#39;t provide a code, a new anonymous user will be created before a connection is added and the transfer is executed, and you will be returned an access token code scoped to it with the success callback. |
| &#x60;state&#x60; | Optional. An opaque string parameter that you can use to carry state across the flow. The parameter will be set &quot;as is&quot; on the callback URI. Make sure that the &#x60;state&#x60; you provide is properly URL-encoded. |
| &#x60;transfer_id&#x60;| Optional. The ID of an prepared transfer to be validated in the webview. The user cannot edit anything on the transfer before validation. |

###### Successfull callback parameters

| Parameter | Description |
| - | - |
| &#x60;transfer_id&#x60; | The ID of the transfer that was created and executed. |
| &#x60;code&#x60; | Optional. If a &#x60;code&#x60; was *not* initially specified, an API code that you can exchange to obtain a permanent access token associated with the newly-created anonymous user holding the transfer. The parameter is URL-encoded, make sure to handle it accordingly. |
| &#x60;state&#x60; | Optional. Identical to the &#x60;state&#x60; parameter that was initially specified. |

###### Additional error codes

| Code | Description |
| - | - |
| &#x60;tos_declined&#x60; | The end-user refused to validate the terms of service. |

#### Migrating from v3

We provide a full backward compatibility layer with current implementations of the webview v3 to ease the transition. All endpoints remains accessible, with the same parameters and callback behaviour. Migration instructions are provided below.

*The v3 compatibility mode is expected to be removed on 31 December 2019.* You should migrate your implementation a soon as possible to new endpoints and parameters.

##### Add connection flow / Edit connection credentials  
&#x60;&#x60;&#x60;
/connect/select
&#x60;&#x60;&#x60;

This endpoint has been superseded by &#x60;/connect&#x60; (no suffix) for adding a new connection, and &#x60;/reconnect&#x60; for resetting or updating an existing connection.

| Endpoint parameter | Migration instructions |
| - | - |
| &#x60;client_id&#x60; | No change. |
| &#x60;redirect_uri&#x60;, &#x60;state&#x60; | No change. |
| &#x60;response_type&#x60; | This parameter is not used anymore. |
| &#x60;id_connector&#x60;, &#x60;connectors&#x60; | Superseded by &#x60;connector_ids&#x60; sent to the &#x60;/connect&#x60; endpoint. |
| &#x60;types&#x60; | Superseded by &#x60;connector_capabilities&#x60; sent to the &#x60;/connect&#x60; endpoint.&lt;br&gt;Use&#x60;connector_capabilities&#x3D;bank&#x60; (bank connection) or &#x60;connector_capabilities&#x3D;document&#x60; (provider connection). |
| &#x60;id_connection&#x60; | Superseded by &#x60;connection_id&#x60; sent to the &#x60;/reconnect&#x60; endpoint. |

Passing the code or access token as an URL fragment is no longer supported, use the &#x60;code&#x60; query parameter.

| Callback parameter | Migration instructions |
| - | - |
| &#x60;id_connection&#x60; | Superseded by &#x60;connection_id&#x60;.&lt;br&gt;In the &#x60;/reconnect&#x60; flow, this parameter is not returned anymore. |
| &#x60;code&#x60; | Still named &#x60;code&#x60;, but in the &#x60;/connect&#x60; flow the parameter is now **only** added if an anonymous user was created, i.e. the &#x60;code&#x60; parameter was **not** provided as a query parameter or fragment.&lt;br&gt;In the &#x60;/reconnect&#x60; flow, this parameter is not returned anymore. |
| &#x60;state&#x60; | No change. |

##### Manage connections

&#x60;&#x60;&#x60;
/accounts
&#x60;&#x60;&#x60;

This endpoint has been superseded by &#x60;/manage&#x60;, that now fully allows users to add/remove connections, reset their credentials or recover from error states.

| Endpoint parameter | Migration instructions |
| - | - |
| &#x60;client_id&#x60; | No change. |
| &#x60;redirect_uri&#x60;, &#x60;state&#x60; | No change, these parameters are now optional. |
| &#x60;response_type&#x60; | This parameter is not used anymore. |
| &#x60;types&#x60; | Superseded by &#x60;connector_capabilities&#x60;.&lt;br&gt;Use&#x60;connector_capabilities&#x3D;bank&#x60; (bank connection) or &#x60;connector_capabilities&#x3D;document&#x60; (provider connection). |

Passing the code or access token as an URL fragment is no longer supported, use the &#x60;code&#x60; query parameter.

| Callback parameter | Migration instructions |
| - | - |
| &#x60;code&#x60; | This parameter is not returned anymore. |
| &#x60;state&#x60; | No change. |

##### Behaviour change

In v3, the &#x60;/accounts&#x60; flow used to redirect to the &#x60;redirect_uri&#x60; after a connection addition. This is no longer the case in v4, where redirection is only performed when the user explicitly closes the flow. If you need to perform actions when a connection is added or removed, you should rely on webhooks.

#### Protocol
This section describes the protocol used to set bank and provider accounts of a user, in case you don&#39;t want to use the webview.

The idea is to call the following services client-side (with AJAX in case of a web application), to ensure the bank and providers credentials will not be sent to your servers.

1. /auth/init
&#x60;&#x60;&#x60;http
POST /auth/init
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;json
{
   &quot;auth_token&quot; : &quot;fBqjMZbYddebUGlkR445JKPA6pCoRaGb&quot;,
   &quot;type&quot; : &quot;temporary&quot;,
   &quot;expires_in&quot; : 1800,
   &quot;id_user&quot;: 1
}
&#x60;&#x60;&#x60;
This service creates a temporarily token, to use in the &quot;Authorization&quot; header in next calls to the API

The returned token has a life-time of 30 minutes, and should be transfered to the API then (cf Permanent Token), so that your server can get a permanent access_token.

It is possible to generate a permanent token immediately, by calling the service with the manage_token, or by supply parameters client_id and client_secret.

2. /banks or /providers
&#x60;&#x60;&#x60;http
GET /banks?expand&#x3D;fields
Authorization: Bearer &lt;token&gt;
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;json
{
   &quot;hidden&quot; : false,
         &quot;charged&quot; : true,
         &quot;name&quot; : &quot;American Express&quot;,
         &quot;id&quot; : 30,
         &quot;fields&quot; : [
            {
               &quot;values&quot; : [
                  {
                     &quot;label&quot; : &quot;Particuliers/Professionnels&quot;,
                     &quot;value&quot; : &quot;pp&quot;
                  },
                  {
                     &quot;value&quot; : &quot;ent&quot;,
                     &quot;label&quot; : &quot;Entreprises&quot;
                  }
               ],
               &quot;label&quot; : &quot;Type de compte&quot;,
               &quot;regex&quot; : null,
               &quot;name&quot; : &quot;website&quot;,
               &quot;type&quot; : &quot;list&quot;
            },
            {
               &quot;type&quot; : &quot;password&quot;,
               &quot;label&quot; : &quot;Code secret&quot;,
               &quot;name&quot; : &quot;password&quot;,
               &quot;regex&quot; : &quot;^[0-9]{6}$&quot;
            }
         ],
      },
      ...
   ],
   &quot;total&quot; : 44,
}
&#x60;&#x60;&#x60;
You get a list of connectors, and all associated fields needed to build the form at step 3.
You can also use that list to show to your user, all available banks.

3. /users/me/connections
Make a POST request and supply the id_bank (ID of the chosen bank) or id_provider (ID of provider), and all requested fields as key/value parameters.
For example:
&#x60;&#x60;&#x60;http
POST /users/me/connections
Authorization: Bearer &lt;token&gt;
-F login&#x3D;12345678
-F password&#x3D;123456
-F id_bank&#x3D;59
&#x60;&#x60;&#x60;
You can get the following return codes:

|Code           |Description                                                  |
|---------------|------------------------------------------------------------ |
|200            |The connection has succeed and has been created              |
|202            |It is necessary to provide complementary information. This occurs on the first connection on some kind of Boursorama accounts for example, where a SMS is sent to the customer. It is necessary to ask the user to fill fields requested in the fields, and do a POST again on /users/me/connections/ID, with the connection ID in id_connection. |
|400            |Unable to connect to the website, the field error in the JSON can be **websiteUnavailable** or **wrongpass**  |
|403            |Invalid token                                                |

4. Activate accounts
The accounts the user wants to aggregate must be activated before any transaction or investment is retrieved.
Several accounts can be activated in 1 request by separating the account ids with commas.
&#x60;&#x60;&#x60;http
PUT /users/me/connections/&lt;id_connection&gt;/accounts/&lt;id_account&gt;?all
&#x60;&#x60;&#x60;

5. Permanent token
If the user validates the share of his accounts, it is necessary to transform the temporary code to a permanent access_token (so that the user won&#39;t expire).

To do that, make a POST request on /auth/token/access with the following parameters:
|Parameter            |Description                                                     |
|---------------------|----------------------------------------------------------------|
|code                 |The temporarily token which will let you get the access_token   |
|client_id            |The ID of your client application                               |
|client_secret        |The secret of your client application                           |

&#x60;&#x60;&#x60;json
POST /auth/token/access

{
   &quot;client_id&quot; : 17473055,
   &quot;client_secret&quot; : &quot;54tHJHjvodbANVzaRtcLzlHGXQiOgw80&quot;,
   &quot;code&quot; : &quot;fBqjMZbYddebUGlkR445JKPA6pCoRaGb&quot;
}
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;http
HTTP/1.1 200 OK

{
   &quot;access_token&quot; : &quot;7wBPuFfb1Hod82f1+KNa0AmrkIuQ3h1G&quot;,
   &quot;token_type&quot;:&quot;Bearer&quot;
}
&#x60;&#x60;&#x60;

### Update accounts
Another important call is when a user wants to add/remove connections to banks or providers, or to change the password on one of them, it is advised to give him a temporarily code from the permanent access_token, with the following call (using the access_token as bearer):
&#x60;&#x60;&#x60;http
POST /auth/token/code
Authorization: Bearer &lt;token&gt;
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;json
{
   &quot;code&quot; : &quot;/JiDppWgbmc+5ztHIUJtHl0ynYfw682Z&quot;,
   &quot;type&quot; : &quot;temporary&quot;,
   &quot;expires_in&quot; : 1800,
}
&#x60;&#x60;&#x60;
Its life-time is 30 minutes, and let the browser to list connections and accounts, via &#x60;GET /users/me/connections?expand&#x3D;accounts&#x60; for example.

 To update the password of a connection, you can do a POST on the *connection* resource, with the field *password* in the data. The new credentials are checked to make sure they are valid, and the return codes are the same as when adding a connection.

## Getting the data (Webhooks)
You have created your users and their connections, now it&#39;s time to get the data.
There are 2 ways to retrieve it, the 2 can be complementary:
- make regular calls to the API
- use the webhooks (recommended)

### Manual Synchronization
It is possible to do a manual synchronization of a user. We recommend to use this method in case the user wants fresh data after logging in.

To trigger the synchronization, call the API as below:
&#x60;PUT /users/ID/connections&#x60;
The following call is blocking until the synchronization is terminated.

Even if it is not recommended, it&#39;s possible to fetch synchronously new data. To do that, you can use the *expand* parameter:
&#x60; /users/ID/connections?expand&#x3D;accounts[transactions,investments[type]],subscriptions&#x60;
&#x60;&#x60;&#x60;json
{
   &quot;connections&quot; : [
      {
         &quot;accounts&quot; : [
            {
               &quot;balance&quot; : 7481.01,
               &quot;currency&quot; : {
                  &quot;symbol&quot; : &quot;€&quot;,
                  &quot;id&quot; : &quot;EUR&quot;,
                  &quot;prefix&quot; : false
               },
               &quot;deleted&quot; : null,
               &quot;display&quot; : true,
               &quot;formatted_balance&quot; : &quot;7 481,01 €&quot;,
               &quot;iban&quot; : &quot;FR76131048379405300290000016&quot;,
               &quot;id&quot; : 17,
               &quot;id_connection&quot; : 7,
               &quot;investments&quot; : [
                  {
                     &quot;code&quot; : &quot;FR0010330902&quot;,
                     &quot;description&quot; : &quot;&quot;,
                     &quot;diff&quot; : -67.86,
                     &quot;id&quot; : 55,
                     &quot;id_account&quot; : 19,
                     &quot;id_type&quot; : 1,
                     &quot;label&quot; : &quot;Agressor PEA&quot;,
                     &quot;portfolio_share&quot; : 0.48,
                     &quot;prev_diff&quot; : 2019.57,
                     &quot;quantity&quot; : 7.338,
                     &quot;type&quot; : {
                        &quot;color&quot; : &quot;AABBCC&quot;,
                        &quot;id&quot; : 1,
                        &quot;name&quot; : &quot;Fonds action&quot;
                     },
                     &quot;unitprice&quot; : 488.98,
                     &quot;unitvalue&quot; : 479.73,
                     &quot;valuation&quot; : 3520.28
                  }
               ],
               &quot;last_update&quot; : &quot;2015-07-04 15:17:30&quot;,
               &quot;name&quot; : &quot;Compte chèque&quot;,
               &quot;number&quot; : &quot;3002900000&quot;,
               &quot;transactions&quot; : [
                  {
                     &quot;active&quot; : true,
                     &quot;application_date&quot; : &quot;2015-06-17&quot;,
                     &quot;coming&quot; : false,
                     &quot;comment&quot; : null,
                     &quot;commission&quot; : null,
                     &quot;country&quot; : null,
                     &quot;date&quot; : &quot;2015-06-18&quot;,
                     &quot;date_scraped&quot; : &quot;2015-07-04 15:17:30&quot;,
                     &quot;deleted&quot; : null,
                     &quot;documents_count&quot; : 0,
                     &quot;formatted_value&quot; : &quot;-16,22 €&quot;,
                     &quot;id&quot; : 309,
                     &quot;id_account&quot; : 17,
                     &quot;id_category&quot; : 9998,
                     &quot;id_cluster&quot; : null,
                     &quot;last_update&quot; : &quot;2015-07-04 15:17:30&quot;,
                     &quot;new&quot; : true,
                     &quot;original_currency&quot; : null,
                     &quot;original_value&quot; : null,
                     &quot;original_wording&quot; : &quot;FACTURE CB HALL&#39;S BEER&quot;,
                     &quot;rdate&quot; : &quot;2015-06-17&quot;,
                     &quot;simplified_wording&quot; : &quot;HALL&#39;S BEER&quot;,
                     &quot;state&quot; : &quot;parsed&quot;,
                     &quot;stemmed_wording&quot; : &quot;HALL&#39;S BEER&quot;,
                     &quot;type&quot; : &quot;card&quot;,
                     &quot;value&quot; : -16.22,
                     &quot;wording&quot; : &quot;HALL&#39;S BEER&quot;
                  }
               ],
               &quot;type&quot; : &quot;checking&quot;
            }
         ],
         &quot;error&quot; : null,
         &quot;expire&quot; : null,
         &quot;id&quot; : 7,
         &quot;id_user&quot; : 7,
         &quot;id_bank&quot; : 41,
         &quot;last_update&quot; : &quot;2015-07-04 15:17:31&quot;
      }
   ],
   &quot;total&quot; : 1,
}
&#x60;&#x60;&#x60;

### Background synchronizations &amp; Webhooks
Webhooks are callbacks sent to your server, when an event is triggered during a synchronization.
Synchronizations are automatic, the frequency can be set using the configuration key &#x60;autosync.frequency&#x60;.
Using webhooks allows you to get the most up-to-date data of your users, after each synchronization.

The automatic synchronization makes it possible to recover new bank entries, or new invoices, at a given frequency.
You have the possibility to add webhooks on several events, and choose to receive each one on a distinct URL.
To see the list of available webhooks you can call the endpoint hereunder:
&#x60;&#x60;&#x60;
curl https://demo.biapi.pro/2.0/webhooks_events \
  -H &#39;Authorization: Bearer &lt;token&gt;&#39;
&#x60;&#x60;&#x60;

The background synchronizations for each user are independent, and their plannings are spread over the day so that they do not overload any website.

Once the synchronization of a user is over, a POST request is sent on the callback URL you have defined, including all webhook data.
A typical json sent to your server is as below:
&#x60;&#x60;&#x60;http
POST /callback HTTP/1.1
Host: example.org
Content-Length: 959
Accept-Encoding: gzip, deflate, compress
Accept: */*
User-Agent: Budgea API/2.0
Content-Type: application/json; charset&#x3D;utf-8
Authorization: Bearer sl/wuqgD2eOo+4Zf9FjvAz3YJgU+JKsJ

{
   &quot;connections&quot; : [
      {
         &quot;accounts&quot; : [
            {
               &quot;balance&quot; : 7481.01,
               &quot;currency&quot; : {
                  &quot;symbol&quot; : &quot;€&quot;,
                  &quot;id&quot; : &quot;EUR&quot;,
                  &quot;prefix&quot; : false
               },
               &quot;deleted&quot; : null,
               &quot;display&quot; : true,
               &quot;formatted_balance&quot; : &quot;7 481,01 €&quot;,
               &quot;iban&quot; : &quot;FR76131048379405300290000016&quot;,
               &quot;id&quot; : 17,
               &quot;id_connection&quot; : 7,
               &quot;investments&quot; : [
                  {
                     &quot;code&quot; : &quot;FR0010330902&quot;,
                     &quot;description&quot; : &quot;&quot;,
                     &quot;diff&quot; : -67.86,
                     &quot;id&quot; : 55,
                     &quot;id_account&quot; : 19,
                     &quot;id_type&quot; : 1,
                     &quot;label&quot; : &quot;Agressor PEA&quot;,
                     &quot;portfolio_share&quot; : 0.48,
                     &quot;prev_diff&quot; : 2019.57,
                     &quot;quantity&quot; : 7.338,
                     &quot;type&quot; : {
                        &quot;color&quot; : &quot;AABBCC&quot;,
                        &quot;id&quot; : 1,
                        &quot;name&quot; : &quot;Fonds action&quot;
                     },
                     &quot;unitprice&quot; : 488.98,
                     &quot;unitvalue&quot; : 479.73,
                     &quot;valuation&quot; : 3520.28
                  }
               ],
               &quot;last_update&quot; : &quot;2015-07-04 15:17:30&quot;,
               &quot;name&quot; : &quot;Compte chèque&quot;,
               &quot;number&quot; : &quot;3002900000&quot;,
               &quot;transactions&quot; : [
                  {
                     &quot;active&quot; : true,
                     &quot;application_date&quot; : &quot;2015-06-17&quot;,
                     &quot;coming&quot; : false,
                     &quot;comment&quot; : null,
                     &quot;commission&quot; : null,
                     &quot;country&quot; : null,
                     &quot;date&quot; : &quot;2015-06-18&quot;,
                     &quot;date_scraped&quot; : &quot;2015-07-04 15:17:30&quot;,
                     &quot;deleted&quot; : null,
                     &quot;documents_count&quot; : 0,
                     &quot;formatted_value&quot; : &quot;-16,22 €&quot;,
                     &quot;id&quot; : 309,
                     &quot;id_account&quot; : 17,
                     &quot;id_category&quot; : 9998,
                     &quot;id_cluster&quot; : null,
                     &quot;last_update&quot; : &quot;2015-07-04 15:17:30&quot;,
                     &quot;new&quot; : true,
                     &quot;original_currency&quot; : null,
                     &quot;original_value&quot; : null,
                     &quot;original_wording&quot; : &quot;FACTURE CB HALL&#39;S BEER&quot;,
                     &quot;rdate&quot; : &quot;2015-06-17&quot;,
                     &quot;simplified_wording&quot; : &quot;HALL&#39;S BEER&quot;,
                     &quot;state&quot; : &quot;parsed&quot;,
                     &quot;stemmed_wording&quot; : &quot;HALL&#39;S BEER&quot;,
                     &quot;type&quot; : &quot;card&quot;,
                     &quot;value&quot; : -16.22,
                     &quot;wording&quot; : &quot;HALL&#39;S BEER&quot;
                  }
               ],
               &quot;type&quot; : &quot;checking&quot;
            }
         ],
         &quot;bank&quot; : {
            &quot;id_weboob&quot; : &quot;ing&quot;,
            &quot;charged&quot; : true,
            &quot;name&quot; : &quot;ING Direct&quot;,
            &quot;id&quot; : 7,
            &quot;hidden&quot; : false
         },
         &quot;error&quot; : null,
         &quot;expire&quot; : null,
         &quot;id&quot; : 7,
         &quot;id_user&quot; : 7,
         &quot;id_bank&quot; : 41,
         &quot;last_update&quot; : &quot;2015-07-04 15:17:31&quot;
      }
   ],
   &quot;total&quot; : 1,
   &quot;user&quot; : {
      &quot;signin&quot; : &quot;2015-07-04 15:17:29&quot;,
      &quot;id&quot; : 7,
      &quot;platform&quot; : &quot;sharedAccess&quot;
   }
}
&#x60;&#x60;&#x60;
The authentication on the callback is made with the access_token of the user (which is a shared secret between your server and the Budgea API).

When you are in production, it is needed to define a HTTPS URL using a valid certificate, delivered by a recognized authority. If this is not the case, you can contact us to add your CA (Certificate Authority) to our PKI (Public Key Infrastructure).

Important: it is necessary to send back a HTTP 200 code, without what we consider that data is not correctly taken into account on your system, and it will be sent again at the next user synchronization.

## Guidelines for production
Now you should have integrated the API inside your application. Make sure your Webhooks URLs are in HTTPS, if so you can enable the production state of the API.

To make things great, here are some good practices, please check you have respected them:
- You have provided to your users a way to configure their accounts
- You have provided to your users a way to change their account passwords
- You consider the **error** field of Connections, to alert the user in case the state is **wrongpass**
- You map IDs of Accounts, Subscriptions, Transactions and Documents in your application, to be sure to correctly match them
- When the deleted field is set on a bank transaction, you delete it in your database
- You don&#39;t loop on all users to launch synchronizations, this might saturate the service

If you have questions about above points, please contact us. Otherwise, you can put into production!

### Going further
If you want to raise the bar for your app and add features such as the ability to do transfers, get invoices, aggregate patrimony and more, please refer to the sections below.
We&#39;ll discuss complementary APIs building upon the aggregation, allowing for the best of financial apps.

## Budgea API Pay
This API allows for the emition of transfers between the aggregated accounts.
Just like the simple aggregation, BI provides a webview or a protocol to follow, to implement this feature.

### API pay protocol
This section describes how the transfer and recipient protocol work, in case you don&#39;t want to integrate the webview.
The idea is to do following calls client side (with AJAX in case of a web application), so that the interaction with the Budgea API is transparent.

#### Executing a transfer
1. /auth/token/code
If you do calls client side, get a new temporary code for the user, from the access_token. This will prevent security issues.
&#x60;&#x60;&#x60;
curl -d &#39;&#39; \
  https://demo.biapi.pro/2.0/auth/token/code \
  -H &#39;Authorization: Bearer &lt;token&gt;&#39;
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;json
{
   &quot;code&quot;: &quot;/JiDppWgbmc+5ztHIUJtHl0ynYfw682Z&quot;,
   &quot;type&quot;: &quot;temporary&quot;,
   &quot;expires_in&quot;: 1800
}
&#x60;&#x60;&#x60;
The returned token has a life-time of 30 minutes.

2. /users/me/accounts?able_to_transfer&#x3D;1
List all the accounts that can do transfers. Authenticate the call with the code you got at step 1.
&#x60;&#x60;&#x60;
curl https://demo.biapi.pro/2.0/users/me/accounts?able_to_transfer&#x3D;1 \
  -H &#39;Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z&#39;
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;json
{
  &quot;accounts&quot; : [
      {
         &quot;display&quot; : true,
         &quot;balance&quot; : 2893.36,
         &quot;id_type&quot; : 2,
         &quot;number&quot; : &quot;****1572&quot;,
         &quot;type&quot; : &quot;checking&quot;,
         &quot;deleted&quot; : null,
         &quot;bic&quot; : &quot;BNPAFRPPXXX&quot;,
         &quot;bookmarked&quot; : false,
         &quot;coming&quot; : -2702.74,
         &quot;id_user&quot; : 1,
         &quot;original_name&quot; : &quot;Compte de chèques&quot;,
         &quot;currency&quot; : {
            &quot;symbol&quot; : &quot;€&quot;,
            &quot;id&quot; : &quot;EUR&quot;,
            &quot;prefix&quot; : false
         },
         &quot;name&quot; : &quot;lol&quot;,
         &quot;iban&quot; : &quot;FR7630004012550000041157244&quot;,
         &quot;last_update&quot; : &quot;2016-12-28 12:31:04&quot;,
         &quot;id&quot; : 723,
         &quot;formatted_balance&quot; : &quot;2893,36 €&quot;,
         &quot;able_to_transfer&quot; : true,
         &quot;id_connection&quot; : 202
      }
   ],
   &quot;total&quot; : 1
}
&#x60;&#x60;&#x60;

3. /users/me/accounts/ID/recipients
List all available recipients for a given account.
&#x60;&#x60;&#x60;
curl https://demo.biapi.pro/2.0/users/me/accounts/723/recipients?limit&#x3D;1 \
  -H &#39;Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z&#39;
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;json
{
  &quot;total&quot; : 27,
   &quot;recipients&quot; : [
      {
         &quot;bank_name&quot; : &quot;BNP PARIBAS&quot;,
         &quot;bic&quot; : &quot;BNPAFRPPXXX&quot;,
         &quot;category&quot; : &quot;Interne&quot;,
         &quot;deleted&quot; : null,
         &quot;enabled_at&quot; : &quot;2016-10-31 18:52:53&quot;,
         &quot;expire&quot; : null,
         &quot;iban&quot; : &quot;FR7630004012550003027641744&quot;,
         &quot;id&quot; : 1,
         &quot;id_account&quot; : 1,
         &quot;id_target_account&quot; : 2,
         &quot;label&quot; : &quot;Livret A&quot;,
         &quot;last_update&quot; : &quot;2016-12-05 12:07:24&quot;,
         &quot;time_scraped&quot; : &quot;2016-10-31 18:52:54&quot;,
         &quot;webid&quot; : &quot;2741588268268091098819849694548441184167285851255682796371&quot;
      }
   ]
}
&#x60;&#x60;&#x60;

4. /users/me/accounts/ID/recipients/ID/transfers
Create the transfer
&#x60;&#x60;&#x60;
curl \
  https://demo.biapi.pro/2.0/users/me/accounts/1/recipients/1/transfers \
  -H &#39;Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z&#39; \
  -F amount&#x3D;10, \
  -F label&#x3D;&quot;Test virement&quot;, \
  -F exec_date&#x3D;&quot;2018-09-12&quot; // optional
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;json
{
   &quot;account_iban&quot; : &quot;FR7630004012550000041157244&quot;,
   &quot;amount&quot; : 10,
   &quot;currency&quot; : {
      &quot;id&quot; : &quot;EUR&quot;,
      &quot;prefix&quot; : false,
      &quot;symbol&quot; : &quot;€&quot;
   },
   &quot;exec_date&quot; : &quot;2018-09-12&quot;,
   &quot;fees&quot; : null
   &quot;formatted_amount&quot; : &quot;10,00 €&quot;,
   &quot;id&quot; : 22,
   &quot;id_account&quot; : 1,,
   &quot;id_recipient&quot; : 1,
   &quot;label&quot; : &quot;Test virement&quot;,
   &quot;recipient_iban&quot; : &quot;FR7630004012550003027641744&quot;,
   &quot;register_date&quot; : &quot;2018-09-12 10:34:59&quot;,
   &quot;state&quot; : &quot;created&quot;,
   &quot;webid&quot; : null
}
&#x60;&#x60;&#x60;

5. /users/me/transfers/ID
Execute the transfer
&#x60;&#x60;&#x60;
curl \
  https://demo.biapi.pro/2.0/users/me/transfers/22 \
  -H &#39;Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z&#39; \
  -F validated&#x3D;true
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;json
{
   &quot;account_iban&quot; : &quot;FR7630004012550000041157244&quot;,
   &quot;amount&quot; : 10,
   &quot;currency&quot; : {
      &quot;id&quot; : &quot;EUR&quot;,
      &quot;prefix&quot; : false,
      &quot;symbol&quot; : &quot;€&quot;
   },
   &quot;exec_date&quot; : &quot;2016-12-19&quot;,
   &quot;fees&quot; : null,
   &quot;fields&quot; : [
      {
         &quot;label&quot; : &quot;Code secret BNP Paribas&quot;,
         &quot;type&quot; : &quot;password&quot;,
         &quot;regex&quot; : &quot;^[0-9]{6}$&quot;,
         &quot;name&quot; : &quot;password&quot;
      }
   ],
   &quot;formatted_amount&quot; : &quot;10,00 €&quot;,
   &quot;id&quot; : 22,
   &quot;id_account&quot; : 1,
   &quot;id_recipient&quot; : 1,
   &quot;label&quot; : &quot;Test virement&quot;,
   &quot;recipient_iban&quot; : &quot;FR7630004012550003027641744&quot;,
   &quot;register_date&quot; : &quot;2016-12-19 10:34:59&quot;,
   &quot;state&quot; : &quot;created&quot;,
   &quot;webid&quot; : null
}
&#x60;&#x60;&#x60;
Here, an authentication step asks user to enter his bank password. The transfer can be validated with:

&#x60;&#x60;&#x60;
curl \
  https://demo.biapi.pro/2.0/users/me/transfers/22 \
  -H &#39;Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z&#39; \
  -F validated&#x3D;true \
  -F password&#x3D;&quot;123456&quot;
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;json
{
   &quot;account_iban&quot; : &quot;FR7630004012550000041157244&quot;,
   &quot;currency&quot; : {
      &quot;id&quot; : &quot;EUR&quot;,
      &quot;prefix&quot; : false,
      &quot;symbol&quot; : &quot;€&quot;
   },
   &quot;amount&quot; : 10,
   &quot;exec_date&quot; : &quot;2016-12-19&quot;,
   &quot;fees&quot; : 0,
   &quot;formatted_amount&quot; : &quot;10,00 €&quot;,
   &quot;id&quot; : 22,
   &quot;id_account&quot; : 1,
   &quot;id_recipient&quot; : 1,
   &quot;label&quot; : &quot;Test virement&quot;,
   &quot;recipient_iban&quot; : &quot;FR7630004012550003027641744&quot;,
   &quot;register_date&quot; : &quot;2016-12-19 10:34:59&quot;,
   &quot;state&quot; : &quot;pending&quot;,
   &quot;webid&quot; : &quot;ZZ10C4FKSNP05TK95&quot;
}
&#x60;&#x60;&#x60;
The field state is changed to *pending*, telling that the transfer has been correctly executed on the bank. A connection synchronization is then launched, to find the bank transaction in the movements history. In this case, the transfer state will be changed to *done*.

#### Adding a recipient
1. /auth/token/code
Get a temporary token for the user. Same procedure than step 1 for a transfer.

2. /users/me/accounts?able_to_transfer&#x3D;1
List accounts allowing transfers. Same procedure than step 2 for a transfer.

3. /users/me/accounts/ID/recipients/
Add a new recipient.
&#x60;&#x60;&#x60;
curl \
  https://demo.biapi.pro/2.0/users/me/accounts/1/recipients \
  -H &#39;Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z&#39; \
  -F iban&#x3D;FR7613048379405300290000355 \
  -F label&#x3D;&quot;Papa&quot;, \
  -F category&#x3D;&quot;Famille&quot; // optional
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;json
{
   &quot;bank_name&quot; : &quot;BNP PARIBAS&quot;,
   &quot;bic&quot; : &quot;BNPAFRPPXXX&quot;,
   &quot;category&quot; : &quot;Famille&quot;,
   &quot;deleted&quot; : null,
   &quot;enabled_at&quot; : null,
   &quot;expire&quot; : &quot;2017-04-29 16:56:20&quot;,
   &quot;fields&quot; : [
      {
         &quot;label&quot; : &quot;Veuillez entrer le code reçu par SMS&quot;,
         &quot;type&quot; : &quot;password&quot;,
         &quot;regex&quot; : &quot;^[0-9]{6}$&quot;,
         &quot;name&quot; : &quot;sms&quot;
      }
   ],
   &quot;iban&quot; : &quot;FR7613048379405300290000355&quot;,
   &quot;id&quot; : 2,
   &quot;id_account&quot; : 1,
   &quot;id_target_account&quot; : null,
   &quot;label&quot; : &quot;Papa&quot;,
   &quot;last_update&quot; : &quot;2017-04-29 16:26:20&quot;,
   &quot;time_scraped&quot; : null,
   &quot;webid&quot; : null
}
&#x60;&#x60;&#x60;
It is necessary to post on the object Recipient with the requested fields (here sms), until the add is validated:
&#x60;&#x60;&#x60;
curl \
  https://demo.biapi.pro/2.0/users/me/accounts/1/recipients/2 \
  -H &#39;Authorization: Bearer /JiDppWgbmc+5ztHIUJtHl0ynYfw682Z&#39; \
  -F sms&#x3D;&quot;123456&quot;
&#x60;&#x60;&#x60;
&#x60;&#x60;&#x60;json
{
   &quot;bank_name&quot; : &quot;BNP PARIBAS&quot;,
   &quot;bic&quot; : &quot;BNPAFRPPXXX&quot;,
   &quot;category&quot; : &quot;Famille&quot;,
   &quot;deleted&quot; : null,
   &quot;enabled_at&quot; : &quot;2017-05-01 00:00:00&quot;,
   &quot;expire&quot; : null,
   &quot;iban&quot; : &quot;FR7613048379405300290000355&quot;,
   &quot;id&quot; : 2,
   &quot;id_account&quot; : 1,
   &quot;id_target_account&quot; : null,
   &quot;label&quot; : &quot;Papa&quot;,
   &quot;last_update&quot; : &quot;2017-04-29 16:26:20&quot;,
   &quot;time_scraped&quot; : null,
   &quot;webid&quot; : &quot;2741588268268091098819849694548441184167285851255682796371&quot;
}
&#x60;&#x60;&#x60;
If the field enabled_at is in the future, it means that it isn&#39;t possible yet to execute a transfer, as the bank requires to wait a validation period.

### API Pay Webview
This section describes how to integrate the webview of the Budgea Pay API inside your application, to let your users do transfers to their recipients.

#### User redirection
To redirect the user to the webview, it is necessary to build a URI authenticated with a temporary token.
This can be done from our library, or by calling the endpoint &#x60;/auth/token/code&#x60; (see the protocol section for an example).
If the parameter **redirect_uri** is supplied, the user will be redirected to that page once the transfer is done.

#### List of pages
Here are a list a pages you may call to redirect your user directly on a page of the process:
|Path                                 |Description of the page                                                           |
|-------------------------------------|----------------------------------------------------------------------------------|
|/transfers                           |List Transfers                                                                    |
|/transfers/accounts                  |List emitter accounts                                                             |
|/transfers/accounts/id/recipients    |List recipients                                                                   |
|/transfers/accounts/id/recipients/id |Initialization of a transfer between the account and the recipient                |
|/transfers/id                        |Detail of a given transfer                                                        |

## Deprecated

This section lists all the deprecated features in Budgea API. The associated date is the date of its removal.
**Do not use them**.

### Key Investments (**2019-06-24**)

Adding a temporary new key &quot;all_investments&quot; that will include deleted investments in the **webhooks**.

### No automatic expand on User objects (**2019-07-30**)
In the API responses, by default, User objects won&#39;t display the keys &quot;config&quot;, &quot;alert_settings&quot; and &quot;invites&quot; anymore.
You will still be able to access this data by expanding the request.
Example: GET /users/me/?expand&#x3D;alert_settings,config

### Renaming of &quot;type&quot; field for jwt tokens (**2019-07-30**)
For user&#39;s tokens in the jwt format, the &quot;type&quot; field will be renamed from &quot;shared_access&quot; to &quot;sharedAccess&quot;.

    """
)
