## 🎉 Zoom Auto Scheduler v0.1.3

### ✨ New Features & Improvements

#### UI/UX Enhancements
- ✅ Menu "Trợ giúp" renamed to "Menu" for better clarity
- ✅ Column header "Giờ" renamed to "THỜI GIAN"
- ✅ Fixed tooltip display (dark background with white text)
- ✅ Improved calendar widget styling in custom recurrence dialog
- ✅ Enhanced spinbox buttons for time adjustment
- ✅ Better context menu styling with clear background colors

#### Meeting ID Management
- ✅ Support for both 10 and 11-digit Meeting IDs
  - 10 digits: `723 543 0618` (3-3-4 format)
  - 11 digits: `873 9908 0624` (3-4-4 format)
- ✅ Auto-trim whitespace from Meeting ID input
- ✅ Flexible input without strict length limits

#### Schedule Improvements
- ✅ Default time set to current time + 1 hour when creating new schedule
- ✅ Duplicate schedule detection
  - Prevents creating 2 schedules for same Zoom room at same time
  - Checks both Meeting ID and Zoom Link
  - Clear warning message with existing schedule details

#### Installation
- ✅ **Desktop shortcut creation now enabled by default**
- ✅ **Startup task (run on Windows boot) now enabled by default**
- Users can uncheck these options during installation if not needed

### 🔧 Technical Details
- Enhanced validation for Meeting ID input
- Improved duplicate detection algorithm
- Better time calculation for default schedule creation
- Refined UI styling with cyan/blue theme consistency

### 📦 Installation
Run `ZoomAuto-Setup-0.1.3.exe` and follow the installer wizard.

### 🗂️ Data Location
- User data: `%LOCALAPPDATA%\ZoomAuto\zoom_schedule.json`
- Installation: `%LOCALAPPDATA%\Programs\ZoomAuto`

### 🛠️ Uninstall
Use Windows Settings → Apps or the uninstaller in Start Menu.

### 📊 Release Info
- Build date: January 22, 2026
- Previous version: 0.1.2
- Changelog: See features above
- SHA256: 56ABB158CC410887360A282F77424D84EE1692C7748EFFDBED1697D3F25E182A

---

**All changes tested and working. Ready for production use!** ✅
