// // // // // // ═══════════════════════ SHARED MODAL HANDLER FUNCTIONS ═══════════════════════

// // // // // function openRelatedModal(modelName, action, pk = null, params = {}) {
// // // // //     let url = `/user/ajax/related/${modelName}/create/`;
// // // // //     if (action === 'edit' && pk) {
// // // // //         url = `/user/ajax/related/${modelName}/${pk}/edit/`;
// // // // //     }

// // // // //     const queryParams = new URLSearchParams();
// // // // //     for (const [key, value] of Object.entries(params)) {
// // // // //         if (value !== null && value !== undefined && value !== '') {
// // // // //             queryParams.append(key, value);
// // // // //         }
// // // // //     }
// // // // //     if (queryParams.toString()) {
// // // // //         url += '?' + queryParams.toString();
// // // // //     }

// // // // //     const modalBody = document.getElementById('modal-body');
// // // // //     const modalContainer = document.getElementById('modal-container');

// // // // //     if (!modalBody || !modalContainer) {
// // // // //         console.error('Modal elements not found');
// // // // //         return;
// // // // //     }

// // // // //     // nested modal state
// // // // //     window.modalStack = window.modalStack || [];
// // // // //     if (params.parent_field) {
// // // // //         window.modalStack.push({
// // // // //             html: modalBody.innerHTML,
// // // // //             parentFieldName: params.parent_field
// // // // //         });
// // // // //         window.nestedModalOpen = true;
// // // // //         window.parentFieldName = params.parent_field;
// // // // //     } else {
// // // // //         window.nestedModalOpen = false;
// // // // //         window.parentFieldName = null;
// // // // //     }

// // // // //     fetch(url, {
// // // // //         headers: { 'X-Requested-With': 'XMLHttpRequest' }
// // // // //     })
// // // // //     .then(async response => {
// // // // //         const data = await response.json();
// // // // //         console.log('Modal response:', data);
// // // // //         if (!response.ok) throw data;
// // // // //         return data;
// // // // //     })
// // // // //     .then(data => {
// // // // //         if (data.html) {
// // // // //             modalBody.innerHTML = data.html;

// // // // //             const form = modalBody.querySelector('form');
// // // // //             if (form) {
// // // // //                 form.dataset.modelName = modelName;
// // // // //                 form.dataset.isNested = params.parent_field ? 'true' : 'false';
// // // // //             } else {
// // // // //                 console.warn('No form found inside returned modal HTML');
// // // // //             }

// // // // //             modalContainer.classList.remove('hidden');
// // // // //         } else {
// // // // //             console.error('Response has no html:', data);
// // // // //             alert('Form HTML returned hoy nai');
// // // // //         }
// // // // //     })
// // // // //     .catch(error => {
// // // // //         console.error('Error loading modal:', error);
// // // // //         alert('Error loading form');
// // // // //     });
// // // // // }

// // // // // function restorePreviousModal() {
// // // // //     const modalBody = document.getElementById('modal-body');
// // // // //     if (!modalBody) return;

// // // // //     if (window.modalStack && window.modalStack.length > 0) {
// // // // //         const previous = window.modalStack.pop();
// // // // //         modalBody.innerHTML = previous.html;
// // // // //         window.parentFieldName = previous.parentFieldName || null;
// // // // //         window.nestedModalOpen = window.modalStack.length > 0;
// // // // //     } else {
// // // // //         closeModal();
// // // // //     }
// // // // // }

// // // // // function handleModalFormSubmit(form, event) {
// // // // //     event.preventDefault();

// // // // //     const formData = new FormData(form);
// // // // //     const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
// // // // //     const isNestedModal = form.dataset.isNested === 'true';
// // // // //     const modelName = form.dataset.modelName;
// // // // //     const parentFieldName = window.parentFieldName;

// // // // //     fetch(form.action, {
// // // // //         method: 'POST',
// // // // //         body: formData,
// // // // //         headers: {
// // // // //             'X-CSRFToken': csrfToken,
// // // // //             'X-Requested-With': 'XMLHttpRequest'
// // // // //         }
// // // // //     })
// // // // //     .then(async response => {
// // // // //         const data = await response.json();
// // // // //         if (!response.ok) throw data;
// // // // //         return data;
// // // // //     })
// // // // //     .then(data => {
// // // // //         if (data.success) {
// // // // //             if (isNestedModal && modelName && parentFieldName) {
// // // // //                 const itemData = data[modelName] || data.item;
// // // // //                 if (itemData) {
// // // // //                     autoSelectInParent(parentFieldName, modelName, itemData);
// // // // //                 }
// // // // //                 restorePreviousModal();
// // // // //             } else {
// // // // //                 closeModal();
// // // // //                 location.reload();
// // // // //             }
// // // // //         } else if (data.html) {
// // // // //             const modalBody = document.getElementById('modal-body');
// // // // //             modalBody.innerHTML = data.html;

// // // // //             const newForm = modalBody.querySelector('form');
// // // // //             if (newForm) {
// // // // //                 newForm.dataset.modelName = modelName;
// // // // //                 newForm.dataset.isNested = isNestedModal ? 'true' : 'false';
// // // // //             }
// // // // //         } else {
// // // // //             console.error('Unexpected submit response:', data);
// // // // //             alert('Unknown submit response');
// // // // //         }
// // // // //     })
// // // // //     .catch(error => {
// // // // //         console.error('Form submission error:', error);
// // // // //         if (error && error.html) {
// // // // //             const modalBody = document.getElementById('modal-body');
// // // // //             modalBody.innerHTML = error.html;
// // // // //         } else {
// // // // //             alert('Error submitting form');
// // // // //         }
// // // // //     });
// // // // // }

// // // // // function autoSelectInParent(fieldName, modelName, itemData) {
// // // // //     const modal = document.getElementById('modal-container');
// // // // //     let field = null;

// // // // //     if (modal && !modal.classList.contains('hidden')) {
// // // // //         field = modal.querySelector(`[name="${fieldName}"]`);
// // // // //     }
// // // // //     if (!field) {
// // // // //         field = document.querySelector(`[name="${fieldName}"]`);
// // // // //     }
// // // // //     if (!field) return;

// // // // //     const value = String(itemData.id);
// // // // //     const text = itemData.text || itemData.name || value;

// // // // //     if (field.tagName === 'SELECT') {
// // // // //         let existing = Array.from(field.options).find(opt => String(opt.value) === value);
// // // // //         if (!existing) {
// // // // //             existing = new Option(text, value, true, true);
// // // // //             field.add(existing);
// // // // //         } else {
// // // // //             existing.selected = true;
// // // // //         }
// // // // //         field.value = value;
// // // // //         field.dispatchEvent(new Event('change', { bubbles: true }));
// // // // //     }
// // // // // }

// // // // // function closeModal() {
// // // // //     const modal = document.getElementById('modal-container');
// // // // //     if (modal) modal.classList.add('hidden');

// // // // //     window.modalStack = [];
// // // // //     window.nestedModalOpen = false;
// // // // //     window.parentFieldName = null;
// // // // // }

// // // // // function buildModalParams(fieldName, modelName) {
// // // // //     return {
// // // // //         parent_field: fieldName,
// // // // //         model: modelName
// // // // //     };
// // // // // }

// // // // // function openEditRelatedFromField(fieldName, modelName) {
// // // // //     const modal = document.getElementById('modal-container');
// // // // //     let field = null;

// // // // //     if (modal && !modal.classList.contains('hidden')) {
// // // // //         field = modal.querySelector(`[name="${fieldName}"]`);
// // // // //     }
// // // // //     if (!field) {
// // // // //         field = document.querySelector(`[name="${fieldName}"]`);
// // // // //     }

// // // // //     if (!field || !field.value) {
// // // // //         alert('Please select an item first');
// // // // //         return;
// // // // //     }

// // // // //     openRelatedModal(modelName, 'edit', field.value, {
// // // // //         parent_field: fieldName
// // // // //     });
// // // // // }

// // // // // document.addEventListener('click', function(e) {
// // // // //     const createBtn = e.target.closest('.related-create-btn');
// // // // //     if (createBtn) {
// // // // //         e.preventDefault();
// // // // //         e.stopPropagation();

// // // // //         const modelName = createBtn.getAttribute('data-model');
// // // // //         const fieldName = createBtn.getAttribute('data-field-name');

// // // // //         if (modelName && fieldName) {
// // // // //             openRelatedModal(modelName, 'create', null, { parent_field: fieldName });
// // // // //         }
// // // // //     }
// // // // // });

// // // // // document.addEventListener('click', function(e) {
// // // // //     const editBtn = e.target.closest('.related-edit-btn');
// // // // //     if (editBtn) {
// // // // //         e.preventDefault();
// // // // //         e.stopPropagation();

// // // // //         const modelName = editBtn.getAttribute('data-model');
// // // // //         const fieldName = editBtn.getAttribute('data-field-name');

// // // // //         if (modelName && fieldName) {
// // // // //             openEditRelatedFromField(fieldName, modelName);
// // // // //         }
// // // // //     }
// // // // // });

// // // // // document.addEventListener('submit', function(e) {
// // // // //     const form = e.target;
// // // // //     const modal = document.getElementById('modal-container');

// // // // //     if (modal && modal.contains(form) && form.tagName === 'FORM') {
// // // // //         handleModalFormSubmit(form, e);
// // // // //     }
// // // // // });

// // // // // document.addEventListener('click', function(e) {
// // // // //     if (e.target.id === 'modal-backdrop') {
// // // // //         if (window.modalStack && window.modalStack.length > 0) {
// // // // //             restorePreviousModal();
// // // // //         } else {
// // // // //             closeModal();
// // // // //         }
// // // // //     }
// // // // // });



// // // // (function () {
// // // //     if (window.__modalHandlersInitialized) return;
// // // //     window.__modalHandlersInitialized = true;

// // // //     window.modalStack = window.modalStack || [];

// // // //     function getActiveField(fieldName) {
// // // //         const modal = document.getElementById('modal-container');
// // // //         if (modal && !modal.classList.contains('hidden')) {
// // // //             const insideModal = modal.querySelector(`[name="${fieldName}"]`);
// // // //             if (insideModal) return insideModal;
// // // //         }
// // // //         return document.querySelector(`[name="${fieldName}"]`);
// // // //     }

// // // //     window.openRelatedModal = function (modelName, action, pk = null, params = {}) {
// // // //         let url = `/user/ajax/related/${modelName}/create/`;
// // // //         if (action === 'edit' && pk) {
// // // //             url = `/user/ajax/related/${modelName}/${pk}/edit/`;
// // // //         }

