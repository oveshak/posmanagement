(function () {
function initProductFormPage() {
    const pageRoot = document.getElementById("main-content");
    if (!pageRoot || !pageRoot.querySelector("#variation-section")) {
        return;
    }

    if (pageRoot.dataset.productFormInitialized === "1") {
        return;
    }
    pageRoot.dataset.productFormInitialized = "1";

    const generateBtn = document.getElementById("generate-variations-by-attributes");
    const addAttributeSlotBtn = document.getElementById("add-attribute-slot");
    const totalForms = document.getElementById("id_variations-TOTAL_FORMS");
    const variationContainer = document.getElementById("variation-formset");
    const variationRowsBlock = document.getElementById("variation-rows-block");
    const variationRowsEmptyHint = document.getElementById("variation-rows-empty-hint");
    const template = document.getElementById("empty-variation-form-template");
    const attributeSlotContainer = document.getElementById("attribute-slot-container");
    const attributeSlotTemplate = document.getElementById("attribute-slot-template");

    const purchaseExcField = document.querySelector('[name="default_purchase_price_exc_tax"]');
    const vatRateField = document.querySelector('[name="vat_rate"]');
    const taxField = document.querySelector('[name="applicable_tax_percent"]');
    const productTaxTypeField = document.querySelector('[name="selling_price_tax_type"]');
    const marginField = document.querySelector('[name="margin_percent"]');
    const purchaseIncField = document.querySelector('[name="default_purchase_price_inc_tax"]');
    const sellingField = document.querySelector('[name="default_selling_price"]');
    const productTypeField = document.querySelector('[name="product_type"]');
    const manageStockField = document.querySelector('[name="manage_stock"]');
    const lowStockField = document.querySelector('[name="low_stock_alert_quantity"]');
    const lowStockWrapper = document.getElementById("low-stock-wrapper");
    const lowStockOriginalParent = lowStockWrapper ? lowStockWrapper.parentElement : null;
    const variationLowStockHost = document.getElementById("variation-low-stock-host");
    const defaultSellingPriceLabel = document.getElementById("default-selling-price-label");
    const enableImeiField = document.querySelector('[name="enable_imei_or_serial"]');
    const singleQtyField = document.querySelector('[name="single_stock_quantity"]');
    const singleImeiStorage = document.querySelector('[name="single_imei_numbers"]');
    const singleImeiInputs = document.getElementById("single-imei-inputs");
    const singleImeiSection = document.getElementById("single-stock-imei-section");
    const singleQuantityWrapper = document.getElementById("single-quantity-wrapper");
    const enableImeiWrapper = document.getElementById("enable-imei-wrapper");
    const pricingTaxStockSettings = document.getElementById("pricing-tax-stock-settings");
    const variationSection = document.getElementById("variation-section");

    function toNumber(value) {
        const parsed = parseFloat(value);
        return Number.isFinite(parsed) ? parsed : null;
    }

    function formatMoney(value) {
        return Number(value).toFixed(2);
    }

    function isVariationModeActive() {
        const productType = String(productTypeField ? productTypeField.value || "" : "single").toLowerCase();
        return productType === "variable" || productType === "variation" || productType === "combo";
    }

    function enforceSearchableSelect(select, placeholderText) {
        if (!select) {
            return;
        }

        select.dataset.forceSearch = "1";
        select.dataset.hideValuePrefix = "1";

        if (placeholderText) {
            select.dataset.placeholder = placeholderText;
        }

        if (!select.tomselect) {
            return;
        }

        select.tomselect.settings.hideSelected = false;
        select.tomselect.settings.closeAfterSelect = false;

        if (placeholderText) {
            select.tomselect.settings.placeholder = placeholderText;
            if (select.tomselect.control_input) {
                select.tomselect.control_input.setAttribute("placeholder", placeholderText);
            }
        }

        select.tomselect.refreshOptions(false);
    }

    function splitLines(value) {
        if (!value) {
            return [];
        }
        return String(value)
            .split(/\r?\n/)
            .map((line) => line.trim())
            .filter(Boolean);
    }

    function splitScannerTokens(value) {
        if (!value) {
            return [];
        }

        return String(value)
            .split(/[\r\n,]+/)
            .map((token) => token.trim())
            .filter(Boolean);
    }

    function debounce(callback, delay) {
        let timerId = null;
        const waitMs = Number.isFinite(delay) ? delay : 200;

        return function () {
            const args = Array.from(arguments);
            if (timerId) {
                window.clearTimeout(timerId);
            }

            timerId = window.setTimeout(function () {
                callback.apply(null, args);
            }, waitMs);
        };
    }

    function getCsrfToken() {
        const formToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (formToken && formToken.value) {
            return formToken.value;
        }

        const cookieValue = document.cookie
            .split(";")
            .map(function (item) { return item.trim(); })
            .find(function (item) { return item.startsWith("csrftoken="); });

        if (!cookieValue) {
            return "";
        }

        return decodeURIComponent(cookieValue.split("=")[1] || "");
    }

    function normalizeDistinctTokens(tokens) {
        const seen = new Set();
        const uniqueTokens = [];

        (tokens || []).forEach(function (token) {
            const cleaned = String(token || "").trim();
            if (!cleaned) {
                return;
            }

            const key = cleaned.toLowerCase();
            if (seen.has(key)) {
                return;
            }

            seen.add(key);
            uniqueTokens.push(cleaned);
        });

        return uniqueTokens;
    }

    function ensureUnickOption(unickField, id, text) {
        if (!unickField || !id) {
            return;
        }

        const optionId = String(id);
        const optionText = String(text || optionId);

        if (unickField.tomselect) {
            if (!unickField.tomselect.options[optionId]) {
                unickField.tomselect.addOption({ value: optionId, text: optionText });
            }
            return;
        }

        const existing = Array.from(unickField.options).find(function (item) {
            return String(item.value) === optionId;
        });

        if (existing) {
            existing.text = optionText;
            return;
        }

        unickField.add(new Option(optionText, optionId, false, false));
    }

    async function resolveUnickTokensFromServer(tokens, createMissing) {
        const csrfToken = getCsrfToken();
        const headers = {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        };

        if (csrfToken) {
            headers["X-CSRFToken"] = csrfToken;
        }

        const response = await fetch("/product/ajax/options/unick/resolve/", {
            method: "POST",
            credentials: "same-origin",
            headers: headers,
            body: JSON.stringify({
                tokens: tokens,
                create_missing: !!createMissing,
            }),
        });

        if (!response.ok) {
            throw new Error("Failed to resolve scanner keys.");
        }

        return response.json();
    }

    async function resolveScannerTokensToUnick(unickField, rawTokens, options) {
        const config = options || {};
        const mergeExisting = !!config.mergeExisting;
        const createMissing = config.createMissing !== false;

        const distinctTokens = normalizeDistinctTokens(rawTokens);
        if (!distinctTokens.length) {
            if (!mergeExisting) {
                setSelectedUnickValues(unickField, []);
            }
            return {
                matchedCount: 0,
                unmatchedTokens: [],
            };
        }

        let resolvedOptions = [];
        let unmatchedTokens = [];

        try {
            const payload = await resolveUnickTokensFromServer(distinctTokens, createMissing);
            resolvedOptions = (payload.results || []).map(function (item) {
                return {
                    id: String(item.id || "").trim(),
                    text: String(item.text || item.id || "").trim(),
                };
            }).filter(function (item) { return item.id; });

            unmatchedTokens = (payload.unmatched || [])
                .map(function (item) { return String(item || "").trim(); })
                .filter(Boolean);
        } catch (error) {
            const localOptions = getUnickOptions(unickField);
            const fallbackResolved = [];
            const fallbackUnmatched = [];

            distinctTokens.forEach(function (token) {
                const resolvedValue = findUnickOptionValue(unickField, token);
                if (!resolvedValue) {
                    fallbackUnmatched.push(token);
                    return;
                }

                const matchedOption = localOptions.find(function (item) {
                    return String(item.value) === String(resolvedValue);
                });

                fallbackResolved.push({
                    id: String(resolvedValue),
                    text: matchedOption ? String(matchedOption.text || resolvedValue) : String(resolvedValue),
                });
            });

            resolvedOptions = fallbackResolved;
            unmatchedTokens = fallbackUnmatched;
        }

        resolvedOptions.forEach(function (item) {
            ensureUnickOption(unickField, item.id, item.text);
        });

        const resolvedIds = resolvedOptions.map(function (item) { return String(item.id); });
        const finalSelection = mergeExisting
            ? getSelectedUnickValues(unickField).concat(resolvedIds)
            : resolvedIds;

        setSelectedUnickValues(unickField, finalSelection);

        return {
            matchedCount: resolvedIds.length,
            unmatchedTokens: unmatchedTokens,
        };
    }

    function getUnickOptions(unickField) {
        if (!unickField) {
            return [];
        }

        if (unickField.tomselect) {
            return Object.values(unickField.tomselect.options || {}).map(function (option) {
                return {
                    value: String(option.value || "").trim(),
                    text: String(option.text || "").trim(),
                };
            });
        }

        return Array.from(unickField.options).map(function (option) {
            return {
                value: String(option.value || "").trim(),
                text: String(option.text || "").trim(),
            };
        });
    }

    function findUnickOptionValue(unickField, token) {
        const normalized = String(token || "").trim().toLowerCase();
        if (!normalized) {
            return "";
        }

        const options = getUnickOptions(unickField);
        const exactMatch = options.find(function (item) {
            return item.text.toLowerCase() === normalized || item.value.toLowerCase() === normalized;
        });
        if (exactMatch) {
            return exactMatch.value;
        }

        const startsWithMatch = options.find(function (item) {
            return item.text.toLowerCase().startsWith(normalized);
        });
        if (startsWithMatch) {
            return startsWithMatch.value;
        }

        const containsMatch = options.find(function (item) {
            return item.text.toLowerCase().includes(normalized);
        });
        return containsMatch ? containsMatch.value : "";
    }

    function getSelectedUnickValues(unickField) {
        if (!unickField) {
            return [];
        }

        if (unickField.tomselect) {
            const current = unickField.tomselect.getValue();
            if (Array.isArray(current)) {
                return current.map(function (value) { return String(value); });
            }
            return current ? [String(current)] : [];
        }

        return Array.from(unickField.selectedOptions).map(function (option) { return String(option.value); });
    }

    function setSelectedUnickValues(unickField, values) {
        const uniqueValues = Array.from(new Set((values || []).map(function (value) {
            return String(value);
        }).filter(Boolean)));

        if (unickField.tomselect) {
            unickField.tomselect.setValue(uniqueValues, true);
            return;
        }

        Array.from(unickField.options).forEach(function (option) {
            option.selected = uniqueValues.includes(String(option.value));
        });
    }

    function scannerFocusNext(event) {
        if (event.key !== "Enter") {
            return;
        }

        event.preventDefault();
        const inputs = Array.from(event.currentTarget.closest(".scanner-input-grid").querySelectorAll(".scanner-input"));
        const index = inputs.indexOf(event.currentTarget);
        if (index >= 0 && inputs[index + 1]) {
            inputs[index + 1].focus();
            inputs[index + 1].select();
        }
    }

    function buildScannerInputs(target, count, existingValues, onUpdate) {
        target.innerHTML = "";
        target.classList.add("scanner-input-grid");

        for (let i = 0; i < count; i += 1) {
            const input = document.createElement("input");
            input.type = "text";
            input.className = "scanner-input";
            input.placeholder = `Scan IMEI ${i + 1}`;
            input.value = existingValues[i] || "";
            input.addEventListener("keydown", scannerFocusNext);
            input.addEventListener("input", onUpdate);
            target.appendChild(input);
        }
    }

    function recalculateProductPrices() {
        if (!purchaseExcField) {
            return;
        }

        const purchaseExc = toNumber(purchaseExcField.value);
        const taxPercent = toNumber(taxField ? taxField.value : 0) || 0;
        const marginPercent = toNumber(marginField ? marginField.value : 0) || 0;
        const taxType = (productTaxTypeField ? productTaxTypeField.value : "exclusive") || "exclusive";

        if (purchaseExc === null) {
            if (purchaseIncField) {
                purchaseIncField.value = "";
            }
            if (sellingField) {
                sellingField.value = "";
            }
            return;
        }

        if (purchaseIncField) {
            purchaseIncField.value = formatMoney(purchaseExc * (1 + (taxPercent / 100)));
        }

        const sellingExc = purchaseExc * (1 + (marginPercent / 100));
        const sellingInc = sellingExc * (1 + (taxPercent / 100));

        if (sellingField) {
            sellingField.value = formatMoney(taxType === "inclusive" ? sellingInc : sellingExc);
        }

        if (defaultSellingPriceLabel) {
            defaultSellingPriceLabel.textContent = taxType === "inclusive"
                ? "Default Selling Price (Inc. Tax)"
                : "Default Selling Price (Exc. Tax)";
        }
    }

    function syncMainSectionVisibility() {
        const isVariationMode = isVariationModeActive();

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

        syncManageStockFields();
        syncVariationRowsVisibility();
    }

    function syncVariationRowsVisibility() {
        const rowCount = variationContainer
            ? Array.from(variationContainer.querySelectorAll(".variation-card")).filter(function (row) {
                return !isRowMarkedForDelete(row);
            }).length
            : 0;
        const isVariationMode = isVariationModeActive();

        if (variationRowsBlock) {
            variationRowsBlock.classList.toggle("hidden-section", !(isVariationMode && rowCount > 0));
        }

        if (variationRowsEmptyHint) {
            variationRowsEmptyHint.classList.toggle("hidden-section", !(isVariationMode && rowCount === 0));
        }
    }

    function syncLowStockPlacement() {
        if (!lowStockWrapper || !variationLowStockHost) {
            return;
        }

        const isVariationMode = isVariationModeActive();

        if (isVariationMode) {
            if (lowStockWrapper.parentElement !== variationLowStockHost) {
                variationLowStockHost.appendChild(lowStockWrapper);
            }
            variationLowStockHost.classList.toggle("hidden-section", !(manageStockField && manageStockField.checked));
            return;
        }

        if (lowStockOriginalParent && lowStockWrapper.parentElement !== lowStockOriginalParent) {
            lowStockOriginalParent.appendChild(lowStockWrapper);
        }

        variationLowStockHost.classList.add("hidden-section");
    }

    function syncManageStockFields() {
        if (!manageStockField || !lowStockField) {
            return;
        }

        const enabled = !!manageStockField.checked;

        if (lowStockWrapper) {
            lowStockWrapper.style.display = enabled ? "" : "none";
        }

        lowStockField.required = enabled;

        if (!enabled) {
            lowStockField.value = "";
        }

        syncLowStockPlacement();
    }

    function renderSingleImeiInputs() {
        if (!singleImeiStorage || !singleImeiInputs) {
            return;
        }

        const shouldShow = productTypeField && productTypeField.value === "single" && enableImeiField && enableImeiField.checked;
        if (singleImeiSection) {
            singleImeiSection.style.display = shouldShow ? "" : "none";
        }
        if (!shouldShow) {
            singleImeiInputs.innerHTML = "";
            singleImeiStorage.value = "";
            return;
        }

        const count = Math.max(0, parseInt(singleQtyField ? singleQtyField.value || "0" : "0", 10) || 0);
        const existing = splitLines(singleImeiStorage.value);

        const syncStorage = function () {
            const values = Array.from(singleImeiInputs.querySelectorAll(".scanner-input"))
                .map((item) => item.value.trim())
                .filter(Boolean);
            singleImeiStorage.value = values.join("\n");
        };

        buildScannerInputs(singleImeiInputs, count, existing, syncStorage);
        syncStorage();
    }

    function fetchVatRateDetails(vatId) {
        if (!vatId) {
            return Promise.resolve({ rate_percent: "0", tax_type: "exclusive" });
        }

        return fetch(`/product/ajax/options/vat-rate/?vat_id=${encodeURIComponent(vatId)}`)
            .then(function (response) { return response.json(); })
            .catch(function () {
                return { rate_percent: "0", tax_type: "exclusive" };
            });
    }

    function applyVatRateToProduct() {
        if (!vatRateField) {
            return;
        }

        fetchVatRateDetails(vatRateField.value).then(function (data) {
            if (taxField) {
                taxField.value = data.rate_percent || "0";
            }
            if (productTaxTypeField && data.tax_type) {
                productTaxTypeField.value = data.tax_type;
            }
            recalculateProductPrices();
        });
    }

    function recalculateVariationRow(row) {
        const purchaseExc = row.querySelector('[name$="-purchase_price_exc_tax"]');
        const purchaseInc = row.querySelector('[name$="-purchase_price_inc_tax"]');
        const tax = row.querySelector('[name$="-applicable_tax_percent"]');
        const taxTypeField = row.querySelector('[name$="-selling_price_tax_type"]');
        const margin = row.querySelector('[name$="-margin_percent"]');
        const sellingExc = row.querySelector('[name$="-price"]');
        const sellingInc = row.querySelector('[name$="-selling_price_inc_tax"]');

        const purchaseExcValue = toNumber(purchaseExc ? purchaseExc.value : null);
        const taxValue = toNumber(tax ? tax.value : 0) || 0;
        const taxType = (taxTypeField ? taxTypeField.value : "exclusive") || "exclusive";
        const marginValue = toNumber(margin ? margin.value : 0) || 0;
        const multiplier = 1 + (taxValue / 100);

        if (purchaseExcValue === null) {
            if (purchaseInc) {
                purchaseInc.value = "";
            }
            return;
        }

        if (purchaseInc) {
            purchaseInc.value = formatMoney(purchaseExcValue * multiplier);
        }

        const sellingExcValue = purchaseExcValue * (1 + (marginValue / 100));
        const sellingIncValue = sellingExcValue * multiplier;

        if (taxType === "inclusive") {
            if (sellingInc) {
                sellingInc.value = formatMoney(sellingIncValue);
            }
            if (sellingExc) {
                sellingExc.value = formatMoney(multiplier > 0 ? (sellingIncValue / multiplier) : sellingIncValue);
            }
            return;
        }

        if (sellingExc) {
            sellingExc.value = formatMoney(sellingExcValue);
        }
        if (sellingInc) {
            sellingInc.value = formatMoney(sellingIncValue);
        }
    }

    function buildVariationComboKey(combo) {
        return combo
            .map(function (item) { return String(item.valueId); })
            .filter(Boolean)
            .sort()
            .join("|");
    }

    function getVariationRowPrefix(row) {
        if (!row || !row.querySelector) {
            return "";
        }

        const anyNamedField = row.querySelector("[name^='variations-']");
        if (!anyNamedField || !anyNamedField.name) {
            return "";
        }

        const match = String(anyNamedField.name).match(/^(variations-\d+)-/);
        return match ? match[1] : "";
    }

    function ensureRowDeleteInput(row) {
        const prefix = getVariationRowPrefix(row);
        if (!prefix) {
            return null;
        }

        const deleteName = `${prefix}-DELETE`;
        let deleteInput = row.querySelector(`[name='${deleteName}']`);
        if (!deleteInput) {
            deleteInput = document.createElement("input");
            deleteInput.type = "hidden";
            deleteInput.name = deleteName;
            deleteInput.value = "";
            row.appendChild(deleteInput);
        }

        return deleteInput;
    }

    function isRowMarkedForDelete(row) {
        const prefix = getVariationRowPrefix(row);
        if (!prefix) {
            return false;
        }

        const deleteInput = row.querySelector(`[name='${prefix}-DELETE']`);
        if (!deleteInput) {
            return false;
        }

        if (deleteInput.type === "checkbox") {
            return !!deleteInput.checked;
        }

        const value = String(deleteInput.value || "").trim().toLowerCase();
        return value === "on" || value === "1" || value === "true";
    }

    function setRowDeleteState(row, shouldDelete) {
        const deleteInput = ensureRowDeleteInput(row);
        if (deleteInput) {
            if (deleteInput.type === "checkbox") {
                deleteInput.checked = !!shouldDelete;
            } else {
                deleteInput.value = shouldDelete ? "on" : "";
            }
        }

        row.classList.toggle("hidden-section", !!shouldDelete);
    }

    function getVariationRowComboKey(row) {
        const attributeValues = row.querySelector('[name$="-attribute_values"]');
        if (!attributeValues) {
            return "";
        }

        let values = [];
        if (attributeValues.tomselect) {
            values = attributeValues.tomselect.getValue();
        } else {
            values = Array.from(attributeValues.selectedOptions).map(function (opt) { return String(opt.value); });
        }

        if (!Array.isArray(values)) {
            values = values ? [String(values)] : [];
        }

        return values
            .map(function (value) { return String(value); })
            .filter(Boolean)
            .sort()
            .join("|");
    }

    function collectExistingVariationComboKeys() {
        const keys = new Set();
        Array.from(variationContainer ? variationContainer.children : []).forEach(function (row) {
            const key = getVariationRowComboKey(row);

            if (key) {
                keys.add(key);
            }
        });

        return keys;
    }

    function applyVatRateToVariationRow(row) {
        const vatField = row.querySelector('[name$="-vat_rate"]');
        const taxField = row.querySelector('[name$="-applicable_tax_percent"]');
        const taxTypeField = row.querySelector('[name$="-selling_price_tax_type"]');
        if (!vatField) {
            return;
        }

        fetchVatRateDetails(vatField.value).then(function (data) {
            if (taxField) {
                taxField.value = data.rate_percent || "0";
            }
            if (taxTypeField && data.tax_type) {
                taxTypeField.value = data.tax_type;
            }
            recalculateVariationRow(row);
        });
    }

    function bindVariationImeiPanel(row) {
        const quantityField = row.querySelector('[name$="-quantity"]');
        const enableField = row.querySelector('[name$="-isunck"]');
        const storageField = row.querySelector('[name$="-imei_numbers"]');
        const panel = row.querySelector('.variation-imei-panel');
        const inputContainer = row.querySelector('.variation-imei-inputs');
        const unickPanel = row.querySelector('.variation-unick-panel');
        const unickField = row.querySelector('[name$="-unickkey"]');
        const unickScannerInput = row.querySelector('.variation-unick-scanner');
        const unickScannerFeedback = row.querySelector('.variation-unick-feedback');

        if (!quantityField || !enableField || !storageField || !panel || !inputContainer) {
            return;
        }

        const updatePanel = function () {
            const qty = Math.max(0, parseInt(quantityField.value || "0", 10) || 0);
            const enabled = !!enableField.checked;

            const showUnickFeedback = function (message, isError) {
                if (!unickScannerFeedback) {
                    return;
                }

                unickScannerFeedback.textContent = message || "";
                unickScannerFeedback.classList.toggle("hidden-section", !message);
                unickScannerFeedback.classList.toggle("text-red-600", !!isError);
                unickScannerFeedback.classList.toggle("dark:text-red-400", !!isError);
                unickScannerFeedback.classList.toggle("text-gray-500", !isError);
                unickScannerFeedback.classList.toggle("dark:text-slate-400", !isError);
            };

            if (unickPanel) {
                unickPanel.classList.toggle("hidden-section", !enabled);
            }

            if (!enabled) {
                panel.classList.add("hidden-section");
                inputContainer.innerHTML = "";
                storageField.value = "";

                if (unickField) {
                    if (unickField.tomselect) {
                        unickField.tomselect.clear(true);
                    } else {
                        Array.from(unickField.options).forEach(function (opt) { opt.selected = false; });
                    }
                }

                if (unickScannerInput) {
                    unickScannerInput.value = "";
                }

                if (unickScannerFeedback) {
                    showUnickFeedback("", false);
                }
                return;
            }

            if (qty === 0) {
                panel.classList.add("hidden-section");
                inputContainer.innerHTML = "";
                storageField.value = "";
                return;
            }

            panel.classList.remove("hidden-section");
            const existing = splitLines(storageField.value);

            const syncUnickFromImei = debounce(function (scannedTokens) {
                if (!unickField) {
                    return;
                }

                resolveScannerTokensToUnick(unickField, scannedTokens, {
                    mergeExisting: false,
                    createMissing: true,
                }).then(function (result) {
                    if (!scannedTokens.length) {
                        showUnickFeedback("", false);
                        return;
                    }

                    if (result.unmatchedTokens.length) {
                        showUnickFeedback(
                            `IMEI scanner matched ${result.matchedCount} key(s). ${result.unmatchedTokens.length} key(s) could not be resolved.`,
                            true
                        );
                        return;
                    }

                    showUnickFeedback(`IMEI scanner synced ${result.matchedCount} unique key(s).`, false);
                }).catch(function () {
                    showUnickFeedback("Scanner sync failed. Try scanning again.", true);
                });
            }, 200);

            const syncStorage = function () {
                const values = Array.from(inputContainer.querySelectorAll(".scanner-input"))
                    .map((item) => item.value.trim())
                    .filter(Boolean);
                storageField.value = values.join("\n");
                syncUnickFromImei(values);
            };

            buildScannerInputs(inputContainer, qty, existing, syncStorage);
            syncStorage();
        };

        quantityField.addEventListener("input", updatePanel);
        quantityField.addEventListener("change", updatePanel);
        enableField.addEventListener("change", updatePanel);
        updatePanel();
    }

    function bindVariationUnickScanner(row) {
        const unickField = row.querySelector('[name$="-unickkey"]');
        const scannerInput = row.querySelector('.variation-unick-scanner');
        const applyButton = row.querySelector('.variation-unick-apply-btn');
        const feedback = row.querySelector('.variation-unick-feedback');

        if (!unickField || !scannerInput || !applyButton) {
            return;
        }

        const showFeedback = function (message, isError) {
            if (!feedback) {
                return;
            }

            feedback.textContent = message || "";
            feedback.classList.toggle("hidden-section", !message);
            feedback.classList.toggle("text-red-600", !!isError);
            feedback.classList.toggle("dark:text-red-400", !!isError);
            feedback.classList.toggle("text-gray-500", !isError);
            feedback.classList.toggle("dark:text-slate-400", !isError);
        };

        const applyScannerValues = function () {
            const tokens = splitScannerTokens(scannerInput.value);
            if (!tokens.length) {
                showFeedback("Scan or paste at least one unique key first.", true);
                return;
            }

            resolveScannerTokensToUnick(unickField, tokens, {
                mergeExisting: true,
                createMissing: true,
            }).then(function (result) {
                scannerInput.value = "";

                if (result.unmatchedTokens.length) {
                    showFeedback(
                        `Matched ${result.matchedCount} key(s). ${result.unmatchedTokens.length} key(s) could not be resolved.`,
                        true
                    );
                    return;
                }

                showFeedback(`Matched ${result.matchedCount} key(s) from scanner input.`, false);
            }).catch(function () {
                showFeedback("Scanner sync failed. Try again.", true);
            });
        };

        if (applyButton.dataset.boundClick !== "1") {
            applyButton.dataset.boundClick = "1";
            applyButton.addEventListener("click", applyScannerValues);
        }

        if (scannerInput.dataset.boundKeydown !== "1") {
            scannerInput.dataset.boundKeydown = "1";
            scannerInput.addEventListener("keydown", function (event) {
                if (event.key === "Enter") {
                    event.preventDefault();
                    applyScannerValues();
                }
            });
        }
    }

    function bindVariationRow(row) {
        const unickField = row.querySelector('[name$="-unickkey"]');
        enforceSearchableSelect(unickField, "Search unique keys");

        ['[name$="-purchase_price_exc_tax"]', '[name$="-applicable_tax_percent"]', '[name$="-margin_percent"]', '[name$="-price"]', '[name$="-selling_price_inc_tax"]', '[name$="-selling_price_tax_type"]'].forEach(function (selector) {
            const field = row.querySelector(selector);
            if (field) {
                field.addEventListener("input", function () { recalculateVariationRow(row); });
                field.addEventListener("change", function () { recalculateVariationRow(row); });
            }
        });

        const vatField = row.querySelector('[name$="-vat_rate"]');
        if (vatField) {
            vatField.addEventListener("change", function () {
                applyVatRateToVariationRow(row);
            });
        }

        bindVariationImeiPanel(row);
        bindVariationUnickScanner(row);
        if (vatField && vatField.value) {
            applyVatRateToVariationRow(row);
        } else {
            recalculateVariationRow(row);
        }
    }

    function loadAttributeValues(attributeSelect) {
        const slot = attributeSelect.closest(".attribute-slot");
        const valuesSelect = slot ? slot.querySelector(".variation-value-select") : null;
        if (!valuesSelect) {
            return;
        }

        const attributeId = attributeSelect.value;

        if (valuesSelect.tomselect) {
            valuesSelect.tomselect.clear();
            valuesSelect.tomselect.clearOptions();
        } else {
            valuesSelect.innerHTML = "";
        }

        renderAttributeSlotSummary(slot);

        if (!attributeId) {
            if (valuesSelect.tomselect) {
                valuesSelect.tomselect.refreshOptions(false);
            }
            return;
        }

        fetch(`/product/ajax/options/attribute-values/?attribute_id=${encodeURIComponent(attributeId)}`)
            .then(function (response) { return response.json(); })
            .then(function (data) {
                (data.results || []).forEach(function (item) {
                    const option = document.createElement("option");
                    option.value = String(item.id);
                    option.textContent = item.text;
                    option.dataset.valueCode = item.code || "";
                    valuesSelect.appendChild(option);
                });

                if (valuesSelect.tomselect) {
                    valuesSelect.tomselect.sync();
                    valuesSelect.tomselect.refreshOptions(false);
                }

                renderAttributeSlotSummary(slot);
            })
            .catch(function () {
                renderAttributeSlotSummary(slot);
                // keep silent
            });
    }

    function renderAttributeSlotSummary(slot) {
        if (!slot) {
            return;
        }

        const attrSelect = slot.querySelector(".variation-attr-select");
        const valuesSelect = slot.querySelector(".variation-value-select");
        if (!attrSelect || !valuesSelect) {
            return;
        }

        let summary = slot.querySelector(".attribute-slot-summary");
        if (!summary) {
            summary = document.createElement("p");
            summary.className = "md:col-span-12 attribute-slot-summary hidden-section";
            slot.appendChild(summary);
        }

        const selectedAttrText = attrSelect.options[attrSelect.selectedIndex]
            ? String(attrSelect.options[attrSelect.selectedIndex].text || "").trim()
            : "";

        let selectedValueIds = [];
        if (valuesSelect.tomselect) {
            const current = valuesSelect.tomselect.getValue();
            if (Array.isArray(current)) {
                selectedValueIds = current.map(function (value) { return String(value); });
            } else if (current) {
                selectedValueIds = [String(current)];
            }
        } else {
            selectedValueIds = Array.from(valuesSelect.selectedOptions).map(function (opt) {
                return String(opt.value);
            });
        }

        const selectedValueTexts = selectedValueIds
            .map(function (id) {
                const option = Array.from(valuesSelect.options).find(function (opt) {
                    return String(opt.value) === String(id);
                });
                return option ? String(option.text || "").trim() : "";
            })
            .filter(Boolean);

        if (!selectedAttrText) {
            summary.textContent = "";
            summary.classList.add("hidden-section");
            return;
        }

        if (!selectedValueTexts.length) {
            summary.textContent = `Selected Attribute: ${selectedAttrText} (choose values)`;
            summary.classList.remove("hidden-section");
            return;
        }

        summary.textContent = `Selected: ${selectedAttrText} -> ${selectedValueTexts.join(", ")}`;
        summary.classList.remove("hidden-section");
    }

    function getNextAttributeSlotIndex() {
        const slots = Array.from(attributeSlotContainer ? attributeSlotContainer.querySelectorAll(".attribute-slot") : []);
        if (!slots.length) {
            return 1;
        }

        const maxSlot = slots.reduce(function (maxValue, slot) {
            const current = parseInt(slot.getAttribute("data-slot") || "0", 10) || 0;
            return Math.max(maxValue, current);
        }, 0);

        return maxSlot + 1;
    }

    function bindAttributeSlot(slot) {
        if (!slot) {
            return;
        }

        const attrSelect = slot.querySelector(".variation-attr-select");
        const valuesSelect = slot.querySelector(".variation-value-select");

        enforceSearchableSelect(attrSelect, "Search attribute");
        enforceSearchableSelect(valuesSelect, "Search values");

        if (attrSelect && attrSelect.dataset.boundChange !== "1") {
            attrSelect.dataset.boundChange = "1";
            attrSelect.addEventListener("change", function () {
                loadAttributeValues(attrSelect);
                renderAttributeSlotSummary(slot);
            });
        }

        if (valuesSelect && valuesSelect.dataset.boundChange !== "1") {
            valuesSelect.dataset.boundChange = "1";
            valuesSelect.addEventListener("change", function () {
                renderAttributeSlotSummary(slot);
            });
        }

        renderAttributeSlotSummary(slot);
    }

    function addAttributeSlot() {
        if (!attributeSlotTemplate || !attributeSlotContainer) {
            return;
        }

        const nextIndex = getNextAttributeSlotIndex();
        const html = attributeSlotTemplate.innerHTML.replace(/__slot__/g, String(nextIndex));
        attributeSlotContainer.insertAdjacentHTML("beforeend", html);

        const slot = attributeSlotContainer.lastElementChild;
        if (!slot) {
            return;
        }

        const attrSelect = slot.querySelector(".variation-attr-select");
        const valuesSelect = slot.querySelector(".variation-value-select");
        enforceSearchableSelect(attrSelect, "Search attribute");
        enforceSearchableSelect(valuesSelect, "Search values");

        if (typeof initializeDynamicUI === "function") {
            initializeDynamicUI(slot);
        }

        bindAttributeSlot(slot);
    }

    function getSelectedValueObjects(slot) {
        const attrSelect = slot.querySelector(".variation-attr-select");
        const valuesSelect = slot.querySelector(".variation-value-select");
        if (!attrSelect || !valuesSelect || !attrSelect.value) {
            return null;
        }

        const attrLabel = attrSelect.options[attrSelect.selectedIndex] ? attrSelect.options[attrSelect.selectedIndex].text : "";
        const selected = Array.from(valuesSelect.selectedOptions).map(function (opt) {
            return {
                attributeId: attrSelect.value,
                attributeLabel: attrLabel,
                valueId: opt.value,
                valueLabel: opt.text,
                valueCode: opt.dataset.valueCode || "",
            };
        });

        if (!selected.length) {
            return null;
        }

        return selected;
    }

    function cartesianProduct(arrays) {
        return arrays.reduce(function (acc, curr) {
            const result = [];
            acc.forEach(function (a) {
                curr.forEach(function (b) {
                    result.push(a.concat([b]));
                });
            });
            return result;
        }, [[]]);
    }

    function buildSkuFromCombo(combo) {
        return combo
            .map(function (item) {
                const source = (item.valueCode || item.valueLabel || "")
                    .toUpperCase()
                    .replace(/[^A-Z0-9]+/g, "-")
                    .replace(/^-+|-+$/g, "");
                return source || "VAL";
            })
            .join("-");
    }

    function addVariationRow() {
        if (!totalForms || !variationContainer || !template) {
            return null;
        }

        const formIndex = parseInt(totalForms.value, 10);
        const html = template.innerHTML.replace(/__prefix__/g, formIndex);
        variationContainer.insertAdjacentHTML("beforeend", html);
        totalForms.value = String(formIndex + 1);

        const row = variationContainer.lastElementChild;
        if (typeof initializeDynamicUI === "function") {
            initializeDynamicUI(row);
        }
        bindVariationRow(row);
        syncVariationRowsVisibility();
        return row;
    }

    function setVariationRowCombination(row, combo) {
        const nameField = row.querySelector('[name$="-name"]');
        const skuField = row.querySelector('[name$="-sku_suffix"]');
        const priceField = row.querySelector('[name$="-price"]');
        const dealerPriceField = row.querySelector('[name$="-dealer_price"]');
        const purchaseExc = row.querySelector('[name$="-purchase_price_exc_tax"]');
        const vatRate = row.querySelector('[name$="-vat_rate"]');
        const tax = row.querySelector('[name$="-applicable_tax_percent"]');
        const taxType = row.querySelector('[name$="-selling_price_tax_type"]');
        const margin = row.querySelector('[name$="-margin_percent"]');
        const quantity = row.querySelector('[name$="-quantity"]');
        const attributeValues = row.querySelector('[name$="-attribute_values"]');

        if (nameField) {
            nameField.value = combo.map(function (item) { return `${item.attributeLabel}: ${item.valueLabel}`; }).join(" / ");
        }

        if (skuField) {
            skuField.value = buildSkuFromCombo(combo);
        }

        if (purchaseExc && purchaseExcField && purchaseExcField.value) {
            purchaseExc.value = purchaseExcField.value;
        }

        if (tax && taxField && taxField.value) {
            tax.value = taxField.value;
        }

        if (taxType && productTaxTypeField && productTaxTypeField.value) {
            taxType.value = productTaxTypeField.value;
        }

        if (vatRate && vatRateField && vatRateField.value) {
            if (vatRate.tomselect) {
                vatRate.tomselect.setValue(vatRateField.value, true);
            } else {
                vatRate.value = vatRateField.value;
            }
        }

        if (margin && marginField && marginField.value) {
            margin.value = marginField.value;
        }

        const fallbackSellingPrice = (sellingField && String(sellingField.value || "").trim() !== "")
            ? String(sellingField.value).trim()
            : "0.00";

        if (priceField) {
            const hasPrice = String(priceField.value || "").trim() !== "";
            if (!hasPrice) {
                priceField.value = fallbackSellingPrice;
            }
        }

        if (dealerPriceField) {
            const hasDealerPrice = String(dealerPriceField.value || "").trim() !== "";
            if (!hasDealerPrice) {
                dealerPriceField.value = String(priceField && priceField.value ? priceField.value : fallbackSellingPrice);
            }
        }

        if (quantity) {
            const hasQuantity = String(quantity.value || "").trim() !== "";
            if (!hasQuantity) {
                quantity.value = "0";
            }
        }

        if (attributeValues) {
            const ids = combo.map(function (item) { return String(item.valueId); });
            if (attributeValues.tomselect) {
                const existing = new Set(Object.keys(attributeValues.tomselect.options));
                combo.forEach(function (item) {
                    const id = String(item.valueId);
                    if (!existing.has(id)) {
                        attributeValues.tomselect.addOption({ value: id, text: item.valueLabel });
                    }
                });
                attributeValues.tomselect.setValue(ids, true);
            } else {
                combo.forEach(function (item) {
                    const id = String(item.valueId);
                    let option = Array.from(attributeValues.options).find(function (opt) { return String(opt.value) === id; });
                    if (!option) {
                        option = new Option(item.valueLabel, id, false, true);
                        attributeValues.add(option);
                    }
                    option.selected = true;
                });
            }
        }

        if (vatRate && vatRate.value) {
            applyVatRateToVariationRow(row);
        } else {
            recalculateVariationRow(row);
        }
    }

    function generateVariationsFromAttributes() {
        const slots = Array.from((attributeSlotContainer || document).querySelectorAll(".attribute-slot"));
        const selectedGroups = [];
        const selectedAttributeIds = new Set();

        slots.forEach(function (slot) {
            const group = getSelectedValueObjects(slot);
            if (!group || !group.length) {
                return;
            }

            const attributeId = String(group[0].attributeId || "");
            if (!attributeId || selectedAttributeIds.has(attributeId)) {
                return;
            }

            selectedAttributeIds.add(attributeId);
            selectedGroups.push(group);
        });

        if (!selectedGroups.length) {
            if (typeof Swal !== "undefined") {
                Swal.fire("Select attributes and values", "Choose at least one attribute with values first.", "warning");
            }
            return;
        }

        const combos = cartesianProduct(selectedGroups);
        if (!combos.length) {
            return;
        }

        if (combos.length > 200) {
            if (!window.confirm(`This will create ${combos.length} variation rows. Continue?`)) {
                return;
            }
        }

        const existingRows = Array.from(variationContainer ? variationContainer.querySelectorAll(".variation-card") : []);
        existingRows.forEach(function (row) {
            setRowDeleteState(row, false);
        });

        const exactRowByCombo = new Map();
        const recyclableRows = [];

        existingRows.forEach(function (row) {
            const comboKey = getVariationRowComboKey(row);
            if (comboKey && !exactRowByCombo.has(comboKey)) {
                exactRowByCombo.set(comboKey, row);
                return;
            }
            recyclableRows.push(row);
        });

        const usedRows = new Set();
        let createdCount = 0;
        let updatedCount = 0;
        let recycledCount = 0;
        let deletedCount = 0;

        combos.forEach(function (combo) {
            const comboKey = buildVariationComboKey(combo);

            let row = comboKey ? exactRowByCombo.get(comboKey) : null;
            if (row && usedRows.has(row)) {
                row = null;
            }

            if (!row) {
                while (recyclableRows.length && usedRows.has(recyclableRows[0])) {
                    recyclableRows.shift();
                }

                if (recyclableRows.length) {
                    row = recyclableRows.shift();
                    recycledCount += 1;
                }
            } else {
                updatedCount += 1;
            }

            if (!row) {
                row = addVariationRow();
                if (row) {
                    createdCount += 1;
                }
            }

            if (row) {
                usedRows.add(row);
                setRowDeleteState(row, false);
                setVariationRowCombination(row, combo);
            }
        });

        existingRows.forEach(function (row) {
            if (usedRows.has(row)) {
                return;
            }

            setRowDeleteState(row, true);
            deletedCount += 1;
        });

        if (typeof Swal !== "undefined") {
            Swal.fire(
                "Variation Generation Done",
                `Created ${createdCount}, Updated ${updatedCount}, Recycled ${recycledCount}, Removed ${deletedCount}.`,
                "success"
            );
        }

        syncVariationRowsVisibility();
    }

    if (generateBtn) {
        generateBtn.addEventListener("click", generateVariationsFromAttributes);
    }

    if (addAttributeSlotBtn) {
        addAttributeSlotBtn.addEventListener("click", addAttributeSlot);
    }

    if (attributeSlotContainer) {
        attributeSlotContainer.addEventListener("click", function (event) {
            const removeBtn = event.target.closest(".remove-attribute-slot");
            if (!removeBtn) {
                return;
            }

            const slots = Array.from(attributeSlotContainer.querySelectorAll(".attribute-slot"));
            if (slots.length <= 1) {
                return;
            }

            const slot = removeBtn.closest(".attribute-slot");
            if (slot) {
                slot.remove();
            }
        });

        if (typeof initializeDynamicUI === "function") {
            initializeDynamicUI(attributeSlotContainer);
        }

        Array.from(attributeSlotContainer.querySelectorAll(".attribute-slot")).forEach(bindAttributeSlot);
    }

    [purchaseExcField, taxField, marginField, productTaxTypeField].forEach(function (field) {
        if (field) {
            field.addEventListener("input", recalculateProductPrices);
            field.addEventListener("change", recalculateProductPrices);
        }
    });

    if (vatRateField) {
        vatRateField.addEventListener("change", applyVatRateToProduct);
    }

    [productTypeField, enableImeiField, singleQtyField].forEach(function (field) {
        if (field) {
            field.addEventListener("change", function () {
                syncMainSectionVisibility();
                renderSingleImeiInputs();
            });
            field.addEventListener("input", renderSingleImeiInputs);
        }
    });

    if (manageStockField) {
        manageStockField.addEventListener("change", syncManageStockFields);
    }

    Array.from(variationContainer ? variationContainer.children : []).forEach(bindVariationRow);

    if (vatRateField && vatRateField.value) {
        applyVatRateToProduct();
    } else {
        recalculateProductPrices();
    }
    syncMainSectionVisibility();
    syncVariationRowsVisibility();
    syncManageStockFields();
    renderSingleImeiInputs();
}

window.__initProductFormPage = initProductFormPage;

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initProductFormPage, { once: true });
} else {
    initProductFormPage();
}

if (!window.__productFormAfterSwapBound) {
    window.__productFormAfterSwapBound = true;
    document.body.addEventListener("htmx:afterSwap", function (event) {
        const target = event.detail?.target;
        const hasMainContent = !!(target && (target.id === "main-content" || target.querySelector?.("#main-content")));
        if (hasMainContent && typeof window.__initProductFormPage === "function") {
            window.__initProductFormPage();
        }
    });
}
})();
