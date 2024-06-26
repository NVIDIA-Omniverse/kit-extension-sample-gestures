# UI Gestures Extension Sample

![previewImage](data/gestures.gif)

## [UI Gestures for omni.ui (omni.example.gesture_window)](exts/omni.example.gesture_window)

![windowPreview](data/gesturewindow_prev.gif)

### About
This extension shows how to create gestures using omni.ui. The focus of this sample extension is to show how to register and create a scene view within a Window.


### [README](exts/omni.example.gesture_window)
See the [README for this extension](exts/omni.example.gesture_window) to learn more about it including how to use it.

## [UI Gestures for Viewport (omni.example.gesture_viewport)](exts/omni.example.gesture_viewport)

![viewportPreview](data/gestureviewport_prev.gif)

### About
This extension shows how to create a simple manipulator with gestures using omni.ui.scene. The focus of this sample extension is to show how to create a simple manipulator and register gestures in the viewport.


### [README](exts/omni.example.gesture_viewport)
See the [README for this extension](exts/omni.example.gesture_viewport) to learn more about it including how to use it.

## [Tutorial](docs/tutorial.md)
Follow a [step-by-step tutorial](docs/tutorial.md) that walks you through how to use omni.ui.scene to build this extension.

## Adding This Extension

To add this extension to your app:

1. Download or Clone the extension, unzip the file if downloaded

2. Create a New Extension

> **NOTE:** This sample has TWO extensions. You will need to repeat the process for both.

**Linux:**
```bash
./repo.sh template new
```

**Windows:**
```powershell
.\repo.bat template new
```

3a. `gesture_viewport` Follow the prompt instructions:
- **? Select with arrow keys what you want to create:** Extension
- **? Select with arrow keys your desired template:**: Python UI Extension
- **? Enter name of extension [name-spaced, lowercase, alphanumeric]:**: omni.example.gesture_viewport
- **? Enter extension_display_name:**: Gesture Viewport
- **? Enter version:**: 0.1.0

3b. `gesture_window` Follow the prompt instructions:
- **? Select with arrow keys what you want to create:** Extension
- **? Select with arrow keys your desired template:**: Python UI Extension
- **? Enter name of extension [name-spaced, lowercase, alphanumeric]:**: omni.example.gesture_window
- **? Enter extension_display_name:**: Gesture Window
- **? Enter version:**: 0.1.0

4. Add the Extension to an Application

In the newly created extension, **copy and paste** the `omni.example.spawn_prims` folder that was cloned into `kit-app-template/sources/extensions/omni.example.gesture_viewport` and `kit-app-template/sources/extensions/omni.example.gesture_window`.

You will be prompted if you want to replace files, **select** `Replace All`.

To add your extension to an application, declare it in the dependencies section of the application's `.kit` file:

```toml
[dependencies]
"omni.example.gesture_viewport" = {}
"omni.example.gesture_window" = {}
```

5. Build with New Extensions
After a new extension has been added to the `.kit` file, the application should be rebuilt to ensure extensions are populated to the build directory.

**Linux:**
```bash
./repo.sh build
```

**Windows:**
```powershell
.\repo.bat build
```

## Contributing
The source code for this repository is provided as-is and we are not accepting outside contributions.