// // // //         const queryParams = new URLSearchParams();
// // // //         Object.entries(params).forEach(([key, value]) => {
// // // //             if (value !== null && value !== undefined && value !== '') {
// // // //                 queryParams.append(key, value);
// // // //             }
// // // //         });
// // // //         if (queryParams.toString()) {
// // // //             url += `?${queryParams.toString()}`;
// // // //         }

// // // //         const modalBody = document.getElementById('modal-body');
// // // //         const modalContainer = document.getElementById('modal-container');
// // // //         if (!modalBody || !modalContainer) return;

// // // //         if (params.parent_field) {
// // // //             window.modalStack.push({
// // // //                 html: modalBody.innerHTML,
// // // //                 parentFieldName: params.parent_field
// // // //             });
// // // //             window.parentFieldName = params.parent_field;
// // // //         } else {
// // // //             window.modalStack = [];
// // // //             window.parentFieldName = null;
// // // //         }

// // // //         fetch(url, {
// // // //             headers: { 'X-Requested-With': 'XMLHttpRequest' }
// // // //         })
// // // //         .then(async response => {
// // // //             const data = await response.json();
// // // //             if (!response.ok) throw data;
// // // //             return data;
// // // //         })
// // // //         .then(data => {
// // // //             if (!data.html) {
// // // //                 console.error('No html returned', data);
// // // //                 return;
// // // //             }

// // // //             modalBody.innerHTML = data.html;

// // // //             const form = modalBody.querySelector('form');
// // // //             if (form) {
// // // //                 form.dataset.modelName = modelName;
// // // //                 form.dataset.isNested = params.parent_field ? 'true' : 'false';
// // // //             }

// // // //             modalContainer.classList.remove('hidden');
// // // //         })
// // // //         .catch(error => {
// // // //             console.error('Error loading modal:', error);
// // // //             alert('Error loading form');
// // // //         });
// // // //     };

// // // //     window.restorePreviousModal = function () {
// // // //         const modalBody = document.getElementById('modal-body');
// // // //         const modalContainer = document.getElementById('modal-container');
// // // //         if (!modalBody || !modalContainer) return;

// // // //         if (window.modalStack.length > 0) {
// // // //             const previous = window.modalStack.pop();
// // // //             modalBody.innerHTML = previous.html;
// // // //             window.parentFieldName = previous.parentFieldName || null;
// // // //         } else {
// // // //             modalContainer.classList.add('hidden');
// // // //             window.parentFieldName = null;
// // // //         }
// // // //     };

// // // //     window.autoSelectInParent = function (fieldName, modelName, itemData) {
// // // //         const field = getActiveField(fieldName);
// // // //         if (!field) return;

// // // //         const optionValue = String(itemData.id);
// // // //         const optionText = itemData.text || itemData.name || optionValue;

// // // //         if (field.tagName === 'SELECT') {
// // // //             let existing = Array.from(field.options).find(opt => String(opt.value) === optionValue);
// // // //             if (!existing) {
// // // //                 existing = new Option(optionText, optionValue, true, true);
// // // //                 field.add(existing);
// // // //             } else {
// // // //                 existing.selected = true;
// // // //                 existing.text = optionText;
// // // //             }
// // // //             field.value = optionValue;
// // // //             field.dispatchEvent(new Event('change', { bubbles: true }));
// // // //         }
// // // //     };

// // // //     window.handleModalFormSubmit = function (form, event) {
// // // //         event.preventDefault();
// // // //         event.stopPropagation();

// // // //         const formData = new FormData(form);
// // // //         const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
// // // //         const isNestedModal = form.dataset.isNested === 'true';
// // // //         const modelName = form.dataset.modelName;
// // // //         const parentFieldName = window.parentFieldName;

// // // //         fetch(form.action, {
// // // //             method: 'POST',
// // // //             body: formData,
// // // //             headers: {
// // // //                 'X-CSRFToken': csrfToken,
// // // //                 'X-Requested-With': 'XMLHttpRequest'
// // // //             }
// // // //         })
// // // //         .then(async response => {
// // // //             const data = await response.json();
// // // //             if (!response.ok) throw data;
// // // //             return data;
// // // //         })
// // // //         .then(data => {
// // // //             if (data.success) {
// // // //                 if (isNestedModal && parentFieldName) {
// // // //                     const itemData = data[modelName] || data.item;
// // // //                     if (itemData) {
// // // //                         window.autoSelectInParent(parentFieldName, modelName, itemData);
// // // //                     }
// // // //                     window.restorePreviousModal();
// // // //                 } else {
// // // //                     window.closeModal();
// // // //                     location.reload();
// // // //                 }
// // // //                 return;
// // // //             }

// // // //             if (data.html) {
// // // //                 const modalBody = document.getElementById('modal-body');
// // // //                 modalBody.innerHTML = data.html;

// // // //                 const newForm = modalBody.querySelector('form');
// // // //                 if (newForm) {
// // // //                     newForm.dataset.modelName = modelName;
// // // //                     newForm.dataset.isNested = isNestedModal ? 'true' : 'false';
// // // //                 }
// // // //             }
// // // //         })
// // // //         .catch(error => {
// // // //             console.error('Form submission error:', error);
// // // //             if (error && error.html) {
// // // //                 const modalBody = document.getElementById('modal-body');
// // // //                 modalBody.innerHTML = error.html;
// // // //             } else {
// // // //                 alert('Error submitting form');
// // // //             }
// // // //         });
// // // //     };

// // // //     window.buildModalParams = function (fieldName, modelName) {
// // // //         return {
// // // //             parent_field: fieldName,
// // // //             model: modelName
// // // //         };
// // // //     };

// // // //     window.openEditRelatedFromField = function (fieldName, modelName) {
// // // //         const field = getActiveField(fieldName);
// // // //         if (!field || !field.value) {
// // // //             alert('Please select an item first');
// // // //             return;
// // // //         }
// // // //         window.openRelatedModal(modelName, 'edit', field.value, {
// // // //             parent_field: fieldName
// // // //         });
// // // //     };

// // // //     window.closeModal = function () {
// // // //         const modal = document.getElementById('modal-container');
// // // //         if (modal) modal.classList.add('hidden');
// // // //         window.modalStack = [];
// // // //         window.parentFieldName = null;
// // // //     };

// // // //     document.addEventListener('click', function (e) {
// // // //         const createBtn = e.target.closest('.related-create-btn');
// // // //         if (createBtn) {
// // // //             e.preventDefault();
// // // //             e.stopPropagation();

// // // //             const modelName = createBtn.getAttribute('data-model');
// // // //             const fieldName = createBtn.getAttribute('data-field-name');

// // // //             if (modelName && fieldName) {
// // // //                 window.openRelatedModal(modelName, 'create', null, {
// // // //                     parent_field: fieldName
// // // //                 });
// // // //             }
// // // //             return;
// // // //         }

// // // //         const editBtn = e.target.closest('.related-edit-btn');
// // // //         if (editBtn) {
// // // //             e.preventDefault();
// // // //             e.stopPropagation();

// // // //             const modelName = editBtn.getAttribute('data-model');
// // // //             const fieldName = editBtn.getAttribute('data-field-name');

// // // //             if (modelName && fieldName) {
// // // //                 window.openEditRelatedFromField(fieldName, modelName);
// // // //             }
// // // //             return;
// // // //         }

// // // //         const trigger = e.target.closest('.modal-trigger');
// // // //         if (trigger) {
// // // //             e.preventDefault();
// // // //             e.stopPropagation();

// // // //             const url = trigger.getAttribute('data-modal-url');
// // // //             const modalBody = document.getElementById('modal-body');
// // // //             const modalContainer = document.getElementById('modal-container');
// // // //             if (!url || !modalBody || !modalContainer) return;

// // // //             fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
// // // //                 .then(async response => {
// // // //                     const data = await response.json();
// // // //                     if (!response.ok) throw data;
// // // //                     return data;
// // // //                 })
// // // //                 .then(data => {
// // // //                     if (data.html) {
// // // //                         modalBody.innerHTML = data.html;
// // // //                         modalContainer.classList.remove('hidden');
// // // //                     }
// // // //                 })
// // // //                 .catch(error => {
// // // //                     console.error('Error loading modal:', error);
// // // //                     alert('Error loading modal');
// // // //                 });
// // // //         }

// // // //         if (e.target.id === 'modal-backdrop') {
// // // //             if (window.modalStack.length > 0) {
// // // //                 window.restorePreviousModal();
// // // //             } else {
// // // //                 window.closeModal();
// // // //             }
// // // //         }
// // // //     });

// // // //     document.addEventListener('submit', function (e) {
// // // //         const modal = document.getElementById('modal-container');
// // // //         const form = e.target;

// // // //         if (modal && modal.contains(form) && form.tagName === 'FORM') {
// // // //             window.handleModalFormSubmit(form, e);
// // // //         }
// // // //     });
// // // // })();


// // // (function () {
// // //     if (window.__modalHandlersInitialized) return;
// // //     window.__modalHandlersInitialized = true;

// // //     window.modalStack = [];
// // //     window.parentFieldName = null;

// // //     function getModalElements() {
// // //         return {
// // //             container: document.getElementById('modal-container'),
// // //             body: document.getElementById('modal-body'),
// // //             backdrop: document.getElementById('modal-backdrop'),
// // //             content: document.getElementById('modal-content')
// // //         };
// // //     }

// // //     function getFieldValue(field) {
// // //         if (!field) return '';
// // //         if (field.tomselect) {
// // //             const value = field.tomselect.getValue();
// // //             if (Array.isArray(value)) return value.length ? value[0] : '';
// // //             return value || '';
// // //         }
// // //         if (typeof window.$ !== 'undefined' && window.$.fn.select2 && window.$(field).data('select2')) {
// // //             const value = window.$(field).val();
// // //             if (Array.isArray(value)) return value.length ? value[0] : '';
// // //             return value || '';
// // //         }
// // //         return field.value || '';
// // //     }

// // //     function getActiveField(fieldName) {
// // //         const { container } = getModalElements();

// // //         if (container && !container.classList.contains('hidden')) {
// // //             const insideModal = container.querySelector(`[name="${fieldName}"]`);
// // //             if (insideModal) return insideModal;
// // //         }

// // //         return document.querySelector(`[name="${fieldName}"]`);
// // //     }

// // //     function initEnhancedSelect(scope) {
// // //         const root = scope || document;

