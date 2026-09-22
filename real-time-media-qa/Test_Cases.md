# Manual Test Cases

## Test Environment

- Operating System: Windows
- Browser: Google Chrome 153.0.8010.52
- Application: WebRTC `getUserMedia()` basic camera demo

## Test Cases
| ID | Test Scenario | Test Type | Priority | Execution Status |
|---|---|---|---|---|
| TC-001 | Allow camera permission and verify successful video initialization | Positive / Functional | High | Executed |
| TC-002 | Deny camera permission and verify failure handling | Negative / Functional | High | Executed |
| TC-003 | Retry camera initialization after permission denial | Negative / Exploratory | Medium | Executed |
| TC-004 | Rapidly click **Open Camera** before the initial media request resolves | Edge Case / Exploratory | Medium | Executed |
| TC-005 | Repeated Permission Prompt Dismissal | Exploratory / Negative / Permission Handling | Medium | Executed - Pass with Existing Defects Reproduced |
| TC-006 | Remove camera availability after a successful stream has started | Resiliency / Exploratory / State Management | High | Executed |
| TC-007 | Trigger an unsupported media-constraint condition | White-Box / Negative / Branch Coverage | Medium | Executed |
| TC-008 | Attempt camera initialization when the camera is unavailable | Negative / Resiliency | High | Executed |


---

## TC-001 - Successful Camera Initialization

**Objective:**  
Verify that the application successfully initializes and displays the camera stream when camera permission is granted.


**Preconditions:**
- WebRTC demo is accessible.
- A functioning camera is connected and available.
- Camera permission has not been blocked for the site.


**Test Steps:**
1. Open the WebRTC `getUserMedia()` camera demo.
2. Click **Open camera**.
3. When prompted for camera access, select **Allow**.
4. Observe the video area.
5. Observe the state of the **Open camera** button.
6. Observe the page for error messages.


**Expected Result:**
The camera stream initializes successfully, live video is displayed in the video area, the Open camera button becomes disabled after initialization, and no error messages are displayed on the page.


**Actual Result:**
Upon selecting Allow, the camera stream initialized successfully and live video displayed in the video area. The Open camera button remained visible and became non-interactive after initialization. No error messages appeared on the page.


**Status:**
Pass


**Evidence:**
 [Successful Camera Initialization](./evidence/TC-001_successful-camera-initialization.jpg)


**Notes:**
Usability Observation: Although the Open camera button becomes disabled after successful camera initialization, its visual appearance does not clearly indicate a disabled state.


---

## TC-002 - Camera Permission Denied

**Objective:**  
Verify that the application handles denied camera permission appropriately.


**Preconditions:**
- WebRTC demo is accessible.
- Camera permission is not permanently allowed for the site.
- Browser permission controls are available.


**Test Steps:**
1. Open the WebRTC `getUserMedia()` camera demo.
2. Click **Open camera**.
3. When prompted for camera access, select **Block** or **Don't allow**.
4. Observe the video area.
5. Observe the **Open camera** button.
6. Observe any error messages displayed on the page.


**Expected Result:**  
No video stream is displayed. The application displays an accurate error message indicating that camera permission was denied. The Open Camera control remains available for retry or provides clear guidance for restoring camera permission.


**Actual Result:**  
No camera stream appeared. The application displayed a NotAllowedError, but the message incorrectly referenced both camera and microphone permissions even though the application requests video access only. Clicking Open Camera again appended another permission error message to the page.


**Status:**  
Fail


**Evidence:**
[Camera Permission Denied](evidence/TC-002_permission-denied-error.png)


**Notes:**  
The permission-denied message states that access to both the camera and microphone was not granted. However, the current media constraints specify audio: false and video: true, so microphone access is not requested. The message should reference camera permission only. Repeated attempts after denial also append additional error messages to the page rather than replacing the existing message or providing clearer recovery guidance.


---

## TC-003 - Retry Camera Initialization After Permission Denial

**Objective:**  
Verify how the application behaves when the user attempts to initialize the camera again after previously denying camera permission.


**Preconditions:**
- WebRTC demo is accessible.
- Camera permission has been denied for the site.
- The previous permission-denied error is visible on the page.


