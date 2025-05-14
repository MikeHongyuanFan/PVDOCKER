// Test script for ApiClient.js
// Note: This is a simple test to check basic functionality

// Create a mock ApiClient for testing
const mockApiClient = {
  basePath: 'https://3.25.246.57',
  
  buildUrl: function(path, pathParams, apiBasePath) {
    if (!path.match(/^\//)) {
      path = '/' + path;
    }
    
    let url = this.basePath + path;
    
    if (apiBasePath !== null && apiBasePath !== undefined) {
      url = apiBasePath + path;
    }
    
    url = url.replace(/\{([\w-\.#]+)\}/g, (fullMatch, key) => {
      let value;
      if (pathParams.hasOwnProperty(key)) {
        value = pathParams[key];
      } else {
        value = fullMatch;
      }
      
      return encodeURIComponent(value);
    });
    
    return url;
  },
  
  paramToString: function(param) {
    if (param == undefined || param == null) {
      return '';
    }
    if (param instanceof Date) {
      return param.toJSON();
    }
    if (typeof param === 'object') {
      return JSON.stringify(param);
    }
    
    return param.toString();
  },
  
  authentications: {
    'Bearer': {type: 'bearer', accessToken: null},
    'jwtAuth': {type: 'bearer', accessToken: null}
  },
  
  applyAuthToRequest: function(request, authNames) {
    authNames.forEach((authName) => {
      const auth = this.authentications[authName];
      if (auth.type === 'bearer' && auth.accessToken) {
        request.headers = request.headers || {};
        request.headers['Authorization'] = 'Bearer ' + auth.accessToken;
      }
    });
    return request;
  }
};

// Test function
function testApiClient() {
  console.log('Testing ApiClient functionality...');
  
  // Test URL building
  const testUrl = mockApiClient.buildUrl('/api/applications/{id}', { id: 123 }, null);
  console.log('Built URL:', testUrl);
  
  // Test parameter conversion
  console.log('String param:', mockApiClient.paramToString('test'));
  console.log('Date param:', mockApiClient.paramToString(new Date()));
  console.log('Object param:', mockApiClient.paramToString({ key: 'value' }));
  
  // Test authentication methods
  mockApiClient.authentications.Bearer.accessToken = 'test-token';
  const request = { headers: {} };
  const authenticatedRequest = mockApiClient.applyAuthToRequest(request, ['Bearer']);
  console.log('Auth headers:', authenticatedRequest.headers);
  
  console.log('All tests completed!');
}

// Run the test
testApiClient();
