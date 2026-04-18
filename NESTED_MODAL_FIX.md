# 🔧 Nested Modal System - Troubleshooting Guide

## সমস্যা: Nested Modal Close হওয়ার পর Parent Modal আবার Open হচ্ছে না

### ✅ এখন Fixed!

আপডেট করা হয়েছে:
1. **openModalWithUrl** - Nested modal properly save করছে
2. **restorePreviousModalAndApply** - Parent modal properly restore করছে
3. **closeModal** - Stack properly manage করছে
4. **handleRelatedSaved** - Save events properly handle করছে

---

## 🧪 কীভাবে Test করবেন?

### Test Case 1: সাধারণ Nested Modal

```
1. একটি list page খুলুন
2. একটি item select করুন এবং "Create Related" button click করুন
3. Modal 1 open হবে ✅
4. Modal 1 এ form fill করুন
5. Save করুন ✅
6. Modal 1 close হবে এবং parent page return হবে ✅
```

### Test Case 2: Double Nested Modal (আগের সমস্যা)

```
1. Parent modal open করুন (Modal 1)
2. Modal 1 এ "Create Related" button click করুন (Modal 2)
3. Modal 2 এ form fill করুন
4. Modal 2 save করুন ✅
5. Modal 2 close হবে এবং Modal 1 restore হবে ✅
6. Modal 1 এ আবার "Create Related" button click করুন (Modal 2 again)
7. Modal 2 open হবে ✅ (এটি আগে fail হচ্ছিল!)
8. Form fill করুন এবং save করুন ✅
9. Modal 2 close এবং Modal 1 restore হবে ✅
```

### Test Case 3: Triple Nested Modal

```
1. Modal 1 open
2. Modal 2 open (from Modal 1)
3. Modal 3 open (from Modal 2)
4. Modal 3 save - Modal 2 restore ✅
5. Modal 2 save - Modal 1 restore ✅
6. Modal 1 save - page close ✅
```

---

## 🐛 Debug Mode চালু করুন

Browser console এ debug logs দেখতে পারবেন:

```
📥 Saved parent modal to stack. Stack length: 1
📝 Modal body loaded. Stack: 1
💾 Form saved. Modal stack length: 1
📤 Restoring parent modal from stack. Remaining stack: 0
🏠 Main content updated
🔒 Closing modal completely
```

---

## ⚠️ Common Issues

### Issue 1: Modal open হচ্ছে না

**Check:**
```javascript
// Browser console এ এই command চালান:
console.log(document.getElementById('modal-container'))
console.log(document.getElementById('modal-body'))
console.log(typeof htmx)
```

**সমাধান:**
- ✅ `modal-container` exist করছে?
- ✅ HTMX library loaded?
- ✅ modal-system.js loaded?

### Issue 2: Parent Modal Close হয়ে যাচ্ছে

**Check console logs:**
- আছে কি `📤 Restoring parent modal`?
- আছে কি `🔒 Closing modal completely`?

**যদি `🔒` দেখা যায়:**
- এর মানে `modalStack.length === 0`
- Parent modal properly save হয়নি

**সমাধান:**
- নিশ্চিত করুন যে **create button** সঠিক class এ আছে: `related-create-btn`
- নিশ্চিত করুন `data-model` এবং `data-field-name` attributes আছে

### Issue 3: Form Values Lost হচ্ছে

**Check:**
- Browser console এ error আছে কি?
- TomSelect properly restored হচ্ছে কি?

**সমাধান:**
```javascript
// View এ ensure করুন:
response['HX-Trigger'] = json.dumps({
    'related:saved': {
        'parentField': 'field_name',  // ← Important!
        'option': {'id': obj.id, 'text': str(obj)}
    }
})
```

---

## 📋 Checklist

### Backend (Django)

```python
# ✅ View এ HX-Trigger পাঠাচ্ছে?
response['HX-Trigger'] = json.dumps({
    'related:saved': {
        'parentField': request.POST.get('_parent_field'),
        'option': {'id': obj.id, 'text': str(obj)}
    }
})

# ✅ Form এ _parent_field hidden input আছে?
<input type="hidden" name="_parent_field" value="{{ parent_field }}">
```

### Frontend (HTML/JavaScript)