// // //         root.querySelectorAll('.js-enhanced-select').forEach(function (select) {
// // //             if (typeof window.$ !== 'undefined' && window.$.fn.select2) {
// // //                 if (window.$(select).data('select2')) {
// // //                     window.$(select).select2('destroy');
// // //                 }
// // //                 window.$(select).select2({
// // //                     theme: 'bootstrap-5',
// // //                     width: '100%',
// // //                     dropdownParent: window.$('#modal-content')
// // //                 });
// // //             }
// // //         });

// // //         root.querySelectorAll('.js-enhanced-multiselect').forEach(function (select) {
// // //             if (typeof window.$ !== 'undefined' && window.$.fn.select2) {
// // //                 if (window.$(select).data('select2')) {
// // //                     window.$(select).select2('destroy');
// // //                 }
// // //                 window.$(select).select2({
// // //                     theme: 'bootstrap-5',
// // //                     width: '100%',
// // //                     dropdownParent: window.$('#modal-content')
// // //                 });
// // //             }
// // //         });
// // //     }

// // //     function refreshParentSelectUi(field) {
// // //         if (!field) return;

// // //         if (field.tomselect) {
// // //             field.tomselect.sync();
// // //             field.tomselect.refreshOptions(false);
// // //             return;
// // //         }

// // //         if (typeof window.$ !== 'undefined' && window.$.fn.select2 && window.$(field).data('select2')) {
// // //             window.$(field).trigger('change.select2');
// // //             return;
// // //         }

// // //         field.dispatchEvent(new Event('change', { bubbles: true }));
// // //     }

// // //     window.buildModalParams = function (fieldName, modelName) {
// // //         const params = {
// // //             parent_field: fieldName,
// // //             model: modelName
// // //         };

// // //         const branchField = getActiveField('branch') || document.getElementById('id_branch');
// // //         const areaField = getActiveField('area') || document.getElementById('id_area');
// // //         const parentField = getActiveField('parent') || document.getElementById('id_parent');

// // //         if (branchField) params.branch_id = getFieldValue(branchField);
// // //         if (areaField) params.area_id = getFieldValue(areaField);
// // //         if (parentField && modelName === 'menu') params.parent_id = getFieldValue(parentField);

// // //         return params;
// // //     };

// // //     window.closeModal = function () {
// // //         const { container, body } = getModalElements();
// // //         if (container) container.classList.add('hidden');
// // //         if (body) body.innerHTML = '';
// // //         window.modalStack = [];
// // //         window.parentFieldName = null;
// // //     };

// // //     window.restorePreviousModal = function () {
// // //         const { container, body } = getModalElements();
// // //         if (!body) return;

// // //         if (window.modalStack.length > 0) {
// // //             const previous = window.modalStack.pop();
// // //             body.innerHTML = previous.html;
// // //             window.parentFieldName = previous.parentFieldName || null;
// // //             initEnhancedSelect(body);
// // //             if (container) container.classList.remove('hidden');
// // //         } else {
// // //             window.closeModal();
// // //         }
// // //     };

// // //     window.autoSelectInParent = function (fieldName, modelName, itemData) {
// // //         const field = getActiveField(fieldName);
// // //         if (!field || !itemData) return;

// // //         const optionValue = String(itemData.id);
// // //         const optionText = itemData.text || itemData.name || optionValue;

// // //         if (field.tagName === 'SELECT') {
// // //             let existing = Array.from(field.options).find(opt => String(opt.value) === optionValue);

// // //             if (!existing) {
// // //                 existing = new Option(optionText, optionValue, true, true);
// // //                 field.add(existing);
// // //             } else {
// // //                 existing.selected = true;
// // //                 existing.text = optionText;
// // //             }

// // //             if (field.multiple) {
// // //                 existing.selected = true;
// // //             } else {
// // //                 field.value = optionValue;
// // //             }

// // //             refreshParentSelectUi(field);
// // //         }
// // //     };

// // //     window.openRelatedModal = function (modelName, action, pk = null, params = {}) {
// // //         let url = `/user/ajax/related/${modelName}/create/`;
// // //         if (action === 'edit' && pk) {
// // //             url = `/user/ajax/related/${modelName}/${pk}/edit/`;
// // //         }

// // //         const queryParams = new URLSearchParams();
// // //         Object.entries(params).forEach(([key, value]) => {
// // //             if (value !== null && value !== undefined && value !== '') {
// // //                 queryParams.append(key, value);
// // //             }
// // //         });
// // //         if (queryParams.toString()) {
// // //             url += `?${queryParams.toString()}`;
// // //         }

// // //         const { container, body } = getModalElements();
// // //         if (!container || !body) return;

// // //         if (params.parent_field) {
// // //             window.modalStack.push({
// // //                 html: body.innerHTML,
// // //                 parentFieldName: params.parent_field
// // //             });
// // //             window.parentFieldName = params.parent_field;
// // //         } else {
// // //             window.modalStack = [];
// // //             window.parentFieldName = null;
// // //         }

// // //         fetch(url, {
// // //             headers: {
// // //                 'X-Requested-With': 'XMLHttpRequest'
// // //             }
// // //         })
// // //         .then(async response => {
// // //             const data = await response.json();
// // //             if (!response.ok) throw data;
// // //             return data;
// // //         })
// // //         .then(data => {
// // //             if (!data.html) {
// // //                 console.error('No html returned from modal endpoint', data);
// // //                 return;
// // //             }

// // //             body.innerHTML = data.html;

// // //             const form = body.querySelector('form');
// // //             if (form) {
// // //                 form.dataset.modelName = modelName;
// // //                 form.dataset.isNested = params.parent_field ? 'true' : 'false';
// // //             }

// // //             initEnhancedSelect(body);
// // //             container.classList.remove('hidden');
// // //         })
// // //         .catch(error => {
// // //             console.error('Error loading modal:', error);
// // //             alert('Error loading form');
// // //         });
// // //     };

// // //     window.openEditRelatedFromField = function (fieldName, modelName) {
// // //         const field = getActiveField(fieldName);
// // //         if (!field) {
// // //             alert('Field not found');
// // //             return;
// // //         }

// // //         const selectedValue = getFieldValue(field);
// // //         if (!selectedValue) {
// // //             alert('Please select an item first');
// // //             return;
// // //         }

// // //         window.openRelatedModal(modelName, 'edit', selectedValue, {
// // //             parent_field: fieldName
// // //         });
// // //     };

// // //     window.handleModalFormSubmit = function (form, event) {
// // //         event.preventDefault();
// // //         event.stopPropagation();

// // //         const formData = new FormData(form);
// // //         const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
// // //         const isNestedModal = form.dataset.isNested === 'true';
// // //         const modelName = form.dataset.modelName || '';
// // //         const parentFieldName = window.parentFieldName;

// // //         fetch(form.action, {
// // //             method: 'POST',
// // //             body: formData,
// // //             headers: {
// // //                 'X-CSRFToken': csrfToken,
// // //                 'X-Requested-With': 'XMLHttpRequest'
// // //             }
// // //         })
// // //         .then(async response => {
// // //             const data = await response.json();
// // //             if (!response.ok) throw data;
// // //             return data;
// // //         })
// // //         .then(data => {
// // //             if (data.success) {
// // //                 if (isNestedModal && parentFieldName) {
// // //                     const itemData = data[modelName] || data.item;
// // //                     if (itemData) {
// // //                         window.autoSelectInParent(parentFieldName, modelName, itemData);
// // //                     }
// // //                     window.restorePreviousModal();
// // //                 } else {
// // //                     window.closeModal();
// // //                     location.reload();
// // //                 }
// // //                 return;
// // //             }

// // //             if (data.html) {
// // //                 const { body, container } = getModalElements();
// // //                 if (!body) return;

// // //                 body.innerHTML = data.html;
// // //                 const newForm = body.querySelector('form');
// // //                 if (newForm) {
// // //                     newForm.dataset.modelName = modelName;
// // //                     newForm.dataset.isNested = isNestedModal ? 'true' : 'false';
// // //                 }
// // //                 initEnhancedSelect(body);
// // //                 if (container) container.classList.remove('hidden');
// // //             }
// // //         })
// // //         .catch(error => {
// // //             console.error('Form submission error:', error);

// // //             if (error && error.html) {
// // //                 const { body, container } = getModalElements();
// // //                 if (body) {
// // //                     body.innerHTML = error.html;
// // //                     const newForm = body.querySelector('form');
// // //                     if (newForm) {
// // //                         newForm.dataset.modelName = modelName;
// // //                         newForm.dataset.isNested = isNestedModal ? 'true' : 'false';
// // //                     }
// // //                     initEnhancedSelect(body);
// // //                 }
// // //                 if (container) container.classList.remove('hidden');
// // //             } else {
// // //                 alert('Error submitting form');
// // //             }
// // //         });
// // //     };

// // //     document.addEventListener('click', function (e) {
// // //         const createBtn = e.target.closest('.related-create-btn');
// // //         if (createBtn) {
// // //             e.preventDefault();
// // //             e.stopPropagation();

// // //             const modelName = createBtn.getAttribute('data-model');
// // //             const fieldName = createBtn.getAttribute('data-field-name');

// // //             if (modelName && fieldName) {
// // //                 window.openRelatedModal(modelName, 'create', null, window.buildModalParams(fieldName, modelName));
// // //             }
// // //             return;
// // //         }

// // //         const editBtn = e.target.closest('.related-edit-btn');
// // //         if (editBtn) {
// // //             e.preventDefault();
// // //             e.stopPropagation();

// // //             const modelName = editBtn.getAttribute('data-model');
// // //             const fieldName = editBtn.getAttribute('data-field-name');

// // //             if (modelName && fieldName) {
// // //                 window.openEditRelatedFromField(fieldName, modelName);
// // //             }
// // //             return;
// // //         }

// // //         const trigger = e.target.closest('.modal-trigger');
// // //         if (trigger) {
// // //             e.preventDefault();
// // //             e.stopPropagation();

// // //             const url = trigger.getAttribute('data-modal-url');
// // //             const { container, body } = getModalElements();

// // //             if (!url || !container || !body) return;

// // //             fetch(url, {
// // //                 headers: {
// // //                     'X-Requested-With': 'XMLHttpRequest'
// // //                 }
// // //             })
// // //             .then(async response => {
// // //                 const data = await response.json();
// // //                 if (!response.ok) throw data;
// // //                 return data;
// // //             })
// // //             .then(data => {
// // //                 if (data.html) {
// // //                     body.innerHTML = data.html;
// // //                     initEnhancedSelect(body);
// // //                     container.classList.remove('hidden');
// // //                 }
// // //             })
// // //             .catch(error => {
// // //                 console.error('Error loading modal:', error);
// // //                 alert('Error loading modal');
// // //             });
// // //             return;
// // //         }

