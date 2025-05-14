# CrmClientJs.BorrowersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**borrowerGuarantorDetail**](BorrowersApi.md#borrowerGuarantorDetail) | **GET** /api/borrowers/guarantors/{id}/ | 
[**borrowersApplicationsRetrieve**](BorrowersApi.md#borrowersApplicationsRetrieve) | **GET** /api/borrowers/{id}/applications/ | 
[**borrowersCompanyList**](BorrowersApi.md#borrowersCompanyList) | **GET** /api/borrowers/company/ | 
[**borrowersCreate**](BorrowersApi.md#borrowersCreate) | **POST** /api/borrowers/ | 
[**borrowersDestroy**](BorrowersApi.md#borrowersDestroy) | **DELETE** /api/borrowers/{id}/ | 
[**borrowersFinancialSummaryRetrieve**](BorrowersApi.md#borrowersFinancialSummaryRetrieve) | **GET** /api/borrowers/{id}/financial-summary/ | 
[**borrowersGuarantorsByBorrowerId**](BorrowersApi.md#borrowersGuarantorsByBorrowerId) | **GET** /api/borrowers/{id}/guarantors/ | 
[**borrowersGuarantorsCreate**](BorrowersApi.md#borrowersGuarantorsCreate) | **POST** /api/borrowers/guarantors/ | 
[**borrowersGuarantorsDestroy**](BorrowersApi.md#borrowersGuarantorsDestroy) | **DELETE** /api/borrowers/guarantors/{id}/ | 
[**borrowersGuarantorsGuaranteedApplicationsRetrieve**](BorrowersApi.md#borrowersGuarantorsGuaranteedApplicationsRetrieve) | **GET** /api/borrowers/guarantors/{id}/guaranteed_applications/ | 
[**borrowersGuarantorsList**](BorrowersApi.md#borrowersGuarantorsList) | **GET** /api/borrowers/guarantors/ | 
[**borrowersGuarantorsPartialUpdate**](BorrowersApi.md#borrowersGuarantorsPartialUpdate) | **PATCH** /api/borrowers/guarantors/{id}/ | 
[**borrowersGuarantorsUpdate**](BorrowersApi.md#borrowersGuarantorsUpdate) | **PUT** /api/borrowers/guarantors/{id}/ | 
[**borrowersList**](BorrowersApi.md#borrowersList) | **GET** /api/borrowers/ | 
[**borrowersPartialUpdate**](BorrowersApi.md#borrowersPartialUpdate) | **PATCH** /api/borrowers/{id}/ | 
[**borrowersRetrieve**](BorrowersApi.md#borrowersRetrieve) | **GET** /api/borrowers/{id}/ | 
[**borrowersUpdate**](BorrowersApi.md#borrowersUpdate) | **PUT** /api/borrowers/{id}/ | 



## borrowerGuarantorDetail

> BorrowerGuarantor borrowerGuarantorDetail(id)



API endpoint for managing guarantors

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

let apiInstance = new CrmClientJs.BorrowersApi();
let id = 56; // Number | A unique integer value identifying this guarantor.
apiInstance.borrowerGuarantorDetail(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this guarantor. | 

### Return type

[**BorrowerGuarantor**](BorrowerGuarantor.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## borrowersApplicationsRetrieve

> BorrowerDetail borrowersApplicationsRetrieve(id)



Get all applications for a borrower

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

let apiInstance = new CrmClientJs.BorrowersApi();
let id = 56; // Number | A unique integer value identifying this borrower.
apiInstance.borrowersApplicationsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this borrower. | 

### Return type

[**BorrowerDetail**](BorrowerDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## borrowersCompanyList

> PaginatedBorrowerListList borrowersCompanyList(opts)



View for listing company borrowers

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

let apiInstance = new CrmClientJs.BorrowersApi();
let opts = {
  'page': 56 // Number | A page number within the paginated result set.
};
apiInstance.borrowersCompanyList(opts, (error, data, response) => {
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

### Return type

[**PaginatedBorrowerListList**](PaginatedBorrowerListList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## borrowersCreate

> BorrowerDetail borrowersCreate(opts)



API endpoint for managing borrowers

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

let apiInstance = new CrmClientJs.BorrowersApi();
let opts = {
  'borrowerDetailRequest': new CrmClientJs.BorrowerDetailRequest() // BorrowerDetailRequest | 
};
apiInstance.borrowersCreate(opts, (error, data, response) => {
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
 **borrowerDetailRequest** | [**BorrowerDetailRequest**](BorrowerDetailRequest.md)|  | [optional] 

### Return type

[**BorrowerDetail**](BorrowerDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## borrowersDestroy

> borrowersDestroy(id)



API endpoint for managing borrowers

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

let apiInstance = new CrmClientJs.BorrowersApi();
let id = 56; // Number | A unique integer value identifying this borrower.
apiInstance.borrowersDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this borrower. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## borrowersFinancialSummaryRetrieve

> BorrowerFinancialSummary borrowersFinancialSummaryRetrieve(id)



Get a financial summary for a borrower

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

let apiInstance = new CrmClientJs.BorrowersApi();
let id = 56; // Number | 
apiInstance.borrowersFinancialSummaryRetrieve(id, (error, data, response) => {
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

[**BorrowerFinancialSummary**](BorrowerFinancialSummary.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## borrowersGuarantorsByBorrowerId

> BorrowerDetail borrowersGuarantorsByBorrowerId(id)



Get all guarantors for a borrower

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

let apiInstance = new CrmClientJs.BorrowersApi();
let id = 56; // Number | A unique integer value identifying this borrower.
apiInstance.borrowersGuarantorsByBorrowerId(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this borrower. | 

### Return type

[**BorrowerDetail**](BorrowerDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## borrowersGuarantorsCreate

> BorrowerGuarantor borrowersGuarantorsCreate(opts)



API endpoint for managing guarantors

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

let apiInstance = new CrmClientJs.BorrowersApi();
let opts = {
  'borrowerGuarantorRequest': new CrmClientJs.BorrowerGuarantorRequest() // BorrowerGuarantorRequest | 
};
apiInstance.borrowersGuarantorsCreate(opts, (error, data, response) => {
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
 **borrowerGuarantorRequest** | [**BorrowerGuarantorRequest**](BorrowerGuarantorRequest.md)|  | [optional] 

### Return type

[**BorrowerGuarantor**](BorrowerGuarantor.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## borrowersGuarantorsDestroy

> borrowersGuarantorsDestroy(id)



API endpoint for managing guarantors

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

let apiInstance = new CrmClientJs.BorrowersApi();
let id = 56; // Number | A unique integer value identifying this guarantor.
apiInstance.borrowersGuarantorsDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this guarantor. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## borrowersGuarantorsGuaranteedApplicationsRetrieve

> BorrowerGuarantor borrowersGuarantorsGuaranteedApplicationsRetrieve(id)



Get all applications guaranteed by a guarantor

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

let apiInstance = new CrmClientJs.BorrowersApi();
let id = 56; // Number | A unique integer value identifying this guarantor.
apiInstance.borrowersGuarantorsGuaranteedApplicationsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this guarantor. | 

### Return type

[**BorrowerGuarantor**](BorrowerGuarantor.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## borrowersGuarantorsList

> PaginatedBorrowerGuarantorList borrowersGuarantorsList(opts)



API endpoint for managing guarantors

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

let apiInstance = new CrmClientJs.BorrowersApi();
let opts = {
  'application': 56, // Number | 
  'borrower': 56, // Number | 
  'guarantorType': "guarantorType_example", // String | * `individual` - Individual * `company` - Company
  'page': 56, // Number | A page number within the paginated result set.
  'search': "search_example" // String | A search term.
};
apiInstance.borrowersGuarantorsList(opts, (error, data, response) => {
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
 **application** | **Number**|  | [optional] 
 **borrower** | **Number**|  | [optional] 
 **guarantorType** | **String**| * &#x60;individual&#x60; - Individual * &#x60;company&#x60; - Company | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **search** | **String**| A search term. | [optional] 

### Return type

[**PaginatedBorrowerGuarantorList**](PaginatedBorrowerGuarantorList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## borrowersGuarantorsPartialUpdate

> BorrowerGuarantor borrowersGuarantorsPartialUpdate(id, opts)



API endpoint for managing guarantors

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

let apiInstance = new CrmClientJs.BorrowersApi();
let id = 56; // Number | A unique integer value identifying this guarantor.
let opts = {
  'patchedBorrowerGuarantorRequest': new CrmClientJs.PatchedBorrowerGuarantorRequest() // PatchedBorrowerGuarantorRequest | 
};
apiInstance.borrowersGuarantorsPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this guarantor. | 
 **patchedBorrowerGuarantorRequest** | [**PatchedBorrowerGuarantorRequest**](PatchedBorrowerGuarantorRequest.md)|  | [optional] 

### Return type

[**BorrowerGuarantor**](BorrowerGuarantor.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## borrowersGuarantorsUpdate

> BorrowerGuarantor borrowersGuarantorsUpdate(id, opts)



API endpoint for managing guarantors

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

let apiInstance = new CrmClientJs.BorrowersApi();
let id = 56; // Number | A unique integer value identifying this guarantor.
let opts = {
  'borrowerGuarantorRequest': new CrmClientJs.BorrowerGuarantorRequest() // BorrowerGuarantorRequest | 
};
apiInstance.borrowersGuarantorsUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this guarantor. | 
 **borrowerGuarantorRequest** | [**BorrowerGuarantorRequest**](BorrowerGuarantorRequest.md)|  | [optional] 

### Return type

[**BorrowerGuarantor**](BorrowerGuarantor.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## borrowersList

> PaginatedBorrowerListList borrowersList(opts)



API endpoint for managing borrowers

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

let apiInstance = new CrmClientJs.BorrowersApi();
let opts = {
  'hasApplications': true, // Boolean | 
  'maritalStatus': "maritalStatus_example", // String | * `single` - Single * `married` - Married * `de_facto` - De Facto * `divorced` - Divorced * `widowed` - Widowed
  'ordering': "ordering_example", // String | Which field to use when ordering the results.
  'page': 56, // Number | A page number within the paginated result set.
  'residencyStatus': "residencyStatus_example", // String | * `citizen` - Citizen * `permanent_resident` - Permanent Resident * `temporary_resident` - Temporary Resident * `foreign_investor` - Foreign Investor
  'search': "search_example" // String | A search term.
};
apiInstance.borrowersList(opts, (error, data, response) => {
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
 **hasApplications** | **Boolean**|  | [optional] 
 **maritalStatus** | **String**| * &#x60;single&#x60; - Single * &#x60;married&#x60; - Married * &#x60;de_facto&#x60; - De Facto * &#x60;divorced&#x60; - Divorced * &#x60;widowed&#x60; - Widowed | [optional] 
 **ordering** | **String**| Which field to use when ordering the results. | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **residencyStatus** | **String**| * &#x60;citizen&#x60; - Citizen * &#x60;permanent_resident&#x60; - Permanent Resident * &#x60;temporary_resident&#x60; - Temporary Resident * &#x60;foreign_investor&#x60; - Foreign Investor | [optional] 
 **search** | **String**| A search term. | [optional] 

### Return type

[**PaginatedBorrowerListList**](PaginatedBorrowerListList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## borrowersPartialUpdate

> BorrowerDetail borrowersPartialUpdate(id, opts)



API endpoint for managing borrowers

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

let apiInstance = new CrmClientJs.BorrowersApi();
let id = 56; // Number | A unique integer value identifying this borrower.
let opts = {
  'patchedBorrowerDetailRequest': new CrmClientJs.PatchedBorrowerDetailRequest() // PatchedBorrowerDetailRequest | 
};
apiInstance.borrowersPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this borrower. | 
 **patchedBorrowerDetailRequest** | [**PatchedBorrowerDetailRequest**](PatchedBorrowerDetailRequest.md)|  | [optional] 

### Return type

[**BorrowerDetail**](BorrowerDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## borrowersRetrieve

> BorrowerDetail borrowersRetrieve(id)



API endpoint for managing borrowers

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

let apiInstance = new CrmClientJs.BorrowersApi();
let id = 56; // Number | A unique integer value identifying this borrower.
apiInstance.borrowersRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this borrower. | 

### Return type

[**BorrowerDetail**](BorrowerDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## borrowersUpdate

> BorrowerDetail borrowersUpdate(id, opts)



API endpoint for managing borrowers

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

let apiInstance = new CrmClientJs.BorrowersApi();
let id = 56; // Number | A unique integer value identifying this borrower.
let opts = {
  'borrowerDetailRequest': new CrmClientJs.BorrowerDetailRequest() // BorrowerDetailRequest | 
};
apiInstance.borrowersUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this borrower. | 
 **borrowerDetailRequest** | [**BorrowerDetailRequest**](BorrowerDetailRequest.md)|  | [optional] 

### Return type

[**BorrowerDetail**](BorrowerDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json

