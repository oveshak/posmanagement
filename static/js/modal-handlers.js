
// // (function () {
// //     const modalStack = [];
// //     let lastHandledSaveSignature = null;
// //     let lastHandledSaveAt = 0;

// //     function appPrefix() {
// //         const fromBody = (document.body?.dataset?.appPrefix || "").trim();
// //         if (fromBody) return fromBody.replace(/\/$/, "");
// //         if (window.location.pathname.startsWith("/user/")) return "/user";
// //         return "";
// //     }

// //     function getModalContainer() {
// //         return document.getElementById("modal-container");
// //     }

// //     function getModalBody() {
// //         return document.getElementById("modal-body");
// //     }

// //     function showModal() {
// //         const modal = getModalContainer();
// //         if (modal) modal.classList.remove("hidden");
// //     }

// //     function hideModal() {
// //         const modal = getModalContainer();
// //         if (modal) modal.classList.add("hidden");
// //     }

// //     function currentModalForm() {
// //         const body = getModalBody();
// //         if (!body) return null;
// //         return body.querySelector("form");
// //     }

// //     function getCsrfToken() {
// //         const cookieValue = document.cookie
// //             .split("; ")
// //             .find(row => row.startsWith("csrftoken="))
// //             ?.split("=")[1];

// //         if (cookieValue) return decodeURIComponent(cookieValue);
// //         return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || "";
// //     }

// //     function findField(fieldName, root = null) {
// //         const base = root || currentModalForm() || document;
// //         return base.querySelector(`[name="${fieldName}"]`) || document.querySelector(`[name="${fieldName}"]`);
// //     }

// //     function captureFormState(root = null) {
// //         const form = root?.querySelector?.("form") || currentModalForm();
// //         if (!form) return {};

// //         const state = {};

// //         form.querySelectorAll("input, select, textarea").forEach((el) => {
// //             if (!el.name) return;

// //             if (el.type === "checkbox") {
// //                 if (el.name.endsWith("[]")) {
// //                     if (!state[el.name]) state[el.name] = [];
// //                     if (el.checked) state[el.name].push(el.value);
// //                 } else {
// //                     state[el.name] = !!el.checked;
// //                 }
// //                 return;
// //             }

// //             if (el.type === "radio") {
// //                 if (el.checked) state[el.name] = el.value;
// //                 return;
// //             }

// //             if (el.tagName === "SELECT" && el.multiple) {
// //                 state[el.name] = Array.from(el.selectedOptions).map(opt => String(opt.value));
// //                 return;
// //             }

// //             if (el.type !== "file") {
// //                 state[el.name] = el.value;
// //             }
// //         });

// //         return state;
// //     }

// //     function captureSelectOptions(root = null) {
// //         const form = root?.querySelector?.("form") || currentModalForm() || root || document;
// //         const snapshot = {};

// //         if (!form?.querySelectorAll) return snapshot;

// //         form.querySelectorAll("select[name]").forEach((select) => {
// //             const name = select.name;
// //             snapshot[name] = {
// //                 multiple: !!select.multiple,
// //                 options: Array.from(select.options).map((opt) => ({
// //                     value: String(opt.value),
// //                     text: opt.text,
// //                     selected: !!opt.selected
// //                 }))
// //             };
// //         });

// //         return snapshot;
// //     }

// //     function restoreSelectOptions(root = null, snapshot = {}) {
// //         const form = root?.querySelector?.("form") || currentModalForm() || root || document;
// //         if (!form) return;

// //         Object.entries(snapshot).forEach(([name, config]) => {
// //             const select = form.querySelector(`select[name="${name}"]`);
// //             if (!select) return;

// //             const currentPlaceholder = Array.from(select.options).find(
// //                 (opt) => opt.value === "" && !config.options.some(o => o.value === "")
// //             );

// //             select.innerHTML = "";

// //             if (currentPlaceholder) {
// //                 select.add(new Option(currentPlaceholder.text, currentPlaceholder.value, false, false));
// //             }

// //             config.options.forEach((optData) => {
// //                 const opt = new Option(
// //                     optData.text,
// //                     optData.value,
// //                     false,
// //                     !!optData.selected
// //                 );
// //                 select.add(opt);
// //             });

// //             refreshTomSelect(select);
// //         });
// //     }

// //     function restoreFormState(root = null, state = {}) {
// //         const form = root?.querySelector?.("form") || currentModalForm();
// //         if (!form) return;

// //         Object.entries(state).forEach(([name, value]) => {
// //             const elements = form.querySelectorAll(`[name="${name}"]`);
// //             if (!elements.length) return;

// //             elements.forEach((el) => {
// //                 if (el.type === "checkbox") {
// //                     if (Array.isArray(value)) {
// //                         el.checked = value.includes(el.value);
// //                     } else {
// //                         el.checked = !!value;
// //                     }
// //                     return;
// //                 }

// //                 if (el.type === "radio") {
// //                     el.checked = String(el.value) === String(value);
// //                     return;
// //                 }

// //                 if (el.tagName === "SELECT" && el.multiple) {
// //                     const values = Array.isArray(value) ? value.map(String) : [];
// //                     Array.from(el.options).forEach((opt) => {
// //                         opt.selected = values.includes(String(opt.value));
// //                     });

// //                     if (el.tomselect) {
// //                         el.tomselect.setValue(values, true);
// //                         el.tomselect.refreshItems();
// //                         el.tomselect.refreshOptions(false);
// //                     }
// //                     return;
// //                 }

// //                 if (el.tagName === "SELECT") {
// //                     const strValue = value == null ? "" : String(value);

// //                     let option = Array.from(el.options).find(opt => String(opt.value) === strValue);
// //                     if (!option && strValue !== "") {
// //                         option = new Option(strValue, strValue, true, true);
// //                         el.add(option);
// //                     }

// //                     el.value = strValue;

// //                     if (el.tomselect) {
// //                         if (strValue === "") {
// //                             el.tomselect.clear(true);
// //                         } else {
// //                             el.tomselect.addOption({ value: strValue, text: option?.text || strValue });
// //                             el.tomselect.setValue(strValue, true);
// //                         }
// //                         el.tomselect.refreshItems();
// //                         el.tomselect.refreshOptions(false);
// //                     }
// //                     return;
// //                 }

// //                 if (el.type !== "file") {
// //                     el.value = value ?? "";
// //                 }
// //             });
// //         });
// //     }

// //     function destroyTomSelectInstances(root = document) {
// //         root.querySelectorAll("select.js-enhanced-select, select.js-enhanced-multiselect").forEach((el) => {
// //             if (el.tomselect) {
// //                 el.tomselect.destroy();
// //             }
// //         });
// //     }

// //     // function initTomSelect(root = document) {
// //     //     root.querySelectorAll("select.js-enhanced-select").forEach((el) => {
// //     //         if (el.tomselect) return;
// //     //         new TomSelect(el, {
// //     //             create: false,
// //     //             allowEmptyOption: true,
// //     //             placeholder: el.dataset.placeholder || "Search...",
// //     //             maxOptions: 500,
// //     //             plugins: ["dropdown_input", "clear_button"],
// //     //         });
// //     //     });

// //     //     root.querySelectorAll("select.js-enhanced-multiselect").forEach((el) => {
// //     //         if (el.tomselect) return;
// //     //         new TomSelect(el, {
// //     //             create: false,
// //     //             plugins: ["remove_button", "clear_button"],
// //     //             placeholder: el.dataset.placeholder || "Search...",
// //     //             maxOptions: 500,
// //     //         });
// //     //     });
// //     // }



// //     function initTomSelect(root = document) {
// //     root.querySelectorAll("select.js-enhanced-select").forEach((el) => {
// //         const initialValue = el.dataset.selectedValue || el.value || "";

// //         if (el.tomselect) {
// //             if (initialValue !== "") {
// //                 el.tomselect.setValue(String(initialValue), true);
// //                 el.tomselect.refreshItems();
// //                 el.tomselect.refreshOptions(false);
// //             }
// //             return;
// //         }

// //         const control = new TomSelect(el, {
// //             create: false,
// //             allowEmptyOption: true,
// //             placeholder: el.dataset.placeholder || "Search...",
// //             maxOptions: 500,
// //             plugins: ["dropdown_input", "clear_button"],
// //         });

// //         if (initialValue !== "") {
// //             control.setValue(String(initialValue), true);
// //             control.refreshItems();
// //             control.refreshOptions(false);
// //         }
// //     });

// //     root.querySelectorAll("select.js-enhanced-multiselect").forEach((el) => {
// //         const initialValues =
// //             (el.dataset.selectedValue || "")
// //                 .split(",")
// //                 .map(v => v.trim())
// //                 .filter(Boolean);

// //         if (el.tomselect) {
// //             if (initialValues.length) {
// //                 el.tomselect.setValue(initialValues, true);
// //                 el.tomselect.refreshItems();
// //                 el.tomselect.refreshOptions(false);
// //             }
// //             return;
// //         }

// //         const control = new TomSelect(el, {
// //             create: false,
// //             plugins: ["remove_button", "clear_button"],
// //             placeholder: el.dataset.placeholder || "Search...",
// //             maxOptions: 500,
// //         });

// //         if (initialValues.length) {
// //             control.setValue(initialValues, true);
// //             control.refreshItems();
// //             control.refreshOptions(false);
// //         }
// //     });
// // }


// //     function refreshTomSelect(select) {
// //         if (!select || !select.tomselect) return;

// //         const selectedValues = Array.from(select.selectedOptions).map(opt => String(opt.value));
// //         select.tomselect.clear(true);
// //         select.tomselect.clearOptions();

// //         Array.from(select.options).forEach((opt) => {
// //             select.tomselect.addOption({
// //                 value: String(opt.value),
// //                 text: opt.text
// //             });
// //         });

// //         if (select.multiple) {
// //             select.tomselect.setValue(selectedValues, true);
// //         } else {
// //             select.tomselect.setValue(select.value ? String(select.value) : "", true);
// //         }

// //         select.tomselect.refreshItems();
// //         select.tomselect.refreshOptions(false);
// //     }

// //     function setSingleSelectValue(select, value, text, silent = false) {
// //         if (!select) return false;

// //         value = String(value);

// //         let existing = Array.from(select.options).find(opt => String(opt.value) === value);
// //         if (!existing) {
// //             existing = new Option(text, value, true, true);
// //             select.add(existing);
// //         } else {
// //             existing.text = text;
// //             existing.selected = true;
// //         }

// //         select.value = value;

// //         if (select.tomselect) {
// //             select.tomselect.addOption({ value, text });
// //             select.tomselect.setValue(value, silent);
// //             select.tomselect.refreshItems();
// //             select.tomselect.refreshOptions(false);
// //         }

// //         if (!silent) {
// //             select.dispatchEvent(new Event("change", { bubbles: true }));
// //             select.dispatchEvent(new Event("input", { bubbles: true }));
// //         }

// //         return String(select.value) === value;
// //     }

// //     function addMultiSelectValue(select, value, text, silent = false) {
// //         if (!select) return false;

// //         value = String(value);

// //         let existing = Array.from(select.options).find(opt => String(opt.value) === value);
// //         if (!existing) {
// //             existing = new Option(text, value, true, true);
// //             select.add(existing);
// //         } else {
// //             existing.text = text;
// //             existing.selected = true;
// //         }

// //         if (select.tomselect) {
// //             select.tomselect.addOption({ value, text });

// //             const current = select.tomselect.getValue();
// //             const arr = Array.isArray(current) ? current : (current ? [current] : []);
// //             const next = [...new Set([...arr.map(String), value])];

// //             select.tomselect.setValue(next, silent);
// //             select.tomselect.refreshItems();
// //             select.tomselect.refreshOptions(false);
// //         } else {
// //             existing.selected = true;
// //         }

// //         if (!silent) {
// //             select.dispatchEvent(new Event("change", { bubbles: true }));
// //             select.dispatchEvent(new Event("input", { bubbles: true }));
// //         }

// //         return Array.from(select.selectedOptions).some(opt => String(opt.value) === value);
// //     }

// //     function upsertRelatedOption(fieldName, option, root = null, silent = false) {
// //         const select = findField(fieldName, root);
// //         if (!select || !option) return false;

// //         const value = String(option.id);
// //         const text = option.text || value;

// //         if (select.multiple) {
// //             return addMultiSelectValue(select, value, text, silent);
// //         }
// //         return setSingleSelectValue(select, value, text, silent);
// //     }

// //     function ensureRelatedOptionSelected(fieldName, option, root = null, tries = 15, delay = 220, silent = false) {
// //         let attempt = 0;

// //         function run() {
// //             attempt += 1;
// //             const ok = upsertRelatedOption(fieldName, option, root, silent);
// //             if (ok) return;

// //             if (attempt < tries) {
// //                 setTimeout(run, delay);
// //             }
// //         }

// //         run();
// //     }

// //     function clearBindingMarkers(root) {
// //         if (!root?.querySelectorAll) return;

// //         root.querySelectorAll("[data-bound-click], [data-bound-dependent]").forEach((el) => {
// //             el.removeAttribute("data-bound-click");
// //             el.removeAttribute("data-bound-dependent");
// //         });
// //     }

// //     function getCleanHtmlForStack(root) {
// //         const wrapper = document.createElement("div");
// //         wrapper.innerHTML = root.innerHTML;
// //         clearBindingMarkers(wrapper);
// //         return wrapper.innerHTML;
// //     }

// //     async function fetchJSON(url) {
// //         const response = await fetch(url, {
// //             credentials: "same-origin",
// //             headers: { "X-Requested-With": "XMLHttpRequest" }
// //         });
// //         if (!response.ok) throw new Error("Request failed");
// //         return await response.json();
// //     }

// //     function parseHXTriggerHeader(xhr) {
// //         if (!xhr) return null;

// //         const triggerHeader = xhr.getResponseHeader("HX-Trigger");
// //         if (!triggerHeader) return null;

// //         try {
// //             return JSON.parse(triggerHeader);
// //         } catch (error) {
// //             console.warn("Invalid HX-Trigger header:", triggerHeader);
// //             return null;
// //         }
// //     }

// //     function extractRelatedSavedDetail(triggers) {
// //         if (!triggers) return null;
// //         return triggers["related:saved"] || triggers["crud:saved"] || null;
// //     }

// //     function isDuplicateSaveEvent(detail) {
// //         if (!detail) return false;

// //         const signature = JSON.stringify({
// //             parentField: detail.parentField || "",
// //             optionId: detail.option?.id ?? "",
// //             optionText: detail.option?.text ?? "",
// //             message: detail.message || ""
// //         });

// //         const now = Date.now();
// //         const isDup = signature === lastHandledSaveSignature && (now - lastHandledSaveAt) < 1200;

// //         if (!isDup) {
// //             lastHandledSaveSignature = signature;
// //             lastHandledSaveAt = now;
// //         }

// //         return isDup;
// //     }

// //     function getSelectedValue(fieldName, root = null) {
// //         const el = findField(fieldName, root);
// //         if (!el) return "";
// //         return el.value || "";
// //     }


// //     async function loadAreaOptions(branchId, selectedIds = [], root = null) {
// //     const areaSelect = findField("area", root);
// //     if (!areaSelect) return;

// //     const selectedStrings = (selectedIds || []).map(String);

