# Defect Reports

## Test Environment

- Operating System: Windows
- Browser: Google Chrome 153.0.8010.52
- Application: WebRTC `getUserMedia()` basic camera demo


---

## BUG-001 - Permission Denial Error Incorrectly References Microphone Access

**Defect Type:** Error Message / Content  
**Severity:** Low  
**Priority:** Medium  
**Status:** Open  
**Reproducibility:** 100%

### Description

When camera permission is denied, the application displays an error message stating that permission was not granted for both the camera and microphone.

However, the current `getUserMedia()` configuration requests video access only (`video: true`) and explicitly disables audio access (`audio: false`).

As a result, the displayed message incorrectly references microphone permission.

### Preconditions

- WebRTC `getUserMedia()` demo is accessible.
- Camera permission has not already been permanently allowed.
- Browser permission controls are available.

### Steps to Reproduce

1. Open the WebRTC `getUserMedia()` camera demo.
2. Click **Open camera**.
3. Deny camera permission when prompted.
4. Observe the error message displayed on the page.

### Expected Result

The application should display an error message accurately stating that camera permission was not granted.

### Actual Result

The application displays:

`NotAllowedError: Permissions have not been granted to use your camera and microphone, you need to allow the page access to your devices in order for the demo to work.`

The message incorrectly references microphone permission even though audio access is not requested.

### Technical Observation

The media constraints specify:

`audio: false`  
`video: true`

The permission-denied error message therefore does not accurately reflect the resources requested by the application.

### Evidence

- [Incorrect microphone reference](evidence/TC-002_permission-denied-error.png)

### Related Test Case:

