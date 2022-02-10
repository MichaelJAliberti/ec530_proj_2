# ec530_proj_2

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
