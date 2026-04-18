# Modal System - সম্পূর্ণ গাইড

## সমস্যা কী ছিল?
✗ Modal বন্ধ হচ্ছিল না  
✗ Auto-select কাজ করছিল না  
✗ Nested modal open হলে সমস্যা হচ্ছিল  
✗ সব apps এ একই রকম behavior ছিল না  

## সমাধান কী করেছি?
✅ **নতুন Modal System** তৈরি করেছি (`modal-system.js`)  
✅ **Universal Modal Template** তৈরি করেছি  
✅ সব apps এ **একই behavior** নিশ্চিত করেছি  
✅ **Nested modals** সঠিকভাবে handle করছে  
✅ **Auto-select** নতুন item গুলি perfectly কাজ করছে  

---

## ৩টি মূল ফাইল

### 1️⃣ `static/js/modal-system.js`
**এটি কী করে:**
- Modal open/close করে
- Form state save এবং restore করে
- Nested modals manage করে
- Auto-select feature handle করে
- সব apps এর জন্য unified system

**Global Functions:**
```javascript
// Modal বন্ধ করুন
closeModal()

// Success alert দেখান
showSuccessAlert("Success message")

// Error alert দেখান
showErrorAlert("Error message")
```

### 2️⃣ `templates/common/universal_modal_form.html`
**এটি সব forms এর জন্য universal template**

কোথায় ব্যবহার করবেন:
- Product form
- User form
- Any related model form

### 3️⃣ `templates/base.html`
**Updated:** নতুন `modal-system.js` load করছে

---

## কীভাবে ব্যবহার করবেন?

### Step 1: Modal Template ব্যবহার করুন
আপনার form template এ:

```django
{% extends 'base.html' %}

{% block content %}
    <!-- আপনার list page -->
{% endblock %}

<!-- Modal form page হলে -->
{% include 'common/universal_modal_form.html' with 
    title="Product যোগ করুন"
    post_url="/product/create/"
    model_name="product"
    parent_field="category"
    form=form
%}
```

### Step 2: Django View এ Setup করুন

```python
from django.http import HttpResponse
from django.views import View

class ProductCreateModal(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'product/create_modal.html', {
            'form': form,
            'title': 'Product যোগ করুন',
            'post_url': '/product/create/',
            'model_name': 'product',
        })
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            obj = form.save()
            
            # Return trigger for auto-select
            response = render(request, 'product/create_modal.html', {
                'form': form,
                'title': 'Product যোগ করুন',
            })
            
            response['HX-Trigger'] = json.dumps({
                'related:saved': {
                    'parentField': request.POST.get('_parent_field', ''),
                    'option': {
                        'id': obj.id,
                        'text': str(obj)
                    },
                    'message': 'Product সফলভাবে তৈরি হয়েছে!'
                }
            })
            return response
        
        return render(request, 'product/create_modal.html', {'form': form})
```

### Step 3: HTML এ Modal Trigger বাটন যোগ করুন

```html
<!-- Single select এর জন্য create button -->
<button class="related-create-btn" 
        data-model="product" 
        data-field-name="category">
    + Add Product
</button>

<!-- Edit button -->
<button class="related-edit-btn" 
        data-model="product" 
        data-field-name="category">
    Edit Product
</button>

<!-- Direct modal trigger -->
<a href="/product/create/" class="modal-trigger">
    Create Product
</a>
```

---

## Features বিস্তারিত

### 1️⃣ Modal Open/Close
```javascript
// Any form এ close button click করলে automatically close হয়
<button type="button" onclick="closeModal()">Close</button>
```

### 2️⃣ Auto-Select নতুন Item
মডেল save হলে automatically select field এ নতুন item select হয়:
```javascript
// View থেকে এই response পাঠান:
response['HX-Trigger'] = json.dumps({
    'related:saved': {
        'parentField': 'category',  // Field name
        'option': {
            'id': product.id,
            'text': str(product)      // Display text
        },
        'message': 'Product তৈরি হয়েছে!'
    }
})
```

