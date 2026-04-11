# SweetAlert2 Integration Guide

## Overview
Beautiful alerts are now integrated across your entire site using SweetAlert2. Automatic integration with Django's Messages Framework.

## Usage Examples

### 1. **Using Django Messages Framework (Automatic)**
In your Django views, use standard Django messages:

```python
from django.contrib import messages

# Success Message
messages.success(request, "User created successfully!")

# Error Message
messages.error(request, "An error occurred!")

# Warning Message
messages.warning(request, "Please verify your email!")

# Info Message
messages.info(request, "Here is some information.")
```

These will automatically display as SweetAlert2 notifications!

### 2. **Manual JavaScript Alerts**
In your HTML/JavaScript templates, use these functions:

#### Success Alert
```html
<script>
  showSuccess('Success!', 'Your data has been saved.');
</script>
```

#### Error Alert
```html
<script>
  showError('Error!', 'Something went wrong. Please try again.');
</script>
```

#### Warning Alert
```html
<script>
  showWarning('Warning!', 'Are you sure about this action?');
</script>
```

#### Info Alert
```html
<script>
  showInfo('Information', 'Here is some useful information.');
</script>
```

#### Generic Alert
```html
<script>
  showAlert('Hello', 'This is a custom message', 'question', 'Got it!');
</script>
```

### 3. **Confirmation Dialog**
```html
<!-- HTML Button -->
<button onclick="showConfirm('Delete?', 'This action cannot be undone!', function(confirmed) {
  if (confirmed) {
    // Handle confirmation
    console.log('User confirmed!');
  }
})">Delete Item</button>
```

### 4. **Delete Confirmation (Special)**
```html
<button onclick="showDeleteConfirm('Delete User?', 'The user will be permanently removed.', function(confirmed) {
  if (confirmed) {
    // Submit delete form
    document.getElementById('deleteForm').submit();
  }
})">Delete</button>
```

### 5. **Loading Alert**
```html
<script>
  showLoading('Processing...', 'Please wait while we process your request.');
  
  // After some operation
  setTimeout(() => {
    closeAlert();
    showSuccess('Done!', 'Your request has been processed.');
  }, 3000);
</script>
```

### 6. **Form Submission with Confirmation**
```html
<form id="myForm" method="POST">
  {% csrf_token %}
  <!-- form fields -->
  <button type="button" onclick="confirmSubmit('myForm', 'Are you sure you want to save these changes?')">
    Save
  </button>
</form>
```

## Available Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `showSuccess(title, text)` | Show success alert | `showSuccess('Done!', 'Saved successfully')` |
| `showError(title, text)` | Show error alert | `showError('Error!', 'Something went wrong')` |
| `showWarning(title, text)` | Show warning alert | `showWarning('Warning!', 'Proceed with caution')` |
| `showInfo(title, text)` | Show info alert | `showInfo('Info', 'Here is info')` |
| `showAlert(title, text, icon, button)` | Generic alert | `showAlert('Hello', 'Message', 'info', 'OK')` |
| `showConfirm(title, text, callback)` | Confirmation dialog | `showConfirm('Sure?', 'Text', function(confirmed){})` |
| `showDeleteConfirm(title, text, callback)` | Delete confirmation | `showDeleteConfirm('Delete?', 'Text', callback)` |
| `showLoading(title, text)` | Loading alert | `showLoading('Loading...', 'Please wait')` |
| `closeAlert()` | Close current alert | `closeAlert()` |
| `confirmSubmit(formId, message)` | Confirm before submit | `confirmSubmit('myForm', 'Save?')` |

## Customization

To customize colors or behavior, edit `/static/js/alerts.js` and modify the `confirmButtonColor` properties:

- `#10b981` - Green (Success)
- `#ef4444` - Red (Error)
- `#f59e0b` - Amber (Warning)
- `#3b82f6` - Blue (Info)

## Examples in Views

```python
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

class YourView(View):
    def post(self, request):
        try:
            # Do something
            obj = Model.objects.create(...)
            messages.success(request, "Item created successfully!")
            return redirect('success_url')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('error_url')
```

## Bootstrap Integration

The alerts work seamlessly with your existing Bootstrap/Tailwind CSS. No additional styling needed!

## Troubleshooting

**Q: Alerts not showing?**
- Ensure SweetAlert2 CDN is loaded in base.html
- Check that `/static/js/alerts.js` is included
- Verify messages are being passed from the view

**Q: Custom styling not working?**
- SweetAlert2 CSS is automatically included via CDN
- Modify the JavaScript functions in alerts.js to change colors

**Q: Alerts closing too fast?**
- Success alerts auto-close after 2 seconds (timer: 2000)
- Remove/modify the `timer` in alerts.js to change this
