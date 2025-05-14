# CrmClientJs.RemindersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**remindersCreate**](RemindersApi.md#remindersCreate) | **POST** /api/reminders/ | 
[**remindersDestroy**](RemindersApi.md#remindersDestroy) | **DELETE** /api/reminders/{id}/ | 
[**remindersList**](RemindersApi.md#remindersList) | **GET** /api/reminders/ | 
[**remindersPartialUpdate**](RemindersApi.md#remindersPartialUpdate) | **PATCH** /api/reminders/{id}/ | 
[**remindersRetrieve**](RemindersApi.md#remindersRetrieve) | **GET** /api/reminders/{id}/ | 
[**remindersUpdate**](RemindersApi.md#remindersUpdate) | **PUT** /api/reminders/{id}/ | 



## remindersCreate

> Reminder remindersCreate(reminderRequest)



API endpoint for managing reminders

### Example

```javascript
import CrmClientJs from 'crmClientJS';
let defaultClient = CrmClientJs.ApiClient.instance;
// Configure Bearer (JWT) access token for authorization: jwtAuth
let jwtAuth = defaultClient.authentications['jwtAuth'];
jwtAuth.accessToken = "YOUR ACCESS TOKEN"
// Configure Bearer (JWT) access token for authorization: Bearer
let Bearer = defaultClient.authentications['Bearer'];
Bearer.accessToken = "YOUR ACCESS TOKEN"

let apiInstance = new CrmClientJs.RemindersApi();
let reminderRequest = new CrmClientJs.ReminderRequest(); // ReminderRequest | 
apiInstance.remindersCreate(reminderRequest, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **reminderRequest** | [**ReminderRequest**](ReminderRequest.md)|  | 

### Return type

[**Reminder**](Reminder.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## remindersDestroy

> remindersDestroy(id)



API endpoint for managing reminders

### Example

```javascript
import CrmClientJs from 'crmClientJS';
let defaultClient = CrmClientJs.ApiClient.instance;
// Configure Bearer (JWT) access token for authorization: jwtAuth
let jwtAuth = defaultClient.authentications['jwtAuth'];
jwtAuth.accessToken = "YOUR ACCESS TOKEN"
// Configure Bearer (JWT) access token for authorization: Bearer
let Bearer = defaultClient.authentications['Bearer'];
Bearer.accessToken = "YOUR ACCESS TOKEN"

let apiInstance = new CrmClientJs.RemindersApi();
let id = 56; // Number | A unique integer value identifying this reminder.
apiInstance.remindersDestroy(id, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| A unique integer value identifying this reminder. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## remindersList

> PaginatedReminderList remindersList(opts)



API endpoint for managing reminders

### Example

```javascript
import CrmClientJs from 'crmClientJS';
let defaultClient = CrmClientJs.ApiClient.instance;
// Configure Bearer (JWT) access token for authorization: jwtAuth
let jwtAuth = defaultClient.authentications['jwtAuth'];
jwtAuth.accessToken = "YOUR ACCESS TOKEN"
// Configure Bearer (JWT) access token for authorization: Bearer
let Bearer = defaultClient.authentications['Bearer'];
Bearer.accessToken = "YOUR ACCESS TOKEN"

let apiInstance = new CrmClientJs.RemindersApi();
let opts = {
  'isSent': true, // Boolean | 
  'page': 56, // Number | A page number within the paginated result set.
  'recipientType': "recipientType_example", // String | * `client` - Client * `bdm` - Business Development Manager * `broker` - Broker * `custom` - Custom Email
  'relatedApplication': 56, // Number | 
  'relatedBorrower': 56, // Number | 
  'search': "search_example" // String | A search term.
};
apiInstance.remindersList(opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **isSent** | **Boolean**|  | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **recipientType** | **String**| * &#x60;client&#x60; - Client * &#x60;bdm&#x60; - Business Development Manager * &#x60;broker&#x60; - Broker * &#x60;custom&#x60; - Custom Email | [optional] 
 **relatedApplication** | **Number**|  | [optional] 
 **relatedBorrower** | **Number**|  | [optional] 
 **search** | **String**| A search term. | [optional] 

### Return type

[**PaginatedReminderList**](PaginatedReminderList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## remindersPartialUpdate

> Reminder remindersPartialUpdate(id, opts)



API endpoint for managing reminders

### Example

```javascript
import CrmClientJs from 'crmClientJS';
let defaultClient = CrmClientJs.ApiClient.instance;
// Configure Bearer (JWT) access token for authorization: jwtAuth
let jwtAuth = defaultClient.authentications['jwtAuth'];
jwtAuth.accessToken = "YOUR ACCESS TOKEN"
// Configure Bearer (JWT) access token for authorization: Bearer
let Bearer = defaultClient.authentications['Bearer'];
Bearer.accessToken = "YOUR ACCESS TOKEN"

let apiInstance = new CrmClientJs.RemindersApi();
let id = 56; // Number | A unique integer value identifying this reminder.
let opts = {
  'patchedReminderRequest': new CrmClientJs.PatchedReminderRequest() // PatchedReminderRequest | 
};
apiInstance.remindersPartialUpdate(id, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| A unique integer value identifying this reminder. | 
 **patchedReminderRequest** | [**PatchedReminderRequest**](PatchedReminderRequest.md)|  | [optional] 

### Return type

[**Reminder**](Reminder.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## remindersRetrieve

> Reminder remindersRetrieve(id)



API endpoint for managing reminders

### Example

```javascript
import CrmClientJs from 'crmClientJS';
let defaultClient = CrmClientJs.ApiClient.instance;
// Configure Bearer (JWT) access token for authorization: jwtAuth
let jwtAuth = defaultClient.authentications['jwtAuth'];
jwtAuth.accessToken = "YOUR ACCESS TOKEN"
// Configure Bearer (JWT) access token for authorization: Bearer
let Bearer = defaultClient.authentications['Bearer'];
Bearer.accessToken = "YOUR ACCESS TOKEN"

let apiInstance = new CrmClientJs.RemindersApi();
let id = 56; // Number | A unique integer value identifying this reminder.
apiInstance.remindersRetrieve(id, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| A unique integer value identifying this reminder. | 

### Return type

[**Reminder**](Reminder.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## remindersUpdate

> Reminder remindersUpdate(id, reminderRequest)



API endpoint for managing reminders

### Example

```javascript
import CrmClientJs from 'crmClientJS';
let defaultClient = CrmClientJs.ApiClient.instance;
// Configure Bearer (JWT) access token for authorization: jwtAuth
let jwtAuth = defaultClient.authentications['jwtAuth'];
jwtAuth.accessToken = "YOUR ACCESS TOKEN"
// Configure Bearer (JWT) access token for authorization: Bearer
let Bearer = defaultClient.authentications['Bearer'];
Bearer.accessToken = "YOUR ACCESS TOKEN"

let apiInstance = new CrmClientJs.RemindersApi();
let id = 56; // Number | A unique integer value identifying this reminder.
let reminderRequest = new CrmClientJs.ReminderRequest(); // ReminderRequest | 
apiInstance.remindersUpdate(id, reminderRequest, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **Number**| A unique integer value identifying this reminder. | 
 **reminderRequest** | [**ReminderRequest**](ReminderRequest.md)|  | 

### Return type

[**Reminder**](Reminder.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json