### 3️⃣ Nested Modals
একটি modal এর মধ্যে আরেকটি modal খুলুন:
```html
<!-- Modal 1 (Parent) -->
<select name="category">
    <option>-- Select --</option>
</select>
<button class="related-create-btn" data-model="subcategory">
    + Add Sub Category
</button>

<!-- যখন উপরের button click হয়, Modal 2 (Nested) খুলবে -->
```

**কী ঘটে:**
1. Parent modal এর state save হয়
2. Nested modal খুলে
3. Nested modal এ save করলে parent restore হয়
4. Auto-select কাজ করে

### 4️⃣ TomSelect Integration
Select elements automatically enhanced হয়:
```html
<!-- Single select -->
<select name="category" class="js-enhanced-select">
    <option>-- Search --</option>
</select>

<!-- Multiple select -->
<select name="tags" class="js-enhanced-multiselect" multiple>
    <option>-- Search --</option>
</select>
```

---

## সব Apps এ Apply করার জন্য

### App 1: Product
✅ `product/views.py` - Modal views যোগ করুন  
✅ `product/templates/` - Modal templates তৈরি করুন  

### App 2: User
✅ `user/views.py` - Modal views যোগ করুন  
✅ `user/templates/` - Modal templates তৈরি করুন  

### App 3: GlobalApp
✅ `globalapp/views.py` - Modal views যোগ করুন  
✅ `globalapp/templates/` - Modal templates তৈরি করুন  

### App 4: Dashboard
✅ `dashboard/views.py` - Modal views যোগ করুন  
✅ `dashboard/templates/` - Modal templates তৈরি করুন  

---

## Testing করুন

### Test 1: Simple Modal
```html
<a href="/product/create/" class="modal-trigger">Create Product</a>
```
✅ Modal open হবে  
✅ Form submit করলে modal close হবে  

### Test 2: Auto-Select
```html
<select name="product" class="js-enhanced-select">
    <!-- Options -->
</select>
<button class="related-create-btn" data-model="product">
    + Create
</button>
```
✅ Create করলে নতুন product auto-select হবে  

### Test 3: Nested Modal
```html
<!-- Parent select -->
<select name="category">
    <option>-- Select --</option>
</select>
<button class="related-create-btn" data-model="product">+ Create</button>

<!-- Product create modal এ আরেকটি nested modal -->
<select name="brand">
    <option>-- Select --</option>
</select>
<button class="related-create-btn" data-model="brand">+ Create</button>
```
✅ সব nested properly close হবে  
✅ সব values restore হবে  

---

## Troubleshooting

### সমস্যা: Modal open হচ্ছে না
**সমাধান:**
```html
<!-- Check করুন -->
✅ Script loaded: <script src="{% static 'js/modal-system.js' %}"></script>
✅ Modal HTML exists: <div id="modal-container">...</div>
✅ HTMX loaded: <script src="https://unpkg.com/htmx.org@1.9.12"></script>
```

### সমস্যা: Close button কাজ করছে না
**সমাধান:**
```html
<!-- এই onclick attribute নিশ্চিত করুন -->
<button type="button" onclick="closeModal()">Close</button>

<!-- অথবা modal-backdrop click -->
<div id="modal-backdrop"><!-- Backdrop --</div>
```

### সমস্যা: Auto-select কাজ করছে না
**সমাধান:**
```python
# View এ response header check করুন:
response['HX-Trigger'] = json.dumps({
    'related:saved': {
        'parentField': 'category_name',  # Form field এর নাম
        'option': {
            'id': obj.id,
            'text': str(obj)
        }
    }
})
```

---

## বেস্ট প্র্যাকটিস

✅ সর্বদা `data-parent_field` পাঠান  
✅ Modal form এ error handling করুন  
✅ Success message show করুন  
✅ Form state save করুন (nested modal এর জন্য)  
✅ TomSelect use করুন better UX এর জন্য  

---

## File Structure

```
static/js/
└── modal-system.js          ← নতুন system
    
templates/common/
├── universal_modal_form.html  ← সব forms এর জন্য
└── header.html

templates/base.html           ← Updated with new script
```

---

**Questions?** Check `modal-system.js` comments বা documentation পড়ুন।