// // //         if (e.target.id === 'modal-backdrop') {
// // //             if (window.modalStack.length > 0) {
// // //                 window.restorePreviousModal();
// // //             } else {
// // //                 window.closeModal();
// // //             }
// // //         }
// // //     });

// // //     document.addEventListener('submit', function (e) {
// // //         const { container } = getModalElements();
// // //         const form = e.target;

// // //         if (container && container.contains(form) && form.tagName === 'FORM') {
// // //             window.handleModalFormSubmit(form, e);
// // //         }
// // //     });

// // //     document.addEventListener('DOMContentLoaded', function () {
// // //         initEnhancedSelect(document);
// // //     });
// // // })();



// // // (function () {
// // //     if (window.__modalHandlersInitialized) return;
// // //     window.__modalHandlersInitialized = true;

// // //     window.modalStack = [];
// // //     window.parentFieldName = null;

// // //     function getModalElements() {
// // //         return {
// // //             container: document.getElementById('modal-container'),
// // //             body: document.getElementById('modal-body'),
// // //             backdrop: document.getElementById('modal-backdrop'),
// // //             content: document.getElementById('modal-content')
// // //         };
// // //     }

// // //     function getFieldValue(field) {
// // //         if (!field) return '';

// // //         if (typeof window.$ !== 'undefined' && window.$.fn.select2 && window.$(field).data('select2')) {
// // //             const value = window.$(field).val();
// // //             if (Array.isArray(value)) return value.length ? value[0] : '';
// // //             return value || '';
// // //         }

// // //         return field.value || '';
// // //     }

// // //     function getActiveField(fieldName) {
// // //         const { container } = getModalElements();

// // //         if (container && !container.classList.contains('hidden')) {
// // //             const insideModal = container.querySelector(`[name="${fieldName}"]`);
// // //             if (insideModal) return insideModal;
// // //         }

// // //         return document.querySelector(`[name="${fieldName}"]`);
// // //     }

// // //     function initEnhancedSelect(scope) {
// // //         const root = scope || document;

// // //         root.querySelectorAll('.js-enhanced-select').forEach(function (select) {
// // //             if (typeof window.$ !== 'undefined' && window.$.fn.select2) {
// // //                 if (window.$(select).data('select2')) {
// // //                     window.$(select).select2('destroy');
// // //                 }

// // //                 window.$(select).select2({
// // //                     theme: 'bootstrap-5',
// // //                     width: '100%',
// // //                     dropdownParent: window.$('#modal-content')
// // //                 });
// // //             }
// // //         });

// // //         root.querySelectorAll('.js-enhanced-multiselect').forEach(function (select) {
// // //             if (typeof window.$ !== 'undefined' && window.$.fn.select2) {
// // //                 if (window.$(select).data('select2')) {
// // //                     window.$(select).select2('destroy');
// // //                 }

// // //                 window.$(select).select2({
// // //                     theme: 'bootstrap-5',
// // //                     width: '100%',
// // //                     dropdownParent: window.$('#modal-content')
// // //                 });
// // //             }
// // //         });
// // //     }

// // //     function refreshFieldUi(field) {
// // //         if (!field) return;

// // //         if (typeof window.$ !== 'undefined' && window.$.fn.select2 && window.$(field).data('select2')) {
// // //             window.$(field).trigger('change');
// // //         } else {
// // //             field.dispatchEvent(new Event('change', { bubbles: true }));
// // //         }
// // //     }

// // //     window.buildModalParams = function (fieldName, modelName) {
// // //         const params = {
// // //             parent_field: fieldName,
// // //             model: modelName
// // //         };

// // //         const branchField = getActiveField('branch') || document.getElementById('id_branch');
// // //         const areaField = getActiveField('area') || document.getElementById('id_area');
// // //         const parentField = getActiveField('parent') || document.getElementById('id_parent');

// // //         if (branchField) params.branch_id = getFieldValue(branchField);
// // //         if (areaField) params.area_id = getFieldValue(areaField);
// // //         if (parentField && modelName === 'menu') params.parent_id = getFieldValue(parentField);

// // //         return params;
// // //     };

// // //     window.closeModal = function () {
// // //         const { container, body } = getModalElements();

// // //         if (container) container.classList.add('hidden');
// // //         if (body) body.innerHTML = '';

// // //         window.modalStack = [];
// // //         window.parentFieldName = null;
// // //     };

// // //     window.restorePreviousModal = function () {
// // //         const { container, body } = getModalElements();
// // //         if (!body) return;

// // //         if (window.modalStack.length > 0) {
// // //             const previous = window.modalStack.pop();
// // //             body.innerHTML = previous.html;
// // //             window.parentFieldName = previous.parentFieldName || null;
// // //             initEnhancedSelect(body);

// // //             if (container) container.classList.remove('hidden');
// // //         } else {
// // //             window.closeModal();
// // //         }
// // //     };

// // //     window.autoSelectInParent = function (fieldName, modelName, itemData) {
// // //         const field = getActiveField(fieldName);
// // //         if (!field || !itemData) return;

// // //         const optionValue = String(itemData.id);
// // //         const optionText = itemData.text || itemData.name || optionValue;

// // //         if (field.tagName === 'SELECT') {
// // //             let existing = Array.from(field.options).find(opt => String(opt.value) === optionValue);

// // //             if (!existing) {
// // //                 existing = new Option(optionText, optionValue, true, true);
// // //                 field.add(existing);
// // //             } else {
// // //                 existing.text = optionText;
// // //             }

// // //             if (field.multiple) {
// // //                 existing.selected = true;
// // //             } else {
// // //                 field.value = optionValue;
// // //             }

// // //             refreshFieldUi(field);
// // //         }
// // //     };

// // //     window.openRelatedModal = function (modelName, action, pk = null, params = {}) {
// // //         let url = `/user/ajax/related/${modelName}/create/`;

// // //         if (action === 'edit' && pk) {
// // //             url = `/user/ajax/related/${modelName}/${pk}/edit/`;
// // //         }

// // //         const queryParams = new URLSearchParams();
// // //         Object.entries(params).forEach(([key, value]) => {
// // //             if (value !== null && value !== undefined && value !== '') {
// // //                 queryParams.append(key, value);
// // //             }
// // //         });

// // //         if (queryParams.toString()) {
// // //             url += `?${queryParams.toString()}`;
// // //         }

// // //         const { container, body } = getModalElements();
// // //         if (!container || !body) return;

// // //         if (params.parent_field) {
// // //             window.modalStack.push({
// // //                 html: body.innerHTML,
// // //                 parentFieldName: params.parent_field
// // //             });
// // //             window.parentFieldName = params.parent_field;
// // //         } else {
// // //             window.modalStack = [];
// // //             window.parentFieldName = null;
// // //         }

// // //         fetch(url, {
// // //             headers: {
// // //                 'X-Requested-With': 'XMLHttpRequest'
// // //             }
// // //         })
// // //         .then(async response => {
// // //             const data = await response.json();
// // //             if (!response.ok) throw data;
// // //             return data;
// // //         })
// // //         .then(data => {
// // //             if (!data.html) {
// // //                 console.error('No html returned from modal endpoint', data);
// // //                 return;
// // //             }

// // //             body.innerHTML = data.html;

// // //             const form = body.querySelector('form');
// // //             if (form) {
// // //                 form.dataset.modelName = modelName;
// // //                 form.dataset.isNested = params.parent_field ? 'true' : 'false';
// // //             }

// // //             initEnhancedSelect(body);
// // //             container.classList.remove('hidden');
// // //         })
// // //         .catch(error => {
// // //             console.error('Error loading modal:', error);
// // //             alert('Error loading form');
// // //         });
// // //     };

// // //     window.openEditRelatedFromField = function (fieldName, modelName) {
// // //         const field = getActiveField(fieldName);
// // //         if (!field) {
// // //             alert('Field not found');
// // //             return;
// // //         }

// // //         const selectedValue = getFieldValue(field);
// // //         if (!selectedValue) {
// // //             alert('Please select an item first');
// // //             return;
// // //         }

// // //         window.openRelatedModal(modelName, 'edit', selectedValue, {
// // //             parent_field: fieldName
// // //         });
// // //     };

// // //     window.handleModalFormSubmit = function (form, event) {
// // //         event.preventDefault();
// // //         event.stopPropagation();

// // //         const formData = new FormData(form);
// // //         const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
// // //         const isNestedModal = form.dataset.isNested === 'true';
// // //         const modelName = form.dataset.modelName || '';
// // //         const parentFieldName = window.parentFieldName;

// // //         fetch(form.action, {
// // //             method: 'POST',
// // //             body: formData,
// // //             headers: {
// // //                 'X-CSRFToken': csrfToken,
// // //                 'X-Requested-With': 'XMLHttpRequest'
// // //             }
// // //         })
// // //         .then(async response => {
// // //             const data = await response.json();
// // //             if (!response.ok) throw data;
// // //             return data;
// // //         })
// // //         .then(data => {
// // //             if (data.success) {
// // //                 if (isNestedModal && parentFieldName) {
// // //                     const itemData = data[modelName] || data.item;
// // //                     if (itemData) {
// // //                         window.autoSelectInParent(parentFieldName, modelName, itemData);
// // //                     }
// // //                     window.restorePreviousModal();
// // //                 } else {
// // //                     window.closeModal();
// // //                     location.reload();
// // //                 }
// // //                 return;
// // //             }

// // //             if (data.html) {
// // //                 const { body, container } = getModalElements();
// // //                 if (!body) return;

// // //                 body.innerHTML = data.html;

// // //                 const newForm = body.querySelector('form');
// // //                 if (newForm) {
// // //                     newForm.dataset.modelName = modelName;
// // //                     newForm.dataset.isNested = isNestedModal ? 'true' : 'false';
// // //                 }

// // //                 initEnhancedSelect(body);
// // //                 if (container) container.classList.remove('hidden');
// // //             }
// // //         })
// // //         .catch(error => {
// // //             console.error('Form submission error:', error);

// // //             if (error && error.html) {
// // //                 const { body, container } = getModalElements();

// // //                 if (body) {
// // //                     body.innerHTML = error.html;

