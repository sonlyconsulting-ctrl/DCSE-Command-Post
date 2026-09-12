(() => {
  "use strict";

  const STORAGE_KEY = "ctj.commercial.order.v1";
  const CART_KEY = "ctj.commercial.cart.v1";
  const catalog = window.CTJ_CATALOG;
  const productIndex = new Map(catalog.products.map((product) => [product.id, product]));

  const state = loadState();
  let cart = loadCart();
  let activeFilter = "ALL";

  const els = {
    catalog: document.getElementById("catalog"),
    cartDrawer: document.getElementById("cartDrawer"),
    cartScrim: document.getElementById("cartScrim"),
    cartItems: document.getElementById("cartItems"),
    cartAdvice: document.getElementById("cartAdvice"),
    cartTotal: document.getElementById("cartTotal"),
    cartCountTop: document.getElementById("cartCountTop"),
    cartCountSection: document.getElementById("cartCountSection"),
    openCartTop: document.getElementById("openCartTop"),
    openCartSection: document.getElementById("openCartSection"),
    heroCart: document.getElementById("heroCart"),
    closeCart: document.getElementById("closeCart"),
    clearCart: document.getElementById("clearCart"),
    checkoutFromCart: document.getElementById("checkoutFromCart"),
    checkout: document.getElementById("checkout"),
    closeCheckout: document.getElementById("closeCheckout"),
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
  renderCart();
  attachEvents();
  configureResizeReporting();

  function freshState() {
    return {
      version: 2,
      orderId: null,
      cartIds: [],
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
      if (!parsed || typeof parsed !== "object") return freshState();
      if (parsed.version === 1 && parsed.productId) {
        return { ...freshState(), cartIds: [parsed.productId], customerEmail: parsed.customerEmail || "" };
      }
      return { ...freshState(), ...parsed };
    } catch {
      return freshState();
    }
  }

  function loadCart() {
    try {
      const parsed = JSON.parse(localStorage.getItem(CART_KEY) || "[]");
      return Array.isArray(parsed) ? parsed.filter((id) => productIndex.has(id)) : [];
    } catch {
      return [];
    }
  }

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch {
      showStatus("Your browser could not save this order locally. Keep the order summary before leaving this page.", "error");
    }
  }

  function saveCart() {
    try {
      localStorage.setItem(CART_KEY, JSON.stringify(cart));
    } catch {
      // Cart still works in memory for this session.
    }
  }

  function clearState() {
    Object.assign(state, freshState());
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch {
      // In-memory reset still succeeds.
    }
  }

  function renderCatalog() {
    els.catalog.textContent = "";
    const visible = catalog.products.filter((product) => activeFilter === "ALL" || product.filterRole === activeFilter);

    for (const product of visible) {
      const card = document.createElement("article");
      card.className = "product-card" + (product.id === "intro-trio" || product.id === "complete" ? " featured" : "");
      card.setAttribute("data-product-id", product.id);

      if (product.badge) appendText(card, "span", "badge", product.badge);
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
      actions.className = "card-action-row actions";

      const add = document.createElement("button");
      add.type = "button";
      add.className = "button button-primary" + (cart.includes(product.id) ? " in-cart" : "");
      add.textContent = cart.includes(product.id) ? "In cart" : "Add to cart";
      add.setAttribute("data-add-product", product.id);
      add.setAttribute("aria-label", (cart.includes(product.id) ? "Remove " : "Add ") + product.title + (cart.includes(product.id) ? " from cart" : " to cart"));
      actions.appendChild(add);

      const buyNow = document.createElement("button");
      buyNow.type = "button";
      buyNow.className = "button button-quiet";
      buyNow.textContent = "Buy now";
      buyNow.setAttribute("data-buy-now", product.id);
      actions.appendChild(buyNow);

      card.appendChild(actions);
      els.catalog.appendChild(card);
    }
  }

  function renderCart() {
    els.cartItems.textContent = "";
    const items = cart.map((id) => productIndex.get(id)).filter(Boolean);

    if (!items.length) {
      appendText(els.cartItems, "p", "field-help", "Your cart is empty. Select one or more CTJ products to build your path.");
    } else {
      for (const product of items) {
        const line = document.createElement("article");
        line.className = "cart-line";

        const copy = document.createElement("div");
        appendText(copy, "h3", "", product.title);
        appendText(copy, "p", "", product.role);
        const remove = document.createElement("button");
        remove.type = "button";
        remove.className = "remove-item";
        remove.textContent = "Remove";
        remove.setAttribute("data-remove-product", product.id);
        copy.appendChild(remove);

        line.appendChild(copy);
        appendText(line, "strong", "", formatMoney(product.price));
        els.cartItems.appendChild(line);
      }
    }

    els.cartTotal.textContent = formatMoney(cartTotal());
    els.cartCountTop.textContent = String(cart.length);
    els.cartCountSection.textContent = String(cart.length);
    els.checkoutFromCart.disabled = !cart.length;
    els.clearCart.disabled = !cart.length;
    renderCartAdvice();
  }

  function renderCartAdvice() {
    els.cartAdvice.textContent = "";

    const has = (id) => cart.includes(id);
    if (has("complete")) {
      els.cartAdvice.textContent = "The Complete Keeper Collection already contains the current CTJ product family. Review duplicate items before checkout.";
      return;
    }

    if (has("sca") && has("focus-flow") && has("mental-ingenuity")) {
      els.cartAdvice.textContent = "First-time customers may prefer the $45 CTJ Intro Trio instead of these three $20 products. Eligibility remains a separate verification rule.";
      return;
    }

    if (has("focus-flow") && has("mental-ingenuity")) {
      els.cartAdvice.textContent = "The $30 Focus & Flow + Mental Ingenuity pair saves $10 versus these two individual products.";
      return;
    }

    if (has("part-1") && has("part-2") && has("part-3")) {
      els.cartAdvice.textContent = "The $99 Parts 1-3 Collection saves $18 versus the three individual modules.";
      return;
    }

    els.cartAdvice.textContent = "Mix standalone products and bundles as needed. Cart pricing does not silently substitute one product for another.";
  }

  function attachEvents() {
    document.addEventListener("click", (event) => {
      const addTarget = event.target.closest("[data-add-product]");
      if (addTarget) {
        toggleCart(addTarget.getAttribute("data-add-product"));
        return;
      }

      const buyNow = event.target.closest("[data-buy-now]");
      if (buyNow) {
        cart = [buyNow.getAttribute("data-buy-now")];
        saveCart();
        renderCart();
        beginOrderFromCart();
        return;
      }

      const remove = event.target.closest("[data-remove-product]");
      if (remove) {
        cart = cart.filter((id) => id !== remove.getAttribute("data-remove-product"));
        saveCart();
        renderCart();
        renderCatalog();
        return;
      }

      const filter = event.target.closest("[data-filter]");
      if (filter) {
        activeFilter = filter.getAttribute("data-filter");
        document.querySelectorAll("[data-filter]").forEach((button) => button.classList.toggle("active", button === filter));
        renderCatalog();
      }
    });

    [els.openCartTop, els.openCartSection, els.heroCart].forEach((button) => {
      if (button) button.addEventListener("click", openCart);
    });

    els.closeCart.addEventListener("click", closeCart);
    els.cartScrim.addEventListener("click", closeCart);

    els.clearCart.addEventListener("click", () => {
      cart = [];
      saveCart();
      renderCart();
      renderCatalog();
    });

    els.checkoutFromCart.addEventListener("click", beginOrderFromCart);

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
    });

    els.downloadSummary.addEventListener("click", downloadOrderSummary);

    els.startOver.addEventListener("click", () => {
      clearState();
      cart = [];
      saveCart();
      els.checkout.hidden = true;
      renderCart();
      renderCatalog();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  function toggleCart(productId) {
    if (!productIndex.has(productId)) return;
    cart = cart.includes(productId) ? cart.filter((id) => id !== productId) : [...cart, productId];
    saveCart();
    renderCart();
    renderCatalog();
  }

  function openCart() {
    els.cartDrawer.classList.add("open");
    els.cartDrawer.setAttribute("aria-hidden", "false");
    els.cartScrim.hidden = false;
    els.closeCart.focus();
  }

  function closeCart() {
    els.cartDrawer.classList.remove("open");
    els.cartDrawer.setAttribute("aria-hidden", "true");
    els.cartScrim.hidden = true;
  }

  function beginOrderFromCart() {
    const items = cart.map((id) => productIndex.get(id)).filter(Boolean);
    if (!items.length) return;

    clearState();
    state.orderId = createOrderId();
    state.cartIds = [...cart];
    state.orderStatus = "ORDER_INTENT";
    state.createdAt = new Date().toISOString();
    saveState();

    resetCheckoutView();
    renderOrderProducts(items);
    els.customerEmail.value = "";
    closeCart();
    els.checkout.hidden = false;
    showStatus("Order intent created. No payment has been recorded yet.", "info");
    els.customerEmail.focus();
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

  function renderOrderProducts(items) {
    els.orderProduct.textContent = "";
    const list = document.createElement("div");
    list.className = "order-list";

    for (const product of items) {
      const line = document.createElement("div");
      line.className = "order-line";
      const text = document.createElement("div");
      appendText(text, "strong", "", product.title);
      appendText(text, "p", "field-help", product.role);
      line.appendChild(text);
      appendText(line, "strong", "", formatMoney(product.price));
      list.appendChild(line);
    }

    els.orderProduct.appendChild(list);
    const total = document.createElement("div");
    total.className = "order-total";
    appendText(total, "span", "", "Order " + state.orderId + " total");
    appendText(total, "strong", "", formatMoney(orderTotal()));
    els.orderProduct.appendChild(total);
  }

  function showPaymentStep() {
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

    showStatus("Amount due: " + formatMoney(orderTotal()) + ". Payment is completed outside this page.", "info");
  }

  function selectPaymentMethod(methodId) {
    const method = catalog.paymentMethods.find((item) => item.id === methodId);
    if (!method) return;

    state.paymentMethodId = methodId;
    state.orderStatus = "PAYMENT_PENDING";
    saveState();

    els.paymentInstructions.textContent = "";
    appendText(els.paymentInstructions, "p", "eyebrow", method.label.toUpperCase());
    appendCopyLine(els.paymentInstructions, "Pay to", method.merchant);
    appendCopyLine(els.paymentInstructions, "Amount", formatMoney(orderTotal()));
    appendCopyLine(els.paymentInstructions, "Order ID", state.orderId);
    appendText(els.paymentInstructions, "p", "field-help", "Use the order ID in the payment note when the provider permits it. No provider destination link is shown until it is verified.");
    els.paymentInstructions.hidden = false;
    els.stepSubmission.hidden = false;
    els.payerIdentity.focus();
    showStatus(method.label + " selected. Complete payment externally, then return with the transaction/reference ID.", "info");
  }

  function showPendingStep() {
    const method = catalog.paymentMethods.find((item) => item.id === state.paymentMethodId);
    if (!method) return;

    els.stepProduct.hidden = true;
    els.stepPayment.hidden = true;
    els.stepSubmission.hidden = true;
    els.stepPending.hidden = false;
    els.pendingSummary.textContent = "";

    addSummary("Order ID", state.orderId);
    addSummary("Products", orderItems().map((product) => product.title).join("; "));
    addSummary("Amount", formatMoney(orderTotal()));
    addSummary("Payment method", method.label);
    addSummary("Merchant", method.merchant);
    addSummary("Email", state.customerEmail);
    addSummary("Transaction/reference", state.transactionReference);
    addSummary("Status", "PAYMENT_SUBMITTED - merchant verification required");

    showStatus("Payment details submitted. This is not yet a verified paid order.", "success");
  }

  function orderItems() {
    return state.cartIds.map((id) => productIndex.get(id)).filter(Boolean);
  }

  function cartTotal() {
    return cart.reduce((sum, id) => sum + (productIndex.get(id)?.price || 0), 0);
  }

  function orderTotal() {
    return orderItems().reduce((sum, product) => sum + product.price, 0);
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
    const method = catalog.paymentMethods.find((item) => item.id === state.paymentMethodId);
    if (!method) return;

    const lines = [
      "SONLY CONSULTING",
      "THE CRITICAL THINKER'S JOURNEY",
      "ORDER SUMMARY",
      "",
      "Order ID: " + state.orderId,
      ...orderItems().map((product) => product.title + ": " + formatMoney(product.price)),
      "Total: " + formatMoney(orderTotal()),
      "Payment method: " + method.label,
      "Merchant: " + method.merchant,
      "Customer email: " + state.customerEmail,
      "Transaction/reference: " + state.transactionReference,
      "Status: PAYMENT_SUBMITTED - merchant verification required",
      "",
      "Customer-submitted payment details do not equal verified payment.",
      "Access follows merchant-side verification."
    ];

    const blob = new Blob([lines.join("\n")], { type: "text/plain;charset=utf-8" });
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
