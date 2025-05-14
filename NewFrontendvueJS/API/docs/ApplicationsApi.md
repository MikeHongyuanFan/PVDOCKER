# CrmClientJs.ApplicationsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**applicationsApplicationsAddFeeCreate**](ApplicationsApi.md#applicationsApplicationsAddFeeCreate) | **POST** /api/applications/applications/{id}/add_fee/ | 
[**applicationsApplicationsAddNoteCreate**](ApplicationsApi.md#applicationsApplicationsAddNoteCreate) | **POST** /api/applications/applications/{id}/add_note/ | 
[**applicationsApplicationsAddRepaymentCreate**](ApplicationsApi.md#applicationsApplicationsAddRepaymentCreate) | **POST** /api/applications/applications/{id}/add_repayment/ | 
[**applicationsApplicationsBorrowersUpdate**](ApplicationsApi.md#applicationsApplicationsBorrowersUpdate) | **PUT** /api/applications/applications/{id}/borrowers/ | 
[**applicationsApplicationsCreate**](ApplicationsApi.md#applicationsApplicationsCreate) | **POST** /api/applications/applications/ | 
[**applicationsApplicationsDestroy**](ApplicationsApi.md#applicationsApplicationsDestroy) | **DELETE** /api/applications/applications/{id}/ | 
[**applicationsApplicationsDocumentsRetrieve**](ApplicationsApi.md#applicationsApplicationsDocumentsRetrieve) | **GET** /api/applications/applications/{id}/documents/ | 
[**applicationsApplicationsExtendLoanCreate**](ApplicationsApi.md#applicationsApplicationsExtendLoanCreate) | **POST** /api/applications/applications/{id}/extend_loan/ | 
[**applicationsApplicationsFeesRetrieve**](ApplicationsApi.md#applicationsApplicationsFeesRetrieve) | **GET** /api/applications/applications/{id}/fees/ | 
[**applicationsApplicationsFundingCalculationCreate**](ApplicationsApi.md#applicationsApplicationsFundingCalculationCreate) | **POST** /api/applications/applications/{id}/funding_calculation/ | 
[**applicationsApplicationsFundingCalculationHistoryRetrieve**](ApplicationsApi.md#applicationsApplicationsFundingCalculationHistoryRetrieve) | **GET** /api/applications/applications/{id}/funding_calculation_history/ | 
[**applicationsApplicationsLedgerRetrieve**](ApplicationsApi.md#applicationsApplicationsLedgerRetrieve) | **GET** /api/applications/applications/{id}/ledger/ | 
[**applicationsApplicationsList**](ApplicationsApi.md#applicationsApplicationsList) | **GET** /api/applications/applications/ | 
[**applicationsApplicationsNotesRetrieve**](ApplicationsApi.md#applicationsApplicationsNotesRetrieve) | **GET** /api/applications/applications/{id}/notes/ | 
[**applicationsApplicationsPartialUpdate**](ApplicationsApi.md#applicationsApplicationsPartialUpdate) | **PATCH** /api/applications/applications/{id}/ | 
[**applicationsApplicationsRecordPaymentCreate**](ApplicationsApi.md#applicationsApplicationsRecordPaymentCreate) | **POST** /api/applications/applications/{id}/record_payment/ | 
[**applicationsApplicationsRemoveBorrowersCreate**](ApplicationsApi.md#applicationsApplicationsRemoveBorrowersCreate) | **POST** /api/applications/applications/{id}/remove_borrowers/ | 
[**applicationsApplicationsRepaymentsRetrieve**](ApplicationsApi.md#applicationsApplicationsRepaymentsRetrieve) | **GET** /api/applications/applications/{id}/repayments/ | 
[**applicationsApplicationsRetrieve**](ApplicationsApi.md#applicationsApplicationsRetrieve) | **GET** /api/applications/applications/{id}/ | 
[**applicationsApplicationsSignCreate**](ApplicationsApi.md#applicationsApplicationsSignCreate) | **POST** /api/applications/applications/{id}/sign/ | 
[**applicationsApplicationsSignatureCreate**](ApplicationsApi.md#applicationsApplicationsSignatureCreate) | **POST** /api/applications/applications/{id}/signature/ | 
[**applicationsApplicationsUpdate**](ApplicationsApi.md#applicationsApplicationsUpdate) | **PUT** /api/applications/applications/{id}/ | 
[**applicationsApplicationsUpdateStageCreate**](ApplicationsApi.md#applicationsApplicationsUpdateStageCreate) | **POST** /api/applications/applications/{id}/update_stage/ | 
[**applicationsApplicationsUploadDocumentCreate**](ApplicationsApi.md#applicationsApplicationsUploadDocumentCreate) | **POST** /api/applications/applications/{id}/upload_document/ | 
[**applicationsApplicationsValidateSchemaCreate**](ApplicationsApi.md#applicationsApplicationsValidateSchemaCreate) | **POST** /api/applications/applications/validate_schema/ | 
[**applicationsBorrowersUpdate**](ApplicationsApi.md#applicationsBorrowersUpdate) | **PUT** /api/applications/{id}/borrowers/ | 
[**applicationsCreateWithCascadeCreate**](ApplicationsApi.md#applicationsCreateWithCascadeCreate) | **POST** /api/applications/create-with-cascade/ | 
[**applicationsExtendLoanCreate**](ApplicationsApi.md#applicationsExtendLoanCreate) | **POST** /api/applications/{id}/extend-loan/ | 
[**applicationsFundingCalculationCreate**](ApplicationsApi.md#applicationsFundingCalculationCreate) | **POST** /api/applications/{id}/funding-calculation/ | 
[**applicationsFundingCalculationHistoryRetrieve**](ApplicationsApi.md#applicationsFundingCalculationHistoryRetrieve) | **GET** /api/applications/{id}/funding-calculation-history/ | 
[**applicationsSignCreate**](ApplicationsApi.md#applicationsSignCreate) | **POST** /api/applications/{id}/sign/ | 
[**applicationsSignatureCreate**](ApplicationsApi.md#applicationsSignatureCreate) | **POST** /api/applications/{id}/signature/ | 
[**applicationsStageUpdate**](ApplicationsApi.md#applicationsStageUpdate) | **PUT** /api/applications/{id}/stage/ | 
[**applicationsValidateSchemaCreate**](ApplicationsApi.md#applicationsValidateSchemaCreate) | **POST** /api/applications/validate-schema/ | 



## applicationsApplicationsAddFeeCreate

> ApplicationDetail applicationsApplicationsAddFeeCreate(id, opts)



Add a fee to an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let opts = {
  'applicationDetailRequest': new CrmClientJs.ApplicationDetailRequest() // ApplicationDetailRequest | 
};
apiInstance.applicationsApplicationsAddFeeCreate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **applicationDetailRequest** | [**ApplicationDetailRequest**](ApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsAddNoteCreate

> ApplicationDetail applicationsApplicationsAddNoteCreate(id, opts)



Add a note to an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let opts = {
  'applicationDetailRequest': new CrmClientJs.ApplicationDetailRequest() // ApplicationDetailRequest | 
};
apiInstance.applicationsApplicationsAddNoteCreate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **applicationDetailRequest** | [**ApplicationDetailRequest**](ApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsAddRepaymentCreate

> ApplicationDetail applicationsApplicationsAddRepaymentCreate(id, opts)



Add a repayment to an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let opts = {
  'applicationDetailRequest': new CrmClientJs.ApplicationDetailRequest() // ApplicationDetailRequest | 
};
apiInstance.applicationsApplicationsAddRepaymentCreate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **applicationDetailRequest** | [**ApplicationDetailRequest**](ApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsBorrowersUpdate

> ApplicationDetail applicationsApplicationsBorrowersUpdate(id, opts)



Update borrowers for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let opts = {
  'applicationDetailRequest': new CrmClientJs.ApplicationDetailRequest() // ApplicationDetailRequest | 
};
apiInstance.applicationsApplicationsBorrowersUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **applicationDetailRequest** | [**ApplicationDetailRequest**](ApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsCreate

> ApplicationCreate applicationsApplicationsCreate(opts)



API endpoint for managing loan applications

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let opts = {
  'applicationCreateRequest': new CrmClientJs.ApplicationCreateRequest() // ApplicationCreateRequest | 
};
apiInstance.applicationsApplicationsCreate(opts, (error, data, response) => {
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
 **applicationCreateRequest** | [**ApplicationCreateRequest**](ApplicationCreateRequest.md)|  | [optional] 

### Return type

[**ApplicationCreate**](ApplicationCreate.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsDestroy

> applicationsApplicationsDestroy(id)



API endpoint for managing loan applications

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
apiInstance.applicationsApplicationsDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## applicationsApplicationsDocumentsRetrieve

> ApplicationDetail applicationsApplicationsDocumentsRetrieve(id)



Get all documents for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
apiInstance.applicationsApplicationsDocumentsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## applicationsApplicationsExtendLoanCreate

> LoanExtension applicationsApplicationsExtendLoanCreate(id, loanExtensionRequest)



Extend a loan with new terms and regenerate repayment schedule

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let loanExtensionRequest = new CrmClientJs.LoanExtensionRequest(); // LoanExtensionRequest | 
apiInstance.applicationsApplicationsExtendLoanCreate(id, loanExtensionRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **loanExtensionRequest** | [**LoanExtensionRequest**](LoanExtensionRequest.md)|  | 

### Return type

[**LoanExtension**](LoanExtension.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsFeesRetrieve

> ApplicationDetail applicationsApplicationsFeesRetrieve(id)



Get all fees for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
apiInstance.applicationsApplicationsFeesRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## applicationsApplicationsFundingCalculationCreate

> FundingCalculationInput applicationsApplicationsFundingCalculationCreate(id, fundingCalculationInputRequest)



Create or update funding calculation for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let fundingCalculationInputRequest = new CrmClientJs.FundingCalculationInputRequest(); // FundingCalculationInputRequest | 
apiInstance.applicationsApplicationsFundingCalculationCreate(id, fundingCalculationInputRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **fundingCalculationInputRequest** | [**FundingCalculationInputRequest**](FundingCalculationInputRequest.md)|  | 

### Return type

[**FundingCalculationInput**](FundingCalculationInput.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsFundingCalculationHistoryRetrieve

> FundingCalculationHistory applicationsApplicationsFundingCalculationHistoryRetrieve(id)



Get funding calculation history for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
apiInstance.applicationsApplicationsFundingCalculationHistoryRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 

### Return type

[**FundingCalculationHistory**](FundingCalculationHistory.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## applicationsApplicationsLedgerRetrieve

> ApplicationDetail applicationsApplicationsLedgerRetrieve(id)



Get ledger entries for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
apiInstance.applicationsApplicationsLedgerRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## applicationsApplicationsList

> PaginatedApplicationDetailList applicationsApplicationsList(opts)



API endpoint for managing loan applications

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let opts = {
  'applicationType': "applicationType_example", // String | * `residential` - Residential * `commercial` - Commercial * `construction` - Construction * `refinance` - Refinance * `investment` - Investment * `smsf` - SMSF
  'bd': 56, // Number | 
  'branch': 56, // Number | 
  'broker': 56, // Number | 
  'createdAfter': new Date("2013-10-20"), // Date | 
  'createdBefore': new Date("2013-10-20"), // Date | 
  'maxInterestRate': 3.4, // Number | 
  'maxLoanAmount': 3.4, // Number | 
  'minInterestRate': 3.4, // Number | 
  'minLoanAmount': 3.4, // Number | 
  'ordering': "ordering_example", // String | Which field to use when ordering the results.
  'page': 56, // Number | A page number within the paginated result set.
  'repaymentFrequency': "repaymentFrequency_example", // String | * `weekly` - Weekly * `fortnightly` - Fortnightly * `monthly` - Monthly * `quarterly` - Quarterly * `annually` - Annually
  'search': "search_example", // String | A search term.
  'stage': "stage_example" // String | * `inquiry` - Inquiry * `sent_to_lender` - Sent to Lender * `funding_table_issued` - Funding Table Issued * `iloo_issued` - ILOO Issued * `iloo_signed` - ILOO Signed * `commitment_fee_paid` - Commitment Fee Paid * `app_submitted` - App Submitted * `valuation_ordered` - Valuation Ordered * `valuation_received` - Valuation Received * `more_info_required` - More Info Required * `formal_approval` - Formal Approval * `loan_docs_instructed` - Loan Docs Instructed * `loan_docs_issued` - Loan Docs Issued * `loan_docs_signed` - Loan Docs Signed * `settlement_conditions` - Settlement Conditions * `settled` - Settled * `closed` - Closed * `declined` - Declined * `withdrawn` - Withdrawn
};
apiInstance.applicationsApplicationsList(opts, (error, data, response) => {
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
 **applicationType** | **String**| * &#x60;residential&#x60; - Residential * &#x60;commercial&#x60; - Commercial * &#x60;construction&#x60; - Construction * &#x60;refinance&#x60; - Refinance * &#x60;investment&#x60; - Investment * &#x60;smsf&#x60; - SMSF | [optional] 
 **bd** | **Number**|  | [optional] 
 **branch** | **Number**|  | [optional] 
 **broker** | **Number**|  | [optional] 
 **createdAfter** | **Date**|  | [optional] 
 **createdBefore** | **Date**|  | [optional] 
 **maxInterestRate** | **Number**|  | [optional] 
 **maxLoanAmount** | **Number**|  | [optional] 
 **minInterestRate** | **Number**|  | [optional] 
 **minLoanAmount** | **Number**|  | [optional] 
 **ordering** | **String**| Which field to use when ordering the results. | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **repaymentFrequency** | **String**| * &#x60;weekly&#x60; - Weekly * &#x60;fortnightly&#x60; - Fortnightly * &#x60;monthly&#x60; - Monthly * &#x60;quarterly&#x60; - Quarterly * &#x60;annually&#x60; - Annually | [optional] 
 **search** | **String**| A search term. | [optional] 
 **stage** | **String**| * &#x60;inquiry&#x60; - Inquiry * &#x60;sent_to_lender&#x60; - Sent to Lender * &#x60;funding_table_issued&#x60; - Funding Table Issued * &#x60;iloo_issued&#x60; - ILOO Issued * &#x60;iloo_signed&#x60; - ILOO Signed * &#x60;commitment_fee_paid&#x60; - Commitment Fee Paid * &#x60;app_submitted&#x60; - App Submitted * &#x60;valuation_ordered&#x60; - Valuation Ordered * &#x60;valuation_received&#x60; - Valuation Received * &#x60;more_info_required&#x60; - More Info Required * &#x60;formal_approval&#x60; - Formal Approval * &#x60;loan_docs_instructed&#x60; - Loan Docs Instructed * &#x60;loan_docs_issued&#x60; - Loan Docs Issued * &#x60;loan_docs_signed&#x60; - Loan Docs Signed * &#x60;settlement_conditions&#x60; - Settlement Conditions * &#x60;settled&#x60; - Settled * &#x60;closed&#x60; - Closed * &#x60;declined&#x60; - Declined * &#x60;withdrawn&#x60; - Withdrawn | [optional] 

### Return type

[**PaginatedApplicationDetailList**](PaginatedApplicationDetailList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## applicationsApplicationsNotesRetrieve

> ApplicationDetail applicationsApplicationsNotesRetrieve(id)



Get all notes for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
apiInstance.applicationsApplicationsNotesRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## applicationsApplicationsPartialUpdate

> ApplicationDetail applicationsApplicationsPartialUpdate(id, opts)



API endpoint for managing loan applications

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let opts = {
  'patchedApplicationDetailRequest': new CrmClientJs.PatchedApplicationDetailRequest() // PatchedApplicationDetailRequest | 
};
apiInstance.applicationsApplicationsPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **patchedApplicationDetailRequest** | [**PatchedApplicationDetailRequest**](PatchedApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsRecordPaymentCreate

> ApplicationDetail applicationsApplicationsRecordPaymentCreate(id, opts)



Record a payment for a repayment

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let opts = {
  'applicationDetailRequest': new CrmClientJs.ApplicationDetailRequest() // ApplicationDetailRequest | 
};
apiInstance.applicationsApplicationsRecordPaymentCreate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **applicationDetailRequest** | [**ApplicationDetailRequest**](ApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsRemoveBorrowersCreate

> ApplicationBorrower applicationsApplicationsRemoveBorrowersCreate(id, applicationBorrowerRequest)



Remove borrowers from application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let applicationBorrowerRequest = new CrmClientJs.ApplicationBorrowerRequest(); // ApplicationBorrowerRequest | 
apiInstance.applicationsApplicationsRemoveBorrowersCreate(id, applicationBorrowerRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **applicationBorrowerRequest** | [**ApplicationBorrowerRequest**](ApplicationBorrowerRequest.md)|  | 

### Return type

[**ApplicationBorrower**](ApplicationBorrower.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsRepaymentsRetrieve

> ApplicationDetail applicationsApplicationsRepaymentsRetrieve(id)



Get all repayments for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
apiInstance.applicationsApplicationsRepaymentsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## applicationsApplicationsRetrieve

> ApplicationDetail applicationsApplicationsRetrieve(id)



API endpoint for managing loan applications

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
apiInstance.applicationsApplicationsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## applicationsApplicationsSignCreate

> ApplicationSignature applicationsApplicationsSignCreate(id, applicationSignatureRequest)



Sign an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let applicationSignatureRequest = new CrmClientJs.ApplicationSignatureRequest(); // ApplicationSignatureRequest | 
apiInstance.applicationsApplicationsSignCreate(id, applicationSignatureRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **applicationSignatureRequest** | [**ApplicationSignatureRequest**](ApplicationSignatureRequest.md)|  | 

### Return type

[**ApplicationSignature**](ApplicationSignature.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsSignatureCreate

> ApplicationDetail applicationsApplicationsSignatureCreate(id, opts)



Process signature for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let opts = {
  'applicationDetailRequest': new CrmClientJs.ApplicationDetailRequest() // ApplicationDetailRequest | 
};
apiInstance.applicationsApplicationsSignatureCreate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **applicationDetailRequest** | [**ApplicationDetailRequest**](ApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsUpdate

> ApplicationDetail applicationsApplicationsUpdate(id, opts)



API endpoint for managing loan applications

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let opts = {
  'applicationDetailRequest': new CrmClientJs.ApplicationDetailRequest() // ApplicationDetailRequest | 
};
apiInstance.applicationsApplicationsUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **applicationDetailRequest** | [**ApplicationDetailRequest**](ApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsUpdateStageCreate

> ApplicationStageUpdate applicationsApplicationsUpdateStageCreate(id, applicationStageUpdateRequest)



Update application stage

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let applicationStageUpdateRequest = new CrmClientJs.ApplicationStageUpdateRequest(); // ApplicationStageUpdateRequest | 
apiInstance.applicationsApplicationsUpdateStageCreate(id, applicationStageUpdateRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **applicationStageUpdateRequest** | [**ApplicationStageUpdateRequest**](ApplicationStageUpdateRequest.md)|  | 

### Return type

[**ApplicationStageUpdate**](ApplicationStageUpdate.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsUploadDocumentCreate

> ApplicationDetail applicationsApplicationsUploadDocumentCreate(id, opts)



Upload a document for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | A unique integer value identifying this application.
let opts = {
  'applicationDetailRequest': new CrmClientJs.ApplicationDetailRequest() // ApplicationDetailRequest | 
};
apiInstance.applicationsApplicationsUploadDocumentCreate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this application. | 
 **applicationDetailRequest** | [**ApplicationDetailRequest**](ApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsApplicationsValidateSchemaCreate

> ApplicationDetail applicationsApplicationsValidateSchemaCreate(opts)



Validate application schema

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let opts = {
  'applicationDetailRequest': new CrmClientJs.ApplicationDetailRequest() // ApplicationDetailRequest | 
};
apiInstance.applicationsApplicationsValidateSchemaCreate(opts, (error, data, response) => {
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
 **applicationDetailRequest** | [**ApplicationDetailRequest**](ApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsBorrowersUpdate

> ApplicationDetail applicationsBorrowersUpdate(id, opts)



Update borrowers for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | 
let opts = {
  'applicationDetailRequest': new CrmClientJs.ApplicationDetailRequest() // ApplicationDetailRequest | 
};
apiInstance.applicationsBorrowersUpdate(id, opts, (error, data, response) => {
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
 **applicationDetailRequest** | [**ApplicationDetailRequest**](ApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsCreateWithCascadeCreate

> ApplicationCreate applicationsCreateWithCascadeCreate(opts)



API endpoint for managing loan applications

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let opts = {
  'applicationCreateRequest': new CrmClientJs.ApplicationCreateRequest() // ApplicationCreateRequest | 
};
apiInstance.applicationsCreateWithCascadeCreate(opts, (error, data, response) => {
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
 **applicationCreateRequest** | [**ApplicationCreateRequest**](ApplicationCreateRequest.md)|  | [optional] 

### Return type

[**ApplicationCreate**](ApplicationCreate.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsExtendLoanCreate

> LoanExtension applicationsExtendLoanCreate(id, loanExtensionRequest)



Extend a loan with new terms and regenerate repayment schedule

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | 
let loanExtensionRequest = new CrmClientJs.LoanExtensionRequest(); // LoanExtensionRequest | 
apiInstance.applicationsExtendLoanCreate(id, loanExtensionRequest, (error, data, response) => {
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
 **loanExtensionRequest** | [**LoanExtensionRequest**](LoanExtensionRequest.md)|  | 

### Return type

[**LoanExtension**](LoanExtension.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsFundingCalculationCreate

> FundingCalculationInput applicationsFundingCalculationCreate(id, fundingCalculationInputRequest)



Create or update funding calculation for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | 
let fundingCalculationInputRequest = new CrmClientJs.FundingCalculationInputRequest(); // FundingCalculationInputRequest | 
apiInstance.applicationsFundingCalculationCreate(id, fundingCalculationInputRequest, (error, data, response) => {
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
 **fundingCalculationInputRequest** | [**FundingCalculationInputRequest**](FundingCalculationInputRequest.md)|  | 

### Return type

[**FundingCalculationInput**](FundingCalculationInput.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsFundingCalculationHistoryRetrieve

> FundingCalculationHistory applicationsFundingCalculationHistoryRetrieve(id)



Get funding calculation history for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | 
apiInstance.applicationsFundingCalculationHistoryRetrieve(id, (error, data, response) => {
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

[**FundingCalculationHistory**](FundingCalculationHistory.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## applicationsSignCreate

> ApplicationSignature applicationsSignCreate(id, applicationSignatureRequest)



Sign an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | 
let applicationSignatureRequest = new CrmClientJs.ApplicationSignatureRequest(); // ApplicationSignatureRequest | 
apiInstance.applicationsSignCreate(id, applicationSignatureRequest, (error, data, response) => {
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
 **applicationSignatureRequest** | [**ApplicationSignatureRequest**](ApplicationSignatureRequest.md)|  | 

### Return type

[**ApplicationSignature**](ApplicationSignature.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsSignatureCreate

> ApplicationDetail applicationsSignatureCreate(id, opts)



Process signature for an application

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | 
let opts = {
  'applicationDetailRequest': new CrmClientJs.ApplicationDetailRequest() // ApplicationDetailRequest | 
};
apiInstance.applicationsSignatureCreate(id, opts, (error, data, response) => {
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
 **applicationDetailRequest** | [**ApplicationDetailRequest**](ApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsStageUpdate

> ApplicationStageUpdate applicationsStageUpdate(id, applicationStageUpdateRequest)



Update application stage

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let id = 56; // Number | 
let applicationStageUpdateRequest = new CrmClientJs.ApplicationStageUpdateRequest(); // ApplicationStageUpdateRequest | 
apiInstance.applicationsStageUpdate(id, applicationStageUpdateRequest, (error, data, response) => {
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
 **applicationStageUpdateRequest** | [**ApplicationStageUpdateRequest**](ApplicationStageUpdateRequest.md)|  | 

### Return type

[**ApplicationStageUpdate**](ApplicationStageUpdate.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## applicationsValidateSchemaCreate

> ApplicationDetail applicationsValidateSchemaCreate(opts)



Validate application schema

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

let apiInstance = new CrmClientJs.ApplicationsApi();
let opts = {
  'applicationDetailRequest': new CrmClientJs.ApplicationDetailRequest() // ApplicationDetailRequest | 
};
apiInstance.applicationsValidateSchemaCreate(opts, (error, data, response) => {
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
 **applicationDetailRequest** | [**ApplicationDetailRequest**](ApplicationDetailRequest.md)|  | [optional] 

### Return type

[**ApplicationDetail**](ApplicationDetail.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json