**Test Steps:**
1. Open the WebRTC `getUserMedia()` camera demo.
2. Click **Open camera**.
3. Deny camera permission when prompted.
4. Confirm that the permission-denied error appears.
5. Click **Open camera** again without changing browser permission settings.
6. Observe the video area.
7. Observe the error-message area.
8. Observe whether the application provides any recovery instructions or additional feedback.


**Expected Result:**  
The video area remains inactive because camera permission has not been granted. When Open Camera is selected again, the application should handle the repeated failure cleanly without unnecessarily duplicating previously displayed error content. Any recovery guidance provided should accurately reflect the blocked-permission state.


**Actual Result:**  
The video area remained inactive and no camera stream was displayed. Each additional click of Open Camera appended another identical set of permission-related error messages to the page, causing the error area to continuously grow. No recovery guidance was provided for restoring camera permission.


**Status:**  
Fail - Usability Defect Candidate TC-003_duplicate-errors-after-denial.png


**Evidence:**
[Duplicate Errors](evidence/TC-003_duplicate-errors-after-denial.png)


**Notes:**  
Repeated attempts while camera permission remains blocked append duplicate NotAllowedError and generic getUserMedia error messages rather than replacing or clearing the existing error state. This creates increasing visual clutter without giving the user additional information. The application also provides no guidance for recovering from a browser-blocked permission state; this is documented as a usability observation rather than a confirmed functional requirement.


---

## TC-004 - Repeated Camera Initialization Before Permission Resolution

**Objective:**  
Determine whether a user can trigger multiple camera initialization requests before the initial `getUserMedia()` permission request is resolved.


**Preconditions:**
- WebRTC demo is accessible.
- Camera permission has not already been allowed or denied for the site.
- Browser permission prompt is available.


**Test Steps:**
1. Open the WebRTC `getUserMedia()` camera demo.
2. Click **Open camera**.
3. Before selecting an option in the browser permission prompt, attempt to interact with the **Open camera** button again.
4. Observe whether additional camera initialization requests can be triggered.
5. Observe the browser permission interface and application state.


**Expected Result:**
The application/browser should prevent multiple simultaneous camera initialization attempts while the initial permission request is unresolved. Only one active permission request should be presented to the user, and repeated initialization should not result in duplicate prompts, streams, or error states.


**Actual Result:**
Immediately after selecting Open camera, Chrome displayed its camera permission prompt. While the permission prompt was open, the underlying Open camera control could not be interacted with. As a result, additional camera initialization attempts could not be triggered through normal user interaction until the active permission request was resolved or dismissed.


**Status:**
Pass


**Notes:**
In the tested Chrome environment, the prevention of repeated initialization requests appears to be enforced by the browser permission interface rather than by the application's button state. The application itself does not disable the Open camera button until getUserMedia() successfully resolves.


---

## TC-005 - Repeated Permission Prompt Dismissal

**Objective:**  
Evaluate application behavior when the user repeatedly dismisses the browser camera-permission prompt without explicitly allowing or denying camera access.


**Preconditions:**
- WebRTC demo is accessible.
- Camera permission has not already been permanently allowed or blocked.
- Browser permission prompt is available.


**Test Steps:**
1. Open the WebRTC `getUserMedia()` camera demo.
2. Click **Open camera**.
3. When the browser permission prompt appears, close the prompt using the **X** without selecting an allow or deny option.
4. Click **Open camera** again.
5. Repeat the prompt-dismissal process multiple times.
6. Observe whether the browser continues requesting permission.
7. Observe any error messages displayed by the application.
8. Click **Open camera** again after the application begins displaying an error.


**Expected Result:**
The browser re-prompts for permissions on initial dismissals. If the browser eventually treats repeated dismissals as a denial, the failure path triggers, and the application displays a clear error message indicating camera permission was not granted. Subsequent clicks after an error state are handled cleanly without stacking duplicate messages.


**Actual Result:**
Dismissing the browser prompt via the "X" button initially allowed re-prompting on subsequent clicks.  After repeated dismissals, the browser stopped prompting and returned NotAllowedError, which the application caught and displayed on-screen. Once the error state was reached, clicking "Open Camera" repeatedly resulted in stacked, duplicate error messages. The error message incorrectly referenced microphone permissions alongside camera permissions.


