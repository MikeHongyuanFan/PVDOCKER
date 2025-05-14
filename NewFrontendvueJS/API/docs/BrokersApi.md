# CrmClientJs.BrokersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**brokersApplicationsRetrieve**](BrokersApi.md#brokersApplicationsRetrieve) | **GET** /api/brokers/{id}/applications/ | 
[**brokersBdmsApplicationsRetrieve**](BrokersApi.md#brokersBdmsApplicationsRetrieve) | **GET** /api/brokers/bdms/{id}/applications/ | 
[**brokersBdmsCreate**](BrokersApi.md#brokersBdmsCreate) | **POST** /api/brokers/bdms/ | 
[**brokersBdmsDestroy**](BrokersApi.md#brokersBdmsDestroy) | **DELETE** /api/brokers/bdms/{id}/ | 
[**brokersBdmsList**](BrokersApi.md#brokersBdmsList) | **GET** /api/brokers/bdms/ | 
[**brokersBdmsPartialUpdate**](BrokersApi.md#brokersBdmsPartialUpdate) | **PATCH** /api/brokers/bdms/{id}/ | 
[**brokersBdmsRetrieve**](BrokersApi.md#brokersBdmsRetrieve) | **GET** /api/brokers/bdms/{id}/ | 
[**brokersBdmsUpdate**](BrokersApi.md#brokersBdmsUpdate) | **PUT** /api/brokers/bdms/{id}/ | 
[**brokersBranchesBdmsRetrieve**](BrokersApi.md#brokersBranchesBdmsRetrieve) | **GET** /api/brokers/branches/{id}/bdms/ | 
[**brokersBranchesBrokersRetrieve**](BrokersApi.md#brokersBranchesBrokersRetrieve) | **GET** /api/brokers/branches/{id}/brokers/ | 
[**brokersBranchesCreate**](BrokersApi.md#brokersBranchesCreate) | **POST** /api/brokers/branches/ | 
[**brokersBranchesDestroy**](BrokersApi.md#brokersBranchesDestroy) | **DELETE** /api/brokers/branches/{id}/ | 
[**brokersBranchesList**](BrokersApi.md#brokersBranchesList) | **GET** /api/brokers/branches/ | 
[**brokersBranchesPartialUpdate**](BrokersApi.md#brokersBranchesPartialUpdate) | **PATCH** /api/brokers/branches/{id}/ | 
[**brokersBranchesRetrieve**](BrokersApi.md#brokersBranchesRetrieve) | **GET** /api/brokers/branches/{id}/ | 
[**brokersBranchesUpdate**](BrokersApi.md#brokersBranchesUpdate) | **PUT** /api/brokers/branches/{id}/ | 
[**brokersCreate**](BrokersApi.md#brokersCreate) | **POST** /api/brokers/ | 
[**brokersDestroy**](BrokersApi.md#brokersDestroy) | **DELETE** /api/brokers/{id}/ | 
[**brokersList**](BrokersApi.md#brokersList) | **GET** /api/brokers/ | 
[**brokersPartialUpdate**](BrokersApi.md#brokersPartialUpdate) | **PATCH** /api/brokers/{id}/ | 
[**brokersRetrieve**](BrokersApi.md#brokersRetrieve) | **GET** /api/brokers/{id}/ | 
[**brokersStatsRetrieve**](BrokersApi.md#brokersStatsRetrieve) | **GET** /api/brokers/{id}/stats/ | 
[**brokersUpdate**](BrokersApi.md#brokersUpdate) | **PUT** /api/brokers/{id}/ | 



## brokersApplicationsRetrieve

> BrokerDetail brokersApplicationsRetrieve(id)



Get all applications for a broker

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this broker.
apiInstance.brokersApplicationsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this broker. | 

### Return type

[**BrokerDetail**](BrokerDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## brokersBdmsApplicationsRetrieve

> BDM brokersBdmsApplicationsRetrieve(id)



Get all applications for a BDM

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this BDM.
apiInstance.brokersBdmsApplicationsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this BDM. | 

### Return type

[**BDM**](BDM.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## brokersBdmsCreate

> BDM brokersBdmsCreate(bDMRequest)



API endpoint for managing BDMs

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

let apiInstance = new CrmClientJs.BrokersApi();
let bDMRequest = new CrmClientJs.BDMRequest(); // BDMRequest | 
apiInstance.brokersBdmsCreate(bDMRequest, (error, data, response) => {
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
 **bDMRequest** | [**BDMRequest**](BDMRequest.md)|  | 

### Return type

[**BDM**](BDM.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## brokersBdmsDestroy

> brokersBdmsDestroy(id)



API endpoint for managing BDMs

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this BDM.
apiInstance.brokersBdmsDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this BDM. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## brokersBdmsList

> PaginatedBDMList brokersBdmsList(opts)



API endpoint for managing BDMs

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

let apiInstance = new CrmClientJs.BrokersApi();
let opts = {
  'branch': 56, // Number | 
  'page': 56, // Number | A page number within the paginated result set.
  'search': "search_example" // String | A search term.
};
apiInstance.brokersBdmsList(opts, (error, data, response) => {
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
 **branch** | **Number**|  | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **search** | **String**| A search term. | [optional] 

### Return type

[**PaginatedBDMList**](PaginatedBDMList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## brokersBdmsPartialUpdate

> BDM brokersBdmsPartialUpdate(id, opts)



API endpoint for managing BDMs

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this BDM.
let opts = {
  'patchedBDMRequest': new CrmClientJs.PatchedBDMRequest() // PatchedBDMRequest | 
};
apiInstance.brokersBdmsPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this BDM. | 
 **patchedBDMRequest** | [**PatchedBDMRequest**](PatchedBDMRequest.md)|  | [optional] 

### Return type

[**BDM**](BDM.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## brokersBdmsRetrieve

> BDM brokersBdmsRetrieve(id)



API endpoint for managing BDMs

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this BDM.
apiInstance.brokersBdmsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this BDM. | 

### Return type

[**BDM**](BDM.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## brokersBdmsUpdate

> BDM brokersBdmsUpdate(id, bDMRequest)



API endpoint for managing BDMs

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this BDM.
let bDMRequest = new CrmClientJs.BDMRequest(); // BDMRequest | 
apiInstance.brokersBdmsUpdate(id, bDMRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this BDM. | 
 **bDMRequest** | [**BDMRequest**](BDMRequest.md)|  | 

### Return type

[**BDM**](BDM.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## brokersBranchesBdmsRetrieve

> Branch brokersBranchesBdmsRetrieve(id)



Get all BDMs for a branch

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this branch.
apiInstance.brokersBranchesBdmsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this branch. | 

### Return type

[**Branch**](Branch.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## brokersBranchesBrokersRetrieve

> Branch brokersBranchesBrokersRetrieve(id)



Get all brokers for a branch

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this branch.
apiInstance.brokersBranchesBrokersRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this branch. | 

### Return type

[**Branch**](Branch.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## brokersBranchesCreate

> Branch brokersBranchesCreate(branchRequest)



API endpoint for managing branches

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

let apiInstance = new CrmClientJs.BrokersApi();
let branchRequest = new CrmClientJs.BranchRequest(); // BranchRequest | 
apiInstance.brokersBranchesCreate(branchRequest, (error, data, response) => {
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
 **branchRequest** | [**BranchRequest**](BranchRequest.md)|  | 

### Return type

[**Branch**](Branch.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## brokersBranchesDestroy

> brokersBranchesDestroy(id)



API endpoint for managing branches

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this branch.
apiInstance.brokersBranchesDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this branch. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## brokersBranchesList

> PaginatedBranchList brokersBranchesList(opts)



API endpoint for managing branches

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

let apiInstance = new CrmClientJs.BrokersApi();
let opts = {
  'page': 56, // Number | A page number within the paginated result set.
  'search': "search_example" // String | A search term.
};
apiInstance.brokersBranchesList(opts, (error, data, response) => {
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

[**PaginatedBranchList**](PaginatedBranchList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## brokersBranchesPartialUpdate

> Branch brokersBranchesPartialUpdate(id, opts)



API endpoint for managing branches

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this branch.
let opts = {
  'patchedBranchRequest': new CrmClientJs.PatchedBranchRequest() // PatchedBranchRequest | 
};
apiInstance.brokersBranchesPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this branch. | 
 **patchedBranchRequest** | [**PatchedBranchRequest**](PatchedBranchRequest.md)|  | [optional] 

### Return type

[**Branch**](Branch.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## brokersBranchesRetrieve

> Branch brokersBranchesRetrieve(id)



API endpoint for managing branches

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this branch.
apiInstance.brokersBranchesRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this branch. | 

### Return type

[**Branch**](Branch.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## brokersBranchesUpdate

> Branch brokersBranchesUpdate(id, branchRequest)



API endpoint for managing branches

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this branch.
let branchRequest = new CrmClientJs.BranchRequest(); // BranchRequest | 
apiInstance.brokersBranchesUpdate(id, branchRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this branch. | 
 **branchRequest** | [**BranchRequest**](BranchRequest.md)|  | 

### Return type

[**Branch**](Branch.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## brokersCreate

> BrokerDetail brokersCreate(brokerDetailRequest)



API endpoint for managing brokers

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

let apiInstance = new CrmClientJs.BrokersApi();
let brokerDetailRequest = new CrmClientJs.BrokerDetailRequest(); // BrokerDetailRequest | 
apiInstance.brokersCreate(brokerDetailRequest, (error, data, response) => {
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
 **brokerDetailRequest** | [**BrokerDetailRequest**](BrokerDetailRequest.md)|  | 

### Return type

[**BrokerDetail**](BrokerDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## brokersDestroy

> brokersDestroy(id)



API endpoint for managing brokers

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this broker.
apiInstance.brokersDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this broker. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## brokersList

> PaginatedBrokerListList brokersList(opts)



API endpoint for managing brokers

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

let apiInstance = new CrmClientJs.BrokersApi();
let opts = {
  'branch': 56, // Number | 
  'minApplications': 3.4, // Number | 
  'ordering': "ordering_example", // String | Which field to use when ordering the results.
  'page': 56, // Number | A page number within the paginated result set.
  'search': "search_example" // String | A search term.
};
apiInstance.brokersList(opts, (error, data, response) => {
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
 **branch** | **Number**|  | [optional] 
 **minApplications** | **Number**|  | [optional] 
 **ordering** | **String**| Which field to use when ordering the results. | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **search** | **String**| A search term. | [optional] 

### Return type

[**PaginatedBrokerListList**](PaginatedBrokerListList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## brokersPartialUpdate

> BrokerDetail brokersPartialUpdate(id, opts)



API endpoint for managing brokers

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this broker.
let opts = {
  'patchedBrokerDetailRequest': new CrmClientJs.PatchedBrokerDetailRequest() // PatchedBrokerDetailRequest | 
};
apiInstance.brokersPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this broker. | 
 **patchedBrokerDetailRequest** | [**PatchedBrokerDetailRequest**](PatchedBrokerDetailRequest.md)|  | [optional] 

### Return type

[**BrokerDetail**](BrokerDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## brokersRetrieve

> BrokerDetail brokersRetrieve(id)



API endpoint for managing brokers

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this broker.
apiInstance.brokersRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this broker. | 

### Return type

[**BrokerDetail**](BrokerDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## brokersStatsRetrieve

> BrokerDetail brokersStatsRetrieve(id)



Get statistics for a broker

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this broker.
apiInstance.brokersStatsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this broker. | 

### Return type

[**BrokerDetail**](BrokerDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## brokersUpdate

> BrokerDetail brokersUpdate(id, brokerDetailRequest)



API endpoint for managing brokers

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

let apiInstance = new CrmClientJs.BrokersApi();
let id = 56; // Number | A unique integer value identifying this broker.
let brokerDetailRequest = new CrmClientJs.BrokerDetailRequest(); // BrokerDetailRequest | 
apiInstance.brokersUpdate(id, brokerDetailRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this broker. | 
 **brokerDetailRequest** | [**BrokerDetailRequest**](BrokerDetailRequest.md)|  | 

### Return type

[**BrokerDetail**](BrokerDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json

