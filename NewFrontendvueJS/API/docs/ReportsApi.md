# CrmClientJs.ReportsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**reportsApplicationStatusRetrieve**](ReportsApi.md#reportsApplicationStatusRetrieve) | **GET** /api/reports/application-status/ | 
[**reportsApplicationVolumeRetrieve**](ReportsApi.md#reportsApplicationVolumeRetrieve) | **GET** /api/reports/application-volume/ | 
[**reportsRepaymentComplianceRetrieve**](ReportsApi.md#reportsRepaymentComplianceRetrieve) | **GET** /api/reports/repayment-compliance/ | 



## reportsApplicationStatusRetrieve

> ApplicationStatusReport reportsApplicationStatusRetrieve()



API endpoint for application status reports

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

let apiInstance = new CrmClientJs.ReportsApi();
apiInstance.reportsApplicationStatusRetrieve((error, data, response) => {
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

[**ApplicationStatusReport**](ApplicationStatusReport.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## reportsApplicationVolumeRetrieve

> ApplicationVolumeReport reportsApplicationVolumeRetrieve()



API endpoint for application volume reports

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

let apiInstance = new CrmClientJs.ReportsApi();
apiInstance.reportsApplicationVolumeRetrieve((error, data, response) => {
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

[**ApplicationVolumeReport**](ApplicationVolumeReport.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## reportsRepaymentComplianceRetrieve

> RepaymentComplianceReport reportsRepaymentComplianceRetrieve()



API endpoint for repayment compliance reports

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

let apiInstance = new CrmClientJs.ReportsApi();
apiInstance.reportsRepaymentComplianceRetrieve((error, data, response) => {
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

[**RepaymentComplianceReport**](RepaymentComplianceReport.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

