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

- Screenshot: `[add screenshot filename here]`
- Related Test Case: TC-002


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

- Screenshot: `[add BUG-002 screenshot filename here]`
- Related Test Cases: TC-003, TC-005