**Status:**
Pass with Existing Defects Reproduced


**Notes:**
In the tested Chrome environment, repeated permission-prompt dismissals eventually resulted in NotAllowedError and the browser stopped presenting additional permission prompts. This behavior appears to be browser-controlled. Error message continues to state that microphone permissions were not granted, even though only camera access was requested. Repeatedly clicking "Open Camera" after the browser suppresses prompts continuously produces NotAllowedError blocks to the DOM via innerHTML +=.


---

## TC-006 - Camera Becomes Unavailable After Successful Initialization

**Objective:**  
Evaluate how the application responds when an active camera device becomes unavailable after the video stream has already initialized successfully.


**Preconditions:**
- WebRTC demo is accessible.
- System camera is enabled and functioning.
- Browser camera permission is allowed.
- No previous error state is present on the page.


**Test Steps:**
1. Open the WebRTC `getUserMedia()` camera demo.
2. Click **Open camera**.
3. Allow camera access if prompted.
4. Confirm that the live video stream initializes successfully.
5. Confirm that the **Open camera** button becomes non-interactive.
6. While the stream is active, open Windows **Device Manager**.
7. Expand **Cameras**.
8. Right-click the active camera and select **Disable device**.
9. Return to the WebRTC demo.
10. Observe the video area.
11. Observe the page for any error messages, warnings, or state changes.
12. Observe the **Open camera** button.
13. Wait approximately 10–15 seconds and continue observing the page.
14. Re-enable the camera in Device Manager.
15. Return to the demo and observe whether the stream automatically recovers.
16. If it does not recover, refresh the page and determine whether camera functionality can be restored.


**Expected Result:**  
If the active camera becomes unavailable during an initialized stream, the video should stop rendering and the application should clearly indicate that the media stream has been interrupted. The UI should transition out of the successful state and provide a usable recovery path, such as re-enabling the Open Camera control or otherwise allowing the camera to be reinitialized. After camera availability is restored, the stream should be recoverable through a clear retry or page reload without leaving the interface in an inconsistent state.


**Actual Result:**  
When the camera was disabled during an active stream, the live video immediately changed to a solid black display. No error message, warning, or status change appeared automatically. The Open Camera button remained non-interactive, preventing a retry through the application UI.
After manually refreshing the page while the camera remained disabled, the application displayed getUserMedia error: NotReadableError. Repeatedly clicking Open Camera in this state appended duplicate NotReadableError messages to the page.
After the camera was re-enabled in Device Manager, the active stream did not automatically recover. Multiple page reloads were required before camera initialization succeeded again. During part of the recovery process, Chrome displayed camera-use indicators while the application continued to report NotReadableError.


**Status:**  
Fail


**Evidence:**
[Black stream after camera interruption](evidence/TC-006_black-stream-after-camera-disabled.png)
[NotReadableError after page refresh](evidence/TC-006_notreadable-error-after-refresh.png)
[Recovery failure with active camera indicators](evidence/TC-006_notreadable-error-with-active-camera-indicators.jpg)


**Notes:**  
Exact Error: getUserMedia error: NotReadableError
Initial Mid-Stream Behavior: No application error path was triggered because the reviewed implementation only handles failures during the original getUserMedia() request and does not explicitly handle an already-active media track becoming unavailable.
Post-Refresh Path: handleError() → Generic/Other error path (NotReadableError)
BUG-002 Reproduced: Repeated retries during the NotReadableError state appended duplicate error messages to the existing error container.
Recovery Observation: After restoring the camera device, browser/device state did not immediately return to normal. Camera-use indicators remained visible during part of the recovery process even while getUserMedia() continued returning NotReadableError. Because this behavior may involve Chrome or operating-system device state, it is documented as an environment/recovery observation rather than attributed solely to the application.


---

## TC-007 - Unsupported Media Constraint Condition

**Objective:**  
Verify that the application correctly handles an `OverconstrainedError` when the requested camera constraints cannot be satisfied by the available hardware.


