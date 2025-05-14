# CrmClientJs.ProductsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**productsProductsCreate**](ProductsApi.md#productsProductsCreate) | **POST** /api/products/products/ | 
[**productsProductsDestroy**](ProductsApi.md#productsProductsDestroy) | **DELETE** /api/products/products/{id}/ | 
[**productsProductsList**](ProductsApi.md#productsProductsList) | **GET** /api/products/products/ | 
[**productsProductsPartialUpdate**](ProductsApi.md#productsProductsPartialUpdate) | **PATCH** /api/products/products/{id}/ | 
[**productsProductsRetrieve**](ProductsApi.md#productsProductsRetrieve) | **GET** /api/products/products/{id}/ | 
[**productsProductsUpdate**](ProductsApi.md#productsProductsUpdate) | **PUT** /api/products/products/{id}/ | 



## productsProductsCreate

> Product productsProductsCreate(productRequest)



API endpoint for managing loan products

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

let apiInstance = new CrmClientJs.ProductsApi();
let productRequest = new CrmClientJs.ProductRequest(); // ProductRequest | 
apiInstance.productsProductsCreate(productRequest, (error, data, response) => {
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
 **productRequest** | [**ProductRequest**](ProductRequest.md)|  | 

### Return type

[**Product**](Product.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## productsProductsDestroy

> productsProductsDestroy(id)



API endpoint for managing loan products

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

let apiInstance = new CrmClientJs.ProductsApi();
let id = 56; // Number | A unique integer value identifying this Product.
apiInstance.productsProductsDestroy(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this Product. | 

### Return type

null (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## productsProductsList

> PaginatedProductList productsProductsList(opts)



API endpoint for managing loan products

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

let apiInstance = new CrmClientJs.ProductsApi();
let opts = {
  'application': 56, // Number | 
  'applications': [null], // [Number] | 
  'borrower': 56, // Number | 
  'borrowers': [null], // [Number] | 
  'name': "name_example", // String | 
  'nameIcontains': "nameIcontains_example", // String | 
  'ordering': "ordering_example", // String | Which field to use when ordering the results.
  'page': 56, // Number | A page number within the paginated result set.
  'search': "search_example" // String | A search term.
};
apiInstance.productsProductsList(opts, (error, data, response) => {
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
 **applications** | [**[Number]**](Number.md)|  | [optional] 
 **borrower** | **Number**|  | [optional] 
 **borrowers** | [**[Number]**](Number.md)|  | [optional] 
 **name** | **String**|  | [optional] 
 **nameIcontains** | **String**|  | [optional] 
 **ordering** | **String**| Which field to use when ordering the results. | [optional] 
 **page** | **Number**| A page number within the paginated result set. | [optional] 
 **search** | **String**| A search term. | [optional] 

### Return type

[**PaginatedProductList**](PaginatedProductList.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## productsProductsPartialUpdate

> Product productsProductsPartialUpdate(id, opts)



API endpoint for managing loan products

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

let apiInstance = new CrmClientJs.ProductsApi();
let id = 56; // Number | A unique integer value identifying this Product.
let opts = {
  'patchedProductRequest': new CrmClientJs.PatchedProductRequest() // PatchedProductRequest | 
};
apiInstance.productsProductsPartialUpdate(id, opts, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this Product. | 
 **patchedProductRequest** | [**PatchedProductRequest**](PatchedProductRequest.md)|  | [optional] 

### Return type

[**Product**](Product.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json


## productsProductsRetrieve

> Product productsProductsRetrieve(id)



API endpoint for managing loan products

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

let apiInstance = new CrmClientJs.ProductsApi();
let id = 56; // Number | A unique integer value identifying this Product.
apiInstance.productsProductsRetrieve(id, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this Product. | 

### Return type

[**Product**](Product.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## productsProductsUpdate

> Product productsProductsUpdate(id, productRequest)



API endpoint for managing loan products

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

let apiInstance = new CrmClientJs.ProductsApi();
let id = 56; // Number | A unique integer value identifying this Product.
let productRequest = new CrmClientJs.ProductRequest(); // ProductRequest | 
apiInstance.productsProductsUpdate(id, productRequest, (error, data, response) => {
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
 **id** | **Number**| A unique integer value identifying this Product. | 
 **productRequest** | [**ProductRequest**](ProductRequest.md)|  | 

### Return type

[**Product**](Product.md)

### Authorization

[jwtAuth](../README.md#jwtAuth), [Bearer](../README.md#Bearer)

### HTTP request headers

- **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
- **Accept**: application/json

