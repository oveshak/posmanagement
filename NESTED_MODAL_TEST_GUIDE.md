# Nested Modal Test Guide - সম্পূর্ণ Test Case

## আপনার প্রয়োজন (Requirement):
```
যখন নেস্টেড মডাল create/edit করা হয় তখন:
1. নেস্টেড মডাল open → save → auto-select হয়
2. নেস্টেড মডাল close হয় 
3. Parent মডাল restore হয়
4. Parent মডাল form submit → auto-select হয়
5. Parent মডাল close হয়
```

## Test Scenario - কাস্টমার গ্রুপ তৈরি করা

### Step 1: Customer Group Create Modal Open
```
ক্লিক করুন: "Create Customer Group" button
→ Modal খুলবে with fields:
   - Name
   - Branch (select field)
   - Area (select field)
   - Staff (multi-select)
   - Description
```

### Step 2: Branch এ Nested Modal Open করুন
```
Branch field এ click করুন "+" (Create icon)
→ "Create Branch" modal খুলবে
```

### Step 3: Branch Create করুন
```
Form fill করুন:
  - Name: "Test Branch" 
  - Click Save
→ Branch তৈরি হবে
→ Branch মডাল close হবে
→ Customer Group মডাল restore হবে
→ Branch select field এ auto-select হবে ("Test Branch")
```

### Step 4: Area তে Nested Modal Open করুন  
```
Area field এ click করুন "+" (Create icon)
→ "Create Area" modal খুলবে
```

### Step 5: Area Create করুন
```
Form fill করুন:
  - Name: "Test Area"
  - Branch: "Test Branch" (auto-filled from parent)
  - Click Save
→ Area তৈরি হবে
→ Area মডাল close হবে
→ Customer Group মডাল restore হবে
→ Area select field এ auto-select হবে ("Test Area")
```

### Step 6: Parent Form Submit করুন
```
Customer Group মডাল এ:
  - Name: "Test Group"
  - Branch: "Test Branch" ✅ (already selected)
  - Area: "Test Area" ✅ (already selected)
  - Click Save
→ Customer Group তৈরি হবে
→ Customer Group মডাল close হবে ✅
→ Page refresh হবে
```

## Browser Console Logs (Expected)

### Branch Create:
```
⏳ Form beforeRequest: /user/ajax/related/branch/create/
🔍 handleRelatedSaved - parentField="parent_branch", stackLength=1, isNested=true
📤 This is NESTED - will restore parent
   Parent restore step 1: HTML cleared
   Parent restore step 2: HTML restored
   Parent restore step 3: Binding markers cleared
   Parent restore step 4: Modal visible
   Parent restore step 5: DOM settled
   Parent restore step 6: UI re-initialized
   Parent restore step 7: Form state restored
   Parent restore step 8: DOM settled
   Parent restore step 9: Form state re-restored
   Parent restore step 10: Auto-selecting: parent_branch = Test Branch
   Parent restore step 11: Success message shown
```

### Customer Group Create:
```
⏳ Form beforeRequest: /user/ajax/related/customergroup/create/
🔍 handleRelatedSaved - parentField="", stackLength=0, isNested=false
🔒 This is TOP-LEVEL - will close modal
   Auto-selecting: customer_group = Test Group
   Clearing modal body and hiding...
🔒 hideModal() called - removing 'hidden' class
   Modal hidden. Current class: modal-container hidden
✅ Modal closed!
```

## Debugging Commands

### 1. Open Console (F12)
```
Press: F12
Go to: Console tab
Check for logs
```

### 2. View Network Tab
```
Press: F12
Go to: Network tab
Filter by: XHR/Fetch
Look for POST requests to /user/ajax/related/.../create/
Check Response headers for HX-Trigger
```

### 3. Clear Console Before Test
```
console.clear()
// Then perform your test scenario
```

## Common Issues & Solutions