// //     const currentTomValue = areaSelect.tomselect
// //         ? areaSelect.tomselect.getValue()
// //         : areaSelect.value;

// //     const currentValue = Array.isArray(currentTomValue)
// //         ? (currentTomValue[0] || "")
// //         : String(currentTomValue || "");

// //     const preferredValue =
// //         selectedStrings[0] ||
// //         areaSelect.dataset.selectedValue ||
// //         currentValue ||
// //         "";

// //     const preservedOptions = captureSelectOptions(root);
// //     const areaSnapshot = preservedOptions.area || null;

// //     if (!branchId) {
// //         areaSelect.innerHTML = '<option value="">---------</option>';

// //         if (areaSnapshot?.options?.length) {
// //             areaSnapshot.options.forEach((opt) => {
// //                 if (String(opt.value) !== "") {
// //                     const shouldSelect =
// //                         String(opt.value) === String(preferredValue) || !!opt.selected;

// //                     areaSelect.add(
// //                         new Option(opt.text, opt.value, false, shouldSelect)
// //                     );
// //                 }
// //             });
// //         }

// //         areaSelect.dataset.selectedValue = preferredValue ? String(preferredValue) : "";
// //         refreshTomSelect(areaSelect);

// //         if (preferredValue) {
// //             setSingleSelectValue(
// //                 areaSelect,
// //                 String(preferredValue),
// //                 Array.from(areaSelect.options).find(o => String(o.value) === String(preferredValue))?.text || String(preferredValue),
// //                 true
// //             );
// //         }
// //         return;
// //     }

// //     const url = `${appPrefix()}/ajax/options/areas/?branch_id=${branchId}`;
// //     const data = await fetchJSON(url);

// //     areaSelect.innerHTML = '<option value="">---------</option>';

// //     const added = new Set([""]);
// //     let selectedText = "";
// //     let hasPreferred = false;

// //     (data.results || []).forEach((item) => {
// //         const itemValue = String(item.id);
// //         const shouldSelect = itemValue === String(preferredValue);

// //         if (shouldSelect) {
// //             selectedText = item.text;
// //             hasPreferred = true;
// //         }

// //         areaSelect.add(new Option(item.text, item.id, false, shouldSelect));
// //         added.add(itemValue);
// //     });

// //     if (areaSnapshot?.options?.length) {
// //         areaSnapshot.options.forEach((opt) => {
// //             const optValue = String(opt.value);
// //             if (!added.has(optValue) && optValue !== "") {
// //                 const shouldSelect = optValue === String(preferredValue);

// //                 if (shouldSelect && !selectedText) {
// //                     selectedText = opt.text;
// //                     hasPreferred = true;
// //                 }

// //                 areaSelect.add(
// //                     new Option(opt.text, opt.value, false, shouldSelect)
// //                 );
// //             }
// //         });
// //     }

// //     areaSelect.dataset.selectedValue = preferredValue ? String(preferredValue) : "";
// //     refreshTomSelect(areaSelect);

// //     if (preferredValue && hasPreferred) {
// //         setSingleSelectValue(
// //             areaSelect,
// //             String(preferredValue),
// //             selectedText || String(preferredValue),
// //             true
// //         );
// //     } else if (preferredValue) {
// //         setSingleSelectValue(
// //             areaSelect,
// //             String(preferredValue),
// //             String(preferredValue),
// //             true
// //         );
// //     }
// // }

// //     async function loadCustomerGroupOptions(branchId, areaId, selectedIds = [], root = null) {
// //         const customerGroupSelect = findField("customer_group", root) || findField("total_customers", root);
// //         if (!customerGroupSelect) return;

// //         const selectedStrings = (selectedIds || []).map(String);
// //         const preservedOptions = captureSelectOptions(root);
// //         const key = customerGroupSelect.name;
// //         const cgSnapshot = preservedOptions[key] || null;

// //         if (!branchId) {
// //             customerGroupSelect.innerHTML = "";

// //             if (cgSnapshot?.options?.length) {
// //                 cgSnapshot.options.forEach((opt) => {
// //                     customerGroupSelect.add(
// //                         new Option(
// //                             opt.text,
// //                             opt.value,
// //                             false,
// //                             selectedStrings.includes(String(opt.value)) || !!opt.selected
// //                         )
// //                     );
// //                 });
// //             }

// //             refreshTomSelect(customerGroupSelect);
// //             return;
// //         }

// //         const params = new URLSearchParams();
// //         params.append("branch_id", branchId);
// //         if (areaId) params.append("area_id", areaId);

// //         const url = `${appPrefix()}/ajax/options/customer-groups/?${params.toString()}`;
// //         const data = await fetchJSON(url);

// //         const currentSelected = Array.from(customerGroupSelect.selectedOptions).map(o => String(o.value));
// //         customerGroupSelect.innerHTML = "";

// //         const added = new Set();

// //         (data.results || []).forEach(item => {
// //             const itemValue = String(item.id);
// //             const shouldSelect =
// //                 selectedStrings.includes(itemValue) ||
// //                 currentSelected.includes(itemValue);

// //             const option = new Option(item.text, item.id, false, shouldSelect);
// //             customerGroupSelect.add(option);
// //             added.add(itemValue);
// //         });

// //         if (cgSnapshot?.options?.length) {
// //             cgSnapshot.options.forEach((opt) => {
// //                 const optValue = String(opt.value);
// //                 if (!added.has(optValue)) {
// //                     customerGroupSelect.add(
// //                         new Option(
// //                             opt.text,
// //                             opt.value,
// //                             false,
// //                             selectedStrings.includes(optValue) ||
// //                             currentSelected.includes(optValue) ||
// //                             !!opt.selected
// //                         )
// //                     );
// //                 }
// //             });
// //         }

// //         refreshTomSelect(customerGroupSelect);
// //     }

// //     async function syncDependentDropdowns(root = null) {
// //         const branchId = getSelectedValue("branch", root) || getSelectedValue("parent_branch", root) || "";
// //         const areaId = getSelectedValue("area", root) || "";

// //         const areaSelect = findField("area", root);
// //         if (areaSelect) {
// //             await loadAreaOptions(branchId, areaId ? [String(areaId)] : [], root);
// //         }

// //         const cgSelect = findField("customer_group", root) || findField("total_customers", root);
// //         if (cgSelect) {
// //             const selectedCg = Array.from(cgSelect.selectedOptions).map(o => String(o.value));
// //             await loadCustomerGroupOptions(branchId, getSelectedValue("area", root) || areaId, selectedCg, root);
// //         }
// //     }

// //     // function initializeDependentHandlers(root = document) {
// //     //     const branchField = root.querySelector('[name="branch"], [name="parent_branch"]');
// //     //     const areaField = root.querySelector('[name="area"]');

// //     //     if (branchField && !branchField.dataset.boundDependent) {
// //     //         branchField.dataset.boundDependent = "1";
// //     //         branchField.addEventListener("change", async function () {
// //     //             const branchId = this.value || "";
// //     //             await loadAreaOptions(branchId, [], root);
// //     //             await loadCustomerGroupOptions(branchId, "", [], root);
// //     //         });
// //     //     }

// //     //     if (areaField && !areaField.dataset.boundDependent) {
// //     //         areaField.dataset.boundDependent = "1";
// //     //         areaField.addEventListener("change", async function () {
// //     //             const branchId = getSelectedValue("branch", root) || getSelectedValue("parent_branch", root) || "";
// //     //             await loadCustomerGroupOptions(branchId, this.value || "", [], root);
// //     //         });
// //     //     }
// //     // }

// // //     function initializeDependentHandlers(root = document) {
// // //     const branchField = root.querySelector('[name="branch"], [name="parent_branch"]');
// // //     const areaField = root.querySelector('[name="area"]');

// // //     if (branchField && !branchField.dataset.boundDependent) {
// // //         branchField.dataset.boundDependent = "1";
// // //         branchField.addEventListener("change", async function () {
// // //             const branchId = this.value || "";

// // //             const areaSelect = findField("area", root);
// // //             const customerGroupSelect = findField("customer_group", root) || findField("total_customers", root);

// // //             if (areaSelect) {
// // //                 areaSelect.dataset.selectedValue = "";
// // //                 if (areaSelect.tomselect) areaSelect.tomselect.clear(true);
// // //                 else areaSelect.value = "";
// // //             }

// // //             if (customerGroupSelect) {
// // //                 if (customerGroupSelect.tomselect) {
// // //                     customerGroupSelect.tomselect.clear(true);
// // //                 } else {
// // //                     Array.from(customerGroupSelect.options).forEach(opt => {
// // //                         opt.selected = false;
// // //                     });
// // //                 }
// // //             }

// // //             await loadAreaOptions(branchId, [], root);
// // //             await loadCustomerGroupOptions(branchId, "", [], root);
// // //         });
// // //     }

// // //     if (areaField && !areaField.dataset.boundDependent) {
// // //         areaField.dataset.boundDependent = "1";
// // //         areaField.addEventListener("change", async function () {
// // //             const branchId =
// // //                 getSelectedValue("branch", root) ||
// // //                 getSelectedValue("parent_branch", root) ||
// // //                 "";

// // //             const customerGroupSelect = findField("customer_group", root) || findField("total_customers", root);
// // //             if (customerGroupSelect) {
// // //                 if (customerGroupSelect.tomselect) {
// // //                     customerGroupSelect.tomselect.clear(true);
// // //                 } else {
// // //                     Array.from(customerGroupSelect.options).forEach(opt => {
// // //                         opt.selected = false;
// // //                     });
// // //                 }
// // //             }

// // //             await loadCustomerGroupOptions(branchId, this.value || "", [], root);
// // //         });
// // //     }
// // // }


// // // function initializeDependentHandlers(root = document) {
// // //     const branchField = root.querySelector('[name="branch"], [name="parent_branch"]');
// // //     const areaField = root.querySelector('[name="area"]');

// // //     if (branchField && !branchField.dataset.boundDependent) {
// // //         branchField.dataset.boundDependent = "1";
// // //         branchField.addEventListener("change", async function () {
// // //             const branchId = this.value || "";

// // //             const areaSelect = findField("area", root);
// // //             const customerGroupSelect = findField("customer_group", root) || findField("total_customers", root);

// // //             if (areaSelect) {
// // //                 areaSelect.dataset.selectedValue = "";
// // //                 if (areaSelect.tomselect) {
// // //                     areaSelect.tomselect.clear(true);
// // //                 } else {
// // //                     areaSelect.value = "";
// // //                 }
// // //             }

// // //             if (customerGroupSelect) {
// // //                 if (customerGroupSelect.tomselect) {
// // //                     customerGroupSelect.tomselect.clear(true);
// // //                 } else {
// // //                     Array.from(customerGroupSelect.options).forEach((opt) => {
// // //                         opt.selected = false;
// // //                     });
// // //                 }
// // //             }

// // //             await loadAreaOptions(branchId, [], root);
// // //             await loadCustomerGroupOptions(branchId, "", [], root);
// // //         });
// // //     }

// // //     if (areaField && !areaField.dataset.boundDependent) {
// // //         areaField.dataset.boundDependent = "1";
// // //         areaField.addEventListener("change", async function () {
// // //             const branchId =
// // //                 getSelectedValue("branch", root) ||
// // //                 getSelectedValue("parent_branch", root) ||
// // //                 "";

// // //             const areaId = this.value || "";
// // //             const customerGroupSelect = findField("customer_group", root) || findField("total_customers", root);

// // //             if (customerGroupSelect) {
// // //                 if (customerGroupSelect.tomselect) {
// // //                     customerGroupSelect.tomselect.clear(true);
// // //                 } else {
// // //                     Array.from(customerGroupSelect.options).forEach((opt) => {
// // //                         opt.selected = false;
// // //                     });
// // //                 }
// // //             }

// // //             await loadCustomerGroupOptions(branchId, areaId, [], root);
// // //         });
// // //     }
// // // }
   

// // function initializeDependentHandlers(root = document) {
// //     const branchField = root.querySelector('[name="branch"], [name="parent_branch"]');
// //     const areaField = root.querySelector('[name="area"]');

// //     if (branchField && !branchField.dataset.boundDependent) {
// //         branchField.dataset.boundDependent = "1";
// //         branchField.addEventListener("change", async function () {
// //             const branchId = this.value || "";

// //             const areaSelect = findField("area", root);
// //             const customerGroupSelect = findField("customer_group", root) || findField("total_customers", root);

// //             if (areaSelect) {
// //                 areaSelect.dataset.selectedValue = "";
// //                 areaSelect.innerHTML = '<option value="">---------</option>';
// //                 if (areaSelect.tomselect) {
// //                     areaSelect.tomselect.clear(true);
// //                     areaSelect.tomselect.clearOptions();
// //                     areaSelect.tomselect.addOption({ value: "", text: "---------" });
// //                     areaSelect.tomselect.refreshOptions(false);
// //                 } else {
// //                     areaSelect.value = "";
// //                 }
// //             }

// //             if (customerGroupSelect) {
// //                 customerGroupSelect.innerHTML = "";
// //                 if (customerGroupSelect.tomselect) {
// //                     customerGroupSelect.tomselect.clear(true);
// //                     customerGroupSelect.tomselect.clearOptions();
// //                     customerGroupSelect.tomselect.refreshOptions(false);
// //                 } else {
// //                     Array.from(customerGroupSelect.options).forEach((opt) => {
// //                         opt.selected = false;
// //                     });
// //                 }
// //             }

// //             await loadAreaOptions(branchId, [], root);
// //             await loadCustomerGroupOptions(branchId, "", [], root);
// //         });
// //     }

// //     if (areaField && !areaField.dataset.boundDependent) {
// //         areaField.dataset.boundDependent = "1";
// //         areaField.addEventListener("change", async function () {
// //             const branchId =
// //                 getSelectedValue("branch", root) ||
// //                 getSelectedValue("parent_branch", root) ||
// //                 "";

// //             const areaId = this.value || "";
// //             const customerGroupSelect = findField("customer_group", root) || findField("total_customers", root);

// //             if (customerGroupSelect) {
// //                 customerGroupSelect.innerHTML = "";
// //                 if (customerGroupSelect.tomselect) {
// //                     customerGroupSelect.tomselect.clear(true);
// //                     customerGroupSelect.tomselect.clearOptions();
// //                     customerGroupSelect.tomselect.refreshOptions(false);
// //                 }
// //             }

// //             await loadCustomerGroupOptions(branchId, areaId, [], root);
// //         });
// //     }
// // }

// //     function initializeFormSubmitGuard(root = document) {
// //     root.querySelectorAll("form").forEach((form) => {
// //         if (form.dataset.submitGuardBound === "1") return;
// //         form.dataset.submitGuardBound = "1";

// //         form.addEventListener("submit", function (event) {
// //             const modalBody = getModalBody();
// //             if (modalStack.length > 0 && modalBody && !modalBody.contains(form)) {
// //                 event.preventDefault();
// //                 return false;
// //             }

// //             if (form.dataset.submitting === "1") {
// //                 event.preventDefault();
// //                 return false;
// //             }

// //             form.dataset.submitting = "1";

// //             const submitButtons = form.querySelectorAll(
// //                 'button[type="submit"], input[type="submit"]'
// //             );

