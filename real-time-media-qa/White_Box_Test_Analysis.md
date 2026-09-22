# White-Box Test Analysis

## Overview

This analysis documents source-informed testing performed against the WebRTC `getUserMedia()` basic camera demo.

The application's JavaScript source was reviewed to identify execution paths, conditional error handling, asynchronous behavior, and implementation details that could influence test design.

The goal was to use knowledge of the internal implementation to create targeted manual test scenarios rather than relying only on externally visible behavior.

---

## Source Reviewed

Primary JavaScript component reviewed:

`src/content/getusermedia/gum/js/main.js`

The implementation contains logic for:

- Requesting camera access through `navigator.mediaDevices.getUserMedia()`
- Handling successful media initialization
- Handling permission and media-related errors
- Displaying errors in the page
- Disabling the camera initialization control after successful startup

---

## Media Constraints

The application currently requests:

```javascript
const constraints = {
  audio: false,
  video: true
};


QA Observation
The application requests camera/video access only.
Microphone access is explicitly disabled.
This implementation detail was used when validating permission-related error messages and resulted in the identification of BUG-001.

Primary Execution Flow
Open Camera selected
        |
        v
navigator.mediaDevices.getUserMedia()
        |
        +------------------------+
        |                        |
     SUCCESS                  FAILURE
        |                        |
        v                        v
 handleSuccess()            handleError()
        |                        |
        |             +----------+----------+
        |             |          |          |
        |      Overconstrained  NotAllowed  Other
        |          Error          Error      Error
        |             |            |          |
        v             v            v          v
Video stream     Specific msg  Specific msg  Generic msg
displayed              \          /
Button disabled         +---- Generic msg

```

## Execution Path Analysis

**Path 1 - Successful Camera Initialization**
Relevant Logic
The application waits for getUserMedia() to resolve successfully and then calls handleSuccess().
After successful initialization:
- The returned media stream is assigned to the video element.
- The stream becomes available through window.stream.
- The Open camera button is disabled.
Test Derived From Source Review
TC-001 - Successful Camera Initialization
Result
Pass
Camera access was granted, the video stream initialized successfully, the camera feed appeared, and the Open Camera control became non-interactive.
Additional Observation
Although the button becomes disabled, its visual appearance does not strongly communicate its disabled state.

---

**Path 2 - Permission Denied / NotAllowedError**
Relevant Logic
The error handler checks whether:
error.name === 'NotAllowedError'
When this condition is met, the application displays a permission-specific message.
After the conditional logic completes, the application also displays the generic error:
getUserMedia error: NotAllowedError
Test Derived From Source Review
TC-002 - Camera Permission Denied
Result
Fail
The application correctly entered the NotAllowedError path, but the permission-specific message incorrectly referenced both camera and microphone access.
Because the application requests video: true and audio: false, the microphone reference does not accurately represent the requested permissions.
Related Defect
BUG-001 - Permission Denial Error Incorrectly References Microphone Access

---

**Path 3 - Generic / Unhandled Media Error**
Relevant Logic
Errors that are neither OverconstrainedError nor NotAllowedError bypass the specific conditional branches.
The application still executes the generic error handler:
getUserMedia error: [error name]
Test Derived From Source Review
TC-005 - Camera Unavailable at Initialization
Environment Manipulation
The system camera was manually disabled before attempting camera initialization.
Result
The browser returned:
NotFoundError
The application displayed:
getUserMedia error: NotFoundError
Outcome
The generic fallback error path was successfully exercised.
The application remained stable and no video stream initialized.
Additional Observation
The raw API/browser error name is displayed without a user-oriented explanation that no usable camera device is available.

---

**Path 4 - OverconstrainedError**
Relevant Logic
The application contains a specific branch for:
error.name === 'OverconstrainedError'
This path is intended to handle situations where requested media constraints cannot be satisfied by available hardware.
Current Constraint Limitation
The current application configuration requests only:
video: true
No exact resolution, frame rate, device ID, or other restrictive video constraints are defined.
Because of this, the current user interface does not provide an obvious method for naturally producing an OverconstrainedError.
Planned Test
TC-007 - Unsupported Media Constraint Condition
Status
Design Only / Not Yet Executed
A controlled modification or test harness may be required to intentionally request unsupported media constraints and execute this branch.

---

**Error Display Analysis**
The error-display function appends messages to the existing error container instead of replacing previous content.
Relevant behavior:
errorElement.innerHTML += `<p>${msg}</p>`;
Risk Identified
Because new error content is appended, repeated failed camera requests continuously add duplicate messages to the page.
Tests Demonstrating This Behavior
- TC-003 - Retry Camera Initialization After Permission Denial
- TC-005 - Camera Unavailable at Initialization
- TC-008 - Repeated Permission Prompt Dismissal
Related Defect
BUG-002 - Repeated Camera Requests Append Duplicate Error Messages

---

**Asynchronous Initialization Analysis**
Camera initialization uses an asynchronous request:
const stream =
  await navigator.mediaDevices.getUserMedia(constraints);
The Open Camera button is disabled only after the request resolves successfully.
This created a potential test question:
Can multiple camera initialization requests be triggered before the first request resolves?
Test Derived From Source Review
TC-004 - Repeated Camera Initialization Before Permission Resolution
Result
Pass in Tested Chrome Environment
Chrome immediately displayed its permission interface after the first camera request.
While the permission interface was active, the underlying Open Camera control could not be selected again through normal user interaction.
QA Observation
In the tested environment, prevention of repeated initialization was effectively enforced by the browser permission interface rather than by disabling the application control before the asynchronous request began.

---

**Post-Initialization Resiliency Analysis**
After successful camera initialization, the reviewed source assigns the stream to the video element.
No explicit track-ending or camera-disconnection handling was identified in the reviewed file.
This produced an additional resiliency scenario:
TC-006 - Camera Becomes Unavailable After Successful Initialization

---

**Current Path Coverage**
The following primary execution paths identified during source review have been manually exercised:
	
| Execution Path | Test Case | Status |
|---|---|---|
| Successful media initialization | TC-001 | Executed |
| NotAllowedError | TC-002 | Executed |
| Generic/other error (NotFoundError) | TC-005 | Executed |
| OverconstrainedError | TC-007 | Not Yet Executed |

---

Three of the four primary outcome paths identified during source review have been exercised manually.
This is not instrumented code-coverage measurement; it represents manual execution of identified application paths.

**Key Findings**
Source-code review directly influenced test design and resulted in:
- Identification of the inaccurate microphone reference in the permission error
- Identification of duplicate error accumulation caused by appended DOM content
- Creation of a generic fallback-error test
- Creation of an asynchronous repeated-interaction test
- Identification of an untested OverconstrainedError branch
- Creation of a post-initialization camera-interruption resiliency test
The purpose of this test is to evaluate what happens when the camera is removed or disabled after the application has already entered the successful state.