// // //                     const newForm = body.querySelector('form');
// // //                     if (newForm) {
// // //                         newForm.dataset.modelName = modelName;
// // //                         newForm.dataset.isNested = isNestedModal ? 'true' : 'false';
// // //                     }

// // //                     initEnhancedSelect(body);
// // //                 }

// // //                 if (container) container.classList.remove('hidden');
// // //             } else {
// // //                 alert('Error submitting form');
// // //             }
// // //         });
// // //     };

// // //     document.addEventListener('click', function (e) {
// // //         const createBtn = e.target.closest('.related-create-btn');
// // //         if (createBtn) {
// // //             e.preventDefault();
// // //             e.stopPropagation();

// // //             const modelName = createBtn.getAttribute('data-model');
// // //             const fieldName = createBtn.getAttribute('data-field-name');

// // //             if (modelName && fieldName) {
// // //                 window.openRelatedModal(modelName, 'create', null, window.buildModalParams(fieldName, modelName));
// // //             }
// // //             return;
// // //         }

// // //         const editBtn = e.target.closest('.related-edit-btn');
// // //         if (editBtn) {
// // //             e.preventDefault();
// // //             e.stopPropagation();

// // //             const modelName = editBtn.getAttribute('data-model');
// // //             const fieldName = editBtn.getAttribute('data-field-name');

// // //             if (modelName && fieldName) {
// // //                 window.openEditRelatedFromField(fieldName, modelName);
// // //             }
// // //             return;
// // //         }

// // //         const trigger = e.target.closest('.modal-trigger');
// // //         if (trigger) {
// // //             e.preventDefault();
// // //             e.stopPropagation();

// // //             const url = trigger.getAttribute('data-modal-url');
// // //             const { container, body } = getModalElements();

// // //             if (!url || !container || !body) return;

// // //             fetch(url, {
// // //                 headers: {
// // //                     'X-Requested-With': 'XMLHttpRequest'
// // //                 }
// // //             })
// // //             .then(async response => {
// // //                 const data = await response.json();
// // //                 if (!response.ok) throw data;
// // //                 return data;
// // //             })
// // //             .then(data => {
// // //                 if (data.html) {
// // //                     body.innerHTML = data.html;
// // //                     initEnhancedSelect(body);
// // //                     container.classList.remove('hidden');
// // //                 }
// // //             })
// // //             .catch(error => {
// // //                 console.error('Error loading modal:', error);
// // //                 alert('Error loading modal');
// // //             });
// // //             return;
// // //         }

// // //         if (e.target.id === 'modal-backdrop') {
// // //             if (window.modalStack.length > 0) {
// // //                 window.restorePreviousModal();
// // //             } else {
// // //                 window.closeModal();
// // //             }
// // //         }
// // //     });

// // //     document.addEventListener('submit', function (e) {
// // //         const { container } = getModalElements();
// // //         const form = e.target;

// // //         if (container && container.contains(form) && form.tagName === 'FORM') {
// // //             window.handleModalFormSubmit(form, e);
// // //         }
// // //     });

// // //     document.addEventListener('DOMContentLoaded', function () {
// // //         initEnhancedSelect(document);
// // //     });
// // // })();




// // (function () {
// //     if (window.__modalHandlersInitialized) return;
// //     window.__modalHandlersInitialized = true;

// //     window.modalStack = [];
// //     window.parentFieldName = null;

// //     function getModalElements() {
// //         return {
// //             container: document.getElementById('modal-container'),
// //             body: document.getElementById('modal-body'),
// //             backdrop: document.getElementById('modal-backdrop'),
// //             content: document.getElementById('modal-content')
// //         };
// //     }

// //     function getFieldValue(field) {
// //         if (!field) return '';

// //         if (typeof window.$ !== 'undefined' && window.$.fn.select2 && window.$(field).data('select2')) {
// //             const value = window.$(field).val();
// //             if (Array.isArray(value)) return value.length ? value[0] : '';
// //             return value || '';
// //         }

// //         return field.value || '';
// //     }

// //     function getActiveField(fieldName) {
// //         const { container } = getModalElements();

// //         if (container && !container.classList.contains('hidden')) {
// //             const insideModal = container.querySelector(`[name="${fieldName}"]`);
// //             if (insideModal) return insideModal;
// //         }

// //         return document.querySelector(`[name="${fieldName}"]`);
// //     }

// //     function initEnhancedSelect(scope) {
// //         const root = scope || document;

// //         root.querySelectorAll('.js-enhanced-select').forEach(function (select) {
// //             if (typeof window.$ !== 'undefined' && window.$.fn.select2) {
// //                 if (window.$(select).data('select2')) {
// //                     window.$(select).select2('destroy');
// //                 }

// //                 window.$(select).select2({
// //                     width: '100%',
// //                     dropdownParent: window.$('#modal-content'),
// //                     placeholder: select.getAttribute('data-placeholder') || 'Select option',
// //                     allowClear: true
// //                 });
// //             }
// //         });

// //         root.querySelectorAll('.js-enhanced-multiselect').forEach(function (select) {
// //             if (typeof window.$ !== 'undefined' && window.$.fn.select2) {
// //                 if (window.$(select).data('select2')) {
// //                     window.$(select).select2('destroy');
// //                 }

// //                 window.$(select).select2({
// //                     width: '100%',
// //                     dropdownParent: window.$('#modal-content'),
// //                     placeholder: select.getAttribute('data-placeholder') || 'Select option'
// //                 });
// //             }
// //         });
// //     }

// //     function appendOrSelectOption(field, value, text) {
// //         if (!field || field.tagName !== 'SELECT') return;

// //         let existing = Array.from(field.options).find(opt => String(opt.value) === String(value));

// //         if (!existing) {
// //             existing = new Option(text, value, false, false);
// //             field.add(existing);
// //         } else {
// //             existing.text = text;
// //         }

// //         if (field.multiple) {
// //             existing.selected = true;
// //             const values = Array.from(field.selectedOptions).map(opt => String(opt.value));
// //             if (!values.includes(String(value))) {
// //                 existing.selected = true;
// //             }
// //         } else {
// //             field.value = String(value);
// //             existing.selected = true;
// //         }

// //         if (typeof window.$ !== 'undefined' && window.$.fn.select2 && window.$(field).data('select2')) {
// //             if (field.multiple) {
// //                 const current = window.$(field).val() || [];
// //                 const currentValues = Array.isArray(current) ? current.map(String) : [String(current)];
// //                 if (!currentValues.includes(String(value))) {
// //                     currentValues.push(String(value));
// //                 }
// //                 window.$(field).val(currentValues).trigger('change');
// //             } else {
// //                 window.$(field).val(String(value)).trigger('change');
// //             }
// //         } else {
// //             field.dispatchEvent(new Event('change', { bubbles: true }));
// //         }
// //     }

// //     window.buildModalParams = function (fieldName, modelName) {
// //         const params = {
// //             parent_field: fieldName,
// //             model: modelName
// //         };

// //         const branchField = getActiveField('branch') || document.getElementById('id_branch');
// //         const areaField = getActiveField('area') || document.getElementById('id_area');
// //         const parentField = getActiveField('parent') || document.getElementById('id_parent');

// //         if (branchField) {
// //             const branchValue = getFieldValue(branchField);
// //             if (branchValue) params.branch_id = branchValue;
// //         }

// //         if (areaField) {
// //             const areaValue = getFieldValue(areaField);
// //             if (areaValue) params.area_id = areaValue;
// //         }

// //         if (parentField && modelName === 'menu') {
// //             const parentValue = getFieldValue(parentField);
// //             if (parentValue) params.parent_id = parentValue;
// //         }

// //         return params;
// //     };

// //     window.closeModal = function () {
// //         const { container, body } = getModalElements();

// //         if (container) container.classList.add('hidden');
// //         if (body) body.innerHTML = '';

// //         window.modalStack = [];
// //         window.parentFieldName = null;
// //     };

// //     window.restorePreviousModal = function () {
// //         const { container, body } = getModalElements();
// //         if (!body) return false;

// //         if (window.modalStack.length > 0) {
// //             const previous = window.modalStack.pop();
// //             body.innerHTML = previous.html;
// //             window.parentFieldName = previous.parentFieldName || null;
// //             initEnhancedSelect(body);

// //             if (container) container.classList.remove('hidden');
// //             return true;
// //         }

// //         window.closeModal();
// //         return false;
// //     };

// //     window.autoSelectInParent = function (fieldName, modelName, itemData) {
// //         const field = getActiveField(fieldName);
// //         if (!field || !itemData) return;

// //         const optionValue = String(itemData.id);
// //         const optionText = itemData.text || itemData.name || optionValue;

// //         if (field.tagName === 'SELECT') {
// //             appendOrSelectOption(field, optionValue, optionText);
// //         }
// //     };

// //     window.openRelatedModal = function (modelName, action, pk = null, params = {}) {
// //         let url = `/user/ajax/related/${modelName}/create/`;

// //         if (action === 'edit' && pk) {
// //             url = `/user/ajax/related/${modelName}/${pk}/edit/`;
// //         }

// //         const queryParams = new URLSearchParams();
// //         Object.entries(params).forEach(([key, value]) => {
// //             if (value !== null && value !== undefined && value !== '') {
// //                 queryParams.append(key, value);
// //             }
// //         });

// //         if (queryParams.toString()) {
// //             url += `?${queryParams.toString()}`;
// //         }

// //         const { container, body } = getModalElements();
// //         if (!container || !body) return;

// //         if (params.parent_field) {
// //             window.modalStack.push({
// //                 html: body.innerHTML,
// //                 parentFieldName: params.parent_field
// //             });
// //             window.parentFieldName = params.parent_field;
// //         } else {
// //             window.modalStack = [];
// //             window.parentFieldName = null;
// //         }

// //         fetch(url, {
// //             headers: {
// //                 'X-Requested-With': 'XMLHttpRequest'
// //             }
// //         })
// //         .then(async response => {
// //             const data = await response.json();
// //             if (!response.ok) throw data;
// //             return data;
// //         })
// //         .then(data => {
// //             if (!data.html) return;

// //             body.innerHTML = data.html;

// //             const form = body.querySelector('form');
// //             if (form) {
// //                 form.dataset.modelName = modelName;
// //                 form.dataset.isNested = params.parent_field ? 'true' : 'false';
// //             }

// //             initEnhancedSelect(body);
// //             container.classList.remove('hidden');
// //         })
// //         .catch(error => {
// //             console.error('Error loading modal:', error);
// //             alert('Error loading form');
// //         });
// //     };