// //             submitButtons.forEach((btn) => {
// //                 btn.disabled = true;

// //                 if (btn.tagName === "BUTTON") {
// //                     if (!btn.dataset.originalText) {
// //                         btn.dataset.originalText = btn.innerHTML;
// //                     }
// //                     btn.innerHTML = "Saving...";
// //                 } else {
// //                     if (!btn.dataset.originalText) {
// //                         btn.dataset.originalText = btn.value;
// //                     }
// //                     btn.value = "Saving...";
// //                 }
// //             });
// //         });
// //     });
// // }

// //     function buildRelatedUrl(modelName, action, pk = null, extraParams = {}) {
// //         let url = `${appPrefix()}/ajax/related/${modelName}/create/`;
// //         if (action === "edit" && pk) {
// //             url = `${appPrefix()}/ajax/related/${modelName}/${pk}/edit/`;
// //         }

// //         const params = new URLSearchParams();
// //         Object.entries(extraParams).forEach(([key, value]) => {
// //             if (value !== null && value !== undefined && value !== "") {
// //                 params.append(key, value);
// //             }
// //         });

// //         const qs = params.toString();
// //         return qs ? `${url}?${qs}` : url;
// //     }

// //     function openModalWithUrl(url, isNested = false) {
// //         const body = getModalBody();
// //         if (!body) return;

// //         if (isNested && body.innerHTML.trim()) {
// //             const state = captureFormState(body);
// //             const selectOptions = captureSelectOptions(body);

// //             destroyTomSelectInstances(body);

// //             modalStack.push({
// //                 html: getCleanHtmlForStack(body),
// //                 state,
// //                 selectOptions,
// //             });
// //         }

// //         showModal();
// //         htmx.ajax("GET", url, {
// //             target: "#modal-body",
// //             swap: "innerHTML"
// //         });
// //     }

    


// //     function initializeRelatedButtons(root = document) {
// //     root.querySelectorAll(".related-create-btn").forEach((btn) => {
// //         if (btn.dataset.boundClick) return;
// //         btn.dataset.boundClick = "1";

// //         btn.addEventListener("click", function (event) {
// //             event.preventDefault();
// //             event.stopPropagation();

// //             const modelName = this.dataset.model;
// //             const fieldName = this.dataset.fieldName;
// //             const params = { parent_field: fieldName };

// //             if (modelName === "area") {
// //                 const branchId = getSelectedValue("branch", root) || getSelectedValue("parent_branch", root);
// //                 if (branchId) params.branch_id = branchId;
// //             }

// //             if (modelName === "customergroup") {
// //                 const branchId = getSelectedValue("branch", root) || getSelectedValue("parent_branch", root);
// //                 const areaId = getSelectedValue("area", root);
// //                 if (branchId) params.branch_id = branchId;
// //                 if (areaId) params.area_id = areaId;
// //             }

// //             if (modelName === "menu") {
// //                 const parentId = getSelectedValue("parent", root);
// //                 if (parentId) params.parent_id = parentId;
// //             }

// //             const modal = getModalContainer();
// //             const isNested = modal && !modal.classList.contains("hidden");
// //             openModalWithUrl(buildRelatedUrl(modelName, "create", null, params), isNested);
// //         });
// //     });

// //     root.querySelectorAll(".related-edit-btn").forEach((btn) => {
// //         if (btn.dataset.boundClick) return;
// //         btn.dataset.boundClick = "1";

// //         btn.addEventListener("click", function (event) {
// //             event.preventDefault();
// //             event.stopPropagation();

// //             const modelName = this.dataset.model;
// //             const fieldName = this.dataset.fieldName;
// //             const field = findField(fieldName, root);
// //             if (!field) return;

// //             let pk = "";
// //             if (field.multiple) {
// //                 const selected = Array.from(field.selectedOptions);
// //                 if (!selected.length) {
// //                     Swal.fire("Select one item first", "", "warning");
// //                     return;
// //                 }
// //                 pk = selected[0].value;
// //             } else {
// //                 pk = field.value;
// //                 if (!pk) {
// //                     Swal.fire("Select one item first", "", "warning");
// //                     return;
// //                 }
// //             }

// //             const params = { parent_field: fieldName };
// //             const modal = getModalContainer();
// //             const isNested = modal && !modal.classList.contains("hidden");
// //             openModalWithUrl(buildRelatedUrl(modelName, "edit", pk, params), isNested);
// //         });
// //     });
// // }

// //     function initializeDynamicUI(root = document) {
// //         clearBindingMarkers(root);
// //         initTomSelect(root);
// //         initializeRelatedButtons(root);
// //         initializeDependentHandlers(root);
// //         initializeFormSubmitGuard(root);
// //     }

  

// // async function restorePreviousModalAndApply(detail) {
// //     const previous = modalStack.pop();
// //     const body = getModalBody();
// //     if (!body || !previous) return;

// //     // close current nested modal content
// //     body.innerHTML = "";

// //     // restore previous modal
// //     body.innerHTML = previous.html;

// //     clearBindingMarkers(body);
// //     showModal();

// //     initializeDynamicUI(body);
// //     restoreSelectOptions(body, previous.selectOptions || {});
// //     restoreFormState(body, previous.state);

// //     await new Promise(resolve => setTimeout(resolve, 120));

// //     restoreSelectOptions(body, previous.selectOptions || {});
// //     restoreFormState(body, previous.state);

// //     const selectedBranchId =
// //         getSelectedValue("parent_branch", body) ||
// //         getSelectedValue("branch", body) ||
// //         "";

// //     const selectedAreaId = getSelectedValue("area", body) || "";

// //     if (detail.parentField === "branch" || detail.parentField === "parent_branch") {
// //         if (detail.option) {
// //             ensureRelatedOptionSelected(detail.parentField, detail.option, body, 15, 220, true);
// //         }

// //         await loadAreaOptions(selectedBranchId, selectedAreaId ? [String(selectedAreaId)] : [], body);
// //         await loadCustomerGroupOptions(selectedBranchId, getSelectedValue("area", body) || "", [], body);

// //     } else if (detail.parentField === "area") {
// //         if (detail.option) {
// //             await loadAreaOptions(selectedBranchId, [String(detail.option.id)], body);
// //             ensureRelatedOptionSelected("area", detail.option, body, 15, 220, true);
// //             await loadCustomerGroupOptions(selectedBranchId, String(detail.option.id), [], body);
// //         } else {
// //             await loadAreaOptions(selectedBranchId, selectedAreaId ? [String(selectedAreaId)] : [], body);
// //             await loadCustomerGroupOptions(selectedBranchId, selectedAreaId, [], body);
// //         }

// //     } else {
// //         await syncDependentDropdowns(body);

// //         if (detail.parentField && detail.option) {
// //             ensureRelatedOptionSelected(detail.parentField, detail.option, body, 15, 220, true);
// //         }
// //     }

// //     Swal.fire({
// //         toast: true,
// //         position: "top-end",
// //         icon: "success",
// //         title: detail.message || "Saved successfully.",
// //         showConfirmButton: false,
// //         timer: 1200,
// //         timerProgressBar: true,
// //     });
// // }

// // // async function handleRelatedSaved(detail) {
// // //     const body = getModalBody();
// // //     if (!body || !detail) return;
// // //     if (isDuplicateSaveEvent(detail)) return;

// // //     const isNested = modalStack.length > 0;

// // //     // Nested modal case:
// // //     // only current top modal closes, previous modal restores
// // //     if (isNested) {
// // //         await restorePreviousModalAndApply(detail);
// // //         return;
// // //     }

// // //     // Top-level modal case:
// // //     // update parent page fields if needed, then close modal
// // //     const selectedBranchId =
// // //         getSelectedValue("parent_branch", document) ||
// // //         getSelectedValue("branch", document) ||
// // //         "";

// // //     const selectedAreaId = getSelectedValue("area", document) || "";

// // //     if (detail.parentField === "branch" || detail.parentField === "parent_branch") {
// // //         await loadAreaOptions(
// // //             selectedBranchId,
// // //             selectedAreaId ? [String(selectedAreaId)] : [],
// // //             document
// // //         );

// // //         if (detail.option) {
// // //             ensureRelatedOptionSelected(detail.parentField, detail.option, document, 15, 220, true);
// // //         }

// // //         const finalAreaId = getSelectedValue("area", document) || "";
// // //         await loadCustomerGroupOptions(selectedBranchId, finalAreaId, [], document);

// // //     } else if (detail.parentField === "area") {
// // //         if (detail.option) {
// // //             await loadAreaOptions(selectedBranchId, [String(detail.option.id)], document);
// // //             ensureRelatedOptionSelected("area", detail.option, document, 15, 220, true);
// // //             await loadCustomerGroupOptions(selectedBranchId, String(detail.option.id), [], document);
// // //         } else {
// // //             await loadAreaOptions(
// // //                 selectedBranchId,
// // //                 selectedAreaId ? [String(selectedAreaId)] : [],
// // //                 document
// // //             );
// // //             await loadCustomerGroupOptions(selectedBranchId, selectedAreaId, [], document);
// // //         }
// // //     } else {
// // //         await syncDependentDropdowns(document);

// // //         if (detail.parentField && detail.option) {
// // //             ensureRelatedOptionSelected(detail.parentField, detail.option, document, 15, 220, true);
// // //         }
// // //     }

// // //     Swal.fire({
// // //         toast: true,
// // //         position: "top-end",
// // //         icon: "success",
// // //         title: detail.message || "Saved successfully.",
// // //         showConfirmButton: false,
// // //         timer: 1200,
// // //         timerProgressBar: true,
// // //     });

// // //     body.innerHTML = "";
// // //     hideModal();
// // // }

// // async function handleRelatedSaved(detail) {
// //     const body = getModalBody();
// //     if (!body || !detail) return;
// //     if (isDuplicateSaveEvent(detail)) return;

// //     const isNested = modalStack.length > 0;

// //     if (isNested) {
// //         await restorePreviousModalAndApply(detail);
// //         return;
// //     }

// //     const selectedBranchId =
// //         getSelectedValue("parent_branch", document) ||
// //         getSelectedValue("branch", document) ||
// //         "";

// //     const selectedAreaId = getSelectedValue("area", document) || "";

// //     if (detail.parentField === "branch" || detail.parentField === "parent_branch") {
// //         await loadAreaOptions(
// //             selectedBranchId,
// //             selectedAreaId ? [String(selectedAreaId)] : [],
// //             document
// //         );

// //         if (detail.option) {
// //             ensureRelatedOptionSelected(detail.parentField, detail.option, document, 15, 220, true);
// //         }

// //         const finalAreaId = getSelectedValue("area", document) || "";
// //         await loadCustomerGroupOptions(selectedBranchId, finalAreaId, [], document);

// //     } else if (detail.parentField === "area") {
// //         if (detail.option) {
// //             await loadAreaOptions(selectedBranchId, [String(detail.option.id)], document);
// //             ensureRelatedOptionSelected("area", detail.option, document, 15, 220, true);
// //             await loadCustomerGroupOptions(selectedBranchId, String(detail.option.id), [], document);
// //         } else {
// //             await loadAreaOptions(
// //                 selectedBranchId,
// //                 selectedAreaId ? [String(selectedAreaId)] : [],
// //                 document
// //             );
// //             await loadCustomerGroupOptions(selectedBranchId, selectedAreaId, [], document);
// //         }
// //     } else {
// //         await syncDependentDropdowns(document);

// //         if (detail.parentField && detail.option) {
// //             ensureRelatedOptionSelected(detail.parentField, detail.option, document, 15, 220, true);
// //         }
// //     }

// //     Swal.fire({
// //         toast: true,
// //         position: "top-end",
// //         icon: "success",
// //         title: detail.message || "Saved successfully.",
// //         showConfirmButton: false,
// //         timer: 1200,
// //         timerProgressBar: true,
// //     });

// //     body.innerHTML = "";
// //     hideModal();

// //     // refresh current list/form area after top-level save
// //     setTimeout(() => {
// //         refreshMainContent();
// //     }, 150);
// // }

// //     window.closeModal = function () {
// //         if (modalStack.length > 0) {
// //             const previous = modalStack.pop();
// //             const body = getModalBody();
// //             if (body && previous) {
// //                 body.innerHTML = previous.html;
// //                 clearBindingMarkers(body);
// //                 showModal();
// //                 initializeDynamicUI(body);
// //                 restoreSelectOptions(body, previous.selectOptions || {});
// //                 restoreFormState(body, previous.state);

// //                 setTimeout(async () => {
// //                     await syncDependentDropdowns(body);
// //                 }, 80);
// //             }
// //             return;
// //         }

// //         const body = getModalBody();
// //         if (body) body.innerHTML = "";
// //         hideModal();
// //     };

// //     document.addEventListener("DOMContentLoaded", function () {
// //         initializeDynamicUI(document);

// //         setTimeout(async () => {
// //             await syncDependentDropdowns(document);
// //         }, 80);

// //         const backdrop = document.getElementById("modal-backdrop");
// //         if (backdrop) {
// //             backdrop.addEventListener("click", function () {
// //                 closeModal();
// //             });
// //         }
// //     });

// //     document.body.addEventListener("click", function (event) {
// //         const trigger = event.target.closest(".modal-trigger");
// //         if (!trigger) return;

// //         event.preventDefault();
// //         event.stopPropagation();

// //         const url = trigger.getAttribute("data-modal-url") || trigger.getAttribute("href");
// //         if (!url) return;

// //         openModalWithUrl(url, false);
// //     });

// //     // document.body.addEventListener("click", function (event) {
// //     //     const btn = event.target.closest(".delete-btn");
// //     //     if (!btn) return;

// //     //     event.preventDefault();

// //     //     const url = btn.dataset.url;
// //     //     if (!url) return;

// //     //     Swal.fire({
// //     //         title: "Are you sure?",
// //     //         text: "This action cannot be undone.",
// //     //         icon: "warning",
// //     //         showCancelButton: true,
// //     //         confirmButtonText: "Yes, delete it",
// //     //         cancelButtonText: "Cancel"
// //     //     }).then((result) => {
// //     //         if (!result.isConfirmed) return;

// //     //         fetch(url, {
// //     //             method: "POST",
// //     //             credentials: "same-origin",
// //     //             headers: {
// //     //                 "X-CSRFToken": getCsrfToken(),
// //     //                 "X-Requested-With": "XMLHttpRequest",
// //     //                 "HX-Request": "true"
// //     //             }
// //     //         })
// //     //             .then(response => {
// //     //                 if (!response.ok) throw new Error("Delete failed");

// //     //                 const trigger = response.headers.get("HX-Trigger");
// //     //                 if (trigger) {
// //     //                     const events = JSON.parse(trigger);
// //     //                     if (events["crud:deleted"]?.message) {
// //     //                         Swal.fire({
// //     //                             toast: true,
// //     //                             position: "top-end",
// //     //                             icon: "success",
// //     //                             title: events["crud:deleted"].message,
// //     //                             showConfirmButton: false,
// //     //                             timer: 1800,
// //     //                         });
// //     //                     }
// //     //                 }

// //     //                 window.location.reload();
// //     //             })
// //     //             .catch(() => {
// //     //                 Swal.fire("Error", "Delete failed.", "error");
// //     //             });
// //     //     });
// //     // });

