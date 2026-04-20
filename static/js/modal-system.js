
(function () {
    // Prevent duplicate script initialization (e.g., same JS loaded twice)
    if (window.__modalSystemInitialized) {
        console.warn("⚠️ modal-system.js already initialized, skipping duplicate load");
        return;
    }
    window.__modalSystemInitialized = true;

    console.log("✅ modal-system.js LOADED AND EXECUTING");
    
    const modalStack = [];
    let lastHandledSaveSignature = null;
    let lastHandledSaveAt = 0;
    let lastSaveDetail = null;
    let isJustRestoredModal = false;
    let lastRestoreTime = 0;
    let isModalFormLoading = false;
    let isRestoringModal = false;  // NEW: Flag to prevent processing while restoring

    /**
     * ============ UTILITY FUNCTIONS ============
     */

    function prefixFromPathname(pathname = "") {
        const path = (pathname || "").toString();
        if (path.startsWith("/user/")) return "/user";
        if (path.startsWith("/product/")) return "/product";
        if (path.startsWith("/globalapp/")) return "/globalapp";
        if (path.startsWith("/dashboard/")) return "/dashboard";
        return "";
    }

    function appPrefix() {
        // HTMX can keep <body> static while URL/path changes. Prefer current path.
        const fromPath = prefixFromPathname(window.location.pathname || "");
        if (fromPath) return fromPath;

        const fromBody = (document.body?.dataset?.appPrefix || "").trim();
        if (fromBody) return fromBody.replace(/\/$/, "");

        return "";
    }

    function getModalContainer() {
        const modal = document.getElementById("modal-container");
        if (!modal) {
            console.error(`❌ Modal container NOT FOUND! ID: modal-container`);
        }
        return modal;
    }

    function getModalBody() {
        const body = document.getElementById("modal-body");
        if (!body) {
            console.error(`❌ Modal body NOT FOUND! ID: modal-body`);
        }
        return body;
    }

    function showModal() {
        const modal = getModalContainer();
        if (modal) {
            console.log(`📱 showModal() called - removing hidden class`);
            modal.classList.remove("hidden");
            document.body.style.overflow = "hidden";
            console.log(`   ✅ Modal shown. Current classes:`, modal.className);
        } else {
            console.error(`❌ showModal() - no modal container found!`);
        }
    }

    function hideModal() {
        const modal = getModalContainer();
        if (modal) {
            console.log(`🔒 hideModal() called - adding hidden class`);
            modal.classList.add("hidden");
            document.body.style.overflow = "";
            console.log(`   ✅ Modal hidden. Current classes:`, modal.className);
            
            // Verify the modal is actually hidden
            setTimeout(() => {
                const isHidden = modal.classList.contains("hidden");
                console.log(`   ✔️ Verification: Modal is ${isHidden ? 'HIDDEN' : 'VISIBLE'}`);
            }, 50);
        } else {
            console.error(`❌ hideModal() - no modal container found!`);
        }
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

    function resolveRequestForm(elt) {
        if (!elt) return null;
        if (elt.tagName === "FORM") return elt;
        if (typeof elt.closest === "function") return elt.closest("form");
        return null;
    }

    function clearSubmitFallback(form) {
        if (!form || !form.__submitFallbackTimer) return;
        window.clearTimeout(form.__submitFallbackTimer);
        delete form.__submitFallbackTimer;
    }

    function scheduleSubmitFallback(form, timeoutMs = 15000) {
        if (!form) return;
        clearSubmitFallback(form);

        form.__submitFallbackTimer = window.setTimeout(() => {
            if (form.dataset.submitting === "1") {
                console.warn("⏱️ Modal submit fallback reset triggered");
                resetSubmittingState(form);
            }
        }, timeoutMs);
    }

    function ensureModalSubmitWiring(form) {
        if (!form || !form.closest("#modal-body")) return;

        const action = (form.getAttribute("action") || "").trim();
        const hxPost = (form.getAttribute("hx-post") || "").trim();

        if ((!hxPost || hxPost === "null") && action && action !== "null") {
            form.setAttribute("hx-post", action);
        }

        if (!form.hasAttribute("hx-target")) {
            form.setAttribute("hx-target", "#modal-body");
        }

        if (!form.hasAttribute("hx-swap")) {
            form.setAttribute("hx-swap", "innerHTML");
        }

        const enctype = (form.getAttribute("enctype") || "").toLowerCase();
        if (enctype === "multipart/form-data" && !form.hasAttribute("hx-encoding")) {
            form.setAttribute("hx-encoding", "multipart/form-data");
        }

        if (typeof htmx !== "undefined" && htmx.process) {
            htmx.process(form);
        }
    }

    function resetSubmittingState(form) {
        if (!form) return;

        clearSubmitFallback(form);
        delete form.dataset.submitting;

        const submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
        submitButtons.forEach((btn) => {
            btn.disabled = false;
            if (btn.tagName === "BUTTON" && btn.dataset.originalText) {
                btn.innerHTML = btn.dataset.originalText;
            } else if (btn.tagName === "INPUT" && btn.dataset.originalText) {
                btn.value = btn.dataset.originalText;
            }
        });
    }

    function syncPageChromeFromMainContent(mainEl = null, responseText = "") {
        const mainContent = mainEl || document.getElementById("main-content");
        if (!mainContent) return;

        const resolvedPrefix = prefixFromPathname(window.location.pathname || "");
        if (resolvedPrefix && document.body) {
            document.body.dataset.appPrefix = resolvedPrefix;
        }

        let responseTitle = "";
        if (responseText && responseText.includes("<title>")) {
            try {
                const parsed = new DOMParser().parseFromString(responseText, "text/html");
                responseTitle = (parsed.querySelector("title")?.textContent || "").trim();
            } catch (e) {
                responseTitle = "";
            }
        }

        const explicitPageTitle = (mainContent.getAttribute("data-page-title") || "").trim();
        const mainHeading = mainContent.querySelector("h1");
        const headingText = (mainHeading?.textContent || "").trim();
        const effectiveTitle = responseTitle || explicitPageTitle || (headingText ? `${headingText} - Management` : "");

        if (effectiveTitle && document.title !== effectiveTitle) {
            document.title = effectiveTitle;
        }

        const headerTitleEl = document.getElementById("header-page-title");
        const headerSubtitleEl = document.getElementById("header-page-subtitle");
        const contentSubtitle = mainHeading?.parentElement?.querySelector("p") || mainContent.querySelector("p");
        const explicitSubtitle = (mainContent.getAttribute("data-page-subtitle") || "").trim();

        if (headerTitleEl && headingText) {
            headerTitleEl.textContent = headingText;
        }

        if (headerSubtitleEl && explicitSubtitle) {
            headerSubtitleEl.textContent = explicitSubtitle;
        } else if (headerSubtitleEl && contentSubtitle) {
            const subText = (contentSubtitle.textContent || "").trim();
            if (subText) headerSubtitleEl.textContent = subText;
        }
    }

    // Expose for other scripts as a fallback hook.
    window.syncPageChromeFromMainContent = syncPageChromeFromMainContent;

    function findField(fieldName, root = null) {
        const base = root || currentModalForm() || document;
        return base.querySelector(`[name="${fieldName}"]`) || document.querySelector(`[name="${fieldName}"]`);
    }

    /**
     * ============ FORM STATE MANAGEMENT ============
     */

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
                    el.checked = Array.isArray(value) ? value.includes(el.value) : !!value;
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
                    el.value = strValue;

                    if (el.tomselect) {
                        if (strValue === "") {
                            el.tomselect.clear(true);
                        } else {
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

    /**
     * ============ TOM SELECT MANAGEMENT ============
     */

    function destroyTomSelectInstances(root = document) {
        root.querySelectorAll("select").forEach((el) => {
            if (el.tomselect) {
                el.tomselect.destroy();
            }
        });
    }

    function formatOptionWithId(value, text) {
        const id = value == null ? "" : String(value).trim();
        const label = text == null ? "" : String(text).trim();
        if (!id) return label;
        if (!label) return id;
        if (label.startsWith(`${id} - `)) return label;
        return `${id} - ${label}`;
    }

    function buildTomSelectConfig(el, isMulti) {
        const hideValuePrefix = el.dataset.hideValuePrefix === "1";
        const forceSearch = el.dataset.forceSearch === "1";

        function getOptionLabel(data) {
            if (!data) return "";
            const text = data.text == null ? "" : String(data.text).trim();
            if (hideValuePrefix) {
                return text;
            }
            return formatOptionWithId(data.value, data.text);
        }

        return {
            create: false,
            allowEmptyOption: true,
            placeholder: el.dataset.placeholder || "Search...",
            maxOptions: 500,
            searchField: ["text", "value"],
            hideSelected: forceSearch ? false : isMulti,
            closeAfterSelect: forceSearch ? false : !isMulti,
            openOnFocus: true,
            selectOnTab: true,
            plugins: isMulti ? ["remove_button", "clear_button"] : ["dropdown_input", "clear_button"],
            render: {
                option: function (data, escape) {
                    const label = getOptionLabel(data);
                    return `<div>${escape(label)}</div>`;
                },
                item: function (data, escape) {
                    const label = getOptionLabel(data);
                    return `<div>${escape(label)}</div>`;
                }
            }
        };
    }

    function getInitialSelectValues(el) {
        const explicit = (el.dataset.selectedValue || "").trim();

        if (el.multiple) {
            if (explicit) {
                return explicit
                    .split(",")
                    .map((v) => v.trim())
                    .filter(Boolean);
            }
            return Array.from(el.selectedOptions)
                .map((opt) => String(opt.value))
                .filter(Boolean);
        }

        if (explicit) return [explicit];
        const domValue = (el.value || "").toString().trim();
        return domValue ? [domValue] : [];
    }

    function seedSingleSelectFromData(select) {
        if (!select || select.multiple) return;

        const preferred = (select.dataset.selectedValue || "").trim();
        if (!preferred) return;

        const existing = Array.from(select.options).find(
            (opt) => String(opt.value) === preferred
        );

        if (existing) {
            existing.selected = true;
            select.value = preferred;
            return;
        }

        // Keep UI non-empty until dependent options are reloaded.
        const synthetic = new Option(preferred, preferred, false, true);
        synthetic.dataset.synthetic = "1";
        select.add(synthetic);
        select.value = preferred;
    }

    function initTomSelect(root = document) {
        root.querySelectorAll("select").forEach((el) => {
            if (el.tomselect) return;

            // Allow opting out for specific selects when needed.
            if (el.dataset.noEnhance === "1") return;

            // Skip hidden selects used only for transport.
            if (el.type === "hidden") return;

            seedSingleSelectFromData(el);

            const initialValues = getInitialSelectValues(el);
            const control = new TomSelect(el, buildTomSelectConfig(el, !!el.multiple));

            if (initialValues.length) {
                if (el.multiple) {
                    control.setValue(initialValues, true);
                } else {
                    control.setValue(initialValues[0], true);
                }
            }

            el.dataset.selectedValue = el.multiple
                ? initialValues.join(",")
                : (initialValues[0] || "");

            control.on("change", function (value) {
                if (Array.isArray(value)) {
                    el.dataset.selectedValue = value.filter(Boolean).map(String).join(",");
                    return;
                }
                el.dataset.selectedValue = value ? String(value) : "";
            });
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

    /**
     * ============ SELECT VALUE MANAGEMENT ============
     */

    function setSingleSelectValue(select, value, text, silent = false) {
        if (!select) return false;

        value = String(value);

        // Add or update option
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

        // Update TomSelect if available
        if (select.tomselect) {
            select.tomselect.addOption({ value, text });
            select.tomselect.setValue(value, silent);
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

        // Add or update option
        let existing = Array.from(select.options).find(opt => String(opt.value) === value);
        if (!existing) {
            existing = new Option(text, value, true, true);
            select.add(existing);
        } else {
            existing.selected = true;
        }

        // Update TomSelect if available
        if (select.tomselect) {
            select.tomselect.addOption({ value, text });

            const current = select.tomselect.getValue();
            const arr = Array.isArray(current) ? current : (current ? [current] : []);
            const next = [...new Set([...arr.map(String), value])];

            select.tomselect.setValue(next, silent);
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

    function ensureRelatedOptionSelected(fieldName, option, root = null, tries = 20, delay = 150, silent = false) {
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

    async function stabilizeRelatedSelection(fieldName, option, root = document) {
        if (!fieldName || !option) return;

        ensureRelatedOptionSelected(fieldName, option, root, 20, 100, true);

        const targetField = findField(fieldName, root);
        const container = getDependentContainer(targetField);
        if (container) {
            await syncDependentDropdowns(container);
            ensureRelatedOptionSelected(fieldName, option, root, 20, 100, true);
        }
    }

    function getSelectedValue(fieldName, root = null) {
        const el = findField(fieldName, root);
        if (!el) return "";
        return el.value || "";
    }

    function getFieldInContainer(container, names) {
        if (!container || !container.querySelector) return null;
        for (const name of names) {
            const found = container.querySelector(`[name="${name}"]`);
            if (found) return found;
        }
        return null;
    }

    function getSelectedValues(select) {
        if (!select) return [];
        if (select.multiple) {
            const selected = Array.from(select.selectedOptions).map((opt) => String(opt.value));
            if (selected.length) return selected;
            return (select.dataset.selectedValue || "")
                .split(",")
                .map((v) => v.trim())
                .filter(Boolean);
        }
        if (select.value) return [String(select.value)];
        const fallback = (select.dataset.selectedValue || "").trim();
        return fallback ? [fallback] : [];
    }

    function replaceSelectOptions(select, results, selectedValues = []) {
        if (!select) return;

        const previousOptionTextByValue = new Map(
            Array.from(select.options).map((opt) => [String(opt.value), opt.text])
        );

        const fallbackSelectedValues = (select.dataset.selectedValue || "")
            .split(",")
            .map((v) => v.trim())
            .filter(Boolean);

        const effectiveSelectedValues = (selectedValues && selectedValues.length)
            ? selectedValues
            : fallbackSelectedValues;

        const selectedSet = new Set((effectiveSelectedValues || []).map((v) => String(v)));
        const existingPlaceholder = Array.from(select.options).find((opt) => String(opt.value) === "");
        const placeholderText = existingPlaceholder ? existingPlaceholder.text : "---------";

        select.innerHTML = "";

        if (!select.multiple) {
            select.add(new Option(placeholderText, "", false, selectedSet.size === 0));
        }

        const addedValues = new Set();

        (results || []).forEach((item) => {
            const value = String(item.id);
            const text = item.text || value;
            const isSelected = selectedSet.has(value);
            select.add(new Option(text, value, false, isSelected));
            addedValues.add(value);
        });

        // Keep previously selected value(s) visible even if current API response
        // doesn't include them (e.g., strict branch/area scoped options in update mode).
        selectedSet.forEach((value) => {
            if (!value || addedValues.has(value)) return;
            const fallbackText = previousOptionTextByValue.get(value) || value;
            select.add(new Option(fallbackText, value, false, true));
        });

        if (select.multiple) {
            select.dataset.selectedValue = Array.from(selectedSet).join(",");
        } else {
            const singleValue = Array.from(selectedSet)[0] || "";
            select.dataset.selectedValue = singleValue;
            select.value = singleValue;
        }

        refreshTomSelect(select);
    }

    function getDependentContainer(field) {
        return (
            field?.closest("form") ||
            field?.closest("#modal-body") ||
            field?.closest("#main-content") ||
            document
        );
    }

    async function reloadAreasForBranch(container) {
        const branchField = getFieldInContainer(container, ["branch", "parent_branch"]);
        const areaField = getFieldInContainer(container, ["area"]);
        if (!branchField || !areaField) return;

        const selectedFromControl = getSelectedValues(areaField);
        const selectedFromData = (areaField.dataset.selectedValue || "")
            .split(",")
            .map((v) => v.trim())
            .filter(Boolean);

        const previousAreaSelection = selectedFromControl.length
            ? selectedFromControl
            : selectedFromData;
        const hadAreaSelection = previousAreaSelection.length > 0;
        const params = new URLSearchParams();
        if (branchField.value) {
            params.set("branch_id", branchField.value);
        }

        try {
            const query = params.toString();
            const data = await fetchJSON(`/user/ajax/options/areas/${query ? `?${query}` : ""}`);
            replaceSelectOptions(areaField, data.results || [], previousAreaSelection);

            // If branch is selected but area is empty (legacy data), pick the first
            // available area so update forms/modals don't render with a blank area.
            if (!areaField.multiple && branchField.value && !hadAreaSelection) {
                const firstAreaOption = Array.from(areaField.options).find((opt) => String(opt.value || "").trim() !== "");
                if (firstAreaOption) {
                    const value = String(firstAreaOption.value);
                    areaField.value = value;
                    areaField.dataset.selectedValue = value;
                    refreshTomSelect(areaField);
                }
            }
        } catch (error) {
            console.warn("Failed to reload areas by branch", error);
        }
    }

    async function reloadSubcategoriesForCategory(container) {
        const categoryField = getFieldInContainer(container, ["category_name", "category"]);
        const subcategoryField = getFieldInContainer(container, ["subcategory_name", "subcategory"]);
        if (!categoryField || !subcategoryField) return;

        const previousCategorySelection = (subcategoryField.dataset.lastCategoryValue || "").trim();
        const currentCategorySelection = String(categoryField.value || "").trim();
        const categoryChanged = previousCategorySelection !== "" && previousCategorySelection !== currentCategorySelection;

        const existingOptionTextByValue = new Map(
            Array.from(subcategoryField.options).map((opt) => [String(opt.value), opt.text])
        );

        const selectedFromControl = getSelectedValues(subcategoryField);
        const selectedFromData = (subcategoryField.dataset.selectedValue || "")
            .split(",")
            .map((v) => v.trim())
            .filter(Boolean);

        const previousSelection = selectedFromControl.length
            ? selectedFromControl
            : selectedFromData;

        const previousSingleSelection = !subcategoryField.multiple && previousSelection.length
            ? String(previousSelection[0])
            : "";

        const previousSingleText = previousSingleSelection
            ? String(existingOptionTextByValue.get(previousSingleSelection) || previousSingleSelection)
            : "";

        const params = new URLSearchParams();
        if (categoryField.value) {
            params.set("category_id", categoryField.value);
        }

        try {
            const query = params.toString();
            const data = await fetchJSON(`/product/ajax/options/subcategories/${query ? `?${query}` : ""}`);
            const selectedForReplacement = categoryChanged ? [] : previousSelection;
            replaceSelectOptions(subcategoryField, data.results || [], selectedForReplacement);

            if (!subcategoryField.multiple && previousSingleSelection && !categoryChanged) {
                let option = Array.from(subcategoryField.options).find((opt) => String(opt.value) === previousSingleSelection);

                if (!option) {
                    option = new Option(previousSingleText, previousSingleSelection, false, true);
                    subcategoryField.add(option);
                } else {
                    option.selected = true;
                }

                subcategoryField.value = previousSingleSelection;
                subcategoryField.dataset.selectedValue = previousSingleSelection;
                refreshTomSelect(subcategoryField);
            }

            if (categoryChanged) {
                subcategoryField.value = "";
                subcategoryField.dataset.selectedValue = "";
                refreshTomSelect(subcategoryField);
            }

            subcategoryField.dataset.lastCategoryValue = currentCategorySelection;
        } catch (error) {
            console.warn("Failed to reload subcategories by category", error);
        }
    }

    async function reloadCustomerGroups(container) {
        const branchField = getFieldInContainer(container, ["branch", "parent_branch"]);
        const areaField = getFieldInContainer(container, ["area"]);
        const customerGroupField = getFieldInContainer(container, ["customer_group", "total_customers"]);
        if (!customerGroupField) return;

        const selectedFromControl = getSelectedValues(customerGroupField);
        const selectedFromData = (customerGroupField.dataset.selectedValue || "")
            .split(",")
            .map((v) => v.trim())
            .filter(Boolean);

        const previousCustomerGroupSelection = selectedFromControl.length
            ? selectedFromControl
            : selectedFromData;
        const params = new URLSearchParams();

        if (branchField && branchField.value) {
            params.set("branch_id", branchField.value);
        }
        if (areaField && areaField.value) {
            params.set("area_id", areaField.value);
        }

        try {
            const query = params.toString();
            const data = await fetchJSON(`/user/ajax/options/customer-groups/${query ? `?${query}` : ""}`);
            replaceSelectOptions(customerGroupField, data.results || [], previousCustomerGroupSelection);
        } catch (error) {
            console.warn("Failed to reload customer groups", error);
        }
    }

    async function syncDependentDropdowns(container) {
        if (!container) return;
        await reloadAreasForBranch(container);
        await reloadSubcategoriesForCategory(container);
        await reloadCustomerGroups(container);
    }

    function initializeDependentHandlers(root = document) {
        const containersToInit = new Set();

        if (root.matches && root.matches("form")) {
            containersToInit.add(root);
        }

        if (root.querySelectorAll) {
            root.querySelectorAll("form").forEach((form) => containersToInit.add(form));

            root.querySelectorAll('select[name="branch"], select[name="parent_branch"]').forEach((branchField) => {
                const container = getDependentContainer(branchField);
                containersToInit.add(container);

                if (branchField.dataset.boundDependent === "1") return;
                branchField.dataset.boundDependent = "1";

                branchField.addEventListener("change", async () => {
                    await syncDependentDropdowns(container);
                });
            });

            root.querySelectorAll('select[name="area"]').forEach((areaField) => {
                const container = getDependentContainer(areaField);
                containersToInit.add(container);

                if (areaField.dataset.boundDependent === "1") return;
                areaField.dataset.boundDependent = "1";

                areaField.addEventListener("change", async () => {
                    await reloadCustomerGroups(container);
                });
            });

            root.querySelectorAll('select[name="category_name"], select[name="category"]').forEach((categoryField) => {
                const container = getDependentContainer(categoryField);
                containersToInit.add(container);

                if (categoryField.dataset.boundDependentSubcategory === "1") return;
                categoryField.dataset.boundDependentSubcategory = "1";

                categoryField.addEventListener("change", async () => {
                    await reloadSubcategoriesForCategory(container);
                });
            });
        }

        containersToInit.forEach((container) => {
            syncDependentDropdowns(container);
        });
    }

    function initializeProductTypeVisibility(root = document) {
        const mainContent = root?.id === "main-content"
            ? root
            : (root?.querySelector?.("#main-content") || document.getElementById("main-content"));

        if (!mainContent) return;

        const productTypeField = mainContent.querySelector('[name="product_type"]');
        if (!productTypeField) return;

        const pricingTaxStockSettings = mainContent.querySelector("#pricing-tax-stock-settings");
        const variationSection = mainContent.querySelector("#variation-section");
        const singleQuantityWrapper = mainContent.querySelector("#single-quantity-wrapper");
        const enableImeiWrapper = mainContent.querySelector("#enable-imei-wrapper");
        const singleImeiSection = mainContent.querySelector("#single-stock-imei-section");

        const applyVisibility = function () {
            const productTypeValue = String(productTypeField.value || "").toLowerCase();
            const isVariationMode = ["variable", "variation", "combo"].includes(productTypeValue);

            if (pricingTaxStockSettings) {
                pricingTaxStockSettings.style.display = isVariationMode ? "none" : "";
            }
            if (singleQuantityWrapper) {
                singleQuantityWrapper.style.display = isVariationMode ? "none" : "";
            }
            if (enableImeiWrapper) {
                enableImeiWrapper.style.display = isVariationMode ? "none" : "";
            }
            if (variationSection) {
                variationSection.style.display = isVariationMode ? "" : "none";
            }
            if (singleImeiSection) {
                singleImeiSection.style.display = isVariationMode ? "none" : "";
            }
        };

        if (productTypeField.dataset.boundProductTypeVisibility !== "1") {
            productTypeField.dataset.boundProductTypeVisibility = "1";
            productTypeField.addEventListener("change", applyVisibility);
            productTypeField.addEventListener("input", applyVisibility);
        }

        applyVisibility();
    }

    /**
     * ============ MODAL OPERATIONS ============
     */

    function clearBindingMarkers(root) {
        if (!root?.querySelectorAll) return;
        root.querySelectorAll("[data-bound-click], [data-bound-dependent], [data-bound-dependent-subcategory], [data-submit-guard-bound], [data-main-ajax-bound], [data-submitting], [data-original-text]").forEach((el) => {
            el.removeAttribute("data-bound-click");
            el.removeAttribute("data-bound-dependent");
            el.removeAttribute("data-bound-dependent-subcategory");
            el.removeAttribute("data-submit-guard-bound");
            el.removeAttribute("data-main-ajax-bound");
            el.removeAttribute("data-submitting");
            el.removeAttribute("data-original-text");
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
            return null;
        }
    }

    function extractRelatedSavedDetail(triggers) {
        if (!triggers) return null;
        return triggers["related:saved"] || triggers["crud:saved"] || null;
    }

    function extractDeletedDetail(triggers) {
        if (!triggers) return null;
        return triggers["crud:deleted"] || null;
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
        const timeDiff = now - lastHandledSaveAt;
        const isDup = signature === lastHandledSaveSignature && timeDiff < 1200;

        if (!isDup) {
            lastHandledSaveSignature = signature;
            lastHandledSaveAt = now;
        }

        return isDup;
    }

    /**
     * ============ NESTED MODAL HANDLING ============
     */

    function buildRelatedUrl(modelName, action, pk = null, extraParams = {}) {
        let url = `${appPrefix()}/ajax/related/${modelName}/create/`;
        if (action === "edit" && pk) {
            url = `${appPrefix()}/ajax/related/${modelName}/${pk}/edit/`;
        }

        const params = new URLSearchParams();
        Object.entries(extraParams).forEach(([key, value]) => {
            if (value !== null && value !== undefined && value !== "") {
                params.append(key, value);
            }
        });

        const qs = params.toString();
        return qs ? `${url}?${qs}` : url;
    }

    function openModalWithUrl(url, isNested = false) {
        const body = getModalBody();
        if (!body) return;

        // Save current modal state if nested
        if (isNested && body.innerHTML.trim()) {
            const state = captureFormState(body);
            const selectOptions = captureSelectOptions(body);
            const form = body.querySelector("form");
            const parentFieldValue = form?.querySelector('[name="_parent_field"]')?.value || "";

            destroyTomSelectInstances(body);

            modalStack.push({
                html: getCleanHtmlForStack(body),
                state,
                selectOptions,
                parentFieldValue,
            });
        }

        showModal();
        
        isModalFormLoading = true;
        
        // Using HTMX if available, otherwise fetch
        if (typeof htmx !== 'undefined') {
            // Clear body before loading new modal
            body.innerHTML = "";
            htmx.ajax("GET", url, {
                target: "#modal-body",
                swap: "innerHTML"
            });
        } else {
            fetch(url)
                .then(response => response.text())
                .then(html => {
                    body.innerHTML = html;
                    initializeDynamicUI(body);
                    isModalFormLoading = false;
                    console.log(`   Set isModalFormLoading = false`);
                })
                .catch(error => {
                    console.error("Failed to load modal:", error);
                    isModalFormLoading = false;
                    Swal.fire("Error", "Failed to load modal", "error");
                });
        }
    }

    /**
     * ============ RELATED BUTTONS HANDLING ============
     */

    function initializeRelatedButtons(root = document) {
        // Create button
        root.querySelectorAll(".related-create-btn").forEach((btn) => {
            if (btn.dataset.boundClick) return;
            btn.dataset.boundClick = "1";

            btn.addEventListener("click", function (event) {
                event.preventDefault();
                event.stopPropagation();

                const modelName = this.dataset.model;
                const fieldName = this.dataset.fieldName;
                const params = { parent_field: fieldName };

                // Handle dependent fields
                if (modelName === "area") {
                    const branchId = getSelectedValue("branch", root) || getSelectedValue("parent_branch", root);
                    if (branchId) params.branch_id = branchId;
                }

                if (modelName === "customergroup") {
                    const branchId = getSelectedValue("branch", root) || getSelectedValue("parent_branch", root);
                    const areaId = getSelectedValue("area", root);
                    if (branchId) params.branch_id = branchId;
                    if (areaId) params.area_id = areaId;
                }

                if (modelName === "subcategory") {
                    const categoryId = getSelectedValue("category_name", root) || getSelectedValue("category", root);
                    if (categoryId) params.category_id = categoryId;
                }

                if (modelName === "variation_attribute_value") {
                    const sourceFieldName = this.dataset.attributeSource;
                    const attributeId = sourceFieldName
                        ? getSelectedValue(sourceFieldName, root)
                        : (getSelectedValue("attribute", root) || getSelectedValue("variation_attribute", root));
                    if (attributeId) params.attribute_id = attributeId;
                }

                const modal = getModalContainer();
                // Check if modal is visible (not hidden)
                const isNested = modal && !modal.classList.contains("hidden");
                openModalWithUrl(buildRelatedUrl(modelName, "create", null, params), isNested);
            });
        });

        // Edit button
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
                // Check if modal is visible (not hidden)
                const isNested = modal && !modal.classList.contains("hidden");
                openModalWithUrl(buildRelatedUrl(modelName, "edit", pk, params), isNested);
            });
        });
    }

    /**
     * ============ FORM INITIALIZATION ============
     */

    function initializeFormSubmitGuard(root = document) {
        root.querySelectorAll("form").forEach((form) => {
            // IMPORTANT: only guard modal forms.
            // Guarding every page form forces CRUD posts into #modal-body and breaks normal redirects.
            if (!form.closest("#modal-body")) return;

            if (form.dataset.submitGuardBound === "1") return;
            form.dataset.submitGuardBound = "1";

            ensureModalSubmitWiring(form);

            form.addEventListener("submit", function (event) {
                ensureModalSubmitWiring(form);

                // Check if already submitting
                if (form.dataset.submitting === "1") {
                    event.preventDefault();
                    event.stopPropagation();
                    return false;
                }

                form.dataset.submitting = "1";

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

                scheduleSubmitFallback(form);

                // Let HTMX/native submit continue through one single request pipeline.
                return true;
            });

            // Re-enable buttons if form response is an error (200 with HTML, not 204)
            form.addEventListener("htmx:responseError", function (event) {
                console.log(`❌ Form response error`);
                resetSubmittingState(form);
            });
        });
    }

    function initializeMainContentForms(root = document) {
        const mainContents = [];

        if (root?.id === "main-content") {
            mainContents.push(root);
        }

        if (root?.querySelectorAll) {
            mainContents.push(...root.querySelectorAll("#main-content"));
        }

        if (!mainContents.length) {
            const fallback = document.getElementById("main-content");
            if (fallback) mainContents.push(fallback);
        }

        const uniqueMainContents = [...new Set(mainContents)];

        uniqueMainContents.forEach((main) => {
            main.querySelectorAll("form").forEach((form) => {
                if (form.closest("#modal-body")) return;
                if (form.dataset.noMainAjax === "1") return;
                if (form.dataset.mainAjaxBound === "1") return;

                form.dataset.mainAjaxBound = "1";

                const hasHxMethod = form.hasAttribute("hx-get") || form.hasAttribute("hx-post") || form.hasAttribute("hx-put") || form.hasAttribute("hx-patch") || form.hasAttribute("hx-delete");
                const method = (form.getAttribute("method") || "get").toLowerCase();
                const action = form.getAttribute("action") || window.location.href;
                const explicitTarget = (form.getAttribute("hx-target") || "").trim();
                const targetsMainContent = !explicitTarget || explicitTarget === "#main-content" || explicitTarget === "main-content";

                if (!hasHxMethod) {
                    if (method === "get") {
                        form.setAttribute("hx-get", action);
                    } else {
                        form.setAttribute("hx-post", action);
                    }
                }

                // Only apply main-content defaults when this form is intended to update main-content.
                if (targetsMainContent) {
                    if (!form.hasAttribute("hx-target")) form.setAttribute("hx-target", "#main-content");
                    if (!form.hasAttribute("hx-select")) form.setAttribute("hx-select", "#main-content");
                    if (!form.hasAttribute("hx-swap")) form.setAttribute("hx-swap", "outerHTML");
                }

                // GET filter/search forms should update URL; POST forms should not force request URL in history.
                if (method === "get" && !form.hasAttribute("hx-push-url")) {
                    form.setAttribute("hx-push-url", "true");
                }

                const enctype = (form.getAttribute("enctype") || "").toLowerCase();
                if (enctype === "multipart/form-data" && !form.hasAttribute("hx-encoding")) {
                    form.setAttribute("hx-encoding", "multipart/form-data");
                }

                if (typeof htmx !== "undefined" && htmx.process) {
                    htmx.process(form);
                }
            });
        });
    }

    function initializeDynamicUI(root = document) {
        clearBindingMarkers(root);
        initTomSelect(root);
        initializeRelatedButtons(root);
        initializeFormSubmitGuard(root);
        initializeMainContentForms(root);
        initializeDependentHandlers(root);
        initializeProductTypeVisibility(root);
    }

    // Expose this for page-specific scripts (e.g., dynamic product variation slots)
    // so newly injected selects can be enhanced consistently.
    window.initializeDynamicUI = initializeDynamicUI;

    /**
     * ============ MODAL SAVE HANDLING ============
     */

    async function restorePreviousModalAndApply(detail) {
        console.log(`\n${'='.repeat(50)}`);
        console.log(`📥 restorePreviousModalAndApply() CALLED`);
        console.log(`   modalStack.length BEFORE pop: ${modalStack.length}`);
        
        const previous = modalStack.pop();
        const body = getModalBody();
        
        console.log(`   modalStack.length AFTER pop: ${modalStack.length}`);
        console.log(`   previous exists: ${!!previous}`);
        console.log(`   body exists: ${!!body}`);
        
        if (!body || !previous) {
            console.error(`❌ Cannot restore: body=${!!body}, previous=${!!previous}`);
            console.log(`${'='.repeat(50)}\n`);
            return;
        }

        console.log(`📥 Restoring previous modal from stack...`);
        isRestoringModal = true;  // Prevent handleRelatedSaved from processing during restore
        lastRestoreTime = Date.now();
        isJustRestoredModal = true;
        console.log(`   Set isJustRestoredModal = true`);

        // Step 1: Clear everything
        console.log(`   Step 1: Destroying TomSelect instances...`);
        destroyTomSelectInstances(body);
        body.innerHTML = "";
        
        // Step 2: Restore HTML
        console.log(`   Step 2: Restoring HTML...`);
        body.innerHTML = previous.html;

        // Step 3: Clear binding markers
        console.log(`   Step 3: Clearing binding markers...`);
        clearBindingMarkers(body);
        
        // Step 3.5: Restore the hidden _parent_field value
        console.log(`   Step 3.5: Restoring _parent_field...`);
        const parentFieldInput = body.querySelector('[name="_parent_field"]');
        if (parentFieldInput && previous.parentFieldValue) {
            console.log(`      Restoring _parent_field to "${previous.parentFieldValue}"`);
            parentFieldInput.value = previous.parentFieldValue;
        } else if (parentFieldInput) {
            console.log(`      Clearing _parent_field (no saved value)`);
            parentFieldInput.value = "";
        } else {
            console.log(`      ⚠️ No _parent_field input found!`);
        }
        
        // Step 4: Make sure modal is visible
        console.log(`   Step 4: Showing modal...`);
        showModal();

        // Step 5: Wait for DOM to settle
        await new Promise(resolve => setTimeout(resolve, 50));

        // Step 6: Re-initialize everything
        console.log(`   Step 6: Re-initializing UI...`);
        initializeDynamicUI(body);

        if (typeof htmx !== "undefined" && htmx.process) {
            htmx.process(body);
        }
        
        // Step 7: Restore form state
        console.log(`   Step 7: Restoring form state...`);
        restoreSelectOptions(body, previous.selectOptions || {});
        restoreFormState(body, previous.state);

        // Step 8: Wait again for UI updates
        await new Promise(resolve => setTimeout(resolve, 100));

        // Step 9: Restore again to ensure it sticks
        console.log(`   Step 9: Re-restoring form state to ensure it sticks...`);
        restoreSelectOptions(body, previous.selectOptions || {});
        restoreFormState(body, previous.state);

        // Step 10: Auto-select the newly created item
        console.log(`   Step 10: Auto-selecting newly created item...`);
        console.log(`      detail.parentField: ${detail.parentField}`);
        console.log(`      detail.option: ${JSON.stringify(detail.option)}`);
        
        if (detail.parentField && detail.option) {
            console.log(`      ✅ Calling ensureRelatedOptionSelected("${detail.parentField}", ...)`);
            await stabilizeRelatedSelection(detail.parentField, detail.option, body);
        } else {
            console.log(`      ⚠️ Cannot auto-select: missing parentField or option`);
        }

        // Step 11: Show success message
        console.log(`   Step 11: Showing success toast...`);
        Swal.fire({
            toast: true,
            position: "top-end",
            icon: "success",
            title: detail.message || "Saved successfully!",
            showConfirmButton: false,
            timer: 1000,
            timerProgressBar: true,
        });
        
        console.log(`✅ Parent modal restored successfully`);
        
        // Clear the "just restored" flag after a short delay
        setTimeout(() => {
            isJustRestoredModal = false;
            console.log(`   Cleared isJustRestoredModal flag`);
        }, 2000);
        
        isRestoringModal = false;  // Allow handleRelatedSaved to process again
        console.log(`${'='.repeat(50)}\n`);
    }

    async function handleRelatedSaved(detail) {
        console.log(`\n${'='.repeat(50)}`);
        console.log(`🎯 handleRelatedSaved called`);
        console.log(`   Detail:`, detail);
        
        // GUARD: Don't process if we're currently restoring a modal
        if (isRestoringModal) {
            console.log(`⏭️ SKIPPING: Currently restoring a modal`);
            console.log(`${'='.repeat(50)}\n`);
            return;
        }
        
        const body = getModalBody();
        if (!body) {
            console.error(`❌ Modal body not found!`);
            console.log(`${'='.repeat(50)}\n`);
            return;
        }
        
        if (!detail) {
            console.error(`❌ Detail not provided!`);
            console.log(`${'='.repeat(50)}\n`);
            return;
        }
        
        if (isDuplicateSaveEvent(detail)) {
            console.log(`⏭️  Duplicate event - skipping`);
            console.log(`${'='.repeat(50)}\n`);
            return;
        }

        const form = currentModalForm();
        const parentFieldValue = form?.querySelector('[name="_parent_field"]')?.value || "";
        
        // Better nested detection: check if parent_field is not empty AND stack has items
        // Also, if parent_field is explicitly set, this is a nested modal
        let isNested = parentFieldValue && parentFieldValue.trim() !== "" && modalStack.length > 0;
        
        // SAFETY OVERRIDE: If we just restored a modal, don't treat it as nested on first submit
        // The restored modal's form will have a parent_field value from when it was first opened as nested,
        // but after restoration we want its next submit to close the modal (top-level behavior)
        if (isJustRestoredModal && isNested) {
            console.log(`⚠️ OVERRIDE: isJustRestoredModal=true and isNested=true`);
            console.log(`   This is likely a restored form that should be treated as TOP-LEVEL`);
            console.log(`   Converting from nested to top-level...`);
            isNested = false;  // Override to treat as top-level
        }

        console.log(`🔍 Modal Analysis:`);
        console.log(`   _parent_field value: "${parentFieldValue}"`);
        console.log(`   _parent_field trimmed: "${parentFieldValue.trim()}"`);
        console.log(`   _parent_field is truthy: ${!!parentFieldValue}`);
        console.log(`   modalStack.length: ${modalStack.length}`);
        console.log(`   isNested (before override): ${parentFieldValue && parentFieldValue.trim() !== "" && modalStack.length > 0}`);
        console.log(`   isNested (after override): ${isNested}`);
        console.log(`   Form exists: ${!!form}`);
        console.log(`   Modal container hidden: ${getModalContainer()?.classList.contains('hidden')}`);
        console.log(`   isJustRestoredModal: ${isJustRestoredModal}`);

        // Show success toast for ALL saves (both nested and top-level)
        console.log(`🎉 Showing success toast...`);
        console.log(`   Message: "${detail.message || 'Saved successfully!'}"`);
        
        try {
            Swal.fire({
                toast: true,
                position: "top-end",
                icon: "success",
                title: detail.message || "Saved successfully!",
                showConfirmButton: false,
                timer: 2000,
                timerProgressBar: true,
                didOpen: (toast) => {
                    console.log(`   ✅ Toast appeared on screen`);
                },
                didClose: (toast) => {
                    console.log(`   ✅ Toast closed`);
                }
            });
        } catch (error) {
            console.error(`❌ Failed to show Swal alert:`, error);
            // Fallback alert
            alert(detail.message || "Saved successfully!");
        }

        // Nested modal: restore previous modal
        if (isNested) {
            console.log(`\n📤 DECISION: This is NESTED - will restore parent modal`);
            console.log(`   Stack before restore: ${modalStack.length}`);
            await restorePreviousModalAndApply(detail);
            console.log(`   Stack after restore: ${modalStack.length}`);
            console.log(`${'='.repeat(50)}\n`);
            return;
        }

        // Top-level modal: auto-select on parent page and close
        console.log(`\n🔒 DECISION: This is TOP-LEVEL - will close modal`);
        console.log(`   parentField from detail:`, detail.parentField);
        console.log(`   option from detail:`, detail.option);
        console.log(`   Current stack length:`, modalStack.length);
        
        if (detail.parentField && detail.option) {
            console.log(`   Auto-selecting on parent page: ${detail.parentField} = ${detail.option.text}`);
            await stabilizeRelatedSelection(detail.parentField, detail.option, document);
        }

        // Close modal after showing the message (increased timeout for better UX)
        console.log(`⏳ Waiting 1000ms before closing modal...`);
        await new Promise(resolve => setTimeout(resolve, 1000));
        console.log(`   Clearing modal body...`);
        body.innerHTML = "";
        console.log(`   Body cleared. Force closing modal...`);
        hideModal();
        
        // Make absolutely sure it's hidden
        await new Promise(resolve => setTimeout(resolve, 50));
        const modal = getModalContainer();
        if (modal && !modal.classList.contains("hidden")) {
            console.warn(`⚠️ Modal still visible! Force-hiding...`);
            modal.classList.add("hidden");
            document.body.style.overflow = "";
        }
        
        // Verify and log final state
        await new Promise(resolve => setTimeout(resolve, 100));
        const isHidden = getModalContainer()?.classList.contains("hidden");
        console.log(`✅ Modal close complete! Hidden=${isHidden}, StackLength=${modalStack.length}`);
        console.log(`${'='.repeat(50)}\n`);
    }

    /**
     * ============ GLOBAL API ============
     */

    window.closeModal = function () {
        console.log(`\n${'='.repeat(50)}`);
        console.log(`📞 closeModal() called`);
        console.log(`   Current stack length: ${modalStack.length}`);
        
        // If there's a nested modal in stack, restore previous
        if (modalStack.length > 0) {
            const previous = modalStack.pop();
            const body = getModalBody();
            
            console.log(`📤 Restoring parent modal from stack. Remaining: ${modalStack.length}`);
            
            if (body && previous) {
                // Clean up current modal - destroy TomSelect instances
                destroyTomSelectInstances(body);
                body.innerHTML = "";
                
                // Restore previous
                body.innerHTML = previous.html;
                clearBindingMarkers(body);
                showModal();
                
                // Re-initialize
                initializeDynamicUI(body);
                if (typeof htmx !== "undefined" && htmx.process) {
                    htmx.process(body);
                }
                restoreSelectOptions(body, previous.selectOptions || {});
                restoreFormState(body, previous.state);
                
                console.log(`✅ Parent modal restored`);
            } else {
                console.warn(`⚠️ Previous modal data missing`, {previous, body});
            }
            console.log(`${'='.repeat(50)}\n`);
            return;
        }

        // Otherwise, close modal completely
        console.log("🔒 Closing modal completely (no parent to restore)");
        const body = getModalBody();
        if (body) {
            // Cleanup TomSelect instances first
            destroyTomSelectInstances(body);
            
            // Clear modal body (this will trigger HTMX cleanup naturally)
            body.innerHTML = "";
            console.log(`   Modal body cleared`);
        }
        
        hideModal();
        console.log(`✅ Modal closed completely`);
        console.log(`${'='.repeat(50)}\n`);
    };

    window.showErrorAlert = function (message) {
        Swal.fire("Error", message, "error");
    };

    window.showSuccessAlert = function (message) {
        Swal.fire({
            toast: true,
            position: "top-end",
            icon: "success",
            title: message,
            showConfirmButton: false,
            timer: 1200,
            timerProgressBar: true,
        });
    };

    /**
     * ============ STARTUP VERIFICATION ============
     */

    function verifyModalSystem() {
        console.log(`\n${'='.repeat(50)}`);
        console.log(`✅ MODAL SYSTEM INITIALIZING...`);
        
        const container = document.getElementById("modal-container");
        const body = document.getElementById("modal-body");
        const backdrop = document.getElementById("modal-backdrop");
        
        console.log(`   Modal container: ${container ? '✅ FOUND' : '❌ NOT FOUND'}`);
        console.log(`   Modal body: ${body ? '✅ FOUND' : '❌ NOT FOUND'}`);
        console.log(`   Modal backdrop: ${backdrop ? '✅ FOUND' : '❌ NOT FOUND'}`);
        
        if (!container || !body || !backdrop) {
            console.error(`❌ MODAL STRUCTURE INCOMPLETE!`);
            console.error(`   Check base.html has modal-container, modal-body, modal-backdrop`);
        } else {
            console.log(`✅ Modal structure is complete`);
        }
        
        console.log(`✅ Modal system ready!`);
        console.log(`${'='.repeat(50)}\n`);
    }

    /**
     * ============ EVENT LISTENERS ============
     */

    document.addEventListener("DOMContentLoaded", function () {
        // Verify modal system is initialized
        verifyModalSystem();
        
        // Initialize UI
        initializeDynamicUI(document);
        syncPageChromeFromMainContent();

        // Modal backdrop click handler
        const backdrop = document.getElementById("modal-backdrop");
        if (backdrop) {
            backdrop.addEventListener("click", function (event) {
                if (event.target === this) {
                    closeModal();
                }
            });
        }

        // Modal trigger handler
        document.body.addEventListener("click", function (event) {
            const trigger = event.target.closest(".modal-trigger");
            if (!trigger) return;

            event.preventDefault();
            event.stopPropagation();

            const url = trigger.getAttribute("data-modal-url") || trigger.getAttribute("href");
            if (!url) return;

            openModalWithUrl(url, false);
        });

        // In-content links should swap via HTMX instead of forcing full page reload.
        document.body.addEventListener("click", function (event) {
            const link = event.target.closest("#main-content a");
            if (!link) return;

            if (
                link.classList.contains("modal-trigger") ||
                link.classList.contains("delete-btn") ||
                link.hasAttribute("download") ||
                link.target === "_blank" ||
                link.dataset.noHtmx === "1"
            ) {
                return;
            }

            const href = link.getAttribute("href") || "";
            if (!href || href.startsWith("#") || href.startsWith("javascript:") || href.startsWith("mailto:") || href.startsWith("tel:")) {
                return;
            }

            // Let explicit hx-* attributes work normally.
            if (link.hasAttribute("hx-get") || link.hasAttribute("hx-post") || link.hasAttribute("hx-boost")) {
                return;
            }

            event.preventDefault();
            if (typeof htmx !== "undefined") {
                htmx.ajax("GET", href, {
                    source: link,
                    target: "#main-content",
                    select: "#main-content",
                    swap: "outerHTML",
                    pushUrl: true
                });
            } else {
                window.location.href = href;
            }
        });

        // Delete button handler
        document.body.addEventListener("click", function (event) {
            const btn = event.target.closest(".delete-btn");
            if (!btn) return;

            event.preventDefault();

            const url = btn.dataset.url;
            if (!url) return;

            Swal.fire({
                title: "আপনি কি নিশ্চিত?",
                text: "এই পদক্ষেপ পরিবর্তন করা যাবে না।",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "হ্যাঁ, মুছে দিন",
                cancelButtonText: "বাতিল"
            }).then((result) => {
                if (!result.isConfirmed) return;

                if (typeof htmx !== "undefined") {
                    htmx.ajax("POST", url, {
                        source: btn,
                        target: "#main-content",
                        swap: "none",
                        headers: {
                            "X-CSRFToken": getCsrfToken()
                        }
                    });
                    return;
                }

                // Fallback when HTMX is unavailable
                fetch(url, {
                    method: "POST",
                    credentials: "same-origin",
                    headers: {
                        "X-CSRFToken": getCsrfToken(),
                        "X-Requested-With": "XMLHttpRequest",
                        "HX-Request": "true"
                    }
                })
                .then(async response => {
                    if (!response.ok) throw new Error("Delete failed");
                    location.reload();
                })
                .catch(() => {
                    Swal.fire("Error", "Delete failed", "error");
                });
            });
        });
    });

    // HTMX event handlers
    document.body.addEventListener("htmx:beforeRequest", function (event) {
        const form = resolveRequestForm(event.detail?.elt);
        if (form && form.closest("#modal-body")) {
            ensureModalSubmitWiring(form);
        }
    });

    document.body.addEventListener("htmx:beforeSwap", function (event) {
        const target = event.detail?.target;
        if (!target || target.id !== "modal-body") return;

        const xhr = event.detail?.xhr;
        
        const triggers = parseHXTriggerHeader(xhr);
        const detail = extractRelatedSavedDetail(triggers);

        // For 204 responses with related:saved, prevent swap and let afterRequest handle it
        if (detail && xhr?.status === 204) {
            event.detail.shouldSwap = false;
            event.preventDefault();
        } else if (xhr?.status === 200) {
            // Allow the swap to show form validation errors
        }
    });

    document.body.addEventListener("htmx:afterSwap", function (event) {
        if (event.detail.target && event.detail.target.id === "modal-body") {
            console.log(`📝 Modal body loaded. Stack: ${modalStack.length}`);
            isModalFormLoading = false;  // Form is now loaded
            console.log(`   Set isModalFormLoading = false`);
            showModal();
            initializeDynamicUI(event.detail.target);
            
            // CRITICAL: Re-process HTMX attributes on new form elements
            if (typeof htmx !== 'undefined' && htmx.process) {
                console.log(`   🔧 Processing HTMX on modal body...`);
                htmx.process(event.detail.target);
                console.log(`   ✅ HTMX processed - form is now ready for submission`);
            }
            
            // If we just swapped in form HTML (200 response), clear submitting flag to allow retry
            const form = event.detail.target.querySelector("form");
            if (form && form.dataset.submitting === "1") {
                console.log(`   Form loaded after error - clearing submitting flag for retry`);
                delete form.dataset.submitting;
            }
        }

        const target = event.detail?.target;
        const hasMainContent = !!(target && (target.id === "main-content" || target.querySelector?.("#main-content")));
        if (hasMainContent) {
            const activeMain = document.getElementById("main-content");
            if (activeMain) {
                console.log(`🏠 Main content updated`);
                initializeDynamicUI(activeMain);

                // Re-process HTMX attributes inside newly swapped content.
                if (typeof htmx !== "undefined" && htmx.process) {
                    htmx.process(activeMain);
                }

                requestAnimationFrame(() => {
                    syncPageChromeFromMainContent(activeMain, event.detail?.xhr?.responseText || "");
                });
            }
        }
    });

    document.body.addEventListener("htmx:afterSettle", function (event) {
        const target = event.detail?.target;
        const hasMainContent = !!(target && (target.id === "main-content" || target.querySelector?.("#main-content")));
        if (hasMainContent) {
            syncPageChromeFromMainContent();
        }
    });

    document.body.addEventListener("htmx:historyRestore", function () {
        requestAnimationFrame(() => syncPageChromeFromMainContent());
    });

    document.body.addEventListener("htmx:afterRequest", async function (event) {
        const elt = event.detail?.elt;
        const xhr = event.detail?.xhr;
        const requestForm = resolveRequestForm(elt);
        const isModalRequest = !!(requestForm?.closest?.("#modal-body") || elt?.closest?.("#modal-body"));

        // Keep location in sync for non-modal forms after server redirects.
        if (requestForm && !requestForm.closest("#modal-body") && xhr?.responseURL) {
            try {
                const next = new URL(xhr.responseURL, window.location.origin);
                const nextUrl = `${next.pathname}${next.search}${next.hash}`;
                const currentUrl = `${window.location.pathname}${window.location.search}${window.location.hash}`;
                if (nextUrl !== currentUrl) {
                    window.history.replaceState({ htmx: true }, "", nextUrl);
                }
            } catch (e) {
                // ignore malformed responseURL
            }
        }

        // Always clear submitting flag for forms
        if (requestForm) {
            resetSubmittingState(requestForm);
        }

        // Process related:saved events for 204 responses OR if HX-Trigger header is present
        const triggers = parseHXTriggerHeader(xhr);
        const deletedDetail = extractDeletedDetail(triggers);

        if (deletedDetail) {
            Swal.fire({
                toast: true,
                position: "top-end",
                icon: "success",
                title: deletedDetail.message || "Deleted successfully.",
                showConfirmButton: false,
                timer: 1200,
                timerProgressBar: true,
            });

            if (deletedDetail.refreshList) {
                setTimeout(() => {
                    const main = document.getElementById("main-content");
                    if (main && typeof htmx !== "undefined") {
                        htmx.ajax("GET", window.location.href, {
                            target: "#main-content",
                            select: "#main-content",
                            swap: "outerHTML"
                        });
                    } else {
                        location.reload();
                    }
                }, 250);
            }
            return;
        }

        const detail = extractRelatedSavedDetail(triggers);
        
        if (xhr?.status === 204) {
            if (detail) {
                await new Promise(resolve => setTimeout(resolve, 100));
                await handleRelatedSaved(detail);
            } else if (isModalRequest) {
                await new Promise(resolve => setTimeout(resolve, 100));
                await handleRelatedSaved({
                    parentField: "",
                    option: null,
                    message: "Saved successfully!"
                });
            }
        } else if (detail && (xhr?.status === 200 || xhr?.status === 201)) {
            await new Promise(resolve => setTimeout(resolve, 100));
            await handleRelatedSaved(detail);
        }
    });

    ["htmx:responseError", "htmx:sendError", "htmx:timeout", "htmx:sendAbort"].forEach((eventName) => {
        document.body.addEventListener(eventName, function (event) {
            const form = resolveRequestForm(event.detail?.elt);
            if (form && form.closest("#modal-body")) {
                resetSubmittingState(form);
            }
        });
    });

    console.log(`\n✅ Modal System Script Loaded Successfully!\n`);

})();
