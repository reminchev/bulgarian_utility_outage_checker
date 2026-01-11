<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->
## 1.3.1

- 🐛 Fixed binary sensor template syntax
- ✅ Changed from `states.sensor.x.attributes.y` to `state_attr()` function
- 📈 Improved template reliability and compatibility
- 📝 Added details attribute to binary sensor

## 1.2.0

- ⚡ Updated to modern Home Assistant template syntax
- 🔧 Fixed legacy binary_sensor template deprecation warning
- ✨ Added attributes to binary sensor (outage_type, last_check)
- 📝 Improved configuration generation
## 1.1.4

- Use only Alpine packages (no pip) for maximum stability
- Simplified Dockerfile for reliable builds
- All dependencies from system repositories

## 1.1.3

- Fix beautifulsoup4 installation issue
- Install lxml via apk for better compatibility
- Remove pip install fallback that was masking errors

## 1.1.2

- Fix build issues with Dockerfile
- Optimize Python package installation
- Add .gitattributes for proper line endings
- Simplify config metadata to avoid encoding issues

## 1.1.1

- Fixed Dockerfile build issues
- Improved Python package installation
- Optimized dependencies

## 1.1.0

- ✨ Added auto-generated configuration file for easy setup
- ✨ JSON status export for Home Assistant sensors integration
- 📝 Comprehensive usage documentation in README
- 🎨 Custom logo and icon with Bulgarian map
- 🌐 Full bilingual support (Bulgarian/English)
- 🔧 Dashboard integration with ready-to-use examples
- 📊 Binary sensor for outage detection
- 🔄 Automatic configuration snippet generation

## 1.0.0

- Initial release
- Basic outage checking from ERM West
- Configurable check interval
- Support for custom identifiers



