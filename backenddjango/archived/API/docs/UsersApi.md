# CrmClientJs.UsersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**usersAuthLoginCreate**](UsersApi.md#usersAuthLoginCreate) | **POST** /api/users/auth/login/ | 
[**usersAuthRefreshCreate**](UsersApi.md#usersAuthRefreshCreate) | **POST** /api/users/auth/refresh/ | 
[**usersAuthRegisterCreate**](UsersApi.md#usersAuthRegisterCreate) | **POST** /api/users/auth/register/ | 
[**usersNotificationPreferencesRetrieve**](UsersApi.md#usersNotificationPreferencesRetrieve) | **GET** /api/users/notification-preferences/ | 
[**usersNotificationPreferencesUpdate**](UsersApi.md#usersNotificationPreferencesUpdate) | **PUT** /api/users/notification-preferences/ | 
[**usersNotificationsCountRetrieve**](UsersApi.md#usersNotificationsCountRetrieve) | **GET** /api/users/notifications/count/ | 
[**usersNotificationsList**](UsersApi.md#usersNotificationsList) | **GET** /api/users/notifications/ | 
[**usersNotificationsMarkReadCreate**](UsersApi.md#usersNotificationsMarkReadCreate) | **POST** /api/users/notifications/mark-read/ | 
[**usersNotificationsViewsetList**](UsersApi.md#usersNotificationsViewsetList) | **GET** /api/users/notifications-viewset/ | 
[**usersNotificationsViewsetMarkAllAsReadCreate**](UsersApi.md#usersNotificationsViewsetMarkAllAsReadCreate) | **POST** /api/users/notifications-viewset/mark_all_as_read/ | 
[**usersNotificationsViewsetMarkAsReadCreate**](UsersApi.md#usersNotificationsViewsetMarkAsReadCreate) | **POST** /api/users/notifications-viewset/{id}/mark_as_read/ | 
[**usersNotificationsViewsetRetrieve**](UsersApi.md#usersNotificationsViewsetRetrieve) | **GET** /api/users/notifications-viewset/{id}/ | 
[**usersNotificationsViewsetUnreadCountRetrieve**](UsersApi.md#usersNotificationsViewsetUnreadCountRetrieve) | **GET** /api/users/notifications-viewset/unread_count/ | 
[**usersProfileRetrieve**](UsersApi.md#usersProfileRetrieve) | **GET** /api/users/profile/ | 
[**usersProfileUpdatePartialUpdate**](UsersApi.md#usersProfileUpdatePartialUpdate) | **PATCH** /api/users/profile/update/ | 
[**usersProfileUpdateUpdate**](UsersApi.md#usersProfileUpdateUpdate) | **PUT** /api/users/profile/update/ | 
[**usersUsersCreate**](UsersApi.md#usersUsersCreate) | **POST** /api/users/users/ | 
[**usersUsersDestroy**](UsersApi.md#usersUsersDestroy) | **DELETE** /api/users/users/{id}/ | 
[**usersUsersList**](UsersApi.md#usersUsersList) | **GET** /api/users/users/ | 
[**usersUsersMeRetrieve**](UsersApi.md#usersUsersMeRetrieve) | **GET** /api/users/users/me/ | 
[**usersUsersPartialUpdate**](UsersApi.md#usersUsersPartialUpdate) | **PATCH** /api/users/users/{id}/ | 
[**usersUsersRetrieve**](UsersApi.md#usersUsersRetrieve) | **GET** /api/users/users/{id}/ | 
[**usersUsersUpdate**](UsersApi.md#usersUsersUpdate) | **PUT** /api/users/users/{id}/ | 



## usersAuthLoginCreate

> UsersAuthLoginCreate200Response usersAuthLoginCreate(userLoginRequest)



API endpoint for user login

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

let apiInstance = new CrmClientJs.UsersApi();
let userLoginRequest = new CrmClientJs.UserLoginRequest(); // UserLoginRequest | 
apiInstance.usersAuthLoginCreate(userLoginRequest, (error, data, response) => {
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
 **userLoginRequest** | [**UserLoginRequest**](UserLoginRequest.md)|  | 

### Return type

[**UsersAuthLoginCreate200Response**](UsersAuthLoginCreate200Response.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## usersAuthRefreshCreate

> TokenRefresh usersAuthRefreshCreate(tokenRefreshRequest)



Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.

### Example

```javascript
import CrmClientJs from 'crmClientJS';
let defaultClient = CrmClientJs.ApiClient.instance;
// Configure Bearer (JWT) access token for authorization: Bearer
let Bearer = defaultClient.authentications['Bearer'];
Bearer.accessToken = "YOUR ACCESS TOKEN"

let apiInstance = new CrmClientJs.UsersApi();
let tokenRefreshRequest = new CrmClientJs.TokenRefreshRequest(); // TokenRefreshRequest | 
apiInstance.usersAuthRefreshCreate(tokenRefreshRequest, (error, data, response) => {
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
 **tokenRefreshRequest** | [**TokenRefreshRequest**](TokenRefreshRequest.md)|  | 

### Return type

[**TokenRefresh**](TokenRefresh.md)

### Authorization

[Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## usersAuthRegisterCreate

> UserCreate usersAuthRegisterCreate(userCreateRequest)



API endpoint for user registration

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

let apiInstance = new CrmClientJs.UsersApi();
let userCreateRequest = new CrmClientJs.UserCreateRequest(); // UserCreateRequest | 
apiInstance.usersAuthRegisterCreate(userCreateRequest, (error, data, response) => {
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
 **userCreateRequest** | [**UserCreateRequest**](UserCreateRequest.md)|  | 

### Return type

[**UserCreate**](UserCreate.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## usersNotificationPreferencesRetrieve

> NotificationPreference usersNotificationPreferencesRetrieve()



Get notification preferences for the current user

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

let apiInstance = new CrmClientJs.UsersApi();
apiInstance.usersNotificationPreferencesRetrieve((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**NotificationPreference**](NotificationPreference.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## usersNotificationPreferencesUpdate

> NotificationPreference usersNotificationPreferencesUpdate(opts)



Update notification preferences for the current user

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

let apiInstance = new CrmClientJs.UsersApi();
let opts = {
  'notificationPreferenceRequest': new CrmClientJs.NotificationPreferenceRequest() // NotificationPreferenceRequest | 
};
apiInstance.usersNotificationPreferencesUpdate(opts, (error, data, response) => {
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
 **notificationPreferenceRequest** | [**NotificationPreferenceRequest**](NotificationPreferenceRequest.md)|  | [optional] 

### Return type

[**NotificationPreference**](NotificationPreference.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## usersNotificationsCountRetrieve

> NotificationList usersNotificationsCountRetrieve()



API endpoint for getting unread notification count

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

let apiInstance = new CrmClientJs.UsersApi();
apiInstance.usersNotificationsCountRetrieve((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**NotificationList**](NotificationList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## usersNotificationsList

> PaginatedNotificationListList usersNotificationsList(opts)



API endpoint for listing user notifications

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

let apiInstance = new CrmClientJs.UsersApi();
let opts = {
  'isRead': true, // Boolean | 
  'notificationType': "notificationType_example", // String | * `application_status` - Application Status Change * `repayment_upcoming` - Repayment Upcoming * `repayment_overdue` - Repayment Overdue * `note_reminder` - Note Reminder * `document_uploaded` - Document Uploaded * `signature_required` - Signature Required * `system` - System Notification
  'ordering': "ordering_example", // String | Which field to use when ordering the results.
  'page': 56 // Number | A page number within the paginated result set.
};
apiInstance.usersNotificationsList(opts, (error, data, response) => {
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
 **isRead** | **Boolean**|  | [optional] 
 **notificationType** | **String**| * &#x60;application_status&#x60; - Application Status Change * &#x60;repayment_upcoming&#x60; - Repayment Upcoming * &#x60;repayment_overdue&#x60; - Repayment Overdue * &#x60;note_reminder&#x60; - Note Reminder * &#x60;document_uploaded&#x60; - Document Uploaded * &#x60;signature_required&#x60; - Signature Required * &#x60;system&#x60; - System Notification | [optional] 
 **ordering** | **String**| Which field to use when ordering the results. | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 

### Return type

[**PaginatedNotificationListList**](PaginatedNotificationListList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## usersNotificationsMarkReadCreate

> Notification usersNotificationsMarkReadCreate(notificationRequest)



API endpoint for marking notifications as read

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

let apiInstance = new CrmClientJs.UsersApi();
let notificationRequest = new CrmClientJs.NotificationRequest(); // NotificationRequest | 
apiInstance.usersNotificationsMarkReadCreate(notificationRequest, (error, data, response) => {
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
 **notificationRequest** | [**NotificationRequest**](NotificationRequest.md)|  | 

### Return type

[**Notification**](Notification.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## usersNotificationsViewsetList

> PaginatedNotificationListList usersNotificationsViewsetList(opts)



API endpoint for managing notifications

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

let apiInstance = new CrmClientJs.UsersApi();
let opts = {
  'isRead': true, // Boolean | 
  'notificationType': "notificationType_example", // String | * `application_status` - Application Status Change * `repayment_upcoming` - Repayment Upcoming * `repayment_overdue` - Repayment Overdue * `note_reminder` - Note Reminder * `document_uploaded` - Document Uploaded * `signature_required` - Signature Required * `system` - System Notification
  'ordering': "ordering_example", // String | Which field to use when ordering the results.
  'page': 56 // Number | A page number within the paginated result set.
};
apiInstance.usersNotificationsViewsetList(opts, (error, data, response) => {
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
 **isRead** | **Boolean**|  | [optional] 
 **notificationType** | **String**| * &#x60;application_status&#x60; - Application Status Change * &#x60;repayment_upcoming&#x60; - Repayment Upcoming * &#x60;repayment_overdue&#x60; - Repayment Overdue * &#x60;note_reminder&#x60; - Note Reminder * &#x60;document_uploaded&#x60; - Document Uploaded * &#x60;signature_required&#x60; - Signature Required * &#x60;system&#x60; - System Notification | [optional] 
 **ordering** | **String**| Which field to use when ordering the results. | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 

### Return type

[**PaginatedNotificationListList**](PaginatedNotificationListList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## usersNotificationsViewsetMarkAllAsReadCreate

> Notification usersNotificationsViewsetMarkAllAsReadCreate(notificationRequest)



Mark all notifications as read

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

let apiInstance = new CrmClientJs.UsersApi();
let notificationRequest = new CrmClientJs.NotificationRequest(); // NotificationRequest | 
apiInstance.usersNotificationsViewsetMarkAllAsReadCreate(notificationRequest, (error, data, response) => {
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
 **notificationRequest** | [**NotificationRequest**](NotificationRequest.md)|  | 

### Return type

[**Notification**](Notification.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## usersNotificationsViewsetMarkAsReadCreate

> Notification usersNotificationsViewsetMarkAsReadCreate(id, notificationRequest)



Mark a notification as read

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

let apiInstance = new CrmClientJs.UsersApi();
let id = 56; // Number | 
let notificationRequest = new CrmClientJs.NotificationRequest(); // NotificationRequest | 
apiInstance.usersNotificationsViewsetMarkAsReadCreate(id, notificationRequest, (error, data, response) => {
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
 **id** | **Number**|  | 
 **notificationRequest** | [**NotificationRequest**](NotificationRequest.md)|  | 

### Return type

[**Notification**](Notification.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## usersNotificationsViewsetRetrieve

> Notification usersNotificationsViewsetRetrieve(id)



API endpoint for managing notifications

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

let apiInstance = new CrmClientJs.UsersApi();
let id = 56; // Number | 
apiInstance.usersNotificationsViewsetRetrieve(id, (error, data, response) => {
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
 **id** | **Number**|  | 

### Return type

[**Notification**](Notification.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## usersNotificationsViewsetUnreadCountRetrieve

> Notification usersNotificationsViewsetUnreadCountRetrieve()



Get count of unread notifications

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

let apiInstance = new CrmClientJs.UsersApi();
apiInstance.usersNotificationsViewsetUnreadCountRetrieve((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**Notification**](Notification.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## usersProfileRetrieve

> User usersProfileRetrieve()



API endpoint for retrieving user profile

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

let apiInstance = new CrmClientJs.UsersApi();
apiInstance.usersProfileRetrieve((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**User**](User.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## usersProfileUpdatePartialUpdate

> User usersProfileUpdatePartialUpdate(opts)



API endpoint for updating user profile

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

let apiInstance = new CrmClientJs.UsersApi();
let opts = {
  'patchedUserRequest': new CrmClientJs.PatchedUserRequest() // PatchedUserRequest | 
};
apiInstance.usersProfileUpdatePartialUpdate(opts, (error, data, response) => {
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
 **patchedUserRequest** | [**PatchedUserRequest**](PatchedUserRequest.md)|  | [optional] 

### Return type

[**User**](User.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## usersProfileUpdateUpdate

> User usersProfileUpdateUpdate(userRequest)



API endpoint for updating user profile

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

let apiInstance = new CrmClientJs.UsersApi();
let userRequest = new CrmClientJs.UserRequest(); // UserRequest | 
apiInstance.usersProfileUpdateUpdate(userRequest, (error, data, response) => {
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
 **userRequest** | [**UserRequest**](UserRequest.md)|  | 

### Return type

[**User**](User.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## usersUsersCreate

> UserCreate usersUsersCreate(userCreateRequest)



API endpoint for managing users

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

let apiInstance = new CrmClientJs.UsersApi();
let userCreateRequest = new CrmClientJs.UserCreateRequest(); // UserCreateRequest | 
apiInstance.usersUsersCreate(userCreateRequest, (error, data, response) => {
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
 **userCreateRequest** | [**UserCreateRequest**](UserCreateRequest.md)|  | 

### Return type

[**UserCreate**](UserCreate.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## usersUsersDestroy

> usersUsersDestroy(id)



API endpoint for managing users

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

let apiInstance = new CrmClientJs.UsersApi();
let id = 56; // Number | A unique integer value identifying this user.
apiInstance.usersUsersDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this user. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## usersUsersList

> PaginatedUserList usersUsersList(opts)



API endpoint for managing users

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

let apiInstance = new CrmClientJs.UsersApi();
let opts = {
  'page': 56, // Number | A page number within the paginated result set.
  'search': "search_example" // String | A search term.
};
apiInstance.usersUsersList(opts, (error, data, response) => {
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
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **search** | **String**| A search term. | [optional] 

### Return type

[**PaginatedUserList**](PaginatedUserList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## usersUsersMeRetrieve

> User usersUsersMeRetrieve()



Get current user information

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

let apiInstance = new CrmClientJs.UsersApi();
apiInstance.usersUsersMeRetrieve((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**User**](User.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## usersUsersPartialUpdate

> User usersUsersPartialUpdate(id, opts)



API endpoint for managing users

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

let apiInstance = new CrmClientJs.UsersApi();
let id = 56; // Number | A unique integer value identifying this user.
let opts = {
  'patchedUserRequest': new CrmClientJs.PatchedUserRequest() // PatchedUserRequest | 
};
apiInstance.usersUsersPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this user. | 
 **patchedUserRequest** | [**PatchedUserRequest**](PatchedUserRequest.md)|  | [optional] 

### Return type

[**User**](User.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## usersUsersRetrieve

> User usersUsersRetrieve(id)



API endpoint for managing users

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

let apiInstance = new CrmClientJs.UsersApi();
let id = 56; // Number | A unique integer value identifying this user.
apiInstance.usersUsersRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this user. | 

### Return type

[**User**](User.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## usersUsersUpdate

> User usersUsersUpdate(id, userRequest)



API endpoint for managing users

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

let apiInstance = new CrmClientJs.UsersApi();
let id = 56; // Number | A unique integer value identifying this user.
let userRequest = new CrmClientJs.UserRequest(); // UserRequest | 
apiInstance.usersUsersUpdate(id, userRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this user. | 
 **userRequest** | [**UserRequest**](UserRequest.md)|  | 

### Return type

[**User**](User.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json

