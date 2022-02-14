# ec530_proj_2

## Branching Strategy

All branches created should correspond to and fulfill the requirements of a specific Github Issue. 
Issues should identify a feature to add or a bug to be resolved.

Before merging to main, a branch must include the implementation of the desired feature as well as a corresponding test.
If a branch includes modifications to code in the `/src` directory, these changes should be documented in `changelog.md`

## API Schema

*User Tables:*
```
# UserInfo:
{
  UserID: 
  Email:
  Weight: {on registration}
  Height: {on registration}
  Gender:
  PrimaryContact:
  SecondaryContact:
  DoB: 
}


# BillingInfo: (could be combined with UserInfo?)
{
  MedicalCare: 
  Address: 
  PrimaryCare:
  Insurance:
  InsuranceGroupID:
  BillingInfo:
}

# AccessLevel:
{
  UserID: (int)
  Patient: (bool)
  Doctor: (bool)
  Admin: (bool)
}

# Perscription:
{
  UserID:
  Medicine:
  Dosage:
  StartTime:
  StopTime:
}

# Measurements:
{
  UserID:
  DeviceID:
  Height:
  Weight:
  MeasuermentType:
  MeasurementValue:
  Date: (datetime)
}

# MedicalHistory:
{
  UserID:
  Incidents:
}
```

*device tables:*
```
# Devices:
{
  DeviceID:
  DeviceType:
  DateOfPurchase:
  MacAddress:
  CurrentAssignee:
  CurrentFirware:
}

# OwnershipChanges:
{
  DeviceID:
  Assignee:
  Assigner:
  Date:
}

# FirmwareChanges:
{
  DeviceID:
  PreviousFirware:
  NewFirmware:
  Date:
}
```