// // document.body.addEventListener("click", function (event) {
// //     const btn = event.target.closest(".delete-btn");
// //     if (!btn) return;

// //     event.preventDefault();

// //     const url = btn.dataset.url;
// //     if (!url) return;

// //     Swal.fire({
// //         title: "Are you sure?",
// //         text: "This action cannot be undone.",
// //         icon: "warning",
// //         showCancelButton: true,
// //         confirmButtonText: "Yes, delete it",
// //         cancelButtonText: "Cancel"
// //     }).then((result) => {
// //         if (!result.isConfirmed) return;

// //         fetch(url, {
// //             method: "POST",
// //             credentials: "same-origin",
// //             headers: {
// //                 "X-CSRFToken": getCsrfToken(),
// //                 "X-Requested-With": "XMLHttpRequest",
// //                 "HX-Request": "true"
// //             }
// //         })
// //         .then(async response => {
// //             if (!response.ok) throw new Error("Delete failed");

// //             const trigger = response.headers.get("HX-Trigger");
// //             if (trigger) {
// //                 const events = JSON.parse(trigger);
// //                 if (events["crud:deleted"]?.message) {
// //                     Swal.fire({
// //                         toast: true,
// //                         position: "top-end",
// //                         icon: "success",
// //                         title: events["crud:deleted"].message,
// //                         showConfirmButton: false,
// //                         timer: 1600,
// //                     });
// //                 }
// //             }

// //             refreshMainContent();
// //         })
// //         .catch(() => {
// //             Swal.fire("Error", "Delete failed.", "error");
// //         });
// //     });
// // });

// //     document.body.addEventListener("htmx:beforeSwap", function (event) {
// //         const target = event.detail?.target;
// //         if (!target || target.id !== "modal-body") return;

// //         const xhr = event.detail?.xhr;
// //         const triggers = parseHXTriggerHeader(xhr);
// //         const detail = extractRelatedSavedDetail(triggers);

// //         if (detail) {
// //             event.detail.shouldSwap = false;
// //             event.preventDefault();
// //         }
// //     });

// //     document.body.addEventListener("htmx:afterSwap", function (event) {
// //         if (event.detail.target && event.detail.target.id === "modal-body") {
// //             showModal();
// //             initializeDynamicUI(event.detail.target);

// //             setTimeout(async () => {
// //                 await syncDependentDropdowns(event.detail.target);
// //             }, 80);
// //         }

// //         if (event.detail.target && event.detail.target.id === "main-content") {
// //             initializeDynamicUI(event.detail.target);

// //             setTimeout(async () => {
// //                 await syncDependentDropdowns(event.detail.target);
// //             }, 80);
// //         }
// //     });

// //     document.body.addEventListener("htmx:afterRequest", async function (event) {
// //         const elt = event.detail?.elt;
// //         if (elt && elt.tagName === "FORM") {
// //             delete elt.dataset.submitting;

// //             const submitButtons = elt.querySelectorAll(
// //                 'button[type="submit"], input[type="submit"]'
// //             );

// //             submitButtons.forEach((btn) => {
// //                 btn.disabled = false;

// //                 if (btn.tagName === "BUTTON" && btn.dataset.originalText) {
// //                     btn.innerHTML = btn.dataset.originalText;
// //                 } else if (btn.tagName === "INPUT" && btn.dataset.originalText) {
// //                     btn.value = btn.dataset.originalText;
// //                 }
// //             });
// //         }

// //         const xhr = event.detail?.xhr;
// //         const triggers = parseHXTriggerHeader(xhr);
// //         const detail = extractRelatedSavedDetail(triggers);

// //         if (!detail) return;
// //         await handleRelatedSaved(detail);
// //     });
// // function initializeDynamicUI(root = document) {
// //     clearBindingMarkers(root);
// //     initTomSelect(root);
// //     initializeRelatedButtons(root);
// //     initializeDependentHandlers(root);
// //     initializeFormSubmitGuard(root);
// //     initListFilterChain(root);
// // }

// // document.addEventListener("DOMContentLoaded", function () {
// //     initializeDynamicUI(document);
// // });

// // document.body.addEventListener("htmx:afterSwap", function (event) {
// //     initializeDynamicUI(event.target || document);
// // });

// // })();













// (function () {
//     const modalStack = [];
//     let lastHandledSaveSignature = null;
//     let lastHandledSaveAt = 0;

//     function appPrefix() {
//         const fromBody = (document.body?.dataset?.appPrefix || "").trim();
//         if (fromBody) return fromBody.replace(/\/$/, "");
//         if (window.location.pathname.startsWith("/user/")) return "/user";
//         if (window.location.pathname.startsWith("/products/")) return "/products";
//         return "";
//     }

//     function getModalContainer() {
//         return document.getElementById("modal-container");
//     }

//     function getModalBody() {
//         return document.getElementById("modal-body");
//     }

//     function showModal() {
//         const modal = getModalContainer();
//         if (modal) modal.classList.remove("hidden");
//     }

//     function hideModal() {
//         const modal = getModalContainer();
//         if (modal) modal.classList.add("hidden");
//     }

//     function currentModalForm() {
//         const body = getModalBody();
//         if (!body) return null;
//         return body.querySelector("form");
//     }

//     function getCsrfToken() {
//         const cookieValue = document.cookie
//             .split("; ")
//             .find(row => row.startsWith("csrftoken="))
//             ?.split("=")[1];

//         if (cookieValue) return decodeURIComponent(cookieValue);
//         return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || "";
//     }

//     function findField(fieldName, root = null) {
//         const base = root || currentModalForm() || document;
//         return base.querySelector(`[name="${fieldName}"]`) || document.querySelector(`[name="${fieldName}"]`);
//     }

//     function captureFormState(root = null) {
//         const form = root?.querySelector?.("form") || currentModalForm();
//         if (!form) return {};

//         const state = {};

//         form.querySelectorAll("input, select, textarea").forEach((el) => {
//             if (!el.name) return;

//             if (el.type === "checkbox") {
//                 if (el.name.endsWith("[]")) {
//                     if (!state[el.name]) state[el.name] = [];
//                     if (el.checked) state[el.name].push(el.value);
//                 } else {
//                     state[el.name] = !!el.checked;
//                 }
//                 return;
//             }

//             if (el.type === "radio") {
//                 if (el.checked) state[el.name] = el.value;
//                 return;
//             }

//             if (el.tagName === "SELECT" && el.multiple) {
//                 state[el.name] = Array.from(el.selectedOptions).map(opt => String(opt.value));
//                 return;
//             }

//             if (el.type !== "file") {
//                 state[el.name] = el.value;
//             }
//         });

//         return state;
//     }

//     function captureSelectOptions(root = null) {
//         const form = root?.querySelector?.("form") || currentModalForm() || root || document;
//         const snapshot = {};

//         if (!form?.querySelectorAll) return snapshot;

//         form.querySelectorAll("select[name]").forEach((select) => {
//             const name = select.name;
//             snapshot[name] = {
//                 multiple: !!select.multiple,
//                 options: Array.from(select.options).map((opt) => ({
//                     value: String(opt.value),
//                     text: opt.text,
//                     selected: !!opt.selected
//                 }))
//             };
//         });

//         return snapshot;
//     }

//     function restoreSelectOptions(root = null, snapshot = {}) {
//         const form = root?.querySelector?.("form") || currentModalForm() || root || document;
//         if (!form) return;

//         Object.entries(snapshot).forEach(([name, config]) => {
//             const select = form.querySelector(`select[name="${name}"]`);
//             if (!select) return;

//             const currentPlaceholder = Array.from(select.options).find(
//                 (opt) => opt.value === "" && !config.options.some(o => o.value === "")
//             );

//             select.innerHTML = "";

//             if (currentPlaceholder) {
//                 select.add(new Option(currentPlaceholder.text, currentPlaceholder.value, false, false));
//             }

//             config.options.forEach((optData) => {
//                 const opt = new Option(
//                     optData.text,
//                     optData.value,
//                     false,
//                     !!optData.selected
//                 );
//                 select.add(opt);
//             });

//             refreshTomSelect(select);
//         });
//     }

//     function restoreFormState(root = null, state = {}) {
//         const form = root?.querySelector?.("form") || currentModalForm();
//         if (!form) return;

//         Object.entries(state).forEach(([name, value]) => {
//             const elements = form.querySelectorAll(`[name="${name}"]`);
//             if (!elements.length) return;

//             elements.forEach((el) => {
//                 if (el.type === "checkbox") {
//                     if (Array.isArray(value)) {
//                         el.checked = value.includes(el.value);
//                     } else {
//                         el.checked = !!value;
//                     }
//                     return;
//                 }

//                 if (el.type === "radio") {
//                     el.checked = String(el.value) === String(value);
//                     return;
//                 }

//                 if (el.tagName === "SELECT" && el.multiple) {
//                     const values = Array.isArray(value) ? value.map(String) : [];
//                     Array.from(el.options).forEach((opt) => {
//                         opt.selected = values.includes(String(opt.value));
//                     });

//                     if (el.tomselect) {
//                         el.tomselect.setValue(values, true);
//                         el.tomselect.refreshItems();
//                         el.tomselect.refreshOptions(false);
//                     }
//                     return;
//                 }

//                 if (el.tagName === "SELECT") {
//                     const strValue = value == null ? "" : String(value);

//                     let option = Array.from(el.options).find(opt => String(opt.value) === strValue);
//                     if (!option && strValue !== "") {
//                         option = new Option(strValue, strValue, true, true);
//                         el.add(option);
//                     }

//                     el.value = strValue;

//                     if (el.tomselect) {
//                         if (strValue === "") {
//                             el.tomselect.clear(true);
//                         } else {
//                             el.tomselect.addOption({ value: strValue, text: option?.text || strValue });
//                             el.tomselect.setValue(strValue, true);
//                         }
//                         el.tomselect.refreshItems();
//                         el.tomselect.refreshOptions(false);
//                     }
//                     return;
//                 }

//                 if (el.type !== "file") {
//                     el.value = value ?? "";
//                 }
//             });
//         });
//     }

//     function initTomSelect(root = document) {
//         root.querySelectorAll("select.js-enhanced-select").forEach((el) => {
//             const initialValue = el.dataset.selectedValue || el.value || "";

//             if (el.tomselect) {
//                 if (initialValue !== "") {
//                     el.tomselect.setValue(String(initialValue), true);
//                     el.tomselect.refreshItems();
//                     el.tomselect.refreshOptions(false);
//                 }
//                 return;
//             }

//             const control = new TomSelect(el, {
//                 create: false,
//                 allowEmptyOption: true,
//                 placeholder: el.dataset.placeholder || "Search...",
//                 maxOptions: 500,
//                 plugins: ["dropdown_input", "clear_button"],
//             });

//             if (initialValue !== "") {
//                 control.setValue(String(initialValue), true);
//                 control.refreshItems();
//                 control.refreshOptions(false);
//             }
//         });

//         root.querySelectorAll("select.js-enhanced-multiselect").forEach((el) => {
//             const initialValues =
//                 (el.dataset.selectedValue || "")
//                     .split(",")
//                     .map(v => v.trim())
//                     .filter(Boolean);

//             if (el.tomselect) {
//                 if (initialValues.length) {
//                     el.tomselect.setValue(initialValues, true);
//                     el.tomselect.refreshItems();
//                     el.tomselect.refreshOptions(false);
//                 }
//                 return;
//             }

//             const control = new TomSelect(el, {
//                 create: false,
//                 plugins: ["remove_button", "clear_button"],
//                 placeholder: el.dataset.placeholder || "Search...",
//                 maxOptions: 500,
//             });

//             if (initialValues.length) {
//                 control.setValue(initialValues, true);
//                 control.refreshItems();
//                 control.refreshOptions(false);
//             }
//         });
//     }

//     function refreshTomSelect(select) {
//         if (!select || !select.tomselect) return;

//         const selectedValues = Array.from(select.selectedOptions).map(opt => String(opt.value));
//         select.tomselect.clear(true);
//         select.tomselect.clearOptions();

//         Array.from(select.options).forEach((opt) => {
//             select.tomselect.addOption({
//                 value: String(opt.value),
//                 text: opt.text
//             });
//         });

//         if (select.multiple) {
//             select.tomselect.setValue(selectedValues, true);
//         } else {
//             select.tomselect.setValue(select.value ? String(select.value) : "", true);
//         }

//         select.tomselect.refreshItems();
//         select.tomselect.refreshOptions(false);
//     }

//     function setSingleSelectValue(select, value, text, silent = false) {
//         if (!select) return false;

//         value = String(value);

//         let existing = Array.from(select.options).find(opt => String(opt.value) === value);
//         if (!existing) {
//             existing = new Option(text, value, true, true);
//             select.add(existing);
//         } else {
//             existing.text = text;
//             existing.selected = true;
//         }

//         select.value = value;
//         select.dataset.selectedValue = value;

//         if (select.tomselect) {
//             select.tomselect.addOption({ value, text });
//             select.tomselect.setValue(value, silent);
//             select.tomselect.refreshItems();
//             select.tomselect.refreshOptions(false);
//         }

//         if (!silent) {
//             select.dispatchEvent(new Event("change", { bubbles: true }));
//             select.dispatchEvent(new Event("input", { bubbles: true }));
//         }

//         return String(select.value) === value;
//     }

//     function addMultiSelectValue(select, value, text, silent = false) {
//         if (!select) return false;

//         value = String(value);

//         let existing = Array.from(select.options).find(opt => String(opt.value) === value);
//         if (!existing) {
//             existing = new Option(text, value, true, true);
//             select.add(existing);
//         } else {
//             existing.text = text;
//             existing.selected = true;
//         }

//         if (select.tomselect) {
//             select.tomselect.addOption({ value, text });

//             const current = select.tomselect.getValue();
//             const arr = Array.isArray(current) ? current : (current ? [current] : []);
//             const next = [...new Set([...arr.map(String), value])];

//             select.tomselect.setValue(next, silent);
//             select.tomselect.refreshItems();
//             select.tomselect.refreshOptions(false);
//             select.dataset.selectedValue = next.join(",");
//         } else {
//             existing.selected = true;
//         }

//         if (!silent) {
//             select.dispatchEvent(new Event("change", { bubbles: true }));
//             select.dispatchEvent(new Event("input", { bubbles: true }));
//         }

//         return Array.from(select.selectedOptions).some(opt => String(opt.value) === value);
//     }

//     function upsertRelatedOption(fieldName, option, root = null, silent = false) {
//         const select = findField(fieldName, root);
//         if (!select || !option) return false;

//         const value = String(option.id);
//         const text = option.text || value;

//         if (select.multiple) {
//             return addMultiSelectValue(select, value, text, silent);
//         }
//         return setSingleSelectValue(select, value, text, silent);
//     }

//     function ensureRelatedOptionSelected(fieldName, option, root = null, tries = 20, delay = 180, silent = false) {
//         let attempt = 0;

//         function run() {
//             attempt += 1;
//             const ok = upsertRelatedOption(fieldName, option, root, silent);
//             if (ok) return;

//             if (attempt < tries) {
//                 setTimeout(run, delay);
//             }
//         }

//         run();
//     }

//     function clearBindingMarkers(root) {
//         if (!root?.querySelectorAll) return;

