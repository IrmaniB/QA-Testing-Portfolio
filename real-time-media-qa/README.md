# Real-Time Media QA Case Study

## Project Overview

This project is a QA case study focused on real-time media functionality using the WebRTC `getUserMedia()` camera demo.

The purpose of this project is to evaluate media-stream behavior through manual testing, exploratory testing, cross-browser validation, negative testing, and white-box/source-informed test design.

Unlike my previous black-box testing projects, this case study also incorporates source-code review to identify execution paths, error-handling logic, and implementation details that can be used to design targeted test scenarios.

## System Under Test

**Application:** WebRTC Samples  
**Component:** `getUserMedia()` basic camera demo  
**Primary Functionality:** Browser camera access and real-time video-stream initialization

The demo requests access to the user's camera using the browser's `getUserMedia()` API and displays the resulting video stream within the page.

## Testing Approach

This project includes:

- Manual functional testing
- Exploratory testing
- Positive and negative testing
- Permission and error-handling validation
- Cross-browser testing
- Source-code review
- White-box/source-informed test design
- Execution-path and branch analysis
- Resiliency and edge-case testing
- Change-impact analysis

## Skills Demonstrated

This project demonstrates hands-on experience with:

- Real-time media testing
- WebRTC browser functionality
- Cross-browser validation
- Test scenario and test case design
- Negative and edge-case testing
- Source-code review
- White-box testing concepts
- Execution-path analysis
- Error-handling validation
- Defect identification and documentation
- QA risk analysis

## Current Test Environment

Testing was performed across:

- Windows - Google Chrome 153.0.8010.52
- Windows - Microsoft Edge
- Windows - Mozilla Firefox
- iPhone - Safari

Google Chrome was used as the primary deep-dive environment for source-informed testing, error-path analysis, resiliency testing, and runtime constraint manipulation.

Edge, Firefox, and Safari were used for cross-browser compatibility validation of successful camera initialization and permission-denial behavior.

## Project Results

- 8 manual test cases executed
- 4 documented defects
- 4 of 4 manually identified primary execution paths exercised
- Cross-browser validation across Chrome, Edge, Firefox, and Safari
- Source-code review used to derive targeted test scenarios
- Runtime media constraints modified to exercise the `OverconstrainedError` branch
- Mid-stream camera interruption and recovery behavior evaluated
- Real historical code change reviewed through change-impact analysis

## Key Findings

Testing identified issues involving:

- Inaccurate permission-denial messaging
- Duplicate error accumulation during repeated failures
- Missing recovery handling after mid-stream camera interruption
- Stale error messages remaining visible after successful recovery

Cross-browser testing reproduced the permission-message and duplicate-error defects across all tested browsers.

## Project Artifacts

- [Test Plan](./Test_Plan.md)
- [Test Cases](./Test_Cases.md)
- [Defect Reports](./Defect_Reports.md)
- [White-Box Test Analysis](./White_Box_Test_Analysis.md)
- [Change Impact Analysis](./Change_Impact_Analysis.md)
- [Cross-Browser Testing](./Cross_Browser_Testing.md)
- [Test Evidence](./Evidence/)

## Project Status

✅ Initial testing complete
