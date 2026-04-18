"""
Product App - Modal Implementation Example

এই file আপনাকে দেখায় কীভাবে modal system implement করতে হয়।
সব apps এ একই pattern follow করুন।
"""

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
import json

from .models import Product
from .forms import ProductForm


class ProductCreateModalView(LoginRequiredMixin, View):
    """
    Product create করার জন্য modal view
    
    Features:
    - Form display করে
    - Form submission handle করে
    - Auto-select support
    - Proper error handling
    """
    
    def get(self, request):
        """Modal form render করুন"""
        form = ProductForm()
        
        # এখানে যে ফিল্ড থেকে এই modal open হয়েছে
        parent_field = request.GET.get('parent_field', '')
        
        return render(request, 'product/create_modal.html', {
            'form': form,
            'title': 'নতুন Product যোগ করুন',
            'post_url': request.path,
            'model_name': 'product',
            'parent_field': parent_field,
        })
    
    def post(self, request):
        """Form submit handle করুন এবং auto-select trigger পাঠান"""
        form = ProductForm(request.POST, request.FILES)
        parent_field = request.POST.get('_parent_field', '')
        
        if form.is_valid():
            # সংরক্ষণ করুন
            product = form.save(commit=True)
            
            # Modal বন্ধ করুন এবং parent এ auto-select করুন
            response = HttpResponse()
            
            # HX-Trigger header set করুন
            response['HX-Trigger'] = json.dumps({
                'related:saved': {
                    'parentField': parent_field,
                    'option': {
                        'id': product.id,
                        'text': str(product)  # Product এর name
                    },
                    'message': f'"{product}" successfully created!'
                }
            })
            
            return response
        
        # Error case - form আবার render করুন
        return render(request, 'product/create_modal.html', {
            'form': form,
            'title': 'নতুন Product যোগ করুন',
            'post_url': request.path,
            'model_name': 'product',
            'parent_field': parent_field,
        })


class ProductEditModalView(LoginRequiredMixin, View):
    """
    Existing product edit করার জন্য modal view
    """
    
    def get(self, request, pk):
        """Edit form render করুন"""
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        parent_field = request.GET.get('parent_field', '')
        
        return render(request, 'product/edit_modal.html', {
            'form': form,
            'product': product,
            'title': f'Edit: {product.name}',
            'post_url': request.path,
            'model_name': 'product',
            'parent_field': parent_field,
        })
    
    def post(self, request, pk):
        """Update handle করুন"""
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)
        parent_field = request.POST.get('_parent_field', '')
        
        if form.is_valid():
            form.save()
            
            response = HttpResponse()
            response['HX-Trigger'] = json.dumps({
                'related:saved': {
                    'parentField': parent_field,
                    'option': {
                        'id': product.id,
                        'text': str(product)
                    },
                    'message': f'"{product}" successfully updated!'
                }
            })
            
            return response
        
        return render(request, 'product/edit_modal.html', {
            'form': form,
            'product': product,
            'title': f'Edit: {product.name}',
            'post_url': request.path,
            'model_name': 'product',
            'parent_field': parent_field,
        })


# URLs file এ যোগ করুন:
"""
from django.urls import path
from .views import ProductCreateModalView, ProductEditModalView

urlpatterns = [
    # ... existing patterns ...
    
    path('ajax/related/product/create/', ProductCreateModalView.as_view(), name='product_create_modal'),
    path('ajax/related/product/<int:pk>/edit/', ProductEditModalView.as_view(), name='product_edit_modal'),
]
"""


# Template file example (product/create_modal.html):
"""
{% extends 'base.html' %}

{% block content %}
    {% include 'common/universal_modal_form.html' with 
        title=title
        post_url=post_url
        model_name=model_name
        parent_field=parent_field
        form=form
        form_partial_template='product/_form_fields.html'
    %}
{% endblock %}
"""


# Product form partial (product/_form_fields.html):
"""
<!-- এখানে শুধু form fields থাকবে, form tag না -->

<div class="space-y-4">
    <div>
        <label class="block text-sm font-medium text-gray-700">
            Product Name *
        </label>
        {{ form.name }}
        {% if form.name.errors %}
            <ul class="mt-1 text-sm text-red-600">
                {% for error in form.name.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>

    <div>
        <label class="block text-sm font-medium text-gray-700">
            Category *
        </label>
        {{ form.category }}
        {% if form.category.errors %}
            <ul class="mt-1 text-sm text-red-600">
                {% for error in form.category.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>

    <div>
        <label class="block text-sm font-medium text-gray-700">
            Price *
        </label>
        {{ form.price }}
        {% if form.price.errors %}
            <ul class="mt-1 text-sm text-red-600">
                {% for error in form.price.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>

    <div>
        <label class="block text-sm font-medium text-gray-700">
            Description
        </label>
        {{ form.description }}
    </div>
</div>
"""


# HTML form এ যেখানে modal trigger থাকবে:
"""
<div class="space-y-4">
    <div>
        <label class="block text-sm font-medium mb-2">Product *</label>
        
        <div class="flex gap-2">
            <select name="product" class="js-enhanced-select flex-1">
                <option value="">-- Select Product --</option>
                {% for product in products %}
                    <option value="{{ product.id }}">{{ product.name }}</option>
                {% endfor %}
            </select>
            
            <!-- Create button -->
            <button type="button" 
                    class="related-create-btn px-4 py-2 bg-blue-600 text-white rounded"
                    data-model="product"
                    data-field-name="product">
                + Create
            </button>
            
            <!-- Edit button -->
            <button type="button" 
                    class="related-edit-btn px-4 py-2 bg-green-600 text-white rounded"
                    data-model="product"
                    data-field-name="product">
                ✎ Edit
            </button>
        </div>
    </div>
</div>
"""