// //     window.openEditRelatedFromField = function (fieldName, modelName) {
// //         const field = getActiveField(fieldName);
// //         if (!field) {
// //             alert('Field not found');
// //             return;
// //         }

// //         const selectedValue = getFieldValue(field);
// //         if (!selectedValue) {
// //             alert('Please select an item first');
// //             return;
// //         }

// //         window.openRelatedModal(modelName, 'edit', selectedValue, {
// //             parent_field: fieldName
// //         });
// //     };

// //     window.handleModalFormSubmit = function (form, event) {
// //         event.preventDefault();
// //         event.stopPropagation();

// //         const formData = new FormData(form);
// //         const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
// //         const isNestedModal = form.dataset.isNested === 'true';
// //         const modelName = form.dataset.modelName || '';
// //         const parentFieldName = window.parentFieldName;

// //         fetch(form.action, {
// //             method: 'POST',
// //             body: formData,
// //             headers: {
// //                 'X-CSRFToken': csrfToken,
// //                 'X-Requested-With': 'XMLHttpRequest'
// //             }
// //         })
// //         .then(async response => {
// //             const data = await response.json();
// //             if (!response.ok) throw data;
// //             return data;
// //         })
// //         .then(data => {
// //             if (data.success) {
// //                 if (isNestedModal && parentFieldName) {
// //                     const itemData = data[modelName] || data.item;

// //                     const restored = window.restorePreviousModal();
// //                     if (restored && itemData) {
// //                         window.autoSelectInParent(parentFieldName, modelName, itemData);
// //                     }
// //                 } else {
// //                     window.closeModal();
// //                     location.reload();
// //                 }
// //                 return;
// //             }

// //             if (data.html) {
// //                 const { body, container } = getModalElements();
// //                 if (!body) return;

// //                 body.innerHTML = data.html;

// //                 const newForm = body.querySelector('form');
// //                 if (newForm) {
// //                     newForm.dataset.modelName = modelName;
// //                     newForm.dataset.isNested = isNestedModal ? 'true' : 'false';
// //                 }

// //                 initEnhancedSelect(body);
// //                 if (container) container.classList.remove('hidden');
// //             }
// //         })
// //         .catch(error => {
// //             console.error('Form submission error:', error);

// //             if (error && error.html) {
// //                 const { body, container } = getModalElements();

// //                 if (body) {
// //                     body.innerHTML = error.html;

// //                     const newForm = body.querySelector('form');
// //                     if (newForm) {
// //                         newForm.dataset.modelName = modelName;
// //                         newForm.dataset.isNested = isNestedModal ? 'true' : 'false';
// //                     }

// //                     initEnhancedSelect(body);
// //                 }

// //                 if (container) container.classList.remove('hidden');
// //             } else {
// //                 alert('Error submitting form');
// //             }
// //         });
// //     };

// //     document.addEventListener('click', function (e) {
// //         const createBtn = e.target.closest('.related-create-btn');
// //         if (createBtn) {
// //             e.preventDefault();
// //             e.stopPropagation();

// //             const modelName = createBtn.getAttribute('data-model');
// //             const fieldName = createBtn.getAttribute('data-field-name');

// //             if (modelName && fieldName) {
// //                 window.openRelatedModal(modelName, 'create', null, window.buildModalParams(fieldName, modelName));
// //             }
// //             return;
// //         }

// //         const editBtn = e.target.closest('.related-edit-btn');
// //         if (editBtn) {
// //             e.preventDefault();
// //             e.stopPropagation();

// //             const modelName = editBtn.getAttribute('data-model');
// //             const fieldName = editBtn.getAttribute('data-field-name');

// //             if (modelName && fieldName) {
// //                 window.openEditRelatedFromField(fieldName, modelName);
// //             }
// //             return;
// //         }

// //         const trigger = e.target.closest('.modal-trigger');
// //         if (trigger) {
// //             e.preventDefault();
// //             e.stopPropagation();

// //             const url = trigger.getAttribute('data-modal-url');
// //             const { container, body } = getModalElements();

// //             if (!url || !container || !body) return;

// //             fetch(url, {
// //                 headers: {
// //                     'X-Requested-With': 'XMLHttpRequest'
// //                 }
// //             })
// //             .then(async response => {
// //                 const data = await response.json();
// //                 if (!response.ok) throw data;
// //                 return data;
// //             })
// //             .then(data => {
// //                 if (data.html) {
// //                     body.innerHTML = data.html;
// //                     initEnhancedSelect(body);
// //                     container.classList.remove('hidden');
// //                 }
// //             })
// //             .catch(error => {
// //                 console.error('Error loading modal:', error);
// //                 alert('Error loading modal');
// //             });
// //             return;
// //         }

// //         if (e.target.id === 'modal-backdrop') {
// //             if (window.modalStack.length > 0) {
// //                 window.restorePreviousModal();
// //             } else {
// //                 window.closeModal();
// //             }
// //         }
// //     });

// //     document.addEventListener('submit', function (e) {
// //         const { container } = getModalElements();
// //         const form = e.target;

// //         if (container && container.contains(form) && form.tagName === 'FORM') {
// //             window.handleModalFormSubmit(form, e);
// //         }
// //     });

// //     document.addEventListener('DOMContentLoaded', function () {
// //         initEnhancedSelect(document);
// //     });
// // })();







// (function () {
//     if (window.__modalHandlersInitialized) return;
//     window.__modalHandlersInitialized = true;

//     window.modalStack = [];
//     window.parentFieldName = null;
//     window.modalBusy = false;

//     function getModalElements() {
//         return {
//             container: document.getElementById('modal-container'),
//             body: document.getElementById('modal-body'),
//             backdrop: document.getElementById('modal-backdrop'),
//             content: document.getElementById('modal-content')
//         };
//     }

//     function getFieldElement(fieldName) {
//         const { container } = getModalElements();

//         if (container && !container.classList.contains('hidden')) {
//             const insideModal = container.querySelector(`[name="${fieldName}"]`);
//             if (insideModal) return insideModal;
//         }

//         return document.querySelector(`[name="${fieldName}"]`);
//     }

//     function getSelectedValue(fieldName) {
//         const field = getFieldElement(fieldName);
//         if (!field) return null;

//         if (typeof window.$ !== 'undefined' && window.$.fn.select2 && window.$(field).data('select2')) {
//             const value = window.$(field).val();
//             if (Array.isArray(value)) return value.length ? value[0] : null;
//             return value || null;
//         }

//         if (field.tagName === 'SELECT') {
//             return field.value || null;
//         }

//         if (field.type === 'checkbox') {
//             return field.checked ? field.value : null;
//         }

//         return field.value || null;
//     }

//     function getSelectedValues(fieldName) {
//         const field = getFieldElement(fieldName);
//         if (!field) return [];

//         if (typeof window.$ !== 'undefined' && window.$.fn.select2 && window.$(field).data('select2')) {
//             const value = window.$(field).val();
//             if (Array.isArray(value)) return value.filter(Boolean);
//             return value ? [value] : [];
//         }

//         if (field.tagName === 'SELECT' && field.multiple) {
//             return Array.from(field.selectedOptions).map(opt => opt.value).filter(Boolean);
//         }

//         return field.value ? [field.value] : [];
//     }

//     function initEnhancedSelect(scope) {
//         const root = scope || document;

//         root.querySelectorAll('.js-enhanced-select').forEach(function (select) {
//             if (typeof window.$ !== 'undefined' && window.$.fn.select2) {
//                 if (window.$(select).data('select2')) {
//                     window.$(select).select2('destroy');
//                 }

//                 window.$(select).select2({
//                     width: '100%',
//                     dropdownParent: window.$('#modal-content'),
//                     placeholder: select.getAttribute('data-placeholder') || 'Search and select',
//                     allowClear: true,
//                     minimumResultsForSearch: 0
//                 });
//             }
//         });

//         root.querySelectorAll('.js-enhanced-multiselect').forEach(function (select) {
//             if (typeof window.$ !== 'undefined' && window.$.fn.select2) {
//                 if (window.$(select).data('select2')) {
//                     window.$(select).select2('destroy');
//                 }

//                 window.$(select).select2({
//                     width: '100%',
//                     dropdownParent: window.$('#modal-content'),
//                     placeholder: select.getAttribute('data-placeholder') || 'Search and select',
//                     minimumResultsForSearch: 0
//                 });
//             }
//         });
//     }

//     function appendOrSelectOption(field, value, text) {
//         if (!field || field.tagName !== 'SELECT') return;

//         let existingOption = Array.from(field.options).find(opt => String(opt.value) === String(value));
//         if (!existingOption) {
//             existingOption = new Option(text, value, false, false);
//             field.add(existingOption);
//         } else {
//             existingOption.text = text;
//         }

//         if (field.multiple) {
//             existingOption.selected = true;
//         } else {
//             field.value = String(value);
//             existingOption.selected = true;
//         }

//         if (typeof window.$ !== 'undefined' && window.$.fn.select2 && window.$(field).data('select2')) {
//             if (field.multiple) {
//                 const current = window.$(field).val() || [];
//                 const currentValues = Array.isArray(current) ? current.map(String) : [String(current)];
//                 if (!currentValues.includes(String(value))) {
//                     currentValues.push(String(value));
//                 }
//                 window.$(field).val(currentValues).trigger('change');
//             } else {
//                 window.$(field).val(String(value)).trigger('change');
//             }
//         } else {
//             field.dispatchEvent(new Event('change', { bubbles: true }));
//         }
//     }

//     window.buildModalParams = function (fieldName, modelName) {
//         const params = {
//             parent_field: fieldName
//         };

//         const branchValue = getSelectedValue('branch');
//         const areaValue = getSelectedValue('area');
//         const parentValue = getSelectedValue('parent');

//         if (modelName === 'area' && branchValue) {
//             params.branch_id = branchValue;
//         }

//         if (modelName === 'customergroup') {
//             if (branchValue) params.branch_id = branchValue;
//             if (areaValue) params.area_id = areaValue;
//         }

//         if (modelName === 'menu' && parentValue) {
//             params.parent_id = parentValue;
//         }

//         return params;
//     };

//     window.closeModal = function () {
//         const { container, body } = getModalElements();
//         if (container) container.classList.add('hidden');
//         if (body) body.innerHTML = '';
//         window.modalStack = [];
//         window.parentFieldName = null;
//         window.modalBusy = false;
//     };

//     window.restorePreviousModal = function () {
//         const { container, body } = getModalElements();
//         if (!body) return false;

