# User Acceptance Testing Script - Military Supply Analytics Dashboard

**Document Type:** Dashboard Validation Protocol  
**System:** Military Base Supply Dashboard (Proof of Concept)  
**Version:** 1.0  
**Date:** April 2025  
**Status:** Demonstration/Portfolio Project

---

## Table of Contents

1. Test Overview & Objectives
2. Dashboard Components Validation
3. Data Visualization Testing
4. Analytics Accuracy Verification
5. User Experience Validation
6. Performance Testing
7. Browser Compatibility
8. Test Results Documentation

---

## 1. Test Overview & Objectives

### Primary Objectives
- Validate dashboard displays all required visualizations correctly
- Confirm data calculations and transformations are accurate
- Verify dashboard usability for logistics decision-making
- Test performance with simulated dataset
- Ensure browser compatibility across standard platforms

### Success Criteria
- All 13 dashboard visualizations render correctly
- Data calculations match expected business logic
- Dashboard loads within 10 seconds on standard hardware
- Responsive design works on desktop and tablet devices
- No critical errors in browser console

---

## 2. Dashboard Components Validation

### 2.1 Vendor Performance Analytics

#### Test Case UAT-VPA-001: On-Time Delivery Rate Chart
**Objective:** Verify vendor performance metrics display correctly
**Test Steps:**
1. Load dashboard in browser
2. Locate "On-Time Delivery Rate by Vendor" chart
3. Verify all vendors from dataset are displayed
4. Check percentage calculations are accurate
5. Confirm sorting (descending by performance)

**Expected Results:**
- All vendors from `supply_deliveries.csv` appear
- Percentages calculated as: `(on_time_deliveries / total_deliveries) * 100`
- Chart sorted with best performers first
- Hover tooltips show exact values

**Validation Data:**
- Reference: `vendor_summary` calculation in script
- Expected range: 0-100% for each vendor
- Verify against manual calculation of sample vendor

#### Test Case UAT-VPA-002: Average Delay Tracking
**Test Steps:**
1. Review "Average Delivery Delay (Days) by Vendor" chart
2. Verify delay calculations match raw data
3. Check for negative values (early deliveries)
4. Confirm vendor sorting (worst to best)

**Expected Results:**
- Delay = `actual_delivery_date - expected_delivery_date`
- Values can be positive (late) or negative (early)
- Chart clearly indicates which vendors consistently delay

### 2.2 Inventory Risk Management

#### Test Case UAT-IRM-001: Critical Inventory Scatter Plot
**Test Steps:**
1. Locate "Inventory Risk (Coverage < 35 Days)" visualization
2. Verify only bases with <35 days coverage shown
3. Check point sizes represent inventory volume
4. Confirm color coding by supply category

**Expected Results:**
- Only records where `days_remaining < 35` displayed
- Point size correlates with `inventory_units`
- Different colors for each `supply_category`
- Axes clearly labeled

#### Test Case UAT-IRM-002: Critical Inventory Table
**Test Steps:**
1. Review "Critical Base-Category Inventory" bar chart
2. Verify data matches scatter plot
3. Check sorting by urgency (lowest days first)
4. Confirm base-category labeling format

### 2.3 Financial Controls

#### Test Case UAT-FC-001: Budget Utilization Heatmap
**Test Steps:**
1. Examine budget utilization heatmap
2. Verify utilization calculation: `(budget_spent / budget_allocated) * 100`
3. Check color scale interpretation
4. Confirm all base-category combinations shown

**Expected Results:**
- Values >100% indicate overspending
- Color intensity reflects utilization level
- All combinations from `supply_budget.csv` present

---

## 3. Data Visualization Testing

### 3.1 Chart Rendering Validation
**Test Parameters:**
- All charts load without errors
- Proper axis labels and units
- Legend displays correctly
- Interactive features work (hover, zoom)

### 3.2 Data Accuracy Spot Checks
**Sample Verification:**
1. Select 3 random vendors - manually verify on-time percentages
2. Choose 2 bases - confirm budget utilization calculations
3. Pick 1 supply category - validate inventory risk flagging

---

## 4. Analytics Accuracy Verification

### 4.1 Composite Risk Index Validation
**Test Steps:**
1. Review "Composite Base Risk Index" chart
2. Verify calculation methodology documented
3. Check component weights are reasonable
4. Confirm ranking makes operational sense

