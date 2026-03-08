# Zoom Auto Scheduler v1.0.1

## Bug Fixes

- Fixed next-upcoming schedule highlighting becoming incorrect over time.
- Optimized next-upcoming highlight updates to refresh only affected rows instead of rebuilding the entire table.
- Fixed checkbox visibility issue in the first column when highlighting the next-upcoming row.
- Fixed inconsistent text color for highlighted/selected rows across different Windows machines and themes.
- Fixed intermittent "text disappears until clicked" issue by enforcing explicit table item foreground colors.

## Data Safety

- User data remains stored in `%LOCALAPPDATA%\ZoomAuto\`:
  - `zoom_schedule.json`
  - `settings.json`

Updating from v1.0.0 to v1.0.1 does not delete these files.