//         if (window.modalStack.length > 0) {
//             const previous = window.modalStack.pop();
//             body.innerHTML = previous.html;
//             window.parentFieldName = previous.parentFieldName || null;
//             initEnhancedSelect(body);

//             if (container) container.classList.remove('hidden');
//             window.modalBusy = false;
//             return true;
//         }

//         window.closeModal();
//         return false;
//     };

//     window.autoSelectInParent = function (fieldName, modelName, itemData) {
//         const field = getFieldElement(fieldName);
//         if (!field || !itemData) return;

//         const optionValue = String(itemData.id);
//         const optionText = itemData.text || itemData.name || optionValue;

//         if (field.tagName === 'SELECT') {
//             appendOrSelectOption(field, optionValue, optionText);
//         }
//     };

//     window.openRelatedModal = function (modelName, action, pk = null, params = {}) {
//         if (window.modalBusy) return;
//         window.modalBusy = true;

//         let url = `/user/ajax/related/${modelName}/create/`;
//         if (action === 'edit' && pk) {
//             url = `/user/ajax/related/${modelName}/${pk}/edit/`;
//         }

//         const queryParams = new URLSearchParams();
//         Object.entries(params).forEach(([key, value]) => {
//             if (value !== null && value !== undefined && value !== '') {
//                 queryParams.append(key, value);
//             }
//         });
//         if (queryParams.toString()) {
//             url += `?${queryParams.toString()}`;
//         }

//         const { container, body } = getModalElements();
//         if (!container || !body) {
//             window.modalBusy = false;
//             return;
//         }

//         if (params.parent_field) {
//             window.modalStack.push({
//                 html: body.innerHTML,
//                 parentFieldName: params.parent_field
//             });
//             window.parentFieldName = params.parent_field;
//         } else {
//             window.modalStack = [];
//             window.parentFieldName = null;
//         }

//         fetch(url, {
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest'
//             }
//         })
//         .then(async response => {
//             const data = await response.json();
//             if (!response.ok) throw data;
//             return data;
//         })
//         .then(data => {
//             if (!data.html) {
//                 throw new Error(data.message || 'Failed to load modal');
//             }

//             body.innerHTML = data.html;

//             const form = body.querySelector('form');
//             if (form) {
//                 form.dataset.modelName = modelName;
//                 form.dataset.isNested = params.parent_field ? 'true' : 'false';
//             }

//             initEnhancedSelect(body);
//             container.classList.remove('hidden');
//             window.modalBusy = false;
//         })
//         .catch(error => {
//             console.error('Error loading modal:', error);
//             alert(error.message || 'Error loading modal');
//             window.modalBusy = false;
//         });
//     };

//     window.openEditRelatedFromField = function (fieldName, modelName) {
//         const field = getFieldElement(fieldName);
//         if (!field) {
//             alert('Target field not found.');
//             return;
//         }

//         let selectedValue = null;

//         if (field.multiple) {
//             const values = getSelectedValues(fieldName);
//             if (values.length !== 1) {
//                 alert('Edit করতে exactly 1টা item select করতে হবে.');
//                 return;
//             }
//             selectedValue = values[0];
//         } else {
//             selectedValue = getSelectedValue(fieldName);
//             if (!selectedValue) {
//                 alert('আগে একটা item select করো.');
//                 return;
//             }
//         }

//         window.openRelatedModal(modelName, 'edit', selectedValue, {
//             parent_field: fieldName
//         });
//     };

//     window.handleModalFormSubmit = function (form, event) {
//         event.preventDefault();
//         event.stopPropagation();

//         const formData = new FormData(form);
//         const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
//         const isNestedModal = form.dataset.isNested === 'true';
//         const modelName = form.dataset.modelName || '';
//         const parentFieldName = window.parentFieldName;

//         fetch(form.action, {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-CSRFToken': csrfToken,
//                 'X-Requested-With': 'XMLHttpRequest'
//             }
//         })
//         .then(async response => {
//             const data = await response.json();
//             if (!response.ok) throw data;
//             return data;
//         })
//         .then(data => {
//             if (data.success) {
//                 if (isNestedModal && parentFieldName) {
//                     const itemData = data[modelName] || data.item;
//                     const restored = window.restorePreviousModal();

//                     if (restored && itemData) {
//                         window.autoSelectInParent(parentFieldName, modelName, itemData);
//                     }
//                 } else {
//                     window.closeModal();
//                     location.reload();
//                 }
//                 return;
//             }

//             if (data.html) {
//                 const { body, container } = getModalElements();
//                 if (!body) return;

//                 body.innerHTML = data.html;

//                 const newForm = body.querySelector('form');
//                 if (newForm) {
//                     newForm.dataset.modelName = modelName;
//                     newForm.dataset.isNested = isNestedModal ? 'true' : 'false';
//                 }

//                 initEnhancedSelect(body);
//                 if (container) container.classList.remove('hidden');
//             }
//         })
//         .catch(error => {
//             console.error('Form submission error:', error);

//             if (error && error.html) {
//                 const { body, container } = getModalElements();

//                 if (body) {
//                     body.innerHTML = error.html;

//                     const newForm = body.querySelector('form');
//                     if (newForm) {
//                         newForm.dataset.modelName = modelName;
//                         newForm.dataset.isNested = isNestedModal ? 'true' : 'false';
//                     }

//                     initEnhancedSelect(body);
//                 }

//                 if (container) container.classList.remove('hidden');
//             } else {
//                 alert(error.message || 'Error submitting form');
//             }
//         });
//     };

//     document.addEventListener('click', function (e) {
//         const createBtn = e.target.closest('.related-create-btn');
//         if (createBtn) {
//             e.preventDefault();
//             e.stopPropagation();

//             const modelName = createBtn.getAttribute('data-model');
//             const fieldName = createBtn.getAttribute('data-field-name');

//             if (modelName && fieldName) {
//                 window.openRelatedModal(modelName, 'create', null, window.buildModalParams(fieldName, modelName));
//             }
//             return;
//         }

//         const editBtn = e.target.closest('.related-edit-btn');
//         if (editBtn) {
//             e.preventDefault();
//             e.stopPropagation();

//             const modelName = editBtn.getAttribute('data-model');
//             const fieldName = editBtn.getAttribute('data-field-name');

//             if (modelName && fieldName) {
//                 window.openEditRelatedFromField(fieldName, modelName);
//             }
//             return;
//         }

//         const trigger = e.target.closest('.modal-trigger');
//         if (trigger) {
//             e.preventDefault();
//             e.stopPropagation();

//             const url = trigger.getAttribute('data-modal-url');
//             const { container, body } = getModalElements();

//             if (!url || !container || !body || window.modalBusy) return;
//             window.modalBusy = true;

//             fetch(url, {
//                 headers: {
//                     'X-Requested-With': 'XMLHttpRequest'
//                 }
//             })
//             .then(async response => {
//                 const data = await response.json();
//                 if (!response.ok) throw data;
//                 return data;
//             })
//             .then(data => {
//                 if (!data.html) {
//                     throw new Error(data.message || 'Failed to load modal');
//                 }

//                 body.innerHTML = data.html;
//                 initEnhancedSelect(body);
//                 container.classList.remove('hidden');
//                 window.modalBusy = false;
//             })
//             .catch(error => {
//                 console.error('Error loading modal:', error);
//                 alert(error.message || 'Error loading modal');
//                 window.modalBusy = false;
//             });
//             return;
//         }

//         if (e.target.id === 'modal-backdrop') {
//             if (window.modalStack.length > 0) {
//                 window.restorePreviousModal();
//             } else {
//                 window.closeModal();
//             }
//         }
//     });

//     document.addEventListener('submit', function (e) {
//         const { container } = getModalElements();
//         const form = e.target;

//         if (container && container.contains(form) && form.tagName === 'FORM') {
//             window.handleModalFormSubmit(form, e);
//         }
//     });

//     document.addEventListener('DOMContentLoaded', function () {
//         initEnhancedSelect(document);
//     });
// })();


