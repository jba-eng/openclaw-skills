# Changelog

All notable changes to the Spec Coding skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-21

### Added
- Initial release of spec-coding skill
- Sequential task execution engine
- Python utilities for token-efficient operations:
  - `task_manager.py` - Task state management and discovery
  - `task_validator.py` - done_when condition validation
- Strict workflow with 7 stages
- State tracking (planned → in_progress → done)
- User approval workflow at each stage
- Spec file protection (never modifies spec.md or design.md)
- Integration with spec-creation skill

### Features
- Smart project discovery with spec verification
- Automatic task parsing from tasks.md
- done_when condition validation
- Progress tracking and statistics
- Token savings of 30-40% per task
- Diff display before all writes

### Documentation
- Complete README with usage examples
- CHANGELOG for version tracking
- Publishing checklist for ClawHub
- Inline documentation in all Python scripts

---

## Future Enhancements

Planned for future versions:
- Automated test execution and reporting
- Rollback capability for failed tasks
- Task dependency validation
- Parallel task execution (when dependencies allow)
- Integration with CI/CD pipelines
- Task time tracking and estimation
