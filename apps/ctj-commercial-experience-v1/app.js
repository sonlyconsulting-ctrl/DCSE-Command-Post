(() => {
  "use strict";

  const STORAGE_KEY = "ctj.commercial.order.v1";
  const catalog = window.CTJ_CATALOG;
  const productIndex = new Map(catalog.products.map((product) => [product.id, product]));

  const state = loadState();

  const els = {
    catalog: document.getElementById("catalog"),
    checkout: document.getElementById("checkout"),
    closeCheckout: document.getElementById("closeCheckout"),
    resumeButton: document.getElementById("resumeButton"),
    statusBanner: document.getElementById("statusBanner"),
    orderProduct: document.getElementById("orderProduct"),
    identityForm: document.getElementById("identityForm"),
    customerEmail: document.getElementById("customerEmail"),
    stepProduct: document.getElementById("stepProduct"),
    stepPayment: document.getElementById("stepPayment"),
    paymentChoices: document.getElementById("paymentChoices"),
    paymentInstructions: document.getElementById("paymentInstructions"),
    stepSubmission: document.getElementById("stepSubmission"),
    paymentForm: document.getElementById("paymentForm"),
    payerIdentity: document.getElementById("payerIdentity"),
    transactionReference: document.getElementById("transactionReference"),
    backToMethods: document.getElementById("backToMethods"),
    stepPending: document.getElementById("stepPending"),
    pendingSummary: document.getElementById("pendingSummary"),
    downloadSummary: document.getElementById("downloadSummary"),
    startOver: document.getElementById("startOver")
  };

  renderCatalog();
  renderResumeState();
  attachEvents();
  configureResizeReporting();

  function freshState() {
    return {
      version: 1,
      orderId: null,
      productId: null,
      customerEmail: "",
      paymentMethodId: null,
      payerIdentity: "",
      transactionReference: "",
      orderStatus: "EMPTY",
      createdAt: null,
      submittedAt: null
    };
  }

  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return freshState();
      const parsed = JSON.parse(raw);
      if (!parsed || parsed.version !== 1 || typeof parsed !== "object") return freshState();
      return { ...freshState(), ...parsed };
    } catch {
      return freshState();
    }
  }

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch {
      showStatus("Your browser could not save this order locally. Keep the order summary before leaving this page.", "error");
    }
  }

  function clearState() {
    Object.assign(state, freshState());
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch {
      // The in-memory reset still succeeds.
    }
  }

  function renderCatalog() {
    els.catalog.textContent = "";
    for (const product of catalog.products) {
      const card = document.createElement("article");
      card.className = "product-card" + (product.id === "intro-trio" || product.id === "complete" ? " featured" : "");
      card.setAttribute("data-product-id", product.id);

      if (product.badge) {
        const badge = document.createElement("span");
        badge.className = "badge";
        badge.textContent = product.badge;
        card.appendChild(badge);
      }

      appendText(card, "p", "eyebrow", product.role);
      appendText(card, "h3", "", product.title);

      if (product.subtitle) appendText(card, "p", "product-subtitle", product.subtitle);
      appendText(card, "p", "product-tagline", product.tagline);
      appendText(card, "p", "product-meta", product.effort);
      appendText(card, "p", "product-result", "Result: " + product.result);

      const priceRow = document.createElement("div");
      priceRow.className = "price-row";
      appendText(priceRow, "span", "price", formatMoney(product.price));
      if (product.compareAt) appendText(priceRow, "span", "compare-at", formatMoney(product.compareAt));
      card.appendChild(priceRow);

      const list = document.createElement("ul");
      list.className = "includes";
      for (const item of product.includes) appendText(list, "li", "", item);
      card.appendChild(list);

      const actions = document.createElement("div");
      actions.className = "actions";
      const buy = document.createElement("button");
      buy.type = "button";
      buy.className = "button button-primary";
      buy.textContent = "Buy once";
      buy.setAttribute("data-buy-product", product.id);
      buy.setAttribute("aria-label", "Buy " + product.title + " for " + formatMoney(product.price));
      actions.appendChild(buy);
      card.appendChild(actions);

      els.catalog.appendChild(card);
    }
  }

  function attachEvents() {
    els.catalog.addEventListener("click", (event) => {
      const target = event.target.closest("[data-buy-product]");
      if (!target) return;
      beginOrder(target.getAttribute("data-buy-product"));
    });

    els.identityForm.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!els.identityForm.reportValidity()) return;
      state.customerEmail = els.customerEmail.value.trim();
      state.orderStatus = "PAYMENT_PENDING";
      saveState();
      showPaymentStep();
    });

    els.paymentChoices.addEventListener("click", (event) => {
      const target = event.target.closest("[data-payment-method]");
      if (!target) return;
      selectPaymentMethod(target.getAttribute("data-payment-method"));
    });

    els.paymentForm.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!els.paymentForm.reportValidity()) return;
      if (!state.paymentMethodId) {
        showStatus("Choose a payment method before submitting payment details.", "error");
        return;
      }
      state.payerIdentity = els.payerIdentity.value.trim();
      state.transactionReference = els.transactionReference.value.trim();
      state.orderStatus = "PAYMENT_SUBMITTED";
      state.submittedAt = new Date().toISOString();
      saveState();
      showPendingStep();
    });

    els.backToMethods.addEventListener("click", () => {
      state.paymentMethodId = null;
      state.orderStatus = "PAYMENT_PENDING";
      saveState();
      els.stepSubmission.hidden = true;
      els.stepPayment.hidden = false;
      els.paymentInstructions.hidden = true;
      showStatus("Choose another payment method.", "info");
    });

    els.closeCheckout.addEventListener("click", () => {
      els.checkout.hidden = true;
      renderResumeState();
    });

    els.resumeButton.addEventListener("click", () => {
      resumeOrder();
    });

    els.downloadSummary.addEventListener("click", downloadOrderSummary);

    els.startOver.addEventListener("click", () => {
      clearState();
      resetCheckoutView();
      renderResumeState();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  function beginOrder(productId) {
    const product = productIndex.get(productId);
    if (!product) {
      showStatus("That product could not be loaded.", "error");
      return;
    }

    clearState();
    state.orderId = createOrderId();
    state.productId = productId;
    state.orderStatus = "ORDER_INTENT";
    state.createdAt = new Date().toISOString();
    saveState();

    resetCheckoutView();
    renderOrderProduct(product);
    els.customerEmail.value = "";
    els.checkout.hidden = false;
    showStatus("Order intent created. No payment has been recorded yet.", "info");
    els.checkout.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function resumeOrder() {
    const product = productIndex.get(state.productId);
    if (!product || !state.orderId) return;

    resetCheckoutView();
    renderOrderProduct(product);
    els.customerEmail.value = state.customerEmail || "";
    els.payerIdentity.value = state.payerIdentity || "";
    els.transactionReference.value = state.transactionReference || "";
    els.checkout.hidden = false;

    if (state.orderStatus === "PAYMENT_SUBMITTED") {
      showPendingStep();
    } else if (state.paymentMethodId) {
      showPaymentStep();
      selectPaymentMethod(state.paymentMethodId);
    } else if (state.customerEmail) {
      showPaymentStep();
    } else {
      showStatus("Resume your saved order intent.", "info");
    }

    els.checkout.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function resetCheckoutView() {
    els.stepProduct.hidden = false;
    els.stepPayment.hidden = true;
    els.stepSubmission.hidden = true;
    els.stepPending.hidden = true;
    els.paymentInstructions.hidden = true;
    els.statusBanner.textContent = "";
    delete els.statusBanner.dataset.kind;
  }

  function renderOrderProduct(product) {
    els.orderProduct.textContent = "";
    const wrap = document.createElement("div");
    wrap.className = "order-product";
    const text = document.createElement("div");
    appendText(text, "h4", "", product.title);
    appendText(text, "p", "", product.role);
    appendText(text, "p", "", "Order ID: " + state.orderId);
    wrap.appendChild(text);
    appendText(wrap, "strong", "price", formatMoney(product.price));
    els.orderProduct.appendChild(wrap);
  }

  function showPaymentStep() {
    const product = productIndex.get(state.productId);
    if (!product) return;

    els.stepProduct.hidden = true;
    els.stepPayment.hidden = false;
    els.stepSubmission.hidden = true;
    els.stepPending.hidden = true;
    els.paymentChoices.textContent = "";

    for (const method of catalog.paymentMethods) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "payment-choice";
      button.setAttribute("data-payment-method", method.id);
      appendText(button, "strong", "", method.label);
      appendText(button, "span", "", method.merchant);
      els.paymentChoices.appendChild(button);
    }

    showStatus("Amount due: " + formatMoney(product.price) + ". Payment is completed outside this page.", "info");
  }

  function selectPaymentMethod(methodId) {
    const product = productIndex.get(state.productId);
    const method = catalog.paymentMethods.find((item) => item.id === methodId);
    if (!product || !method) return;

    state.paymentMethodId = methodId;
    state.orderStatus = "PAYMENT_PENDING";
    saveState();

    els.paymentInstructions.textContent = "";
    appendText(els.paymentInstructions, "p", "eyebrow", method.label.toUpperCase());
    appendCopyLine(els.paymentInstructions, "Pay to", method.merchant);
    appendCopyLine(els.paymentInstructions, "Amount", formatMoney(product.price));
    appendCopyLine(els.paymentInstructions, "Order ID", state.orderId);
    appendText(els.paymentInstructions, "p", "field-help", "Use the order ID in the payment note when the provider permits it. No provider destination link is shown until it is verified.");
    els.paymentInstructions.hidden = false;
    els.stepSubmission.hidden = false;
    els.payerIdentity.focus();
    showStatus(method.label + " selected. Complete payment externally, then return with the transaction/reference ID.", "info");
  }

  function showPendingStep() {
    const product = productIndex.get(state.productId);
    const method = catalog.paymentMethods.find((item) => item.id === state.paymentMethodId);
    if (!product || !method) return;

    els.stepProduct.hidden = true;
    els.stepPayment.hidden = true;
    els.stepSubmission.hidden = true;
    els.stepPending.hidden = false;
    els.pendingSummary.textContent = "";

    addSummary("Order ID", state.orderId);
    addSummary("Product", product.title);
    addSummary("Amount", formatMoney(product.price));
    addSummary("Payment method", method.label);
    addSummary("Merchant", method.merchant);
    addSummary("Email", state.customerEmail);
    addSummary("Transaction/reference", state.transactionReference);
    addSummary("Status", "PAYMENT_SUBMITTED - merchant verification required");

    showStatus("Payment details submitted. This is not yet a verified paid order.", "success");
    renderResumeState();
  }

  function renderResumeState() {
    els.resumeButton.hidden = !state.orderId || state.orderStatus === "EMPTY";
  }

  function addSummary(term, description) {
    appendText(els.pendingSummary, "dt", "", term);
    appendText(els.pendingSummary, "dd", "", description || "");
  }

  function appendCopyLine(parent, label, value) {
    const line = document.createElement("div");
    line.className = "copy-line";
    const text = document.createElement("span");
    text.textContent = label + ": " + value;
    const copy = document.createElement("button");
    copy.type = "button";
    copy.className = "button button-quiet";
    copy.textContent = "Copy";
    copy.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(value);
        showStatus(label + " copied.", "success");
      } catch {
        showStatus("Copy was unavailable. Select and copy the value manually.", "error");
      }
    });
    line.append(text, copy);
    parent.appendChild(line);
  }

  function appendText(parent, tag, className, value) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    el.textContent = value;
    parent.appendChild(el);
    return el;
  }

  function showStatus(message, kind) {
    els.statusBanner.textContent = message;
    els.statusBanner.dataset.kind = kind || "info";
  }

  function formatMoney(amount) {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: catalog.currency,
      maximumFractionDigits: 0
    }).format(amount);
  }

  function createOrderId() {
    const random = globalThis.crypto && typeof globalThis.crypto.randomUUID === "function"
      ? globalThis.crypto.randomUUID().replace(/-/g, "").slice(0, 10).toUpperCase()
      : Math.random().toString(36).slice(2, 12).toUpperCase();
    return "CTJ-" + random;
  }

  function downloadOrderSummary() {
    const product = productIndex.get(state.productId);
    const method = catalog.paymentMethods.find((item) => item.id === state.paymentMethodId);
    if (!product || !method) return;

    const text = [
      "SONLY CONSULTING",
      "THE CRITICAL THINKER'S JOURNEY",
      "ORDER SUMMARY",
      "",
      "Order ID: " + state.orderId,
      "Product: " + product.title,
      "Amount: " + formatMoney(product.price),
      "Payment method: " + method.label,
      "Merchant: " + method.merchant,
      "Customer email: " + state.customerEmail,
      "Transaction/reference: " + state.transactionReference,
      "Status: PAYMENT_SUBMITTED - merchant verification required",
      "",
      "Customer-submitted payment details do not equal verified payment.",
      "Access follows merchant-side verification."
    ].join("\n");

    const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = (state.orderId || "ctj-order") + "-summary.txt";
    link.click();
    URL.revokeObjectURL(url);
  }

  function configureResizeReporting() {
    const parentOrigin = document.querySelector('meta[name="ctj-parent-origin"]')?.content?.trim();
    if (!parentOrigin || !window.parent || window.parent === window) return;

    const report = () => {
      window.parent.postMessage(
        { type: "CTJ_WIDGET_HEIGHT", version: 1, height: document.documentElement.scrollHeight },
        parentOrigin
      );
    };

    if ("ResizeObserver" in window) {
      const observer = new ResizeObserver(report);
      observer.observe(document.body);
    }
    window.addEventListener("load", report);
    report();
  }
})();