**Preconditions:**
- WebRTC demo is accessible.
- Camera is enabled and functioning.
- Browser camera permission is available.
- Chrome DevTools is accessible.
- The application is using the default `window.constraints` object.


**Test Steps:**
1. Open the WebRTC `getUserMedia()` camera demo.
2. Open Chrome DevTools.
3. Select the **Console** tab.
4. Modify the video constraints to request an unsupported exact resolution.
5. Return to the application.
6. Click **Open camera**.
7. Observe the video area.
8. Observe any error messages displayed.
9. Observe the state of the **Open camera** button.
10. Restore the original video constraint after testing.


**Expected Result:**  
No camera stream initializes, and the video area remains blank. The application catches the constraint failure and displays a specific, user-friendly error message stating that the requested video resolution or settings are not supported by the hardware. The "Open Camera" button remains usable so that the user can retry once valid constraints are set. Restoring valid media constraints allows the application to successfully request permissions and initialize the video stream without requiring a page reload.


**Actual Result:**  
The video area remained blank and no stream rendered when requesting `99999x99999` resolution. The page displayed a specific error message identifying the unsatisfied constraints: `OverconstrainedError: The constraints could not be satisfied by the available devices. Constraints: {"audio":false,"video":{"width":{"exact":99999},"height":{"exact":99999}}}` alongside `getUserMedia error: OverconstrainedError`. After valid constraints were restored, selecting Open Camera and allowing camera access successfully initialized the live video stream. However, the previous OverconstrainedError and generic getUserMedia error: OverconstrainedError messages remained visible beneath the active video stream and were not cleared after successful recovery.


**Status:**  
Fail - OverconstrainedError branch handled successfully, but stale error state remained after successful recovery.


**Evidence:**
[Recovery failure with active camera indicators](evidence/TC-006_notreadable-error-with-active-camera-indicators.jpg)


**Notes:**  
Exact Error Text: `OverconstrainedError: The constraints could not be satisfied by the available devices. Constraints: {"audio":false,"video":{"width":{"exact":99999},"height":{"exact":99999}}}`
Flowchart Path Exercised: handleError() → OverconstrainedError specific branch → generic error output
Recovery Defect: Successful camera initialization does not clear errors generated by previous failed attempts. This results in a contradictory UI state where the application simultaneously displays a functioning live stream and an error indicating that camera initialization failed.


---

## TC-008 - Camera Unavailable at Initialization

**Objective:**  
Verify how the application handles camera initialization when no usable camera device is available.


**Preconditions:**
- WebRTC demo is accessible.
- Browser camera permission is allowed or available to request.
- The system camera can be temporarily disabled.


**Test Steps:**
1. Close or refresh the WebRTC demo so no camera stream is active.
2. Temporarily disable the system camera.
3. Return to the WebRTC `getUserMedia()` demo.
4. Click **Open camera**.
5. Allow camera permission if the browser prompts for it.
6. Observe the video area.
7. Observe any error messages displayed.
8. Observe the state of the **Open camera** button.
9. Re-enable the camera after testing.


**Expected Result:**  
No video stream initializes and the video area remains inactive. The application handles the unavailable-camera condition without crashing and displays an error indicating that no usable camera device is available. The Open Camera button remains available so the user can retry after restoring camera availability. Repeated retries should not unnecessarily duplicate previously displayed error content.


**Actual Result:**  
The video area remained inactive and no video stream was rendered. The application handled the failure through its generic error path and displayed getUserMedia error: NotFoundError. Refreshing the page and resetting browser permissions did not change the result while the system camera remained disabled. Repeatedly clicking Open Camera caused identical NotFoundError messages to accumulate vertically on the page.


**Status:**  
Pass with Existing Defect Reproduced + Usability Observation


**Notes:**  
Exact Error: getUserMedia error: NotFoundError
Execution Path: handleError() → fallback/generic error path
BUG-002 Reproduced: Repeated retries append duplicate error messages because new <p> elements are added to the existing error container.
Usability Observation: The application exposes the raw browser/API error name NotFoundError rather than presenting a user-oriented explanation that no available camera device could be found.