(function () {
    if (window.__modalHandlersInitialized) return;
    window.__modalHandlersInitialized = true;

    window.modalStack = [];
    window.parentFieldName = null;
    window.modalBusy = false;

    function getModalElements() {
        return {
            container: document.getElementById('modal-container'),
            body: document.getElementById('modal-body'),
            backdrop: document.getElementById('modal-backdrop'),
            content: document.getElementById('modal-content')
        };
    }

    function getFieldElement(fieldName) {
        const { container } = getModalElements();

        if (container && !container.classList.contains('hidden')) {
            const insideModal = container.querySelector(`[name="${fieldName}"]`);
            if (insideModal) return insideModal;
        }

        return document.querySelector(`[name="${fieldName}"]`) || document.getElementById(fieldName);
    }

    function getSelectedValue(fieldName) {
        const field = getFieldElement(fieldName);
        if (!field) return null;

        if (typeof window.$ !== 'undefined' && window.$.fn.select2 && window.$(field).data('select2')) {
            const value = window.$(field).val();
            if (Array.isArray(value)) return value.length ? value[0] : null;
            return value || null;
        }

        if (field.tomselect) {
            const value = field.tomselect.getValue();
            if (Array.isArray(value)) return value.length ? value[0] : null;
            return value || null;
        }

        if (field.tagName === 'SELECT') return field.value || null;
        return field.value || null;
    }

    function getSelectedValues(fieldName) {
        const field = getFieldElement(fieldName);
        if (!field) return [];

        if (typeof window.$ !== 'undefined' && window.$.fn.select2 && window.$(field).data('select2')) {
            const value = window.$(field).val();
            if (Array.isArray(value)) return value.filter(Boolean);
            return value ? [value] : [];
        }

        if (field.tomselect) {
            const value = field.tomselect.getValue();
            if (Array.isArray(value)) return value.filter(Boolean);
            return value ? [value] : [];
        }

        if (field.tagName === 'SELECT' && field.multiple) {
            return Array.from(field.selectedOptions).map(opt => opt.value).filter(Boolean);
        }

        return field.value ? [field.value] : [];
    }

    function initEnhancedSelect(scope) {
        const root = scope || document;

        root.querySelectorAll('.js-enhanced-select').forEach(function (select) {
            if (typeof window.$ !== 'undefined' && window.$.fn.select2) {
                if (window.$(select).data('select2')) {
                    window.$(select).select2('destroy');
                }

                window.$(select).select2({
                    width: '100%',
                    dropdownParent: window.$('#modal-content').length ? window.$('#modal-content') : window.$('body'),
                    placeholder: select.getAttribute('data-placeholder') || 'Search and select',
                    allowClear: true,
                    minimumResultsForSearch: 0
                });
            }
        });

        root.querySelectorAll('.js-enhanced-multiselect').forEach(function (select) {
            if (typeof window.$ !== 'undefined' && window.$.fn.select2) {
                if (window.$(select).data('select2')) {
                    window.$(select).select2('destroy');
                }

                window.$(select).select2({
                    width: '100%',
                    dropdownParent: window.$('#modal-content').length ? window.$('#modal-content') : window.$('body'),
                    placeholder: select.getAttribute('data-placeholder') || 'Search and select',
                    minimumResultsForSearch: 0
                });
            }
        });
    }

    function appendOrSelectOption(field, value, text) {
        if (!field || field.tagName !== 'SELECT') return;

        const stringValue = String(value);
        const label = String(text || value);

        let option = Array.from(field.options).find(opt => String(opt.value) === stringValue);

        if (!option) {
            option = new Option(label, stringValue, false, false);
            field.add(option);
        } else {
            option.text = label;
        }

        if (field.multiple) {
            option.selected = true;
        } else {
            field.value = stringValue;
            option.selected = true;
        }

        if (field.tomselect) {
            if (!field.tomselect.options[stringValue]) {
                field.tomselect.addOption({ value: stringValue, text: label });
            } else {
                field.tomselect.updateOption(stringValue, { value: stringValue, text: label });
            }

            if (field.multiple) {
                const current = field.tomselect.getValue();
                const currentValues = Array.isArray(current) ? current.map(String) : (current ? [String(current)] : []);
                if (!currentValues.includes(stringValue)) currentValues.push(stringValue);
                field.tomselect.setValue(currentValues, true);
            } else {
                field.tomselect.setValue(stringValue, true);
            }

            field.tomselect.refreshOptions(false);
            return;
        }

        if (typeof window.$ !== 'undefined' && window.$.fn.select2 && window.$(field).data('select2')) {
            if (field.multiple) {
                const current = window.$(field).val() || [];
                const currentValues = Array.isArray(current) ? current.map(String) : [String(current)];
                if (!currentValues.includes(stringValue)) currentValues.push(stringValue);
                window.$(field).val(currentValues).trigger('change');
            } else {
                window.$(field).val(stringValue).trigger('change');
            }
        } else {
            field.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }

    function getItemFromResponse(modelName, data) {
        return (
            data[modelName] ||
            data.item ||
            data.branch ||
            data.area ||
            data.customergroup ||
            data.customer_group ||
            data.role ||
            data.menu ||
            data.user ||
            data.multibranch ||
            data.mult_branch ||
            null
        );
    }

    window.buildModalParams = function (fieldName, modelName) {
        const params = {
            parent_field: fieldName
        };

        const branchValue = getSelectedValue('branch') || getSelectedValue('id_branch');
        const areaValue = getSelectedValue('area') || getSelectedValue('id_area');
        const parentValue = getSelectedValue('parent') || getSelectedValue('id_parent');

        if (modelName === 'area' && branchValue) {
            params.branch_id = branchValue;
        }

        if (modelName === 'customergroup') {
            if (branchValue) params.branch_id = branchValue;
            if (areaValue) params.area_id = areaValue;
        }

        if (modelName === 'menu' && parentValue) {
            params.parent_id = parentValue;
        }

        return params;
    };

    window.closeModal = function () {
        const { container, body } = getModalElements();
        if (container) container.classList.add('hidden');
        if (body) body.innerHTML = '';
        window.modalStack = [];
        window.parentFieldName = null;
        window.modalBusy = false;
    };

    window.restorePreviousModal = function () {
        const { container, body } = getModalElements();
        if (!body) return false;

        if (window.modalStack.length > 0) {
            const previous = window.modalStack.pop();
            body.innerHTML = previous.html;
            window.parentFieldName = previous.parentFieldName || null;
            initEnhancedSelect(body);

            if (container) container.classList.remove('hidden');
            window.modalBusy = false;
            return true;
        }

        window.closeModal();
        return false;
    };

    window.autoSelectInParent = function (fieldName, modelName, itemData) {
        const field = getFieldElement(fieldName);
        if (!field || !itemData) return;

        const optionValue = String(itemData.id);
        const optionText = itemData.text || itemData.name || `${itemData.id}`;

        if (field.tagName === 'SELECT') {
            appendOrSelectOption(field, optionValue, optionText);
        }
    };

    window.openRelatedModal = function (modelName, action, pk = null, params = {}) {
        if (window.modalBusy) return;
        window.modalBusy = true;

        let url = `/user/ajax/related/${modelName}/create/`;
        if (action === 'edit' && pk) {
            url = `/user/ajax/related/${modelName}/${pk}/edit/`;
        }

        const queryParams = new URLSearchParams();
        Object.entries(params).forEach(([key, value]) => {
            if (value !== null && value !== undefined && value !== '') {
                queryParams.append(key, value);
            }
        });
        if (queryParams.toString()) {
            url += `?${queryParams.toString()}`;
        }

        const { container, body } = getModalElements();
        if (!container || !body) {
            window.modalBusy = false;
            return;
        }

        if (params.parent_field) {
            window.modalStack.push({
                html: body.innerHTML,
                parentFieldName: params.parent_field
            });
            window.parentFieldName = params.parent_field;
        } else {
            window.modalStack = [];
            window.parentFieldName = null;
        }

        fetch(url, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(async response => {
            const data = await response.json();
            if (!response.ok) throw data;
            return data;
        })
        .then(data => {
            if (!data.html) throw new Error(data.message || 'Failed to load modal');

            body.innerHTML = data.html;

            const form = body.querySelector('form');
            if (form) {
                form.dataset.modelName = modelName;
                form.dataset.isNested = params.parent_field ? 'true' : 'false';
            }

            initEnhancedSelect(body);
            container.classList.remove('hidden');
            window.modalBusy = false;
        })
        .catch(error => {
            console.error('Error loading modal:', error);
            alert(error.message || 'Error loading modal');
            window.modalBusy = false;
        });
    };

    window.openEditRelatedFromField = function (fieldName, modelName) {
        const field = getFieldElement(fieldName);
        if (!field) {
            alert('Target field not found.');
            return;
        }

        let selectedValue = null;

        if (field.multiple) {
            const values = getSelectedValues(fieldName);
            if (values.length !== 1) {
                alert('Edit করতে exactly 1টা item select করতে হবে.');
                return;
            }
            selectedValue = values[0];
        } else {
            selectedValue = getSelectedValue(fieldName);
            if (!selectedValue) {
                alert('আগে একটা item select করো.');
                return;
            }
        }

        window.openRelatedModal(modelName, 'edit', selectedValue, {
            parent_field: fieldName
        });
    };

    window.handleModalFormSubmit = function (form, event) {
        event.preventDefault();
        event.stopPropagation();

        const formData = new FormData(form);
        const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
        const isNestedModal = form.dataset.isNested === 'true';
        const modelName = form.dataset.modelName || '';
        const parentFieldName = window.parentFieldName;

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(async response => {
            const data = await response.json();
            if (!response.ok) throw data;
            return data;
        })
        .then(data => {
            if (data.success) {
                if (isNestedModal && parentFieldName) {
                    const itemData = getItemFromResponse(modelName, data);
                    const restored = window.restorePreviousModal();

                    if (restored && itemData) {
                        window.autoSelectInParent(parentFieldName, modelName, itemData);
                    }
                } else {
                    window.closeModal();
                    location.reload();
                }
                return;
            }

            if (data.html) {
                const { body, container } = getModalElements();
                if (!body) return;

                body.innerHTML = data.html;

                const newForm = body.querySelector('form');
                if (newForm) {
                    newForm.dataset.modelName = modelName;
                    newForm.dataset.isNested = isNestedModal ? 'true' : 'false';
                }

                initEnhancedSelect(body);
                if (container) container.classList.remove('hidden');
            }
        })
        .catch(error => {
            console.error('Form submission error:', error);

            if (error && error.html) {
                const { body, container } = getModalElements();

                if (body) {
                    body.innerHTML = error.html;

                    const newForm = body.querySelector('form');
                    if (newForm) {
                        newForm.dataset.modelName = modelName;
                        newForm.dataset.isNested = isNestedModal ? 'true' : 'false';
                    }

                    initEnhancedSelect(body);
                }

                if (container) container.classList.remove('hidden');
            } else {
                alert(error.message || 'Error submitting form');
            }
        });
    };

    document.addEventListener('click', function (e) {
        const createBtn = e.target.closest('.related-create-btn');
        if (createBtn) {
            e.preventDefault();
            e.stopPropagation();

            const modelName = createBtn.getAttribute('data-model');
            const fieldName = createBtn.getAttribute('data-field-name');

            if (modelName && fieldName) {
                window.openRelatedModal(modelName, 'create', null, window.buildModalParams(fieldName, modelName));
            }
            return;
        }

        const editBtn = e.target.closest('.related-edit-btn');
        if (editBtn) {
            e.preventDefault();
            e.stopPropagation();

            const modelName = editBtn.getAttribute('data-model');
            const fieldName = editBtn.getAttribute('data-field-name');

            if (modelName && fieldName) {
                window.openEditRelatedFromField(fieldName, modelName);
            }
            return;
        }

        const trigger = e.target.closest('.modal-trigger');
        if (trigger) {
            e.preventDefault();
            e.stopPropagation();

            const url = trigger.getAttribute('data-modal-url');
            const { container, body } = getModalElements();

            if (!url || !container || !body || window.modalBusy) return;
            window.modalBusy = true;

            fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(async response => {
                const data = await response.json();
                if (!response.ok) throw data;
                return data;
            })
            .then(data => {
                if (!data.html) throw new Error(data.message || 'Failed to load modal');

                body.innerHTML = data.html;
                initEnhancedSelect(body);
                container.classList.remove('hidden');
                window.modalBusy = false;
            })
            .catch(error => {
                console.error('Error loading modal:', error);
                alert(error.message || 'Error loading modal');
                window.modalBusy = false;
            });
            return;
        }

        if (e.target.id === 'modal-backdrop') {
            if (window.modalStack.length > 0) {
                window.restorePreviousModal();
            } else {
                window.closeModal();
            }
        }
    });

    document.addEventListener('submit', function (e) {
        const { container } = getModalElements();
        const form = e.target;

        if (container && container.contains(form) && form.tagName === 'FORM') {
            window.handleModalFormSubmit(form, e);
        }
    });

    document.addEventListener('DOMContentLoaded', function () {
        initEnhancedSelect(document);
    });
})();