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
| TC-003 | Retry camera initialization after permission denial | Negative / Exploratory | Medium | Partially Executed |
| TC-004 | Rapidly click **Open Camera** before the initial media request resolves | Edge Case / Exploratory | Medium | Not Executed |
| TC-005 | Attempt camera initialization when the camera is unavailable | Negative / Resiliency | High | Not Executed |
| TC-006 | Remove camera availability after a successful stream has started | Resiliency / Exploratory | Medium | Not Executed |
| TC-007 | Trigger an unsupported media-constraint condition | White-Box / Branch Coverage | Medium | Design Only |

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
[Add screenshot if applicable]

**Notes:**
Usability Observation: Although the Open camera button becomes disabled after successful camera initialization, its visual appearance does not clearly indicate a disabled state.


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
[Add screenshot if applicable]

**Notes:**  
The permission-denied message states that access to both the camera and microphone was not granted. However, the current media constraints specify audio: false and video: true, so microphone access is not requested. The message should reference camera permission only. Repeated attempts after denial also append additional error messages to the page rather than replacing the existing message or providing clearer recovery guidance.
