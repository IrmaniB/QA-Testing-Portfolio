# QA Testing Portfolio

Hi, I'm Irmani Barnes. This repository is a hands-on Quality Assurance portfolio demonstrating practical experience with manual software testing, defect documentation, source-informed test design, cross-browser validation, and browser automation using Python and Selenium WebDriver.

I built these projects to practice the QA workflow from test planning and execution through defect investigation, technical analysis, regression thinking, and automated validation.

## Portfolio at a Glance

- 25 manual test cases
- 8 documented software defects
- 6 Selenium WebDriver automation scripts
- Real-time media and WebRTC testing
- Cross-browser validation across Chrome, Edge, Firefox, and Safari
- Source-code review and white-box/source-informed test design
- Change-impact and regression-risk analysis
- Coverage includes functional, exploratory, negative, boundary-value, resiliency, responsive/mobile, input-validation, navigation, and e-commerce testing

---

## [Real-Time Media QA Case Study](./real-time-media-qa/)

Technical QA case study focused on the WebRTC `getUserMedia()` camera demo.

### Highlights

- 8 manual test cases executed
- 4 documented defects
- 4 of 4 manually identified primary execution paths exercised
- Cross-browser testing across Chrome, Edge, Firefox, and Safari
- JavaScript source review used to derive targeted test scenarios
- `NotAllowedError`, `NotFoundError`, `NotReadableError`, and `OverconstrainedError` behavior evaluated
- Runtime media constraints modified to deliberately exercise the `OverconstrainedError` branch
- Mid-stream camera interruption and recovery behavior tested
- Real historical code change reviewed through change-impact analysis
- Screenshot evidence linked to relevant test cases and defect reports

### Artifacts

- [Test Plan](./real-time-media-qa/Test_Plan.md)
- [Test Cases](./real-time-media-qa/Test_Cases.md)
- [Defect Reports](./real-time-media-qa/Defect_Reports.md)
- [White-Box Test Analysis](./real-time-media-qa/White_Box_Test_Analysis.md)
- [Change Impact Analysis](./real-time-media-qa/Change_Impact_Analysis.md)
- [Cross-Browser Testing](./real-time-media-qa/Cross_Browser_Testing.md)
- [Test Evidence](./real-time-media-qa/evidence/)

---

## [Manual Software Testing](./manual-testing/)

The manual testing portfolio contains structured testing performed against publicly accessible web applications.

The workbook includes:

- **Test Cases** - Preconditions, test steps, test data, expected results, and priority
- **Execution Log** - Actual results, pass/fail status, environment, notes, and linked defects
- **Bug Report Log** - Reproduction steps, expected versus actual behavior, severity, and supporting evidence
- **Test Summary** - Overall execution results and major findings

Testing includes functional, exploratory, boundary-value, input-validation, responsive/mobile, navigation, link-integrity, and e-commerce scenarios.

---

## Selected Defects Identified

Examples of defects identified during portfolio testing include:

- Incorrect camera permission error referencing microphone access when audio was not requested
- Duplicate error messages accumulating after repeated media failures
- Missing recovery handling after an active camera stream is interrupted
- Stale error messages remaining visible after successful camera recovery
- Broken secondary appointment-scheduling CTA
- Newsletter form accepting an invalid email format
- Missing character-length validation on a personalization field
- Broken product image/resource during an e-commerce search flow

---

## [Selenium WebDriver Automation](./selenium-automation/)

| Script | What It Demonstrates |
| --- | --- |
| `Sephora_Locator.py` | Store-locator interaction, modal handling, browser permission configuration, explicit waits, and location-suggestion validation |
| `Kikiz_Nav.py` | Mobile navigation interaction, element targeting, JavaScript click fallback, and URL validation |
| `Matt_Mathews_Store.py` | Search-field input sanitization validation and safe handling of script-like input |
| `Ulta_Cart.py` | Add-to-bag workflow automation, UI interaction, and cart-state validation |
| `VikkiPrints.py` | Boundary-value testing, long-input validation, cart workflow automation, and automated defect reproduction |
| `GreenEye.py` | CTA validation, multi-tab browser handling, destination-state inspection, and automated reproduction of a broken scheduling flow |

---

## Tools & Technologies

- Python
- Selenium WebDriver
- Git & GitHub
- Chrome DevTools
- Google Chrome
- Microsoft Edge
- Mozilla Firefox
- Safari
- Postman
- Excel
- XPath
- HTML / DOM inspection
- JavaScript source review
- Browser media APIs / WebRTC testing
- Explicit waits and expected conditions
- Assertions and result validation
- JavaScript interaction fallbacks

---

## QA Skills Demonstrated

- Manual Testing
- Functional Testing
- Exploratory Testing
- Negative Testing
- Test Case Design & Execution
- Defect / Bug Reporting
- White-Box / Source-Informed Test Design
- Execution-Path Analysis
- Cross-Browser Testing
- Resiliency & Recovery Testing
- Change-Impact Analysis
- Regression-Risk Analysis
- Boundary-Value Analysis
- Responsive & Mobile UI Testing
- Input Validation Testing
- Navigation & Link Validation
- Browser Automation
- Technical Troubleshooting
- Test Evidence & Result Documentation

---

## Current Development

I am continuing to expand this portfolio with additional QA and software engineering skills, including:

- REST API testing with Postman
- SQL-based data validation
- JavaScript and TypeScript
- Playwright automation
- CI/CD and GitHub Actions
- Additional regression and integration testing

---

## About Me

I am pursuing entry-level opportunities in QA Analysis, Software Testing, Manual QA, and Junior QA Engineering.

My professional background in technical customer support has strengthened my troubleshooting, documentation, issue investigation, and communication skills, which I now apply to software quality assurance.

**LinkedIn:** [Irmani Barnes](https://www.linkedin.com/in/irmani-barnes-057728356)

---

## Portfolio Note

These projects were created for learning and professional portfolio purposes using publicly accessible applications and source code. Results reflect behavior observed during testing and may change as applications, browsers, or websites are updated.
