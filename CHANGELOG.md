# CHANGELOG

## [1.1.2] - 2026-10-16
- Removed TubePlayer Lite configuration, media browser entries, API support, and `play_id` service.
- Added a selectable `Korea Radio` LLM API provider with the `korea_radio` tool.
- Added migration to remove the obsolete TubePlayer port from existing config entries.
- Raised the minimum supported Home Assistant version to 2026.10.0.
- Added connection validation, duplicate server prevention, and HACS brand metadata.
- Added an optional player-reachable playback host for media browser, service, and Assist playback.
- Marked radio items with their resolved `audio/mpeg` MIME type for media-player compatibility filtering.

## [1.1.1] - 2026-05-19
- Optimized HTTP ClientSession to mitigate connection leaks.
- Cached `RadioEndpointManager` API client in `hass.data` to prevent duplicate lookups.
- Realigned folder layout to comply with HACS integration standards.
- Integrated with TubePlayer Lite (v1.1.0).
- Added `play_id` service for YouTube alias playback.
- Separated endpoints for Radio (3005) and Tube (4005).
- Enhanced Media Browser with Category support (Radio/Tube).
- Fixed playback issue by specifying `audio/mpeg` mime-type.
- Restored `MediaClass.MUSIC` and aligned root to HA Official Radio Browser standards.
- Added `async_step_reconfigure` config flow for easier system adjustments.
