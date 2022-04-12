# Changelog

## [2021.4.11]

### Added

- `data_management` module
- `restful_service` sumbodule which initializes restful service based on a dictionary or existing resources
- `resource_factory` submodule which creates resources based on a template dictionary
- `error_handling` submodule to abort curl operations on anticipated fail states
- `template` submodule which contains template for `chats`, `devices`, and `users`
- `class_utils` submodule in `utils` module which enables copying and renaming class definitions

## [2021.2.22]

### Added

- passthroughs `create_from_data` and `fully_augmented` allow creation of variably populated `DeviceInterface` instances
- factory `get_device_reader`, `_read_from_file`, and `_read_from_dict` allow flexibility of input types

### Changed

- all functions converted from classmethods to internal methods
- `__init__` function changed to a bare-bones passthrough
- `check_data_format` renamed to `_check_data`, split into `_check_data_fields` and `check_data_mac`
- `_check` methods now throw exceptions instead of returning booleans
- `read_from_device` renamed to `_read_device_data`, now calls on reading factory methods

## [2021.2.17]

### Added

- module `utils` will now hold wide-use case functions

### Changed

- migrated `check_file` method from `device` to `utils`, generalized to any file format

## [2021.2.15]

### Added

- `device` module and component class `device_interface`
