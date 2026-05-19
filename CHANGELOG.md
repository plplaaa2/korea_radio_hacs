# CHANGELOG

## [1.1.3] - 2026-05-19
- Optimized HTTP ClientSession to mitigate connection leaks.
- Cached `RadioEndpointManager` API client in `hass.data` to prevent duplicate lookups.
- Realigned folder layout to comply with HACS integration standards.

## [1.1.2] - 2026-05-05
- Integrated with TubePlayer Lite (v1.1.0).
- Added `play_id` service for YouTube alias playback.
- Separated endpoints for Radio (3005) and Tube (4005).
- Enhanced Media Browser with Category support (Radio/Tube).

## [1.1.1-dev] - 2026-04-28
- Applied HA Official Radio Browser standards for maximum compatibility.
- Fixed playback issue by specifying `audio/mpeg` mime-type.
- Restored `MediaClass.MUSIC` for better browser compatibility.
- Removed incorrect media_source platform forwarding in `__init__.py`.
- Fixed `ImportError` for `ConfigEntryState` and `AttributeError` for setup deprecation.
- Added `async_step_reconfigure` to `config_flow.py` and improved OptionsFlow.