### Issue 1: Modal doesn't close after parent submit
**Check Console for:**
```
❌ If you see: "handleRelatedSaved - parentField="branch"" with isNested=true
   Problem: _parent_field not cleared after nested restore
   
✅ Should see: "handleRelatedSaved - parentField="" with isNested=false
   Solution: Parent restore is clearing _parent_field correctly
```

### Issue 2: Nested modal doesn't close
**Check Console for:**
```
❌ If you see: NO logs from handleRelatedSaved
   Problem: HX-Trigger header not being received
   
✅ Should see: "💾 Form saved. Triggers: ..." with valid detail
   Solution: Django view is sending correct HX-Trigger header
```

### Issue 3: Auto-select not working
**Check Console for:**
```
❌ If you see: "Auto-selecting: branch = undefined"
   Problem: detail.parentField or detail.option is missing
   
✅ Should see: "Auto-selecting: branch = Test Branch"
   Solution: Django view is sending correct parentField and option
```

## Step-by-Step Debug Process

1. **Open Console (F12)**
   - Go to Console tab
   - Type: `console.clear()`
   - Press: Enter

2. **Start Test**
   - Click "Create Customer Group"
   - Wait for logs

3. **Check Logs**
   - Look for 🔍 handleRelatedSaved
   - Check parentField value
   - Check isNested flag
   - Check stackLength

4. **Proceed with Nested**
   - Click Branch "+" icon
   - Check for 📤 "This is NESTED" log
   - Check for "Parent restore" logs
   - Verify branch auto-selects

5. **Complete Test**
   - Fill and submit parent form
   - Check for 🔒 "This is TOP-LEVEL" log
   - Verify modal closes

## Key Console Logs to Watch

| Log | Meaning |
|-----|---------|
| 📡 htmx:afterRequest | Form submitted |
| 💾 Form saved. Triggers: | Response received |
| 🔍 handleRelatedSaved | Processing save event |
| 📤 This is NESTED | Will restore parent |
| 🔒 This is TOP-LEVEL | Will close modal |
| 🔒 hideModal() called | Modal hiding |
| ✅ Modal closed | Success |
| ❌ Error logs | Problems |

## Modal Stack Visualization

### Top-Level Modal:
```
modalStack = []
└─ Customer Group Modal (isNested = false)
```

### After Opening Branch Create:
```
modalStack = [
  {
    html: "Customer Group form HTML",
    state: {name: "", branch: "", ...},
    selectOptions: {branch: [...], area: [...]}
  }
]
└─ Branch Modal (isNested = true)
```

### After Saving Branch:
```
modalStack = []
└─ Customer Group Modal (with _parent_field = "" now)
```

## Testing Checklist

- [ ] Step 1: Open Customer Group Create modal
- [ ] Step 2: Click Branch create icon
- [ ] Step 3: Check console - see nested logs
- [ ] Step 4: Save branch
- [ ] Step 5: Check console - see parent restore logs
- [ ] Step 6: Verify branch auto-selected
- [ ] Step 7: Click Area create icon
- [ ] Step 8: Save area  
- [ ] Step 9: Verify area auto-selected
- [ ] Step 10: Fill parent form
- [ ] Step 11: Submit parent form
- [ ] Step 12: Check console - see top-level close logs
- [ ] Step 13: Verify modal closes

## Success Criteria

✅ **Pass** if:
- Nested modals open and close properly
- Parent modal restores after nested save
- Auto-select works for newly created items
- Parent modal closes after parent form submit
- All console logs are correct
- Modal stack is properly managed

❌ **Fail** if:
- Modal doesn't close
- Parent modal doesn't restore
- Auto-select doesn't work
- Stack length is wrong
- Expected logs are missing
- Wrong logs appear

## Contact Info

যদি কোন সমস্যা থাকে:
1. Console logs copy করুন (F12 → Console)
2. Network response headers check করুন (F12 → Network → XHR)
3. পাঠান আমাদের কাছে debugging এর জন্য