- TC-002 - [Camera Permission Denied]([./Test_Cases.md](https://github.com/IrmaniB/QA-Testing-Portfolio/blob/main/real-time-media-qa/Test_Cases.md#tc-002---camera-permission-denied))


---

## BUG-002 - Repeated Camera Requests Append Duplicate Error Messages After Permission Denial

**Defect Type:** Usability / Error Handling  
**Severity:** Low  
**Priority:** Low-Medium  
**Status:** Open  
**Reproducibility:** 100%

### Description

When camera permission has been denied, repeatedly selecting **Open camera** appends additional identical error messages to the existing error area.

The application does not clear or replace the previous error state before displaying the new failure message, causing duplicate error content to accumulate on the page.

### Preconditions

- WebRTC `getUserMedia()` demo is accessible.
- Camera permission has been denied or the browser is returning `NotAllowedError`.
- The **Open camera** button remains available.

### Steps to Reproduce

1. Open the WebRTC `getUserMedia()` camera demo.
2. Click **Open camera**.
3. Deny camera permission.
4. Confirm that the permission error appears.
5. Click **Open camera** repeatedly.
6. Observe the error-message area.

### Expected Result

Repeated camera initialization attempts should be handled without unnecessarily duplicating previously displayed error content.

The application should maintain a clear and readable error state.

### Actual Result

Each additional click of **Open camera** appends another identical set of error messages to the page.

The error area continues to grow with repeated:

`NotAllowedError...`

and

`getUserMedia error: NotAllowedError`

messages.

### Technical Observation

The error display logic appends new content to the existing error container using:

`errorElement.innerHTML += ...`

This causes each failure message to remain in the DOM while subsequent errors are added beneath it.

### User Impact

Repeated failures create increasing visual clutter and make the error state harder to read without providing additional useful information.

### Evidence

- [Duplicate errors after permission denial](evidence/TC-003_duplicate-errors-after-denial.png)
- [Duplicate NotReadableError messages during recovery](evidence/TC-006_notreadable-error-with-active-camera-indicators.png)

### Related Test Case:

- TC-003 - [Retry Camera Initialization After Permission Denial](./test_cases.md), TC-005 - [Repeated Permission Prompt Dismissal](./test_cases.md)


---

## BUG-003 - Camera Interruption Is Not Detected After Successful Stream Initialization

**Defect Type:** Resiliency / State Management  
**Severity:** Medium  
**Suggested Priority:** Medium  
**Status:** Open  
**Reproducibility:** Reproduced in tested environment

### Description

When the active camera device becomes unavailable after a video stream has already initialized successfully, the application does not detect or communicate the interruption.

The video display changes to a black screen, but no error message, warning, or status update appears. The **Open camera** button remains disabled, leaving the user without an in-application method to retry camera initialization.

### Preconditions

- WebRTC `getUserMedia()` demo is accessible.
- Camera is enabled and functioning.
- Camera permission is granted.
- Live video stream has initialized successfully.

### Steps to Reproduce

1. Open the WebRTC `getUserMedia()` camera demo.
2. Click **Open camera**.
3. Allow camera access.
4. Confirm that the live camera stream is displayed.
5. While the stream is active, open Windows Device Manager.
6. Disable the active camera device.
7. Return to the WebRTC demo.
8. Observe the video area.
9. Observe the page for error messages or state changes.
10. Attempt to click **Open camera**.

### Expected Result

When the active camera becomes unavailable, the application should detect the media interruption and clearly indicate that the stream has been lost.

The UI should leave the successful state and provide a usable recovery path, such as re-enabling the **Open camera** control or allowing the user to retry initialization.

### Actual Result

The active video immediately changed to a solid black display.

No error message, warning, or state notification appeared.

The **Open camera** button remained disabled and non-interactive, preventing the user from attempting to reinitialize the camera without refreshing the page.

### Technical Observation

The reviewed implementation handles errors generated during the initial `getUserMedia()` request, but no explicit handling was identified for an already-active media track becoming unavailable after successful initialization.

Because the original `getUserMedia()` call had already resolved successfully, disabling the camera did not route through `handleError()`.

After refreshing the page while the camera remained unavailable, the browser returned:

`getUserMedia error: NotReadableError`

### User Impact

A user may remain in an apparently successful application state even though the active video stream has been lost.

The lack of interruption feedback and retry controls can leave the user unable to recover without manually refreshing the page.

### Related Observations

- BUG-002 was reproduced after refreshing into the `NotReadableError` state because repeated retries appended duplicate error messages.
- After re-enabling the camera device, recovery required multiple page reloads in the tested environment.
- Browser camera-use indicators remained active during part of the recovery process even while the application continued reporting `NotReadableError`. This behavior is documented as an environment/browser recovery observation rather than attributed solely to the application.

### Evidence

- [Black stream after camera interruption](evidence/TC-006_camera-disabled-black-stream.png)
- [NotReadableError after page refresh](evidence/TC-006_notreadable-error-after-refresh.png)
- [Recovery failure with active camera indicators](evidence/TC-006_notreadable-error-stacking-recovery-state.png)

### Related Test Case:

- TC-006 - [Camera Becomes Unavailable After Successful Initialization](./test_cases.md)


---

## BUG-004 - Stale Camera Error Remains Visible After Successful Recovery

**Defect Type:** State Management / Error Handling  
**Severity:** Low-Medium  
**Suggested Priority:** Medium  
**Status:** Open  
**Reproducibility:** 100% in tested scenario

### Description

After a camera initialization attempt fails with `OverconstrainedError`, successfully restoring valid media constraints and initializing the camera does not clear the previous error messages from the page.

As a result, the application displays a functioning live camera stream while simultaneously showing an error indicating that camera initialization failed.

### Preconditions

- WebRTC `getUserMedia()` demo is accessible.
- Camera is enabled and functioning.
- Browser camera permission is available.
- Media constraints can be modified through Chrome DevTools.

### Steps to Reproduce

1. Open the WebRTC `getUserMedia()` camera demo.
2. Set unsupported exact video constraints:

   `width: 99999`
   
   `height: 99999`

3. Click **Open camera**.
4. Confirm that `OverconstrainedError` appears.
5. Restore the video constraint to:

   `window.constraints.video = true`

6. Click **Open camera** again.
7. Allow camera permission.
8. Observe the active video stream.
9. Observe the existing error-message area.

### Expected Result

After the camera initializes successfully, errors associated with the previous failed initialization attempt should be cleared or otherwise marked as no longer active.

The UI should accurately reflect the application's current successful state.

### Actual Result

The camera successfully initializes and displays a live video stream.

However, the previous:

`OverconstrainedError`

and

`getUserMedia error: OverconstrainedError`

messages remain visible below the active stream.

### Technical Observation

The reviewed `handleSuccess()` implementation initializes the media stream and disables the Open Camera button but does not clear the existing `#errorMsg` contents.

Errors previously added through `errorMsg()` therefore remain in the DOM after successful recovery.

### User Impact

The interface presents contradictory information by displaying both:

- a functioning live camera stream
- an error indicating that camera initialization failed

This may confuse users about whether the current camera session is functioning correctly.

### Evidence

- [Successful camera stream with stale error still displayed](evidence/TC-007_successful-recovery-with-stale-error.png)

### Related Test Case:

- TC-007 - [Unsupported Media Constraint Condition](./test_cases.md)
