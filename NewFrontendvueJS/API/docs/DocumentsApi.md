# CrmClientJs.DocumentsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**documentsApplicationsLedgerRetrieve**](DocumentsApi.md#documentsApplicationsLedgerRetrieve) | **GET** /api/documents/applications/{application_id}/ledger/ | 
[**documentsDocumentsCreate**](DocumentsApi.md#documentsDocumentsCreate) | **POST** /api/documents/documents/ | 
[**documentsDocumentsCreateVersionCreate**](DocumentsApi.md#documentsDocumentsCreateVersionCreate) | **POST** /api/documents/documents/{id}/create-version/ | 
[**documentsDocumentsDestroy**](DocumentsApi.md#documentsDocumentsDestroy) | **DELETE** /api/documents/documents/{id}/ | 
[**documentsDocumentsDownloadRetrieve**](DocumentsApi.md#documentsDocumentsDownloadRetrieve) | **GET** /api/documents/documents/{id}/download/ | 
[**documentsDocumentsList**](DocumentsApi.md#documentsDocumentsList) | **GET** /api/documents/documents/ | 
[**documentsDocumentsPartialUpdate**](DocumentsApi.md#documentsDocumentsPartialUpdate) | **PATCH** /api/documents/documents/{id}/ | 
[**documentsDocumentsRetrieve**](DocumentsApi.md#documentsDocumentsRetrieve) | **GET** /api/documents/documents/{id}/ | 
[**documentsDocumentsUpdate**](DocumentsApi.md#documentsDocumentsUpdate) | **PUT** /api/documents/documents/{id}/ | 
[**documentsFeesCreate**](DocumentsApi.md#documentsFeesCreate) | **POST** /api/documents/fees/ | 
[**documentsFeesDestroy**](DocumentsApi.md#documentsFeesDestroy) | **DELETE** /api/documents/fees/{id}/ | 
[**documentsFeesList**](DocumentsApi.md#documentsFeesList) | **GET** /api/documents/fees/ | 
[**documentsFeesMarkPaidCreate**](DocumentsApi.md#documentsFeesMarkPaidCreate) | **POST** /api/documents/fees/{id}/mark-paid/ | 
[**documentsFeesPartialUpdate**](DocumentsApi.md#documentsFeesPartialUpdate) | **PATCH** /api/documents/fees/{id}/ | 
[**documentsFeesRetrieve**](DocumentsApi.md#documentsFeesRetrieve) | **GET** /api/documents/fees/{id}/ | 
[**documentsFeesUpdate**](DocumentsApi.md#documentsFeesUpdate) | **PUT** /api/documents/fees/{id}/ | 
[**documentsNoteCommentsCreate**](DocumentsApi.md#documentsNoteCommentsCreate) | **POST** /api/documents/note-comments/ | 
[**documentsNoteCommentsDestroy**](DocumentsApi.md#documentsNoteCommentsDestroy) | **DELETE** /api/documents/note-comments/{id}/ | 
[**documentsNoteCommentsList**](DocumentsApi.md#documentsNoteCommentsList) | **GET** /api/documents/note-comments/ | 
[**documentsNoteCommentsPartialUpdate**](DocumentsApi.md#documentsNoteCommentsPartialUpdate) | **PATCH** /api/documents/note-comments/{id}/ | 
[**documentsNoteCommentsRetrieve**](DocumentsApi.md#documentsNoteCommentsRetrieve) | **GET** /api/documents/note-comments/{id}/ | 
[**documentsNoteCommentsUpdate**](DocumentsApi.md#documentsNoteCommentsUpdate) | **PUT** /api/documents/note-comments/{id}/ | 
[**documentsNotesAddCommentCreate**](DocumentsApi.md#documentsNotesAddCommentCreate) | **POST** /api/documents/notes/{id}/add_comment/ | 
[**documentsNotesCommentsRetrieve**](DocumentsApi.md#documentsNotesCommentsRetrieve) | **GET** /api/documents/notes/{id}/comments/ | 
[**documentsNotesCreate**](DocumentsApi.md#documentsNotesCreate) | **POST** /api/documents/notes/ | 
[**documentsNotesDestroy**](DocumentsApi.md#documentsNotesDestroy) | **DELETE** /api/documents/notes/{id}/ | 
[**documentsNotesList**](DocumentsApi.md#documentsNotesList) | **GET** /api/documents/notes/ | 
[**documentsNotesPartialUpdate**](DocumentsApi.md#documentsNotesPartialUpdate) | **PATCH** /api/documents/notes/{id}/ | 
[**documentsNotesRetrieve**](DocumentsApi.md#documentsNotesRetrieve) | **GET** /api/documents/notes/{id}/ | 
[**documentsNotesUpdate**](DocumentsApi.md#documentsNotesUpdate) | **PUT** /api/documents/notes/{id}/ | 
[**documentsRepaymentsCreate**](DocumentsApi.md#documentsRepaymentsCreate) | **POST** /api/documents/repayments/ | 
[**documentsRepaymentsDestroy**](DocumentsApi.md#documentsRepaymentsDestroy) | **DELETE** /api/documents/repayments/{id}/ | 
[**documentsRepaymentsList**](DocumentsApi.md#documentsRepaymentsList) | **GET** /api/documents/repayments/ | 
[**documentsRepaymentsMarkPaidCreate**](DocumentsApi.md#documentsRepaymentsMarkPaidCreate) | **POST** /api/documents/repayments/{id}/mark-paid/ | 
[**documentsRepaymentsPartialUpdate**](DocumentsApi.md#documentsRepaymentsPartialUpdate) | **PATCH** /api/documents/repayments/{id}/ | 
[**documentsRepaymentsRetrieve**](DocumentsApi.md#documentsRepaymentsRetrieve) | **GET** /api/documents/repayments/{id}/ | 
[**documentsRepaymentsUpdate**](DocumentsApi.md#documentsRepaymentsUpdate) | **PUT** /api/documents/repayments/{id}/ | 



## documentsApplicationsLedgerRetrieve

> ApplicationLedger documentsApplicationsLedgerRetrieve(applicationId)



API endpoint for getting the ledger for an application

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

let apiInstance = new CrmClientJs.DocumentsApi();
let applicationId = 56; // Number | 
apiInstance.documentsApplicationsLedgerRetrieve(applicationId, (error, data, response) => {
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
 **applicationId** | **Number**|  | 

### Return type

[**ApplicationLedger**](ApplicationLedger.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsDocumentsCreate

> Document documentsDocumentsCreate(file, opts)



API endpoint for managing documents

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

let apiInstance = new CrmClientJs.DocumentsApi();
let file = "/path/to/file"; // File | 
let opts = {
  'title': "title_example", // String | 
  'description': "description_example", // String | 
  'documentType': new CrmClientJs.DocumentTypeEnum(), // DocumentTypeEnum | 
  'previousVersion': 56, // Number | 
  'application': 56, // Number | 
  'borrower': 56 // Number | 
};
apiInstance.documentsDocumentsCreate(file, opts, (error, data, response) => {
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
 **file** | **File**|  | 
 **title** | **String**|  | [optional] 
 **description** | **String**|  | [optional] 
 **documentType** | [**DocumentTypeEnum**](DocumentTypeEnum.md)|  | [optional] 
 **previousVersion** | **Number**|  | [optional] 
 **application** | **Number**|  | [optional] 
 **borrower** | **Number**|  | [optional] 

### Return type

[**Document**](Document.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: multipart/form-data, application/x-www-form-urlencoded
- **Accept**: application/json


## documentsDocumentsCreateVersionCreate

> Document documentsDocumentsCreateVersionCreate(id, file, opts)



API endpoint for creating a new version of a document

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | 
let file = "/path/to/file"; // File | 
let opts = {
  'title': "title_example", // String | 
  'description': "description_example", // String | 
  'documentType': new CrmClientJs.DocumentTypeEnum(), // DocumentTypeEnum | 
  'previousVersion': 56, // Number | 
  'application': 56, // Number | 
  'borrower': 56 // Number | 
};
apiInstance.documentsDocumentsCreateVersionCreate(id, file, opts, (error, data, response) => {
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
 **file** | **File**|  | 
 **title** | **String**|  | [optional] 
 **description** | **String**|  | [optional] 
 **documentType** | [**DocumentTypeEnum**](DocumentTypeEnum.md)|  | [optional] 
 **previousVersion** | **Number**|  | [optional] 
 **application** | **Number**|  | [optional] 
 **borrower** | **Number**|  | [optional] 

### Return type

[**Document**](Document.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: multipart/form-data, application/x-www-form-urlencoded
- **Accept**: application/json


## documentsDocumentsDestroy

> documentsDocumentsDestroy(id)



API endpoint for managing documents

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this document.
apiInstance.documentsDocumentsDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this document. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## documentsDocumentsDownloadRetrieve

> Document documentsDocumentsDownloadRetrieve(id)



Download a document

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this document.
apiInstance.documentsDocumentsDownloadRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this document. | 

### Return type

[**Document**](Document.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsDocumentsList

> PaginatedDocumentList documentsDocumentsList(opts)



API endpoint for managing documents

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

let apiInstance = new CrmClientJs.DocumentsApi();
let opts = {
  'application': 56, // Number | 
  'borrower': 56, // Number | 
  'createdAfter': new Date("2013-10-20"), // Date | 
  'createdBefore': new Date("2013-10-20"), // Date | 
  'documentType': "documentType_example", // String | * `application_form` - Application Form * `indicative_letter` - Indicative Letter * `formal_approval` - Formal Approval * `valuation_report` - Valuation Report * `qs_report` - Quantity Surveyor Report * `id_verification` - ID Verification * `bank_statement` - Bank Statement * `payslip` - Payslip * `tax_return` - Tax Return * `contract` - Contract * `other` - Other
  'ordering': "ordering_example", // String | Which field to use when ordering the results.
  'page': 56, // Number | A page number within the paginated result set.
  'search': "search_example" // String | A search term.
};
apiInstance.documentsDocumentsList(opts, (error, data, response) => {
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
 **createdAfter** | **Date**|  | [optional] 
 **createdBefore** | **Date**|  | [optional] 
 **documentType** | **String**| * &#x60;application_form&#x60; - Application Form * &#x60;indicative_letter&#x60; - Indicative Letter * &#x60;formal_approval&#x60; - Formal Approval * &#x60;valuation_report&#x60; - Valuation Report * &#x60;qs_report&#x60; - Quantity Surveyor Report * &#x60;id_verification&#x60; - ID Verification * &#x60;bank_statement&#x60; - Bank Statement * &#x60;payslip&#x60; - Payslip * &#x60;tax_return&#x60; - Tax Return * &#x60;contract&#x60; - Contract * &#x60;other&#x60; - Other | [optional] 
 **ordering** | **String**| Which field to use when ordering the results. | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **search** | **String**| A search term. | [optional] 

### Return type

[**PaginatedDocumentList**](PaginatedDocumentList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsDocumentsPartialUpdate

> Document documentsDocumentsPartialUpdate(id, opts)



API endpoint for managing documents

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this document.
let opts = {
  'title': "title_example", // String | 
  'description': "description_example", // String | 
  'documentType': new CrmClientJs.DocumentTypeEnum(), // DocumentTypeEnum | 
  'file': "/path/to/file", // File | 
  'previousVersion': 56, // Number | 
  'application': 56, // Number | 
  'borrower': 56 // Number | 
};
apiInstance.documentsDocumentsPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this document. | 
 **title** | **String**|  | [optional] 
 **description** | **String**|  | [optional] 
 **documentType** | [**DocumentTypeEnum**](DocumentTypeEnum.md)|  | [optional] 
 **file** | **File**|  | [optional] 
 **previousVersion** | **Number**|  | [optional] 
 **application** | **Number**|  | [optional] 
 **borrower** | **Number**|  | [optional] 

### Return type

[**Document**](Document.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: multipart/form-data, application/x-www-form-urlencoded
- **Accept**: application/json


## documentsDocumentsRetrieve

> Document documentsDocumentsRetrieve(id)



API endpoint for managing documents

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this document.
apiInstance.documentsDocumentsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this document. | 

### Return type

[**Document**](Document.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsDocumentsUpdate

> Document documentsDocumentsUpdate(id, file, opts)



API endpoint for managing documents

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this document.
let file = "/path/to/file"; // File | 
let opts = {
  'title': "title_example", // String | 
  'description': "description_example", // String | 
  'documentType': new CrmClientJs.DocumentTypeEnum(), // DocumentTypeEnum | 
  'previousVersion': 56, // Number | 
  'application': 56, // Number | 
  'borrower': 56 // Number | 
};
apiInstance.documentsDocumentsUpdate(id, file, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this document. | 
 **file** | **File**|  | 
 **title** | **String**|  | [optional] 
 **description** | **String**|  | [optional] 
 **documentType** | [**DocumentTypeEnum**](DocumentTypeEnum.md)|  | [optional] 
 **previousVersion** | **Number**|  | [optional] 
 **application** | **Number**|  | [optional] 
 **borrower** | **Number**|  | [optional] 

### Return type

[**Document**](Document.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: multipart/form-data, application/x-www-form-urlencoded
- **Accept**: application/json


## documentsFeesCreate

> Fee documentsFeesCreate(feeRequest)



API endpoint for managing fees

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

let apiInstance = new CrmClientJs.DocumentsApi();
let feeRequest = new CrmClientJs.FeeRequest(); // FeeRequest | 
apiInstance.documentsFeesCreate(feeRequest, (error, data, response) => {
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
 **feeRequest** | [**FeeRequest**](FeeRequest.md)|  | 

### Return type

[**Fee**](Fee.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsFeesDestroy

> documentsFeesDestroy(id)



API endpoint for managing fees

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this fee.
apiInstance.documentsFeesDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this fee. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## documentsFeesList

> PaginatedFeeList documentsFeesList(opts)



API endpoint for managing fees

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

let apiInstance = new CrmClientJs.DocumentsApi();
let opts = {
  'application': 56, // Number | 
  'dueAfter': new Date("2013-10-20"), // Date | 
  'dueBefore': new Date("2013-10-20"), // Date | 
  'feeType': "feeType_example", // String | * `application` - Application Fee * `valuation` - Valuation Fee * `legal` - Legal Fee * `broker` - Broker Fee * `settlement` - Settlement Fee * `other` - Other Fee
  'isPaid': true, // Boolean | 
  'maxAmount': 3.4, // Number | 
  'minAmount': 3.4, // Number | 
  'ordering': "ordering_example", // String | Which field to use when ordering the results.
  'page': 56, // Number | A page number within the paginated result set.
  'search': "search_example" // String | A search term.
};
apiInstance.documentsFeesList(opts, (error, data, response) => {
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
 **dueAfter** | **Date**|  | [optional] 
 **dueBefore** | **Date**|  | [optional] 
 **feeType** | **String**| * &#x60;application&#x60; - Application Fee * &#x60;valuation&#x60; - Valuation Fee * &#x60;legal&#x60; - Legal Fee * &#x60;broker&#x60; - Broker Fee * &#x60;settlement&#x60; - Settlement Fee * &#x60;other&#x60; - Other Fee | [optional] 
 **isPaid** | **Boolean**|  | [optional] 
 **maxAmount** | **Number**|  | [optional] 
 **minAmount** | **Number**|  | [optional] 
 **ordering** | **String**| Which field to use when ordering the results. | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **search** | **String**| A search term. | [optional] 

### Return type

[**PaginatedFeeList**](PaginatedFeeList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsFeesMarkPaidCreate

> Fee documentsFeesMarkPaidCreate(id, feeRequest)



API endpoint for marking a fee as paid

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | 
let feeRequest = new CrmClientJs.FeeRequest(); // FeeRequest | 
apiInstance.documentsFeesMarkPaidCreate(id, feeRequest, (error, data, response) => {
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
 **feeRequest** | [**FeeRequest**](FeeRequest.md)|  | 

### Return type

[**Fee**](Fee.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsFeesPartialUpdate

> Fee documentsFeesPartialUpdate(id, opts)



API endpoint for managing fees

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this fee.
let opts = {
  'patchedFeeRequest': new CrmClientJs.PatchedFeeRequest() // PatchedFeeRequest | 
};
apiInstance.documentsFeesPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this fee. | 
 **patchedFeeRequest** | [**PatchedFeeRequest**](PatchedFeeRequest.md)|  | [optional] 

### Return type

[**Fee**](Fee.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsFeesRetrieve

> Fee documentsFeesRetrieve(id)



API endpoint for managing fees

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this fee.
apiInstance.documentsFeesRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this fee. | 

### Return type

[**Fee**](Fee.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsFeesUpdate

> Fee documentsFeesUpdate(id, feeRequest)



API endpoint for managing fees

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this fee.
let feeRequest = new CrmClientJs.FeeRequest(); // FeeRequest | 
apiInstance.documentsFeesUpdate(id, feeRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this fee. | 
 **feeRequest** | [**FeeRequest**](FeeRequest.md)|  | 

### Return type

[**Fee**](Fee.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsNoteCommentsCreate

> NoteComment documentsNoteCommentsCreate(noteCommentRequest)



API endpoint for managing note comments

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

let apiInstance = new CrmClientJs.DocumentsApi();
let noteCommentRequest = new CrmClientJs.NoteCommentRequest(); // NoteCommentRequest | 
apiInstance.documentsNoteCommentsCreate(noteCommentRequest, (error, data, response) => {
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
 **noteCommentRequest** | [**NoteCommentRequest**](NoteCommentRequest.md)|  | 

### Return type

[**NoteComment**](NoteComment.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsNoteCommentsDestroy

> documentsNoteCommentsDestroy(id)



API endpoint for managing note comments

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this note comment.
apiInstance.documentsNoteCommentsDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this note comment. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## documentsNoteCommentsList

> PaginatedNoteCommentList documentsNoteCommentsList(opts)



API endpoint for managing note comments

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

let apiInstance = new CrmClientJs.DocumentsApi();
let opts = {
  'createdAfter': new Date("2013-10-20"), // Date | 
  'createdBefore': new Date("2013-10-20"), // Date | 
  'createdBy': 56, // Number | 
  'note': 56, // Number | 
  'ordering': "ordering_example", // String | Which field to use when ordering the results.
  'page': 56, // Number | A page number within the paginated result set.
  'search': "search_example" // String | A search term.
};
apiInstance.documentsNoteCommentsList(opts, (error, data, response) => {
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
 **createdAfter** | **Date**|  | [optional] 
 **createdBefore** | **Date**|  | [optional] 
 **createdBy** | **Number**|  | [optional] 
 **note** | **Number**|  | [optional] 
 **ordering** | **String**| Which field to use when ordering the results. | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **search** | **String**| A search term. | [optional] 

### Return type

[**PaginatedNoteCommentList**](PaginatedNoteCommentList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsNoteCommentsPartialUpdate

> NoteComment documentsNoteCommentsPartialUpdate(id, opts)



API endpoint for managing note comments

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this note comment.
let opts = {
  'patchedNoteCommentRequest': new CrmClientJs.PatchedNoteCommentRequest() // PatchedNoteCommentRequest | 
};
apiInstance.documentsNoteCommentsPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this note comment. | 
 **patchedNoteCommentRequest** | [**PatchedNoteCommentRequest**](PatchedNoteCommentRequest.md)|  | [optional] 

### Return type

[**NoteComment**](NoteComment.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsNoteCommentsRetrieve

> NoteComment documentsNoteCommentsRetrieve(id)



API endpoint for managing note comments

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this note comment.
apiInstance.documentsNoteCommentsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this note comment. | 

### Return type

[**NoteComment**](NoteComment.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsNoteCommentsUpdate

> NoteComment documentsNoteCommentsUpdate(id, noteCommentRequest)



API endpoint for managing note comments

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this note comment.
let noteCommentRequest = new CrmClientJs.NoteCommentRequest(); // NoteCommentRequest | 
apiInstance.documentsNoteCommentsUpdate(id, noteCommentRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this note comment. | 
 **noteCommentRequest** | [**NoteCommentRequest**](NoteCommentRequest.md)|  | 

### Return type

[**NoteComment**](NoteComment.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsNotesAddCommentCreate

> Note documentsNotesAddCommentCreate(id, opts)



Add a comment to a note

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this note.
let opts = {
  'noteRequest': new CrmClientJs.NoteRequest() // NoteRequest | 
};
apiInstance.documentsNotesAddCommentCreate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this note. | 
 **noteRequest** | [**NoteRequest**](NoteRequest.md)|  | [optional] 

### Return type

[**Note**](Note.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsNotesCommentsRetrieve

> Note documentsNotesCommentsRetrieve(id)



Get all comments for a note

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this note.
apiInstance.documentsNotesCommentsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this note. | 

### Return type

[**Note**](Note.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsNotesCreate

> Note documentsNotesCreate(opts)



API endpoint for managing notes

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

let apiInstance = new CrmClientJs.DocumentsApi();
let opts = {
  'noteRequest': new CrmClientJs.NoteRequest() // NoteRequest | 
};
apiInstance.documentsNotesCreate(opts, (error, data, response) => {
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
 **noteRequest** | [**NoteRequest**](NoteRequest.md)|  | [optional] 

### Return type

[**Note**](Note.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsNotesDestroy

> documentsNotesDestroy(id)



API endpoint for managing notes

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this note.
apiInstance.documentsNotesDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this note. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## documentsNotesList

> PaginatedNoteList documentsNotesList(opts)



API endpoint for managing notes

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

let apiInstance = new CrmClientJs.DocumentsApi();
let opts = {
  'application': 56, // Number | 
  'borrower': 56, // Number | 
  'createdAfter': new Date("2013-10-20"), // Date | 
  'createdBefore': new Date("2013-10-20"), // Date | 
  'ordering': "ordering_example", // String | Which field to use when ordering the results.
  'page': 56, // Number | A page number within the paginated result set.
  'search': "search_example" // String | A search term.
};
apiInstance.documentsNotesList(opts, (error, data, response) => {
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
 **createdAfter** | **Date**|  | [optional] 
 **createdBefore** | **Date**|  | [optional] 
 **ordering** | **String**| Which field to use when ordering the results. | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **search** | **String**| A search term. | [optional] 

### Return type

[**PaginatedNoteList**](PaginatedNoteList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsNotesPartialUpdate

> Note documentsNotesPartialUpdate(id, opts)



API endpoint for managing notes

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this note.
let opts = {
  'patchedNoteRequest': new CrmClientJs.PatchedNoteRequest() // PatchedNoteRequest | 
};
apiInstance.documentsNotesPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this note. | 
 **patchedNoteRequest** | [**PatchedNoteRequest**](PatchedNoteRequest.md)|  | [optional] 

### Return type

[**Note**](Note.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsNotesRetrieve

> Note documentsNotesRetrieve(id)



API endpoint for managing notes

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this note.
apiInstance.documentsNotesRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this note. | 

### Return type

[**Note**](Note.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsNotesUpdate

> Note documentsNotesUpdate(id, opts)



API endpoint for managing notes

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this note.
let opts = {
  'noteRequest': new CrmClientJs.NoteRequest() // NoteRequest | 
};
apiInstance.documentsNotesUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this note. | 
 **noteRequest** | [**NoteRequest**](NoteRequest.md)|  | [optional] 

### Return type

[**Note**](Note.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsRepaymentsCreate

> Repayment documentsRepaymentsCreate(repaymentRequest)



API endpoint for managing repayments

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

let apiInstance = new CrmClientJs.DocumentsApi();
let repaymentRequest = new CrmClientJs.RepaymentRequest(); // RepaymentRequest | 
apiInstance.documentsRepaymentsCreate(repaymentRequest, (error, data, response) => {
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
 **repaymentRequest** | [**RepaymentRequest**](RepaymentRequest.md)|  | 

### Return type

[**Repayment**](Repayment.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsRepaymentsDestroy

> documentsRepaymentsDestroy(id)



API endpoint for managing repayments

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this repayment.
apiInstance.documentsRepaymentsDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this repayment. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## documentsRepaymentsList

> PaginatedRepaymentList documentsRepaymentsList(opts)



API endpoint for managing repayments

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

let apiInstance = new CrmClientJs.DocumentsApi();
let opts = {
  'application': 56, // Number | 
  'dueAfter': new Date("2013-10-20"), // Date | 
  'dueBefore': new Date("2013-10-20"), // Date | 
  'isPaid': true, // Boolean | 
  'maxAmount': 3.4, // Number | 
  'minAmount': 3.4, // Number | 
  'ordering': "ordering_example", // String | Which field to use when ordering the results.
  'page': 56, // Number | A page number within the paginated result set.
  'search': "search_example" // String | A search term.
};
apiInstance.documentsRepaymentsList(opts, (error, data, response) => {
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
 **dueAfter** | **Date**|  | [optional] 
 **dueBefore** | **Date**|  | [optional] 
 **isPaid** | **Boolean**|  | [optional] 
 **maxAmount** | **Number**|  | [optional] 
 **minAmount** | **Number**|  | [optional] 
 **ordering** | **String**| Which field to use when ordering the results. | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **search** | **String**| A search term. | [optional] 

### Return type

[**PaginatedRepaymentList**](PaginatedRepaymentList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsRepaymentsMarkPaidCreate

> Repayment documentsRepaymentsMarkPaidCreate(id, repaymentRequest)



API endpoint for marking a repayment as paid

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | 
let repaymentRequest = new CrmClientJs.RepaymentRequest(); // RepaymentRequest | 
apiInstance.documentsRepaymentsMarkPaidCreate(id, repaymentRequest, (error, data, response) => {
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
 **repaymentRequest** | [**RepaymentRequest**](RepaymentRequest.md)|  | 

### Return type

[**Repayment**](Repayment.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsRepaymentsPartialUpdate

> Repayment documentsRepaymentsPartialUpdate(id, opts)



API endpoint for managing repayments

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this repayment.
let opts = {
  'patchedRepaymentRequest': new CrmClientJs.PatchedRepaymentRequest() // PatchedRepaymentRequest | 
};
apiInstance.documentsRepaymentsPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this repayment. | 
 **patchedRepaymentRequest** | [**PatchedRepaymentRequest**](PatchedRepaymentRequest.md)|  | [optional] 

### Return type

[**Repayment**](Repayment.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## documentsRepaymentsRetrieve

> Repayment documentsRepaymentsRetrieve(id)



API endpoint for managing repayments

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this repayment.
apiInstance.documentsRepaymentsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this repayment. | 

### Return type

[**Repayment**](Repayment.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## documentsRepaymentsUpdate

> Repayment documentsRepaymentsUpdate(id, repaymentRequest)



API endpoint for managing repayments

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

let apiInstance = new CrmClientJs.DocumentsApi();
let id = 56; // Number | A unique integer value identifying this repayment.
let repaymentRequest = new CrmClientJs.RepaymentRequest(); // RepaymentRequest | 
apiInstance.documentsRepaymentsUpdate(id, repaymentRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this repayment. | 
 **repaymentRequest** | [**RepaymentRequest**](RepaymentRequest.md)|  | 

### Return type

[**Repayment**](Repayment.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json