```html
<!-- ✅ Modal container আছে? -->
<div id="modal-container">
    <div id="modal-body"></div>
</div>

<!-- ✅ Script loaded? -->
<script src="{% static 'js/modal-system.js' %}"></script>

<!-- ✅ Create button সঠিক? -->
<button class="related-create-btn" 
        data-model="product"
        data-field-name="product">
    + Create
</button>

<!-- ✅ Form has correct action/method? -->
<form hx-post="{{ post_url }}"
      hx-target="#modal-body"
      hx-swap="innerHTML">
    <!-- Form fields -->
</form>
```

---

## 🎯 Key Points

### 1️⃣ Modal Stack Management
```
Level 0 (Page):        modalStack = []
↓ Open Modal 1
Level 1 (Modal 1):     modalStack = [] (parent page saved)
↓ Open Modal 2 from Modal 1
Level 2 (Modal 2):     modalStack = [parentModal1] 
↓ Save Modal 2
Level 1 (Modal 1):     modalStack = [] (parent page restored)
↓ Open Modal 2 again
Level 2 (Modal 2):     modalStack = [parentModal1]
↓ Save Modal 2
Level 1 (Modal 1):     modalStack = [] (restored again)
↓ Save Modal 1
Level 0 (Page):        modalStack = [] (close)
```

### 2️⃣ Form State Capture
```javascript
// যখন nested modal open করি:
state = captureFormState(body)
selectOptions = captureSelectOptions(body)

// যখন nested modal close করি:
restoreFormState(body, previous.state)
restoreSelectOptions(body, previous.selectOptions)
```

### 3️⃣ Auto-Select
```javascript
// Nested modal save হলে:
ensureRelatedOptionSelected(
    'field_name',        // Parent field name
    {id: 123, text: '...'}, // Created object
    body,                // Parent modal body
    20, 100             // Retry settings
)
```

---

## 🚨 Edge Cases

### Case 1: Multiple Create Buttons

```html
<!-- দুটি different fields এর জন্য create button -->
<select name="product">
    <button class="related-create-btn" data-model="product" data-field-name="product">
        Create Product
    </button>
</select>

<select name="vendor">
    <button class="related-create-btn" data-model="vendor" data-field-name="vendor">
        Create Vendor
    </button>
</select>
```

✅ **এটি কাজ করবে** - প্রতিটি button সঠিক `data-field-name` আছে

### Case 2: Dependent Fields

```html
<!-- Branch select, তারপর Area -->
<select name="branch">...</select>
<button class="related-create-btn" data-model="area" data-field-name="area">
    Create Area
</button>
```

✅ **Auto-detect করবে** - Area model detect করে branch_id pass করবে

### Case 3: Multiple Select

```html
<select name="tags" multiple class="js-enhanced-multiselect">...</select>
<button class="related-create-btn" data-model="tag" data-field-name="tags">
    Create Tag
</button>
```

✅ **Multiple add করবে** - নতুন tag add করবে existing tags এর সাথে

---

## 📞 যদি এখনও সমস্যা হয়

### Debug এই গুলি:

```javascript
// 1. Modal container accessible?
console.log(document.getElementById('modal-container'));

// 2. Modal body accessible?
console.log(document.getElementById('modal-body'));

// 3. Stack size?
console.log('Modal Stack Size:', window.modalStack?.length || 'undefined');

// 4. HTMX working?
console.log('HTMX Available:', typeof htmx !== 'undefined');

// 5. TomSelect working?
console.log('TomSelect Available:', typeof TomSelect !== 'undefined');
```

### Network Issue Check:

```javascript
// Open DevTools > Network tab
// করো:
// 1. Parent modal form submit
// 2. দেখো: Response Headers এ HX-Trigger আছে কি?

// Expected:
// HX-Trigger: {"related:saved": {"parentField": "...", "option": {...}}}
```

---

## ✨ সবকিছু ঠিক থাকলে

✅ Parent modal open - কাজ করছে  
✅ Nested modal open - কাজ করছে  
✅ Nested modal save - কাজ করছে  
✅ Parent restore - কাজ করছে  
✅ Parent এ আবার nested - কাজ করছে  
✅ Auto-select - কাজ করছে  
✅ Dark mode - কাজ করছে  

**Everything should work perfectly now! 🎉**

---

Still having issues? Check the browser console for the debug logs:
- 📥 = Parent saved
- 📝 = Modal loaded
- 💾 = Form saved
- 📤 = Parent restoring
- 🏠 = Main content updated
- 🔒 = Modal closing