//         root.querySelectorAll("[data-bound-click], [data-bound-dependent]").forEach((el) => {
//             el.removeAttribute("data-bound-click");
//             el.removeAttribute("data-bound-dependent");
//         });
//     }

//     function getCleanHtmlForStack(root) {
//         const wrapper = document.createElement("div");
//         wrapper.innerHTML = root.innerHTML;
//         clearBindingMarkers(wrapper);
//         return wrapper.innerHTML;
//     }

//     async function fetchJSON(url) {
//         const response = await fetch(url, {
//             credentials: "same-origin",
//             headers: { "X-Requested-With": "XMLHttpRequest" }
//         });
//         if (!response.ok) throw new Error("Request failed");
//         return await response.json();
//     }

//     function parseHXTriggerHeader(xhr) {
//         if (!xhr) return null;

//         const triggerHeader = xhr.getResponseHeader("HX-Trigger");
//         if (!triggerHeader) return null;

//         try {
//             return JSON.parse(triggerHeader);
//         } catch (error) {
//             console.warn("Invalid HX-Trigger header:", triggerHeader);
//             return null;
//         }
//     }

//     function extractRelatedSavedDetail(triggers) {
//         if (!triggers) return null;
//         return triggers["related:saved"] || triggers["crud:saved"] || null;
//     }

//     function isDuplicateSaveEvent(detail) {
//         if (!detail) return false;

//         const signature = JSON.stringify({
//             parentField: detail.parentField || "",
//             optionId: detail.option?.id ?? "",
//             optionText: detail.option?.text ?? "",
//             message: detail.message || ""
//         });

//         const now = Date.now();
//         const isDup = signature === lastHandledSaveSignature && (now - lastHandledSaveAt) < 1200;

//         if (!isDup) {
//             lastHandledSaveSignature = signature;
//             lastHandledSaveAt = now;
//         }

//         return isDup;
//     }

//     function getSelectedValue(fieldName, root = null) {
//         const el = findField(fieldName, root);
//         if (!el) return "";
//         return el.value || "";
//     }

//     async function loadAreaOptions(branchId, selectedIds = [], root = null) {
//         const areaSelect = findField("area", root);
//         if (!areaSelect) return;

//         const selectedStrings = (selectedIds || []).map(String);

//         const currentTomValue = areaSelect.tomselect
//             ? areaSelect.tomselect.getValue()
//             : areaSelect.value;

//         const currentValue = Array.isArray(currentTomValue)
//             ? (currentTomValue[0] || "")
//             : String(currentTomValue || "");

//         const preferredValue =
//             selectedStrings[0] ||
//             areaSelect.dataset.selectedValue ||
//             currentValue ||
//             "";

//         const preservedOptions = captureSelectOptions(root);
//         const areaSnapshot = preservedOptions.area || null;

//         if (!branchId) {
//             areaSelect.innerHTML = '<option value="">---------</option>';

//             if (areaSnapshot?.options?.length) {
//                 areaSnapshot.options.forEach((opt) => {
//                     if (String(opt.value) !== "") {
//                         const shouldSelect =
//                             String(opt.value) === String(preferredValue) || !!opt.selected;

//                         areaSelect.add(
//                             new Option(opt.text, opt.value, false, shouldSelect)
//                         );
//                     }
//                 });
//             }

//             areaSelect.dataset.selectedValue = preferredValue ? String(preferredValue) : "";
//             refreshTomSelect(areaSelect);

//             if (preferredValue) {
//                 setSingleSelectValue(
//                     areaSelect,
//                     String(preferredValue),
//                     Array.from(areaSelect.options).find(o => String(o.value) === String(preferredValue))?.text || String(preferredValue),
//                     true
//                 );
//             }
//             return;
//         }

//         const url = `${appPrefix()}/ajax/options/areas/?branch_id=${branchId}`;
//         const data = await fetchJSON(url);

//         areaSelect.innerHTML = '<option value="">---------</option>';

//         const added = new Set([""]);
//         let selectedText = "";
//         let hasPreferred = false;

//         (data.results || []).forEach((item) => {
//             const itemValue = String(item.id);
//             const shouldSelect = itemValue === String(preferredValue);

//             if (shouldSelect) {
//                 selectedText = item.text;
//                 hasPreferred = true;
//             }

//             areaSelect.add(new Option(item.text, item.id, false, shouldSelect));
//             added.add(itemValue);
//         });

//         if (areaSnapshot?.options?.length) {
//             areaSnapshot.options.forEach((opt) => {
//                 const optValue = String(opt.value);
//                 if (!added.has(optValue) && optValue !== "") {
//                     const shouldSelect = optValue === String(preferredValue);

//                     if (shouldSelect && !selectedText) {
//                         selectedText = opt.text;
//                         hasPreferred = true;
//                     }

//                     areaSelect.add(
//                         new Option(opt.text, opt.value, false, shouldSelect)
//                     );
//                 }
//             });
//         }

//         areaSelect.dataset.selectedValue = preferredValue ? String(preferredValue) : "";
//         refreshTomSelect(areaSelect);

//         if (preferredValue && hasPreferred) {
//             setSingleSelectValue(
//                 areaSelect,
//                 String(preferredValue),
//                 selectedText || String(preferredValue),
//                 true
//             );
//         } else if (preferredValue) {
//             setSingleSelectValue(
//                 areaSelect,
//                 String(preferredValue),
//                 String(preferredValue),
//                 true
//             );
//         }
//     }

//     async function loadCustomerGroupOptions(branchId, areaId, selectedIds = [], root = null) {
//         const customerGroupSelect = findField("customer_group", root) || findField("total_customers", root);
//         if (!customerGroupSelect) return;

//         const selectedStrings = (selectedIds || []).map(String);
//         const preservedOptions = captureSelectOptions(root);
//         const key = customerGroupSelect.name;
//         const cgSnapshot = preservedOptions[key] || null;

//         if (!branchId) {
//             customerGroupSelect.innerHTML = "";

//             if (cgSnapshot?.options?.length) {
//                 cgSnapshot.options.forEach((opt) => {
//                     customerGroupSelect.add(
//                         new Option(
//                             opt.text,
//                             opt.value,
//                             false,
//                             selectedStrings.includes(String(opt.value)) || !!opt.selected
//                         )
//                     );
//                 });
//             }

//             refreshTomSelect(customerGroupSelect);
//             return;
//         }

//         const params = new URLSearchParams();
//         params.append("branch_id", branchId);
//         if (areaId) params.append("area_id", areaId);

//         const url = `${appPrefix()}/ajax/options/customer-groups/?${params.toString()}`;
//         const data = await fetchJSON(url);

//         customerGroupSelect.innerHTML = "";
//         const added = new Set();

//         (data.results || []).forEach((item) => {
//             const val = String(item.id);
//             const selected = selectedStrings.includes(val);
//             customerGroupSelect.add(new Option(item.text, item.id, false, selected));
//             added.add(val);
//         });

//         if (cgSnapshot?.options?.length) {
//             cgSnapshot.options.forEach((opt) => {
//                 const val = String(opt.value);
//                 if (!added.has(val)) {
//                     customerGroupSelect.add(
//                         new Option(
//                             opt.text,
//                             opt.value,
//                             false,
//                             selectedStrings.includes(val) || !!opt.selected
//                         )
//                     );
//                 }
//             });
//         }

//         refreshTomSelect(customerGroupSelect);
//     }

//     async function syncDependentDropdowns(root = document) {
//         const branchId =
//             getSelectedValue("parent_branch", root) ||
//             getSelectedValue("branch", root) ||
//             "";

//         const areaSelect = findField("area", root);
//         const currentArea =
//             areaSelect?.dataset?.selectedValue ||
//             getSelectedValue("area", root) ||
//             "";

//         await loadAreaOptions(branchId, currentArea ? [String(currentArea)] : [], root);

//         const finalArea =
//             findField("area", root)?.dataset?.selectedValue ||
//             getSelectedValue("area", root) ||
//             "";

//         const customerGroupSelect = findField("customer_group", root) || findField("total_customers", root);
//         const currentCustomerGroups = customerGroupSelect?.multiple
//             ? Array.from(customerGroupSelect.selectedOptions || []).map(o => String(o.value))
//             : [];

//         await loadCustomerGroupOptions(branchId, finalArea, currentCustomerGroups, root);
//     }

//     function buildRelatedUrl(modelName, action = "create", pk = null, params = {}) {
//         const prefix = appPrefix();
//         let url = "";

//         if (action === "edit" && pk) {
//             url = `${prefix}/ajax/related/${modelName}/${pk}/edit/`;
//         } else {
//             url = `${prefix}/ajax/related/${modelName}/create/`;
//         }

//         const searchParams = new URLSearchParams(params);
//         const qs = searchParams.toString();
//         return qs ? `${url}?${qs}` : url;
//     }

//     function openModalWithUrl(url, nested = false) {
//         const body = getModalBody();
//         if (!body) return;

//         if (nested) {
//             modalStack.push({
//                 html: getCleanHtmlForStack(body),
//                 state: captureFormState(body),
//                 selectOptions: captureSelectOptions(body),
//             });
//         }

//         fetch(url, {
//             headers: {
//                 "HX-Request": "true",
//                 "X-Requested-With": "XMLHttpRequest",
//             },
//             credentials: "same-origin",
//         })
//             .then(res => res.text())
//             .then(html => {
//                 body.innerHTML = html;
//                 showModal();
//                 initializeDynamicUI(body);

//                 setTimeout(async () => {
//                     await syncDependentDropdowns(body);
//                 }, 80);
//             });
//     }

//     function initializeRelatedButtons(root = document) {
//         root.querySelectorAll(".related-create-btn").forEach((btn) => {
//             if (btn.dataset.boundClick) return;
//             btn.dataset.boundClick = "1";

//             btn.addEventListener("click", function (event) {
//                 event.preventDefault();
//                 event.stopPropagation();

//                 const modelName = this.dataset.model;
//                 const fieldName = this.dataset.fieldName;
//                 const params = { parent_field: fieldName };

//                 if (modelName === "area") {
//                     const branchId =
//                         getSelectedValue("parent_branch", root) ||
//                         getSelectedValue("branch", root) ||
//                         "";
//                     if (branchId) params.branch_id = branchId;
//                 }

//                 if (modelName === "customergroup") {
//                     const branchId =
//                         getSelectedValue("parent_branch", root) ||
//                         getSelectedValue("branch", root) ||
//                         "";
//                     const areaId = getSelectedValue("area", root) || "";
//                     if (branchId) params.branch_id = branchId;
//                     if (areaId) params.area_id = areaId;
//                 }

//                 if (modelName === "menu") {
//                     const parentId = getSelectedValue("parent", root);
//                     if (parentId) params.parent_id = parentId;
//                 }

//                 const modal = getModalContainer();
//                 const isNested = modal && !modal.classList.contains("hidden");
//                 openModalWithUrl(buildRelatedUrl(modelName, "create", null, params), isNested);
//             });
//         });

//         root.querySelectorAll(".related-edit-btn").forEach((btn) => {
//             if (btn.dataset.boundClick) return;
//             btn.dataset.boundClick = "1";

//             btn.addEventListener("click", function (event) {
//                 event.preventDefault();
//                 event.stopPropagation();

//                 const modelName = this.dataset.model;
//                 const fieldName = this.dataset.fieldName;
//                 const field = findField(fieldName, root);
//                 if (!field) return;

//                 let pk = "";
//                 if (field.multiple) {
//                     const selected = Array.from(field.selectedOptions);
//                     if (!selected.length) {
//                         Swal.fire("Select one item first", "", "warning");
//                         return;
//                     }
//                     pk = selected[0].value;
//                 } else {
//                     pk = field.value;
//                     if (!pk) {
//                         Swal.fire("Select one item first", "", "warning");
//                         return;
//                     }
//                 }

//                 const params = { parent_field: fieldName };
//                 const modal = getModalContainer();
//                 const isNested = modal && !modal.classList.contains("hidden");
//                 openModalWithUrl(buildRelatedUrl(modelName, "edit", pk, params), isNested);
//             });
//         });
//     }

//     function initializeDependentHandlers(root = document) {
//         const branchField = findField("branch", root) || findField("parent_branch", root);
//         const areaField = findField("area", root);

//         if (branchField && !branchField.dataset.boundDependent) {
//             branchField.dataset.boundDependent = "1";
//             branchField.addEventListener("change", async function () {
//                 const branchId = this.value || "";
//                 const areaSelect = findField("area", root);
//                 if (areaSelect) {
//                     areaSelect.dataset.selectedValue = "";
//                 }
//                 await loadAreaOptions(branchId, [], root);
//                 await loadCustomerGroupOptions(branchId, "", [], root);
//             });
//         }

//         if (areaField && !areaField.dataset.boundDependent) {
//             areaField.dataset.boundDependent = "1";
//             areaField.addEventListener("change", async function () {
//                 const branchId =
//                     getSelectedValue("parent_branch", root) ||
//                     getSelectedValue("branch", root) ||
//                     "";
//                 const areaId = this.value || "";
//                 this.dataset.selectedValue = areaId;
//                 await loadCustomerGroupOptions(branchId, areaId, [], root);
//             });
//         }
//     }

//     // function initializeFormSubmitGuard(root = document) {
//     //     root.querySelectorAll("form[hx-post]").forEach((form) => {
//     //         if (form.dataset.boundSubmitGuard) return;
//     //         form.dataset.boundSubmitGuard = "1";

//     //         form.addEventListener("htmx:beforeRequest", function () {
//     //             const submitBtn = form.querySelector('button[type="submit"]');
//     //             if (!submitBtn) return;
//     //             submitBtn.disabled = true;
//     //             submitBtn.dataset.originalText = submitBtn.innerHTML;
//     //             submitBtn.innerHTML = "Saving...";
//     //         });

//     //         form.addEventListener("htmx:afterRequest", function () {
//     //             const submitBtn = form.querySelector('button[type="submit"]');
//     //             if (!submitBtn) return;
//     //             submitBtn.disabled = false;
//     //             submitBtn.innerHTML = submitBtn.dataset.originalText || "Save";
//     //         });
//     //     });
//     // }

//     function initializeFormSubmitGuard(root = document) {
//     root.querySelectorAll("form[hx-post]").forEach((form) => {
//         if (form.dataset.submitGuardBound === "1") return;
//         form.dataset.submitGuardBound = "1";

//         form.addEventListener("submit", function (event) {
//             if (!form.hasAttribute("hx-post")) {
//                 return;
//             }

//             const modalBody = getModalBody();
//             if (modalStack.length > 0 && modalBody && !modalBody.contains(form)) {
//                 event.preventDefault();
//                 return false;
//             }

//             if (form.dataset.submitting === "1") {
//                 event.preventDefault();
//                 return false;
//             }

//             form.dataset.submitting = "1";
//         });

//         form.addEventListener("htmx:beforeRequest", function () {
//             const submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
//             submitButtons.forEach((btn) => {
//                 btn.disabled = true;
//                 if (btn.tagName === "BUTTON") {
//                     if (!btn.dataset.originalText) btn.dataset.originalText = btn.innerHTML;
//                     btn.innerHTML = "Saving...";
//                 } else {
//                     if (!btn.dataset.originalText) btn.dataset.originalText = btn.value;
//                     btn.value = "Saving...";
//                 }
//             });
//         });

