# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature for detecting table renames
- Support for analyzing views and materialized views

### Changed
- Improved performance of query analysis by 20%
- Refactored codebase to improve modularity and testability

### Fixed
- Fixed a bug that caused incorrect column mappings in certain scenarios
- Resolved an issue with handling large schemas

## [1.0.0] - 2023-06-08

### Added
- Initial release of Schema Evolution Analyzer
- Support for detecting schema evolution patterns
- Integration with PostgreSQL storage backend
- Prometheus metrics for monitoring
- Comprehensive test suite