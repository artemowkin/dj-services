# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.x] - 2020-01-06

### Deleted

- `FormsCRUDStrategy`
- `FormsMixin`
- `CRUDService`
- Views

### Changed

- Forms API is no longer used in services strategies
- Services and strategies are no longer had `form` and `change_form` attributes

### Added

- `CommonCRUDStrategy` - strategy with simple common CRUD functionality
- `UserCRUDStrategy` - strategy with CRUD functionality using user
- `get_user_kwarg` method in `UserCRUDStrategy`

## [1.1.x] - 2020-11-25

### Added

- Mixin with create/update functionality for CRUD strategies - `FormsMixin`
- Added `change_form` attribute to the `CRUDService` and `FormsCRUDStrategy`

## [1.0.0] - 2020-11-09

### Added

- Base class for CRUD strategies - `BaseCRUDStrategy`
- Base class for CRUD services - `BaseCRUDService`

### Changed

- Renamed `SimpleCRUDStrategy` to `FormsCRUDStrategy`

## [0.2.0] - 2020-11-01

First stable release

### Added

- Extended parameters functionality in `SimpleCRUDStrategy`

## [0.1.3] - 2020-10-21

### Fixed

- Version of setuptools

## [0.1.2] - 2020-10-21

### Fixed

- Problems in setup.py

## [0.1.1] - 2020-10-21

### Fixed

- Some issues

## [0.1.0] - 2020-10-21

### Added

#### Services

- BaseService
- CRUDService

#### Strategies

- BaseStrategy
- SimpleCRUDStrategy