//         form.addEventListener("htmx:afterRequest", function () {
//             form.dataset.submitting = "0";
//             const submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
//             submitButtons.forEach((btn) => {
//                 btn.disabled = false;
//                 if (btn.tagName === "BUTTON") {
//                     btn.innerHTML = btn.dataset.originalText || "Save";
//                 } else {
//                     btn.value = btn.dataset.originalText || "Save";
//                 }
//             });
//         });
//     });
// }

// function initializeModalTriggers(root = document) {
//     root.querySelectorAll(".modal-trigger").forEach((el) => {
//         if (el.dataset.boundModalTrigger) return;
//         el.dataset.boundModalTrigger = "1";

//         el.addEventListener("click", function (e) {
//             e.preventDefault();
//             e.stopPropagation();

//             const url = this.dataset.modalUrl || this.getAttribute("href");
//             if (!url) return;

//             openModalWithUrl(url, false);
//         });
//     });
// }

//     function initializeDynamicUI(root = document) {
//         clearBindingMarkers(root);
//         initTomSelect(root);
//         initializeRelatedButtons(root);
//         initializeDependentHandlers(root);
//         initializeFormSubmitGuard(root);
//         initializeModalTriggers(root);
//     }

//     async function restorePreviousModalAndApply(detail) {
//         const previous = modalStack.pop();
//         const body = getModalBody();
//         if (!body || !previous) return;

//         body.innerHTML = "";
//         body.innerHTML = previous.html;

//         clearBindingMarkers(body);
//         showModal();

//         initializeDynamicUI(body);
//         restoreSelectOptions(body, previous.selectOptions || {});
//         restoreFormState(body, previous.state);

//         await new Promise(resolve => setTimeout(resolve, 120));

//         restoreSelectOptions(body, previous.selectOptions || {});
//         restoreFormState(body, previous.state);

//         const selectedBranchId =
//             getSelectedValue("parent_branch", body) ||
//             getSelectedValue("branch", body) ||
//             "";

//         const selectedAreaId =
//             findField("area", body)?.dataset?.selectedValue ||
//             getSelectedValue("area", body) ||
//             "";

//         if (detail.parentField === "branch" || detail.parentField === "parent_branch") {
//             if (detail.option) {
//                 ensureRelatedOptionSelected(detail.parentField, detail.option, body, 20, 180, true);
//             }

//             const branchField = findField(detail.parentField, body);
//             if (branchField && detail.option) {
//                 branchField.dataset.selectedValue = String(detail.option.id);
//             }

//             await loadAreaOptions(selectedBranchId, selectedAreaId ? [String(selectedAreaId)] : [], body);
//             await loadCustomerGroupOptions(selectedBranchId, getSelectedValue("area", body) || "", [], body);

//         } else if (detail.parentField === "area") {
//             if (detail.option) {
//                 await loadAreaOptions(selectedBranchId, [String(detail.option.id)], body);
//                 ensureRelatedOptionSelected("area", detail.option, body, 20, 180, true);

//                 const areaField = findField("area", body);
//                 if (areaField) {
//                     areaField.dataset.selectedValue = String(detail.option.id);
//                     areaField.dispatchEvent(new Event("change", { bubbles: true }));
//                     areaField.dispatchEvent(new Event("input", { bubbles: true }));
//                 }

//                 await loadCustomerGroupOptions(selectedBranchId, String(detail.option.id), [], body);
//             } else {
//                 await loadAreaOptions(selectedBranchId, selectedAreaId ? [String(selectedAreaId)] : [], body);
//                 await loadCustomerGroupOptions(selectedBranchId, selectedAreaId, [], body);
//             }

//         } else {
//             await syncDependentDropdowns(body);

//             if (detail.parentField && detail.option) {
//                 ensureRelatedOptionSelected(detail.parentField, detail.option, body, 20, 180, true);

//                 const targetField = findField(detail.parentField, body);
//                 if (targetField) {
//                     targetField.dispatchEvent(new Event("change", { bubbles: true }));
//                     targetField.dispatchEvent(new Event("input", { bubbles: true }));
//                 }
//             }
//         }

//         Swal.fire({
//             toast: true,
//             position: "top-end",
//             icon: "success",
//             title: detail.message || "Saved successfully.",
//             showConfirmButton: false,
//             timer: 1200,
//             timerProgressBar: true,
//         });
//     }

//     async function handleRelatedSaved(detail) {
//         const body = getModalBody();
//         if (!body || !detail) return;
//         if (isDuplicateSaveEvent(detail)) return;

//         const isNested = modalStack.length > 0;

//         if (isNested) {
//             await restorePreviousModalAndApply(detail);
//             return;
//         }

//         const selectedBranchId =
//             getSelectedValue("parent_branch", document) ||
//             getSelectedValue("branch", document) ||
//             "";

//         const selectedAreaId =
//             findField("area", document)?.dataset?.selectedValue ||
//             getSelectedValue("area", document) ||
//             "";

//         if (detail.parentField === "branch" || detail.parentField === "parent_branch") {
//             if (detail.option) {
//                 ensureRelatedOptionSelected(detail.parentField, detail.option, document, 20, 180, true);

//                 const branchField = findField(detail.parentField, document);
//                 if (branchField) {
//                     branchField.dataset.selectedValue = String(detail.option.id);
//                 }
//             }

//             const finalBranchId =
//                 getSelectedValue("parent_branch", document) ||
//                 getSelectedValue("branch", document) ||
//                 "";

//             await loadAreaOptions(
//                 finalBranchId,
//                 selectedAreaId ? [String(selectedAreaId)] : [],
//                 document
//             );

//             const finalAreaId = getSelectedValue("area", document) || "";
//             await loadCustomerGroupOptions(finalBranchId, finalAreaId, [], document);

//         } else if (detail.parentField === "area") {
//             if (detail.option) {
//                 await loadAreaOptions(selectedBranchId, [String(detail.option.id)], document);
//                 ensureRelatedOptionSelected("area", detail.option, document, 20, 180, true);

//                 const areaField = findField("area", document);
//                 if (areaField) {
//                     areaField.dataset.selectedValue = String(detail.option.id);
//                     areaField.dispatchEvent(new Event("change", { bubbles: true }));
//                     areaField.dispatchEvent(new Event("input", { bubbles: true }));
//                 }

//                 await loadCustomerGroupOptions(selectedBranchId, String(detail.option.id), [], document);
//             } else {
//                 await loadAreaOptions(
//                     selectedBranchId,
//                     selectedAreaId ? [String(selectedAreaId)] : [],
//                     document
//                 );
//                 await loadCustomerGroupOptions(selectedBranchId, selectedAreaId, [], document);
//             }
//         } else {
//             await syncDependentDropdowns(document);

//             if (detail.parentField && detail.option) {
//                 ensureRelatedOptionSelected(detail.parentField, detail.option, document, 20, 180, true);

//                 const targetField = findField(detail.parentField, document);
//                 if (targetField) {
//                     targetField.dispatchEvent(new Event("change", { bubbles: true }));
//                     targetField.dispatchEvent(new Event("input", { bubbles: true }));
//                 }
//             }
//         }

//         Swal.fire({
//             toast: true,
//             position: "top-end",
//             icon: "success",
//             title: detail.message || "Saved successfully.",
//             showConfirmButton: false,
//             timer: 1200,
//             timerProgressBar: true,
//         });

//         body.innerHTML = "";
//         hideModal();
//     }

//     window.closeModal = function () {
//         if (modalStack.length > 0) {
//             const previous = modalStack.pop();
//             const body = getModalBody();
//             if (body && previous) {
//                 body.innerHTML = previous.html;
//                 clearBindingMarkers(body);
//                 showModal();
//                 initializeDynamicUI(body);
//                 restoreSelectOptions(body, previous.selectOptions || {});
//                 restoreFormState(body, previous.state);

//                 setTimeout(async () => {
//                     await syncDependentDropdowns(body);
//                 }, 80);
//             }
//             return;
//         }

//         const body = getModalBody();
//         if (body) body.innerHTML = "";
//         hideModal();
//     };

//     document.addEventListener("DOMContentLoaded", function () {
//         initializeDynamicUI(document);

//         setTimeout(async () => {
//             await syncDependentDropdowns(document);
//         }, 80);

//         const backdrop = document.getElementById("modal-backdrop");
//         if (backdrop) {
//             backdrop.addEventListener("click", function () {
//                 closeModal();
//             });
//         }
//     });

//     document.body.addEventListener("htmx:afterSwap", function (event) {
//         const target = event.detail?.target;
//         if (!target) return;

//         if (target.id === "modal-body" || target.closest?.("#modal-body")) {
//             initializeDynamicUI(getModalBody());
//             setTimeout(async () => {
//                 await syncDependentDropdowns(getModalBody());
//             }, 80);
//             return;
//         }

//         initializeDynamicUI(document);
//     });

//     document.body.addEventListener("htmx:afterRequest", async function (event) {
//         const xhr = event.detail?.xhr;
//         const triggers = parseHXTriggerHeader(xhr);
//         const detail = extractRelatedSavedDetail(triggers);

//         if (detail) {
//             await handleRelatedSaved(detail);
//             return;
//         }

//         if (triggers?.["crud:deleted"]) {
//             const payload = triggers["crud:deleted"];
//             Swal.fire({
//                 toast: true,
//                 position: "top-end",
//                 icon: "success",
//                 title: payload.message || "Deleted successfully.",
//                 showConfirmButton: false,
//                 timer: 1200,
//                 timerProgressBar: true,
//             });
//         }
//     });

//     document.body.addEventListener("htmx:configRequest", function (event) {
//         const token = getCsrfToken();
//         if (token) {
//             event.detail.headers["X-CSRFToken"] = token;
//         }
//     });
// })();



