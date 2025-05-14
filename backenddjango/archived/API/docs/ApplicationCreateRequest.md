# CrmClientJs.ApplicationCreateRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**referenceNumber** | **String** |  | [optional] 
**loanAmount** | **Number** |  | [optional] 
**loanTerm** | **Number** | Loan term in months | [optional] 
**interestRate** | **Number** |  | [optional] 
**purpose** | **String** |  | [optional] 
**repaymentFrequency** | [**RepaymentFrequencyEnum**](RepaymentFrequencyEnum.md) |  | [optional] 
**applicationType** | [**ApplicationCreateApplicationType**](ApplicationCreateApplicationType.md) |  | [optional] 
**productId** | **String** |  | [optional] 
**estimatedSettlementDate** | **Date** |  | [optional] 
**stage** | [**StageEnum**](StageEnum.md) |  | [optional] 
**borrowers** | [**[BorrowerRequest]**](BorrowerRequest.md) |  | [optional] 
**guarantors** | [**[GuarantorRequest]**](GuarantorRequest.md) |  | [optional] 
**companyBorrowers** | [**[CompanyBorrowerRequest]**](CompanyBorrowerRequest.md) |  | [optional] 
**securityAddress** | **String** |  | [optional] 
**securityType** | **String** |  | [optional] 
**securityValue** | **Number** |  | [optional] 
**valuerCompanyName** | **String** |  | [optional] 
**valuerContactName** | **String** |  | [optional] 
**valuerPhone** | **String** |  | [optional] 
**valuerEmail** | **String** |  | [optional] 
**qsCompanyName** | **String** |  | [optional] 
**qsContactName** | **String** |  | [optional] 
**qsPhone** | **String** |  | [optional] 
**qsEmail** | **String** |  | [optional] 
**fundingCalculationInput** | [**FundingCalculationInputRequest**](FundingCalculationInputRequest.md) |  | [optional] 