**Business Logic Check:**
- Higher risk scores for bases with: high route risk, low inventory, budget overruns, frequent emergencies
- Index calculation: `mean([route_risk, low_supply_ratio, overspend_ratio, emergency_ratio]) * 100`

### 4.2 Lead Time Analysis
**Test Steps:**
1. Examine "Procurement Lead Time by Supply Category" box plot
2. Verify lead time calculation: `actual_delivery_date - order_date`
3. Check for outliers and their reasonableness
4. Confirm statistical measures (median, quartiles)

---

## 5. User Experience Validation

### 5.1 Dashboard Navigation
**Test Scenarios:**
- First-time user can understand dashboard purpose
- Charts are logically grouped and sequenced
- Visual hierarchy guides attention to critical information
- Dashboard tells a coherent analytical story

### 5.2 Decision Support Effectiveness
**Test Questions:**
- Can user quickly identify worst-performing vendors?
- Are inventory risks clearly highlighted?
- Is budget variance information actionable?
- Does dashboard support operational decision-making?

---

## 6. Performance Testing

### 6.1 Load Time Testing
**Test Environment:** Standard laptop (8GB RAM, mid-range processor)
**Measurements:**
- Initial dashboard load time
- Chart rendering completion time
- Browser memory usage
- CPU utilization during load

**Acceptance Criteria:**
- Dashboard fully loaded within 10 seconds
- Memory usage <500MB
- No browser freezing or lag

### 6.2 Data Processing Validation
**Test Steps:**
1. Verify CSV files load correctly
2. Check data transformation accuracy
3. Confirm aggregation calculations
4. Validate derived metrics

---

## 7. Browser Compatibility

### 7.1 Cross-Browser Testing
**Test Browsers:**
- Chrome (latest version)
- Firefox (latest version)
- Safari (if available)
- Edge (latest version)

**Test Items:**
- All charts render identically
- Interactive features work consistently
- Layout maintains integrity
- No JavaScript errors in console

### 7.2 Responsive Design Testing
**Test Devices/Screens:**
- Desktop (1920x1080)
- Laptop (1366x768)
- Tablet landscape (1024x768)
- Large monitor (2560x1440)

---

## 8. Test Results Documentation

### 8.1 Test Execution Log
**Required Documentation:**
- Screenshot of each major visualization
- Browser console log (no critical errors)
- Performance metrics (load times)
- Any visual inconsistencies noted

### 8.2 Issues Classification
- **Critical:** Dashboard won't load or major calculation errors
- **High:** Charts missing or significantly incorrect data
- **Medium:** Minor visual issues or performance problems
- **Low:** Cosmetic improvements or enhancements

### 8.3 User Feedback Collection
**Evaluation Criteria:**
- Visual clarity and readability
- Information usefulness for decision-making
- Ease of interpretation
- Overall dashboard effectiveness

---

## Test Checklist

### Pre-Test Setup
- [ ] Python environment configured
- [ ] All required libraries installed (dash, plotly, pandas)
- [ ] CSV data files in correct directory structure
- [ ] Dashboard script runs without errors

### Core Functionality Tests
- [ ] All 13 visualizations render correctly
- [ ] Data calculations verified accurate
- [ ] Interactive features functional
- [ ] No critical browser console errors

### Performance Validation
- [ ] Dashboard loads within 10 seconds
- [ ] Smooth interaction with charts
- [ ] Acceptable memory usage
- [ ] Responsive design validated

### Final Validation
- [ ] Dashboard serves intended analytical purpose
- [ ] Visualizations support decision-making
- [ ] Documentation matches actual functionality
- [ ] Portfolio presentation ready

---

## Known Limitations (Portfolio Context)

1. **Simulated Data:** Dashboard uses fictional data for demonstration
2. **Static Analysis:** No real-time data integration
3. **Single User:** No multi-user access or authentication
4. **Development Environment:** Not production-hardened

---

## Success Metrics for Portfolio Demonstration

- **Technical Competency:** Clean code, proper data handling, effective visualizations
- **Business Understanding:** Relevant KPIs, logical groupings, actionable insights  
- **Design Quality:** Professional appearance, clear labeling, intuitive layout
- **Documentation:** Complete technical and business documentation package