(function () {
    const modalStack = [];
    let lastHandledSaveSignature = null;
    let lastHandledSaveAt = 0;

    function appPrefix() {
    const fromBody = (document.body?.dataset?.appPrefix || "").trim();
    if (fromBody) return fromBody.replace(/\/$/, "");

    if (window.location.pathname.startsWith("/user/")) return "/user";
    if (window.location.pathname.startsWith("/product/")) return "/product";
  

    return "";
}

    function getModalContainer() {
        return document.getElementById("modal-container");
    }

    function getModalBody() {
        return document.getElementById("modal-body");
    }

    function showModal() {
        const modal = getModalContainer();
        if (modal) modal.classList.remove("hidden");
    }

    function hideModal() {
        const modal = getModalContainer();
        if (modal) modal.classList.add("hidden");
    }

    function currentModalForm() {
        const body = getModalBody();
        if (!body) return null;
        return body.querySelector("form");
    }

    function getCsrfToken() {
        const cookieValue = document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="))
            ?.split("=")[1];

        if (cookieValue) return decodeURIComponent(cookieValue);
        return document.querySelector('input[name="csrfmiddlewaretoken"]')?.value || "";
    }

    function findField(fieldName, root = null) {
        const base = root || currentModalForm() || document;
        return base.querySelector(`[name="${fieldName}"]`) || document.querySelector(`[name="${fieldName}"]`);
    }

    function captureFormState(root = null) {
        const form = root?.querySelector?.("form") || currentModalForm();
        if (!form) return {};

        const state = {};

        form.querySelectorAll("input, select, textarea").forEach((el) => {
            if (!el.name) return;

            if (el.type === "checkbox") {
                if (el.name.endsWith("[]")) {
                    if (!state[el.name]) state[el.name] = [];
                    if (el.checked) state[el.name].push(el.value);
                } else {
                    state[el.name] = !!el.checked;
                }
                return;
            }

            if (el.type === "radio") {
                if (el.checked) state[el.name] = el.value;
                return;
            }

            if (el.tagName === "SELECT" && el.multiple) {
                state[el.name] = Array.from(el.selectedOptions).map(opt => String(opt.value));
                return;
            }

            if (el.type !== "file") {
                state[el.name] = el.value;
            }
        });

        return state;
    }

    function captureSelectOptions(root = null) {
        const form = root?.querySelector?.("form") || currentModalForm() || root || document;
        const snapshot = {};

        if (!form?.querySelectorAll) return snapshot;

        form.querySelectorAll("select[name]").forEach((select) => {
            const name = select.name;
            snapshot[name] = {
                multiple: !!select.multiple,
                options: Array.from(select.options).map((opt) => ({
                    value: String(opt.value),
                    text: opt.text,
                    selected: !!opt.selected
                }))
            };
        });

        return snapshot;
    }

    function restoreSelectOptions(root = null, snapshot = {}) {
        const form = root?.querySelector?.("form") || currentModalForm() || root || document;
        if (!form) return;

        Object.entries(snapshot).forEach(([name, config]) => {
            const select = form.querySelector(`select[name="${name}"]`);
            if (!select) return;

            const currentPlaceholder = Array.from(select.options).find(
                (opt) => opt.value === "" && !config.options.some(o => o.value === "")
            );

            select.innerHTML = "";

            if (currentPlaceholder) {
                select.add(new Option(currentPlaceholder.text, currentPlaceholder.value, false, false));
            }

            config.options.forEach((optData) => {
                const opt = new Option(
                    optData.text,
                    optData.value,
                    false,
                    !!optData.selected
                );
                select.add(opt);
            });

            refreshTomSelect(select);
        });
    }

    function restoreFormState(root = null, state = {}) {
        const form = root?.querySelector?.("form") || currentModalForm();
        if (!form) return;

        Object.entries(state).forEach(([name, value]) => {
            const elements = form.querySelectorAll(`[name="${name}"]`);
            if (!elements.length) return;

            elements.forEach((el) => {
                if (el.type === "checkbox") {
                    if (Array.isArray(value)) {
                        el.checked = value.includes(el.value);
                    } else {
                        el.checked = !!value;
                    }
                    return;
                }

                if (el.type === "radio") {
                    el.checked = String(el.value) === String(value);
                    return;
                }

                if (el.tagName === "SELECT" && el.multiple) {
                    const values = Array.isArray(value) ? value.map(String) : [];
                    Array.from(el.options).forEach((opt) => {
                        opt.selected = values.includes(String(opt.value));
                    });

                    if (el.tomselect) {
                        el.tomselect.setValue(values, true);
                        el.tomselect.refreshItems();
                        el.tomselect.refreshOptions(false);
                    }
                    return;
                }

                if (el.tagName === "SELECT") {
                    const strValue = value == null ? "" : String(value);

                    let option = Array.from(el.options).find(opt => String(opt.value) === strValue);
                    if (!option && strValue !== "") {
                        option = new Option(strValue, strValue, true, true);
                        el.add(option);
                    }

                    el.value = strValue;
                    el.dataset.selectedValue = strValue;

                    if (el.tomselect) {
                        if (strValue === "") {
                            el.tomselect.clear(true);
                        } else {
                            el.tomselect.addOption({ value: strValue, text: option?.text || strValue });
                            el.tomselect.setValue(strValue, true);
                        }
                        el.tomselect.refreshItems();
                        el.tomselect.refreshOptions(false);
                    }
                    return;
                }

                if (el.type !== "file") {
                    el.value = value ?? "";
                }
            });
        });
    }

    function initTomSelect(root = document) {
        root.querySelectorAll("select.js-enhanced-select").forEach((el) => {
            const initialValue = el.dataset.selectedValue || el.value || "";

            if (el.tomselect) {
                if (initialValue !== "") {
                    el.tomselect.setValue(String(initialValue), true);
                    el.tomselect.refreshItems();
                    el.tomselect.refreshOptions(false);
                }
                return;
            }

            const control = new TomSelect(el, {
                create: false,
                allowEmptyOption: true,
                placeholder: el.dataset.placeholder || "Search...",
                maxOptions: 500,
                plugins: ["dropdown_input", "clear_button"],
            });

            if (initialValue !== "") {
                control.setValue(String(initialValue), true);
                control.refreshItems();
                control.refreshOptions(false);
            }
        });

        root.querySelectorAll("select.js-enhanced-multiselect").forEach((el) => {
            const initialValues =
                (el.dataset.selectedValue || "")
                    .split(",")
                    .map(v => v.trim())
                    .filter(Boolean);

            if (el.tomselect) {
                if (initialValues.length) {
                    el.tomselect.setValue(initialValues, true);
                    el.tomselect.refreshItems();
                    el.tomselect.refreshOptions(false);
                }
                return;
            }

            const control = new TomSelect(el, {
                create: false,
                plugins: ["remove_button", "clear_button"],
                placeholder: el.dataset.placeholder || "Search...",
                maxOptions: 500,
            });

            if (initialValues.length) {
                control.setValue(initialValues, true);
                control.refreshItems();
                control.refreshOptions(false);
            }
        });
    }

    function refreshTomSelect(select) {
        if (!select || !select.tomselect) return;

        const selectedValues = Array.from(select.selectedOptions).map(opt => String(opt.value));
        select.tomselect.clear(true);
        select.tomselect.clearOptions();

        Array.from(select.options).forEach((opt) => {
            select.tomselect.addOption({
                value: String(opt.value),
                text: opt.text
            });
        });

        if (select.multiple) {
            select.tomselect.setValue(selectedValues, true);
        } else {
            select.tomselect.setValue(select.value ? String(select.value) : "", true);
        }

        select.tomselect.refreshItems();
        select.tomselect.refreshOptions(false);
    }

    function setSingleSelectValue(select, value, text, silent = false) {
        if (!select) return false;

        value = String(value);

        let existing = Array.from(select.options).find(opt => String(opt.value) === value);
        if (!existing) {
            existing = new Option(text, value, true, true);
            select.add(existing);
        } else {
            existing.text = text;
            existing.selected = true;
        }

        select.value = value;
        select.dataset.selectedValue = value;

        if (select.tomselect) {
            select.tomselect.addOption({ value, text });
            select.tomselect.setValue(value, true);
            select.tomselect.refreshItems();
            select.tomselect.refreshOptions(false);
        }

        if (!silent) {
            select.dispatchEvent(new Event("change", { bubbles: true }));
            select.dispatchEvent(new Event("input", { bubbles: true }));
        }

        return String(select.value) === value;
    }

    function addMultiSelectValue(select, value, text, silent = false) {
        if (!select) return false;

        value = String(value);

        let existing = Array.from(select.options).find(opt => String(opt.value) === value);
        if (!existing) {
            existing = new Option(text, value, true, true);
            select.add(existing);
        } else {
            existing.text = text;
            existing.selected = true;
        }

        if (select.tomselect) {
            select.tomselect.addOption({ value, text });

            const current = select.tomselect.getValue();
            const arr = Array.isArray(current) ? current : (current ? [current] : []);
            const next = [...new Set([...arr.map(String), value])];

            select.tomselect.setValue(next, true);
            select.tomselect.refreshItems();
            select.tomselect.refreshOptions(false);
            select.dataset.selectedValue = next.join(",");
        } else {
            existing.selected = true;
        }

        if (!silent) {
            select.dispatchEvent(new Event("change", { bubbles: true }));
            select.dispatchEvent(new Event("input", { bubbles: true }));
        }

        return Array.from(select.selectedOptions).some(opt => String(opt.value) === value);
    }

    function upsertRelatedOption(fieldName, option, root = null, silent = false) {
        const select = findField(fieldName, root);
        if (!select || !option) return false;

        const value = String(option.id);
        const text = option.text || value;

        if (select.multiple) {
            return addMultiSelectValue(select, value, text, silent);
        }
        return setSingleSelectValue(select, value, text, silent);
    }

    function ensureRelatedOptionSelected(fieldName, option, root = null, tries = 20, delay = 180, silent = false) {
        let attempt = 0;

        function run() {
            attempt += 1;
            const ok = upsertRelatedOption(fieldName, option, root, silent);
            if (ok) return;

            if (attempt < tries) {
                setTimeout(run, delay);
            }
        }

        run();
    }

    function clearBindingMarkers(root) {
        if (!root?.querySelectorAll) return;

        root.querySelectorAll("[data-bound-click], [data-bound-dependent]").forEach((el) => {
            el.removeAttribute("data-bound-click");
            el.removeAttribute("data-bound-dependent");
        });
    }

    function getCleanHtmlForStack(root) {
        const wrapper = document.createElement("div");
        wrapper.innerHTML = root.innerHTML;
        clearBindingMarkers(wrapper);
        return wrapper.innerHTML;
    }

    async function fetchJSON(url) {
        const response = await fetch(url, {
            credentials: "same-origin",
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });
        if (!response.ok) throw new Error("Request failed");
        return await response.json();
    }

    function parseHXTriggerHeader(xhr) {
        if (!xhr) return null;

        const triggerHeader = xhr.getResponseHeader("HX-Trigger");
        if (!triggerHeader) return null;

        try {
            return JSON.parse(triggerHeader);
        } catch (error) {
            console.warn("Invalid HX-Trigger header:", triggerHeader);
            return null;
        }
    }

    function extractRelatedSavedDetail(triggers) {
        if (!triggers) return null;
        return triggers["related:saved"] || triggers["crud:saved"] || null;
    }

    function isDuplicateSaveEvent(detail) {
        if (!detail) return false;

        const signature = JSON.stringify({
            parentField: detail.parentField || "",
            optionId: detail.option?.id ?? "",
            optionText: detail.option?.text ?? "",
            message: detail.message || ""
        });

        const now = Date.now();
        const isDup = signature === lastHandledSaveSignature && (now - lastHandledSaveAt) < 1200;

        if (!isDup) {
            lastHandledSaveSignature = signature;
            lastHandledSaveAt = now;
        }

        return isDup;
    }

    function getSelectedValue(fieldName, root = null) {
        const el = findField(fieldName, root);
        if (!el) return "";
        return el.value || "";
    }

    async function loadAreaOptions(branchId, selectedIds = [], root = null) {
        const areaSelect = findField("area", root);
        if (!areaSelect) return;

        const selectedStrings = (selectedIds || []).map(String);

        const currentTomValue = areaSelect.tomselect
            ? areaSelect.tomselect.getValue()
            : areaSelect.value;

        const currentValue = Array.isArray(currentTomValue)
            ? (currentTomValue[0] || "")
            : String(currentTomValue || "");

        const preferredValue =
            selectedStrings[0] ||
            areaSelect.dataset.selectedValue ||
            currentValue ||
            "";

        const preservedOptions = captureSelectOptions(root);
        const areaSnapshot = preservedOptions.area || null;

        if (!branchId) {
            areaSelect.innerHTML = '<option value="">---------</option>';

            if (areaSnapshot?.options?.length) {
                areaSnapshot.options.forEach((opt) => {
                    if (String(opt.value) !== "") {
                        const shouldSelect =
                            String(opt.value) === String(preferredValue) || !!opt.selected;

                        areaSelect.add(
                            new Option(opt.text, opt.value, false, shouldSelect)
                        );
                    }
                });
            }

            areaSelect.dataset.selectedValue = preferredValue ? String(preferredValue) : "";
            refreshTomSelect(areaSelect);

            if (preferredValue) {
                setSingleSelectValue(
                    areaSelect,
                    String(preferredValue),
                    Array.from(areaSelect.options).find(o => String(o.value) === String(preferredValue))?.text || String(preferredValue),
                    true
                );
            }
            return;
        }

        const url = `${appPrefix()}/ajax/options/areas/?branch_id=${branchId}`;
        const data = await fetchJSON(url);

        areaSelect.innerHTML = '<option value="">---------</option>';

        const added = new Set([""]);
        let selectedText = "";
        let hasPreferred = false;

        (data.results || []).forEach((item) => {
            const itemValue = String(item.id);
            const shouldSelect = itemValue === String(preferredValue);

            if (shouldSelect) {
                selectedText = item.text;
                hasPreferred = true;
            }

            areaSelect.add(new Option(item.text, item.id, false, shouldSelect));
            added.add(itemValue);
        });

        if (areaSnapshot?.options?.length) {
            areaSnapshot.options.forEach((opt) => {
                const optValue = String(opt.value);
                if (!added.has(optValue) && optValue !== "") {
                    const shouldSelect = optValue === String(preferredValue);

                    if (shouldSelect && !selectedText) {
                        selectedText = opt.text;
                        hasPreferred = true;
                    }

                    areaSelect.add(
                        new Option(opt.text, opt.value, false, shouldSelect)
                    );
                }
            });
        }

        areaSelect.dataset.selectedValue = preferredValue ? String(preferredValue) : "";
        refreshTomSelect(areaSelect);

        if (preferredValue && hasPreferred) {
            setSingleSelectValue(
                areaSelect,
                String(preferredValue),
                selectedText || String(preferredValue),
                true
            );
        } else if (preferredValue) {
            setSingleSelectValue(
                areaSelect,
                String(preferredValue),
                String(preferredValue),
                true
            );
        }
    }

    async function loadCustomerGroupOptions(branchId, areaId, selectedIds = [], root = null) {
        const customerGroupSelect = findField("customer_group", root) || findField("total_customers", root);
        if (!customerGroupSelect) return;

        const selectedStrings = (selectedIds || []).map(String);
        const preservedOptions = captureSelectOptions(root);
        const key = customerGroupSelect.name;
        const cgSnapshot = preservedOptions[key] || null;

        if (!branchId) {
            customerGroupSelect.innerHTML = "";

            if (cgSnapshot?.options?.length) {
                cgSnapshot.options.forEach((opt) => {
                    customerGroupSelect.add(
                        new Option(
                            opt.text,
                            opt.value,
                            false,
                            selectedStrings.includes(String(opt.value)) || !!opt.selected
                        )
                    );
                });
            }

            refreshTomSelect(customerGroupSelect);
            return;
        }

        const params = new URLSearchParams();
        params.append("branch_id", branchId);
        if (areaId) params.append("area_id", areaId);

        const url = `${appPrefix()}/ajax/options/customer-groups/?${params.toString()}`;
        const data = await fetchJSON(url);

        customerGroupSelect.innerHTML = "";
        const added = new Set();

        (data.results || []).forEach((item) => {
            const val = String(item.id);
            const selected = selectedStrings.includes(val);
            customerGroupSelect.add(new Option(item.text, item.id, false, selected));
            added.add(val);
        });

        if (cgSnapshot?.options?.length) {
            cgSnapshot.options.forEach((opt) => {
                const val = String(opt.value);
                if (!added.has(val)) {
                    customerGroupSelect.add(
                        new Option(
                            opt.text,
                            opt.value,
                            false,
                            selectedStrings.includes(val) || !!opt.selected
                        )
                    );
                }
            });
        }

        refreshTomSelect(customerGroupSelect);
    }

    async function syncDependentDropdowns(root = document) {
        const branchId =
            getSelectedValue("parent_branch", root) ||
            getSelectedValue("branch", root) ||
            "";

        const areaSelect = findField("area", root);
        const currentArea =
            areaSelect?.dataset?.selectedValue ||
            getSelectedValue("area", root) ||
            "";

        await loadAreaOptions(branchId, currentArea ? [String(currentArea)] : [], root);

        const finalArea =
            findField("area", root)?.dataset?.selectedValue ||
            getSelectedValue("area", root) ||
            "";

        const customerGroupSelect = findField("customer_group", root) || findField("total_customers", root);
        const currentCustomerGroups = customerGroupSelect?.multiple
            ? Array.from(customerGroupSelect.selectedOptions || []).map(o => String(o.value))
            : [];

        await loadCustomerGroupOptions(branchId, finalArea, currentCustomerGroups, root);
    }

    function buildRelatedUrl(modelName, action = "create", pk = null, params = {}) {
        const prefix = appPrefix();
        let url = "";

        if (action === "edit" && pk) {
            url = `${prefix}/ajax/related/${modelName}/${pk}/edit/`;
        } else {
            url = `${prefix}/ajax/related/${modelName}/create/`;
        }

        const searchParams = new URLSearchParams(params);
        const qs = searchParams.toString();
        return qs ? `${url}?${qs}` : url;
    }

    function openModalWithUrl(url, nested = false) {
        const body = getModalBody();
        if (!body) return;

        if (nested) {
            modalStack.push({
                html: getCleanHtmlForStack(body),
                state: captureFormState(body),
                selectOptions: captureSelectOptions(body),
            });
        }

        fetch(url, {
            headers: {
                "HX-Request": "true",
                "X-Requested-With": "XMLHttpRequest",
            },
            credentials: "same-origin",
        })
            .then(res => res.text())
            .then(html => {
                body.innerHTML = html;
                showModal();
                initializeDynamicUI(body);

                setTimeout(async () => {
                    await syncDependentDropdowns(body);
                }, 80);
            });
    }

    function initializeRelatedButtons(root = document) {
        root.querySelectorAll(".related-create-btn").forEach((btn) => {
            if (btn.dataset.boundClick) return;
            btn.dataset.boundClick = "1";

            btn.addEventListener("click", function (event) {
                event.preventDefault();
                event.stopPropagation();

                const modelName = this.dataset.model;
                const fieldName = this.dataset.fieldName;
                const params = { parent_field: fieldName };

                if (modelName === "area") {
                    const branchId =
                        getSelectedValue("parent_branch", root) ||
                        getSelectedValue("branch", root) ||
                        "";
                    if (branchId) params.branch_id = branchId;
                }

                if (modelName === "customergroup") {
                    const branchId =
                        getSelectedValue("parent_branch", root) ||
                        getSelectedValue("branch", root) ||
                        "";
                    const areaId = getSelectedValue("area", root) || "";
                    if (branchId) params.branch_id = branchId;
                    if (areaId) params.area_id = areaId;
                }

                if (modelName === "menu") {
                    const parentId = getSelectedValue("parent", root);
                    if (parentId) params.parent_id = parentId;
                }
                
                const modal = getModalContainer();
                const isNested = modal && !modal.classList.contains("hidden");
                openModalWithUrl(buildRelatedUrl(modelName, "create", null, params), isNested);
            });
        });

        root.querySelectorAll(".related-edit-btn").forEach((btn) => {
            if (btn.dataset.boundClick) return;
            btn.dataset.boundClick = "1";

            btn.addEventListener("click", function (event) {
                event.preventDefault();
                event.stopPropagation();

                const modelName = this.dataset.model;
                const fieldName = this.dataset.fieldName;
                const field = findField(fieldName, root);
                if (!field) return;

                let pk = "";
                if (field.multiple) {
                    const selected = Array.from(field.selectedOptions);
                    if (!selected.length) {
                        Swal.fire("Select one item first", "", "warning");
                        return;
                    }
                    pk = selected[0].value;
                } else {
                    pk = field.value;
                    if (!pk) {
                        Swal.fire("Select one item first", "", "warning");
                        return;
                    }
                }

                const params = { parent_field: fieldName };
                const modal = getModalContainer();
                const isNested = modal && !modal.classList.contains("hidden");
                openModalWithUrl(buildRelatedUrl(modelName, "edit", pk, params), isNested);
            });
        });
    }

    function initializeModalTriggers(root = document) {
        root.querySelectorAll(".modal-trigger").forEach((el) => {
            if (el.dataset.boundModalTrigger) return;
            el.dataset.boundModalTrigger = "1";

            el.addEventListener("click", function (e) {
                e.preventDefault();
                e.stopPropagation();

                const url = this.dataset.modalUrl || this.getAttribute("href");
                if (!url) return;

                openModalWithUrl(url, false);
            });
        });
    }

    function initializeDependentHandlers(root = document) {
        const branchField = findField("branch", root) || findField("parent_branch", root);
        const areaField = findField("area", root);

        if (branchField && !branchField.dataset.boundDependent) {
            branchField.dataset.boundDependent = "1";
            branchField.addEventListener("change", async function () {
                const branchId = this.value || "";
                const areaSelect = findField("area", root);
                if (areaSelect) {
                    areaSelect.dataset.selectedValue = "";
                }
                await loadAreaOptions(branchId, [], root);
                await loadCustomerGroupOptions(branchId, "", [], root);
            });
        }

        if (areaField && !areaField.dataset.boundDependent) {
            areaField.dataset.boundDependent = "1";
            areaField.addEventListener("change", async function () {
                const branchId =
                    getSelectedValue("parent_branch", root) ||
                    getSelectedValue("branch", root) ||
                    "";
                const areaId = this.value || "";
                this.dataset.selectedValue = areaId;
                await loadCustomerGroupOptions(branchId, areaId, [], root);
            });
        }
    }

    function initializeFormSubmitGuard(root = document) {
        root.querySelectorAll("form[hx-post]").forEach((form) => {
            if (form.dataset.submitGuardBound === "1") return;
            form.dataset.submitGuardBound = "1";

            form.addEventListener("submit", function (event) {
                if (!form.hasAttribute("hx-post")) {
                    return;
                }

                const modalBody = getModalBody();
                if (modalStack.length > 0 && modalBody && !modalBody.contains(form)) {
                    event.preventDefault();
                    return false;
                }

                if (form.dataset.submitting === "1") {
                    event.preventDefault();
                    return false;
                }

                form.dataset.submitting = "1";
            });

            form.addEventListener("htmx:beforeRequest", function () {
                const submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
                submitButtons.forEach((btn) => {
                    btn.disabled = true;
                    if (btn.tagName === "BUTTON") {
                        if (!btn.dataset.originalText) btn.dataset.originalText = btn.innerHTML;
                        btn.innerHTML = "Saving...";
                    } else {
                        if (!btn.dataset.originalText) btn.dataset.originalText = btn.value;
                        btn.value = "Saving...";
                    }
                });
            });

            form.addEventListener("htmx:afterRequest", function () {
                form.dataset.submitting = "0";
                const submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
                submitButtons.forEach((btn) => {
                    btn.disabled = false;
                    if (btn.tagName === "BUTTON") {
                        btn.innerHTML = btn.dataset.originalText || "Save";
                    } else {
                        btn.value = btn.dataset.originalText || "Save";
                    }
                });
            });
        });
    }

    function refreshMainContent() {
    const mainContent = document.getElementById("main-content");
    if (!mainContent) {
        window.location.reload();
        return;
    }

    const url = window.location.href;
    htmx.ajax("GET", url, {
        target: "#main-content",
        swap: "outerHTML"
    });
}
    function initializeDeleteButtons(root = document) {
    root.querySelectorAll(".delete-btn").forEach((btn) => {
        if (btn.dataset.boundDeleteBtn === "1") return;
        btn.dataset.boundDeleteBtn = "1";

        btn.addEventListener("click", function (event) {
            event.preventDefault();
            event.stopPropagation();

            const url = this.dataset.url || this.getAttribute("href");
            if (!url) return;

            Swal.fire({
                title: "Are you sure?",
                text: "This action cannot be undone.",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Yes, delete it",
                cancelButtonText: "Cancel"
            }).then((result) => {
                if (!result.isConfirmed) return;

                fetch(url, {
                    method: "POST",
                    credentials: "same-origin",
                    headers: {
                        "X-CSRFToken": getCsrfToken(),
                        "X-Requested-With": "XMLHttpRequest",
                        "HX-Request": "true"
                    }
                })
                .then(async (response) => {
                    if (!response.ok) throw new Error("Delete failed");

                    const triggerHeader = response.headers.get("HX-Trigger");
                    if (triggerHeader) {
                        try {
                            const events = JSON.parse(triggerHeader);

                            if (events["crud:deleted"]?.message) {
                                Swal.fire({
                                    toast: true,
                                    position: "top-end",
                                    icon: "success",
                                    title: events["crud:deleted"].message,
                                    showConfirmButton: false,
                                    timer: 1500,
                                    timerProgressBar: true,
                                });
                            }
                        } catch (e) {
                            console.warn("Invalid HX-Trigger on delete:", triggerHeader);
                        }
                    }

                    refreshMainContent();
                })
                .catch(() => {
                    Swal.fire("Error", "Delete failed.", "error");
                });
            });
        });
    });
}
    function initializeDynamicUI(root = document) {
        clearBindingMarkers(root);
        initTomSelect(root);
        initializeRelatedButtons(root);
        initializeModalTriggers(root);
        initializeDependentHandlers(root);
        initializeFormSubmitGuard(root);
        initializeDeleteButtons(root);
    }

    // async function restorePreviousModalAndApply(detail) {
    //     const previous = modalStack.pop();
    //     const body = getModalBody();
    //     if (!body || !previous) return;

    //     body.innerHTML = previous.html;

    //     clearBindingMarkers(body);
    //     showModal();

    //     initializeDynamicUI(body);
    //     restoreSelectOptions(body, previous.selectOptions || {});
    //     restoreFormState(body, previous.state || {});

    //     await new Promise(resolve => setTimeout(resolve, 120));

    //     restoreSelectOptions(body, previous.selectOptions || {});
    //     restoreFormState(body, previous.state || {});

    //     if (detail.parentField && detail.option) {
    //         ensureRelatedOptionSelected(detail.parentField, detail.option, body, 20, 180, false);

    //         const targetField = findField(detail.parentField, body);
    //         if (targetField) {
    //             if (!targetField.multiple) {
    //                 targetField.dataset.selectedValue = String(detail.option.id);
    //             }
    //             targetField.dispatchEvent(new Event("change", { bubbles: true }));
    //             targetField.dispatchEvent(new Event("input", { bubbles: true }));
    //         }
    //     }

    //     await syncDependentDropdowns(body);

    //     Swal.fire({
    //         toast: true,
    //         position: "top-end",
    //         icon: "success",
    //         title: detail.message || "Saved successfully.",
    //         showConfirmButton: false,
    //         timer: 1200,
    //         timerProgressBar: true,
    //     });
    // }


    async function restorePreviousModalAndApply(detail) {
    const previous = modalStack.pop();
    const body = getModalBody();
    if (!body || !previous) return;

    body.innerHTML = previous.html;

    clearBindingMarkers(body);
    showModal();

    initializeDynamicUI(body);
    restoreSelectOptions(body, previous.selectOptions || {});
    restoreFormState(body, previous.state || {});

    await new Promise(resolve => setTimeout(resolve, 120));

    restoreSelectOptions(body, previous.selectOptions || {});
    restoreFormState(body, previous.state || {});

    if (detail.parentField && detail.option) {
        ensureRelatedOptionSelected(detail.parentField, detail.option, body, 20, 180, false);

        const targetField = findField(detail.parentField, body);
        if (targetField) {
            if (!targetField.multiple) {
                targetField.dataset.selectedValue = String(detail.option.id);
            }
            targetField.dispatchEvent(new Event("change", { bubbles: true }));
            targetField.dispatchEvent(new Event("input", { bubbles: true }));
        }
    }

    await syncDependentDropdowns(body);

    Swal.fire({
        toast: true,
        position: "top-end",
        icon: "success",
        title: detail.message || "Saved successfully.",
        showConfirmButton: false,
        timer: 1200,
        timerProgressBar: true,
    });
}


    // async function handleRelatedSaved(detail) {
    //     const body = getModalBody();
    //     if (!body || !detail) return;
    //     if (isDuplicateSaveEvent(detail)) return;

    //     const isNested = modalStack.length > 0;

    //     if (isNested) {
    //         await restorePreviousModalAndApply(detail);
    //         return;
    //     }

    //     if (detail.parentField && detail.option) {
    //         ensureRelatedOptionSelected(detail.parentField, detail.option, document, 20, 180, false);

    //         const targetField = findField(detail.parentField, document);
    //         if (targetField) {
    //             if (!targetField.multiple) {
    //                 targetField.dataset.selectedValue = String(detail.option.id);
    //             }
    //             targetField.dispatchEvent(new Event("change", { bubbles: true }));
    //             targetField.dispatchEvent(new Event("input", { bubbles: true }));
    //         }
    //     }

    //     await syncDependentDropdowns(document);

    //     Swal.fire({
    //         toast: true,
    //         position: "top-end",
    //         icon: "success",
    //         title: detail.message || "Saved successfully.",
    //         showConfirmButton: false,
    //         timer: 1200,
    //         timerProgressBar: true,
    //     });

    //     body.innerHTML = "";
    //     hideModal();
    // }


//     async function handleRelatedSaved(detail) {
//     const body = getModalBody();
//     if (!body || !detail) return;
//     if (isDuplicateSaveEvent(detail)) return;

//     const isNested = modalStack.length > 0;

//     if (isNested) {
//         await restorePreviousModalAndApply(detail);
//         return;
//     }

//     if (detail.parentField && detail.option) {
//         ensureRelatedOptionSelected(detail.parentField, detail.option, document, 20, 180, false);

//         const targetField = findField(detail.parentField, document);
//         if (targetField) {
//             if (!targetField.multiple) {
//                 targetField.dataset.selectedValue = String(detail.option.id);
//             }
//             targetField.dispatchEvent(new Event("change", { bubbles: true }));
//             targetField.dispatchEvent(new Event("input", { bubbles: true }));
//         }
//     }

//     await syncDependentDropdowns(document);

//     Swal.fire({
//         toast: true,
//         position: "top-end",
//         icon: "success",
//         title: detail.message || "Saved successfully.",
//         showConfirmButton: false,
//         timer: 1200,
//         timerProgressBar: true,
//     });

//     body.innerHTML = "";
//     hideModal();
// }


async function handleRelatedSaved(detail) {
    const body = getModalBody();
    if (!body || !detail) return;
    if (isDuplicateSaveEvent(detail)) return;

    const isNested = modalStack.length > 0;

    if (isNested) {
        await restorePreviousModalAndApply(detail);
        return;
    }

    const fieldName = detail.parentField || "";
    const option = detail.option || null;

    // branch/area/customer_group এর জন্য আগে dependent sync, পরে final select
    if (fieldName === "branch") {
        ensureRelatedOptionSelected(fieldName, option, document, 20, 180, false);
        await syncDependentDropdowns(document);
        ensureRelatedOptionSelected(fieldName, option, document, 20, 180, false);
    } else if (fieldName === "area" || fieldName === "customer_group") {
        await syncDependentDropdowns(document);
        ensureRelatedOptionSelected(fieldName, option, document, 20, 180, false);
    } else if (fieldName && option) {
        ensureRelatedOptionSelected(fieldName, option, document, 20, 180, false);
    }

    const targetField = fieldName ? findField(fieldName, document) : null;
    if (targetField) {
        if (!targetField.multiple) {
            targetField.dataset.selectedValue = String(option.id);
        }
        targetField.dispatchEvent(new Event("change", { bubbles: true }));
        targetField.dispatchEvent(new Event("input", { bubbles: true }));
    }

    Swal.fire({
        toast: true,
        position: "top-end",
        icon: "success",
        title: detail.message || "Saved successfully.",
        showConfirmButton: false,
        timer: 1200,
        timerProgressBar: true,
    });

    body.innerHTML = "";
    hideModal();
}

    window.closeModal = function () {
        if (modalStack.length > 0) {
            const previous = modalStack.pop();
            const body = getModalBody();
            if (body && previous) {
                body.innerHTML = previous.html;
                clearBindingMarkers(body);
                showModal();
                initializeDynamicUI(body);
                restoreSelectOptions(body, previous.selectOptions || {});
                restoreFormState(body, previous.state || {});

                setTimeout(async () => {
                    await syncDependentDropdowns(body);
                }, 80);
            }
            return;
        }

        const body = getModalBody();
        if (body) body.innerHTML = "";
        hideModal();
    };

    document.addEventListener("DOMContentLoaded", function () {
        initializeDynamicUI(document);

        setTimeout(async () => {
            await syncDependentDropdowns(document);
        }, 80);

        const backdrop = document.getElementById("modal-backdrop");
        if (backdrop) {
            backdrop.addEventListener("click", function () {
                closeModal();
            });
        }
    });

    document.body.addEventListener("htmx:afterSwap", function (event) {
        const target = event.detail?.target;
        if (!target) return;

        if (target.id === "modal-body" || target.closest?.("#modal-body")) {
            initializeDynamicUI(getModalBody());
            setTimeout(async () => {
                await syncDependentDropdowns(getModalBody());
            }, 80);
            return;
        }

        initializeDynamicUI(document);
    });

    // document.body.addEventListener("htmx:afterRequest", async function (event) {
    //     const xhr = event.detail?.xhr;
    //     const triggers = parseHXTriggerHeader(xhr);
    //     const detail = extractRelatedSavedDetail(triggers);

    //     if (detail) {
    //         await handleRelatedSaved(detail);
    //         return;
    //     }

    //     if (triggers?.["crud:deleted"]) {
    //         const payload = triggers["crud:deleted"];
    //         Swal.fire({
    //             toast: true,
    //             position: "top-end",
    //             icon: "success",
    //             title: payload.message || "Deleted successfully.",
    //             showConfirmButton: false,
    //             timer: 1200,
    //             timerProgressBar: true,
    //         });
    //     }
    // });


    document.body.addEventListener("htmx:afterRequest", async function (event) {
    const xhr = event.detail?.xhr;
    const triggers = parseHXTriggerHeader(xhr);
    const detail = extractRelatedSavedDetail(triggers);

    if (detail) {
        await handleRelatedSaved(detail);
        return;
    }

    if (triggers?.["crud:deleted"]) {
        const payload = triggers["crud:deleted"];
        Swal.fire({
            toast: true,
            position: "top-end",
            icon: "success",
            title: payload.message || "Deleted successfully.",
            showConfirmButton: false,
            timer: 1200,
            timerProgressBar: true,
        });

        refreshMainContent();
    }
});


    document.body.addEventListener("htmx:configRequest", function (event) {
        const token = getCsrfToken();
        if (token) {
            event.detail.headers["X-CSRFToken"] = token;
        }
    });
})();